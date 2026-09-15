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
PROBE_WORKDIR="${CODEX_PROBE_WORKDIR:-}"

setup_fixture() {
  if [[ -n "$PROBE_WORKDIR" ]]; then
    [[ -d "$PROBE_WORKDIR" ]] || { echo "ERROR: CODEX_PROBE_WORKDIR does not exist: $PROBE_WORKDIR" >&2; exit 2; }
    return
  fi

  PROBE_WORKDIR="${TMPDIR:-/tmp}/livingware-codex-probe-$RUN_ID"
  rm -rf "$PROBE_WORKDIR"
  mkdir -p "$PROBE_WORKDIR/src" "$PROBE_WORKDIR/tests"

  cat > "$PROBE_WORKDIR/package.json" <<'JSON'
{"name":"livingware-progressive-probe-fixture","private":true,"type":"module","scripts":{"test":"node --test tests/*.test.js"}}
JSON
  cat > "$PROBE_WORKDIR/src/normalize-path.js" <<'JS'
export function normalizePath(value) {
  if (value === '') throw new Error('empty path');
  return value.replace(/\\+/g, '/').replace(/\/$/, '');
}
JS
  cat > "$PROBE_WORKDIR/tests/normalize-path.test.js" <<'JS'
import test from 'node:test';
import assert from 'node:assert/strict';
import { normalizePath } from '../src/normalize-path.js';
test('normalizes duplicate separators', () => assert.equal(normalizePath('a\\\\b/'), 'a/b'));
test('empty path remains empty', () => assert.equal(normalizePath(''), ''));
JS
  git -C "$PROBE_WORKDIR" init -q
  git -C "$PROBE_WORKDIR" config user.email probe@example.invalid
  git -C "$PROBE_WORKDIR" config user.name "Livingware Probe"
  git -C "$PROBE_WORKDIR" add .
  git -C "$PROBE_WORKDIR" commit -qm "fixture: failing normalizePath baseline"
}

setup_fixture
mkdir -p "$RUN_DIR"
SUMMARY="$RUN_DIR/summary.tsv"
printf 'probe-workdir\t%s\n' "$PROBE_WORKDIR" > "$RUN_DIR/run-info.tsv"
printf 'scenario\trequired_skill\tforbidden_skills\trouting\tbehavior\truntime\tattempts\tduration_seconds\tinput-count\tcached-input-count\tuncached-input-count\toutput-count\treasoning-output-count\tjsonl\tstderr\n' > "$SUMMARY"

command -v "$CODEX_BIN" >/dev/null 2>&1 || { echo "ERROR: Codex CLI not found: $CODEX_BIN" >&2; exit 2; }
command -v timeout >/dev/null 2>&1 || { echo "ERROR: GNU timeout is required" >&2; exit 2; }
[[ "$RETRIES" =~ ^[1-9][0-9]*$ ]] || { echo "ERROR: CODEX_PROBE_RETRIES must be positive" >&2; exit 2; }
[[ "$TIMEOUT_SECONDS" =~ ^[1-9][0-9]*$ ]] || { echo "ERROR: CODEX_PROBE_TIMEOUT must be positive" >&2; exit 2; }

scenario_names=("baseline" "unexplained-failure" "implementation" "completion-claim")
required_skills=("none" "systematic-debugging" "test-driven-development" "verification-before-completion")
forbidden_skills=(
  "systematic-debugging,test-driven-development,verification-before-completion"
  "test-driven-development,verification-before-completion"
  "systematic-debugging,verification-before-completion"
  "systematic-debugging,test-driven-development"
)
prompts=(
  "Reply with exactly: OK"
  "A unit test started failing after a dependency update. Diagnose the root cause only. Do not modify files and do not propose a fix until the cause is established. In the final answer, report only the investigation state and whether root cause is established."
  "The root cause is established: normalizePath now rejects an empty string. Implement the authorized bug fix with a regression test. Do not reopen root-cause investigation unless new contradictory evidence appears. In the final answer, summarize the test/change result."
  "Implementation and focused tests are green. Determine whether it is valid to claim the fix is complete and ready to merge. Do not modify files. In the final answer, state the exact claim scope and the evidence that supports or limits it."
)
scenario_sandboxes=("read-only" "read-only" "workspace-write" "read-only")

