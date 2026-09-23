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

python3 - "$summary" "$RESULT" "$probe_rc" <<'PY'
import csv
import json
import pathlib
import sys

summary_path = pathlib.Path(sys.argv[1])
result_path = pathlib.Path(sys.argv[2])
probe_rc = int(sys.argv[3])

scenario_claims = {
    "baseline": {
        "target": "workflow-routing",
        "expected_skill": None,
        "claim": "ordinary baseline work does not activate debugging, TDD, or completion verification",
    },
    "unexplained-failure": {
        "target": "systematic-debugging-runtime",
        "expected_skill": "systematic-debugging",
        "claim": "an unexplained failure activates systematic-debugging and does not preload implementation/completion workflows",
    },
    "implementation": {
        "target": "test-driven-development-runtime",
        "expected_skill": "test-driven-development",
        "claim": "an established root cause routes to implementation/TDD rather than reopening debugging or preloading completion verification",
    },
    "completion-claim": {
        "target": "verification-before-completion-runtime",
        "expected_skill": "verification-before-completion",
        "claim": "an imminent completion/merge claim activates verification-before-completion rather than debugging or TDD",
    },
}

def routing_frontier(value: str) -> str:
    if value == "pass":
        return "PASS"
    if value == "fail":
        return "FAIL"
    return "UNKNOWN"

def binary_frontier(value: str) -> str:
    return "PASS" if value == "pass" else "FAIL"

with summary_path.open(newline="", encoding="utf-8") as fh:
    rows = list(csv.DictReader(fh, delimiter="\t"))

cases = []
for row in rows:
    scenario = row["scenario"]
    contract = scenario_claims.get(scenario, {
        "target": "skill-runtime",
        "expected_skill": row.get("required_skill") or None,
        "claim": f"live skill-runtime scenario {scenario}",
    })
    routing = row["routing"]
    behavior = row["behavior"]
    runtime = row["runtime"]
    cases.append({
        "case_id": f"codex-live-{scenario}",
        "target_id": contract["target"],
        "provenance": "OBSERVED",
        "task_or_fixture_identity": scenario,
        "expected_skill": contract["expected_skill"],
        "forbidden_skills": [x for x in row.get("forbidden_skills", "").split(",") if x],
        "claim": contract["claim"],
        "observed_trace": {
            "runtime": runtime,
            "routing_observation": routing,
            "behavior_observation": behavior,
            "duration_seconds": int(row["duration_seconds"]) if row.get("duration_seconds") else None,
            "token_usage": {
                "input": int(row["input-count"]) if row.get("input-count") else None,
                "cached_input": int(row["cached-input-count"]) if row.get("cached-input-count") else None,
                "uncached_input": int(row["uncached-input-count"]) if row.get("uncached-input-count") else None,
                "output": int(row["output-count"]) if row.get("output-count") else None,
                "reasoning_output": int(row["reasoning-output-count"]) if row.get("reasoning-output-count") else None,
            },
            "jsonl_ref": row.get("jsonl") or None,
            "stderr_ref": row.get("stderr") or None,
        },
        "evaluation": {
            "routing": {
                "frontier": routing_frontier(routing),
                "evidence_kind": "DETERMINISTIC_TRACE_CHECK",
                "note": "UNKNOWN means no explicit skill-load event was observed; behavior evidence must not be promoted into routing evidence.",
            },
            "behavior": {
                "frontier": binary_frontier(behavior),
                "evidence_kind": "DETERMINISTIC_OUTPUT_CHECK",
            },
            "runtime": {
                "frontier": binary_frontier(runtime),
                "evidence_kind": "PROCESS_EXIT_STATUS",
            },
        },
    })

overall = "PASS"
if probe_rc != 0 or any(
    c["evaluation"]["routing"]["frontier"] == "FAIL"
    or c["evaluation"]["behavior"]["frontier"] == "FAIL"
    or c["evaluation"]["runtime"]["frontier"] == "FAIL"
    for c in cases
):
    overall = "FAIL"
elif any(c["evaluation"]["routing"]["frontier"] == "UNKNOWN" for c in cases):
    overall = "QUALIFIED_BOUNDED"

payload = {
    "schema_version": "livingware.eval-run.v1",
    "runner": "tests/eval-skills/live-skill-runtime-eval.sh",
    "source_probe": "tests/codex/live-progressive-skill-probe.sh",
    "evidence_provenance": "OBSERVED",
    "probe_exit_code": probe_rc,
    "overall_disposition": overall,
    "cases": cases,
    "limitations": [
        "This run evaluates the authenticated Codex harness actually invoked by the source probe.",
        "An unobserved explicit skill-load event is UNKNOWN for routing, even if behavior appears correct.",
        "One run is regression evidence for the pinned episode, not a universal performance or model-quality claim.",
    ],
}

result_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
print(result_path)
print(json.dumps({"overall_disposition": overall, "case_count": len(cases)}, indent=2))
PY

if [[ "$probe_rc" -ne 0 ]]; then
  echo "Livingware live skill-runtime eval: FAIL (source probe exit=$probe_rc)" >&2
  exit "$probe_rc"
fi

echo "Livingware live skill-runtime eval artifact: $RESULT"
