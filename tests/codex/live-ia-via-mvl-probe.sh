#!/usr/bin/env bash
set -u -o pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT_BASE="${CODEX_PROBE_OUTPUT_DIR:-$ROOT/.artifacts/ia-via-mvl-probe}"
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
RUN_DIR="$OUT_BASE/$RUN_ID"
TIMEOUT_SECONDS="${CODEX_PROBE_TIMEOUT:-180}"
CODEX_BIN="${CODEX_BIN:-codex}"

mkdir -p "$RUN_DIR"
SUMMARY="$RUN_DIR/summary.tsv"
printf 'scenario\tbehavior\truntime\tduration_seconds\tjsonl\tstderr\n' > "$SUMMARY"

command -v "$CODEX_BIN" >/dev/null 2>&1 || { echo "ERROR: Codex CLI not found: $CODEX_BIN" >&2; exit 2; }
command -v timeout >/dev/null 2>&1 || { echo "ERROR: GNU timeout is required" >&2; exit 2; }

scenario_names=("ui-ia-change" "local-r0-maintenance" "duplicate-semantic-owner")
prompts=(
  "Create an implementation plan only; do not modify files. The feature materially changes a user-facing analytical workbench by adding a new Comparison panel and moving one existing semantic selector from a generic settings menu to the work surface where its meaning is used. The repository uses Livingware Engineer. Apply the planning workflow, including any pre-UI structural review and verification-scope analysis required by the installed skills. In the final answer include the plan sections and disposition needed before implementation."
  "Create an implementation plan only; do not modify files. The change is a behavior-preserving refactor of one private pure helper used only by its existing unit tests. No UI, route, persistence, schema, dependency, authorization, process boundary, or public API changes. The repository uses Livingware Engineer. Apply the planning workflow and choose only the verification justified by the change. In the final answer state whether any UI information-architecture review applies and give the verification impact radius."
  "Create an implementation plan only; do not modify files. A request proposes adding a second workspace-global Chat drawer inside one workbench even though the existing shell already owns the single workspace-global Chat drawer and its state. The new drawer would duplicate that semantic owner. The repository uses Livingware Engineer. Apply the planning workflow. Do not solve the conflict by styling, hiding, or locally duplicating state. In the final answer state the pre-UI disposition and whether production UI implementation may proceed."
)

extract_text() {
  python3 - "$1" <<'PY'
import json, sys
out=[]
for line in open(sys.argv[1], encoding='utf-8', errors='ignore'):
    try: obj=json.loads(line)
    except Exception: continue
    stack=[obj]
    while stack:
        x=stack.pop()
        if isinstance(x,dict):
            for k,v in x.items():
                if k in {'text','message','content','output_text'} and isinstance(v,str): out.append(v)
                elif isinstance(v,(dict,list)): stack.append(v)
        elif isinstance(x,list): stack.extend(x)
print('\n'.join(out))
PY
}

behavior_oracle() {
  local name="$1" json_file="$2" text
  text="$(extract_text "$json_file")"
  case "$name" in
    ui-ia-change)
      [[ "$text" =~ IA[-[:space:]]*[Bb]efore[-[:space:]]*UI|information[[:space:]-]architecture ]] &&
      [[ "$text" =~ GO_FOR_UI|REVISE_IA ]] &&
      [[ "$text" =~ R3|real[-[:space:]]browser|vertical[/[:space:]-]*E2E ]] &&
      [[ "$text" =~ semantic[[:space:]-]owner|semantic[[:space:]-]ownership ]]
      ;;
    local-r0-maintenance)
      [[ "$text" =~ NOT_APPLICABLE|not[[:space:]]applicable|no[[:space:]].*IA ]] &&
      [[ "$text" =~ R0|local[[:space:]]only ]] &&
      ! [[ "$text" =~ full[[:space:]-]suite[[:space:]].*required|vertical[/[:space:]-]*E2E[[:space:]].*required ]]
      ;;
    duplicate-semantic-owner)
      [[ "$text" =~ REVISE_IA|revise[[:space:]]IA ]] &&
      [[ "$text" =~ duplicate|competing|semantic[[:space:]-]owner ]] &&
      [[ "$text" =~ must[[:space:]]not[[:space:]]proceed|may[[:space:]]not[[:space:]]proceed|stop|block ]]
      ;;
    *) return 1 ;;
  esac
}

failures=0
for i in 0 1 2; do
  name="${scenario_names[$i]}"
  prompt="${prompts[$i]}"
  scenario_dir="$RUN_DIR/$name"
  mkdir -p "$scenario_dir"
  json_file="$scenario_dir/attempt-1.jsonl"
  err_file="$scenario_dir/attempt-1.stderr.log"
  echo "=== Scenario: $name ==="
  start="$(date +%s)"
  timeout "$TIMEOUT_SECONDS" "$CODEX_BIN" exec --json --ephemeral --sandbox read-only -C "$ROOT" "$prompt" >"$json_file" 2>"$err_file"
  rc=$?
  end="$(date +%s)"
  duration=$((end-start))
  if [[ "$rc" -eq 0 ]]; then
    runtime="pass"
    if behavior_oracle "$name" "$json_file"; then behavior="pass"; else behavior="fail"; fi
  elif [[ "$rc" -eq 124 ]]; then
    runtime="timeout"; behavior="fail"
  else
    runtime="error"; behavior="fail"
  fi
  printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$name" "$behavior" "$runtime" "$duration" "$json_file" "$err_file" >> "$SUMMARY"
  echo "[$name] behavior=$behavior runtime=$runtime (${duration}s)"
  [[ "$behavior" == "pass" && "$runtime" == "pass" ]] || failures=$((failures+1))
done

echo
echo "Captured probe artifacts: $RUN_DIR"
echo "Summary: $SUMMARY"
cat "$SUMMARY"

if (( failures > 0 )); then
  echo "IA/VIA live MVL probe: FAIL ($failures scenario(s))" >&2
  exit 1
fi

echo "IA/VIA live MVL probe: PASS"
