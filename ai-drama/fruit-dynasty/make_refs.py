"""
make_refs.py — Fruit Dynasty character reference generator (FREE HF Spaces).

Plain-English: this script talks to a free image machine on Hugging Face,
asks for a photorealistic fruit character, and saves vertical portraits
so you can pick your favorite for each actor.

Usage:
  python ai-drama/fruit-dynasty/make_refs.py --character limon --count 4
  python ai-drama/fruit-dynasty/make_refs.py --character mango --count 4 --list
  python ai-drama/fruit-dynasty/make_refs.py --list

Rules baked in:
 - Prompt = Locked look + ", cinematic portrait, " + Style line (from series-bible.md)
 - Size = 768x1344 vertical (allowed range on FLUX Krea dev is 256-2048)
 - Saves to ai-drama/fruit-dynasty/refs/<character>/01.png, 02.png... never overwrites
 - If free GPU quota runs out, waits and retries, then tells you plainly
 - PG-13 only: prompts contain no violence, gore or suggestive content
"""

import argparse
import os
import shutil
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

# Repo root = two levels up from this file: ai-drama/fruit-dynasty/ -> repo root
REPO_ROOT = Path(__file__).resolve().parents[2]
REFS_ROOT = Path(__file__).resolve().parent / "refs"

# Verified working Space first, then fallbacks from the task.
SPACES = [
    "black-forest-labs/FLUX.1-Krea-dev",
    "mcp-tools/FLUX.1-Krea-dev",
    "black-forest-labs/FLUX.1-dev",
    "black-forest-labs/FLUX.1-schnell",
]

STYLE_LINE = (
    "photorealistic anthropomorphic fruit character, cinematic vertical 9:16, "
    "shallow depth of field, warm amber and deep green color grade, "
    "film grain, dramatic lighting, 35mm"
)

# Locked looks copied verbatim from series-bible.md
CHARACTERS = {
    "don-coco": "photorealistic coconut head with a gray coconut-fiber beard and wise dark eyes, elderly man's body, black three-piece suit, gold pocket watch, wooden cane",
    "mango": "photorealistic ripe golden-orange mango head with a small green leaf on top, confident smirk, athletic man's body, cream linen suit with open collar, gold chain",
    "limon": "photorealistic bright yellow lemon head with sharp intense eyes and a permanent frown, lean man's body, black turtleneck, gray wool overcoat, wire glasses",
    "kiwi": "photorealistic fuzzy brown kiwi fruit head, sliced open on top to show bright green flesh like hair, big innocent eyes, skinny young man's body, oversized green hoodie, headphones around neck",
    "platano": "photorealistic slightly spotted yellow banana head, tall and curved, stoic heavy-lidded eyes, broad muscular man's body, black chauffeur suit, black leather gloves, dark sunglasses",
    "don-pina": "photorealistic pineapple head with a tall spiky green crown and a golden scarred face, heavyset man's body, white suit with a red silk shirt, many gold rings, smoking a cigar",
    "el-jalapeno": "photorealistic glossy dark green jalapeño pepper head with narrow red eyes, lean man's body, long black leather coat, black gloves, standing in shadows",
    "aguacate": "photorealistic dark green bumpy avocado head, round gold glasses, older man's body, brown tweed suit, bow tie, leather briefcase",
    "uva-brothers": "two identical men, each with a photorealistic cluster of purple grapes as a head, matching black tracksuits, gold chains, standing side by side",
}

WIDTH = 768
HEIGHT = 1344


def build_prompt(character: str) -> str:
    locked = CHARACTERS[character]
    return f"{locked}, cinematic portrait, {STYLE_LINE}"


def next_index(out_dir: Path) -> int:
    """Find the next free number so we never overwrite: 01.png, 02.png..."""
    out_dir.mkdir(parents=True, exist_ok=True)
    i = 1
    while (out_dir / f"{i:02d}.png").exists():
        i += 1
    return i


def is_quota_error(msg: str) -> bool:
    m = msg.lower()
    keywords = [
        "quota", "gpu", "zero-gpu", "zero gpu", "rate limit", "429",
        "overloaded", "queue full", "capacity", "try again", "timeout",
        "503", "500", "connection", "space is sleeping", "running out",
    ]
    return any(k in m for k in keywords)


def get_client(space: str, token: str | None):
    from gradio_client import Client

    if token:
        return Client(space, hf_token=token)
    return Client(space)


def generate_one(client, prompt: str, max_retries: int = 6):
    """Call /infer with retries. Returns (result_dict, seed)."""
    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            result, seed = client.predict(
                prompt=prompt,
                seed=0,
                randomize_seed=True,
                width=WIDTH,
                height=HEIGHT,
                guidance_scale=4.5,
                num_inference_steps=28,
                api_name="/infer",
            )
            return result, seed
        except Exception as e:  # noqa: BLE001
            last_err = e
            msg = str(e)
            print(f"  Attempt {attempt}/{max_retries} failed: {msg[:300]}")
            if is_quota_error(msg) and attempt < max_retries:
                wait = 60 * attempt  # 60s, 120s, 180s...
                print(f"  Free GPU busy or quota hit. Waiting {wait}s before retry...")
                time.sleep(wait)
                # Re-create client to wake sleeping Space
                continue
            if attempt >= max_retries:
                break
            time.sleep(10)
    raise RuntimeError(f"All retries failed. Last error: {last_err}")


