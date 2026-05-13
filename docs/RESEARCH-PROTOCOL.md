# Research protocol — how agents handle "I don't know"

When an agent encounters a knowledge gap (a new tool, a niche term, a policy change, a competitor move), it must NOT guess. It must follow this protocol.

## When to invoke

Trigger conditions:
- An agent reads a doc that references something undefined.
- A reply or lead mentions a competitor, product, or term the agent doesn't recognize.
- `growth-strategist`'s weekly review needs evidence for a hypothesis.
- `ai-tool-watcher`'s scan finds a new tool worth evaluating.
- A failure mode the playbook doesn't cover.

## Steps

1. **Confirm the gap is real.** Re-read the immediate context. If the answer is already in `docs/RESEARCH.md` or `docs/PLAYBOOK.md`, use it.
2. **Cost-check.** Research uses Sonnet + WebFetch. Each research run costs ~$0.02–$0.10. If the goal-active state forbids spend (e.g. zero-dollar goal), defer and log to `tracker/STATUS.md` with `research-deferred:<topic>`.
3. **Decompose the question.** Write 2–5 specific sub-questions that would resolve the gap. Vague questions waste budget.
4. **Source plan.** For each sub-question, pick the most authoritative source type:
   - Tool docs > vendor blog > 3rd-party tutorial > Reddit/HN
   - Primary research paper > journalist write-up > LinkedIn post
   - Pricing page > review aggregator > YouTube reviewer
5. **Fetch.** Use WebFetch (or in a future iteration, a tools-with-search agent). Cap at 3 fetches per research task. If you need more, escalate.
6. **Synthesize.** Write a 200–500 word brief at `docs/research/<topic-slug>.md` with:
   - The question
   - The answer (3–7 bullets)
   - Source URLs (real, retrievable)
   - Confidence (high/med/low)
   - Stale-by date (when this should be re-researched)
7. **Cross-reference.** Update `docs/RESEARCH.md` Part 6 (open questions) — mark the question answered or split into deeper sub-questions.
8. **Log.** `tracker/log.jsonl` entry with `agent: <invoking_agent>, action: research, topic: <slug>, sources: [...], confidence: <level>`.

## When to make our own tool

If research reveals no tool exists that gets us the results we want, the criteria for building it ourselves:

| Criterion | Threshold |
|-----------|-----------|
| Estimated build time | ≤ 1 week of human + agent work |
| Recurring cost saved | ≥ 3× the build's API cost over 90 days |
| Maintenance burden | ≤ 30 min/week ongoing |
| Strategic depth | Does this differentiate vs competitors? |

If yes to all four, file an issue tagged `build-tool` and `growth-strategist` adds it to the weekly experiment queue.

If no, document the gap in `docs/research/gaps.md` for re-evaluation in a quarter.

## Anti-patterns (do NOT do these)

- **Cargo-cult research.** Don't fetch 10 sources because "more is better." Three good sources beat ten mediocre ones.
- **Confirmation bias.** If first 3 sources agree, that's a signal — verify with a 4th that disagrees in principle.
- **Fabricating URLs.** Never. If you can't retrieve a real URL, write "no source found" and downgrade confidence.
- **Locking yourself into a vendor.** Research that ends with "use X" should also note "switching cost if X disappears".
- **Stale dependency.** Every research brief has a stale-by date. If used past that date, re-research first.

## Example: how `ai-tool-watcher` answers "is there a cheaper Smartlead alternative?"

1. Sub-questions: (a) Which tools offer multi-inbox warmup at <$30/mo? (b) What do their deliverability benchmarks look like? (c) Is the API parity good enough to drop-in replace?
2. Sources: Smartlead pricing page, Instantly pricing page, Smartlead vs Instantly comparison reviews, Reddit r/Coldemail recent threads (last 60 days), GlockApps quarterly inbox report.
3. Synthesis at `docs/research/smartlead-alternatives-2026.md`.
4. Conclusion + confidence + stale-by 90 days.
5. If a cheaper alt is viable, `growth-strategist` adds an A/B experiment for next week.
