# Goals state directory

Active long-horizon goal state lives in `current.json` here, written and
read by the `/goal` slash command (see `.claude/commands/goal.md`).

This is a Claude Code emulation of OpenAI Codex CLI's experimental `/goal`
long-horizon mode (Codex CLI 0.128.0+, April 2026). The Codex version
persists goal state in SQLite with model-callable tools (`create_goal`,
`update_goal`, `get_goal`) and a runtime-controlled auto-continuation
loop. Claude Code has no equivalent runtime, so this implementation
substitutes:

- **SQLite row** → `current.json` file
- **Model tools** → slash subcommands (`/goal <obj>`, `/goal continue`,
  `/goal check`, `/goal pause`, `/goal resume`, `/goal done`, `/goal
  clear`)
- **Runtime auto-continuation** → user-driven `/goal continue` per cycle
  (interactive sessions don't auto-loop unattended)
- **Token-budget enforcement** → optional `turn_budget` field that pauses
  the goal when exceeded

The four status values mirror Codex: `active`, `paused`, `complete`,
`abandoned`. Only `complete` and `abandoned` are terminal. The model may
transition `active → complete` only by quoting validation output that
demonstrably satisfies the stop condition; pause/resume/clear are
user-controlled.

## Usage

```
/goal Migrate all FutureBuilder usages in lib/ to Riverpod AsyncValue, keep tests green
/goal check
/goal continue
/goal pause
/goal resume
/goal done
/goal clear
```

A good goal defines four things — objective, stop condition, out of
scope, validation commands — so the loop has measurable evidence to halt
on. See the command file for the full spec.
