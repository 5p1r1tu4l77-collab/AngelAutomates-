# Make.com playbook — squeezing the free tier for token-free glue

## The constraint (verified May 2026)

Make.com free plan:
- **1,000 operations/month** (an "operation" = one module execution; a typical scenario run uses 3–8 ops)
- **Max 2 active scenarios**
- **15-minute minimum interval** between scenario runs
- **5-minute max execution time** per run
- **No API access** — paid Core plan ($9/mo) is required to create scenarios programmatically

So **I cannot build scenarios on your account remotely**. But the free 2-scenario / 1k-ops budget is enough to handle the two highest-leverage non-LLM glue tasks. Step-by-step recipes below.

Why this matters: every operation Make handles is one we don't pay for in LLM tokens. This is the "use less tokens" play — let dumb glue do the dumb glue.

## Recipe 1: Gmail → GitHub repository_dispatch (when a cold-email reply lands)

**Why this is high-leverage:** turns a poll-style reply check (currently the `reply-triage` agent every 15 min, which costs LLM tokens whether or not there's a reply) into an event-driven trigger that only fires when an actual reply lands. We save ~96 reply-triage runs per day during quiet periods.

**Operations per trigger:** 3 (Gmail watch + Router + GitHub HTTP). At 5 replies/day average = 15 ops/day = 450 ops/month. Half the free budget.

### Build steps in Make.com

1. Click **+ Create a new scenario**.
2. **Trigger:** Search for **Gmail** → choose **Watch Emails**.
   - Connection: connect your Gmail account.
   - Folder: `INBOX`
   - Filter: search query `from:* AND subject:re:* AND newer_than:1d`
   - Limit: 10 (keeps ops low)
   - Schedule: "At regular intervals" → 15 min.
3. **Router:** Add a **Router** module after Gmail (lets you classify by subject pattern).
4. **Filter** (on the route you'll process): add a filter `Subject CONTAINS re:` AND `From DOES NOT CONTAIN noreply` AND `From DOES NOT CONTAIN mailer-daemon`.
5. **Action:** Search for **HTTP** → **Make a request**.
   - URL: `https://api.github.com/repos/5p1r1tu4l77-collab/AngelAutomates-/dispatches`
   - Method: `POST`
   - Headers:
     - `Accept: application/vnd.github+json`
     - `Authorization: Bearer {{your_github_pat}}`
     - `Content-Type: application/json`
   - Body type: Raw JSON
   - Body:
     ```json
     {
       "event_type": "gmail-reply-received",
       "client_payload": {
         "from": "{{1.from.address}}",
         "subject": "{{1.subject}}",
         "snippet": "{{1.snippet}}",
         "thread_id": "{{1.threadId}}",
         "received_at": "{{1.date}}"
       }
     }
     ```
6. **Save & schedule the scenario.**

### GitHub side (already shipped this commit)

Workflow: `.github/workflows/on-gmail-reply.yml` listens for the `gmail-reply-received` repository_dispatch and triggers the `reply-triage` agent with the payload as user-input. **No polling.** No LLM tokens spent on empty checks.

### GitHub PAT note

Create a fine-grained PAT at https://github.com/settings/personal-access-tokens with:
- Repository access: only `5p1r1tu4l77-collab/AngelAutomates-`
- Repository permissions: **Contents: Read and write**, **Metadata: Read-only**
- Expiration: 1 year

Paste into Make's HTTP module Authorization header. Don't commit it anywhere.

## Recipe 2: Cal.com booking → GitHub repository_dispatch (when a discovery call books)

**Why this matters:** the moment a prospect books, we want `sales-ops` to start prepping the kickoff doc + contract. Webhook = instant. Cron poll = up-to-15-minute delay AND wasted ops.

**Operations per trigger:** 2 (webhook trigger + HTTP). At 4 bookings/day average = 8 ops/day = 240 ops/month. Comfortably inside the remaining budget.

### Build steps in Make.com

1. **+ Create a new scenario.**
2. **Trigger:** Search for **Webhooks** → **Custom webhook**.
   - Click **Add** → name it `cal-com-booking` → save. Make gives you a unique URL like `https://hook.eu2.make.com/<id>`. Copy this.
3. In Cal.com → Event Type → Webhooks → Add subscription:
   - URL: paste the Make webhook URL.
   - Subscribe to: `BOOKING_CREATED` and `BOOKING_RESCHEDULED`.
4. Back in Make: with the trigger selected, click **Re-determine data structure** then trigger one test booking from Cal.com so Make learns the payload shape.
5. **Action:** Add another **HTTP** → **Make a request** module.
   - URL: `https://api.github.com/repos/5p1r1tu4l77-collab/AngelAutomates-/dispatches`
   - Method: `POST`
   - Headers: same as Recipe 1 (Bearer GitHub PAT, application/vnd.github+json).
   - Body:
     ```json
     {
       "event_type": "calendar-booking-created",
       "client_payload": {
         "lead_email": "{{1.payload.attendees[0].email}}",
         "lead_name": "{{1.payload.attendees[0].name}}",
         "start_time": "{{1.payload.startTime}}",
         "end_time": "{{1.payload.endTime}}",
         "event_type_slug": "{{1.payload.type}}"
       }
     }
     ```
6. **Save & activate.**

### GitHub side

Workflow: `.github/workflows/on-calcom-booking.yml` listens for `calendar-booking-created`, finds the lead row in `data/pipeline.csv`, marks `stage: scheduled`, and triggers `sales-ops` so the contract template is pre-filled before the human even shows up to the call.

## Operation-budget math

- Recipe 1 worst-case: 30 reply checks/day × 3 ops = 90 ops/day = 2,700 ops/month → **over budget**.
- Recipe 1 realistic: most days you have 0–5 replies; the watcher only triggers when emails arrive. ~450 ops/month.
- Recipe 2: 240 ops/month at steady state.
- Headroom: ~310 ops/month for ad-hoc one-shots.

If you outgrow the budget: either (a) upgrade to Make Core ($9/mo, 10k ops, unlimited scenarios), (b) move to **n8n self-hosted** (free, unlimited, needs a $5/mo VPS or free Oracle Cloud tier), or (c) replace the Make scenarios with the equivalent Cloudflare Worker (free, 100k req/day, no scenario limit) — see `docs/AUTOMATION-LAYER.md`.

## What this saves

Without these scenarios, the `reply-triage` and `appointment-setter` agents poll on cron every 15 min, **regardless** of whether there's anything to do. That's:
- 96 reply-triage runs/day × 1.5k tokens × $0 (free LLM tier) = $0 cost but 96 wasted runs / day on the free LLM rate limit.
- Same for appointment-setter.

With these scenarios:
- Agents only run when there's a real event.
- Free LLM rate-limit headroom doubles.
- Latency from "lead replies" → "draft response ready" drops from up to 15 min to ~30 sec.

This is exactly the "use less tokens" lift you asked for, with the bonus of being faster.

## What I committed alongside

- `automation/make-blueprints/README.md` — quick reference, links to this doc.
- `.github/workflows/on-gmail-reply.yml` — listens for `gmail-reply-received` repository_dispatch.
- `.github/workflows/on-calcom-booking.yml` — listens for `calendar-booking-created`.

You build the Make scenarios; I built the GitHub side that catches them.

## Sources

- [Make.com pricing 2026 — Lindy](https://www.lindy.ai/blog/make-com-pricing)
- [Make.com free plan operation limits — Make Community](https://community.make.com/t/max-number-of-scenarios-operations-in-free-plan/16537)
- [Make API scenarios reference — Make Developer Hub](https://developers.make.com/api-documentation/api-reference/scenarios)
- [n8n vs Make vs Zapier 2026 — Digidop](https://www.digidop.com/blog/n8n-vs-make-vs-zapier)
