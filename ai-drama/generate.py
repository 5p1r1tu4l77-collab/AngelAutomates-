#!/usr/bin/env python3
"""Generate production-ready micro-drama episode scripts with Claude.

Reads series-bible.md + season-1-outline.md, uses episodes/ep01.md as the
format example, and writes one file per episode (shot list, AI prompts,
dialogue, SFX, post kit) into episodes/ (or episodes-es/ for Spanish).

Usage:
    pip install anthropic
    export ANTHROPIC_API_KEY=sk-ant-...

    python generate.py 6-10            # write episodes 6 through 10
    python generate.py 6-30            # the rest of the season
    python generate.py 1-30 --lang es  # Spanish version of the whole season
    python generate.py 7 --force       # regenerate one episode
    python generate.py 6 --dry-run     # print the prompt, no API call
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODEL = "claude-opus-5-5"

SYSTEM_INSTRUCTIONS = """You are the head writer and AI-video director of a vertical micro-drama series.
You write episodes that are 60-90 seconds long, shot entirely with AI image/video tools.

Every episode you write must:
- Open with conflict in the first line. No slow establishing shots.
- End on a cliffhanger: a reveal, a threat, a door opening, a phone ringing.
- Stay under 120 words of total dialogue. Faces and reactions carry the scene.
- Use only the character [TAGS] and location [TAGS] from the series bible, so the
  production team can paste the locked looks in and keep characters consistent.
- Follow the episode's line in the season outline exactly, and stay consistent
  with the previous episode.
- Use only fictional people, brands, and companies.
- Match the exact markdown structure of the example episode: title, runtime/location/cast
  line, on-screen hook text, a shot list table with the same columns, an end card,
  and a post kit (caption with hashtags, pinned comment, Spanish caption).

Output only the episode markdown, with no preamble."""


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_range(spec: str) -> list[int]:
    if "-" in spec:
        start, end = (int(x) for x in spec.split("-", 1))
        return list(range(start, end + 1))
    return [int(spec)]


def out_dir(lang: str) -> Path:
    return ROOT / ("episodes" if lang == "en" else f"episodes-{lang}")


def build_system() -> list[dict]:
    # Stable across every episode, so it's cached after the first request.
    context = (
        f"{SYSTEM_INSTRUCTIONS}\n\n"
        f"<series_bible>\n{read(ROOT / 'series-bible.md')}\n</series_bible>\n\n"
        f"<season_outline>\n{read(ROOT / 'season-1-outline.md')}\n</season_outline>\n\n"
        f"<example_episode>\n{read(ROOT / 'episodes' / 'ep01.md')}\n</example_episode>"
    )
    return [{"type": "text", "text": context, "cache_control": {"type": "ephemeral"}}]


def build_user_prompt(ep: int, lang: str) -> str:
    parts = []
    english = out_dir("en") / f"ep{ep:02d}.md"
    previous = out_dir(lang) / f"ep{ep - 1:02d}.md"
    if not previous.exists():
        previous = out_dir("en") / f"ep{ep - 1:02d}.md"
    if ep > 1 and previous.exists():
        parts.append(f"<previous_episode>\n{read(previous)}\n</previous_episode>")

    if lang == "es" and english.exists():
        parts.append(f"<english_episode>\n{read(english)}\n</english_episode>")
        parts.append(
            f"Translate episode {ep} into natural Latin American Spanish for a "
            "telenovela-loving audience. Keep the shot list, timings, and visual prompts "
            "in English (the AI video tools work best in English), but translate the "
            "title, hook text, all dialogue, the end card, and the post kit. Replace the "
            "post kit's Spanish caption line with an English caption line."
        )
    elif lang == "es":
        parts.append(
            f"Write episode {ep} directly in natural Latin American Spanish. Keep the "
            "visual prompts in English; write the title, hook text, dialogue, end card, "
            "and post kit in Spanish, with an English caption line instead of a Spanish one."
        )
    else:
        parts.append(f"Write episode {ep} of the season, following its line in the outline.")
    return "\n\n".join(parts)


def generate(client, ep: int, lang: str) -> str:
    with client.beta.messages.stream(
        model=MODEL,
        max_tokens=64000,
        system=build_system(),
        messages=[{"role": "user", "content": build_user_prompt(ep, lang)}],
        output_config={"effort": "high"},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    ) as stream:
        message = stream.get_final_message()

    if message.stop_reason == "refusal":
        raise RuntimeError(f"episode {ep}: request was declined ({message.stop_details})")
    if message.stop_reason == "max_tokens":
        raise RuntimeError(f"episode {ep}: output was cut off at max_tokens")
    text = "".join(block.text for block in message.content if block.type == "text")
    return text.strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("episodes", help="episode number or range, e.g. 6 or 6-30")
    parser.add_argument("--lang", choices=["en", "es"], default="en")
    parser.add_argument("--force", action="store_true", help="overwrite episodes that already exist")
    parser.add_argument("--dry-run", action="store_true", help="print the prompt for the first episode and exit")
    args = parser.parse_args()

    episodes = parse_range(args.episodes)
    if args.dry_run:
        print(build_system()[0]["text"])
        print("\n" + "=" * 60 + "\n")
        print(build_user_prompt(episodes[0], args.lang))
        return 0

    try:
        import anthropic
    except ImportError:
        print("Missing dependency: run `pip install anthropic` first.", file=sys.stderr)
        return 1

    client = anthropic.Anthropic()
    target = out_dir(args.lang)
    target.mkdir(exist_ok=True)

    for ep in episodes:
        path = target / f"ep{ep:02d}.md"
        if path.exists() and not args.force:
            print(f"skip  {path.relative_to(ROOT)} (exists; use --force to redo)")
            continue
        print(f"write {path.relative_to(ROOT)} ...", flush=True)
        try:
            path.write_text(generate(client, ep, args.lang), encoding="utf-8")
        except anthropic.AuthenticationError:
            print("Authentication failed: set ANTHROPIC_API_KEY.", file=sys.stderr)
            return 1
        except anthropic.RateLimitError:
            print(f"Rate limited on episode {ep}. Wait a minute and rerun; finished episodes are skipped.", file=sys.stderr)
            return 1
        except (anthropic.APIStatusError, anthropic.APIConnectionError, RuntimeError) as err:
            print(f"Failed on episode {ep}: {err}", file=sys.stderr)
            return 1
    print("done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
