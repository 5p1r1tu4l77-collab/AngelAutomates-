# ============================================================================
# AngelAutomates - Navarro Mission Control
# One-command automation for everything.
# ============================================================================

.PHONY: help setup dev test lint build-all build-web build-android build-ios \
        build-linux build-macos build-windows clean antigravity gsd gsd-full \
        gsd-ship obsidian-sync hooks status

.DEFAULT_GOAL := help

# Colors
CYAN := \033[0;36m
GREEN := \033[0;32m
YELLOW := \033[1;33m
PURPLE := \033[0;35m
BOLD := \033[1m
NC := \033[0m

help: ## Show this help
	@echo ""
	@echo "$(PURPLE)$(BOLD)  AngelAutomates - Navarro Mission Control$(NC)"
	@echo "$(CYAN)  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-18s$(NC) %s\n", $$1, $$2}'
	@echo ""

# ─── Setup ──────────────────────────────────────────────────────────────

setup: ## First-time project setup (deps + hooks + vault)
	@echo "$(CYAN)[SETUP]$(NC) Installing dependencies..."
	flutter pub get || echo "$(YELLOW)[SKIP]$(NC) flutter not available"
	@echo "$(CYAN)[SETUP]$(NC) Installing git hooks..."
	@$(MAKE) hooks
	@echo "$(CYAN)[SETUP]$(NC) Initializing Obsidian vault..."
	@bash scripts/obsidian-sync.sh --once
	@echo "$(GREEN)[SETUP]$(NC) Done! Run 'make antigravity' to launch."

hooks: ## Install pre-commit hooks
	@chmod +x scripts/*.sh
	@mkdir -p .githooks
	@cp scripts/pre-commit.sh .githooks/pre-commit
	@chmod +x .githooks/pre-commit
	@git config core.hooksPath .githooks
	@echo "$(GREEN)[HOOKS]$(NC) Pre-commit hook installed."

# ─── Development ────────────────────────────────────────────────────────

dev: ## Start Flutter dev server
	flutter run -d chrome --web-port=8080

dev-mobile: ## Start Flutter dev server for mobile
	flutter run

hot: ## Hot restart the running app
	@echo "r" | flutter attach

# ─── Quality ────────────────────────────────────────────────────────────

lint: ## Format + analyze all code
	@echo "$(CYAN)[LINT]$(NC) Formatting..."
	dart format .
	@echo "$(CYAN)[LINT]$(NC) Analyzing..."
	flutter analyze --no-fatal-infos
	@echo "$(GREEN)[LINT]$(NC) Clean."

format: ## Format all Dart files
	dart format .

analyze: ## Run static analysis
	flutter analyze

test: ## Run all tests with coverage
	flutter test --coverage

test-watch: ## Run tests continuously
	@while true; do flutter test; echo "$(YELLOW)[TEST]$(NC) Waiting..."; sleep 10; done

# ─── Build ──────────────────────────────────────────────────────────────

build-all: build-web build-android ## Build all platforms
	@echo "$(GREEN)[BUILD]$(NC) All platforms built."

build-web: ## Build for web
	flutter build web --release

build-android: ## Build Android APK
	flutter build apk --release

build-ios: ## Build iOS (macOS only)
	flutter build ios --release --no-codesign

build-linux: ## Build for Linux
	flutter build linux --release

build-macos: ## Build for macOS
	flutter build macos --release

build-windows: ## Build for Windows
	flutter build windows --release

# ─── Automation ─────────────────────────────────────────────────────────

antigravity: ## Launch multi-terminal dev environment
	@chmod +x scripts/antigravity.sh
	@bash scripts/antigravity.sh --all

antigravity-stop: ## Stop all antigravity terminals
	@bash scripts/antigravity.sh --stop

antigravity-status: ## Check antigravity terminal status
	@bash scripts/antigravity.sh --status

gsd: ## Get Shit Done - quick pipeline (format, analyze, test)
	@chmod +x scripts/gsd.sh
	@bash scripts/gsd.sh --quick

gsd-full: ## GSD full pipeline (includes builds)
	@bash scripts/gsd.sh --full

gsd-ship: ## GSD + build + auto-commit + push
	@bash scripts/gsd.sh --ship

# ─── Obsidian ───────────────────────────────────────────────────────────

obsidian-sync: ## Sync Obsidian vault with project state
	@chmod +x scripts/obsidian-sync.sh
	@bash scripts/obsidian-sync.sh --once

obsidian-watch: ## Watch mode - sync vault every 5 min
	@bash scripts/obsidian-sync.sh --watch

# ─── Utilities ──────────────────────────────────────────────────────────

clean: ## Clean all build artifacts
	flutter clean
	rm -rf build/ .logs/
	@echo "$(GREEN)[CLEAN]$(NC) All clean."

deps: ## Update dependencies
	flutter pub get

upgrade: ## Upgrade dependencies
	flutter pub upgrade

status: ## Show project status
	@echo ""
	@echo "$(PURPLE)$(BOLD)  Project Status$(NC)"
	@echo "$(CYAN)  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━$(NC)"
	@echo "  Branch:  $$(git rev-parse --abbrev-ref HEAD)"
	@echo "  Commit:  $$(git log -1 --oneline)"
	@echo "  Changes: $$(git status --porcelain | wc -l | tr -d ' ') files"
	@echo "  Sources: $$(find lib -name '*.dart' 2>/dev/null | wc -l | tr -d ' ') dart files"
	@echo "  Tests:   $$(find test -name '*.dart' 2>/dev/null | wc -l | tr -d ' ') test files"
	@echo ""
