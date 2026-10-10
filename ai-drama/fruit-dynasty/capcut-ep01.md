# Making Episode 1 in CapCut — *Fallen Fruit*

Your CapCut subscription can handle almost the whole episode: images, animation, voices, lip sync, captions and editing. This guide turns `episodes/ep01.md` into a copy-paste checklist.

CapCut renames and moves its AI tools often, and some are released country by country. If a button here has a slightly different name in your app, look for the closest match. The tools you need:

| You need | Look for in CapCut | If you don't have it |
|---|---|---|
| Make images | **AI image** / **Image Canvas** (Seedream model) | Keep using `make_refs.py` with OpenCode |
| Animate an image | **AI video** / **Video Studio** → image-to-video (Seedance model) | Use the free tier of Kling or Dreamina's website, then import the clips |
| Talking characters | **AI dialogue** / **talking photo** / **lip sync** | Animate without lip sync and keep the mouth off-screen or turned away |
| Voices | **Text to speech** | — |
| Captions | **Auto captions** | — |

---

## Step 1 — Get your master images (5 min)

Download these from GitHub. Open each link, then click the **download** button (↓) at the top right of the image:

- Limón: `github.com/5p1r1tu4l77-collab/AngelAutomates-/blob/ai-drama-kit/ai-drama/fruit-dynasty/refs/limon/MASTER.png`
- Don Coco (current version): `github.com/5p1r1tu4l77-collab/AngelAutomates-/blob/ai-drama-kit/ai-drama/fruit-dynasty/refs/don-coco/MASTER.png`

Make a phone or PC album called **Rotten - Cast** and keep every master in it.

## Step 2 — Finish the cast in CapCut (20–30 min)

Episode 1 needs **Mango, Kiwi and Plátano**, and Don Coco should be redone, because the current one looks too human. Make them in CapCut's AI image tool so you don't burn your free Hugging Face quota.

**How:** open AI image. If it lets you add a **reference image**, add Limón's MASTER and choose "style" reference (not "character"), so every fruit looks like it's from the same show. Set the ratio to **9:16**. Paste one prompt, generate, and pick the best result. Save it to the album as `<name>-MASTER`.

