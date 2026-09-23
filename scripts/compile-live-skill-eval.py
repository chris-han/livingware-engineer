#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


SCENARIO_CLAIMS = {
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


def _maybe_int(value: str | None) -> int | None:
    if not value:
        return None
    return int(value)


def _routing_frontier(value: str, expected_skill: str | None) -> str:
    if value == "pass":
        return "PASS"
    if value == "fail":
        return "FAIL"
    if value == "unobserved" and expected_skill is None:
        return "PASS"
    return "UNKNOWN"


def _binary_frontier(value: str) -> str:
    return "PASS" if value == "pass" else "FAIL"


def compile_summary(summary_path: Path, probe_exit_code: int) -> dict:
    with summary_path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))

    cases = []
    for row in rows:
        scenario = row["scenario"]
        contract = SCENARIO_CLAIMS.get(
            scenario,
            {
                "target": "skill-runtime",
                "expected_skill": row.get("required_skill") or None,
                "claim": f"live skill-runtime scenario {scenario}",
            },
        )
        routing = row["routing"]
        behavior = row["behavior"]
        runtime = row["runtime"]
        cases.append(
            {
                "case_id": f"codex-live-{scenario}",
                "target_id": contract["target"],
                "provenance": "OBSERVED",
                "task_or_fixture_identity": scenario,
                "expected_skill": contract["expected_skill"],
                "forbidden_skills": [
                    item
                    for item in row.get("forbidden_skills", "").split(",")
                    if item
                ],
                "claim": contract["claim"],
                "observed_trace": {
                    "runtime": runtime,
                    "routing_observation": routing,
                    "behavior_observation": behavior,
                    "duration_seconds": _maybe_int(row.get("duration_seconds")),
                    "token_usage": {
                        "input": _maybe_int(row.get("input-count")),
                        "cached_input": _maybe_int(row.get("cached-input-count")),
                        "uncached_input": _maybe_int(row.get("uncached-input-count")),
                        "output": _maybe_int(row.get("output-count")),
                        "reasoning_output": _maybe_int(row.get("reasoning-output-count")),
                    },
                    "jsonl_ref": row.get("jsonl") or None,
                    "stderr_ref": row.get("stderr") or None,
                },
                "evaluation": {
                    "routing": {
                        "frontier": _routing_frontier(routing, contract["expected_skill"]),
                        "evidence_kind": "DETERMINISTIC_TRACE_CHECK",
                        "note": (
                            "For scenarios requiring a skill, UNKNOWN means no explicit skill-load event "
                            "was observed; behavior evidence must not be promoted into routing "
                            "evidence. For a no-skill baseline, absence of forbidden skill-load "
                            "events is the expected routing evidence."
                        ),
                    },
                    "behavior": {
                        "frontier": _binary_frontier(behavior),
                        "evidence_kind": "DETERMINISTIC_OUTPUT_CHECK",
                    },
                    "runtime": {
                        "frontier": _binary_frontier(runtime),
                        "evidence_kind": "PROCESS_EXIT_STATUS",
                    },
                },
            }
        )

    overall = "PASS"
    if probe_exit_code != 0 or any(
        case["evaluation"]["routing"]["frontier"] == "FAIL"
        or case["evaluation"]["behavior"]["frontier"] == "FAIL"
        or case["evaluation"]["runtime"]["frontier"] == "FAIL"
        for case in cases
    ):
        overall = "FAIL"
    elif any(
        case["evaluation"]["routing"]["frontier"] == "UNKNOWN" for case in cases
    ):
        overall = "QUALIFIED_BOUNDED"

    return {
        "schema_version": "livingware.eval-run.v1",
        "compiler": "scripts/compile-live-skill-eval.py",
        "source_probe": "tests/codex/live-progressive-skill-probe.sh",
        "evidence_provenance": "OBSERVED",
        "probe_exit_code": probe_exit_code,
        "overall_disposition": overall,
        "cases": cases,
        "limitations": [
            "This run evaluates the authenticated Codex harness actually invoked by the source probe.",
            "An unobserved explicit skill-load event is UNKNOWN for routing, even if behavior appears correct.",
            "One run is regression evidence for the pinned episode, not a universal performance or model-quality claim.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("summary", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--probe-exit-code", type=int, default=0)
    args = parser.parse_args()

    payload = compile_summary(args.summary, args.probe_exit_code)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    print(
        json.dumps(
            {
                "overall_disposition": payload["overall_disposition"],
                "case_count": len(payload["cases"]),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
