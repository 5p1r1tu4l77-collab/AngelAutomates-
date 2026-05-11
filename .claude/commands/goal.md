---
description: "Set or manage a long-running objective (Claude Code port of OpenAI Codex /goal)"
argument-hint: "<objective> | status | pause | resume | clear | complete | budget <N>"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite, AskUserQuestion
---

# /goal — persistent objective manager

You are running the `/goal` slash command. This is a Claude Code port of OpenAI Codex CLI's `/goal` feature: a persistent, self-checking objective that you (the model) iterate on across turns, with plan → act → test → review → decide loops until a stop condition is met.

## Arguments

The raw argument string is: `$ARGUMENTS`

Treat the **first whitespace-separated token** (lowercased) as the subcommand, and the rest as its payload. If `$ARGUMENTS` is empty, the subcommand is `status`.

| Subcommand     | Effect                                                                                                  |
| -------------- | ------------------------------------------------------------------------------------------------------- |
| _(empty)_      | Same as `status`                                                                                        |
| `status`       | Print the current goal's objective, status, iteration count, criteria, and last 3 progress entries      |
| `pause`        | Set `status: "paused"`; do not iterate                                                                  |
| `resume`       | Set `status: "active"`; run one iteration                                                               |
| `clear`        | Move `.claude/goals/active.json` to `.claude/goals/archive/<goal_id>.json`; do not iterate              |
| `complete`     | Set `status: "complete"`, archive, report final summary                                                 |
| `budget <N>`   | Update `max_iterations` to integer `N`; do not iterate                                                  |
| _anything else_ | Treat the whole `$ARGUMENTS` string as a new objective (see "Setting a new goal" below)                 |

## State file

Single source of truth: `.claude/goals/active.json`. Schema documented at `.claude/goals/SCHEMA.md`. Read it once at the start of every invocation. If the file does not exist, treat it as "no active goal".

When you write the file, always:
- Refresh `updated_at` to the current UTC ISO-8601 timestamp (use `date -u +%Y-%m-%dT%H:%M:%SZ`).
- Preserve all fields you didn't intend to change.

## Setting a new goal

1. If an active goal already exists with status `active` or `paused`, call `AskUserQuestion`:
   - Question: "There's already an active goal: '<existing objective>'. Replace it?"
   - Options: "Replace (archive the old one)", "Cancel (keep the existing goal)".
   - If "Cancel", stop and report.
2. Generate a `goal_id` of the form `YYYYMMDD-XXXX` (date + 4 random hex chars). Use `date -u +%Y%m%d` and `openssl rand -hex 2` (or `tr -dc 0-9a-f </dev/urandom | head -c 4` if openssl is missing).
3. Derive `completion_criteria`:
   - If the objective contains explicit success markers ("when X passes", "until Y is green"), extract them.
   - Otherwise ask the user via `AskUserQuestion` for 1–3 concrete criteria. Keep it short — one question, options like "Use the criteria I'll dictate" / "Auto-derive from the objective text". On auto-derive, infer reasonable criteria from the objective.
4. Write `.claude/goals/active.json`:
   ```json
   {
     "goal_id": "<id>",
     "objective": "<verbatim user input>",
     "status": "active",
     "completion_criteria": ["...", "..."],
     "max_iterations": 20,
     "iterations": 0,
     "created_at": "<now>",
     "updated_at": "<now>",
     "progress_log": []
   }
   ```
5. Run **one iteration** (see below).

## Running one iteration

Triggered by: a new goal being set, `resume`, or any subcommand that lands while `status == "active"` and is not a control verb (pause/clear/complete/budget/status).

Before iterating, check:
- If `status != "active"`, do not iterate — just report state.
- If `iterations >= max_iterations`, set `status: "budget_limited"`, save, report, stop.

Iteration steps:

1. **PLAN.** Use `TodoWrite` to record 1–3 concrete next steps that move toward `completion_criteria`. The first todo should be marked `in_progress`.
2. **ACT.** Execute the in-progress todo. Make code changes, run tools, fetch info — whatever the step requires. Stay scoped: this is one step, not the whole goal.
3. **TEST.** If you touched Dart files under `lib/`, run:
   ```bash
   flutter analyze
   flutter test
   ```
   Skip if no Dart files changed. If `flutter` is not installed in this environment, note it in the progress log and continue.
4. **REVIEW.** Append to `progress_log`:
   ```json
   { "ts": "<now>", "iteration": <new>, "summary": "<one sentence: what changed>", "tests": "<pass|fail|skipped|n/a>" }
   ```
   Increment `iterations` by 1. Mark the todo `completed`.
5. **DECIDE.** Evaluate against `completion_criteria`:
   - All criteria met → set `status: "complete"`, archive (see "Archiving") and report the final summary.
   - Tests failed or step blocked → keep `status: "active"`, surface the blocker, stop. Do not retry blindly on the same turn.
   - `iterations >= max_iterations` → set `status: "budget_limited"`, save, report.
   - Otherwise → save with `status: "active"`, stop, and tell the user "one iteration done — run `/goal resume` to continue, or `/goal` to see status".

**Important:** One iteration per slash-command invocation. Do not chain iterations within a single turn. The user controls pacing.

## Archiving

When status becomes terminal (`complete`, `budget_limited`) or on explicit `clear`:

```bash
mkdir -p .claude/goals/archive
mv .claude/goals/active.json .claude/goals/archive/<goal_id>.json
```

The archive directory is gitignored — these are local per-developer records.

## Status report format

When reporting status, output a compact block:

```
📌 Goal <goal_id> — <status>
   Objective: <objective>
   Iterations: <iterations>/<max_iterations>
   Criteria:
     - [ ] <criterion>
     - [x] <met criterion>
   Last progress:
     <iter>: <summary> (tests: <result>)
```

## Notes & edge cases

- If `.claude/goals/active.json` is malformed JSON, report the error and offer to `clear` it. Do not auto-overwrite.
- `budget <N>` accepts any positive integer. If `N` is missing or non-numeric, report usage and stop.
- Never modify `goal_id`, `created_at`, or `objective` after creation. To change the objective, the user must `clear` and set a new goal.
- Do not infer goals from ordinary tasks — only act when `/goal` is explicitly invoked. (Mirrors Codex's tool instruction.)
