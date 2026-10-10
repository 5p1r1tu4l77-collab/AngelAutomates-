# AI Drama Kit — *The Maid Owns the Mansion*

A complete, ready-to-produce AI micro-drama: 30 episodes × 60–90 sec, vertical video, with an English and a Spanish version.

| File | What it is |
|---|---|
| `series-bible.md` | Characters with **locked looks** (copy-paste prompts), locations, style line, show rules |
| `season-1-outline.md` | All 30 episodes, each with its cliffhanger, plus the paywall plan |
| `episodes/ep01–05.md` | Fully produced scripts: shot-by-shot AI prompts, dialogue, SFX, captions, hashtags |
| `generate.py` | Writes episodes 6–30, and the Spanish version, with Claude |
| `fruit-dynasty/` | **Second show:** *Rotten to the Core*, an all-male AI fruit crime-family drama (all 20 episodes + trailer scripted in English and Spanish). **Start with `fruit-dynasty/START-HERE.md`** |
| `fruit-dynasty/capcut-ep01.md` | Step-by-step guide to making Episode 1 entirely in CapCut: cast images, voices, all 12 shots, editing, export |

---

## Week 1: get to the first post

**Day 1: characters (about 2 hrs)**
- [ ] Generate one master reference image per character from the **Locked look** text in the bible (Midjourney, Flux, Ideogram, or the image tool inside Kling/Higgsfield).
- [ ] Regenerate until each face is perfect. These images are your actors, so save them in a `refs/` folder.
- [ ] Assign each character one fixed voice in ElevenLabs. Write the voice ID next to the name in the bible.

**Day 2–3: produce episodes 1–3 (about 2–3 hrs each at first, under 1 hr once you're practiced)**
- [ ] For each shot row, generate a still image using the character reference image plus the prompt plus the style line.
- [ ] Animate each still with image-to-video (Kling, Veo, Runway, or Hailuo), using the shot's camera note as the motion prompt.
- [ ] Generate the dialogue in ElevenLabs, then lip-sync the talking shots (Kling lip-sync, Hedra, or Sync Labs).
- [ ] Edit in CapCut: cut on dialogue, burn in big captions, add the SFX column, and put the hook text on screen for the first 2 seconds.
- [ ] Export at 1080×1920. Keep each episode **over 60 seconds**, because TikTok Creator Rewards only pays on videos longer than 1 minute.

**Day 4: write the rest**
```
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...      # from console.anthropic.com
python generate.py 6-30                   # about $2–5 total in API costs
python generate.py 1-30 --lang es         # Spanish season
```
Read every generated episode before you produce it. Rewrite any line that feels flat, because you're the showrunner.

**Day 5: launch**
- [ ] Set up the same handle on TikTok, YouTube Shorts, Instagram Reels, and Facebook. Example: `@maidownsthemansion`. Make a separate Spanish account: `@lasirvientaesladueña`.
- [ ] Post episodes 1, 2, and 3 at once, so new viewers can binge.
- [ ] Turn on the **"AI-generated" label** on every post. It's required, and skipping it gets accounts demonetized.

## Posting schedule

- **2 episodes a day** (about 12pm and 7pm) until episode 10. Build the whole Act 1 before launch so you never miss a day.
- Add every episode to a **"Part 1, 2, 3…" playlist** (TikTok Playlists, YouTube Shorts playlist).
- Pin a comment on every post asking a question. The pinned comments are already written in each episode's post kit, and comments push your videos to more viewers.
- After 3 days, check which episode has the best **completion rate** and reuse its hook style in your re-cut trailers.

## Ways to make money, in order

1. **Platform payouts:** TikTok Creator Rewards (10k followers and 100k views in 30 days, videos over 1 min), YouTube Partner Program (Shorts), Facebook content monetization. Facebook micro-drama audiences pay well and skew 35+.
2. **Paywall from episode 11:** episode 10 ends on the season's biggest cliffhanger. Post "full season, link in bio" and sell access through Patreon, Ko-fi, or Gumroad, at $4.99 for the season or $2.99 a month.
3. **License the series:** pitch the finished season, in both languages, to micro-drama apps (ReelShort, DramaBox, ShortMax and others) and to Spanish-language streaming and FAST channels. Several now buy AI-produced series.
4. **Sell the system:** once you have results, package the bible template, the prompts, and `generate.py` as a "$29 AI Drama Starter Kit." It fits next to your Angel Automates services.

## Rules that keep the account alive

- **Label everything as AI.** Never present the show as real events.
- **No real people, faces, voices, brands, or songs** you don't have rights to. Use the platform's licensed audio library.
- **Keep it PG-13.** Slaps and wine throws are fine. Avoid graphic violence and anything sexual, which get suppressed or demonetized.
- **Quality beats volume.** Platforms are cutting payouts for low-effort AI spam. Consistent faces and a strong story are what make this show different.

## Realistic expectations

Most accounts need **3–6 weeks of daily posting** before one episode breaks out. When one does, the playlist turns that spike into binge-viewers. If the first 10 episodes stall after 3 weeks, keep the production workflow and swap in a new concept: run `generate.py` against a new bible and outline. Your second show will be faster to make than your first.
