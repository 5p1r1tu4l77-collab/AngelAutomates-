# Goal state schema

This directory holds state for the `/goal` slash command (see `.claude/commands/goal.md`). It's a Claude Code port of OpenAI Codex CLI's `/goal` feature.

## Files

- **`active.json`** — the currently active or paused goal. At most one at a time. **Gitignored** (per-developer state).
- **`archive/<goal_id>.json`** — finalized goals (`complete`, `budget_limited`, or `clear`ed). Gitignored.
- **`.gitkeep`** — placeholder so the directory exists in version control.

## `active.json` shape

```json
{
  "goal_id": "20260511-a1b2",
  "objective": "Add a dark mode toggle to the counter app, persisted across restarts",
  "status": "active",
  "completion_criteria": [
    "Toggle visible in app settings",
    "Theme choice persists across restarts",
    "flutter analyze + flutter test pass"
  ],
  "max_iterations": 20,
  "iterations": 3,
  "created_at": "2026-05-11T12:54:00Z",
  "updated_at": "2026-05-11T13:10:00Z",
  "progress_log": [
    { "ts": "2026-05-11T12:55:10Z", "iteration": 1, "summary": "Added ThemeProvider scaffolding", "tests": "pass" },
    { "ts": "2026-05-11T13:01:22Z", "iteration": 2, "summary": "Wired toggle into Settings page", "tests": "pass" },
    { "ts": "2026-05-11T13:10:00Z", "iteration": 3, "summary": "Persisted theme via shared_preferences", "tests": "pass" }
  ]
}
```

## Field reference

| Field                  | Type                  | Notes                                                                                |
| ---------------------- | --------------------- | ------------------------------------------------------------------------------------ |
| `goal_id`              | string                | `YYYYMMDD-XXXX` (date + 4 hex). Immutable after creation.                            |
| `objective`            | string                | Verbatim user input. Immutable — clear and re-create to change.                      |
| `status`               | enum                  | `active` \| `paused` \| `complete` \| `budget_limited`                               |
| `completion_criteria`  | string[]              | 1–3 concrete success conditions. Derived from objective or supplied by user.         |
| `max_iterations`       | integer               | Default `20`. Adjust via `/goal budget <N>`.                                         |
| `iterations`           | integer               | Running count, incremented once per iteration. Status flips to `budget_limited` at cap. |
| `created_at`           | ISO-8601 UTC          | Immutable.                                                                           |
| `updated_at`           | ISO-8601 UTC          | Refreshed on every write.                                                            |
| `progress_log`         | array                 | One entry per completed iteration. `{ ts, iteration, summary, tests }`.              |

## Status lifecycle

```
                    /goal <objective>
                          │
                          ▼
                      ┌────────┐
        /goal pause   │ active │   one iteration completes (not done)
       ┌──────────────┤        ├──────────────┐
       │              └───┬────┘              │
       ▼                  │                   │
  ┌────────┐              │                   │
  │ paused │── /goal resume                   │
  └────────┘              │                   │
                          ▼                   ▼
                    ┌──────────┐      ┌────────────────┐
                    │ complete │      │ budget_limited │
                    └──────────┘      └────────────────┘
                          │                   │
                          └────────┬──────────┘
                                   ▼
                              archived to
                          archive/<goal_id>.json
```

## Differences from Codex `/goal`

This is a deliberate simplification of the upstream feature so it fits Claude Code's model:

| Codex                                | Here                                                                  |
| ------------------------------------ | --------------------------------------------------------------------- |
| Per-thread SQLite row                | Single JSON file in the repo                                          |
| Daemon auto-continues when idle      | Turn-based — each `/goal` invocation runs at most one iteration       |
| Token + wall-clock budget            | Iteration counter only (live token usage isn't exposed to commands)   |
| Model `update_goal` tool             | Model edits this JSON file directly                                   |
| `config.toml` `[features].goals` gate | None — slash commands are opt-in by definition                       |
