#!/usr/bin/env bash
set -u -o pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
RAW_BASE="${LIVINGWARE_EVAL_RAW_DIR:-$ROOT/.artifacts/livingware-eval-skill-runtime/raw}"
OUT_BASE="${LIVINGWARE_EVAL_OUTPUT_DIR:-$ROOT/.artifacts/livingware-eval-skill-runtime}"
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
OUT_DIR="$OUT_BASE/$RUN_ID"
RESULT="$OUT_DIR/eval-run.json"

mkdir -p "$OUT_DIR" "$RAW_BASE"

set +e
CODEX_PROBE_OUTPUT_DIR="$RAW_BASE" \
  CODEX_PROBE_RETRIES="${CODEX_PROBE_RETRIES:-1}" \
  CODEX_PROBE_TIMEOUT="${CODEX_PROBE_TIMEOUT:-180}" \
  bash "$ROOT/tests/codex/live-progressive-skill-probe.sh"
probe_rc=$?
set -e

summary="$(find "$RAW_BASE" -type f -name summary.tsv -print 2>/dev/null | sort | tail -1)"
if [[ -z "$summary" || ! -f "$summary" ]]; then
  echo "ERROR: live progressive-skill probe produced no summary.tsv" >&2
  exit 2
fi

python3 "$ROOT/scripts/compile-live-skill-eval.py" \
  "$summary" "$RESULT" --probe-exit-code "$probe_rc"

if [[ "$probe_rc" -ne 0 ]]; then
  echo "Livingware live skill-runtime eval: FAIL (source probe exit=$probe_rc)" >&2
  exit "$probe_rc"
fi

echo "Livingware live skill-runtime eval artifact: $RESULT"
