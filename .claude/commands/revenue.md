---
description: "Print today's revenue dashboard and outstanding human tasks"
allowed-tools: Read, Bash, Glob
---

# /revenue

Show the operator the state of the money pipeline right now.

## Steps

1. Read `tracker/dashboard.md` and print the "Today" and "Month-to-date" tables.
2. Read `tracker/STATUS.md` and print the "Open decisions" checklist plus any unresolved agent events from the last 48h.
3. Tally last 24h from `tracker/log.jsonl` (use `grep` + a Python one-liner if needed): count of agent runs by status (`ok` / `skipped` / `error`), total `cost_usd`, total `revenue_impact` distribution.
4. Print a one-line recommendation: which agent (if any) is the bottleneck right now? If pipeline_value < $5000 and emails_sent_24h < 100, recommend manually triggering `prospector` + `icp-researcher` + `copywriter` via `workflow_dispatch`.

## Output format

```
📊 Revenue snapshot — <timestamp>
   Today:    <sent> sent, <replies> replies, <booked> booked, $<closed> closed-won
   MTD:      $<mrr> MRR, $<pipeline> pipeline
   Spend:    $<today> / $<daily_allowance> today  ·  $<mtd> / $<cap> MTD
   Agents:   <ok>/<skipped>/<error> in last 24h

🔍 Bottleneck: <agent name + why>

📌 Open human tasks:
   - <task>
   - <task>
```

Do not call any APIs. Read-only command. Cost: zero.
