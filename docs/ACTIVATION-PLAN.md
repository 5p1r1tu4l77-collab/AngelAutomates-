# Activation plan — go from "everything is built" to "leads landing in your inbox"

The repo now has 20 agents, 30 workflows, scrapers, senders, the LLM router, the Make.com playbook, and the execution audit. **None of it produces a dollar until secrets are in place.** This doc is the checklist to flip it on, ordered by leverage.

Time-to-first-cold-email: ~45 minutes of your time, end-to-end. Time-to-first-booked-call: 5–10 days from activation.

## Phase 0 — One-time signups (~30 min, all free, do these in order)

| # | Service | URL | Purpose | Get this | Add to repo as |
|---|---------|-----|---------|----------|----------------|
| 1 | Google AI Studio | https://aistudio.google.com/apikey | Free Gemini API for the LLM router | API key (no credit card) | Repo Secret: `GEMINI_API_KEY` |
| 2 | Gmail App Password | https://myaccount.google.com/apppasswords | SMTP auth for cold sending | 16-digit app password | Repo Secrets: `GMAIL_USER` (email), `GMAIL_APP_PASSWORD` (password) |
| 3 | Cal.com | https://cal.com (sign in with Google) | Free booking page | Public booking URL (e.g. `cal.com/your-name/discovery`) | Will use in `data/calendar.txt` and Make scenario |
| 4 | Stripe | https://stripe.com | Collect payment when you close | Account verified, bank linked | Optional now; add `STRIPE_API_KEY` later |
| 5 | (optional) Groq | https://console.groq.com | Backup free LLM provider | API key | Repo Secret: `GROQ_API_KEY` (only for redundancy) |

**Adding repo secrets**: In GitHub → repo settings → Secrets and variables → Actions → "New repository secret". Same for `GMAIL_USER`, `GMAIL_APP_PASSWORD`, `GEMINI_API_KEY`.

## Phase 1 — Smoke-test the loop (~5 min, after Phase 0)

You do this once to verify everything is wired correctly before letting it run on cron.

| # | Action | What it proves |
|---|--------|----------------|
| 1 | Actions tab → "free · lead scrape" → "Run workflow" → query `roofing contractor Houston TX` → submit | Scraper produces real lead rows in `data/leads-new.csv`. ~5 min. |
| 2 | Actions tab → "agent · icp-researcher" → "Run workflow" → submit | LLM router works; rows get personalization line. ~2 min. |
| 3 | Actions tab → "agent · copywriter" → "Run workflow" → submit | Drafts appear in `data/drafts/_pending/`. ~3 min. |
| 4 | Locally: review 1 draft. If it looks good, `git mv data/drafts/_pending/X.md data/drafts/_approved/` and push. | Approval gate works. |
| 5 | Actions tab → "free · gmail send" → "Run workflow" → cap=1, dry_run=true → submit | Gmail sender wires up correctly without actually sending. |
| 6 | Same workflow, dry_run=false, cap=1 | One real cold email leaves your Gmail. Check sent folder. |

If any step fails, the run logs tell you exactly which secret is missing or which CSV row is malformed. Don't proceed to Phase 2 until all 6 pass.

## Phase 2 — Let cron take over (after Phase 1 passes)

Nothing for you to do here except watch.

- **Hourly**: `prospector` pulls fresh leads.
- **Every 15 min**: `icp-researcher` enriches.
- **Every 30 min**: `copywriter` drafts.
- **You**: every morning at 10am ET, review what's in `data/drafts/_pending/` and move good drafts to `_approved/` (initially 100% — drop to spot-checks once you trust the output).
- **4× daily on weekdays**: `free · gmail send` ships the approved drafts.
- **Every 15 min**: `reply-triage` checks for replies (or fires instantly if you build the Make.com scenario).
- **Daily 9am ET**: `kpi-tracker` rewrites `tracker/dashboard.md`.
- **Every 6 hours**: `compliance-monitor` watches bounce/blacklist signals.

## Phase 3 — Wire the event-driven layer (~30 min, optional but recommended)

Build the two Make.com scenarios per `docs/MAKE-COM-PLAYBOOK.md`:

1. Gmail watcher → GitHub `gmail-reply-received` event (10 min)
2. Cal.com webhook → GitHub `calendar-booking-created` event (5 min, after Cal.com signup)

This turns reply-triage and sales-ops from polling agents to instant-response agents, saves Gemini rate-limit headroom, and gets prospects a confirmation reply within 30 seconds instead of up to 15 minutes.

## Phase 4 — Manual outreach in parallel (the human-only channels)

While the scraped + drafted automation is running, also work the channels I cannot automate (per the audit):

- **LinkedIn**: 20 connection requests/day per `data/outreach-week-1/day-1-monday.md`
- **Personal network DMs**: 10/day per same doc
- **Reddit value-give**: 3 answers/day per `data/outreach-week-1/day-2-tuesday.md`
- **FB groups**: 1 post/group/week

Combined volume target for Week 1: ~195 touches → ~4–6 booked calls → 1 close at $500.

## Phase 5 — When first $500 lands

1. Update `tracker/decisions.md` — log the win.
2. Update `data/pipeline.csv` — set the row to `closed-won`.
3. Run `/onboard <lead_id>` (the slash command shipped earlier).
4. Create `data/pilots/active/<client-slug>.json` per `pilot-deliverer` agent's spec.
5. When MTD revenue ≥ $1000 AND `tracker/quota.json spend_usd == 0`, run `/goal complete` to close the zero-dollar goal.
6. After goal closes, you can optionally add `ANTHROPIC_API_KEY` to flip the LLM router to paid Anthropic for the highest-judgment agents (copywriter, growth-strategist).

## Things I can do for you autonomously (if you say go)

These don't cost anything and don't require your signups:

| Action | What it does | Time | Risk |
|--------|--------------|------|------|
| Trigger the scraper now via push event | I can't currently — GitHub MCP doesn't expose workflow_dispatch. You trigger via UI. | — | — |
| Create a Notion CRM database | Mirror `data/pipeline.csv` to your Notion workspace for visual pipeline tracking | 2 min | requires Notion MCP probe |
| Provision a Supabase free Postgres | Replace CSVs with a real DB once you outgrow them (post-Phase 5) | 5 min | requires Supabase MCP |
| Deploy a Cloudflare Worker webhook receiver | Free alternative to Make.com when you outgrow 1k ops/mo | 15 min | needs your Cloudflare token |
| Write more agent prompts | E.g., a customer-success agent for retention | varies | low |
| Adapt SalesGPT patterns | Borrow voice-call handling from open-source repo | 30 min | low |

Tell me which to run.

## Reality check

The bottleneck right now is NOT code. It's **30 minutes of you doing signups and pasting secrets**. Every additional thing I build before you do those 30 minutes is wasted leverage. The activation plan above is the highest-ROI activity in the entire repo.

If you do nothing else for the rest of the week: **do Phase 0 + Phase 1**. That alone produces real cold emails leaving your Gmail, and you start collecting real reply data to learn from.
