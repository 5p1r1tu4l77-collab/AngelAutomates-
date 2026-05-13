# Status & blockers

Append-only log of agent errors, compliance trips, and human-action-required items. Newest at the bottom.

## 🚧 Active goal constraint (goal 20260513-0687)

**"Make money using 0 dollars"** — paid agent fleet is PAUSED until first $1,000 collected.

- Do NOT enable scheduled workflows (cron triggers exist but secrets are unset → they fail closed).
- Do NOT run `python scripts/run_agent.py <name>` outside of `--dry-run`.
- Manual playbook in `docs/ZERO-DOLLAR-PLAYBOOK.md`. Follow that until goal is `complete`.
- Track every paid temptation here. Each $0 of restraint protects the goal.

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
