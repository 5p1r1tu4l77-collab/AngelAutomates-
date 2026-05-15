# AngelAutomates — Session Handoff (2026-05-15)

**Paste this entire file into a new Claude session as the first message.** It is self-contained: a new instance with Gmail/Notion/Calendar/GitHub MCP can pick up exactly where the previous session ended without re-discovering state.

---

## Project in one paragraph

`5p1r1tu4l77-collab/AngelAutomates-` is the operating repo for AngelAutomates, a productized AI cold-outreach + appointment-setting agency. There is also a Flutter starter app (`navarro_mission_control`) in the same repo, but the active work is the agency operations. An active long-running goal (`20260513-0687` — "Make money using 0 dollars") gates everything: no paid services, no Anthropic API on the user's side, no cron-fleet activation until the first $1k revenue is collected. The full agent fleet (20 agents under `.claude/agents/`) is paused because their secrets aren't set. This session bypassed the secrets bottleneck by using MCP tools (Gmail, Notion, Calendar) to do the cold-outreach work directly inside the Claude session — zero new secrets, zero LLM spend on the user's side.

---

## Git state

- Repo: `5p1r1tu4l77-collab/AngelAutomates-`
- Branch: `claude/debug-and-fix-Yhyfl` (do NOT push to a different branch without permission)
- Last 3 commits (newest first):
  - `5ead9f1` — Batch 3: owner-name enrichment + V2 drafts + Reply Playbook + slots
  - `5c55029` — Batch 2: 10 more cold drafts + Notion pipeline sync
  - `1618f96` — Engineer past the secret-setup bottleneck via Gmail MCP
- Push pattern: `git push -u origin claude/debug-and-fix-Yhyfl` with retries on network errors.

---

## What's been built this session

### 20 Gmail drafts (all in user's Drafts folder, `[VERIFY]` or `[VERIFY-V2]` subject prefix)

**Tier A — 5 V2 drafts with real owner names** (send these first, may need email-guess verification):

| Company | Owner | V2 To: (guess) | Subject |
|---|---|---|---|
| Integris Roofing | Cody Zegarrundo (founder) | cody@integrisroofing.com | `[VERIFY-V2] integris pipeline — 1 question` |
| Rose Roofing | Jonathan Rose (3rd gen) | jonathan@roseroofing.com | `[VERIFY-V2] jonathan — 3rd-gen rose roofing` |
| Telge Roofing | Roy Campbell | roy@telgeroofing.com | `[VERIFY-V2] roy — keeping cypress crews booked` |
| Braun's Roofing | Skeeter Braun (founder 1987) | skeeter@braunsroofing.com | `[VERIFY-V2] skeeter — 46 years + qualified pipeline?` |
| Air Innovations | Troy Behrens | troy@airinnovationsllc.com | `[VERIFY-V2] troy — pre-summer AC pipeline` |

**Tier B — 15 V1 drafts at info@ with "hi there" greeting**:

Roofing (10): State Roofing TX, Rose Roofing, Texas Storm Group, Delaneys Restoration, TSG Roofing, Moss Roofing Houston, Integris Roofing, Lone Star Roofing, Telge Roofing, Braun's Roofing.

HVAC (5): Air Innovations, All Star A/C, Smart Air, ASAP Air, Mission AC.

