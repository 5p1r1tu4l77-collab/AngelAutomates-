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

## Common commands

```bash
flutter pub get       # install deps
flutter analyze       # static analysis (matches CI)
flutter test          # run unit/widget tests (matches CI)
flutter run -d chrome # run the web build locally
```
