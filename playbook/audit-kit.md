# Visibility Audit Kit — The Consultative Front Door

A cold "want a website?" pitch asks for a favor. A **visibility audit** hands the
owner a problem they didn't know the size of — with the fix already priced. Same
prospect, far higher reply and close rates, because you lead with *their* numbers
instead of your offer.

This is a new income line **and** a better top of funnel for everything else in
the kit. Every red item on an audit maps to a service you already sell.

## The two products

| Product | Price | What it is | When to use |
|---------|-------|------------|-------------|
| **Free Mini-Audit** | $0 | 3-4 sharp bullets in a message: their single biggest gap + what it's costing them. Pure lead magnet. | Cold outreach. Replaces the generic pitch. |
| **Full Visibility Report** | **$129** | The polished `templates/audit/` page — scorecard, cost-of-inaction, prioritized action plan. Live link they can save as a PDF. | Sell to prospects who won't buy a site *yet* but will pay to learn where they stand. Also: **free** with any Starter Site — a value-add that justifies the price. |

Rule of thumb: the mini-audit gets the reply; the report or the free mockup
closes. Never charge for the mini-audit — it's the hook.

## How to produce a report with Claude (~15 min)

**Step 1 — Gather public info (5 min).** From Google Maps + their site (open it
on a phone) collect: business name, category, city, whether the profile is
claimed, hours/photos/description completeness, star rating + review count,
whether the owner replies to reviews, whether a website exists, and how it looks
on mobile. Note what you'd search to find them ("[category] [city]") and whether
they show up.

**Step 2 — Hand it to Claude (1 min):**
> "Build a visibility report from templates/audit/ for [info dump]. Score each
> category from the public facts only — don't invent anything. Put it in
> audits/<business-slug>/ and push."

Claude scores each area, writes factual verdicts, fills the cost-of-inaction and
the three-step action plan (mapped to the prices below), and pushes. It goes live at:
`https://5p1r1tu4l77-collab.github.io/AngelAutomates-/audits/<business-slug>/`

**Step 3 — Send it.** (Templates below.)

## Every finding is a fix you already sell

| Audit finding | The fix | Price |
|---------------|---------|-------|
| No website / Facebook-only | Starter Site | $350 |
| Site is ancient / breaks on mobile | Site Rebuild | $350 |
| Google Business Profile thin or unclaimed | GBP setup/cleanup | $100 |
| No way to get a quote without calling | Contact/quote form → their email | $75 |
| Menu/prices not online | Online menu / price list page | $75 |
| Few reviews / not asking for them | Review-request setup (QR + templates) | $150 |
| "I don't have time to keep it updated" | Monthly care plan | $50/mo |

So a single report is a menu of upsells the owner asked for by reading it. Put
the biggest-impact, lowest-friction fix as Priority 1.

## Outreach templates (audit-led)

### Template A — Cold, leads with the mini-audit

Subject: found 3 things costing [Business Name] customers

> Hi [name],
>
> I look for local businesses that are clearly great but hard to find online, and
> [Business Name] jumped out — [specific: "4.8 stars from 160 people is elite"].
> I ran a quick visibility check and noticed three things:
>
> 1. [Biggest gap, e.g. "No website — so anyone who Googles you has to call and hope you pick up."]
> 2. [Second, e.g. "Your Google profile is missing hours and photos, so you rank below shops with worse reviews."]
> 3. [Third, e.g. "There's no way to see your prices without messaging you."]
>
> I put the fixes and what they cost in a one-page report — want me to send it
> over? Free, no obligation. Here's the kind of work I do: [demo link]
>
> — Angel

### Template B — They bit; deliver the report link

> Here's your visibility report, live: [audit link]
>
> Open it on your phone. The red items are the ones actually costing you calls
> right now — #1 is the one I'd fix first. Want me to build a free mockup of that
> fix so you can see it before deciding anything?

### Template C — Report → mockup handoff (the close bridge)

> Glad it was useful. The quickest win on there is [#1 fix]. I can build you a
> free live mockup of it this week — you'll see your own [homepage / new profile]
> before you spend a cent. Want me to?

From here you're back in the normal flow: free mockup → `closing-kit.md`.

## Selling the paid $129 report

Most prospects get the report free (as the hook, or bundled with a site). Charge
the $129 only when someone wants the analysis but isn't ready to build — usually a
bigger/pickier business. Pitch:

> I do a full written visibility report — every part of your online presence
> scored, what each gap is costing you, and a prioritized plan — for $129. If you
> decide to have me fix anything within 30 days, I credit the full $129 toward the
> work. So it's essentially free if you move forward.

The 30-day credit removes the risk and pulls them toward buying the fixes.

## Rules

- **Never invent facts.** Every score and line comes from public info you actually
  checked. A wrong claim ("you have no reviews" when they have 200) kills trust
  instantly. When unsure, phrase it as a question, not a verdict.
- **Lead with impact, not features.** "Costing you calls," not "not mobile-optimized."
- **One report ≈ 15 min.** It's a sales tool. Don't gold-plate it.
- **Priority 1 is always the cheapest big win** — the easiest yes gets them into
  the pipeline; the rest upsell later.
- Keep audits live even after a no — owners often come back when a competitor
  passes them. After they become a paying client and the fixes ship, delete the
  audit folder.
