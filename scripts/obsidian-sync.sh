#!/usr/bin/env bash
# ============================================================================
# OBSIDIAN SYNC - Knowledge Base Auto-Updater
# ============================================================================
# Keeps the Obsidian vault in sync with project state.
# Generates daily notes, updates project docs, tracks automations.
#
# Usage: ./scripts/obsidian-sync.sh [--once|--watch]
# ============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VAULT_DIR="$PROJECT_DIR/obsidian-vault"

GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

sync_daily_note() {
    local DATE=$(date +%Y-%m-%d)
    local NOTE="$VAULT_DIR/daily-notes/${DATE}.md"

    if [[ ! -f "$NOTE" ]]; then
        cat > "$NOTE" << EOF
---
date: ${DATE}
type: daily-note
tags: [auto-generated, daily]
---

# ${DATE} - Daily Log

## Project Status
- **Branch:** $(git -C "$PROJECT_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
- **Last Commit:** $(git -C "$PROJECT_DIR" log -1 --oneline 2>/dev/null || echo "none")
- **Uncommitted Changes:** $(git -C "$PROJECT_DIR" status --porcelain 2>/dev/null | wc -l | tr -d ' ')

## Dart Files
$(find "$PROJECT_DIR/lib" -name "*.dart" 2>/dev/null | wc -l | tr -d ' ') source files

## Test Files
$(find "$PROJECT_DIR/test" -name "*.dart" 2>/dev/null | wc -l | tr -d ' ') test files

## Notes
-

## Links
- [[projects/navarro-mission-control|Project Home]]
EOF
        echo -e "${GREEN}[SYNC]${NC} Created daily note: ${DATE}.md"
    fi
}

sync_project_index() {
    cat > "$VAULT_DIR/projects/navarro-mission-control.md" << EOF
---
type: project
status: active
tags: [flutter, cross-platform, automation, angel-automates]
updated: $(date +%Y-%m-%d)
---

# Navarro Mission Control

## Overview
Cross-platform Flutter application with full AngelAutomates automation pipeline.

## Stats
- **Source Files:** $(find "$PROJECT_DIR/lib" -name "*.dart" 2>/dev/null | wc -l | tr -d ' ')
- **Test Files:** $(find "$PROJECT_DIR/test" -name "*.dart" 2>/dev/null | wc -l | tr -d ' ')
- **Platforms:** Android, iOS, macOS, Windows, Linux, Web
- **Branch:** $(git -C "$PROJECT_DIR" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")
- **Commits:** $(git -C "$PROJECT_DIR" rev-list --count HEAD 2>/dev/null || echo "0")

## Automation
- [[automations/ci-pipeline|CI/CD Pipeline]] - GitHub Actions
- [[automations/gsd-pipeline|GSD Pipeline]] - Get Shit Done runner
- [[automations/antigravity|Antigravity]] - Multi-terminal launcher

## Structure
\`\`\`
lib/         - Dart source code
test/        - Tests
web/         - Web platform
android/     - Android platform
ios/         - iOS platform
macos/       - macOS platform
linux/       - Linux platform
windows/     - Windows platform
scripts/     - Automation scripts
\`\`\`

## Recent Daily Notes
$(ls "$VAULT_DIR/daily-notes/"*.md 2>/dev/null | sort -r | head -5 | while read f; do
    echo "- [[daily-notes/$(basename "$f" .md)|$(basename "$f" .md)]]"
done)
EOF
    echo -e "${GREEN}[SYNC]${NC} Updated project index"
}

sync_once() {
    echo -e "${CYAN}[OBSIDIAN]${NC} Syncing vault..."
    mkdir -p "$VAULT_DIR/daily-notes" "$VAULT_DIR/projects" "$VAULT_DIR/automations" "$VAULT_DIR/templates"
    sync_daily_note
    sync_project_index
    echo -e "${GREEN}[OBSIDIAN]${NC} Sync complete."
}

watch_mode() {
    echo -e "${CYAN}[OBSIDIAN]${NC} Watch mode - syncing every 5 minutes..."
    while true; do
        sync_once
        sleep 300
    done
}

MODE="${1:---once}"

case "$MODE" in
    --once)  sync_once ;;
    --watch) watch_mode ;;
    *)
        echo "Usage: $0 [--once|--watch]"
        exit 1
        ;;
esac
