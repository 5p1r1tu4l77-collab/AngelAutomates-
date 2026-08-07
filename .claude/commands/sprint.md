---
description: Sprint mode — define an ordered batch of 2–5 related /goal-style objectives and step through them one cycle at a time.
argument-hint: [<name> -- <obj1> | <obj2> | ... | check | next | status | clear]
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
---

# /sprint — ordered multi-goal sprint mode

You are running the `/sprint` slash command. A sprint is a named, ordered list
of 2–5 related objectives, each with its own verifiable stop condition. You
work through them in sequence using the same plan→act→verify loop as `/goal`,
one cycle per invocation.

**State file:** `.claude/goals/sprint.json`
**Arguments:** `$ARGUMENTS`

## State schema

```json
{
  "name": "<sprint name>",
  "created_at": "<ISO8601>",
  "updated_at": "<ISO8601>",
  "current_index": 0,
  "status": "active | paused | complete | abandoned",
  "goals": [
    {
      "objective": "<one sentence>",
      "stop_condition": "<measurable evidence>",
      "out_of_scope": "<what not to touch>",
      "validation": "<exact commands>",
      "status": "pending | active | complete | skipped",
      "turns": 0,
      "notes": []
    }
  ]
}
```

Sprint `status` is `complete` only when every goal is `complete` or `skipped`.

## Dispatch

Parse `$ARGUMENTS`:

- empty or `check` or `status` → **Show status**
- starts with `next` or `continue` → **Run next cycle**
- starts with `pause` → set sprint `status: paused`, write, report
- starts with `resume` → set sprint `status: active`, write, report
- starts with `clear` or `abandon` → delete `.claude/goals/sprint.json`, report
- starts with `skip` → mark `current_index` goal as `skipped`, advance
  `current_index`, write, report
- anything containing ` -- ` → **Define sprint** (treat text before ` -- ` as
  the name, text after as pipe-delimited objectives)
- anything else → error: "Unknown subcommand. Usage: `/sprint <name> -- <obj1> | <obj2>`"

If a sprint already exists and is `active` or `paused` when the user tries to
define a new one, refuse and tell them to `/sprint clear` first.

---

## Action: Show status

1. If `.claude/goals/sprint.json` does not exist → "No active sprint. Define
   one with `/sprint <name> -- <obj1> | <obj2> | ...`." Stop.
2. Read the file and print:
   - Sprint name, overall status, `current_index / total` progress
   - For each goal: index, objective, status, turn count
   - Last 2 notes from the current goal
3. Do not start working.

## Action: Define sprint

Parse `$ARGUMENTS` on ` -- `:
- Left side → `name`
- Right side → split on ` | ` to get objectives (2–5 required; refuse outside
  that range)

For each objective, you must populate `stop_condition`, `out_of_scope`, and
`validation`. Use the same decision rule as `/goal`: infer from context if you
can, otherwise ask the user in one consolidated question with proposed defaults.

Write `.claude/goals/sprint.json` with all goals `status: pending`,
`current_index: 0`, sprint `status: active`.

Immediately proceed into **Run next cycle** for the first goal.

## Action: Run next cycle

This runs exactly one plan→act→verify cycle on the current goal, then yields.

1. Read `.claude/goals/sprint.json`.
2. If missing → "No sprint set." Stop.
3. If sprint `status` is `paused` → "Sprint is paused. Use `/sprint resume`."
   Stop.
4. If sprint `status` is `complete` or `abandoned` → report, stop.
5. Identify the current goal: `goals[current_index]`.
6. If that goal's status is `pending`, set it to `active`, write file.
7. Create a TodoWrite list scoped to this cycle (3–6 items).
8. **Plan:** 1–3 sentences on the next concrete step for this goal. Check
   `notes` to avoid repeating prior work.
9. **Act:** make the change (Edit/Write/Bash), staying within scope.
10. **Verify:** run the goal's `validation` commands. Capture output.
11. **Decide:**
    - Stop condition met → set goal `status: complete`, advance
      `current_index`:
      - If next index exists → set it to `active`, report "Goal N complete.
        Next: '<objective>'. Run `/sprint next` to continue."
      - If no next index → set sprint `status: complete`, report "Sprint
        '<name>' complete! All goals done."
      - Write file and stop.
    - Stop condition not met → append note, increment goal `turns`, update
      `updated_at`, write file. End with: "Cycle complete on goal N
      ('<objective>'). Run `/sprint next` for another cycle, or `/sprint
      pause` to hold."
12. If all remaining goals exhausted → set sprint `status: complete`, report.

## Rules

- **One cycle per invocation.** Yield after verification.
- **Evidence over vibes.** Only advance a goal when validation output
  demonstrably satisfies the stop condition — quote it.
- **Scope discipline.** Respect each goal's `out_of_scope`. If cross-goal
  dependencies arise, surface them to the user.
- **Persistence is the source of truth.** Re-read the JSON at the start of
  every action.
- **Never create a sprint from ordinary chat.** Only `/sprint <name> -- ...`
  creates sprint state.
- **2–5 goals only.** Refuse if the user provides fewer than 2 or more than 5.

## Now do it

Subcommand / arguments: `$ARGUMENTS`

Dispatch per the rules above.
