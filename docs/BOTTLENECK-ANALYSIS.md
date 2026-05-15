# Bottleneck analysis — what's actually blocking the next dollar

Synthesized 2026-05-15 after web research. Companion to `docs/EXECUTION-PLAN.md`.

## The funnel and who owns each step

| # | Step | Auto / Manual | Blocking? |
|---|------|---------------|-----------|
| 1 | Source 50 leads/day | **Auto** (`scrape_google_maps.py`, free) | No |
| 2 | Find owner emails | **Auto** (`find_email.py`, free) | No |
| 3 | Personalize each lead | Could be auto (copywriter agent) — but agent is **paused** because Anthropic API call ≠ $0 | **YES — this is the bottleneck** |
| 4 | Send cold emails | Could be auto (Brevo SMTP, 300/day free) — needs human to sign up + add `BREVO_SMTP_KEY` | Light |
| 5 | LinkedIn DMs (20/day) | **Manual** — 40% restriction rate makes automation suicidal | Human-only |
| 6 | Triage replies | Could be auto (reply-triage agent) — paused for same reason as #3 | Same as #3 |
| 7 | Book discovery call | Manual click on Cal.com link | Human-only |
| 8 | Run discovery call | **Manual — must be human voice** | Human-only |
| 9 | Close on call | **Manual — must be human** | Human-only |
| 10 | Sign contract + collect payment | Stripe + DocuSign, manual approval | Light |
| 11 | Deliver pilot (5 appts) | Could be auto (pilot-deliverer agent) — paused for same reason | Same as #3 |

**The single biggest blocker**: the agents that do steps 3, 6, 11 are paused because each Anthropic API call adds to `tracker/quota.json` `spend_usd`, which violates the zero-dollar goal's strict "`spend_usd == 0`" criterion.

If those three agents could run for $0, the human bottleneck collapses from "you do everything except sourcing" to "you run calls and sign contracts." That's the difference between 30 hours/week of grind and 5 hours/week.

## The fix: route agents through free-tier LLMs until the $1k clears

Three providers offer production-grade LLMs free, no credit card, in 2026:

| Provider | Model | Daily limit | Speed | Cost |
|----------|-------|-------------|-------|------|
| **Google Gemini 2.5 Flash-Lite** | Flash-Lite | 1,000 RPD, 15 RPM, 250k TPM | Fast | **$0** |
| **Groq Llama 3.3 70B** | Llama 3.3 70B | 1,000 RPD, 30 RPM, 6k TPM | Fastest (315 TPS) | **$0** |
| **OpenRouter free** | Llama 3.3 / DeepSeek / Mistral | varies, 20 RPM | Medium | **$0** |

Our fleet's load estimate (all 20 agents running on schedule):

| Cadence | Calls/day |
|---------|-----------|
| Every 15 min (4 agents) | 96 × 4 = 384 |
| Every 30 min (2 agents) | 48 × 2 = 96 |
| Hourly (3 agents) | 24 × 3 = 72 |
| Every 6 hours (1 agent) | 4 |
| Daily (1 agent) | 1 |
| Weekly (4 agents) | 4 / week |
| Event-driven (5 agents) | ~10 avg |
| **Peak total** | **~570 calls/day** |

That fits inside one free tier (Gemini = 1,000 RPD) with margin. Splitting load 60/40 between Gemini and Groq gives us 2,000 RPD headroom and natural redundancy if one provider rate-limits.

## Quality tradeoff

Gemini 2.5 Flash-Lite ≈ Anthropic Haiku quality. Fine for routing, classification, simple extraction (60% of our calls).

Groq Llama 3.3 70B ≈ between Haiku and Sonnet for writing tasks. Slightly worse than Sonnet on tone/nuance for cold emails, but acceptable for the **drafting** step — the human still approves before sending.

This means: free-tier output goes to `_pending/` for human review (same gate that existed before). The human catches any quality dips. Quality risk is bounded.

Once the $1k lands → switch to Anthropic Sonnet for client-facing copy, keep Gemini for cheap routing. Best of both worlds.

## Privacy tradeoff (honest)

- **Gemini free tier**: per Google's ToS, free-tier inputs/outputs CAN be used to improve their models. For us, drafting public-facing cold emails to people whose names came from public Google Maps listings = **acceptable risk**. Once we have actual client data (contracts, MRR, NPS), we'd switch those calls to paid.
- **Groq free tier**: their current ToS does not use data for training. Better for any data we'd later mark sensitive.
- **OpenRouter free**: depends on the underlying provider; some opt in to training, some don't. Treat as Gemini-equivalent risk.

Strategy: **use Gemini for cold-email drafting + reply classification** (the data here is unavoidably public anyway), **Groq for anything that touches `data/pipeline.csv`** rows after `interested` stage (slightly more sensitive). Document the routing rule in the LLM client.

## What we're committing this turn

- `scripts/llm_client.py` — provider-agnostic LLM call. Routes by env var `LLM_PROVIDER` (defaults to `gemini` when `ANTHROPIC_API_KEY` is unset and `GEMINI_API_KEY` is set; falls back through Groq, OpenRouter, Anthropic).
- `scripts/run_agent.py` — calls into the abstraction instead of Anthropic directly.
- `scripts/guards.py` — treats free providers as `cost_usd = 0` in the quota tracker, so running on Gemini/Groq does NOT trip the zero-dollar gate.
- Workflow secrets to add: `GEMINI_API_KEY` and/or `GROQ_API_KEY` (either or both — system falls back gracefully).
- `docs/BOTTLENECK-ANALYSIS.md` — this file.

After commit, the human's only remaining action to unblock the fleet:

1. Get a Gemini API key from https://aistudio.google.com (5 min, no credit card)
2. Add it as `GEMINI_API_KEY` repo secret
3. Manually trigger one agent workflow to verify

Total time to unblock: 10 minutes. After that, the agent fleet runs end-to-end on the same cron schedule, costing $0, generating leads + drafts + replies on autopilot.

## Sources

- [Gemini API free tier 2026 — TokenMix](https://tokenmix.ai/blog/gemini-api-free-tier-limits)
- [Gemini API rate limits — Google AI for Developers](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Groq free tier limits 2026 — TokenMix](https://tokenmix.ai/blog/groq-free-tier-limits-2026)
- [Groq rate limits — GroqDocs](https://console.groq.com/docs/rate-limits)
- [OpenRouter free models — CostGoat](https://costgoat.com/pricing/openrouter-free-models)
- [Free LLM API tier list 2026 — Mr Computer Science](https://www.mrcomputerscience.com/free-llm-api-tier-list-2026-for-broke-developers/)
