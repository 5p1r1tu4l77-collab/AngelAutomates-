# Case study template

Use this skeleton when filling `data/case-studies/<client-slug>.md`. The `content-engine` agent reads these to write inbound posts.

## Headline

`<Service vertical>: <X> appointments in <Y> days, $<Z> in pipeline`

Example: `Residential roofing: 18 appointments in 30 days, $312k in pipeline`

## Stats block

```
Client:       <type, e.g. "Texas residential roofer, 24 employees">
Window:       <date range>
Sent:         <emails>
Open rate:    <%>
Reply rate:   <%>
Booked:       <appointments>
Closed:       <jobs sold>
Pipeline $:   <total>
Close rate:   <%>
Avg ticket:   $<usd>
ROI:          <multiple of our fee>
```

## Narrative (3 paragraphs)

1. **Before** — what their growth bottleneck was; what they were already trying.
2. **What we did** — high-level (not the tactical playbook, save that for the buy-call). Lead source, personalization angle, sequence cadence, key inflection.
3. **After** — the numbers. End on the ROI multiple stated plainly.

## Pull-quotes

Include 1–2 client quotes if you have written permission (`data/permissions.csv`). Otherwise omit — never fabricate.

## Anonymization rules

- If permission missing: "a TX-based residential roofer with 20+ employees" — never the company name.
- Always real numbers, even when anonymized.
- Never include lead's real names. Always: "the homeowner / business owner".

## Usage

- `content-engine` pulls these for LinkedIn / X / shorts.
- `copywriter` uses the headline + stats block as `{{case_study_one_liner}}` merge tag in Step-2 cold emails.
- Sales calls reference these as proof.
