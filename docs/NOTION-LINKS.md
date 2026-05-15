# Notion workspace links

Created via MCP on 2026-05-15. These live in the user's personal Notion workspace; not visible to anyone else.

## Pages

- **Activation Checklist** — https://www.notion.so/3611afd6c57881f1a28dfc4ec5a409da
  Mirror of `docs/ACTIVATION-PLAN.md`. Use this to knock through the 30-min Phase 0 setup.

- **Pipeline (database)** — https://www.notion.so/e03862f62d664d099c3e9f4e1f21b4ec
  Mirror of `data/pipeline.csv`. Stage/source/owner are colored selects. Includes a Kanban board view grouped by Stage. Use to visually track leads through cold-email → reply → discovery → close.

## Move them where you want

I parented these under an existing sandbox page in your workspace ("Click me to see even more detail" → Activation Checklist → Pipeline). Drag them to a more permanent spot whenever convenient — links above will follow the move.

## Two-way sync

The repo's `data/pipeline.csv` is the canonical source agents read. The Notion DB is your visual review surface.

**Shipped: one-way CSV → Notion sync.** `scripts/sync_pipeline_to_notion.py` + `.github/workflows/on-pipeline-sync-notion.yml`. Triggers on every push that touches `data/pipeline.csv`. Upserts by `lead_id`.

To activate (5 min, one-time):

1. Go to https://notion.so/profile/integrations → "+ New integration".
2. Name it `AngelAutomates Sync`. Type: Internal. Workspace: yours.
3. Copy the "Internal Integration Token". Add it to GitHub repo secrets as `NOTION_API_KEY`.
4. Open the [Pipeline database](https://www.notion.so/e03862f62d664d099c3e9f4e1f21b4ec) → `...` menu → Connections → search "AngelAutomates Sync" → confirm.
5. Add `NOTION_DATABASE_ID` repo secret with value `e03862f62d664d099c3e9f4e1f21b4ec` (the DB id from the URL).
6. Push any change to `data/pipeline.csv` (or run the workflow_dispatch manually). Rows appear in Notion within 30 seconds.

If you want **Notion → CSV** (the other direction): requires Notion webhook + Cloudflare Worker + GitHub repository_dispatch. More moving parts. Recommended only if you'd rather edit pipeline state in Notion than in CSVs. Tell me to build it.

Most practical for now: keep the one-way mirror. CSV stays the truth; Notion is the visual review surface.
