# CLAUDE.md

Project notes for Claude Code working in this repo.

## Project

`navarro_mission_control` — Flutter app, currently the stock counter starter. Supports Android, iOS, Linux, macOS, web, and Windows. CI (`.github/workflows/flutter-ci.yml`) runs `flutter analyze` and `flutter test` on every push.

## Goal awareness

This repo ships a `/goal` slash command (see `.claude/commands/goal.md`) that ports OpenAI Codex CLI's `/goal` feature: it persists a long-running objective in `.claude/goals/active.json` and runs one plan → act → test → review iteration per invocation.

**At the start of every session**, check whether `.claude/goals/active.json` exists. If it does:
- If `status == "active"`, surface a one-line banner: `📌 Active goal: <objective> (iter <n>/<max>).` Then continue with whatever the user asked.
- If `status == "paused"`, mention it once: `📌 Paused goal: <objective>. Run /goal resume to continue.` Don't auto-resume.
- If `status` is terminal (`complete`, `budget_limited`), the file should have been archived — if it's still present, flag it as stale.

Don't infer or create goals from ordinary tasks. Only act on `/goal` when the user explicitly invokes the slash command.

Schema for `active.json`: see `.claude/goals/SCHEMA.md`.

## Agency operations

This repo is not just a Flutter app — it also operates AngelAutomates, a productized AI cold-outreach + appointment-setting agency. Twelve scheduled Claude agents under `.claude/agents/` are run on GitHub Actions cron via the reusable workflow `.github/workflows/_agent-runner.yml`.

- **Operating playbook**: `docs/PLAYBOOK.md` (read this before changing agent behavior).
- **Current offer**: `docs/OFFER.md` (locked for first 90 days; do not edit casually).
- **Current ICP**: `docs/ICP.md` (changes go through the `recruiter` agent's PR).
- **Human's daily routine**: `docs/HUMAN-LOOP.md`.
- **Dashboard**: `tracker/dashboard.md` (rewritten by `kpi-tracker`).
- **What's blocking right now**: `tracker/STATUS.md`.
- **Strategy log**: `tracker/decisions.md`.
- **Research dossier**: `docs/RESEARCH.md` — toolstack, business model knowledge, open questions.
- **Research protocol**: `docs/RESEARCH-PROTOCOL.md` — how agents handle "I don't know" without guessing.
- **Task board**: `tracker/task-board.md` — queue of work. `task-router` dispatches.
- **Zero-dollar playbook**: `docs/ZERO-DOLLAR-PLAYBOOK.md` (active while goal 20260513-0687 is open).

Twenty agents total (12 core + 8 meta/zero-dollar):
- **Pipeline**: prospector, icp-researcher, copywriter, outreach-dispatcher, reply-triage, appointment-setter, sales-ops.
- **Ops**: kpi-tracker, compliance-monitor, content-engine.
- **Strategy**: growth-strategist, recruiter, competitor-scanner, ai-tool-watcher, self-improver.
- **Zero-dollar mode**: network-outreacher, pilot-deliverer, referral-asker, case-study-writer.
- **Meta**: task-router.

Slash commands available:
- `/goal` — long-running objective tracker (see above).
- `/revenue` — print today's KPIs + outstanding human tasks (read-only, free).
- `/onboard <lead_id>` — run the new-client onboarding sequence.

When working on agent prompts or workflows, always check `docs/PLAYBOOK.md` "Conventions" and "Models" sections first. Never reach into `data/drafts/_pending/` programmatically — those are human-approval-gated by design.

## Common commands

```bash
flutter pub get        # install deps
flutter analyze        # static analysis (matches CI)
flutter test           # run unit/widget tests (matches CI)
flutter run -d chrome  # run the web build locally

# Agent ops
pip install -r scripts/requirements.txt
python scripts/run_agent.py <agent_name> --dry-run     # local dry-run
DRY_RUN=1 python scripts/run_agent.py prospector       # same via env
```
