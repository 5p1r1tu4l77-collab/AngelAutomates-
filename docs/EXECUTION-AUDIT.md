# Execution audit — who can do what, what's blocking the next dollar

Built by classifying every revenue-blocking task, then for each one finding the cheapest path to actually executing it. Companion to `docs/BOTTLENECK-ANALYSIS.md`.

Key columns:
- **Who can do it**: human-only (H), scriptable on schedule (S), one-shot via my MCP integrations now (M), or a hybrid (S+H).
- **State**: shipped | scripted-needs-secret | researched-pending-decision | human-only-by-design.
- **Unblock action**: smallest concrete step that flips it green.

## The full audit

| # | Task | Who | State | Unblock action | Source |
|---|------|-----|-------|----------------|--------|
| 1 | Source 50 ICP-matched leads/day | S | shipped | nothing — `scripts/scrape_google_maps.py` runs on cron | this repo |
| 2 | Find owner email per lead | S | shipped | nothing — `scripts/find_email.py` runs after scrape | this repo |
| 3 | Personalize each cold email (~25/day) | S | scripted-needs-secret | add `GEMINI_API_KEY` (free) → unblocks `copywriter` agent | docs/BOTTLENECK-ANALYSIS.md |
| 4 | Send cold emails (~25/day) | S | shipped | add `GMAIL_USER` + `GMAIL_APP_PASSWORD` secrets → `scripts/send_via_gmail.py` runs on cron 4× day | this commit |
| 5 | Send cold emails (~300/day, when scaling) | S | researched-pending-decision | sign up Brevo free, add `BREVO_SMTP_KEY` | docs/EXECUTION-PLAN.md |
| 6 | LinkedIn 20 connection requests/day | H | human-only-by-design | no safe automation in 2026 (40% restriction rate) | docs/EXECUTION-PLAN.md |
| 7 | Personal-network DMs (10/day) | H | human-only-by-design | relationships, not tasks | docs/HUMAN-LOOP.md |
| 8 | Reddit value-give answers (3/day) | H | human-only-by-design | account reputation matters; community sniffs bots | docs/ZERO-DOLLAR-PLAYBOOK.md |
| 9 | Triage inbound replies (categorize, draft response) | M / S | M-ready, S-needs-secret | (M) authorize Gmail MCP for me to read+draft NOW; (S) `reply-triage` agent needs `GEMINI_API_KEY` | this audit |
| 10 | Propose meeting times for interested leads | M / S | M-ready, S-needs-secret | (M) authorize Calendar MCP for me to check availability; (S) `appointment-setter` needs Cal.com API or webhook | this audit |
| 11 | Receive booked-meeting webhook from Cal.com | S | researched-pending-decision | sign up Cal.com free + deploy a Cloudflare Worker (free, 100k req/day) → posts repository_dispatch events | docs/EXECUTION-PLAN.md, this audit |
| 12 | Run discovery call (12 min) | H | human-only-by-design | voice + judgment; AI isn't there yet for trust-building | docs/HUMAN-LOOP.md |
| 13 | Handle objections live | H | human-only-by-design | same as above; `templates/objection-handler.md` arms you with answers | this repo |
| 14 | Sign contract (DocuSign) | H | human-only-by-design | legal authorization can't be delegated to an AI | docs/HUMAN-LOOP.md |
| 15 | Generate Stripe invoice link | S | scripted-needs-secret | add `STRIPE_API_KEY`; `sales-ops` agent generates JSON in `data/stripe_queue/_pending/` for human approval | .claude/agents/sales-ops.md |
| 16 | Post Stripe invoice & charge | S+H | human-approves-script-posts | human approves the JSON → script posts; never auto-charges | .claude/agents/sales-ops.md (audit-fixed) |
| 17 | Receive Stripe payment webhook | S | researched-pending-decision | same Cloudflare Worker as #11; second route | docs/EXECUTION-PLAN.md |
| 18 | Onboard new client (kickoff doc, intake) | M / S | M-ready, S-needs-secret | (M) Notion MCP can create the kickoff doc in their workspace; (S) `sales-ops` agent does it via Gemini | this audit |
| 19 | Daily KPI dashboard | S | scripted-needs-secret | `kpi-tracker` needs LLM key | this repo |
| 20 | Compliance / bounce / blacklist watch | S | scripted-needs-secret | `compliance-monitor` needs LLM key + MXToolbox optional | this repo |
| 21 | Weekly strategy review | S | scripted-needs-secret | `growth-strategist` needs LLM key | this repo |
| 22 | Weekly competitor scan | S | scripted-needs-secret | `competitor-scanner` needs LLM key + WebFetch (which the scripts already have) | this repo |
| 23 | Weekly tool-watch | S | scripted-needs-secret | `ai-tool-watcher` needs LLM key | this repo |
| 24 | Weekly self-improvement PR | S | scripted-needs-secret | `self-improver` needs LLM key + GitHub PR write (already have via GH Actions) | this repo |
| 25 | Bi-weekly niche pivot proposal | S | scripted-needs-secret | `recruiter` needs LLM key | this repo |
| 26 | Case study after pilot | S | scripted-needs-secret | `case-study-writer` event-triggered; needs LLM key | this repo |
| 27 | Referral ask after milestone | S | scripted-needs-secret | `referral-asker` event-triggered; needs LLM key | this repo |
| 28 | Daily inbound content (LinkedIn / X) | S+H | scripted-needs-secret-and-publisher | `content-engine` drafts; you publish (LinkedIn auto-publish has same ban risk) | this repo |
| 29 | Manual pilot delivery | S+H | scripted-needs-secret | `pilot-deliverer` produces daily packages; human sends from Gmail | this repo |
| 30 | Pay yourself / business banking | H | human-only-by-design | KYC requires real human | financial regulation |