classify_runtime_failure() {
  local rc="$1" stderr_file="$2" json_file="$3"
  if [[ "$rc" -eq 124 ]]; then printf 'timeout'; return; fi
  if grep -Eqi 'request timed out|reconnecting|backend-api|transport channel closed|connection|network|auth|unauthorized|forbidden' "$stderr_file" "$json_file" 2>/dev/null; then
    printf 'backend-failure'
  else
    printf 'error'
  fi
}

extract_usage_counts() {
  python3 - "$1" <<'PY'
import json, sys
latest=None
for line in open(sys.argv[1], encoding='utf-8', errors='ignore'):
    try: obj=json.loads(line)
    except Exception: continue
    stack=[obj]
    while stack:
        x=stack.pop()
        if isinstance(x,dict):
            u=x.get('usage')
            if isinstance(u,dict) and isinstance(u.get('input_tokens'),(int,float)): latest=u
            stack.extend(v for v in x.values() if isinstance(v,(dict,list)))
        elif isinstance(x,list): stack.extend(x)
if not latest: print('\t\t\t\t')
else:
    inp=int(latest.get('input_tokens',0) or 0); cached=int(latest.get('cached_input_tokens',0) or 0)
    out=int(latest.get('output_tokens',0) or 0); reasoning=int(latest.get('reasoning_output_tokens',0) or 0)
    print(f'{inp}\t{cached}\t{max(inp-cached,0)}\t{out}\t{reasoning}')
PY
}

observed_skill_event() {
  local json_file="$1" skill="$2"
  python3 - "$json_file" "$skill" <<'PY'
import json, re, sys

json_file, skill = sys.argv[1], sys.argv[2]
path_re = re.compile(rf'(?:^|[/\\])skills[/\\]{re.escape(skill)}[/\\]SKILL\.md(?:$|[\s"\'`])', re.I)
explicit_marker_keys = {
    'type', 'event', 'event_type', 'kind', 'name', 'tool_name', 'function',
    'function_name', 'action', 'operation', 'op', 'command'
}

def flatten_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from flatten_strings(v)
    elif isinstance(value, list):
        for v in value:
            yield from flatten_strings(v)

def is_explicit_skill_record(obj):
    if not isinstance(obj, dict):
        return False
    marker_values = []
    for key in explicit_marker_keys:
        value = obj.get(key)
        if isinstance(value, str):
            marker_values.append(value)
    marker = ' '.join(marker_values).lower()
    payload = '\n'.join(flatten_strings(obj))

    # Strong evidence 1: a structured event/tool/action whose marker itself is
    # skill-specific and whose payload names the target skill.
    if 'skill' in marker and skill.lower() in payload.lower():
        return True

    # Strong evidence 2: an executed/read command or structured record refers
    # to the target skill's concrete SKILL.md path. Merely mentioning another
    # skill by name inside loaded lifecycle/handoff prose does not count.
    if path_re.search(payload):
        commandish = any(token in marker for token in (
            'command', 'exec', 'shell', 'read', 'cat', 'sed', 'python', 'tool'
        ))
        if commandish or 'skill' in marker:
            return True
    return False

with open(json_file, encoding='utf-8', errors='ignore') as fh:
    for line in fh:
        try:
            root = json.loads(line)
        except Exception:
            continue
        stack = [root]
        while stack:
            current = stack.pop()
            if is_explicit_skill_record(current):
                raise SystemExit(0)
            if isinstance(current, dict):
                stack.extend(v for v in current.values() if isinstance(v, (dict, list)))
            elif isinstance(current, list):
                stack.extend(v for v in current if isinstance(v, (dict, list)))
raise SystemExit(1)
PY
}

routing_oracle() {
  local json_file="$1" required="$2" forbidden_csv="$3"
  local observed_any=0 forbidden_hit=0 skill
  IFS=',' read -ra forbidden <<< "$forbidden_csv"
  for skill in "${forbidden[@]}"; do
    if observed_skill_event "$json_file" "$skill"; then
      observed_any=1
      forbidden_hit=1
      echo "forbidden:$skill" >&2
    fi
  done
  if (( forbidden_hit )); then printf 'fail'; return; fi
  if [[ "$required" == "none" ]]; then
    if (( observed_any )); then printf 'fail'; else printf 'unobserved'; fi
    return
  fi
  if observed_skill_event "$json_file" "$required"; then printf 'pass'; else printf 'unobserved'; fi
}

