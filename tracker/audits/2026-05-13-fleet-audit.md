# Fleet audit — 2026-05-13

Read-only audit of all 20 agent prompts performed by a subagent. Source: Explore subagent run during PR #4 development.

## Blockers (applied this commit)

1. **`outreach-dispatcher` missing explicit input contract** → added `## Inputs` section pointing at `data/drafts/_approved/`.
2. **`copywriter` / `icp-researcher` apparent race on `leads-enriched.csv`** → clarified non-overlapping status values (`enriched` written by researcher; `drafted` written by copywriter; copywriter only reads `enriched` rows). Added lock annotation.
3. **`appointment-setter` reads `bookings.csv` with unclear semantics** → clarified it is a future Cal.com webhook target; appointment-setter does not currently read or write it.

## High-risk (applied this commit)

1. **`sales-ops` Stripe invoice guard** — separated draft (writes JSON to `data/stripe_queue/`) from live posting (only on human-approved + Stripe webhook).
2. **`reply-triage` `nurture.csv` schema undefined** — added schema and append-only semantics.
3. **`kpi-tracker` could mutate pipeline state** — locked to read-only; only writes to `tracker/dashboard.md` and appends summary line to `tracker/log.jsonl`.
4. **`compliance-monitor` kill-switch atomicity** — switch writes reason directly to `tracker/KILL_SWITCH`; downstream agents check the file itself, not the runs directory.

## Medium (applied where cheap)

- `appointment-setter` switched Sonnet → Haiku (cost saving on routine slot-proposal).
- `content-engine` cadence relaxed to every-other-day + event-driven on new case study landing.
- `network-outreacher` added idempotency check against `data/network-touches.csv`.
- `pilot-deliverer` documented re-read rule for pilot JSON.
- `referral-asker` 90-day idempotency rule.

## Low / polish (deferred)

These are documentation tweaks; queued via `tracker/task-board.md` for the next cycle.

- Add `et` timezone suffix to all `cadence: *-business-hours` strings.
- Document all `data/` subdirectories in PLAYBOOK § Conventions.
- Add `revenue_impact` justification one-liner to each agent's Revenue check section.
- Complete `task-router` routing table with all 20 agents.

## Outcomes to verify after first live run

- No two agents update the same row's `status` within the same window.
- `KILL_SWITCH` causes a verifiable pause on `outreach-dispatcher` within 1 cron cycle.
- `sales-ops` never auto-creates a live Stripe invoice.
