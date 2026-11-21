#!/usr/bin/env bash
set -u -o pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RAW_BASE="${LIVINGWARE_EVAL_RAW_DIR:-$ROOT/.artifacts/livingware-eval-skill-runtime/raw}"
OUT_BASE="${LIVINGWARE_EVAL_OUTPUT_DIR:-$ROOT/.artifacts/livingware-eval-skill-runtime}"
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$OUT_BASE" "$RAW_BASE" || exit 2
OUT_DIR="$(mktemp -d "$OUT_BASE/$RUN_ID-XXXXXXXX")" || exit 2
RAW_RUN_DIR="$(mktemp -d "$RAW_BASE/$RUN_ID-XXXXXXXX")" || exit 2
RUN_ID="${OUT_DIR##*/}"
RESULT="$OUT_DIR/eval-run.json"
CODEX_BIN="${CODEX_BIN:-codex}"

PYTHON_BIN="${CODEX_PROBE_PYTHON:-}"
if [[ -z "$PYTHON_BIN" ]]; then
  for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1 && "$candidate" -c 'import sys; raise SystemExit(sys.version_info < (3, 8))' >/dev/null 2>&1; then
      PYTHON_BIN="$(command -v "$candidate")"; break
    fi
  done
fi
[[ -n "$PYTHON_BIN" ]] && "$PYTHON_BIN" -c 'import sys; raise SystemExit(sys.version_info < (3, 8))' >/dev/null 2>&1 || { echo "ERROR: Python 3.8 or newer is required" >&2; exit 2; }
export CODEX_PROBE_PYTHON="$PYTHON_BIN"
repository_commit="$(git -C "$ROOT" rev-parse HEAD 2>/dev/null || true)"
livingware_version="$("$PYTHON_BIN" - "$ROOT/package.json" <<'PY'
import json, sys
print(json.load(open(sys.argv[1], encoding="utf-8"))["version"])
PY
)"

set +e
CODEX_PROBE_OUTPUT_DIR="$RAW_RUN_DIR" \
  CODEX_PROBE_RETRIES="${CODEX_PROBE_RETRIES:-1}" \
  CODEX_PROBE_TIMEOUT="${CODEX_PROBE_TIMEOUT:-180}" \
  CODEX_BIN="$CODEX_BIN" \
  bash "$ROOT/tests/codex/live-progressive-skill-probe.sh"
probe_rc=$?
set -e

summary="$(find "$RAW_RUN_DIR" -type f -name summary.tsv -print 2>/dev/null | head -1)"
if [[ -z "$summary" || ! -f "$summary" ]]; then
  echo "ERROR: live progressive-skill probe produced no summary.tsv" >&2
  exit 2
fi
codex_version="$(sed -n $'s/^codex-version\t//p' "${summary%/*}/run-info.tsv" | head -1)"

"$PYTHON_BIN" "$ROOT/scripts/compile-live-skill-eval.py" \
  "$summary" "$RESULT" \
  --probe-exit-code "$probe_rc" \
  --run-id "$RUN_ID" \
  --repository-commit "$repository_commit" \
  --livingware-version "$livingware_version" \
  --codex-version "$codex_version"

if [[ "$probe_rc" -ne 0 ]]; then
  echo "Livingware live skill-runtime eval: FAIL (source probe exit=$probe_rc)" >&2
  exit "$probe_rc"
fi

echo "Livingware live skill-runtime eval artifact: $RESULT"
