# Human-in-the-loop — what you do every day

This is the operator's manual. Everything not on this list is automated; everything on this list is a leverage point where human judgment outperforms an agent.

## Daily

### 9:00am ET — Standup (10 min)
1. Open `tracker/dashboard.md`. Scan top: sends, replies, bookings, MRR.
2. Open `tracker/STATUS.md`. Anything red? Triage now or assign back to the responsible agent.
3. Glance at `data/pipeline.csv` for any `closed-won` row added overnight. If yes → check that `sales-ops` already drafted the contract.

### 10:00am ET — Draft approvals (15–30 min)
1. `ls data/drafts/_pending/`. For each draft:
   - First 100 emails ever sent: read 100% line-by-line.
   - After that: spot-check 1 in 5.
   - Approve by moving file to `data/drafts/_approved/`.
   - Reject by moving to `data/drafts/_rejected/` and adding a one-line reason at the bottom. The `copywriter` agent reads rejections to improve.

### 3:00pm ET — Discovery calls (30–90 min)
- Calendar shows 0–3 calls at steady state.
- Show up. Run the OFFER.md script. Aim to sign on the call.
- After each call, update `data/pipeline.csv`: stage = `discovery-done` / `closed-won` / `lost`. Add 1-line note.

### Anytime — Reply to Twilio pages
- `kpi-tracker` and `reply-triage` page you on urgency. Respond within the same business day.

## Weekly — Monday 9am ET (30 min)

1. Read `growth-strategist`'s PR from `[experiment]` branch.
2. Either merge (commit to the experiment for the week) or close (with a one-line "why not" comment).
3. Update `tracker/decisions.md` outcome of last week's experiment.

## Weekly — Friday 3pm ET (15 min)

1. Skim `tracker/log.jsonl` for any agent error frequency. Open issues for repeat offenders.
2. Top off domain warming if Smartlead dashboard flags any.
3. Pay outstanding API bills if Anthropic or others sent invoices.

## Bi-weekly — 1st & 15th (15 min)

1. Review `recruiter` proposal if any. Merge new ICP or close.

## Monthly (60 min total)

1. **Compliance review** — `compliance-monitor`'s last 4 weekly reports. Rotate any inbox showing >2% bounce rate.
2. **Pricing review** — sample 10 lost deals. If price was the objection on >4 of them, escalate to growth-strategist as next experiment.
3. **Books** — reconcile Stripe payouts vs MRR in `tracker/dashboard.md`. Pay yourself.

## Never delegated to agents

- Signing contracts (legal exposure).
- Hiring humans (VA, freelancer, employee).
- Talking to a client about a complaint (relationship).
- Changing the OFFER.md or pricing without weighing competitive landscape.
- Anything involving the bank account.

## On-call escalation paths

| Signal | Source | Your action |
|--------|--------|-------------|
| Spam-complaint reply | `reply-triage` SMS | Add domain to suppression list immediately. Investigate sender pattern. |
| Blacklist hit | `compliance-monitor` SMS + `KILL_SWITCH` | Confirm hit on MXToolbox manually. Pause sending. Open domain rotation issue. |
| Payment failed | `kpi-tracker` SMS | Call the client. Don't wait for retry. |
| 0 sends in 8h | `kpi-tracker` SMS | Check `tracker/STATUS.md` for cause. Probably an API key or quota issue. |
