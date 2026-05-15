"""Sync data/pipeline.csv → Notion pipeline database.

Reads every row in data/pipeline.csv, upserts into the Notion database
defined by NOTION_DATABASE_ID. Uses lead_id as the dedup key (stored as
the "Lead ID" property in Notion).

One-way sync: CSV is canonical. Edits in Notion are ignored on next sync
(could be overwritten). Two-way sync would require Notion webhooks +
conflict resolution; not worth it until volume justifies.

Triggered by the on-pipeline-update.yml workflow on any push that
changes data/pipeline.csv. Costs zero LLM tokens (pure REST calls).

Required env:
- NOTION_API_KEY: from https://notion.so/profile/integrations
- NOTION_DATABASE_ID: the data source ID (NOT the database id) of the
  AngelAutomates Pipeline DB. Find it in the database URL after
  collection://, e.g. 16bb09e2172b4098a01759ab490e269d.

The integration must be invited to the database via Notion UI:
  open the database → ... menu → Connections → add your integration.
"""

from __future__ import annotations

import csv
import json
import os
import pathlib
import sys
from datetime import datetime, timezone

REPO = pathlib.Path(__file__).resolve().parent.parent
PIPELINE_CSV = REPO / "data" / "pipeline.csv"
LOG = REPO / "tracker" / "log.jsonl"

NOTION_VERSION = "2022-06-28"

# Pipeline.csv columns → Notion property names (case-sensitive).
COLUMN_MAP = {
    "lead_id": "Lead ID",
    "company": "Company",
    "contact": "Contact",
    "stage": "Stage",
    "owner": "Owner",
    "next_step": "Next Step",
    "proposed_slots": "Proposed Slots",
    "booked_slot": "Booked Slot",
    "value_usd": "Value USD",
    "close_date": "Close Date",
    "onboarded_at": "Onboarded At",
    "notes": "Notes",
}

# Stage / Owner / Source values must match the Notion select options exactly.
ALLOWED_STAGES = {"new", "contacted", "replied", "interested", "scheduling",
                  "scheduled", "discovery-done", "closed-won", "closed-lost", "nurture"}
ALLOWED_OWNERS = {"me", "agent"}


def to_property_value(field: str, value: str) -> dict | None:
    """Convert a CSV string into a Notion property value object."""
    value = (value or "").strip()
    if not value:
        return None

    if field in {"company"}:
        return {"title": [{"text": {"content": value[:2000]}}]}
    if field in {"lead_id", "contact", "next_step", "proposed_slots", "notes"}:
        return {"rich_text": [{"text": {"content": value[:2000]}}]}
    if field == "stage":
        if value not in ALLOWED_STAGES:
            return None
        return {"select": {"name": value}}
    if field == "owner":
        if value not in ALLOWED_OWNERS:
            return None
        return {"select": {"name": value}}
    if field == "value_usd":
        try:
            return {"number": float(value)}
        except ValueError:
            return None
    if field in {"booked_slot", "close_date", "onboarded_at"}:
        # Accept ISO date or datetime
        return {"date": {"start": value}}
    return None


def build_properties(row: dict) -> dict:
    props: dict = {}
    for csv_field, notion_field in COLUMN_MAP.items():
        v = to_property_value(csv_field, row.get(csv_field, ""))
        if v is not None:
            props[notion_field] = v
    return props


def existing_pages(client, database_id: str) -> dict[str, str]:
    """Return {lead_id: page_id} for all existing rows."""
    out: dict[str, str] = {}
    cursor: str | None = None
    while True:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        r = client.post(
            f"https://api.notion.com/v1/databases/{database_id}/query",
            json=body,
        )
        r.raise_for_status()
        data = r.json()
        for page in data.get("results", []):
            lead_prop = page.get("properties", {}).get("Lead ID", {})
            rich = lead_prop.get("rich_text", [])
            if rich:
                lead_id = rich[0].get("plain_text", "").strip()
                if lead_id:
                    out[lead_id] = page["id"]
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
    return out


def upsert(client, database_id: str, row: dict, existing: dict[str, str]) -> str:
    lead_id = row.get("lead_id", "").strip()
    if not lead_id:
        return "skipped:no-lead-id"
    props = build_properties(row)
    if "Lead ID" not in props:
        return "skipped:no-lead-id-prop"

    if lead_id in existing:
        page_id = existing[lead_id]
        r = client.patch(
            f"https://api.notion.com/v1/pages/{page_id}",
            json={"properties": props},
        )
        r.raise_for_status()
        return "updated"
    else:
        r = client.post(
            "https://api.notion.com/v1/pages",
            json={"parent": {"database_id": database_id}, "properties": props},
        )
        r.raise_for_status()
        return "created"


def main() -> int:
    api_key = os.environ.get("NOTION_API_KEY", "").strip()
    db_id = os.environ.get("NOTION_DATABASE_ID", "").strip()
    dry_run = os.environ.get("DRY_RUN") == "1"

    if not PIPELINE_CSV.exists():
        print(f"[notion-sync] no {PIPELINE_CSV}; nothing to sync")
        return 0

    with PIPELINE_CSV.open(encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r.get("lead_id")]

    print(f"[notion-sync] {len(rows)} rows in pipeline.csv (dry_run={dry_run})")
    if not rows:
        return 0

    if dry_run:
        for r in rows[:5]:
            print(f"  - would upsert {r.get('lead_id')} stage={r.get('stage')}")
        _log(len(rows), 0, 0, dry_run=True)
        return 0

    if not api_key or not db_id:
        print("[notion-sync] NOTION_API_KEY and NOTION_DATABASE_ID required (or use --dry-run)", file=sys.stderr)
        return 2

    try:
        import httpx
    except ImportError:
        print("[notion-sync] httpx not installed; pip install httpx", file=sys.stderr)
        return 2

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }
    with httpx.Client(headers=headers, timeout=30.0) as client:
        existing = existing_pages(client, db_id)
        created = updated = 0
        for row in rows:
            try:
                result = upsert(client, db_id, row, existing)
                if result == "created":
                    created += 1
                elif result == "updated":
                    updated += 1
                print(f"[notion-sync] {row.get('lead_id')}: {result}")
            except Exception as e:
                print(f"[notion-sync] error on {row.get('lead_id')}: {e}", file=sys.stderr)

    _log(len(rows), created, updated, dry_run=False)
    print(f"[notion-sync] created={created} updated={updated}")
    return 0


def _log(rows: int, created: int, updated: int, dry_run: bool) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({
            "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "agent": "sync_pipeline_to_notion",
            "rows": rows, "created": created, "updated": updated,
            "status": "ok", "revenue_impact": 1, "dry_run": dry_run,
        }, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
