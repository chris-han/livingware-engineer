#!/usr/bin/env python3
"""Deterministic blocked-recovery routing for the data-collection pipeline."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


RECOVERED = {"FOUND_OFFICIAL_SOURCE", "FOUND_PUBLIC_ANNOUNCEMENT", "FOUND_PUBLIC_ATTACHMENT"}


def decide_recovery(case: dict[str, Any]) -> str:
    """Return the next acquisition state without performing network access."""
    if case.get("alternate_source") in RECOVERED or case.get("same_site_alternate_entry") in RECOVERED:
        return "USE_RECOVERED_ROUTE"

    status = case.get("http_status")
    initial_failure = case.get("initial_failure")
    attempts = int(case.get("blocked_retry_attempts") or 0)

    if status == 401 or initial_failure == "LOGIN_REQUIRED":
        return "STOP_AUTH_REQUIRED"

    if attempts >= 1:
        return "STOP_AFTER_BOUNDED_RETRY"

    if status == 429:
        if not bool(case.get("rate_backoff_respected")):
            return "WAIT_RATE_LIMIT"
        return "BLOCKED_RETRY_ONCE"

    if status == 403:
        public = bool(case.get("public_resource_confirmed"))
        interpretation = case.get("blocked_interpretation")
        if public and interpretation == "SESSION_OR_BOT_BLOCK":
            return "BLOCKED_RETRY_ONCE"
        return "STOP_ACCESS_BOUNDARY"

    if initial_failure == "HOST_NOT_ALLOWLISTED":
        return "STOP_ENVIRONMENT_OR_ALLOWLIST"

    return "STOP_UNRESOLVED"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("case_json", type=Path)
    args = p.parse_args()
    payload = json.loads(args.case_json.read_text(encoding="utf-8"))
    print(decide_recovery(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
