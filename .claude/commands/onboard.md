---
description: "Run the new-client onboarding sequence for a closed-won deal"
argument-hint: "<lead_id>"
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
---

# /onboard

Onboard a new client whose deal was just marked `closed-won` in `data/pipeline.csv`.

## Argument

`$ARGUMENTS` is the `lead_id`. Required. If empty, print usage and stop.

## Steps

1. Look up the row in `data/pipeline.csv`. If not found or stage != `closed-won`, ask via `AskUserQuestion` whether to proceed anyway.
2. Run the same logic as the `sales-ops` agent (see `.claude/agents/sales-ops.md`):
   - Generate contract from `templates/contract.md` → `data/contracts/<lead_id>.md`. Ask the human for any missing fields (`{{fee_usd}}`, `{{term_months}}`, `{{monthly_appts}}`, `{{niche}}`).
   - Draft kickoff email → `data/drafts/_pending/<lead_id>-kickoff.md`.
   - Draft onboarding doc → `data/clients/<client_slug>/kickoff.md` (create directory).
   - Append Stripe invoice request → `data/stripe_queue/<lead_id>.json` (create dir if missing). DO NOT call Stripe — human reviews first.
3. Print a checklist for the human:
   ```
   ✅ Contract drafted: data/contracts/<lead_id>.md
   ⬜ Send via DocuSign (manual)
   ⬜ Create Stripe invoice (manual review queue: data/stripe_queue/<lead_id>.json)
   ⬜ Schedule kickoff call
   ⬜ Mark `onboarded_at` in pipeline.csv after Stripe webhook fires
   ```
4. Update `tracker/STATUS.md` with the new client + outstanding items.

## Revenue note

A clean onboarding is the difference between churn at month 2 and 12-month retention. Don't rush this; ask the human if anything in the template is stale.
