---
type: automation-runbook
tags: [automation, ci, github-actions]
updated: 2026-04-16
---

# CI/CD Pipeline

## Overview
Automated CI/CD via GitHub Actions. Triggers on every push and PR.

## Workflows

### ci.yml - Continuous Integration
- **Trigger:** Push to main, claude/**, feature/**; PRs to main
- **Steps:**
  1. Format check (`dart format --set-exit-if-changed .`)
  2. Static analysis (`flutter analyze`)
  3. Run tests with coverage (`flutter test --coverage`)
  4. Build matrix: Web, Android, iOS, Linux, macOS, Windows
- **Artifacts:** Coverage report, web build

### deploy.yml - Deployment
- **Trigger:** Push to main, version tags (v*)
- **Steps:**
  1. Build web release
  2. Deploy to GitHub Pages
  3. Create GitHub Release (on tags)

### obsidian-sync.yml - Vault Sync
- **Trigger:** Push to main/claude/** (when lib/, test/, or pubspec.yaml changes)
- **Steps:**
  1. Generate daily note with build info
  2. Update project index
  3. Auto-commit vault updates

## Manual Triggers
```bash
make gsd          # Quick: format + analyze + test
make gsd-full     # Full: + builds + commit
make gsd-ship     # Ship: + push to remote
```

## Links
- [[projects/navarro-mission-control|Project Home]]
- [[automations/gsd-pipeline|GSD Pipeline]]
- [[automations/antigravity|Antigravity Launcher]]
