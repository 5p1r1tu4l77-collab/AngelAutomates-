"""Guards for the agent fleet: locks, kill-switch, daily spend cap, quotas.

Every scheduled agent calls guards.preflight() before doing any work.
Successful preflight returns None; a string return is a reason to skip
(stale lock, kill-switch on, daily budget hit, paused workflow).
"""

from __future__ import annotations

import contextlib
import json
import os
import pathlib
import time
from datetime import datetime, timezone

REPO = pathlib.Path(__file__).resolve().parent.parent
LOCKS = REPO / "tracker" / "locks"
QUOTA = REPO / "tracker" / "quota.json"
KILL_SWITCH = REPO / "tracker" / "KILL_SWITCH"
STATUS = REPO / "tracker" / "STATUS.md"

LOCK_TTL_SECONDS = 600  # a lock older than 10 minutes is stale

# Rough $/Mtoken (input, output) — update when Anthropic changes pricing.
PRICING = {
    "claude-haiku-4-5-20251001": (1.0, 5.0),
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-opus-4-7": (15.0, 75.0),
}

MONTHLY_CAP_USD = float(os.environ.get("MONTHLY_BUDGET_USD", "80"))


def _now() -> float:
    return time.time()


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    inp, out = PRICING.get(model, (3.0, 15.0))
    return round((input_tokens * inp + output_tokens * out) / 1_000_000, 6)


def _load_quota() -> dict:
    if not QUOTA.exists():
        return {"month": datetime.now(timezone.utc).strftime("%Y-%m"), "spend_usd": 0.0, "calls": {}}
    try:
        data = json.loads(QUOTA.read_text())
    except json.JSONDecodeError:
        return {"month": datetime.now(timezone.utc).strftime("%Y-%m"), "spend_usd": 0.0, "calls": {}}
    cur = datetime.now(timezone.utc).strftime("%Y-%m")
    if data.get("month") != cur:
        return {"month": cur, "spend_usd": 0.0, "calls": {}}
    return data


def _save_quota(data: dict) -> None:
    QUOTA.parent.mkdir(parents=True, exist_ok=True)
    QUOTA.write_text(json.dumps(data, indent=2) + "\n")


def record_cost(usd: float) -> None:
    if usd <= 0:
        return
    data = _load_quota()
    data["spend_usd"] = round(data.get("spend_usd", 0.0) + usd, 6)
    _save_quota(data)


def preflight(agent: str) -> str | None:
    if KILL_SWITCH.exists():
        # Only compliance-monitor and kpi-tracker run during a kill-switch.
        if agent not in {"compliance-monitor", "kpi-tracker"}:
            return f"kill-switch active: {KILL_SWITCH.read_text().strip()[:120]}"

    data = _load_quota()
    if data.get("spend_usd", 0.0) >= MONTHLY_CAP_USD:
        return f"monthly cap ${MONTHLY_CAP_USD:.0f} reached (spent ${data['spend_usd']:.2f})"

    LOCKS.mkdir(parents=True, exist_ok=True)
    lockfile = LOCKS / f"{agent}.lock"
    if lockfile.exists():
        try:
            held = json.loads(lockfile.read_text())
            age = _now() - held.get("ts", 0)
            if age < LOCK_TTL_SECONDS:
                return f"already running (lock age {int(age)}s)"
        except json.JSONDecodeError:
            pass  # malformed lock → take it
    return None


@contextlib.contextmanager
def lock(agent: str):
    LOCKS.mkdir(parents=True, exist_ok=True)
    lockfile = LOCKS / f"{agent}.lock"
    lockfile.write_text(json.dumps({"pid": os.getpid(), "ts": _now()}))
    try:
        yield
    finally:
        try:
            lockfile.unlink()
        except FileNotFoundError:
            pass


def append_status(line: str) -> None:
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with STATUS.open("a", encoding="utf-8") as f:
        f.write(f"- {stamp} — {line}\n")
