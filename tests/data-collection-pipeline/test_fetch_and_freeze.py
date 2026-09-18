#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import http.server
import json
from pathlib import Path
import socketserver
import subprocess
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "skills" / "data-collection-pipeline" / "scripts" / "fetch_and_freeze.py"
VERIFY = ROOT / "skills" / "data-collection-pipeline" / "scripts" / "verify_frozen.py"
PAYLOAD = b"public-corpus-payload\n"


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/ok.pdf":
            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.end_headers()
            self.wfile.write(PAYLOAD)
        elif self.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "/ok.pdf")
            self.end_headers()
        elif self.path == "/auth":
            self.send_response(401)
            self.end_headers()
        elif self.path == "/forbidden":
            self.send_response(403)
            self.end_headers()
        elif self.path == "/missing":
            self.send_response(404)
            self.end_headers()
        elif self.path == "/rate":
            self.send_response(429)
            self.end_headers()
        else:
            self.send_response(500)
            self.end_headers()

    def log_message(self, fmt, *args):
        pass


def run(url: str, out: Path):
    return subprocess.run(
        [str(SCRIPT), url, "--output-dir", str(out), "--retrieved-at", "2026-09-18T00:00:00Z"],
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    with socketserver.TCPServer(("127.0.0.1", 0), Handler) as server:
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_address[1]}"
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ok = run(base + "/redirect", root / "ok")
            assert ok.returncode == 0, ok.stderr
            ok_record = json.loads(ok.stdout)
            assert ok_record["state"] == "SUCCESS"
            assert ok_record["http_status"] == 200
            assert ok_record["resolved_url"].endswith("/ok.pdf")
            assert ok_record["sha256"] == hashlib.sha256(PAYLOAD).hexdigest()
            assert Path(ok_record["artifact_path"]).read_bytes() == PAYLOAD
            manifest_path = root / "ok" / "manifest.jsonl"
            manifest_row = json.loads(manifest_path.read_text().strip())
            assert manifest_row["freeze_state"] == "FROZEN"

            verified = subprocess.run([str(VERIFY), str(manifest_path)], text=True, capture_output=True, check=False)
            assert verified.returncode == 0
            verify_record = json.loads(verified.stdout)
            assert verify_record["state"] == "OFFLINE_VERIFIED"

            Path(ok_record["artifact_path"]).write_bytes(b"tampered")
            tampered = subprocess.run([str(VERIFY), str(manifest_path)], text=True, capture_output=True, check=False)
            assert tampered.returncode == 3
            tampered_record = json.loads(tampered.stdout)
            assert tampered_record["state"] == "VERIFY_FAILED"
            assert tampered_record["failures"][0]["reason"] == "HASH_MISMATCH"

            expected = {
                "/auth": "AUTH_REQUIRED",
                "/forbidden": "ACCESS_DENIED",
                "/missing": "NOT_FOUND",
                "/rate": "RATE_LIMITED",
            }
            for path, state in expected.items():
                result = run(base + path, root / state.lower())
                assert result.returncode == 2
                record = json.loads(result.stdout)
                assert record["state"] == state
                assert record["freeze_state"] == "NOT_FROZEN"

        server.shutdown()

    print("PASS: fetch_and_freeze classifies blocked routes and freezes successful bytes with provenance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
