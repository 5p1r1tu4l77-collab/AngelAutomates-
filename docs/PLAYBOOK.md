# Operating playbook

The SOPs that the agent fleet collectively follows. If an agent's behavior contradicts this doc, this doc wins — file an issue and fix the agent.

## The pipeline

```
Apollo / Apify
     │  prospector (hourly)
     ▼
data/leads-new.csv          (status: new)
     │  icp-researcher (15-min)
     ▼
data/leads-enriched.csv     (status: enriched)
     │  copywriter (30-min)
     ▼
data/drafts/_pending/       (you approve 10am)
     │  human → _approved/
     ▼
data/drafts/_approved/
     │  outreach-dispatcher (15-min, business hours)
     ▼
Smartlead → inbox of lead
     │  reply lands in Smartlead
     ▼
reply-triage (15-min)
     │  interested →
     ▼
data/pipeline.csv (status: interested)
     │  appointment-setter (15-min)
     ▼
data/pipeline.csv (status: scheduling)
     │  lead picks slot via Cal.com webhook
     ▼
data/bookings.csv
     │  human runs the call
     ▼
data/pipeline.csv (status: closed-won)
     │  sales-ops (30-min, business hours)
     ▼
Stripe invoice + contract + kickoff
     │  Stripe webhook confirms payment
     ▼
data/pipeline.csv (status: onboarded)
```

## Conventions

- **CSV is the bus.** Never store state inside an agent's prompt or run output. State lives in CSVs and JSON files in `data/` and `tracker/`. Agents read and write; the orchestrator commits.
- **One status field per row.** Agents update `status` to claim a row. Race conditions are prevented by the lock + the fact that each pipeline stage's agent only touches its own status values.
- **Drafts are atomic.** A draft file in `_pending/` is the unit. Move atomically between `_pending/`, `_approved/`, `_rejected/`, `_sent/<date>/`.
- **Never delete; archive.** Old leads go to `data/archive/<year>/<month>.csv`. Sales records keep for tax purposes.
- **Idempotency.** Every agent must be safe to re-run within the same window. If the work was already done, the agent should detect and exit clean.

## Naming

- `lead_id` = `<domain-slug>-<first-name-slug>` (lowercase, hyphenated, ASCII only).
- `run_id` = unix-timestamp + 6-char random hex.
- `goal_id` (for the `/goal` command) = `YYYYMMDD-XXXX`.
- `experiment_id` = `<date>-<slug>`, slug ≤ 5 words.

## Budget rules

- Daily soft cap: `MONTHLY_BUDGET_USD / 30`. Past it, only `revenue_impact: 3` agents run.
- Monthly hard cap: `MONTHLY_BUDGET_USD`. Past it, every agent exits clean except `compliance-monitor` and `kpi-tracker`.
- The hard cap exists to prevent runaway spend from a stuck loop.

## Models — which to use when

| Job | Model | Why |
|-----|-------|-----|
| Routing, classification, simple extraction | `claude-haiku-4-5-20251001` | 1/3 the cost; quality is fine. |
| Personalized writing, multi-step reasoning, summarization with judgment | `claude-sonnet-4-6` | The workhorse for client-facing copy. |
| Quarterly strategy / huge corpus review | `claude-opus-4-7` | Reserved. Only `growth-strategist` may opt in, sparingly. |

## Failure modes & recoveries

| Failure | Detection | Recovery |
|---------|-----------|----------|
| Agent times out | GitHub Actions 8-min limit | Lock auto-expires after 10 min; next run picks up |
| Stale lock | lock > 10 min old | preflight ignores it and proceeds |
| Quota exhausted | `quota.json` spend ≥ cap | All non-essential agents exit; alert on dashboard |
| Kill-switch tripped | `tracker/KILL_SWITCH` present | Only compliance + KPI run; human clears manually |
| API key missing | env var absent | Agent errors out; logged; human fixes secret |
| CSV corruption | manual or merge conflict | Restore from previous git commit (everything's tracked) |

## Security

- Secrets live in GitHub Actions secrets, never in the repo.
- `tracker/secrets/` is for local dev only and is gitignored.
- Agents never log API keys (orchestrator scrubs).
- Client data: minimal (no PII beyond business email + name); not subject to HIPAA/GLBA in current niches.

## When to call a human

Agents must page (Twilio SMS + `tracker/STATUS.md` line) when:
- Legal language detected in a reply
- Reply contains "lawsuit", "attorney", "complaint", "BBB", "refund"
- A closed-won client's payment fails twice
- `compliance-monitor` trips the kill-switch
- Any agent errors 3 times in a row in the same hour
