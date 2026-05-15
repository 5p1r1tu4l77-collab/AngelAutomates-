"""Send approved cold-email drafts via Gmail SMTP using an app password.

Free, no third-party SMTP service required. The user generates a 16-digit
Gmail app password (account.google.com/apppasswords) and stores it as the
GitHub Actions secret `GMAIL_APP_PASSWORD`. Sender address as `GMAIL_USER`.

Reads each `*.md` file in data/drafts/_approved/, parses the structured
header (subject, body, lead metadata), sends via Gmail SMTP, then moves
the file to data/drafts/_sent/<YYYY-MM-DD>/<lead_id>.md.

Hard-capped at GMAIL_DAILY_CAP (default 25) sends per run to stay well
under Gmail's 500/day limit and avoid spam-flag risk on cold outreach.

Draft file format expected (markdown with simple key:value frontmatter):
    ---
    lead_id: <id>
    to: name@example.com
    subject: short subject
    ---
    body of the email here
    multi-line ok
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import smtplib
import sys
import time
from datetime import datetime, timezone
from email.message import EmailMessage

REPO = pathlib.Path(__file__).resolve().parent.parent
APPROVED = REPO / "data" / "drafts" / "_approved"
SENT_ROOT = REPO / "data" / "drafts" / "_sent"
LOG = REPO / "tracker" / "log.jsonl"
SUPPRESSION = REPO / "data" / "suppression.csv"
KILL_SWITCH = REPO / "tracker" / "KILL_SWITCH"

GMAIL_HOST = "smtp.gmail.com"
GMAIL_PORT = 587
DEFAULT_DAILY_CAP = 25
INTER_SEND_PAUSE_S = 90  # 90 sec between sends to look human


def parse_draft(path: pathlib.Path) -> tuple[dict, str]:
    raw = path.read_text(encoding="utf-8")
    meta: dict[str, str] = {}
    body = raw
    if raw.startswith("---\n"):
        end = raw.find("\n---\n", 4)
        if end != -1:
            for line in raw[4:end].splitlines():
                if ":" in line:
                    k, _, v = line.partition(":")
                    meta[k.strip().lower()] = v.strip()
            body = raw[end + 5 :].strip()
    return meta, body


def load_suppressed_domains() -> set[str]:
    if not SUPPRESSION.exists():
        return set()
    domains: set[str] = set()
    import csv
    with SUPPRESSION.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            d = (row.get("domain") or "").strip().lower()
            if d:
                domains.add(d)
    return domains


def is_suppressed(email: str, suppressed: set[str]) -> bool:
    return email.split("@", 1)[-1].lower() in suppressed


def send_one(server: smtplib.SMTP, sender: str, to: str, subject: str, body: str) -> None:
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    server.send_message(msg)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cap", type=int, default=int(os.environ.get("GMAIL_DAILY_CAP", DEFAULT_DAILY_CAP)))
    ap.add_argument("--dry-run", action="store_true", default=os.environ.get("DRY_RUN") == "1")
    args = ap.parse_args()

    started = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if KILL_SWITCH.exists():
        reason = KILL_SWITCH.read_text(encoding="utf-8").strip()[:200]
        print(f"[gmail] kill-switch active: {reason}", file=sys.stderr)
        return 0

    user = os.environ.get("GMAIL_USER", "").strip()
    pw = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
    if not args.dry_run and (not user or not pw):
        print("[gmail] GMAIL_USER and GMAIL_APP_PASSWORD must be set (or use --dry-run)", file=sys.stderr)
        return 2

    if not APPROVED.exists():
        print(f"[gmail] no {APPROVED} dir; nothing to send")
        return 0

    drafts = sorted(APPROVED.glob("*.md"))
    if not drafts:
        print("[gmail] no approved drafts")
        return 0
    drafts = drafts[: args.cap]

    suppressed = load_suppressed_domains()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    sent_dir = SENT_ROOT / today
    sent_dir.mkdir(parents=True, exist_ok=True)

    sent = 0
    skipped: list[tuple[str, str]] = []

    if args.dry_run:
        print(f"[gmail] dry-run: would send {len(drafts)} drafts (cap={args.cap})")
        for d in drafts:
            meta, _ = parse_draft(d)
            print(f"  - {d.name} → {meta.get('to', '?')}")
        _log_summary(started, sent=0, skipped=[(d.name, "dry-run") for d in drafts], dry_run=True)
        return 0

    server = smtplib.SMTP(GMAIL_HOST, GMAIL_PORT, timeout=30)
    server.starttls()
    server.login(user, pw)

    try:
        for i, draft in enumerate(drafts):
            meta, body = parse_draft(draft)
            to = meta.get("to", "")
            subject = meta.get("subject", "")
            if not to or not subject:
                skipped.append((draft.name, "missing to/subject in frontmatter"))
                continue
            if is_suppressed(to, suppressed):
                skipped.append((draft.name, "suppressed domain"))
                continue
            try:
                send_one(server, user, to, subject, body)
                shutil.move(str(draft), str(sent_dir / draft.name))
                sent += 1
                print(f"[gmail] sent {draft.name} → {to}")
            except Exception as e:
                skipped.append((draft.name, f"smtp error: {e}"))
                print(f"[gmail] error sending {draft.name}: {e}", file=sys.stderr)
            if i + 1 < len(drafts):
                time.sleep(INTER_SEND_PAUSE_S)
    finally:
        server.quit()

    _log_summary(started, sent, skipped, dry_run=False)
    print(f"[gmail] sent={sent} skipped={len(skipped)}")
    return 0


def _log_summary(started: str, sent: int, skipped: list[tuple[str, str]], dry_run: bool) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({
            "ts": started,
            "agent": "send_via_gmail",
            "sent": sent,
            "skipped": [{"file": fn, "reason": r} for fn, r in skipped],
            "status": "ok" if not skipped or sent > 0 else "partial",
            "revenue_impact": 3,
            "dry_run": dry_run,
        }, separators=(",", ":")) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
