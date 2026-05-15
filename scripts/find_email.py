"""Extract a best-guess owner email from each unenriched lead's website.

For each row in data/leads-new.csv with status='new' and empty email, fetch
the homepage, look for /contact and /about, and pull email candidates from
mailto: links and visible text. Writes the email back to the row plus a
confidence score (0–3).

Confidence:
- 3: email on /contact with a personal-looking local part (john@..., james@...)
- 2: email on homepage / footer with a personal-looking local part
- 1: generic mailbox (info@, contact@, hello@, office@)
- 0: nothing found

Costs nothing. No API keys. Run after scrape_google_maps.py.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import pathlib
import re
import sys
import time
from datetime import datetime, timezone

REPO = pathlib.Path(__file__).resolve().parent.parent
CSV_PATH = REPO / "data" / "leads-new.csv"
LOG = REPO / "tracker" / "log.jsonl"

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
GENERIC_LOCALS = {"info", "contact", "hello", "office", "support", "admin", "sales", "team", "mail", "general"}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

MAX_FETCHES_PER_LEAD = 2
TIMEOUT_S = 10
SLEEP_S = 1.0


def score_email(email: str) -> int:
    local = email.split("@", 1)[0].lower()
    if local in GENERIC_LOCALS:
        return 1
    if re.match(r"^[a-z]+\.?[a-z]*$", local) and 2 <= len(local) <= 20:
        return 2  # looks like a personal email
    return 1


def find_in_html(html: str, domain: str) -> list[tuple[str, int]]:
    """Return [(email, base_score), ...] preferring on-domain matches."""
    if not html or not domain:
        return []
    found: dict[str, int] = {}
    for raw in EMAIL_RE.findall(html):
        e = raw.lower()
        if e.endswith(("@example.com", "@sentry.io", "@wixpress.com")):
            continue
        s = score_email(e)
        if e.endswith("@" + domain):
            s += 1  # prefer on-domain
        found[e] = max(s, found.get(e, 0))
    return sorted(found.items(), key=lambda kv: -kv[1])


def try_fetch(client, url: str) -> str:
    try:
        r = client.get(url, timeout=TIMEOUT_S, follow_redirects=True)
        if r.status_code == 200 and "text/html" in r.headers.get("content-type", ""):
            return r.text
    except Exception as e:
        print(f"[find_email] fetch fail {url}: {e}", file=sys.stderr)
    return ""


def enrich_row(client, row: dict) -> tuple[str, int]:
    """Return (email, confidence). Empty email if nothing found."""
    domain = row.get("domain", "").strip()
    if not domain:
        return "", 0
    base = f"https://{domain}"
    pages = [base, f"{base}/contact", f"{base}/about", f"{base}/team"]
    fetched = 0
    best: tuple[str, int] = ("", 0)
    for u in pages:
        if fetched >= MAX_FETCHES_PER_LEAD:
            break
        html = try_fetch(client, u)
        fetched += 1
        if not html:
            continue
        results = find_in_html(html, domain)
        if results:
            email, score = results[0]
            if score > best[1]:
                best = (email, min(score, 3))
            if score >= 3:
                break
        time.sleep(SLEEP_S)
    return best


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=25, help="max leads to enrich this run")
    ap.add_argument("--dry-run", action="store_true", default=os.environ.get("DRY_RUN") == "1")
    args = ap.parse_args()

    if not CSV_PATH.exists():
        print(f"[find_email] no {CSV_PATH}; nothing to do")
        return 0

    rows: list[dict] = []
    with CSV_PATH.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames or []

    if "email_confidence" not in fieldnames:
        fieldnames = list(fieldnames) + ["email_confidence"]

    targets = [r for r in rows if r.get("status") == "new" and not r.get("email")][: args.limit]
    print(f"[find_email] {len(targets)} candidates to enrich (limit={args.limit}, dry_run={args.dry_run})")
    if not targets or args.dry_run:
        if args.dry_run:
            with LOG.open("a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "agent": "find_email",
                    "candidates": len(targets),
                    "status": "ok",
                    "dry_run": True,
                    "revenue_impact": 3,
                }, separators=(",", ":")) + "\n")
        return 0

    found = 0
    try:
        import httpx
    except ImportError:
        print("[find_email] httpx not installed; install: pip install httpx", file=sys.stderr)
        return 1
    with httpx.Client(headers=HEADERS) as client:
        for row in targets:
            email, conf = enrich_row(client, row)
            if email:
                row["email"] = email
                row["email_confidence"] = str(conf)
                found += 1
                print(f"[find_email] {row['domain']} -> {email} (c={conf})")
            else:
                row["email_confidence"] = "0"

    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            for k in fieldnames:
                r.setdefault(k, "")
            writer.writerow(r)

    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({
            "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "agent": "find_email",
            "candidates": len(targets),
            "found": found,
            "status": "ok",
            "revenue_impact": 3,
            "dry_run": False,
        }, separators=(",", ":")) + "\n")
    print(f"[find_email] enriched {found}/{len(targets)} leads")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
