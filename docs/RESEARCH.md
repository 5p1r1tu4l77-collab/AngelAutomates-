# Research dossier — how AI agents work, how AI businesses make money, what tools win

This doc is the single source of strategic knowledge the fleet shares. Every agent can read it; the `growth-strategist`, `recruiter`, and `ai-tool-watcher` agents are responsible for keeping it current.

Last refreshed: 2026-05-13. Refresh cadence: `ai-tool-watcher` weekly, `growth-strategist` monthly full review.

---

## Part 1 — How AI agents actually work (the engineering model)

### The minimum viable agent

An "agent" is a loop:

```
while not done:
    observe(state)         # read inputs, files, recent events
    plan(state, goal)      # decide next action(s)
    act(action)            # call a tool / write a file / send a request
    observe(result)        # ingest the tool result
    if goal_met(state): break
```

In this repo, that loop is realized as: **a system prompt** (in `.claude/agents/<name>.md`) + **an LLM call** (Anthropic API) + **structured outputs** (CSV rows, files in `data/drafts/`) + **a scheduler** (GitHub Actions cron or event triggers).

### The four ingredients

| Ingredient | What it is | Where it lives in this repo |
|------------|------------|----------------------------|
| **Prompt** | Instructions the model treats as ground truth | `.claude/agents/<name>.md` body |
| **Tools** | Functions the model can request (read file, send email, query API) | `scripts/*_client.py` (planned for week 2); for now agents emit structured text the orchestrator interprets |
| **Memory** | State persisted across runs | `data/*.csv`, `tracker/log.jsonl`, `tracker/decisions.md` |
| **Orchestrator** | The runtime that connects model ↔ tools ↔ memory ↔ scheduler | `scripts/run_agent.py` |

### Agent patterns in the wild (2024–2026)

1. **ReAct (Reason + Act)** — interleave thinking and tool calls. Default Anthropic tool-use loop.
2. **Plan-and-execute** — generate a plan up front, execute each step, replan on failure. Our `growth-strategist` follows this.
3. **Multi-agent orchestration** — a router agent picks specialists. Our `task-router` will do this once tasks queue up.
4. **Reflection / self-improvement** — read past runs, propose prompt edits. Our `self-improver` agent.
5. **Tool-call chains** — a stable pipeline (extract → enrich → write → send). Our outbound pipeline (`prospector` → `icp-researcher` → `copywriter` → `outreach-dispatcher`).

### Why most agents fail in production

Public post-mortems from agent companies converge on five failure modes:

1. **No state hygiene** — agents overwrite each other's work or duplicate it. We address this with the CSV-bus convention (PLAYBOOK §Conventions) and per-agent locks.
2. **Cost spiral** — agents in a loop blow through API budgets in hours. Our `guards.py` enforces a monthly cap with a kill-switch carveout.
3. **No human-in-the-loop on the dangerous step** — sending email / making payments / signing contracts without review. Our `_pending/` → `_approved/` directory pattern forces a human pause.
4. **Stale context** — agents act on data from yesterday because they don't observe before acting. Every agent in this repo reads its inputs at start, never assumes.
5. **Hallucinated tool calls** — agent invents a tool that doesn't exist. We use structured-output prompting (agents emit CSV/JSON the orchestrator parses) rather than free-form tool calls when reliability matters.

### How LLMs work (operator-level model)

You don't need a PhD to operate this fleet, but the mental model that helps:

- LLMs are **next-token predictors** trained on huge text corpora. They do not "look things up" at inference time unless you give them a tool that does.
- Their "memory" within a single call is only the messages you pass. Across calls — nothing — unless you persist state externally (we do, in `data/` and `tracker/`).
- **Hallucination is statistical.** It happens most when the prompt asks for specifics the model can't verify. Mitigation: tools (let the model fetch ground truth), structured output (constrain the format), grounding (paste the source data into the prompt).
- **Context window** = the maximum text the model can read at once. For Claude Sonnet 4.6 in this repo, ~200k tokens. We never blow this because each agent reads only its slice of state.
- **Cost** scales with input + output tokens. Haiku ≈ 1/3 of Sonnet ≈ 1/5 of Opus. We route boring work to Haiku.

