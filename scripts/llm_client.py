"""Provider-agnostic LLM client for the agent fleet.

Routes calls through whichever free-tier provider is available. Treats free
providers as zero-cost so they don't trip the zero-dollar goal's quota gate.

Selection order (first usable wins):
  1. LLM_PROVIDER env override (one of: anthropic, gemini, groq, openrouter)
  2. ANTHROPIC_API_KEY → Anthropic (paid; only when goal lets us spend)
  3. GEMINI_API_KEY → Google Gemini free tier
  4. GROQ_API_KEY → Groq free tier
  5. OPENROUTER_API_KEY → OpenRouter free models

Sensitive-data callers (the orchestrator pass `data_class="sensitive"`) skip
Gemini (since its free tier may use inputs for training) and prefer Groq/Anthropic.

Returns a CallResult with the model text plus accounting (cost in USD,
provider name, token counts). The orchestrator writes this verbatim to
tracker/log.jsonl.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from typing import Literal

DataClass = Literal["public", "sensitive"]

# Mapping from logical agent-frontmatter model names to per-provider concrete
# model IDs. The orchestrator passes the logical name; this module picks the
# provider's closest equivalent.
LOGICAL_TO_PROVIDER = {
    "claude-haiku-4-5-20251001": {
        "anthropic": "claude-haiku-4-5-20251001",
        "gemini": "gemini-2.5-flash-lite",
        "groq": "llama-3.1-8b-instant",
        "openrouter": "meta-llama/llama-3.3-70b-instruct:free",
    },
    "claude-sonnet-4-6": {
        "anthropic": "claude-sonnet-4-6",
        "gemini": "gemini-2.5-flash",
        "groq": "llama-3.3-70b-versatile",
        "openrouter": "meta-llama/llama-3.3-70b-instruct:free",
    },
    "claude-opus-4-7": {
        "anthropic": "claude-opus-4-7",
        "gemini": "gemini-2.5-pro",
        "groq": "llama-3.3-70b-versatile",
        "openrouter": "deepseek/deepseek-chat-v3:free",
    },
}

# Pricing $/Mtoken (input, output). 0/0 = free tier.
PRICING = {
    "anthropic:claude-haiku-4-5-20251001": (1.0, 5.0),
    "anthropic:claude-sonnet-4-6": (3.0, 15.0),
    "anthropic:claude-opus-4-7": (15.0, 75.0),
    # All free-tier entries:
    "gemini:gemini-2.5-flash-lite": (0.0, 0.0),
    "gemini:gemini-2.5-flash": (0.0, 0.0),
    "gemini:gemini-2.5-pro": (0.0, 0.0),
    "groq:llama-3.1-8b-instant": (0.0, 0.0),
    "groq:llama-3.3-70b-versatile": (0.0, 0.0),
    "openrouter:meta-llama/llama-3.3-70b-instruct:free": (0.0, 0.0),
    "openrouter:deepseek/deepseek-chat-v3:free": (0.0, 0.0),
}


@dataclass
class CallResult:
    text: str
    provider: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float


def select_provider(data_class: DataClass = "public") -> str:
    override = os.environ.get("LLM_PROVIDER", "").strip().lower()
    if override in {"anthropic", "gemini", "groq", "openrouter"}:
        return override
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"
    # For sensitive data, skip Gemini free tier (uses inputs to improve models).
    if data_class == "sensitive":
        if os.environ.get("GROQ_API_KEY"):
            return "groq"
        if os.environ.get("ANTHROPIC_API_KEY"):
            return "anthropic"
    if os.environ.get("GEMINI_API_KEY"):
        return "gemini"
    if os.environ.get("GROQ_API_KEY"):
        return "groq"
    if os.environ.get("OPENROUTER_API_KEY"):
        return "openrouter"
    raise RuntimeError(
        "no LLM provider configured. Set one of: ANTHROPIC_API_KEY, "
        "GEMINI_API_KEY, GROQ_API_KEY, OPENROUTER_API_KEY."
    )


def estimate_cost(provider: str, model: str, input_tokens: int, output_tokens: int) -> float:
    inp, out = PRICING.get(f"{provider}:{model}", (0.0, 0.0))
    return round((input_tokens * inp + output_tokens * out) / 1_000_000, 6)


def call(
    logical_model: str,
    system: str,
    user: str,
    max_tokens: int,
    data_class: DataClass = "public",
) -> CallResult:
    provider = select_provider(data_class)
    concrete_model = LOGICAL_TO_PROVIDER.get(logical_model, {}).get(provider, logical_model)

    if provider == "anthropic":
        return _call_anthropic(concrete_model, system, user, max_tokens)
    if provider == "gemini":
        return _call_gemini(concrete_model, system, user, max_tokens)
    if provider == "groq":
        return _call_groq(concrete_model, system, user, max_tokens)
    if provider == "openrouter":
        return _call_openrouter(concrete_model, system, user, max_tokens)
    raise RuntimeError(f"unknown provider {provider}")


def _call_anthropic(model: str, system: str, user: str, max_tokens: int) -> CallResult:
    from anthropic import Anthropic

    client = Anthropic()
    resp = client.messages.create(
        model=model, max_tokens=max_tokens, system=system,
        messages=[{"role": "user", "content": user}],
    )
    text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
    in_t, out_t = resp.usage.input_tokens, resp.usage.output_tokens
    return CallResult(text, "anthropic", model, in_t, out_t, estimate_cost("anthropic", model, in_t, out_t))


def _call_gemini(model: str, system: str, user: str, max_tokens: int) -> CallResult:
    """Call Gemini via REST so we don't need a SDK."""
    import httpx

    key = os.environ["GEMINI_API_KEY"]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    body = {
        "system_instruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.7},
    }
    r = httpx.post(url, json=body, timeout=60.0)
    r.raise_for_status()
    data = r.json()
    text = ""
    candidates = data.get("candidates") or []
    if candidates:
        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts)
    usage = data.get("usageMetadata", {})
    in_t = int(usage.get("promptTokenCount", 0))
    out_t = int(usage.get("candidatesTokenCount", 0))
    return CallResult(text, "gemini", model, in_t, out_t, 0.0)