Each prompt puts the face right after the head (that's what fixed the blank-faced Mango):

**Don Coco**
> photorealistic whole brown hairy coconut shell as the head with rough fibrous husk texture, with a clearly visible human face on the coconut: wise dark human eyes, bushy gray coconut-fiber eyebrows, nose, mouth and a long gray coconut-fiber beard, elderly man's body, black three-piece suit, gold pocket watch, wooden cane, cinematic portrait, warm amber and deep green color grade, film grain, dramatic lighting, 35mm

**Mango**
> photorealistic ripe golden-orange mango as the head with a small green leaf on top, with a clearly visible human face on the mango skin: two confident human eyes, raised eyebrows, nose and a smirking mouth, athletic man's body, cream linen suit over an open-collar white shirt, gold chain, cinematic portrait, warm amber and deep green color grade, film grain, dramatic lighting, 35mm

**Kiwi**
> photorealistic fuzzy brown kiwi fruit as the head, sliced open on top to show bright green flesh like hair, with a clearly visible human face on the kiwi skin: big innocent human eyes, eyebrows, nose and a shy mouth, skinny 19-year-old man's body, oversized green hoodie, headphones around neck, cinematic portrait, warm amber and deep green color grade, film grain, dramatic lighting, 35mm

**Plátano**
> photorealistic slightly spotted yellow banana as the head, tall and curved, with a clearly visible human face on the banana peel: stoic heavy-lidded human eyes, eyebrows, nose and a firm mouth, broad muscular man's body, black chauffeur suit, black leather gloves, dark sunglasses pushed up on the head, cinematic portrait, warm amber and deep green color grade, film grain, dramatic lighting, 35mm

**The rest of the cast** (not in Ep 1, but needed from Ep 4 on, so make them the same day while your style is dialed in):

**Uva Brothers** (Ep 4, 6)
> two identical men, each with a photorealistic cluster of plump purple grapes as the head, with a clearly visible human face on the grape cluster: two smug human eyes, eyebrows, nose and mouth, matching black tracksuits, gold chains, standing side by side, cinematic portrait, warm amber and deep green color grade, film grain, dramatic lighting, 35mm

**Don Piña** (Ep 5)
> photorealistic pineapple as the head with a tall spiky green crown and a golden scarred rind, with a clearly visible human face on the pineapple: two menacing human eyes, thick eyebrows, nose and a grinning mouth, heavyset man's body, white suit with a red silk shirt, many gold rings, holding a cigar, cinematic portrait, warm amber and deep green color grade, film grain, dramatic lighting, 35mm

**El Jalapeño** (Ep 5, 7, 8)
> photorealistic glossy dark green jalapeño pepper as the head, with a clearly visible human face on the pepper skin: narrow glowing red human eyes, sharp eyebrows, nose and a thin mouth, lean man's body, long black leather coat, black gloves, standing in shadows with faint steam rising, cinematic portrait, warm amber and deep green color grade, film grain, dramatic lighting, 35mm

**Aguacate** (Ep 7, 8)
> photorealistic dark green bumpy avocado as the head, with a clearly visible human face on the avocado skin: nervous human eyes behind round gold glasses, eyebrows, nose and mouth, older man's body, brown tweed suit, bow tie, holding a leather briefcase, cinematic portrait, warm amber and deep green color grade, film grain, dramatic lighting, 35mm

**Coco Jr.** (Ep 15–20)
> photorealistic young green coconut as the head with a pale scar across the husk, with a clearly visible human face on the coconut: determined dark human eyes, eyebrows, nose and mouth, muscular young man's body, faded canvas dock worker's jacket, gray beanie, cinematic portrait, warm amber and deep green color grade, film grain, dramatic lighting, 35mm

**Check every image:** fruit texture looks real, two eyes plus a mouth, human hands, right outfit. If one is off, regenerate rather than settling, because these images are your actors for all 20 episodes.

## Step 3 — Pick each character's voice (10 min)

In **Text to speech**, choose one voice per character and **write down its name**. Always use the same voice for that character.

| Character | Pick a voice that is… | Settings |
|---|---|---|
| Don Coco | Deep, old, slow, raspy (a "wise elder" or "narrator" type) | Speed 0.9× |
| Mango | Smooth, confident, charming young man | Normal |
| Limón | Low, dry, serious | Speed 0.95× |
| Kiwi | Young, soft, emotional | Normal |

My voice picks: Don Coco = ______ · Mango = ______ · Limón = ______ · Kiwi = ______

## Step 4 — Make the 12 shots (about 2 hrs the first time)

For each shot:
1. **Make the still** in AI image: the master image(s) as character reference + the **Scene prompt** + 9:16.
2. **Animate it** in AI video (image-to-video): paste the **Motion prompt**, about 5 seconds.
3. **If the shot has a speaking line** marked 🗣️: run the still (or the clip) through **AI dialogue / lip sync** with that character's voice and the line.

Add this to the end of **every** scene prompt:
> photorealistic anthropomorphic fruit characters, cinematic vertical 9:16, shallow depth of field, warm amber and deep green color grade, film grain, dramatic lighting, 35mm

| # | Reference | Scene prompt | Motion prompt | Audio |
|---|---|---|---|---|
| 1 | none | Extreme close-up of a crystal glass of fresh orange juice set down on a candlelit wooden dinner table, small hands sliding it forward | slow-motion push-in on the glass, candle flames flicker | V.O. **Don Coco:** "Every empire falls the same way. From the inside." |
| 2 | Don Coco, Mango, Limón, Kiwi, Plátano | Long birthday dinner table in a Spanish-colonial hacienda courtyard at night, the coconut patriarch at the head, three fruit sons seated, banana bodyguard standing behind him, candles and a coconut cake | slow symmetrical push-in, guests laughing | 🗣️ **Mango** (raising glass): "To Papá. Eighty years, and still the hardest nut in the market." + laughter, guitar |
| 3 | Limón | The lemon man at the dinner table, not raising his glass, frowning at his father, candlelight | subtle head turn, eyes narrow | 🗣️ **Limón:** "Eighty years. And you still haven't named an heir." (music stops) |
| 4 | Don Coco | The coconut patriarch chuckling and lifting a glass of orange juice at the head of the table | lifts the glass slowly toward his mouth | 🗣️ **Don Coco:** "Tonight, I will." |
| 5 | Don Coco | The coconut patriarch drinking, his eyes suddenly wide with shock | eyes widen, glass slips from his hand | Heartbeat SFX |
| 6 | none | A crystal glass shattering on a stone courtyard floor, orange juice splashing | slow-motion shatter and splash | Glass shatter SFX |
| 7 | Don Coco, Plátano, Kiwi | A thin crack running down the coconut patriarch's forehead as he collapses into the banana bodyguard's arms, chairs falling behind | handheld shaky camera, collapse | 🗣️ **Kiwi:** "PAPÁ!" + gasps, chairs falling |
| 8 | Don Coco, Mango, Limón | The mango son rushes forward, but the dying coconut father pushes past him and grabs the lemon son's coat with a trembling hand | quick movement, hand grips the coat | 🗣️ **Mango:** "Papá, I'm here—" |
| 9 | Limón | Extreme close-up of the lemon man holding his dying father, a single drop of lemon juice running down his cheek like a tear | the juice tear slowly rolls down | 🗣️ **Don Coco** (whisper, off-screen): "Limón… don't trust the sweet ones." + soft strings |
| 10 | Don Coco, Limón | Over-the-shoulder: the coconut father pulls the lemon son close to whisper in his ear | slow lean in | 🗣️ **Don Coco** (whisper): "It was one of my sons…" |
| 11 | none | A gold pocket watch falling open on a stone floor, the hands stopped at midnight | watch drops and settles, the second hand stops | The clock stops ticking |
| 12 | Kiwi, Limón, Mango | The three fruit brothers' faces in candlelight: the kiwi sobbing, the lemon in shock, and the mango half in shadow wiping a single tear… then a faint smile | slow pan left to right, ending on the mango's smile | Bass hit, then cut to black |

**Tips**
- **Shots 2 and 12 have several characters.** If the tool struggles with that many references, make each fruit separately and cut between quick close-ups. That's more dramatic anyway.
- **Never show fruit being cut or smashed on camera.** The crack in shot 7 and the juice tear are the limit, to keep it PG-13 and monetizable.
- Save every clip as `ep01-shot01.mp4`, `ep01-shot02.mp4`…

## Step 5 — Edit (30–45 min)

1. **New project, 9:16.** Drop shots 1–12 in order.
2. **Trim** each clip to its timing in `episodes/ep01.md` (about 70 seconds total). **Stay above 60 seconds**, because TikTok only pays on videos longer than a minute.
3. **Voices:** add the text-to-speech lines that aren't already lip-synced (shot 1's narration, shot 9's whisper).
4. **Hook text** for the first 2 seconds, big and centered: **One sip. One son. One betrayal.**
5. **Auto captions:** turn them on, use a bold style, and put them in the lower third. Fix any misheard words, especially names (Limón, Papá).
6. **Sound:** a tense or orchestral track from CapCut's licensed library, low under the dialogue. Add the sound effects from the table (heartbeat, glass shatter, gasps, clock stopping, bass hit).
7. **End card** (last 2 seconds, black screen): **Part 2 → which son did it?**
8. **Export:** 1080×1920, 30fps, highest quality.

## Step 6 — Post

- Use the caption, hashtags and pinned comment from the **Post kit** at the bottom of `episodes/ep01.md`.
- **Turn on the AI-generated content label** on TikTok, YouTube and Instagram. It's required, and skipping it can get the account demonetized.
- Make Episodes 2 and 3 the same way before launch, then post all three on day one so new viewers can binge.

---

## Episodes 2–20 and the trailer

Every episode file uses the same format as Episode 1, so the same steps work for all of them:

- **Reference images:** for each shot, use the masters of the characters named in brackets, e.g. `[LIMÓN]`, `[KIWI]`.
- **Scene prompt:** use the shot's **Visual prompt** column, with the style line added to the end.
- **Motion prompt:** use the **Camera** column, plus the action in the visual prompt.
- **Audio:** use the **Dialogue / VO** and **SFX** columns.
- **Spanish versions:** duplicate the finished English CapCut project. Replace the voice clips with Spanish text-to-speech from `episodes-es/`, redo the lip-sync shots, and re-run auto captions in Spanish. The visuals stay exactly the same.