### Why Claude (vs GPT-4 / Llama / Gemini) here

- Claude's tool-use API is reliable enough for chained pipelines.
- Sonnet is the right cost/quality tradeoff for client-facing copy.
- Haiku handles classification and routing at ~1/3 cost.
- Anthropic has stable rate limits and predictable pricing.
- Same provider for all agents simplifies cost tracking.

This is not religious. If pricing or quality shifts, `ai-tool-watcher` will surface it and `growth-strategist` will run a controlled A/B.

---

## Part 2 — How AI-leveraged businesses actually make money (the business model)

### The seven monetization shapes I see working in 2026

| Shape | Margin | Time-to-revenue | Examples I've observed publicly |
|-------|--------|----------------|--------------------------------|
| **Productized service agency** | 50–80% | 2–4 wk | Lead-gen, content, bookkeeping, SDR-as-a-service. **This is us.** |
| **Custom AI builds (1-off)** | 30–60% | 4–8 wk | "Build us a custom GPT for support" at $5k–$25k. Upsell from agency. |
| **Vertical SaaS** | 70–90% | 6–18 mo | Industry-specific AI tools (legal intake, dental scheduling). |
| **Info products / cohorts** | 80–95% | 1–3 mo | Course on "how to run an AI agency". High refund risk. |
| **Affiliate + content** | 60–90% | 6–12 mo | YouTube + AI tool affiliate links. Slow ramp. |
| **Marketplace / aggregator** | 10–30% | 6–18 mo | Hire-an-AI-agent marketplaces. Two-sided cold start. |
| **Pure prompt-flipping** | varies | 1 wk | Reselling GPT wrappers. Race-to-zero margins. |

We picked productized service agency because it's the fastest path from $0 to $30k MRR for one operator + an agent fleet, and the LTV per client justifies real engineering investment in the fleet.

### What the public $10k+/mo operators are doing

Synthesizing from public playbooks I've seen circulated 2024–2026:

**Charlie Morgan (Imperium Agency, since ~2020):**
- Niche-first thinking: pick a vertical with high LTV and low tech adoption.
- Productize the offer: same delivery for every client. No bespoke work.
- Money-back guarantee on a measurable outcome (appointments, leads, jobs).

**Daniel Fazio (Cold Email Wizard, since ~2020):**
- Volume × personalization wins. AI's job is to make personalization cheap.
- Inbox-warming and deliverability discipline matter more than copy.
- A new agency should hand-deliver the first 5 clients before tooling up.

**Alex Hormozi ($100M Offers):**
- Value equation: (dream outcome × likelihood of success) ÷ (time delay × effort & sacrifice). Optimize each lever.
- Guarantees radically increase conversion.
- Specificity in the offer beats benefits.

**Heriger / various YouTube agency operators:**
- Lifecycle: 0–$10k MRR with manual + Loom-and-link; $10k–$50k MRR with hired SDRs/VAs; $50k+ with proprietary tooling.
- The "tooling moat" matters only after PMF.

**r/sweatystartup and r/SaaS empirical posts:**
- First client typically comes from a free channel (personal network, FB group, Reddit).
- Average time to first $500: 14–30 days for focused operators, never for scattered ones.
- Highest-converting niches in cold outbound 2024–2026: home services, dental/med, accounting firms, e-commerce 3PLs.

### Why "AI agency" failed for most people who tried it

Publicly visible failure patterns:

1. **No niche.** Selling "AI automation" to anyone with a credit card. Closes infrequent, deliverables custom, no compounding.
2. **Product on top of product.** Wrappers around GPT/Make.com with no defensible delivery. Customer cancels in 2 months.
3. **Building before selling.** Spent 3 months building tooling, ran out of cash before client #1.
4. **Vanity automation.** Built everything to be automated, then realized the bottleneck was sales calls — which they hate doing.
5. **Burning compliance.** Got domains blacklisted on day 30 because they sent 500/inbox without warming.

