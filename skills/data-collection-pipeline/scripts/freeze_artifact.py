#!/usr/bin/env python3
"""Freeze an already-acquired artifact into a portable JSONL provenance manifest."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import time


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("artifact", type=Path)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--requested-url", required=True)
    p.add_argument("--resolved-url")
    p.add_argument("--content-type")
    p.add_argument("--http-status", type=int)
    p.add_argument("--retrieved-at")
    p.add_argument("--source-id")
    args = p.parse_args()

    artifact = args.artifact.resolve()
    manifest = args.manifest.resolve()
    if not artifact.is_file():
        raise SystemExit(f"artifact does not exist: {artifact}")

    manifest.parent.mkdir(parents=True, exist_ok=True)
    body = artifact.read_bytes()
    record = {
        "state": "FROZEN",
        "freeze_state": "FROZEN",
        "artifact_path": str(Path(artifact).relative_to(manifest.parent))
        if artifact.is_relative_to(manifest.parent)
        else str(Path(__import__("os").path.relpath(artifact, manifest.parent))),
        "requested_url": args.requested_url,
        "resolved_url": args.resolved_url or args.requested_url,
        "retrieved_at": args.retrieved_at or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "content_type": args.content_type,
        "http_status": args.http_status,
        "byte_size": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
        "source_id": args.source_id,
    }

    with manifest.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    print(json.dumps(record, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