def save_result(result, out_path: Path):
    """result is a dict with path/url, or a filepath string."""
    if isinstance(result, dict):
        local_path = result.get("path")
        url = result.get("url")
        if local_path and os.path.exists(local_path):
            shutil.copyfile(local_path, out_path)
            return
        if url:
            # url may be http or base64 data — download it
            import urllib.request

            if url.startswith("data:"):
                import base64

                header, b64 = url.split(",", 1)
                out_path.write_bytes(base64.b64decode(b64))
                return
            urllib.request.urlretrieve(url, out_path)
            return
    if isinstance(result, str) and os.path.exists(result):
        shutil.copyfile(result, out_path)
        return
    raise RuntimeError(f"Could not save image: unexpected result type {type(result)}: {result!r}")


def main():
    load_dotenv(REPO_ROOT / ".env")
    token = os.getenv("HF_TOKEN", "").strip()
    if not token or token == "REPLACE_ME_WITH_YOUR_TOKEN":
        print("WARNING: No real HF_TOKEN found in .env.")
        print("The free Spaces often still work without a token, but you may hit")
        print("quota faster. To add one, edit repo-root .env and set HF_TOKEN=hf_...")
        print("Never paste your token in chat — only in that file.")
        token = None

    ap = argparse.ArgumentParser(description="Generate Fruit Dynasty refs (free HF Spaces)")
    ap.add_argument("--character", default="limon", help="Which character slug to generate")
    ap.add_argument("--count", type=int, default=4, help="How many images to make")
    ap.add_argument("--list", action="store_true", help="List characters and exit")
    ap.add_argument("--space", default=None, help="Force a specific Space (default: auto)")
    args = ap.parse_args()

    if args.list:
        print("Cast:")
        for k in CHARACTERS:
            print(f" - {k}")
        return

    char = args.character.lower().strip()
    # friendly aliases: limón -> limon, etc.
    aliases = {
        "limón": "limon",
        "platáno": "platano",
        "don-piña": "don-pina",
        "don-pina": "don-pina",
        "don piña": "don-pina",
        "don coco": "don-coco",
        "el-jalapeño": "el-jalapeno",
        "el jalapeño": "el-jalapeno",
        "uva brothers": "uva-brothers",
        "uvas": "uva-brothers",
    }
    char = aliases.get(char, char)
    if char not in CHARACTERS:
        print(f"Unknown character '{args.character}'. Choose from:")
        for k in CHARACTERS:
            print(f" - {k}")
        sys.exit(1)

    prompt = build_prompt(char)
    print(f"Character: {char}")
    print(f"Prompt: {prompt}")
    print(f"Size: {WIDTH}x{HEIGHT} vertical")

    out_dir = REFS_ROOT / char
    start_idx = next_index(out_dir)
    print(f"Saving to: {out_dir} (starting at {start_idx:02d}.png, never overwriting)")

    spaces_to_try = [args.space] if args.space else SPACES
    client = None
    active_space = None
    for sp in spaces_to_try:
        try:
            print(f"Trying Space: {sp} ...")
            client = get_client(sp, token)
            active_space = sp
            print(f"Connected to {sp}")
            break
        except Exception as e:  # noqa: BLE001
            print(f"  Could not connect to {sp}: {e}")
            continue

    if client is None:
        print("")
        print("Every free Space failed to connect.")
        print("Cheapest paid option: fal.ai or Replicate (pay per image, usually")
        print("a few cents each). I will not spend money without asking you first.")
        sys.exit(2)

    made = []
    for n in range(args.count):
        idx = start_idx + n
        out_path = out_dir / f"{idx:02d}.png"
        print(f"\n[{n+1}/{args.count}] Generating -> {out_path.name} ...")
        try:
            result, seed = generate_one(client, prompt)
            save_result(result, out_path)
            print(f"  Saved {out_path} (seed {seed})")
            made.append(str(out_path))
        except Exception as e:  # noqa: BLE001
            msg = str(e)
            print(f"  FAILED: {msg[:500]}")
            if is_quota_error(msg):
                print("")
                print("The free GPU quota ran out (this happens — free Spaces reset).")
                print("What to do: wait 1-2 hours and run the same command again.")
                print("Your existing images are safe — rerunning never overwrites.")
                print("If every free Space keeps failing, cheapest paid fix is")
                print("fal.ai or Replicate. I will not spend money without asking.")
            break

    print("")
    if made:
        print(f"Done! Made {len(made)} image(s) with {active_space}:")
        for m in made:
            print(f" - {m}")
        print("Open them and pick your favorite. Then tell me which one,")
        print(f"and I will save it as refs/{char}/MASTER.png")
    else:
        print("No images made this run. See message above.")
        sys.exit(3)


if __name__ == "__main__":
    main()
