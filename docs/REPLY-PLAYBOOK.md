# Reply Playbook — what to do when a prospect responds

**Synced to Notion at `Reply Playbook — what to do when a prospect responds` (under AngelAutomates — Activation Checklist).** This file is the source of truth.

When a reply lands in your Gmail inbox, follow this. Goal: a booked discovery call within 60 seconds of opening their reply.

## Step 0 — Classify the reply (10 sec)

| Bucket | Signal | Next step |
|---|---|---|
| **Interested** | "sure, let's talk" / "what times work" / "send me more info" | Reply with slots (Step 1) |
| **Curious / objecting** | "how much" / "how are you different" / "we already have an agency" | Brief reply + push to call (Step 2) |
| **Not interested** | "not now" / "remove me" / "unsubscribe" | Notion stage = `closed-lost`. No reply unless they ask to be removed. |
| **Auto-reply / OOO** | Bouncer / vacation | Nothing. Note in Notion. Resume in 7 days. |

## Step 1 — Interested prospect (45 sec)

```
hi {first_name} —

perfect. i have:

• tue may 19, 11:00 am ct
• wed may 20, 2:00 pm ct
• thu may 21, 10:30 am ct
• fri may 22, 1:00 pm ct
• tue may 26, 11:00 am ct
• wed may 27, 2:00 pm ct

which works? i'll send a google meet link once you pick.

— {your first name}
```

After they pick a slot:
1. Google Calendar → create event at that time.
2. Title: `Discovery — {company} × AngelAutomates`.
3. Add their email as guest. Add Google Meet link.
4. Description: paste the original-email personalization line.
5. Send the invite.
6. Notion: drag card from `replied` → `scheduled`. Fill `Booked Slot`.

## Step 2 — Curious / objecting (60 sec)

```
hi {first_name} —

good question — easiest if i walk you through it on a 12-min call. that way i can also ask 2-3 questions about your shop so i'm not pitching the wrong thing.

any of these work?

• tue may 19, 11:00 am ct
• wed may 20, 2:00 pm ct
• thu may 21, 10:30 am ct

— {your first name}
```

## Step 3 — The call itself

Follow `templates/discovery-call-script.md`. Three questions, then the offer. 12 min. Close on the call or walk away with a clean no.

## Don'ts

- Don't reply to "how much" with a number in email. Escalate to call.
- Don't reply to "send me a deck" with a deck. "Faster if i walk you through it — got 12 min?"
- Don't write more than 6 lines.
- Don't send Cal.com / Calendly links in zero-dollar mode. Manual slots in plain text convert higher.

## Slot inventory (refreshed 2026-05-15, expires when used or 5/27)

Confirmed free on `angenavarr77@gmail.com` (America/Chicago):

| Day | Date | Time (CT) |
|---|---|---|
| Tue | May 19 | 11:00 AM |
| Wed | May 20 | 2:00 PM |
| Thu | May 21 | 10:30 AM |
| Fri | May 22 | 1:00 PM |
| Tue | May 26 | 11:00 AM |
| Wed | May 27 | 2:00 PM |

Mon May 25 = Memorial Day, skipped.

When slots run out, refresh from Calendar (ask in next Claude session, or run the `suggest_time` MCP call).
