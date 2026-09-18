#!/usr/bin/env python3
"""Verify frozen artifacts against a JSONL manifest without network access."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("manifest", type=Path)
    args = p.parse_args()

    failures = []
    checked = 0
    frozen = 0
    with args.manifest.open("r", encoding="utf-8") as f:
        for lineno, raw in enumerate(f, 1):
            if not raw.strip():
                continue
            checked += 1
            record = json.loads(raw)
            if record.get("freeze_state") != "FROZEN":
                continue
            frozen += 1
            path = Path(record.get("artifact_path", ""))
            expected = record.get("sha256")
            if not path.is_file():
                failures.append({"line": lineno, "reason": "MISSING_ARTIFACT", "path": str(path)})
                continue
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if not expected or actual != expected:
                failures.append({
                    "line": lineno,
                    "reason": "HASH_MISMATCH",
                    "path": str(path),
                    "expected": expected,
                    "actual": actual,
                })

    result = {
        "manifest": str(args.manifest),
        "records_checked": checked,
        "frozen_records": frozen,
        "failures": failures,
        "state": "OFFLINE_VERIFIED" if not failures else "VERIFY_FAILED",
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if not failures else 3


if __name__ == "__main__":
    raise SystemExit(main())