def _call_groq(model: str, system: str, user: str, max_tokens: int) -> CallResult:
    """Call Groq via OpenAI-compatible REST."""
    import httpx

    key = os.environ["GROQ_API_KEY"]
    r = httpx.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        },
        timeout=60.0,
    )
    r.raise_for_status()
    data = r.json()
    text = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})
    in_t = int(usage.get("prompt_tokens", 0))
    out_t = int(usage.get("completion_tokens", 0))
    return CallResult(text, "groq", model, in_t, out_t, 0.0)


def _call_openrouter(model: str, system: str, user: str, max_tokens: int) -> CallResult:
    """Call OpenRouter via OpenAI-compatible REST."""
    import httpx

    key = os.environ["OPENROUTER_API_KEY"]
    r = httpx.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/5p1r1tu4l77-collab/AngelAutomates-",
            "X-Title": "AngelAutomates",
        },
        json={
            "model": model,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        },
        timeout=60.0,
    )
    r.raise_for_status()
    data = r.json()
    text = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})
    in_t = int(usage.get("prompt_tokens", 0))
    out_t = int(usage.get("completion_tokens", 0))
    return CallResult(text, "openrouter", model, in_t, out_t, 0.0)


if __name__ == "__main__":
    # CLI smoke test: python scripts/llm_client.py "say hello"
    if len(sys.argv) < 2:
        print("usage: python scripts/llm_client.py '<prompt>'", file=sys.stderr)
        raise SystemExit(2)
    r = call("claude-haiku-4-5-20251001", "You are helpful.", sys.argv[1], 200)
    print(json.dumps({"provider": r.provider, "model": r.model, "text": r.text, "cost_usd": r.cost_usd}, indent=2))