Our fleet design addresses all five: locked niche (roofing), productized offer, manual-first then automation, human-loop on sales calls, dedicated `compliance-monitor` with kill-switch.

---

## Part 3 — The tool landscape (what to use, what to avoid)

Last verified 2026-05-13 by initial dossier write. `ai-tool-watcher` refreshes weekly.

### Cold email infrastructure

| Tool | Cost (entry) | Notes |
|------|-------------|-------|
| **Smartlead.ai** | $39/mo | Default. Multi-inbox warmup, decent UI, API works. |
| Instantly.ai | $37/mo | Comparable. Slightly worse warmup, better unibox. |
| Lemlist | $59/mo | More expensive; video personalization. Overkill for us. |
| Mailshake | $59/mo | Older, slower iteration. Avoid. |
| Apollo "sequences" | bundled | Cheaper if you're already on Apollo; deliverability is weaker. Use only as fallback. |
| SendGrid / Mailgun raw | $20/mo | Build-your-own. Don't — warmup is 70% of the value. |

### Lead data / sourcing

| Tool | Cost | Notes |
|------|------|-------|
| **Apollo.io** | $49/mo basic | Default. ~280M contacts, decent filters, API. |
| Apify (Google Maps scraper) | pay-as-you-go ~$20/mo | Best for hyperlocal niches. |
| LinkedIn Sales Navigator | $99/mo | High quality but limits scraping; pair with PhantomBuster (~$70/mo). |
| Clay.com | $149/mo | Best enrichment + waterfalls. Overkill until tier 3. |
| ZoomInfo | $$$ | Enterprise. Skip. |

### Workflow / glue

| Tool | Cost | Notes |
|------|------|-------|
| **n8n self-hosted** | $0 (host yourself, $5/mo Hetzner VPS) | Default once we scale. Open source. |
| Make.com (Integromat) | $9–29/mo | Easiest to start. Free tier exists. |
| Zapier | $19+/mo | Most expensive. Use only if a unique integration is missing elsewhere. |
| Pipedream | $19/mo | Code-friendly. |

### LLMs

| Provider | Best model (May 2026) | Why we use it |
|----------|----------------------|---------------|
| **Anthropic** | Claude Sonnet 4.6 / Haiku 4.5 / Opus 4.7 | Default. Tool-use reliable, pricing predictable. |
| OpenAI | GPT-5 family | Comparable quality; we don't dual-source yet (operational cost). |
| Google | Gemini 2.x | Long-context strong; weaker tool use. Watch for price drops. |
| Meta (open) | Llama 3.3 70B / 405B | Self-host cost = $$$. Not worth it at our volume. |
| Mistral | Mistral Large 2 | EU-friendly. Niche. |

### Payments / contracts / CRM

| Tool | Cost | Notes |
|------|------|-------|
| **Stripe** | 2.9% + 30¢ per txn | Default. Free to start. |
| **DocuSign free tier** | 0 (3 envelopes/mo) | Default until volume forces upgrade. |
| PandaDoc free tier | 0 | Alternative. |
| HubSpot free CRM | 0 | Skip — we use this repo's CSVs as CRM. Re-evaluate at $30k MRR. |
| ServiceTitan / JobNimbus | $$$ | Client-side. Useful for integrations as upsell. |

### Calendar / scheduling

| Tool | Cost | Notes |
|------|------|-------|
| **Cal.com** | 0 free tier | Default. Open source, embeddable. |
| Calendly | $10/mo | More polished but pay-walled. |
| SavvyCal | $12/mo | Best when you have many team members. |

### Domains / inboxes

