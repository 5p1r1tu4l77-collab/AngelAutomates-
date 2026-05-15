# ICP — Ideal Customer Profile (current)

**Status**: active
**Updated**: 2026-05-13
**Owner**: human + `recruiter` agent

## Primary niche: residential roofing contractors

| Attribute | Value |
|-----------|-------|
| Country | US |
| Annual revenue | $500k – $10M |
| Employee count | 5 – 80 |
| Years in business | ≥ 3 |
| Service type | residential roofing (storm work + retail) |
| Geography weighting | TX, FL, GA, OH, MO, OK, KS (storm-belt) |
| Decision maker | Owner / President / GM |
| Buying triggers | hail event in last 12 months; expanded crew in last 6 months; recent hire on LinkedIn |

## Secondary niche (parallel test): residential HVAC

Same shape. Geography: AZ, TX, FL, CA, NV. Decision maker: Owner / Ops Manager. Trigger: heat-pump rebate eligibility, seasonal turnover.

## Apollo / Apify query (roofing)

```
industry: "Construction" OR "Roofing"
keywords: "residential roofing" OR "roof replacement"
employee_count: 5-80
country: United States
state: Texas, Florida, Georgia, Ohio, Missouri, Oklahoma, Kansas
titles: Owner, President, CEO, General Manager, Operations Manager
exclude_industries: "Real Estate", "Insurance", "Manufacturing"
```

## Exclusion rules (compliance + fit)

- No commercial-only roofers (different buying cycle).
- No franchise corporate HQs (decisions roll up; not the buyer).
- No companies whose website fails to mention "residential" or "roof replacement" anywhere.
- No companies whose Google Reviews count > 1,500 (already too big; will procure in-house).

## Personalization research checklist (for `icp-researcher`)

Pick ONE of these per lead and write a 1-sentence hook:

1. A recent project in their portfolio gallery (city + roof type).
2. A specific service area town they list (especially smaller / rural).
3. A team member named on their About page (and what role).
4. A specific brand they install (GAF Master Elite, CertainTeed SELECT, etc).
5. A storm date if they mention recent storm response on their site.

## Anti-personalization (do NOT use)

- "Saw your website" / "Loved your site" / "Cool logo"
- Their LinkedIn headline (too obviously scraped)
- Anything from their LinkedIn bio (same)
- Numerical employee count (creepy)
