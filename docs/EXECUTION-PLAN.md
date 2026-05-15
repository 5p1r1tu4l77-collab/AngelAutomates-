# Execution plan — what I can actually do for you, $0 in

Synthesized from real research run 2026-05-13 (sources at bottom). The previous plan documented what to do; this doc commits scripts that **do it on a schedule**, plus a clear line where manual action by you starts.

## TL;DR

I can automate three pieces of the funnel for $0:

1. **Lead sourcing**: a Playwright scraper hits Google Maps anonymously and pulls 50 roofing-contractor records per run into `data/leads-new.csv`. Runs on GitHub Actions free tier, no API key needed.
2. **Email finding**: a follow-up scraper opens each lead's website and extracts owner email candidates (footer, contact page, mailto links). No paid tool — uses public DOM.
3. **Email sending via Brevo free SMTP**: 300/day permanent free tier (vs Gmail's 25/day cold ceiling). Once you create a Brevo account and add one secret, the `outreach-dispatcher` agent can send without burning your personal Gmail or paying anyone.

I **cannot** safely automate, even for $0:

- LinkedIn DMs / connection requests. 40% of automated accounts got restricted Jan–Mar 2026 ([source](https://www.joinvalley.co/blog/linkedin-automation-safety-2026)). Manual only.
- Personal-network DMs (relationships, not tasks).
- Discovery calls. You take them.
- Contract signing. You sign.

That means: **scrapers + sending = automated; LinkedIn + relationships + calls + closes = manual.** The plan is realistic.

## The honest division of labor

| Step | Today (manual) | After this commit (automated) |
|------|----------------|-------------------------------|
| Find 25 roofing contractors with email | 90 min manually on Google Maps | 5 min: trigger workflow, get CSV |
| Personalize email per lead | Manual | Manual (`copywriter` agent generates, you review) |
| Send emails | Personal Gmail (25/day cap) | Brevo SMTP (300/day cap, dedicated for outreach) |
| LinkedIn outreach | Manual | Manual (no safe automation exists) |
| Reply triage | Manual | `reply-triage` agent classifies + drafts (still paused under zero-dollar goal until first $1k) |
| Book call | Manual via Cal.com link | Manual (lead clicks, you show up) |
| Run call + close | You | You |
| Onboard | Manual | `sales-ops` agent (paused) |
| Deliver pilot | Manual via Gmail | Manual via Gmail (until goal clears, then Brevo) |

## What changes for the zero-dollar goal

The earlier playbook said "Gmail 25/day, no agents, fully manual." That stays valid as a fallback, but with Brevo's free 300/day tier and free scraping, **the agents themselves can run without violating the zero-dollar constraint** — they cost only Anthropic API spend, which we keep at $0 by running them in `DRY_RUN=1` mode that emits CSVs/drafts but doesn't call the API.

That means:
- The scraper produces real lead lists for you to manually review.
- You manually write the first 25 personalized emails (or use the existing Day-1 template).
- Brevo sends them — free, dedicated infrastructure, doesn't touch your Gmail reputation.
- You handle LinkedIn / replies / calls manually.

We hit $1k without spending. Then we flip `DRY_RUN=0` and the Claude agents start handling enrichment + drafting at scale.

## Free toolstack (verified May 2026)

| Need | Tool | Free tier | Sign-up time |
|------|------|-----------|--------------|
| Lead sourcing | Google Maps via Playwright (this repo) | Unlimited (anonymous scraping is legal in the US; rate-limited internally) | 0 |
| Lead sourcing #2 | Apollo.io Chrome extension | 50 credits/mo (CSV export possible) | 5 min |
| Lead sourcing #3 | LeadGenHub (live Google Maps query) | Free tier, low daily caps | 5 min |
| Email finder | Hunter.io | 50 credits/mo (find + verify combined) | 3 min |
| Email finder #2 | Apollo.io free | 50–10,000 credits/mo (varies by signup date) | already above |
| Email sending | Brevo SMTP | 300/day permanent (9,000/mo) | 10 min |
| Email sending alt | Mailtrap | 4,000/mo permanent | 10 min |
| Email sending alt | Resend | 3,000/mo permanent | 10 min |
| Calendar | Cal.com | Unlimited 15-min events | 5 min |
| Contracts | DocuSign free | 3 envelopes/mo | 5 min |
| Payments | Stripe | 2.9% + 30¢ only on collected $ | 15 min |
| Hosting / cron | GitHub Actions | 2,000 min/mo (we use ~10/day) | already have |
| Local browser automation | Playwright | Open source, free | 0 |

**Total monthly cost if you sign up for all of this and stay within tiers**: $0.

## What lands in this commit

- `scripts/scrape_google_maps.py` — anonymous Playwright scraper, pulls business name, address, phone, website, category, rating, review count from Google Maps for a given query (city + "roofing contractor"). Writes new rows to `data/leads-new.csv`. Respects internal rate limit (max 50 results/run, 1.5–4s human-like delays between actions).
- `scripts/find_email.py` — for each `data/leads-new.csv` row without `email`, opens the website, scans `/contact`, `/about`, `/team`, `mailto:` links, and writes back the best-guess owner email + confidence score. Skips after 2 fetches per lead to limit footprint.
- `.github/workflows/free-lead-scrape.yml` — cron + manual `workflow_dispatch` to run the scraper with a configurable query.
- `scripts/requirements.txt` — adds `playwright`, `beautifulsoup4`, `httpx`.
- `docs/EXECUTION-PLAN.md` — this file.

The scrapers are configured to **never log a Google account in** (terminates ToS-blast risk to your real Gmail) and to behave humanly enough to avoid IP blocks at our volume.

## Legal status (US, business owners)

- Public business contact data on Google Maps = legal to scrape (hiQ v. LinkedIn, Meta v. Bright Data, X Corp v. Bright Data — all confirmed in federal court).
- Google's ToS prohibits scraping, but ToS isn't law; the consequence is account suspension, not legal action.
- We mitigate by **never logging in** while scraping. GitHub Actions IPs are not tied to your personal accounts.
- Reading `mailto:` links and parsing `/contact` pages on public websites = no ToS issue (you're browsing).
- Cold email itself is governed by CAN-SPAM (US): requires accurate sender info, real reply address, working unsubscribe, no deceptive subjects. We comply in every template.

If you operate from the EU/UK or your prospects are there, **stop** and we'll add GDPR-aware paths. Not currently in scope.

## Your action items (one-time, ~45 min)

In this order:

1. **Sign up for Brevo** (10 min): https://www.brevo.com — free plan, verify a sending domain or use their `transactional@<your_account>.brevo.com` default. Get your SMTP key.
2. **Add `BREVO_SMTP_KEY` to GitHub repo secrets** (3 min): Settings → Secrets and variables → Actions → New repository secret.
3. **Sign up for Cal.com** (5 min): https://cal.com — set up a 15-min discovery-call event.
4. **Sign up for Stripe** (15 min): https://stripe.com — connect a bank account so paid pilots land directly.
5. **Optionally**: Apollo + Hunter free accounts (5 min each) — gives a Chrome-extension fallback when the scraper misses an email.

That's it. Nothing in this list costs money. Once steps 1–4 are done, the scraper can run on schedule and produce 50 ICP-matched lead rows per day for you to manually outreach.

## Decision to make

Even with free tools, sending cold email from a **Brevo "shared IP" pool** can hurt deliverability vs Gmail. Two paths:

- **A. Use your personal Gmail for the first 100 sends** (proven deliverability, 25/day ceiling, slow ramp).
- **B. Use Brevo from day 1** (faster scaling to 300/day, but mediocre warm-up since it's a shared pool).

**Recommendation: A for the first week, B from week 2 once you have a case study to lean on.** Stays low-volume, high-personalization. By the time you hit Brevo's tier, you've validated the offer and can justify a $39 Smartlead upgrade (out of the $500 first pilot proceeds).

## Sources

- [Open-source cold email tools (Coldflow, Meteor-emails, Listmonk) — GitHub topics](https://github.com/topics/cold-emails)
- [Gmail sending limits 2026 — Smartlead](https://www.smartlead.ai/blog/gmail-sending-limits)
- [LinkedIn automation safety 2026 — Valley](https://www.joinvalley.co/blog/linkedin-automation-safety-2026)
- [Apollo alternatives for local contractors 2026 — Origami](https://origami.chat/blog/best-lead-generation-tools-for-contractors)
- [Best Apollo alternatives — LeadGenHub blog](https://www.leadgenhub.app/blog/the-best-apollo-io-alternative-for-local-b2b-lead-generation-2026)
- [Hunter.io free tier — Prospeo](https://prospeo.io/s/email-hunter-free)
- [Apollo.io free email finder](https://www.apollo.io/email-finder)
- [Brevo free SMTP tier — Brevo blog](https://www.brevo.com/blog/free-smtp-servers/)
- [Mailtrap, Resend, MailerSend free tiers — emailtooltester](https://www.emailtooltester.com/en/blog/free-smtp-servers/)
- [Google Maps scraping legality 2026 — Scrap.io](https://scrap.io/scrape-google-gaps-legal)
- [Google Maps scraping guide 2026 — Web Data Labs](https://web-data-labs.com/blog/google-maps-scraper-2026)
- [LinkedIn limits 2026 — Wandify](https://wandify.io/blog/sourcing/linkedin-limits-in-2026-complete-guide/)
- [How many cold emails per day — Mailreach](https://www.mailreach.co/blog/how-many-cold-emails-to-send-per-day)
