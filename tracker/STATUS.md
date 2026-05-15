# Status & blockers

Append-only log of agent errors, compliance trips, and human-action-required items. Newest at the bottom.

## 🚨 Action needed (15 Gmail drafts ready)

15 personalized cold-email drafts live in your Gmail Drafts folder via Gmail MCP. All subjects start with `[VERIFY]` so you cannot accidentally send before reviewing. Two verticals, both fit the existing ICP:

- **Roofing (10):** State Roofing Texas, Rose Roofing, Texas Storm Group, Delaneys Restoration, TSG Roofing, Moss Roofing Houston, Integris Roofing, Lone Star Roofing, Telge Roofing, Braun's Roofing.
- **HVAC (5):** Air Innovations, All Star A/C, Smart Air, ASAP Air, Mission AC.

Per-draft workflow (~30 sec each):
1. Open the draft in Gmail.
2. **Verify or replace the To: address.** I used `info@<domain>` as a placeholder. Owner email from the company's contact page converts 3–5× better, but `info@` is acceptable for batch one.
3. **Replace `[your name]`** in the signature with your first name.
4. **Remove the `[VERIFY]` prefix** from the subject line.
5. Read the body once. If it sounds right, hit send.

Total: ~10 min for 15 first-touch cold emails. At a 3–5% reply rate on cold, expect 0–1 reply on this batch. The volume target for first booking is 50–100 sends.

Tracking:
- `data/leads-enriched.csv` with status `drafted-via-mcp-session`.
- Notion `AngelAutomates Pipeline` DB, Stage = `new`, Owner = `agent`, Source = `google-maps`. When you send, drag the card to `contacted` in the Pipeline Board view.

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
