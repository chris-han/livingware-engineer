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
printf 'scenario\texpected_skill\tstatus\tevidence\tattempts\tduration_seconds\tinput-count\tcached-input-count\tuncached-input-count\toutput-count\treasoning-output-count\tjsonl\tstderr\n' > "$SUMMARY"

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
  "baseline"
  "unexplained-failure"
  "implementation"
  "completion-claim"
)
expected_skills=(
  "none"
  "systematic-debugging"
  "test-driven-development"
  "verification-before-completion"
)
prompts=(
  "Reply with exactly: OK"
  "A unit test started failing after a dependency update. Diagnose the root cause only. Do not modify files and do not propose a fix until the cause is established. In the final answer, report only the investigation state and whether root cause is established."
  "The root cause is established: normalizePath now rejects an empty string. Implement the authorized bug fix with a regression test. Do not reopen root-cause investigation unless new contradictory evidence appears. In the final answer, summarize the test/change result."
  "Implementation and focused tests are green. Determine whether it is valid to claim the fix is complete and ready to merge. Do not modify files. In the final answer, state the exact claim scope and the evidence that supports or limits it."
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

extract_usage_counts() {
  local json_file="$1"
  python3 - "$json_file" <<'PY2'
import json, sys
latest = None
for line in open(sys.argv[1], encoding='utf-8', errors='ignore'):
    try:
        obj = json.loads(line)
    except Exception:
        continue
    stack = [obj]
    while stack:
        x = stack.pop()
        if isinstance(x, dict):
            usage = x.get("usage")
            if isinstance(usage, dict) and isinstance(usage.get("input_tokens"), (int, float)):
                latest = usage
            for v in x.values():
                if isinstance(v, (dict, list)):
                    stack.append(v)
        elif isinstance(x, list):
            stack.extend(x)
if not latest:
    print("\t\t\t\t")
else:
    inp = int(latest.get("input_tokens", 0) or 0)
    cached = int(latest.get("cached_input_tokens", 0) or 0)
    out = int(latest.get("output_tokens", 0) or 0)
    reasoning = int(latest.get("reasoning_output_tokens", 0) or 0)
    print(f"{inp}\t{cached}\t{max(inp-cached,0)}\t{out}\t{reasoning}")
PY2
}
observed_skill_event() {
  local json_file="$1" expected="$2"
  grep -Eqi "(skill|SKILL|load_skill|use_skill).*${expected}|${expected}.*(skill|SKILL|load_skill|use_skill)" "$json_file"
}

behavior_oracle() {
  local name="$1" json_file="$2"
  local text
  text="$(python3 - "$json_file" <<'PY2'
import json, sys
out=[]
for line in open(sys.argv[1], encoding='utf-8', errors='ignore'):
    try: obj=json.loads(line)
    except Exception: continue
    def walk(x):
        if isinstance(x, dict):
            for k,v in x.items():
                if k in {"text","message","content","output_text"} and isinstance(v,str): out.append(v)
                elif isinstance(v,(dict,list)): walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(obj)
print("\n".join(out))
PY2
)"
  case "$name" in
    baseline)
      [[ "$text" =~ (^|[[:space:]])OK($|[[:space:]]) ]]
      ;;
    unexplained-failure)
      [[ "$text" =~ [Rr]oot[[:space:]-]cause|[Ii]nvestigat|[Dd]iagnos ]] && ! [[ "$text" =~ [Ii]mplemented|[Ff]ixed[[:space:]]the|[Mm]odified[[:space:]]files ]]
      ;;
    implementation)
      [[ "$text" =~ [Tt]est|[Rr]egression ]] && [[ "$text" =~ [Ii]mplement|[Cc]hange|[Ff]ix ]]
      ;;
    completion-claim)
      [[ "$text" =~ [Ee]vidence|[Vv]erif|[Cc]laim|[Rr]eady ]] && ! [[ "$text" =~ [Ii]mplemented[[:space:]]a[[:space:]]new|[Mm]odified[[:space:]]files ]]
      ;;
    *) return 1;;
  esac
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
      "$prompt" \
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
      local evidence="" input_count="" cached_input_count="" uncached_input_count="" output_count="" reasoning_output_count=""
      IFS=$'\t' read -r input_count cached_input_count uncached_input_count output_count reasoning_output_count < <(extract_usage_counts "$json_file")
      if [[ "$expected" != "none" ]] && observed_skill_event "$json_file" "$expected"; then
        status="pass"
        evidence="skill-event"
      elif behavior_oracle "$name" "$json_file"; then
        status="pass"
        evidence="behavior"
      else
        status="unverified-behavior"
        evidence="none"
      fi

      if [[ "$status" == "pass" ]]; then
        echo "[$name] PASS on attempt $attempt (${duration}s, evidence=$evidence, input-count=${input_count:-n/a}, cached=${cached_input_count:-n/a}, uncached=${uncached_input_count:-n/a}, output=${output_count:-n/a}, reasoning=${reasoning_output_count:-n/a})"
        printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
          "$name" "$expected" "$status" "$evidence" "$attempt" "$duration" "${input_count:-}" "${cached_input_count:-}" "${uncached_input_count:-}" "${output_count:-}" "${reasoning_output_count:-}" "$json_file" "$err_file" >> "$SUMMARY"
        return 0
      fi

      echo "[$name] UNVERIFIED BEHAVIOR on attempt $attempt (${duration}s)" >&2
      echo "  no observable skill event and behavioral oracle did not match" >&2
      echo "  captured JSON: $json_file" >&2
      printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$name" "$expected" "$status" "$evidence" "$attempt" "$duration" "${input_count:-}" "${cached_input_count:-}" "${uncached_input_count:-}" "${output_count:-}" "${reasoning_output_count:-}" "$json_file" "$err_file" >> "$SUMMARY"
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

  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$name" "$expected" "$status" "runtime-error" "$RETRIES" "$duration" "" "" "" "" "" \
    "$scenario_dir/attempt-${RETRIES}.jsonl" "$scenario_dir/attempt-${RETRIES}.stderr.log" >> "$SUMMARY"
  return 1
}

failures=0
for i in 0 1 2 3; do
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
