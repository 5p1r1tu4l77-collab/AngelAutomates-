#!/usr/bin/env bash
# ============================================================================
# GSD - GET SHIT DONE Pipeline
# ============================================================================
# Automated task pipeline: format -> analyze -> test -> build -> report -> push
# Runs everything sequentially with clear status output.
#
# Usage: ./scripts/gsd.sh [--quick|--full|--build|--ship]
# ============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VAULT_DIR="$PROJECT_DIR/obsidian-vault"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Tracking
STEP=0
TOTAL=0
FAILURES=0
START_TIME=$(date +%s)

banner() {
    echo -e "${BOLD}${PURPLE}"
    echo "   ██████╗ ███████╗██████╗ "
    echo "  ██╔════╝ ██╔════╝██╔══██╗"
    echo "  ██║  ███╗███████╗██║  ██║"
    echo "  ██║   ██║╚════██║██║  ██║"
    echo "  ╚██████╔╝███████║██████╔╝"
    echo "   ╚═════╝ ╚══════╝╚═════╝ "
    echo -e "${CYAN}  GET SHIT DONE${NC}"
    echo ""
}

step() {
    STEP=$((STEP + 1))
    echo -e "\n${BOLD}${BLUE}[$STEP/$TOTAL]${NC} ${BOLD}$1${NC}"
    echo -e "${BLUE}$(printf '%.0s─' {1..60})${NC}"
}

pass() {
    echo -e "${GREEN}  PASS${NC} $1"
}

fail() {
    echo -e "${RED}  FAIL${NC} $1"
    FAILURES=$((FAILURES + 1))
}

skip() {
    echo -e "${YELLOW}  SKIP${NC} $1"
}

# Pipeline stages
stage_format() {
    step "Formatting Code"
    if command -v dart &>/dev/null; then
        dart format . && pass "Code formatted" || fail "Format failed"
    else
        skip "dart not found - skipping format"
    fi
}

stage_analyze() {
    step "Static Analysis"
    if command -v flutter &>/dev/null; then
        flutter analyze --no-fatal-infos && pass "Analysis clean" || fail "Analysis found issues"
    else
        skip "flutter not found - skipping analysis"
    fi
}

stage_test() {
    step "Running Tests"
    if command -v flutter &>/dev/null; then
        flutter test --coverage && pass "All tests passed" || fail "Tests failed"
    else
        skip "flutter not found - skipping tests"
    fi
}

stage_build_web() {
    step "Building Web"
    if command -v flutter &>/dev/null; then
        flutter build web --release && pass "Web build complete" || fail "Web build failed"
    else
        skip "flutter not found - skipping web build"
    fi
}

stage_build_android() {
    step "Building Android APK"
    if command -v flutter &>/dev/null; then
        flutter build apk --release && pass "Android build complete" || fail "Android build failed"
    else
        skip "flutter not found - skipping Android build"
    fi
}

stage_obsidian_report() {
    step "Generating Obsidian Report"
    local DATE=$(date +%Y-%m-%d)
    local TIME=$(date +%H:%M:%S)
    local END_TIME=$(date +%s)
    local DURATION=$((END_TIME - START_TIME))

    mkdir -p "$VAULT_DIR/daily-notes"

    cat > "$VAULT_DIR/daily-notes/${DATE}-gsd-run.md" << EOF
---
date: ${DATE}
time: ${TIME}
type: gsd-report
tags: [auto-generated, gsd-pipeline]
duration: ${DURATION}s
failures: ${FAILURES}
---

# GSD Pipeline Report - ${DATE} ${TIME}

## Summary
- **Duration:** ${DURATION} seconds
- **Steps Run:** ${STEP}
- **Failures:** ${FAILURES}
- **Status:** $([ "$FAILURES" -eq 0 ] && echo "ALL CLEAR" || echo "HAS FAILURES")

## Pipeline Steps
1. Format Code
2. Static Analysis
3. Run Tests
4. Build (if --full or --build)
5. Obsidian Report
6. Auto-commit (if --ship)

## Links
- [[projects/navarro-mission-control|Project Home]]
- [[automations/gsd-pipeline|GSD Pipeline Docs]]
EOF

    pass "Report saved to obsidian-vault/daily-notes/${DATE}-gsd-run.md"
}

stage_auto_commit() {
    step "Auto-Commit & Push"
    cd "$PROJECT_DIR"
    if [[ -n $(git status --porcelain 2>/dev/null) ]]; then
        git add -A
        git commit -m "gsd: automated pipeline run $(date +%Y-%m-%d_%H:%M:%S)" || fail "Commit failed"
        pass "Changes committed"

        BRANCH=$(git rev-parse --abbrev-ref HEAD)
        git push -u origin "$BRANCH" && pass "Pushed to origin/$BRANCH" || fail "Push failed"
    else
        pass "No changes to commit"
    fi
}

# Summary
summary() {
    local END_TIME=$(date +%s)
    local DURATION=$((END_TIME - START_TIME))

    echo -e "\n${BOLD}${BLUE}$(printf '%.0s═' {1..60})${NC}"
    if [[ "$FAILURES" -eq 0 ]]; then
        echo -e "${BOLD}${GREEN}  GSD COMPLETE - ALL CLEAR${NC}"
    else
        echo -e "${BOLD}${RED}  GSD COMPLETE - ${FAILURES} FAILURE(S)${NC}"
    fi
    echo -e "  ${CYAN}Duration: ${DURATION}s | Steps: ${STEP} | Failures: ${FAILURES}${NC}"
    echo -e "${BOLD}${BLUE}$(printf '%.0s═' {1..60})${NC}\n"
}

# Main
cd "$PROJECT_DIR"
banner

MODE="${1:---quick}"

case "$MODE" in
    --quick)
        TOTAL=4
        stage_format
        stage_analyze
        stage_test
        stage_obsidian_report
        ;;
    --full)
        TOTAL=7
        stage_format
        stage_analyze
        stage_test
        stage_build_web
        stage_build_android
        stage_obsidian_report
        stage_auto_commit
        ;;
    --build)
        TOTAL=3
        stage_build_web
        stage_build_android
        stage_obsidian_report
        ;;
    --ship)
        TOTAL=7
        stage_format
        stage_analyze
        stage_test
        stage_build_web
        stage_build_android
        stage_obsidian_report
        stage_auto_commit
        ;;
    *)
        echo "Usage: $0 [--quick|--full|--build|--ship]"
        echo "  --quick  Format, analyze, test, report (default)"
        echo "  --full   Everything including builds and auto-commit"
        echo "  --build  Build only + report"
        echo "  --ship   Full pipeline + push to remote"
        exit 1
        ;;
esac

summary
exit $FAILURES
