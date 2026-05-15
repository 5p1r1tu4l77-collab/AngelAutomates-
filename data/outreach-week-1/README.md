# Week 1 — zero-dollar outreach package

Goal for this week: **5 booked discovery calls** for the $500 pilot offer (roofing). All channels free. All sending done by hand from your existing accounts.

Read `docs/ZERO-DOLLAR-PLAYBOOK.md` first if you haven't. This directory has the daily packages.

## Day-by-day

| Day | Focus | Touches | File |
|-----|-------|---------|------|
| Mon | Personal network + LinkedIn launch | 35 | `day-1-monday.md` |
| Tue | LinkedIn + Reddit + FB group post #1 | 30 | `day-2-tuesday.md` |
| Wed | Gmail cold email burst (25) + LinkedIn 20 | 50 | `day-3-wednesday.md` |
| Thu | Reply-handle + LinkedIn 20 + 1 FB | 30 | `day-4-thursday.md` |
| Fri | Gmail 25 + LinkedIn 20 + book calls | 50 | `day-5-friday.md` |

**Total**: ~195 touches across the week. Realistic reply rate at this personalization level: 4–7%. Expected: 8–13 replies → 4–6 booked calls → 1 close at $500.

## Daily rhythm (90 min/day)

- 8:00–8:30 AM ET: read `tracker/STATUS.md` + the day's package; queue your work.
- 9:00–10:00 AM ET: send LinkedIn DMs + connection requests (one batch, ≤20).
- 10:00–10:30 AM ET: cold emails from Gmail (≤25/day from your real address).
- 12:00–12:15 PM ET: check replies; tag in `data/pipeline.csv`; book any interested into Cal.com.
- 4:00–4:15 PM ET: end-of-day update — log `data/network-touches.csv`, update STATUS.

## Free tools required (sign up before Monday)

- Cal.com free account → public booking link
- LinkedIn (use your real account)
- Gmail (use your real account — separate from anything compliance-sensitive)
- A free Facebook account → join 3 contractor groups (see `data/fb-groups.csv` once you join)
- DocuSign free (3 envelopes/month — enough for first 3 closes)
- Stripe account (free to start; you only pay 2.9% on collected payments)

## What NOT to do this week

- Don't buy any tool. None.
- Don't send more than 25 cold emails/day from Gmail (account flag risk).
- Don't exceed 20 LinkedIn connection requests per 24h.
- Don't post the same message in 2+ FB groups in the same day (cross-post flag).
- Don't run the paid agent fleet. The goal `20260513-0687` enforces $0 spend.

## When you close client #1

1. Update `data/pipeline.csv` row to `closed-won`.
2. Run `/onboard <lead_id>` in this repo.
3. Create `data/pilots/active/<client-slug>.json` (see `.claude/agents/pilot-deliverer.md` for shape).
4. Day 14 deadline starts.
5. When Stripe payment confirms, log to `tracker/decisions.md` AS THE WIN.
6. When MTD revenue ≥ $1k AND `tracker/quota.json` still shows $0 spend → run `/goal complete`.
