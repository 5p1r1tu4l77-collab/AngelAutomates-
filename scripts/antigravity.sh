#!/usr/bin/env bash
# ============================================================================
# ANTIGRAVITY - Multi-Terminal Launcher
# ============================================================================
# Launches parallel development sessions for zero-touch development.
# Each "terminal" runs as a background process with its own log file.
#
# Usage: ./scripts/antigravity.sh [--all|--dev|--test|--lint|--sync|--watch]
# ============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LOG_DIR="$PROJECT_DIR/.logs"
PID_FILE="$LOG_DIR/antigravity.pids"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

banner() {
    echo -e "${PURPLE}"
    echo "  ___  _  _ _____ ___ ___ ___    ___   _____ _____   __"
    echo " / _ \| \| |_   _|_ _/ __| _ \  /_\ \ / /_ _|_   _| / /"
    echo "| (_) | .\` | | |  | | (_ |   / / _ \ V / | |  | |  / / "
    echo " \___/|_|\_| |_| |___\___|_|_\/_/ \_\_/ |___| |_| /_/  "
    echo ""
    echo -e "${CYAN}  >> ANTIGRAVITY MODE ENGAGED <<${NC}"
    echo ""
}

setup() {
    mkdir -p "$LOG_DIR"
    : > "$PID_FILE"
    echo -e "${GREEN}[SETUP]${NC} Log directory: $LOG_DIR"
}

launch_terminal() {
    local name="$1"
    local color="$2"
    local cmd="$3"
    local log_file="$LOG_DIR/${name}.log"

    echo -e "${color}[TERMINAL $name]${NC} Launching: $cmd"
    echo -e "${color}[TERMINAL $name]${NC} Log: $log_file"

    cd "$PROJECT_DIR"
    nohup bash -c "$cmd" > "$log_file" 2>&1 &
    local pid=$!
    echo "$name:$pid" >> "$PID_FILE"
    echo -e "${color}[TERMINAL $name]${NC} PID: $pid ${GREEN}RUNNING${NC}"
}

stop_all() {
    echo -e "\n${RED}[ANTIGRAVITY]${NC} Shutting down all terminals..."
    if [[ -f "$PID_FILE" ]]; then
        while IFS=: read -r name pid; do
            if kill -0 "$pid" 2>/dev/null; then
                kill "$pid" 2>/dev/null || true
                echo -e "${YELLOW}[STOPPED]${NC} $name (PID: $pid)"
            fi
        done < "$PID_FILE"
        rm -f "$PID_FILE"
    fi
    echo -e "${GREEN}[ANTIGRAVITY]${NC} All terminals stopped."
}

status() {
    echo -e "\n${CYAN}[STATUS]${NC} Active terminals:"
    if [[ -f "$PID_FILE" ]]; then
        while IFS=: read -r name pid; do
            if kill -0 "$pid" 2>/dev/null; then
                echo -e "  ${GREEN}RUNNING${NC}  $name (PID: $pid)"
            else
                echo -e "  ${RED}STOPPED${NC}  $name (PID: $pid)"
            fi
        done < "$PID_FILE"
    else
        echo "  No active terminals."
    fi
}

# Terminal definitions
launch_dev() {
    launch_terminal "DEV-SERVER" "$GREEN" \
        "flutter run -d chrome --web-port=8080 2>&1 || echo '[DEV] Flutter not available, starting web server fallback'; cd build/web 2>/dev/null && python3 -m http.server 8080 || echo '[DEV] Waiting for build...'"
}

launch_test_watcher() {
    launch_terminal "TEST-WATCHER" "$BLUE" \
        "while true; do flutter test 2>&1; echo '[TEST] Waiting for changes...'; sleep 10; done"
}

launch_lint_watcher() {
    launch_terminal "LINT-WATCHER" "$YELLOW" \
        "while true; do dart format . 2>&1; flutter analyze 2>&1; echo '[LINT] Waiting for changes...'; sleep 15; done"
}

launch_obsidian_sync() {
    launch_terminal "OBSIDIAN-SYNC" "$PURPLE" \
        "bash $SCRIPT_DIR/obsidian-sync.sh --watch"
}

launch_git_daemon() {
    launch_terminal "GIT-DAEMON" "$CYAN" \
        "while true; do
            cd $PROJECT_DIR
            if [[ -n \$(git status --porcelain 2>/dev/null) ]]; then
                echo \"[GIT] Changes detected, auto-committing...\"
                git add -A
                git commit -m \"auto: $(date +%Y-%m-%d_%H:%M:%S) automated commit\" 2>/dev/null || true
                echo \"[GIT] Committed.\"
            else
                echo \"[GIT] No changes.\"
            fi
            sleep 60
        done"
}

# Main
trap stop_all EXIT INT TERM

banner
setup

MODE="${1:---all}"

case "$MODE" in
    --all)
        echo -e "${CYAN}[ANTIGRAVITY]${NC} Launching ALL terminals...\n"
        launch_dev
        launch_test_watcher
        launch_lint_watcher
        launch_obsidian_sync
        launch_git_daemon
        ;;
    --dev)      launch_dev ;;
    --test)     launch_test_watcher ;;
    --lint)     launch_lint_watcher ;;
    --sync)     launch_obsidian_sync ;;
    --watch)    launch_git_daemon ;;
    --stop)     stop_all; exit 0 ;;
    --status)   status; exit 0 ;;
    *)
        echo "Usage: $0 [--all|--dev|--test|--lint|--sync|--watch|--stop|--status]"
        exit 1
        ;;
esac

echo ""
status
echo -e "\n${CYAN}[ANTIGRAVITY]${NC} All terminals launched. Logs in: $LOG_DIR/"
echo -e "${CYAN}[ANTIGRAVITY]${NC} Run '$0 --status' to check status"
echo -e "${CYAN}[ANTIGRAVITY]${NC} Run '$0 --stop' to stop all terminals"
echo -e "\n${GREEN}>> You are now in antigravity mode. Zero gravity. Zero touch. <<${NC}\n"

# Keep alive
wait