Note: 5 of the Tier B V1 drafts (Integris, Rose, Telge, Braun's, Air Innovations) overlap with Tier A V2 drafts. When the human sends V2, they should delete the matching V1 to avoid double-sending.

### Notion artifacts (workspace already authenticated via Notion MCP)

| Item | ID |
|---|---|
| Pipeline DB | `e03862f6-2d66-4d09-9c3e-9f4e1f21b4ec` |
| Pipeline data source (use for creating cards) | `16bb09e2-172b-4098-a017-59ab490e269d` |
| Parent page "AngelAutomates — Activation Checklist" | `3611afd6-c578-81f1-a28d-fc4ec5a409da` |
| Reply Playbook page | `3611afd6-c578-81a2-b570-dff71ffa4348` |

15 cards in the Pipeline DB (Stage=`new`, Owner=`agent`, Source=`google-maps`). 5 of them have `Contact` populated with owner name + caveats in `Notes`.

Stage enum on Pipeline DB: `new`, `contacted`, `replied`, `interested`, `scheduling`, `scheduled`, `discovery-done`, `closed-won`, `closed-lost`, `nurture`.

### Calendar slot inventory (verified open on `angenavarr77@gmail.com`, America/Chicago)

| Day | Date | Time (CT) |
|---|---|---|
| Tue | May 19 | 11:00 AM |
| Wed | May 20 | 2:00 PM |
| Thu | May 21 | 10:30 AM |
| Fri | May 22 | 1:00 PM |
| Tue | May 26 | 11:00 AM |
| Wed | May 27 | 2:00 PM |

Mon May 25 = Memorial Day, skipped. These slots are baked into `docs/REPLY-PLAYBOOK.md`.

---

## Hard constraints from CLAUDE.md (do NOT violate)

1. **Goal 20260513-0687 is active.** No paid services. No Anthropic API on user side. No Smartlead/Apollo/Apify. Track in `tracker/quota.json`.
2. **Do NOT run** `python scripts/run_agent.py <name>` outside of `--dry-run`. Cron triggers fail closed because secrets are unset; do not enable them.
3. **Do NOT touch** `data/drafts/_pending/` — human-approval-gated by design.
4. **Branch lock**: develop only on `claude/debug-and-fix-Yhyfl`.
5. **Frugal GitHub posting**: only comment on PRs when genuinely necessary.

---

## MCP tools verified working this session

- **Gmail MCP** (`mcp__72ec8ceb-...`): `create_draft`, `list_drafts`, `search_threads`, label tools. **No update_draft, no delete_draft** — replacing a draft means creating a new one and asking the human to delete the old.
- **Notion MCP** (`mcp__7a300568-...`): full read/write on AngelAutomates workspace. Use `notion-fetch` to get a DB schema before creating cards.
- **Calendar MCP** (`mcp__843330e9-...`): `list_calendars`, `list_events`, `suggest_time`, `create_event`. Primary calendar = `angenavarr77@gmail.com`, TZ = `America/Chicago`.
- **GitHub MCP** (`mcp__github__...`): scoped to `5p1r1tu4l77-collab/angelautomates-` only.
- **WebSearch / WebFetch**: search works, fetch is blocked by anti-bot on most contractor sites. Use WebSearch for facts; have the human visit sites for direct email addresses.

---

## Repo files for full context (in priority order)

1. `CLAUDE.md` — project rules (read first, always)
2. `tracker/STATUS.md` — current "Action needed" banner
3. `docs/ZERO-DOLLAR-PLAYBOOK.md` — campaign rules
4. `docs/REPLY-PLAYBOOK.md` — decision tree for inbound replies
5. `templates/cold-email.md` — voice rules + Step-1/2/3 cadence
6. `templates/discovery-call-script.md` — the 12-min call
7. `data/leads-enriched.csv` — the 15 leads, 5 with `full_name`
8. `tracker/log.jsonl` — append-only audit trail (this session = mcp-batch-1, mcp-batch-2, mcp-batch-3)
9. `.claude/goals/active.json` — the active goal, check via session-start hook

---

## What the human needs to do (in order)

1. Open Gmail Drafts. Process the 5 `[VERIFY-V2]` drafts: verify the `firstname@domain` email (check the company's contact page or LinkedIn), replace `[your name]`, remove `[VERIFY-V2]`, send. Delete the matching V1 draft.
2. Process the remaining 10 `[VERIFY]` info@ drafts: replace `[your name]`, remove `[VERIFY]`, send.
3. In Notion Pipeline Board view, drag each sent card from `new` → `contacted`.
4. When a reply lands: follow `docs/REPLY-PLAYBOOK.md`. The 6 pre-baked calendar slots are already in the prefab reply text.

---

## What the next Claude session should do (priority order)

1. **First check**: read `tracker/STATUS.md` and `.claude/goals/active.json`. Banner the active goal per CLAUDE.md.
2. **Ask the human**: "Did you send any of the 20 drafts? How many? Any replies yet?"
3. Based on answer:
   - **No drafts sent**: diagnose blocker (confusion? embarrassment? technical? no time?). Lower friction — offer to walk them through draft 1.
   - **Some sent, no replies**: 3+ days in, draft Step-2 follow-ups using `templates/cold-email.md` Step-2 pattern. Create as Gmail drafts with `[VERIFY-STEP2]` subject prefix.
   - **A reply landed**: read the reply (ask human to paste or use `get_thread`), classify per Reply Playbook, draft the response in Gmail.
   - **Wants more volume**: source next batch from a new geography (DFW or Austin) or vertical (med spa, dental, solar — all residential high-ticket fits ICP). Use WebSearch. Don't exceed 25 cold/day Gmail cap.
   - **Wants the remaining 10 enriched**: WebSearch each company for owner name + LinkedIn, follow the batch-3 pattern.

4. **If 5+ days have passed since send, no replies**: switch the human to LinkedIn-DM mode for the same 15 leads. Use `docs/ZERO-DOLLAR-PLAYBOOK.md` LinkedIn cap (20 connection requests/day).

---

## Caveats / unresolved

- **Integris Roofing draft addresses Cody Zegarrundo** as founder (per `theroof.store` article). But LinkedIn lists Michael Thrower with title "CEO/Owner". Both could be true (Cody founded, Michael bought it; or co-owners). Have human verify before sending.
- **All V2 owner emails are GUESSES** (firstname@domain). They may bounce. Best fallback if uncertain: replace the V2 To: with the V1's info@<domain>.
- **"Skeeter" Braun** is the public name; real first name may differ but Skeeter is what appears in reviews and on LinkedIn.
- **WebFetch is blocked** by anti-bot on most contractor sites. WebSearch works fine. The full Playwright scraper in the repo handles anti-bot but only runs on GitHub Actions cron, which is paused under the zero-dollar goal.
- **5 Tier-B drafts overlap with Tier-A V2 drafts**. The human MUST delete the V1 after sending V2 to avoid double-touch (looks spammy and tanks deliverability).
- **Gmail MCP has no draft delete/update**. If a draft needs replacing, create a new one and explicitly tell the human to delete the old one.

---

## Session-start banner you should print

When you take over, first message back to the human should be roughly:

> 📌 Active goal: Make money using 0 dollars (iter N/M). 20 cold-email drafts sit in your Gmail Drafts folder from yesterday's session — 5 personalized with owner names (`[VERIFY-V2]` prefix), 15 generic info@ (`[VERIFY]` prefix). Notion `AngelAutomates Pipeline` has 15 cards in `new`. Reply Playbook + 6 pre-baked calendar slots are in `docs/REPLY-PLAYBOOK.md`. What's the status — sent any? Any replies?

Then wait for the human's answer before doing anything else.
