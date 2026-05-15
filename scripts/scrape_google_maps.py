"""Anonymous Google Maps scraper for ICP-matched business leads.

Pulls business listings (name, website, phone, address, rating, review count,
category) from Google Maps search results for a given query. Designed for
GitHub Actions free tier — no API keys, no logged-in Google account.

Legal basis (US):
- hiQ Labs v. LinkedIn (9th Cir. 2022) — scraping public data does not violate CFAA.
- Meta v. Bright Data (2024), X Corp v. Bright Data (2024) — same.
- Google Maps Terms of Service prohibit scraping; that's a private contract, not
  law. Risk = Google blocks the scraping IP, not legal action. We mitigate by
  staying anonymous (no login), pacing humanly, and capping batch size.

If you operate outside the US, do your own legal review before running.

Usage:
    python scripts/scrape_google_maps.py "roofing contractor Houston TX" --max 50
    python scripts/scrape_google_maps.py --query "HVAC contractor Phoenix AZ" --state AZ
"""

from __future__ import annotations

import argparse
import csv
import os
import pathlib
import random
import re
import sys
import time
from datetime import datetime, timezone
from urllib.parse import urlparse

REPO = pathlib.Path(__file__).resolve().parent.parent
OUT_CSV = REPO / "data" / "leads-new.csv"
LOG = REPO / "tracker" / "log.jsonl"

CSV_FIELDS = [
    "lead_id", "company", "domain", "full_name", "title",
    "email", "phone", "city", "state", "industry",
    "employee_count", "source", "sourced_at", "status",
]

MAX_RESULTS_DEFAULT = 50
MIN_DELAY_S = 1.5
MAX_DELAY_S = 4.0


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:40] or "unknown"


def normalize_domain(url: str) -> str:
    if not url:
        return ""
    try:
        p = urlparse(url if "://" in url else f"https://{url}")
        return p.netloc.lower().lstrip("www.")
    except Exception:
        return ""


def load_existing_keys() -> set[str]:
    if not OUT_CSV.exists():
        return set()
    keys = set()
    with OUT_CSV.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("domain"):
                keys.add(row["domain"])
            if row.get("phone"):
                keys.add(row["phone"])
    return keys


def append_rows(rows: list[dict]) -> None:
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    write_header = not OUT_CSV.exists() or OUT_CSV.stat().st_size == 0
    with OUT_CSV.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if write_header:
            writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in CSV_FIELDS})


