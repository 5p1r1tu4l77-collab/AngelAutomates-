# Status & blockers

Append-only log of agent errors, compliance trips, and human-action-required items. Newest at the bottom.

## 🚨 Action needed (Gmail drafts ready)

I drafted 5 personalized cold emails directly into your Gmail Drafts folder via Gmail MCP. They're real Houston-area residential roofing contractors sourced from public search results. Subjects start with `[VERIFY]` so you cannot miss the review step.

For each draft (~30 sec each):
1. Open the draft in Gmail.
2. **Verify or replace the To: address.** I used `info@<domain>` as a placeholder. The contractor's website's contact page has the real owner email; sometimes the info@ is fine.
3. **Replace `[your name]` in the signature** with your first name.
4. Remove the `[VERIFY]` prefix from the subject line.
5. Read the body once. If it sounds right, hit send.

Total: ~5 min for 5 first-touch cold emails. **This is the first revenue-generating action this whole repo has produced.**

Tracking in `data/leads-enriched.csv` with status `drafted-via-mcp-session`. When you send, update to `contacted` and add a row to `data/pipeline.csv` (or wait for me to do it next session).

## 🚧 Active goal constraint (goal 20260513-0687)

**"Make money using 0 dollars"** — paid agent fleet is PAUSED until first $1,000 collected.

- Do NOT enable scheduled workflows (cron triggers exist but secrets are unset → they fail closed).
- Do NOT run `python scripts/run_agent.py <name>` outside of `--dry-run`.
- Manual playbook in `docs/ZERO-DOLLAR-PLAYBOOK.md`. Follow that until goal is `complete`.
- Track every paid temptation here. Each $0 of restraint protects the goal.

## Agent fleet at-a-glance

- **Outbound pipeline (paid, paused)**: `prospector` → `icp-researcher` → `copywriter` → `outreach-dispatcher` → `reply-triage` → `appointment-setter` → `sales-ops`.
- **Always-on (paid, paused)**: `kpi-tracker`, `compliance-monitor`.
- **Inbound + content (paid, paused)**: `content-engine`.
- **Strategy / weekly (paid, paused)**: `growth-strategist`, `recruiter`, `competitor-scanner`, `ai-tool-watcher`, `self-improver`.
- **Zero-dollar mode (active during current goal)**: `network-outreacher`, `pilot-deliverer`, `referral-asker`, `case-study-writer`, `task-router`.
- **Meta**: `task-router` consumes `tracker/task-board.md`; runs every 5 min once secrets land.

See `docs/RESEARCH.md` for the why and `docs/PLAYBOOK.md` for the how.

## Open decisions (human)

- [ ] Confirm primary niche: roofing (recommended) vs HVAC vs solar
- [ ] Pick 3 sending domains (brandable, NOT angelautomates.com)
- [ ] Open Stripe account + add `STRIPE_API_KEY` to GitHub secrets
- [ ] Open DocuSign account
- [ ] Add `ANTHROPIC_API_KEY` to GitHub secrets
- [ ] Open Smartlead account + add `SMARTLEAD_API_KEY`
- [ ] Open Apollo account + add `APOLLO_API_KEY`
- [ ] Form LLC if not yet (single-member, ~$300 in most states)
- [ ] Separate bank account for the business

## Agent events

_(none yet — first agent run will append below)_
