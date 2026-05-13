# Task board

Read this file in agent runs to learn what needs to happen. The `task-router` agent processes the `## Open` section every 5 minutes and event-driven on push.

## Format

```
## Open

- [task-id: <YYYYMMDD-HHMM-SLUG>] {agent_hint: "<optional>"} <one-line description>
  Inputs: <files/values>
  Deadline: <ISO or "asap">
  Created: <ISO ts>
```

When `task-router` dispatches a task it moves the block to `## Dispatched`. When the specialist finishes, it moves the block to `## Completed` with the outcome.

## Open

- [task-id: 20260513-2300-zd-pivot] {agent_hint: "network-outreacher"} Generate Monday's zero-dollar outreach package per ZERO-DOLLAR-PLAYBOOK
  Inputs: docs/ZERO-DOLLAR-PLAYBOOK.md, data/network-targets.csv (create empty if missing)
  Deadline: 2026-05-18T13:00:00Z
  Created: 2026-05-13T23:33:14Z

- [task-id: 20260513-2301-toolwatch] {agent_hint: "ai-tool-watcher"} Verify Anthropic May 2026 pricing in docs/RESEARCH.md is current
  Inputs: docs/RESEARCH.md Part 3
  Deadline: asap
  Created: 2026-05-13T23:33:14Z

- [task-id: 20260513-2302-scancompete] {agent_hint: "competitor-scanner"} First competitor scan baseline for roofing lead-gen agencies
  Inputs: docs/RESEARCH.md, manual seed list TBD
  Deadline: 2026-05-19T14:00:00Z
  Created: 2026-05-13T23:33:14Z

## Dispatched

(none yet)

## Completed

- [task-id: bootstrap] {agent_hint: "human"} Scaffold the agency repo with 12-agent fleet
  Result: shipped PR #4 (commits d11bb6e + ac4d7bd + d67b911)
  Completed: 2026-05-13T23:33:14Z