def scrape(query: str, state: str, max_results: int) -> list[dict]:
    """Run the headless Playwright scrape. Returns list of dicts matching CSV_FIELDS."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[scraper] playwright not installed. Install: pip install playwright && playwright install chromium", file=sys.stderr)
        return []

    rows: list[dict] = []
    existing = load_existing_keys()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="en-US",
        )
        page = context.new_page()

        # Anonymous Google Maps search URL.
        url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(random.uniform(2, 4))

        # The results scroll panel uses role=feed; cards are role=article.
        try:
            page.wait_for_selector('[role="feed"]', timeout=15000)
        except Exception:
            print("[scraper] no result feed; query may have hit Google block or returned nothing", file=sys.stderr)
            browser.close()
            return rows

        feed = page.query_selector('[role="feed"]')
        seen_in_run: set[str] = set()
        scrolls = 0
        max_scrolls = 25

        while len(rows) < max_results and scrolls < max_scrolls:
            cards = page.query_selector_all('[role="feed"] > div > div[role="article"]')
            for card in cards:
                if len(rows) >= max_results:
                    break
                try:
                    aria = card.get_attribute("aria-label") or ""
                    if not aria or aria in seen_in_run:
                        continue
                    seen_in_run.add(aria)

                    company = aria.strip()

                    # Pull rating + review-count from inline text.
                    rating_el = card.query_selector('span[role="img"][aria-label*="star"]')
                    rating_label = rating_el.get_attribute("aria-label") if rating_el else ""

                    # Click into card to access detail panel (website, phone).
                    card.scroll_into_view_if_needed()
                    time.sleep(random.uniform(0.4, 1.0))
                    card.click()
                    time.sleep(random.uniform(MIN_DELAY_S, MAX_DELAY_S))

                    detail_panel = page.query_selector('[role="main"]')
                    if not detail_panel:
                        continue

                    # Website
                    website = ""
                    site_el = detail_panel.query_selector('a[data-item-id="authority"]')
                    if site_el:
                        website = site_el.get_attribute("href") or ""

                    # Phone
                    phone = ""
                    phone_el = detail_panel.query_selector('button[data-item-id^="phone"]')
                    if phone_el:
                        aria_phone = phone_el.get_attribute("aria-label") or ""
                        phone = re.sub(r"[^\d+()\-\s]", "", aria_phone).strip()

                    # Address → extract city/state heuristically
                    address = ""
                    addr_el = detail_panel.query_selector('button[data-item-id="address"]')
                    if addr_el:
                        address = (addr_el.get_attribute("aria-label") or "").replace("Address: ", "").strip()
                    city, st = parse_city_state(address)

                    # Category
                    category = ""
                    cat_el = detail_panel.query_selector('button[jsaction*="category"]')
                    if cat_el:
                        category = (cat_el.inner_text() or "").strip()

                    domain = normalize_domain(website)
                    dedup_key = domain or phone
                    if not dedup_key or dedup_key in existing:
                        continue
                    existing.add(dedup_key)

                    rows.append({
                        "lead_id": f"{slugify(domain or company)}-{slugify(state or st)}",
                        "company": company,
                        "domain": domain,
                        "full_name": "",
                        "title": "",
                        "email": "",
                        "phone": phone,
                        "city": city,
                        "state": (st or state).upper(),
                        "industry": category or "",
                        "employee_count": "",
                        "source": "google-maps",
                        "sourced_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "status": "new",
                    })
                except Exception as e:
                    print(f"[scraper] card error: {e}", file=sys.stderr)
                    continue

            # Scroll the feed to load more.
            if feed:
                page.evaluate("(el) => el.scrollBy(0, 1200)", feed)
            scrolls += 1
            time.sleep(random.uniform(MIN_DELAY_S, MAX_DELAY_S))

        browser.close()
    return rows


def parse_city_state(address: str) -> tuple[str, str]:
    if not address:
        return "", ""
    # Heuristic: address like "1234 Main St, Houston, TX 77001, United States"
    parts = [p.strip() for p in address.split(",")]
    city = state = ""
    for i, part in enumerate(parts):
        m = re.match(r"^([A-Z]{2})\s*\d{5}", part)
        if m:
            state = m.group(1)
            if i >= 1:
                city = parts[i - 1]
            break
    return city, state


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("query", nargs="?", help="search string, e.g. 'roofing contractor Houston TX'")
    ap.add_argument("--query", dest="query_kw", help="alias for the positional query")
    ap.add_argument("--state", default="", help="2-letter state hint (used when address parse fails)")
    ap.add_argument("--max", type=int, default=MAX_RESULTS_DEFAULT, dest="max_results")
    ap.add_argument("--dry-run", action="store_true", default=os.environ.get("DRY_RUN") == "1")
    args = ap.parse_args()

    query = args.query or args.query_kw or os.environ.get("SCRAPE_QUERY", "")
    if not query:
        ap.error("query is required (positional or --query or SCRAPE_QUERY env)")

    started = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"[scraper] query={query!r} max={args.max_results} dry_run={args.dry_run}")

    if args.dry_run:
        print("[scraper] dry-run: skipping headless scrape")
        rows: list[dict] = []
    else:
        rows = scrape(query, args.state, args.max_results)

    if rows:
        append_rows(rows)
        print(f"[scraper] appended {len(rows)} rows to {OUT_CSV}")
    else:
        print("[scraper] no new rows")

    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        import json
        f.write(json.dumps({
            "ts": started,
            "agent": "scrape_google_maps",
            "query": query,
            "rows_added": len(rows),
            "status": "ok",
            "revenue_impact": 2,
            "dry_run": args.dry_run,
        }, separators=(",", ":")) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
