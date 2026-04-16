# AngelAutomates - Navarro Mission Control

## Project Overview
Cross-platform Flutter application (navarro_mission_control) with full automation pipeline.
All workflows are designed to run hands-free with zero manual intervention.

## Tech Stack
- **Framework:** Flutter (Dart) ^3.11.4
- **Platforms:** Android, iOS, macOS, Windows, Linux, Web
- **CI/CD:** GitHub Actions
- **Task Runner:** Make + custom GSD (Get Shit Done) scripts
- **Knowledge Base:** Obsidian vault (obsidian-vault/)
- **Automation:** Multi-terminal launcher + pre-commit hooks

## Quick Start - Zero Touch Automation

```bash
# Launch everything (multi-terminal dev environment)
make antigravity

# Run the full GSD pipeline (lint + test + build + deploy)
make gsd

# Single commands
make dev          # Start dev server
make test         # Run all tests
make lint         # Lint and format
make build-all    # Build all platforms
make clean        # Clean build artifacts
```

## Directory Structure
```
.github/workflows/   # CI/CD automation (runs on every push/PR)
scripts/             # Automation scripts
  antigravity.sh     # Multi-terminal launcher
  gsd.sh            # Get Shit Done task runner
  obsidian-sync.sh  # Obsidian vault auto-sync
  pre-commit.sh     # Pre-commit hook
.obsidian/           # Obsidian workspace config
obsidian-vault/      # Knowledge management vault
  daily-notes/      # Auto-generated daily logs
  templates/        # Note templates
  projects/         # Project documentation
  automations/      # Automation runbooks
.githooks/           # Git hooks
Makefile             # One-command task runner
```

## Automation Workflows

### 1. Antigravity (Multi-Terminal Launcher)
Launches parallel terminal sessions for simultaneous development:
- Terminal 1: Flutter dev server (hot reload)
- Terminal 2: Test watcher (auto-run tests on file change)
- Terminal 3: Lint watcher (auto-format on save)
- Terminal 4: Obsidian vault sync
- Terminal 5: Git auto-commit daemon

Run: `make antigravity` or `./scripts/antigravity.sh`

### 2. GSD Pipeline (Get Shit Done)
Sequential automation pipeline:
1. Format all Dart code
2. Run static analysis
3. Execute all tests
4. Build for target platforms
5. Generate coverage reports
6. Sync Obsidian vault with results
7. Auto-commit and push

Run: `make gsd` or `./scripts/gsd.sh`

### 3. CI/CD (GitHub Actions)
Triggers automatically on push/PR:
- `ci.yml` - Lint, test, build matrix (all platforms)
- `deploy.yml` - Auto-deploy on main branch merge
- `obsidian-sync.yml` - Sync vault documentation

### 4. Pre-Commit Hooks
Auto-runs before every commit:
- `dart format` on all changed .dart files
- `dart analyze` for static analysis
- Blocks commit if tests fail

## Obsidian Superpowers
The obsidian-vault/ directory is a full Obsidian knowledge base:
- **Daily Notes:** Auto-generated build/test logs
- **Templates:** Standardized note templates for bugs, features, automation
- **Projects:** Living documentation that updates with code changes
- **Automations:** Runbooks for every automated workflow

## Permissions Mode
Claude Code can operate in dangerously-bypass mode via .claude/settings.json.
All automation scripts are pre-approved for execution without manual confirmation.

## Common Commands
| Command | Description |
|---------|-------------|
| `make antigravity` | Launch multi-terminal dev environment |
| `make gsd` | Run full Get Shit Done pipeline |
| `make dev` | Start Flutter dev server |
| `make test` | Run all tests |
| `make lint` | Format + analyze |
| `make build-all` | Build all platforms |
| `make obsidian-sync` | Sync Obsidian vault |
| `make clean` | Clean everything |
| `make setup` | First-time project setup |
