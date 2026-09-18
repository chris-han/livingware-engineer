#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BOOT="$ROOT/skills/data-collection-pipeline/scripts/bootstrap_crawlee.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
RUNTIME="$TMP/target-runtime"

set +e
python3 "$BOOT" --mode core --backend target --runtime-dir "$RUNTIME" > "$TMP/install.json" 2> "$TMP/install.stderr"
RC=$?
set -e
if [[ "$RC" -ne 0 ]]; then
  echo "FAIL: target fallback install exited $RC" >&2
  cat "$TMP/install.json" >&2 || true
  cat "$TMP/install.stderr" >&2 || true
  exit "$RC"
fi

grep -Fq '"state": "READY"' "$TMP/install.json"
grep -Fq '"runtime_backend": "target"' "$TMP/install.json"
grep -Fq '"installed_version": "1.10.1"' "$TMP/install.json"

RUNTIME_PY="$(python3 - "$TMP/install.json" <<'PY'
import json, sys
print(json.load(open(sys.argv[1], encoding="utf-8"))["python_executable"])
PY
)"
[[ -x "$RUNTIME_PY" ]] || { echo "FAIL: target launcher not executable: $RUNTIME_PY"; exit 1; }

"$RUNTIME_PY" - <<'PY'
import importlib.metadata
import importlib.util
assert importlib.metadata.version("crawlee") == "1.10.1"
assert importlib.util.find_spec("playwright") is None
from crawlee.crawlers import FileDownloadCrawler
assert FileDownloadCrawler
PY

export PIP_NO_INDEX=1
export HTTP_PROXY="http://127.0.0.1:9"
export HTTPS_PROXY="http://127.0.0.1:9"
export ALL_PROXY="http://127.0.0.1:9"

python3 "$BOOT" --mode core --runtime-dir "$RUNTIME" --offline > "$TMP/offline.json"
grep -Fq '"state": "READY"' "$TMP/offline.json"
grep -Fq '"runtime_backend": "target"' "$TMP/offline.json"
grep -Fq '"installed_dependency": false' "$TMP/offline.json"

echo "PASS: target-directory fallback installs and reuses Crawlee without stdlib venv"
