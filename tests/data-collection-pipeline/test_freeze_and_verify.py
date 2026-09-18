#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
FREEZE = ROOT / "skills" / "data-collection-pipeline" / "scripts" / "freeze_artifact.py"
VERIFY = ROOT / "skills" / "data-collection-pipeline" / "scripts" / "verify_frozen.py"
PAYLOAD = b"public-corpus-payload\n"


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        corpus = root / "corpus"
        corpus.mkdir()
        artifact = corpus / "document.pdf"
        artifact.write_bytes(PAYLOAD)
        manifest = corpus / "manifest.jsonl"

        frozen = subprocess.run(
            [
                sys.executable,
                str(FREEZE),
                str(artifact),
                "--manifest",
                str(manifest),
                "--requested-url",
                "https://example.test/document.pdf",
                "--resolved-url",
                "https://cdn.example.test/document.pdf",
                "--content-type",
                "application/pdf",
                "--http-status",
                "200",
                "--retrieved-at",
                "2026-09-18T00:00:00Z",
                "--source-id",
                "fixture-document",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        assert frozen.returncode == 0, frozen.stderr
        row = json.loads(frozen.stdout)
        assert row["freeze_state"] == "FROZEN"
        assert row["sha256"] == hashlib.sha256(PAYLOAD).hexdigest()
        assert row["artifact_path"] == "document.pdf"
        assert json.loads(manifest.read_text())["source_id"] == "fixture-document"

        verified = subprocess.run(
            [sys.executable, str(VERIFY), str(manifest)],
            text=True,
            capture_output=True,
            check=False,
        )
        assert verified.returncode == 0, verified.stderr
        assert json.loads(verified.stdout)["state"] == "OFFLINE_VERIFIED"

        artifact.write_bytes(b"tampered")
        tampered = subprocess.run(
            [sys.executable, str(VERIFY), str(manifest)],
            text=True,
            capture_output=True,
            check=False,
        )
        assert tampered.returncode == 3
        result = json.loads(tampered.stdout)
        assert result["state"] == "VERIFY_FAILED"
        assert result["failures"][0]["reason"] == "HASH_MISMATCH"

    print("PASS: local freezer records portable provenance and offline verification detects tampering")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