| Tool | Cost | Notes |
|------|------|-------|
| **Cloudflare Registrar** | ~$10/yr per domain | Default. At-cost pricing. |
| Porkbun | ~$10/yr | Alternative. |
| Google Workspace | $6/user/mo per inbox | Required for warmup. Cheaper alternatives (Zoho Mail) sometimes cause deliverability issues. |
| Outlook 365 | $6/user/mo | Slightly better deliverability for B2B email in some niches. |

### Comms (page-the-human)

| Tool | Cost | Notes |
|------|------|-------|
| **Twilio** | pay-per-SMS ~$0.0075 | Default. API is rock-solid. |
| Pushover | $5 one-time | Cheapest. |
| Slack incoming webhooks | 0 | Use if you live in Slack. |

### Compliance / deliverability

| Tool | Cost | Notes |
|------|------|-------|
| **MXToolbox** | free for basic; $99/mo for monitoring | Default. Blacklist + DNS health. |
| GlockApps | $79/mo | Inbox-placement tests. Run weekly. |
| Postmark Spam Tester | 0 | One-shot check. |

---

## Part 4 — Decision framework: "is this expense going to make us money?"

Before spending any dollar (API, tool, ad, domain), answer:

1. **What pipeline stage does it unblock?** Sourcing, enrichment, sending, replying, closing, retaining. If it unblocks none, skip.
2. **What's the expected dollar return per dollar spent (rough)?** Document your assumption in `tracker/decisions.md`. If <3×, defer.
3. **Is there a free or cheaper substitute that gets us 80% of the way there?** If yes, use it until the cheaper option becomes the bottleneck.
4. **Can the expense be paid from cash flow vs. capital?** Cash flow = safe. Capital = only if expected return ≥ 5× and recoverable in ≤ 30 days.
5. **Does the expense create a dependency / lock-in?** Annual contracts, proprietary data formats, switching costs — apply skepticism.

Every agent has a `revenue_impact` field. Every paid tool should have a similar manual review.

---

## Part 5 — References and further reading (no URLs fabricated)

Where to keep learning. I'm naming sources I have direct knowledge of from training; verify links by searching the names.

- **Anthropic engineering blog** — best technical resource on building with Claude (tool use patterns, prompt caching, agent loops).
- **OpenAI Cookbook** — same for GPT; many patterns transfer.
- **Daniel Fazio's "Cold Email Wizard" newsletter and YouTube** — the most empirical cold-email playbook 2020–present.
- **Charlie Morgan ("Charlie Morgan Coaching" on YouTube)** — agency-building specifics.
- **Alex Hormozi's "$100M Offers" and "$100M Leads"** — offer construction and lead-gen fundamentals.
- **r/sweatystartup** — empirical posts from small-business owners on what's working.
- **r/SaaS** — software-side perspective.
- **Indie Hackers** — bootstrapped business case studies.
- **Hacker News (HN)** — early signals on tool trends; filter for substance.
- **"Latent Space" podcast (swyx)** — AI tooling deep dives.
- **"AI Engineer" conference talks** — annual snapshot of what production AI looks like.

When in doubt, search a name and find the most-cited piece of work. The `ai-tool-watcher` agent will keep this list trimmed and current.

---

## Part 6 — Open research questions (the team owns these)

Things we don't have firm answers to yet. Each is owned by a specific agent.

| Question | Owner | Decision deadline |
|----------|-------|-------------------|
| Is Sonnet 4.6 or Sonnet 4.7 better for cold-email personalization at our volume? | `ai-tool-watcher` | After 1k emails sent |
| Do dedicated rotating sender domains beat parked-domain alts? | `compliance-monitor` + `growth-strategist` | Month 2 |
| What's the best 2nd-niche given current saturation? | `recruiter` | Bi-weekly |
| Is there a cheaper alternative to Smartlead that holds deliverability? | `ai-tool-watcher` | Tier 2 |
| What's the right pricing model for the AI-build upsell (fixed vs T&M)? | `growth-strategist` | After 3 closes |
| Should we open-source any portion of this fleet as marketing? | `growth-strategist` | Month 6 |
