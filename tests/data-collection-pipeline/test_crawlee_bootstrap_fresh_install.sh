#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BOOT="$ROOT/skills/data-collection-pipeline/scripts/bootstrap_crawlee.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
if [[ -n "${CRAWLEE_BOOTSTRAP_TEST_RUNTIME:-}" ]]; then
  RUNTIME="$CRAWLEE_BOOTSTRAP_TEST_RUNTIME"
  rm -rf "$RUNTIME"
else
  RUNTIME="$TMP/crawlee-runtime"
fi

run_bootstrap() {
  local label="$1"
  local stdout_file="$2"
  local stderr_file="$3"
  shift 3

  set +e
  python3 "$BOOT" "$@" >"$stdout_file" 2>"$stderr_file"
  local rc=$?
  set -e

  if [[ "$rc" -ne 0 ]]; then
    echo "FAIL: $label exited with code $rc" >&2
    if [[ -s "$stdout_file" ]]; then
      echo "--- bootstrap stdout ---" >&2
      cat "$stdout_file" >&2
    fi
    if [[ -s "$stderr_file" ]]; then
      echo "--- bootstrap stderr ---" >&2
      cat "$stderr_file" >&2
    fi
    return "$rc"
  fi
}

python3 "$BOOT" --mode core --runtime-dir "$RUNTIME" --plan > "$TMP/core-plan.json"
grep -Fq '"requirement": "crawlee==1.10.1"' "$TMP/core-plan.json"
grep -Fq '"browser_extra": false' "$TMP/core-plan.json"

if python3 "$BOOT" --mode core --runtime-dir "$RUNTIME" --check-only > "$TMP/precheck.json"; then
  echo "FAIL: fresh runtime unexpectedly reported READY" >&2
  exit 1
fi
grep -Fq '"state": "MISSING_RUNTIME"' "$TMP/precheck.json"

run_bootstrap "core install" "$TMP/core-install.json" "$TMP/core-install.stderr" --mode core --runtime-dir "$RUNTIME"
grep -Fq '"state": "READY"' "$TMP/core-install.json"
grep -Fq '"installed_version": "1.10.1"' "$TMP/core-install.json"
grep -Fq '"browser_extra": false' "$TMP/core-install.json"

run_bootstrap "core check-only" "$TMP/core-check.json" "$TMP/core-check.stderr" --mode core --runtime-dir "$RUNTIME" --check-only
grep -Fq '"state": "READY"' "$TMP/core-check.json"

RUNTIME_PY="$(python3 - "$TMP/core-install.json" <<'PY'
import json, sys
print(json.load(open(sys.argv[1], encoding="utf-8"))["python_executable"])
PY
)"
"$RUNTIME_PY" - <<'PY'
import importlib.util
import importlib.metadata
assert importlib.metadata.version("crawlee") == "1.10.1"
assert importlib.util.find_spec("playwright") is None, "core bootstrap must not install browser extra"
from crawlee.crawlers import FileDownloadCrawler
assert FileDownloadCrawler
PY

python3 "$BOOT" --mode browser --runtime-dir "$RUNTIME" --skip-browser-binary --plan > "$TMP/browser-plan.json"
grep -Fq '"requirement": "crawlee[playwright]==1.10.1"' "$TMP/browser-plan.json"
grep -Fq '"browser_extra": true' "$TMP/browser-plan.json"

run_bootstrap "browser extra install" "$TMP/browser-install.json" "$TMP/browser-install.stderr" --mode browser --runtime-dir "$RUNTIME" --skip-browser-binary
grep -Fq '"state": "READY"' "$TMP/browser-install.json"
grep -Fq '"installed_version": "1.10.1"' "$TMP/browser-install.json"
grep -Fq '"browser_extra": true' "$TMP/browser-install.json"
grep -Fq '"browser_binary_installed": false' "$TMP/browser-install.json"

"$VENV_PY" - <<'PY'
import importlib.util
import importlib.metadata
assert importlib.metadata.version("crawlee") == "1.10.1"
assert importlib.util.find_spec("playwright") is not None, "browser escalation must install Playwright extra"
from crawlee.crawlers import PlaywrightCrawler
assert PlaywrightCrawler
PY

echo "PASS: fresh install lazily provisions Crawlee core, then browser extra only on escalation"