## Total accounting

- **Already shipped & runs without further action**: 2 (lead sourcing, email finding)
- **Shipped this commit, needs ONE secret to flip on**: 1 (Gmail send)
- **Already-shipped agents that need the LLM router secret to flip on**: 14 (everything LLM-based)
- **Researched paths that need a one-time signup + integration**: 4 (Brevo / Cal.com / Stripe / Cloudflare Worker)
- **MCP-executable by me right now (with your authorization)**: 4 categories (Gmail draft/triage, Calendar availability, Notion CRM, Supabase DB)
- **Truly human-only by design**: 7 (LinkedIn, network DMs, Reddit, calls, objections, contract sign, banking)

## The MCPs I have authenticated this session

These are connected via the user's Claude Code session. **Not** the agent fleet — these are one-shot actions I can take right now if authorized.

| MCP | Capabilities | What I'd execute |
|-----|--------------|------------------|
| GitHub (already in use) | search, create issues, PRs, push | already pushing every commit |
| Gmail | search threads, list/create labels, create drafts | search inbox for cold-email replies; create drafts for your one-click send |
| Google Calendar | list calendars, list/create/update events, suggest_time | check your weekly availability; create event blocks for discovery calls |
| Notion | create pages, create databases, search, update | spin up a CRM database in your Notion workspace mirroring `data/pipeline.csv` |
| Supabase | create project, run SQL, deploy edge functions | provision a free Postgres for the agent fleet's pipeline state |
| Vercel | list projects, deploy, get logs | deploy a webhook receiver to your Vercel account (free tier) |

## Recommended order of operations (next 24 hours)

If your goal is "first $1k as fast as possible" with $0 spend:

1. **Add `GEMINI_API_KEY`** to repo secrets (free, 5 min). Unblocks 14 LLM agents.
2. **Add `GMAIL_USER` + `GMAIL_APP_PASSWORD`** (free, 5 min). Unblocks the Gmail send workflow.
3. **Authorize me to use Gmail + Calendar MCPs** (this session, 0 min). I draft reply triage + propose meeting times directly into your accounts; you click send.
4. **Sign up for Cal.com free** + paste your booking URL into `data/calendar.txt` (free, 5 min). Then `appointment-setter` agent has a real link.
5. **Run the lead scraper manually once** to get your first 50 leads (free, 10 min). Then approve 25 drafts in `data/drafts/_pending/`.
6. **Send Day 1 of Week 1**. The whole loop is then live.

Total time to live operations: **~45 minutes of your time**.

## Decision needed from you

I can autonomously continue building things that don't touch your personal accounts (Cloudflare Worker code, more open-source repo adaptations, more agent prompts). But the **biggest near-term lift** comes from authorizing the MCP integrations so I can act on your behalf in your real Gmail / Calendar / Notion **right now**.

Each MCP authorization is scoped to one specific action. You decide which to enable. I'll prompt with concrete actions, not blank checks.
