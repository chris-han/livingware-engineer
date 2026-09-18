#!/usr/bin/env python3
"""Fetch a public URL and freeze deterministic provenance into a JSONL manifest.

Standard-library only. Intended for already-discovered candidate URLs, not crawling.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request


def classify_status(status: int) -> str:
    if 200 <= status < 300:
        return "SUCCESS"
    if status == 401:
        return "AUTH_REQUIRED"
    if status == 403:
        return "ACCESS_DENIED"
    if status in (404, 410):
        return "NOT_FOUND"
    if status == 429:
        return "RATE_LIMITED"
    if 400 <= status < 500:
        return "CLIENT_ERROR"
    if 500 <= status < 600:
        return "SERVER_ERROR"
    return "HTTP_OTHER"


def safe_name(url: str, explicit: str | None, content_type: str | None) -> str:
    if explicit:
        return explicit
    path_name = Path(urllib.parse.urlparse(url).path).name
    if path_name:
        return path_name
    ext = mimetypes.guess_extension((content_type or "").split(";", 1)[0].strip()) or ".bin"
    return f"artifact{ext}"


def append_manifest(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def fetch(url: str, timeout: float, user_agent: str) -> tuple[dict, bytes | None]:
    req = urllib.request.Request(url, headers={"User-Agent": user_agent})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            status = int(resp.status)
            headers = resp.headers
            final_url = resp.geturl()
    except urllib.error.HTTPError as e:
        body = e.read()
        status = int(e.code)
        headers = e.headers
        final_url = e.geturl()
    except (urllib.error.URLError, TimeoutError) as e:
        return ({
            "state": "TRANSPORT_ERROR",
            "requested_url": url,
            "error": str(e),
        }, None)

    content_type = headers.get("Content-Type") if headers else None
    record = {
        "state": classify_status(status),
        "requested_url": url,
        "resolved_url": final_url,
        "http_status": status,
        "content_type": content_type,
        "content_length": len(body),
    }
    return record, body


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("url")
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--manifest", type=Path)
    p.add_argument("--name")
    p.add_argument("--timeout", type=float, default=30.0)
    p.add_argument("--user-agent", default="livingware-data-collection/1.0")
    p.add_argument("--retrieved-at", help="Optional fixed timestamp for reproducible tests")
    args = p.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest = args.manifest or (args.output_dir / "manifest.jsonl")
    record, body = fetch(args.url, args.timeout, args.user_agent)
    record["retrieved_at"] = args.retrieved_at or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    if record["state"] == "SUCCESS" and body is not None:
        filename = safe_name(record.get("resolved_url", args.url), args.name, record.get("content_type"))
        target = args.output_dir / filename
        target.write_bytes(body)
        digest = hashlib.sha256(body).hexdigest()
        record.update({
            "artifact_path": str(target),
            "sha256": digest,
            "byte_size": len(body),
            "freeze_state": "FROZEN",
        })
    else:
        record["freeze_state"] = "NOT_FROZEN"

    append_manifest(manifest, record)
    print(json.dumps(record, ensure_ascii=False, sort_keys=True))
    return 0 if record["state"] == "SUCCESS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
