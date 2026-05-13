# Zero-dollar playbook — $0 in, $1,000 out

**Active goal**: `20260513-0687` — "Make money using 0 dollars". Completion gate: `tracker/dashboard.md` MTD revenue ≥ $1,000 AND `tracker/quota.json` spend_usd == 0 cumulative.

The full agent fleet in this repo is paused under this constraint (every Anthropic API call adds to spend). This doc is the manual playbook that gets us to first revenue **without spending a cent**, after which we can unlock the paid agents from cash flow.

## Hard rules

1. **No paid services.** No Anthropic API, no Smartlead, no Apollo, no Apify, no paid LinkedIn, no Google Ads, no domain purchases.
2. **No paid tools subscriptions.** Free tiers only.
3. **Stripe is allowed** — it costs nothing until a payment lands (2.9% + 30¢ taken FROM the payment, not paid up-front).
4. **Anthropic free trial credits do NOT count** — if Anthropic gives $5 free, that's $5 of "consumption" tracked in quota.json. Don't run agents.

## Free toolstack

| Need | Free tool |
|------|-----------|
| Send email | Personal Gmail (≤30 cold/day to avoid flag) |
| 1:1 outreach | LinkedIn (20 connections/day free), X DMs, FB Messenger |
| Calendar | Cal.com free tier (15 mins/event unlimited) |
| Payments | Stripe (no monthly fee, only % per txn) |
| Contracts | DocuSign free tier (3 envelopes/mo) — or PandaDoc free |
| Lead research | Google Maps + LinkedIn + company sites (manual) |
| CRM | this repo's `data/pipeline.csv` |
| Drafts | this repo's `data/drafts/` (you write them; no agent) |
| Voice notes / calls | Phone you already own |
| Video on calls | Google Meet (free) |

## The 14-day plan

### Days 1–3 — Outreach (target: 5 booked discovery calls)

**Goal**: 5 booked 15-min discovery calls by end of day 3.

| Channel | Daily target | Notes |
|---------|--------------|-------|
| Personal network DMs | 10/day | Ask: "do you know any roofing/HVAC owners locally?" — warm intros close 10× cold |
| LinkedIn connection requests | 20/day | Free cap. Targeted note referencing their company specifically |
| Facebook contractor groups | 1 post + 5 comments/day | Join "Roofers United", "HVAC Owners Network", local chapters — give value first |
| Reddit (r/Roofing, r/HVAC) | 3 helpful answers/day | Don't pitch. Build a flair. Add link in profile bio. |
| Cold email via Gmail | 25/day | Manually researched from Google Maps. Same playbook as `templates/cold-email.md` but plain text from your real address. |

**Total touches/day**: ~60. Reply rate manually ≈ 5% (personalized + warm channels). 3 booked calls/day is realistic.

### Days 4–7 — Discovery calls + close (target: 1 paying client)

- Run discovery calls per `docs/OFFER.md` script, but **adjust the offer to a manually-deliverable pilot**:
  - $500 for 5 booked qualified appointments delivered in 14 days. No subscription.
  - Money-back if you don't deliver.
  - $500 is below the standard $2k retainer for two reasons: (a) you're doing manual delivery, lower margin; (b) easier first-yes.
- **Stretch**: sell a $1,000 pilot if buyer wants more volume (10 appts). Either way, you hit the $1k criterion in 1–2 closes.

**Closing script tweaks vs OFFER.md**:
- Position the pilot as: "I'm refining a process — you get a discounted pilot, I get a case study with your permission."
- Ask for full $500 / $1k up-front via Stripe link before scheduling the kickoff.
- DocuSign one-page MSA (use a stripped `templates/contract.md`).

### Days 8–14 — Manual delivery (target: hit committed appointment count, get paid)

For each closed client, manually:
1. Build a 100-lead list from Google Maps + LinkedIn (~2 hours).
2. Research and personalize a 1-sentence hook per lead (~3 hours).
3. Send 25 emails/day from your Gmail (5 days × 25 = 125 emails, comfortably under daily spam threshold).
4. Reply to interested leads, propose Cal.com slots manually (~30 min/day).
5. Deliver the 5–10 appointments to the client's calendar via Cal.com invite forwarding.

Total time per client first pilot: ~25–30 hours over 14 days. Hourly: $500/30 = $16.67. Low but the goal is the **case study + cash flow seed**, not the hourly rate.

### Once paid

1. Stripe payout lands → log it in `tracker/dashboard.md` and `tracker/decisions.md`.
2. **Goal is hit**. `/goal complete` archives this objective.
3. Unlock the paid agents:
   - $80 of the $1k buys Smartlead + 3 domains + Anthropic credits.
   - Switch from manual delivery to the agent fleet for client #2 onward.
   - Each subsequent client retains ~85% margin vs ~50% on manual.

## What changes in this repo

- **`tracker/STATUS.md`** — add a banner that the agent fleet is paused under the active goal. (Done in this iteration.)
- **No GitHub Actions workflows are enabled** — they exist in the repo but secrets aren't set, so they exit clean at the orchestrator's "ANTHROPIC_API_KEY missing" check (treat as a kill-switch for now).
- **CSV-based manual pipeline** — you populate `data/leads-new.csv` and `data/drafts/_pending/<id>.md` by hand. The schemas already lock these for the eventual automated cutover.

## Risk acknowledgments

- **Gmail sending limits**: 30/day cold is the realistic limit before Google flags you. Never exceed.
- **LinkedIn weekly limit**: 100 connections/week as of 2026. Don't blow through it.
- **Spam risk**: keep emails short, plain-text, with a real reply address. Never use fake unsubscribe footers (CAN-SPAM applies even to your personal account).
- **Pilot churn**: a manually-delivered pilot can damage reputation if you miss the appointment target. Promise less; target 5 appts when you know you can hit 7.
- **Personal time**: this is a 30-hour, 14-day grind. Block calendar time honestly.

## Why this is realistic, not optimistic

Examples of agencies that hit first $500–$1k with zero spend by week 2 (publicly documented playbooks):
- Daniel Fazio (cold-email playbook): emphasizes personal network + LinkedIn before any tooling.
- Charlie Morgan: started agency with $0, first client from FB group post.
- Multiple r/sweatystartup posts (2024–2025) detailing $0→$5k cycles using only Gmail + Calendly.

The pattern is consistent: **the first client always comes from a free channel**. Tools only help with scaling past client #2.

## Definition of "done" (mirrors goal criteria)

- [ ] First $1,000 collected in Stripe
- [ ] `tracker/quota.json` shows `spend_usd: 0.0` at the time of collection
- [ ] `tracker/decisions.md` has the win logged with date, channel, amount, client (or anonymized)

When all three are true, run `/goal complete`.
