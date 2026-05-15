# Day 3 — Wednesday: Gmail cold-email burst + LinkedIn

**Target touches today**: 50 (25 cold emails from Gmail + 20 LinkedIn connects + 5 follow-ups)

## Block 1 — Reply triage (15 min)

Same as Tuesday.

## Block 2 — Sourcing for cold email (45 min, 25 leads)

Go to **Google Maps**. Search: `roofing contractor [city]` for ONE city in the storm-belt list. Walk the results:

For each business that fits the ICP (5–80 employees, has a website, owner-operated feel):

1. Visit website. Find an owner/decision-maker name and email.
   - Footer / contact page / About page.
   - If only "info@" — use [Hunter.io free tier (25 searches/mo)](https://hunter.io) to find a personal email. Free tier only; no upgrades.
2. Capture in `data/leads-new.csv` (the schema is locked):

```csv
lead_id,company,domain,full_name,title,email,phone,city,state,industry,employee_count,source,sourced_at,status
abc-roofing-john,ABC Roofing,abcroofing.com,John Doe,Owner,john@abcroofing.com,555-1234,Houston,TX,Roofing,12,maps,2026-05-20T14:00Z,new
...
```

3. While on the site, note ONE specific fact: a recent project, a service area, a brand they install, a team member. Add to a notes column or your scratchpad.

## Block 3 — Personalized Gmail outreach (45 min, 25 sends)

Send from your real Gmail. ≤25 emails/day max — exceed this and Gmail flags you.

### Subject (≤4 words, lowercase)

Pick from this library:
- `quick {{city}} roofing question`
- `re: {{company}}`
- `homeowner referral idea`
- `{{first_name}} — quick one`
- `pilot for {{company}}`

### Body (50–80 words, personalized)

```
hi {{first_name}} —

{{personalization specific to them: "saw you handle storm restoration across
the gulf coast — that's our exact target"}}.

i'm doing 2 free pilots this month for residential roofing owners — 5
qualified booked appointments in 14 days, no cost. i need 1 more contractor
in {{state}} to round out the test.

worth a 10-min call this week?

— {{your_first_name}}
```

### Anti-patterns

- No images, no logos, no signature graphic. Plain text → delivered. HTML → spam folder.
- No tracking pixels. Your Gmail account isn't set up for tracking; faking it triggers Gmail's anti-spam.
- 1 email per minute, not faster. Use Boomerang or just space them yourself.
- Send between 9am and 11am ET in the recipient's timezone for max open rate.

## Block 4 — LinkedIn (30 min, 20 connects)

Same as Mon/Tue. Different state. Different specific facts.

## Block 5 — Day log

Same.