behavior_oracle() {
  local name="$1" json_file="$2" text
  text="$(python3 - "$json_file" <<'PY'
import json,sys
out=[]
for line in open(sys.argv[1], encoding='utf-8', errors='ignore'):
    try: obj=json.loads(line)
    except Exception: continue
    def walk(x):
        if isinstance(x,dict):
            for k,v in x.items():
                if k in {'text','message','content','output_text'} and isinstance(v,str): out.append(v)
                elif isinstance(v,(dict,list)): walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(obj)
print('\n'.join(out))
PY
)"
  case "$name" in
    baseline) [[ "$text" =~ (^|[[:space:]])OK($|[[:space:]]) ]] ;;
    unexplained-failure) [[ "$text" =~ [Rr]oot[[:space:]-]cause|[Ii]nvestigat|[Dd]iagnos ]] && ! [[ "$text" =~ [Ii]mplemented|[Ff]ixed[[:space:]]the|[Mm]odified[[:space:]]files ]] ;;
    implementation) [[ "$text" =~ [Tt]est|[Rr]egression ]] && [[ "$text" =~ [Ii]mplement|[Cc]hange|[Ff]ix ]] ;;
    completion-claim) [[ "$text" =~ [Ee]vidence|[Vv]erif|[Cc]laim|[Rr]eady ]] && ! [[ "$text" =~ [Ii]mplemented[[:space:]]a[[:space:]]new|[Mm]odified[[:space:]]files ]] ;;
    *) return 1 ;;
  esac
}

probe_one() {
  local name="$1" required="$2" forbidden="$3" prompt="$4" sandbox_mode="$5"
  local scenario_dir="$RUN_DIR/$name" attempt rc start end duration runtime routing behavior
  mkdir -p "$scenario_dir"
  echo "=== Scenario: $name (required: $required; forbidden: $forbidden) ==="

  for ((attempt=1; attempt<=RETRIES; attempt++)); do
    local json_file="$scenario_dir/attempt-${attempt}.jsonl" err_file="$scenario_dir/attempt-${attempt}.stderr.log"
    start="$(date +%s)"
    timeout "$TIMEOUT_SECONDS" "$CODEX_BIN" exec --json --ephemeral --sandbox "$sandbox_mode" -C "$PROBE_WORKDIR" "$prompt" >"$json_file" 2>"$err_file"
    rc=$?; end="$(date +%s)"; duration=$((end-start))

    if [[ "$rc" -eq 0 ]]; then
      runtime="pass"
      routing="$(routing_oracle "$json_file" "$required" "$forbidden")"
      if behavior_oracle "$name" "$json_file"; then behavior="pass"; else behavior="fail"; fi
      local input_count="" cached="" uncached="" output="" reasoning=""
      IFS=$'\t' read -r input_count cached uncached output reasoning < <(extract_usage_counts "$json_file")
      printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
        "$name" "$required" "$forbidden" "$routing" "$behavior" "$runtime" "$attempt" "$duration" \
        "${input_count:-}" "${cached:-}" "${uncached:-}" "${output:-}" "${reasoning:-}" "$json_file" "$err_file" >> "$SUMMARY"
      echo "[$name] routing=$routing behavior=$behavior runtime=$runtime (${duration}s, uncached=${uncached:-n/a})"
      [[ "$routing" != "fail" && "$behavior" == "pass" ]] && return 0
      return 1
    fi

    runtime="$(classify_runtime_failure "$rc" "$err_file" "$json_file")"
    echo "[$name] runtime=$runtime attempt=$attempt exit=$rc" >&2
    if (( attempt < RETRIES )); then sleep "$BACKOFF_SECONDS"; fi
  done

  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t\t\t\t\t\t%s\t%s\n' \
    "$name" "$required" "$forbidden" "unobserved" "fail" "$runtime" "$RETRIES" "$duration" \
    "$scenario_dir/attempt-${RETRIES}.jsonl" "$scenario_dir/attempt-${RETRIES}.stderr.log" >> "$SUMMARY"
  return 1
}

failures=0
for i in 0 1 2 3; do
  probe_one "${scenario_names[$i]}" "${required_skills[$i]}" "${forbidden_skills[$i]}" "${prompts[$i]}" "${scenario_sandboxes[$i]}" || failures=$((failures+1))
done

echo
echo "Probe workdir: $PROBE_WORKDIR"
echo "Captured probe artifacts: $RUN_DIR"
echo "Summary: $SUMMARY"
cat "$SUMMARY"

if (( failures > 0 )); then
  echo "Live Codex progressive-skill probe: FAIL ($failures scenario(s))" >&2
  exit 1
fi

echo "Live Codex progressive-skill probe: PASS"
