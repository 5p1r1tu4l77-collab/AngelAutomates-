---
type: automation-runbook
tags: [automation, antigravity, multi-terminal]
updated: 2026-04-16
---

# Antigravity - Multi-Terminal Launcher

## Overview
Launches 5 parallel development sessions as background processes.
Zero gravity. Zero touch. Everything runs simultaneously.

## Usage
```bash
make antigravity          # Launch all terminals
make antigravity-stop     # Stop all
make antigravity-status   # Check status
```

## Terminals

| # | Name | Purpose | Interval |
|---|------|---------|----------|
| 1 | DEV-SERVER | Flutter dev server (hot reload) | Continuous |
| 2 | TEST-WATCHER | Auto-run tests on changes | Every 10s |
| 3 | LINT-WATCHER | Auto-format + analyze | Every 15s |
| 4 | OBSIDIAN-SYNC | Vault auto-sync | Every 5min |
| 5 | GIT-DAEMON | Auto-commit changes | Every 60s |

## Selective Launch
```bash
./scripts/antigravity.sh --dev    # Dev server only
./scripts/antigravity.sh --test   # Test watcher only
./scripts/antigravity.sh --lint   # Lint watcher only
./scripts/antigravity.sh --sync   # Obsidian sync only
./scripts/antigravity.sh --watch  # Git daemon only
```

## Logs
All terminal output is logged to `.logs/`:
- `.logs/DEV-SERVER.log`
- `.logs/TEST-WATCHER.log`
- `.logs/LINT-WATCHER.log`
- `.logs/OBSIDIAN-SYNC.log`
- `.logs/GIT-DAEMON.log`

## Links
- [[projects/navarro-mission-control|Project Home]]
- [[automations/ci-pipeline|CI Pipeline]]
- [[automations/gsd-pipeline|GSD Pipeline]]
