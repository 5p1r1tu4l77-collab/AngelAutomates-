# Status & blockers

Append-only log of agent errors, compliance trips, and human-action-required items. Newest at the bottom.

## 🚨 Action needed — 20 Gmail drafts + Reply Playbook ready

**Two batches of cold-email drafts now sit in your Gmail Drafts folder.** All subjects start with `[VERIFY]` or `[VERIFY-V2]`.

### Tier A — 5 personalized drafts with real owner names (send these first)

These have been enriched: real owner first names in greeting + best-guess direct email. Higher conversion than info@ generic drafts.

| Company | Owner | Subject prefix | Notes |
|---|---|---|---|
| Integris Roofing | **Cody Zegarrundo** (founder) | `[VERIFY-V2] integris pipeline — 1 question` | LinkedIn also shows Michael Thrower as CEO — verify before sending |
| Rose Roofing | **Jonathan Rose** (3rd-gen, took over 2017) | `[VERIFY-V2] jonathan — 3rd-gen rose roofing` | Wife Jessica co-runs |
| Telge Roofing | **Roy Campbell** (owner since 2013) | `[VERIFY-V2] roy — keeping cypress crews booked` | 28k customers, GAF Master Elite |
| Braun's Roofing | **Skeeter Braun** (founder/pres, 1987) | `[VERIFY-V2] skeeter — 46 years + qualified pipeline?` | Skeeter is the real public name |
| Air Innovations | **Troy Behrens** (owner, w/ wife Kelly) | `[VERIFY-V2] troy — pre-summer AC pipeline` | HVAC, Cypress |

**Workflow per V2 draft (~45 sec):**
1. Verify the owner email guess (`firstname@domain.com`). If LinkedIn or BBB shows different, use that. If unsure, replace To: with `info@<domain>` (fall back to V1's address).
2. Replace `[your name]` in signature.
3. Remove `[VERIFY-V2]` from subject.
4. Send.
5. **Delete the V1 [VERIFY] draft for the same company** (don't send both).

### Tier B — 10 generic-greeting drafts (`info@`, "hi there")

The other 10 drafts (State Roofing TX, Texas Storm Group, Delaneys, TSG, Moss, Lone Star, All Star A/C, Smart Air, ASAP Air, Mission AC) still use info@ + "hi there" since I couldn't pin owner names confidently. Send as-is, or skip in this batch and ask me to enrich them next session.

### Tier C — Reply Playbook (new)

📋 **`docs/REPLY-PLAYBOOK.md`** + Notion page: `Reply Playbook — what to do when a prospect responds`.

When a reply comes in:
1. Classify (interested / curious / not-interested / OOO).
2. Paste the prefab reply with these 6 pre-baked time slots (verified open on your calendar):
   - Tue May 19, 11:00 AM CT
   - Wed May 20, 2:00 PM CT
   - Thu May 21, 10:30 AM CT
   - Fri May 22, 1:00 PM CT
   - Tue May 26, 11:00 AM CT
   - Wed May 27, 2:00 PM CT
3. They pick → you create a Google Calendar event with their email + Meet link → Notion card moves to `scheduled`.

Goal: <60 seconds from opening a reply to having a meeting on the books.

### Tracking
- `data/leads-enriched.csv`: 15 rows, owner names filled for the 5 V2 leads.
- Notion `AngelAutomates Pipeline`: 15 cards, Stage=new. Owner-name leads have `Contact` filled. Drag to `contacted` after you send.

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
