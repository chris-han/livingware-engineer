#!/usr/bin/env bash
set -u -o pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT_BASE="${CODEX_PROBE_OUTPUT_DIR:-$ROOT/.artifacts/codex-progressive-skill-probe}"
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
RUN_DIR="$OUT_BASE/$RUN_ID"
RETRIES="${CODEX_PROBE_RETRIES:-3}"
TIMEOUT_SECONDS="${CODEX_PROBE_TIMEOUT:-120}"
BACKOFF_SECONDS="${CODEX_PROBE_BACKOFF:-5}"
CODEX_BIN="${CODEX_BIN:-codex}"

mkdir -p "$RUN_DIR"
SUMMARY="$RUN_DIR/summary.tsv"
printf 'scenario\texpected_skill\tstatus\tattempts\tduration_seconds\tjsonl\tstderr\n' > "$SUMMARY"

command -v "$CODEX_BIN" >/dev/null 2>&1 || {
  echo "ERROR: Codex CLI not found: $CODEX_BIN" >&2
  exit 2
}
command -v timeout >/dev/null 2>&1 || {
  echo "ERROR: GNU timeout is required" >&2
  exit 2
}

if ! [[ "$RETRIES" =~ ^[1-9][0-9]*$ ]]; then
  echo "ERROR: CODEX_PROBE_RETRIES must be a positive integer" >&2
  exit 2
fi
if ! [[ "$TIMEOUT_SECONDS" =~ ^[1-9][0-9]*$ ]]; then
  echo "ERROR: CODEX_PROBE_TIMEOUT must be a positive integer" >&2
  exit 2
fi

scenario_names=(
  "unexplained-failure"
  "implementation"
  "completion-claim"
)
expected_skills=(
  "systematic-debugging"
  "test-driven-development"
  "verification-before-completion"
)
prompts=(
  "A unit test started failing after a dependency update. Diagnose the root cause only. Do not modify files and do not propose a fix until the cause is established."
  "The root cause is established: normalizePath now rejects an empty string. Implement the authorized bug fix with a regression test."
  "Implementation and focused tests are green. Determine whether it is valid to claim the fix is complete and ready to merge."
)

classify_failure() {
  local rc="$1" stderr_file="$2" json_file="$3"
  if [[ "$rc" -eq 124 ]]; then
    printf 'timeout'
    return
  fi
  if grep -Eqi 'request timed out|reconnecting|backend-api|transport channel closed|connection|network|auth|unauthorized|forbidden' "$stderr_file" "$json_file" 2>/dev/null; then
    printf 'backend-failure'
    return
  fi
  printf 'codex-error'
}

probe_one() {
  local name="$1" expected="$2" prompt="$3"
  local attempt rc start end duration status="failed"
  local scenario_dir="$RUN_DIR/$name"
  mkdir -p "$scenario_dir"

  echo "=== Scenario: $name (expected: $expected) ==="

  for ((attempt=1; attempt<=RETRIES; attempt++)); do
    local json_file="$scenario_dir/attempt-${attempt}.jsonl"
    local err_file="$scenario_dir/attempt-${attempt}.stderr.log"
    local meta_file="$scenario_dir/attempt-${attempt}.meta.txt"
    start="$(date +%s)"

    echo "[$name] attempt $attempt/$RETRIES (timeout=${TIMEOUT_SECONDS}s)"
    timeout "$TIMEOUT_SECONDS" "$CODEX_BIN" exec \
      --json \
      --ephemeral \
      --sandbox read-only \
      -C "$ROOT" \
      "$prompt Before doing any work, state the single Livingware workflow skill governing the current state exactly as SKILL=<name>. Do not name multiple workflow skills." \
      >"$json_file" 2>"$err_file"
    rc=$?
    end="$(date +%s)"
    duration=$((end-start))

    {
      echo "scenario=$name"
      echo "expected_skill=$expected"
      echo "attempt=$attempt"
      echo "exit_code=$rc"
      echo "duration_seconds=$duration"
      echo "jsonl=$json_file"
      echo "stderr=$err_file"
    } > "$meta_file"

    if [[ "$rc" -eq 0 ]]; then
      if grep -Fq "SKILL=$expected" "$json_file"; then
        status="pass"
        echo "[$name] PASS on attempt $attempt (${duration}s)"
        printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
          "$name" "$expected" "$status" "$attempt" "$duration" "$json_file" "$err_file" >> "$SUMMARY"
        return 0
      fi

      status="routing-mismatch"
      echo "[$name] ROUTING MISMATCH on attempt $attempt (${duration}s)" >&2
      echo "  expected marker: SKILL=$expected" >&2
      echo "  captured JSON: $json_file" >&2
      printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$name" "$expected" "$status" "$attempt" "$duration" "$json_file" "$err_file" >> "$SUMMARY"
      return 1
    fi

    status="$(classify_failure "$rc" "$err_file" "$json_file")"
    echo "[$name] $status on attempt $attempt (exit=$rc, ${duration}s)" >&2
    echo "  JSON:   $json_file" >&2
    echo "  stderr: $err_file" >&2

    if (( attempt < RETRIES )); then
      echo "[$name] retrying after ${BACKOFF_SECONDS}s..." >&2
      sleep "$BACKOFF_SECONDS"
    fi
  done

  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$name" "$expected" "$status" "$RETRIES" "$duration" \
    "$scenario_dir/attempt-${RETRIES}.jsonl" "$scenario_dir/attempt-${RETRIES}.stderr.log" >> "$SUMMARY"
  return 1
}

failures=0
for i in 0 1 2; do
  if ! probe_one "${scenario_names[$i]}" "${expected_skills[$i]}" "${prompts[$i]}"; then
    failures=$((failures+1))
  fi
done

echo
echo "Captured probe artifacts: $RUN_DIR"
echo "Summary: $SUMMARY"
cat "$SUMMARY"

if (( failures > 0 )); then
  echo "Live Codex progressive-skill probe: FAIL ($failures scenario(s))" >&2
  exit 1
fi

echo "Live Codex progressive-skill probe: PASS"
