#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / "tests" / "data-collection-pipeline" / "fixtures" / "tender-law-historical-v1.json"
DEFAULT_REPO = Path("/home/chris/repo/semantier-runtime")


def git_bytes(repo: Path, spec: str) -> bytes:
    proc = subprocess.run(
        ["git", "-C", str(repo), "show", spec],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.decode("utf-8", errors="replace").strip())
    return proc.stdout


def git_text(repo: Path, spec: str) -> str:
    return git_bytes(repo, spec).decode("utf-8")


def validate_fixture_shape(data: dict) -> None:
    assert data["schema_version"] == "1.0"
    assert re.fullmatch(r"[0-9a-f]{40}", data["source_commit"])
    assert data["status_manifest_path"].endswith("下载状态.tsv")
    assert len(data["artifacts"]) >= 2
    for item in data["artifacts"]:
        assert item["status"] == "SUCCESS"
        assert item["path"].endswith(".pdf")
        assert item["source_url"].startswith("https://")
        assert re.fullmatch(r"[0-9a-f]{40}", item["git_blob_sha"])
        assert re.fullmatch(r"[0-9a-f]{64}", item["sha256"])
        assert item["byte_size"] > 0


def parse_status_tsv(text: str) -> dict[str, tuple[str, str, str]]:
    rows = {}
    for raw in text.splitlines():
        if not raw.strip():
            continue
        name, status, digest, source_url = raw.split("\t")
        rows[name] = (status, digest, source_url)
    return rows


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repo", type=Path, default=Path(os.environ.get("SEMANTIER_RUNTIME_ROOT", DEFAULT_REPO)))
    p.add_argument("--require-external", action="store_true", default=os.environ.get("REQUIRE_TENDER_LAW_FIXTURE") == "1")
    args = p.parse_args()

    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    validate_fixture_shape(data)

    repo = args.repo
    probe = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--git-dir"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if probe.returncode != 0:
        if args.require_external:
            raise SystemExit(f"required Semantier repository unavailable: {repo}")
        print(f"SKIP: external tender-law fixture repository unavailable at {repo}")
        return 0

    commit = data["source_commit"]
    manifest_text = git_text(repo, f"{commit}:{data['status_manifest_path']}")
    status_rows = parse_status_tsv(manifest_text)

    for item in data["artifacts"]:
        basename = Path(item["path"]).name
        assert basename in status_rows, f"missing historical status row: {basename}"
        status, digest, source_url = status_rows[basename]
        assert status == item["status"]
        assert digest == item["sha256"]
        assert source_url == item["source_url"]

        blob = git_bytes(repo, f"{commit}:{item['path']}")
        assert blob.startswith(b"%PDF-"), f"not a PDF: {item['path']}"
        assert len(blob) == item["byte_size"], f"size mismatch: {item['path']}"
        actual = hashlib.sha256(blob).hexdigest()
        assert actual == item["sha256"], f"SHA-256 mismatch: {item['path']}"

        git_sha = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", f"{commit}:{item['path']}"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout.strip()
        assert git_sha == item["git_blob_sha"], f"Git blob mismatch: {item['path']}"

    print(
        "PASS: historical tender-law PDFs match pinned Git blobs, historical 下载状态.tsv, "
        "byte sizes, PDF magic, source URLs, and SHA-256"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
