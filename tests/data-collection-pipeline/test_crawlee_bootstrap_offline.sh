#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BOOT="$ROOT/skills/data-collection-pipeline/scripts/bootstrap_crawlee.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

CACHE="${CRAWLEE_BOOTSTRAP_TEST_RUNTIME:-}"
if [[ -z "$CACHE" ]]; then
  echo "FAIL: CRAWLEE_BOOTSTRAP_TEST_RUNTIME must point to the cache created by the fresh-install test" >&2
  exit 1
fi
[[ -x "$CACHE/venv/bin/python" ]] || { echo "FAIL: expected cached runtime at $CACHE" >&2; exit 1; }

# Poison all package/network routes. Offline/check-only behavior must still work.
export PIP_NO_INDEX=1
export PIP_INDEX_URL="http://127.0.0.1:9/simple"
export PIP_FIND_LINKS="$TMP/empty-wheelhouse"
export HTTP_PROXY="http://127.0.0.1:9"
export HTTPS_PROXY="http://127.0.0.1:9"
export ALL_PROXY="http://127.0.0.1:9"
mkdir -p "$PIP_FIND_LINKS"

python3 "$BOOT" --mode core --runtime-dir "$CACHE" --offline > "$TMP/offline-core.json"
grep -Fq '"state": "READY"' "$TMP/offline-core.json"
grep -Fq '"installed_version": "1.10.1"' "$TMP/offline-core.json"
grep -Fq '"installed_dependency": false' "$TMP/offline-core.json"
grep -Fq '"offline": true' "$TMP/offline-core.json"

python3 "$BOOT" --mode core --runtime-dir "$CACHE" --check-only > "$TMP/check-core.json"
grep -Fq '"state": "READY"' "$TMP/check-core.json"
grep -Fq '"installed_dependency": false' "$TMP/check-core.json"

# Browser Python extra was installed by the fresh-install test, but Chromium was intentionally not.
python3 "$BOOT" --mode browser --runtime-dir "$CACHE" --offline --skip-browser-binary > "$TMP/offline-browser-extra.json"
grep -Fq '"state": "READY"' "$TMP/offline-browser-extra.json"
grep -Fq '"installed_dependency": false' "$TMP/offline-browser-extra.json"

if python3 "$BOOT" --mode browser --runtime-dir "$CACHE" --offline > "$TMP/offline-browser-binary.json"; then
  echo "FAIL: offline browser mode unexpectedly claimed Chromium readiness" >&2
  exit 1
fi
grep -Fq '"state": "OFFLINE_BROWSER_BINARY_MISSING"' "$TMP/offline-browser-binary.json"

# Cache miss and check-only must not create any runtime.
MISS="$TMP/missing-runtime"
if python3 "$BOOT" --mode core --runtime-dir "$MISS" --offline > "$TMP/offline-miss.json"; then
  echo "FAIL: offline cache miss unexpectedly succeeded" >&2
  exit 1
fi
grep -Fq '"state": "OFFLINE_CACHE_MISS"' "$TMP/offline-miss.json"
[[ ! -e "$MISS" ]] || { echo "FAIL: offline mode mutated missing runtime" >&2; exit 1; }

CHECK_MISS="$TMP/check-missing-runtime"
if python3 "$BOOT" --mode core --runtime-dir "$CHECK_MISS" --check-only > "$TMP/check-miss.json"; then
  echo "FAIL: check-only cache miss unexpectedly succeeded" >&2
  exit 1
fi
grep -Fq '"state": "MISSING_RUNTIME"' "$TMP/check-miss.json"
[[ ! -e "$CHECK_MISS" ]] || { echo "FAIL: check-only mutated missing runtime" >&2; exit 1; }

# Force installation failure without network. The bootstrap should return structured state, not a traceback.
FAIL_RUNTIME="$TMP/install-failure-runtime"
set +e
python3 "$BOOT" --mode core --runtime-dir "$FAIL_RUNTIME" > "$TMP/install-failure.json" 2> "$TMP/install-failure.stderr"
RC=$?
set -e
[[ "$RC" -eq 6 ]] || { echo "FAIL: expected install failure exit 6, got $RC"; cat "$TMP/install-failure.json"; cat "$TMP/install-failure.stderr"; exit 1; }
grep -Fq '"state": "INSTALL_FAILED"' "$TMP/install-failure.json"
if grep -Fq "Traceback" "$TMP/install-failure.stderr"; then
  echo "FAIL: install failure leaked traceback instead of structured result" >&2
  cat "$TMP/install-failure.stderr"
  exit 1
fi

# A failed installation leaves no false-ready cache; check-only remains non-mutating.
if python3 "$BOOT" --mode core --runtime-dir "$FAIL_RUNTIME" --check-only > "$TMP/post-failure-check.json"; then
  echo "FAIL: failed installation cache unexpectedly reported READY" >&2
  exit 1
fi
grep -Eq '"state": "(MISSING_CRAWLEE|VERSION_MISMATCH|CAPABILITY_MISMATCH)"' "$TMP/post-failure-check.json"

echo "PASS: offline cache reuse, no-network failure, and check-only behavior are deterministic"
