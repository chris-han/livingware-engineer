#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "data-collection-pipeline" / "fixtures" / "ccgp-blocked-recovery-v1.json"
POLICY = ROOT / "skills" / "data-collection-pipeline" / "scripts" / "recovery_policy.py"


def load_policy():
    spec = importlib.util.spec_from_file_location("recovery_policy", POLICY)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert data["schema_version"] == "1.0"
    assert data["recovery_invariant"] == "A blocked entry point is not evidence that the source is unavailable."
    assert set(data["observed_failure_taxonomy"]) == {
        "LOGIN_REQUIRED",
        "HOST_NOT_ALLOWLISTED",
        "ATTACHMENT_HTTP_FAILURE",
    }

    entries = {item["project_id"]: item for item in data["verified_public_entries"]}
    assert entries["CZ2026-0323"]["announcement_url"].endswith("t20260618_26778683.htm")
    assert entries["CZ2026-0323"]["official_attachment_host"] == "gdgpo.czt.gd.gov.cn"
    assert entries["CZ2026-0323"]["attachment_count_observed"] == 6
    assert entries["N5100012026001757"]["announcement_url"].endswith("t20260708_26897346.htm")
    assert entries["N5100012026001757"]["official_attachment_host"] == "gpx.ccgp-sichuan.gov.cn"
    assert entries["N5100012026001757"]["attachment_count_observed"] == 1

    policy = load_policy()
    observed = {}
    for scenario in data["scenarios"]:
        actual = policy.decide_recovery(scenario["input"])
        observed[scenario["id"]] = actual
        assert actual == scenario["expected"], (
            f"{scenario['id']}: expected {scenario['expected']}, got {actual}"
        )

    # The central regression: recovery routes always win before blocked retry.
    assert observed["same-site-recovers-before-blocked-retry"] == "USE_RECOVERED_ROUTE"
    assert observed["alternate-source-recovers-before-blocked-retry"] == "USE_RECOVERED_ROUTE"

    # Authentication is not bot handling.
    assert observed["401-never-auto-escalates"] == "STOP_AUTH_REQUIRED"

    # A blocked retry is conditional and bounded, not a generic second chance.
    assert observed["403-public-bot-block-may-escalate-once"] == "BLOCKED_RETRY_ONCE"
    assert observed["403-access-boundary-does-not-escalate"] == "STOP_ACCESS_BOUNDARY"
    assert observed["429-waits-before-escalation"] == "WAIT_RATE_LIMIT"
    assert observed["429-after-backoff-may-escalate-once"] == "BLOCKED_RETRY_ONCE"
    assert observed["blocked-retry-is-never-open-ended"] == "STOP_AFTER_BOUNDED_RETRY"

    print("PASS: CCGP blocked-recovery regression preserves recovery-before-retry ordering")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
