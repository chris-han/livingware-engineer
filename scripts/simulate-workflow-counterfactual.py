#!/usr/bin/env python3
"""Bounded replay and Monte Carlo what-if evaluation for Livingware workflows.

This is an evaluation utility, not an execution engine or learning authority.
It never mutates repository state and never labels simulated output as observed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import statistics
import sys
from pathlib import Path
from typing import Any

SCHEMA = "livingware.counterfactual.v1"
PROVENANCE = {"OBSERVED", "REPLAYED", "SIMULATED", "INFERRED", "ASSUMED"}
LAYERS = {"ROUTING", "WORKFLOW", "TOOL", "POLICY"}
MODES = {"REPLAY", "MONTE_CARLO"}
METRICS = ("latency_seconds", "uncached_input_tokens", "tool_calls")
EPSILON = 1e-9


class ValidationError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def rounded(value: float) -> float:
    return round(float(value), 6)


def validate_provenance(node: dict[str, Any], where: str) -> None:
    require(node.get("provenance") in PROVENANCE, f"{where}: invalid or missing provenance")
    require(isinstance(node.get("source_ref"), str) and node["source_ref"].strip(), f"{where}: missing source_ref")


def validate_metric(metric: dict[str, Any], name: str, mode: str, where: str) -> None:
    require(isinstance(metric, dict), f"{where}.{name}: metric must be an object")
    validate_provenance(metric, f"{where}.{name}")
    distribution = metric.get("distribution")
    require(distribution in {"fixed", "triangular"}, f"{where}.{name}: unsupported distribution")
    if mode == "REPLAY":
        require(distribution == "fixed", f"{where}.{name}: replay requires fixed metrics")
    if distribution == "fixed":
        value = metric.get("value")
        require(isinstance(value, (int, float)) and not isinstance(value, bool), f"{where}.{name}: fixed value must be numeric")
        require(value >= 0, f"{where}.{name}: metric values must be nonnegative")
    else:
        low, modal, high = metric.get("low"), metric.get("mode"), metric.get("high")
        require(all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in (low, modal, high)), f"{where}.{name}: triangular parameters must be numeric")
        require(0 <= low <= modal <= high, f"{where}.{name}: require 0 <= low <= mode <= high")


def validate_alternative(name: str, alt: dict[str, Any], mode: str) -> None:
    require(isinstance(alt.get("start_state"), str) and alt["start_state"], f"{name}: missing start_state")
    terminals = alt.get("terminal_states")
    require(isinstance(terminals, list) and terminals and all(isinstance(x, str) and x for x in terminals), f"{name}: terminal_states required")
    transitions = alt.get("transitions")
    require(isinstance(transitions, list) and transitions, f"{name}: transitions required")

    outgoing: dict[str, list[dict[str, Any]]] = {}
    destination_states: set[str] = set()
    for i, transition in enumerate(transitions):
        where = f"{name}.transitions[{i}]"
        require(isinstance(transition, dict), f"{where}: transition must be object")
        src, dst = transition.get("from"), transition.get("to")
        require(isinstance(src, str) and src, f"{where}: missing from")
        require(isinstance(dst, str) and dst, f"{where}: missing to")
        destination_states.add(dst)
        probability = transition.get("probability")
        require(isinstance(probability, dict), f"{where}: probability object required")
        validate_provenance(probability, f"{where}.probability")
        p = probability.get("value")
        require(isinstance(p, (int, float)) and not isinstance(p, bool) and 0 <= p <= 1, f"{where}: probability must be in [0,1]")
        if mode == "REPLAY":
            require(abs(float(p) - 1.0) <= EPSILON, f"{where}: replay requires probability 1.0")
        metrics = transition.get("metrics")
        require(isinstance(metrics, dict), f"{where}: metrics required")
        for metric_name in METRICS:
            require(metric_name in metrics, f"{where}: missing metric {metric_name}")
            validate_metric(metrics[metric_name], metric_name, mode, where)
        outgoing.setdefault(src, []).append(transition)

    terminal_set = set(terminals)
    states = set(outgoing) | destination_states | {alt["start_state"]}
    for state in states - terminal_set:
        require(state in outgoing, f"{name}: nonterminal state {state!r} has no outgoing transitions")
        total = sum(float(t["probability"]["value"]) for t in outgoing[state])
        require(abs(total - 1.0) <= EPSILON, f"{name}: outgoing probabilities for {state!r} sum to {total}, not 1.0")
        if mode == "REPLAY":
            require(len(outgoing[state]) == 1, f"{name}: replay requires exactly one outgoing transition per visited state")


def validate(payload: dict[str, Any]) -> None:
    require(payload.get("schema_version") == SCHEMA, f"schema_version must be {SCHEMA}")
    require(payload.get("layer") in LAYERS, "layer must be ROUTING, WORKFLOW, TOOL, or POLICY")
    for field in ("decision_point", "baseline_choice", "alternate_choice"):
        require(isinstance(payload.get(field), str) and payload[field].strip(), f"missing {field}")
    frozen = payload.get("frozen_basis")
    require(isinstance(frozen, dict), "frozen_basis required")
    for field in ("fixture_id", "repository_state", "workflow_version", "policy_version"):
        require(isinstance(frozen.get(field), str) and frozen[field].strip(), f"frozen_basis.{field} required")
    require(isinstance(frozen.get("operator_versions"), dict), "frozen_basis.operator_versions required")

    mode = payload.get("mode")
    require(mode in MODES, "mode must be REPLAY or MONTE_CARLO; REAL_REEXECUTION is external")
    max_steps = payload.get("max_steps")
    require(isinstance(max_steps, int) and not isinstance(max_steps, bool) and max_steps > 0, "max_steps must be a positive integer")
    if mode == "MONTE_CARLO":
        require(isinstance(payload.get("seed"), int) and not isinstance(payload.get("seed"), bool), "MONTE_CARLO requires integer seed")
        require(isinstance(payload.get("rollouts"), int) and not isinstance(payload.get("rollouts"), bool) and payload["rollouts"] > 0, "MONTE_CARLO requires positive integer rollouts")
    else:
        require(payload.get("rollouts") in (None, 1), "REPLAY does not accept stochastic rollout counts")

    alternatives = payload.get("alternatives")
    require(isinstance(alternatives, dict) and set(alternatives) == {"baseline", "alternate"}, "alternatives must contain exactly baseline and alternate")
    for name, alt in alternatives.items():
        require(isinstance(alt, dict), f"{name}: alternative must be object")
        validate_alternative(name, alt, mode)

    intervention_layers = payload.get("intervention_layers", [payload["layer"]])
    require(isinstance(intervention_layers, list) and intervention_layers and all(x in LAYERS for x in intervention_layers), "intervention_layers contains invalid layer")


def sample_metric(metric: dict[str, Any], rng: random.Random | None) -> float:
    if metric["distribution"] == "fixed":
        return float(metric["value"])
    assert rng is not None
    return float(rng.triangular(float(metric["low"]), float(metric["high"]), float(metric["mode"])))


def choose_transition(transitions: list[dict[str, Any]], rng: random.Random | None, mode: str) -> dict[str, Any]:
    if mode == "REPLAY":
        return transitions[0]
    assert rng is not None
    needle = rng.random()
    cumulative = 0.0
    for transition in transitions:
        cumulative += float(transition["probability"]["value"])
        if needle <= cumulative + EPSILON:
            return transition
    return transitions[-1]


def run_once(alt: dict[str, Any], mode: str, max_steps: int, rng: random.Random | None) -> dict[str, Any]:
    outgoing: dict[str, list[dict[str, Any]]] = {}
    for t in alt["transitions"]:
        outgoing.setdefault(t["from"], []).append(t)
    terminal_set = set(alt["terminal_states"])
    state = alt["start_state"]
    totals = {name: 0.0 for name in METRICS}
    steps = 0
    while state not in terminal_set:
        if steps >= max_steps:
            return {"outcome": "LOOP_LIMIT", "metrics": totals, "steps": steps}
        transition = choose_transition(outgoing[state], rng, mode)
        for name in METRICS:
            totals[name] += sample_metric(transition["metrics"][name], rng)
        state = transition["to"]
        steps += 1
    return {"outcome": state, "metrics": totals, "steps": steps}


def summarize(runs: list[dict[str, Any]], terminal_states: list[str]) -> dict[str, Any]:
    count = len(runs)
    outcomes: dict[str, int] = {}
    for run in runs:
        outcomes[run["outcome"]] = outcomes.get(run["outcome"], 0) + 1
    success_label = "SUCCESS" if "SUCCESS" in terminal_states else terminal_states[0]
    success = outcomes.get(success_label, 0)
    failure = count - success - outcomes.get("LOOP_LIMIT", 0)
    result: dict[str, Any] = {
        "runs": count,
        "success_rate": rounded(success / count),
        "failure_rate": rounded(failure / count),
        "loop_limit_rate": rounded(outcomes.get("LOOP_LIMIT", 0) / count),
        "outcomes": dict(sorted(outcomes.items())),
    }
    for metric in METRICS:
        values = [float(run["metrics"][metric]) for run in runs]
        if metric == "tool_calls":
            values = [float(max(0, round(v))) for v in values]
        result[metric] = {
            "mean": rounded(statistics.fmean(values)),
            "median": rounded(statistics.median(values)),
        }
    return result


def provenance_summary(payload: dict[str, Any]) -> dict[str, list[str]]:
    summary: dict[str, set[str]] = {"probability": set(), **{m: set() for m in METRICS}}
    for alt in payload["alternatives"].values():
        for transition in alt["transitions"]:
            summary["probability"].add(transition["probability"]["provenance"])
            for metric in METRICS:
                summary[metric].add(transition["metrics"][metric]["provenance"])
    return {key: sorted(values) for key, values in summary.items()}


def rng_for(seed: int, alternative_name: str) -> random.Random:
    digest = hashlib.sha256(f"{seed}:{alternative_name}".encode("utf-8")).digest()
    return random.Random(int.from_bytes(digest[:8], "big"))


def compare(payload: dict[str, Any]) -> dict[str, Any]:
    validate(payload)
    mode = payload["mode"]
    input_digest = "sha256:" + hashlib.sha256(canonical_bytes(payload)).hexdigest()
    run_count = payload["rollouts"] if mode == "MONTE_CARLO" else 1
    summaries: dict[str, Any] = {}
    for name in ("baseline", "alternate"):
        alt = payload["alternatives"][name]
        rng = rng_for(payload["seed"], name) if mode == "MONTE_CARLO" else None
        runs = [run_once(alt, mode, payload["max_steps"], rng) for _ in range(run_count)]
        summaries[name] = summarize(runs, alt["terminal_states"])

    baseline, alternate = summaries["baseline"], summaries["alternate"]
    deltas: dict[str, Any] = {
        "success_rate": rounded(baseline["success_rate"] - alternate["success_rate"]),
        "failure_rate": rounded(baseline["failure_rate"] - alternate["failure_rate"]),
        "loop_limit_rate": rounded(baseline["loop_limit_rate"] - alternate["loop_limit_rate"]),
    }
    for metric in METRICS:
        deltas[metric] = {
            stat: rounded(baseline[metric][stat] - alternate[metric][stat]) for stat in ("mean", "median")
        }

    provenance = provenance_summary(payload)
    assumption_sensitive = any(p in {"ASSUMED", "INFERRED"} for values in provenance.values() for p in values)
    intervention_layers = payload.get("intervention_layers", [payload["layer"]])
    isolated = len(set(intervention_layers)) == 1
    result: dict[str, Any] = {
        "schema_version": SCHEMA,
        "input_digest": input_digest,
        "mode": mode,
        "layer": payload["layer"],
        "decision_point": payload["decision_point"],
        "alternatives": summaries,
        "deltas_baseline_minus_alternate": deltas,
        "provenance_summary": provenance,
        "assumption_sensitive": assumption_sensitive,
        "exploratory": not isolated,
        "isolated_attribution": isolated,
        "claim_scope": "what-if simulation; not causal effect" if mode == "MONTE_CARLO" else "deterministic replay; not new observed evidence",
    }
    if mode == "MONTE_CARLO":
        result["seed"] = payload["seed"]
        result["rollouts"] = payload["rollouts"]
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path)
    args = parser.parse_args()
    try:
        payload = json.loads(args.fixture.read_text(encoding="utf-8"))
        result = compare(payload)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(json.dumps({"error": str(exc), "schema_version": SCHEMA}, sort_keys=True, separators=(",", ":")))
        return 2
    print(json.dumps(result, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
