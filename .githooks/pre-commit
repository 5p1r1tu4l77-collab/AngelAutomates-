#!/usr/bin/env bash
# ============================================================================
# PRE-COMMIT HOOK
# ============================================================================
# Auto-runs before every commit:
# 1. Format changed Dart files
# 2. Run static analysis
# 3. Run tests (optional, set RUN_TESTS_ON_COMMIT=true)
# ============================================================================

set -eo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}[PRE-COMMIT]${NC} Running checks..."

# Get changed Dart files
DART_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.dart$' || true)

if [[ -z "$DART_FILES" ]]; then
    echo -e "${YELLOW}[PRE-COMMIT]${NC} No Dart files changed, skipping."
    exit 0
fi

# Step 1: Format
echo -e "${GREEN}[FORMAT]${NC} Formatting changed files..."
if command -v dart &>/dev/null; then
    echo "$DART_FILES" | xargs dart format
    echo "$DART_FILES" | xargs git add
    echo -e "${GREEN}[FORMAT]${NC} Done."
else
    echo -e "${YELLOW}[FORMAT]${NC} dart not found, skipping format."
fi

# Step 2: Analyze
echo -e "${GREEN}[ANALYZE]${NC} Running static analysis..."
if command -v flutter &>/dev/null; then
    flutter analyze --no-fatal-infos || {
        echo -e "${RED}[ANALYZE]${NC} Analysis failed. Fix issues before committing."
        exit 1
    }
    echo -e "${GREEN}[ANALYZE]${NC} Clean."
else
    echo -e "${YELLOW}[ANALYZE]${NC} flutter not found, skipping analysis."
fi

# Step 3: Tests (optional)
if [[ "${RUN_TESTS_ON_COMMIT:-false}" == "true" ]]; then
    echo -e "${GREEN}[TEST]${NC} Running tests..."
    if command -v flutter &>/dev/null; then
        flutter test || {
            echo -e "${RED}[TEST]${NC} Tests failed. Fix before committing."
            exit 1
        }
        echo -e "${GREEN}[TEST]${NC} All passed."
    fi
fi

echo -e "${GREEN}[PRE-COMMIT]${NC} All checks passed."
