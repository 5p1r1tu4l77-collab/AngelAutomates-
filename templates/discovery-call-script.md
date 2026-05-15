# Discovery-call script — 12-minute close

Use on every booked discovery call during the zero-dollar phase (and beyond, with minor tweaks once we have full retainer pricing). Target: close on the call or walk away with a no.

## Pre-call checklist (90 seconds before)

1. Open their website in a tab. Note: city, service area, years in business, current marketing visible (Google reviews count, do they have BBB, do they have a quote-call CTA).
2. Open `data/pipeline.csv` and find their row. Note the personalization line that opened the email.
3. Open `tracker/dashboard.md` so you have current stats ready (current pilot count, % delivery rate).
4. Cal.com sends a video link 5 min before — be there 90 seconds early.

## The 12 minutes

### 0:00–1:30 — Rapport + transition (90 sec)

> "Hey {{first_name}}, thanks for jumping on. Quick context for the call — I usually keep these to 10–12 minutes, just enough to figure out if we're a fit. Cool with you?"

Wait for yes. Pause.

> "Awesome. Before I tell you what I do, I want to make sure I'm not pitching the wrong thing. Can I ask you 3 quick questions about your business?"

Always get explicit yes here. It frames the rest as their conversation, not your pitch.

### 1:30–4:30 — Discovery (3 questions, 3 min)

**Q1**: "What's your average ticket on a residential job — ballpark?"
(Listen. They'll often anchor low. Note it.)

**Q2**: "How many new homeowners do you talk to in a typical month? And of those, how many turn into estimates on the roof?"
(Listen for: are they lead-starved or close-rate-starved? Lead-starved is our buyer.)

**Q3**: "If 20 more pre-qualified homeowners landed on your calendar next month, could your crew handle the volume — or would that break something?"
(If they say it'd break things, the conversation pivots to fewer-higher-quality. If they say "bring it on," they're our buyer.)

### 4:30–7:30 — The offer (3 min)

> "Got it. Here's exactly what we do: we book qualified discovery calls between you and homeowners who are actively looking at roof replacement. We do it cold — meaning these are not people who've heard of you. We send the emails from our infrastructure, our domains, our deliverability. Your domain reputation stays clean.
>
> What you get: {{N}} qualified appointments per month. Qualified means decision-maker, in your service area, confirmed in writing. Every appointment that doesn't meet that bar, we replace for free.
>
> What you do: show up to the calls. Tell us within 48 hours if one wasn't qualified.
>
> The price: ${{price}}. {{term}}. If we don't hit the {{N}} number in any month, next month is free."

PAUSE. Wait for them to talk. Whoever speaks first loses; sit in the silence.

### 7:30–11:00 — Handle objections (3.5 min)

Use `templates/objection-handler.md` for specific responses. Most common:

- **"That's expensive."** → "Tell me about the math. {{ticket}} × {{close_rate}} × {{N}} = ${{$revenue}}. Our fee is ${{price}}. What part of that math doesn't work?"
- **"How is this different from {{competitor}}?"** → "Real answer: they're probably fine too. Two things we do differently: {{differentiator_1}} and {{differentiator_2}}. If those don't matter to you, go with whoever's cheapest."
- **"I tried lead gen before, it didn't work."** → "What didn't work — the lead quality or the follow-up on your end? Because if the answer is follow-up, we should solve that before we even talk about leads."
- **"Send me some info."** → "I can send a one-pager, but honestly, you'd save time deciding right now if it's a yes or no. What's the actual hesitation?"

### 11:00–12:00 — Close or walk (60 sec)

Try to close on the call:

> "Sounds like there's a fit. I'd rather you make a decision now than think about it for a week — both because that thinking rarely changes the answer, and because we only have {{N}} pilot slots this month. Yes or no?"

If yes: "Great. I'll text you a DocuSign and Stripe link in the next 10 minutes. Sign and pay today, we start tomorrow."

If no: "Totally fair. Mind if I follow up in 90 days?" (then add to nurture)

If "maybe" / "let me think": "Sure. What specifically do you need to decide on?" (drill into the real objection)

## After the call (5 min)

1. Update `data/pipeline.csv`: stage = `discovery-done` / `closed-won` / `lost`. Add notes.
2. If closed: trigger `/onboard <lead_id>` to draft the contract.
3. If lost: log the reason in `data/lost-deals.csv` for `growth-strategist` to read weekly.
4. Send the follow-up DocuSign + Stripe link from your phone before you stand up.

## Anti-patterns (do NOT do these)

- Don't talk for more than 2 consecutive minutes. Make them work.
- Don't lower the price on the first call. Ever. If they push back, talk about the math, not the price.
- Don't say "yes" to a discount in exchange for "thinking about it" — that's the worst trade.
- Don't promise specific results outside the offer (e.g., "you'll close 30% of these"). Stick to what's in `docs/OFFER.md`.
- Don't keep the call past 15 minutes. Time pressure is your friend.

## Recording (with permission)

If they consent: record on Otter or Google Meet. After the call, paste the transcript into `data/calls/<lead_id>-<date>.md`. The `self-improver` agent reads these to refine the script weekly.
