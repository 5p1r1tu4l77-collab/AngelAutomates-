---
type: automation-runbook
tags: [automation, gsd, pipeline]
updated: 2026-04-16
---

# GSD Pipeline (Get Shit Done)

## Overview
Sequential automation pipeline that handles the entire dev workflow.
Zero manual intervention required.

## Modes

### Quick Mode (default)
```bash
make gsd
# or: ./scripts/gsd.sh --quick
```
1. Format all Dart code
2. Run static analysis
3. Execute all tests
4. Generate Obsidian report

### Full Mode
```bash
make gsd-full
# or: ./scripts/gsd.sh --full
```
Quick mode + builds (web, android) + auto-commit

### Ship Mode
```bash
make gsd-ship
# or: ./scripts/gsd.sh --ship
```
Full mode + push to remote

### Build Only
```bash
./scripts/gsd.sh --build
```
Web + Android builds + report

## Output
- Console output with color-coded pass/fail
- Obsidian daily note with run report
- Auto-committed changes (full/ship modes)

## Links
- [[projects/navarro-mission-control|Project Home]]
- [[automations/ci-pipeline|CI Pipeline]]
- [[automations/antigravity|Antigravity Launcher]]
