# Notion workspace links

Created via MCP on 2026-05-15. These live in the user's personal Notion workspace; not visible to anyone else.

## Pages

- **Activation Checklist** — https://www.notion.so/3611afd6c57881f1a28dfc4ec5a409da
  Mirror of `docs/ACTIVATION-PLAN.md`. Use this to knock through the 30-min Phase 0 setup.

- **Pipeline (database)** — https://www.notion.so/e03862f62d664d099c3e9f4e1f21b4ec
  Mirror of `data/pipeline.csv`. Stage/source/owner are colored selects. Includes a Kanban board view grouped by Stage. Use to visually track leads through cold-email → reply → discovery → close.

## Move them where you want

I parented these under an existing sandbox page in your workspace ("Click me to see even more detail" → Activation Checklist → Pipeline). Drag them to a more permanent spot whenever convenient — links above will follow the move.

## Two-way sync (NOT shipped yet)

The repo's `data/pipeline.csv` is the canonical source agents read. The Notion DB is your visual review surface. They are **not synced** yet. Two paths if you want sync:

1. **CSV → Notion (one-way)**: a workflow `agent · sync-pipeline-to-notion` that reads `data/pipeline.csv` after every change and upserts rows into the Notion DB via API. Easy to build (~60 LOC). Tell me to ship it.

2. **Notion → CSV (other direction)**: requires a Notion webhook into a Cloudflare Worker → GitHub repository_dispatch. More moving parts. Recommended only if you'd rather edit pipeline state in Notion than in CSVs.

Most practical: ship #1 (read-only Notion mirror) so you have visual review without editing-conflict risk. The CSV stays the truth.
