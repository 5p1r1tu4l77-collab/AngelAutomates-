---
description: Long-horizon goal mode — set a durable objective with a verifiable stop condition and iterate plan→act→verify until done.
argument-hint: [<objective> | check | continue | pause | resume | done | clear]
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, TodoWrite
---

# /goal — long-horizon goal mode

You are running the `/goal` slash command, a Claude Code emulation of OpenAI
Codex's `/goal` long-horizon mode. A "goal" is durable thread state: a single
verifiable objective that you (Claude) keep working toward across many turns,
checking your own progress against measurable evidence (tests, builds, lints,
typecheck, screenshots) until a stop condition is satisfied.

**State file:** `.claude/goals/current.json`
**Arguments:** `$ARGUMENTS` — first word is the subcommand (or empty).

## State schema

```json
{
  "goal_id": "<uuid>",
  "objective": "<one sentence: what to achieve>",
  "stop_condition": "<measurable, verifiable evidence that ends the loop>",
  "out_of_scope": "<what NOT to change>",
  "validation": "<exact commands or checks that prove progress>",
  "status": "active | paused | complete | abandoned",
  "turns": 0,
  "turn_budget": null,
  "created_at": "<ISO8601>",
  "updated_at": "<ISO8601>",
  "notes": ["<turn-by-turn notes>"]
}
```

Only `status: complete` and `status: abandoned` are terminal. The model
(you) may transition `active → complete` when the stop condition is
demonstrably met. The user controls `pause`, `resume`, `clear`. You must
never silently invent a goal from an ordinary task — only `/goal <objective>`
creates one.

## Dispatch

Parse the first whitespace-delimited token of `$ARGUMENTS`:

- empty or `check` or `status` → **Show status** (below)
- `continue` or `resume` → **Resume/continue loop** (below)
- `pause` → set `status: paused`, write file, report
- `done` or `complete` → mark `status: complete`, write file, report
- `clear` or `abandon` → delete `.claude/goals/current.json`, report
- anything else → treat the entire `$ARGUMENTS` as a new objective: **Set goal** (below)

If a goal already exists and is `active` or `paused` when the user tries to
set a new one, refuse and tell them to `/goal clear` or `/goal done` first.

---

## Action: Show status

1. If `.claude/goals/current.json` does not exist, say "No active goal. Set
   one with `/goal <objective>`." and stop.
2. Read it and print: objective, stop condition, status, turn count, last
   updated, and the last 3 notes. Do not start working.

## Action: Set goal

The user supplied a new objective in `$ARGUMENTS`. Before writing the file:

1. Verify no active/paused goal exists (refuse if it does).
2. Decide whether you have enough to write a *good* goal. A good goal needs
   four fields you can either infer confidently from `$ARGUMENTS` and the
   repo, or must ask the user for in one batched question:
   - **objective** — one sentence, scoped, achievable
   - **stop_condition** — measurable evidence (e.g. "`flutter test` passes
     with zero failures and `flutter analyze` reports no issues")
   - **out_of_scope** — what you will not touch
   - **validation** — exact commands you will run each cycle as evidence
3. If any field is genuinely ambiguous, ask the user one consolidated
   question with concrete proposed defaults — do NOT spam multiple round
   trips. If `$ARGUMENTS` is rich enough, fill defaults yourself and tell
   the user what you assumed.
4. Write `.claude/goals/current.json` with `status: active`, `turns: 0`,
   fresh `goal_id` (any unique short id), `created_at` and `updated_at`
   set to the output of `date -u +%Y-%m-%dT%H:%M:%SZ`.
5. Immediately proceed into the **loop** for turn 1.

## Action: Resume/continue loop (the verification loop)

This is the heart of `/goal`. Run **one** plan→act→verify cycle, then yield
back to the user. (Claude Code is interactive; we cannot truly run for hours
unattended. The user re-invokes `/goal continue` to keep going, or you can
queue the next cycle by ending with a clear "next step" call to action.)

1. Read `.claude/goals/current.json`.
2. If missing → "No goal set." Stop.
3. If `status` is `complete`, `abandoned`, or `paused` → report and stop.
   Do not act.
4. Create a TodoWrite list scoped to *this cycle only* (3–6 items max):
   plan the next concrete step, execute it, run the validation commands,
   compare against the stop condition, decide continue/complete.
5. **Plan**: in 1–3 sentences, state the next concrete step toward the
   objective and why it advances the stop condition. Re-read recent notes
   from the state file so you do not repeat work.
6. **Act**: make the change (Edit/Write/Bash). Stay strictly within scope —
   if you find yourself wanting to touch something in `out_of_scope`, stop
   and surface it to the user instead of doing it.
7. **Verify**: run the exact commands in `validation`. Capture pass/fail and
   a one-line summary of evidence.
8. **Decide**:
   - If the stop condition is *demonstrably* satisfied by the verification
     output → set `status: complete`, write the file, congratulate, stop.
   - If verification fails or the objective is not yet met → append a
     concise note to `notes` (what was done, evidence, what's next),
     increment `turns`, update `updated_at`, write the file, then end the
     turn with: "Cycle N complete. Run `/goal continue` for the next
     cycle, or `/goal pause` to hold." Do NOT auto-loop silently.
9. If `turn_budget` is set and `turns >= turn_budget` → set `status:
   paused`, write the file, and tell the user the budget is exhausted.

## Action: Pause / Done / Clear

- **pause** → read file, set `status: paused`, update `updated_at`, write
  file, report.
- **done** → read file, set `status: complete`, update `updated_at`, write
  file, report. Use this when the user manually declares victory.
- **clear** → `rm -f .claude/goals/current.json` (via Bash), report.

---

## Rules you must follow

- **Never** start the loop unless the user invoked `/goal <objective>` or
  `/goal continue` (or `/goal resume`). Ordinary chat messages do not
  resume a goal — that's the whole point of explicit state.
- **One cycle per invocation.** Yield back after verification. The user is
  in the loop on purpose.
- **Evidence over vibes.** Do not mark `complete` without running the
  validation commands and quoting their output.
- **Scope discipline.** Refuse to touch `out_of_scope` paths or features.
- **Persistence is the source of truth.** Always re-read the JSON file at
  the start of every action — do not trust prior context.
- **No silent goal creation.** If the user asks you to "keep working on X"
  without `/goal`, do the task normally; do not write the state file.

## Now do it

Subcommand / objective: `$ARGUMENTS`

Dispatch on the first token per the rules above and execute the
corresponding action.
