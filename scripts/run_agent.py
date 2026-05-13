"""Run a scheduled agent: load its prompt, call Anthropic, log the run.

Usage:
    python scripts/run_agent.py <agent_name> [--dry-run]

The agent definition lives at .claude/agents/<agent_name>.md with YAML
frontmatter (model, max_tokens, revenue_impact, allowed_tools). The body is
the system prompt. Tool execution is intentionally minimal here — most
agents emit structured output (CSV rows, drafts, JSON decisions) that other
scripts pick up. Anything requiring real tool use (sending email, calling
Apollo, etc.) is handled by named helpers in scripts/ that the orchestrator
invokes after the model response.

Designed for GitHub Actions cron jobs. Exits 0 on success or graceful skip
(locked, kill-switch tripped, budget exhausted) and non-zero on real error.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
import time
import uuid
from datetime import datetime, timezone

import guards

REPO = pathlib.Path(__file__).resolve().parent.parent
AGENTS = REPO / ".claude" / "agents"
LOG = REPO / "tracker" / "log.jsonl"
STATUS = REPO / "tracker" / "STATUS.md"

DEFAULT_MAX_TOKENS = 1500
DEFAULT_MODEL = "claude-haiku-4-5-20251001"


def parse_agent(name: str) -> tuple[dict, str]:
    path = AGENTS / f"{name}.md"
    if not path.exists():
        raise SystemExit(f"agent not found: {path}")
    raw = path.read_text(encoding="utf-8")
    meta: dict = {}
    body = raw
    if raw.startswith("---\n"):
        end = raw.find("\n---\n", 4)
        if end != -1:
            header = raw[4:end]
            body = raw[end + 5 :]
            for line in header.splitlines():
                if ":" in line:
                    k, _, v = line.partition(":")
                    meta[k.strip()] = v.strip().strip('"')
    return meta, body.strip()


def append_log(entry: dict) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, separators=(",", ":")) + "\n")


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def call_anthropic(model: str, system: str, user: str, max_tokens: int) -> dict:
    """Call the Anthropic API. Imported lazily so DRY_RUN paths need no SDK."""
    from anthropic import Anthropic

    client = Anthropic()
    resp = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
    usage = resp.usage
    cost = guards.estimate_cost(model, usage.input_tokens, usage.output_tokens)
    return {
        "text": text,
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "cost_usd": cost,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("agent")
    p.add_argument("--dry-run", action="store_true", default=os.environ.get("DRY_RUN") == "1")
    p.add_argument("--user-input", default="Begin your scheduled run. Inspect repo state and act per your prompt.")
    args = p.parse_args()

    run_id = f"{int(time.time())}-{uuid.uuid4().hex[:6]}"
    started = now_iso()

    skip = guards.preflight(args.agent)
    if skip:
        append_log({
            "ts": started, "agent": args.agent, "run_id": run_id,
            "status": "skipped", "reason": skip, "revenue_impact": 0,
        })
        print(f"[{args.agent}] skipped: {skip}")
        return 0

    meta, system_prompt = parse_agent(args.agent)
    model = meta.get("model", DEFAULT_MODEL)
    max_tokens = int(meta.get("max_tokens", DEFAULT_MAX_TOKENS))
    revenue_impact = int(meta.get("revenue_impact", 1))

    with guards.lock(args.agent):
        start = time.monotonic()
        try:
            if args.dry_run:
                result = {"text": "[dry-run: model not called]", "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0}
            else:
                result = call_anthropic(model, system_prompt, args.user_input, max_tokens)
        except Exception as e:
            append_log({
                "ts": started, "agent": args.agent, "run_id": run_id,
                "status": "error", "error": str(e)[:500], "revenue_impact": revenue_impact,
            })
            guards.append_status(f"[{args.agent}] error: {e}")
            print(f"[{args.agent}] ERROR: {e}", file=sys.stderr)
            return 2

        duration = round(time.monotonic() - start, 2)
        guards.record_cost(result["cost_usd"])

        out_dir = REPO / "tracker" / "runs" / args.agent
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / f"{run_id}.md").write_text(result["text"], encoding="utf-8")

        append_log({
            "ts": started, "agent": args.agent, "run_id": run_id,
            "status": "ok", "duration_s": duration,
            "model": model,
            "input_tokens": result["input_tokens"], "output_tokens": result["output_tokens"],
            "cost_usd": result["cost_usd"],
            "revenue_impact": revenue_impact,
            "dry_run": args.dry_run,
        })
        print(f"[{args.agent}] ok in {duration}s (${result['cost_usd']:.4f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
