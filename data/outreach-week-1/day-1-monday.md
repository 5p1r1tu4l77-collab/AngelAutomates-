# Day 1 — Monday: personal network + LinkedIn launch

**Target touches today**: 35 (10 personal network DMs + 20 LinkedIn connects + 5 follow-ups on connects from prior weeks)

**Expected outcomes**: 1–3 reply within 24h. 0–1 booked call.

---

## Block 1 — Personal network (30 min, 10 DMs)

Pick 10 people who fit ANY of these patterns from your phone contacts / LinkedIn / Facebook / WhatsApp:

- They own or work at a home-services business (roofing, HVAC, plumbing, electrical, contractor).
- They live in TX, FL, GA, OH, MO, OK, KS, AZ, NV.
- They've referred you work before — anyone.
- They're loud on social media and like helping.
- A family member who knows "everyone in town".

### Personal-network DM template (adapt per person)

```
Hey {{first_name}},

Random ask — do you know any roofing or HVAC owners locally?

Quick context: I'm doing 2 free pilots this month to refine a new
lead-gen process for those guys. No catch, no pitch, just a free
trial of 5 booked appointments. If a name comes to mind, would
appreciate the intro.

If not, no worries at all. Hope all's well otherwise.

— {{your_name}}
```

### Track each one

Append to `data/network-touches.csv` (create if missing):

```csv
date,channel,target,relationship,status
2026-05-18,personal-dm,Jane Smith,college roommate,sent
2026-05-18,personal-dm,...
```

---

## Block 2 — LinkedIn connection requests (45 min, 20 connects)

### Sourcing (15 min)

LinkedIn search:
- Title: "Owner" OR "President" OR "CEO" OR "General Manager"
- Industry: "Construction" (filter "Roofing" after results load)
- Region: pick ONE state from {TX, FL, GA, OH, MO, OK, KS}
- Connections: 2nd or 3rd (avoids competing with your existing network)

Save 20 profile URLs in `data/linkedin-targets.csv`:

```csv
date,name,title,company,city,profile_url,note,status
2026-05-18,John Doe,Owner,ABC Roofing,Houston TX,linkedin.com/in/...,"GAF Master Elite, lots of storm work",sent
...
```

### Connect-note template (300 chars max, hit the limit)

Note the PROSPECT-SPECIFIC fact — don't be generic:

```
Hey {{first_name}} — saw {{specific_fact: e.g., "you do storm restoration in
Houston"}}. I'm running a no-cost pilot this month to send {{niche}} owners
20 qualified appointments. Looking for 2 contractors to test it with — open
to a quick chat if relevant?
```

### Variants by fact type

If they list **GAF/CertainTeed/Owens Corning Master Elite**:
> "Hey {{first_name}} — saw you're {{brand}} Master Elite, that's a real signal of quality. I'm running a no-cost lead-gen pilot this month for 2 contractors. Open to a 10-min chat?"

If they **list specific cities served**:
> "Hey {{first_name}} — saw you cover {{cities}} — that's the kind of focused market I'd want to send qualified appts into. Free pilot this month — open to chatting?"

If they **mention storm work**:
> "Hey {{first_name}} — saw you do storm restoration. Curious if your post-storm pipeline goes hot fast then dries up. I run a no-cost pilot that smooths that — chat?"

---

## Block 3 — Follow-ups on prior week's connects (15 min, 5 follow-ups)

For any 1st-degree connection from prior weeks that hasn't messaged back, send ONE follow-up. Cap your follow-up volume at 5/day to avoid burning the LI account.

```
Hey {{first_name}} — circling back. Still have 2 pilot slots open this
month. If now's not right, all good — just let me know if I should circle
back in 90 days?
```

---

## Block 4 — End-of-day log (15 min)

1. Append every touch to `data/network-touches.csv`.
2. For each reply: tag in `data/pipeline.csv` (create if missing): `lead_id, name, stage, channel, source_message_date, notes`.
3. Update `tracker/STATUS.md` with the day's numbers:
   - "2026-05-18: 35 touches sent. {{N}} replies received. {{M}} calls booked."

---

## Anti-patterns (today)

- Don't pitch in the first personal-network DM. Ask for a name.
- Don't connect-request anyone without a personalized note. LinkedIn's algorithm penalizes generic requests.
- Don't break the 20-connection daily cap. The account ban is unrecoverable.
- Don't go for >10 personal network DMs in one day. Relationship fatigue is real.

## Revenue math for today

10 personal DMs × 30% reply × 15% intro rate = ~0.45 warm intros queued.
20 LI connects × 30% accept × 20% reply rate = ~1.2 conversations.
5 follow-ups × 5% reply = ~0.25 conversations.
≈ 1.9 conversations / day × 5 days = ~9–10 conversations / week → 4–5 booked calls realistic.
