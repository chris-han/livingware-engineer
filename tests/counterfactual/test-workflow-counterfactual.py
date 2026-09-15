#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "simulate-workflow-counterfactual.py"
FIXTURE = ROOT / "tests" / "counterfactual" / "fixtures" / "routing-whatif-v1.json"


def run_payload(payload: dict) -> tuple[int, bytes, dict]:
    with tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False) as handle:
        json.dump(payload, handle)
        path = Path(handle.name)
    try:
        proc = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, check=False)
        body = json.loads(proc.stdout.decode("utf-8"))
        return proc.returncode, proc.stdout, body
    finally:
        path.unlink(missing_ok=True)


def make_replay_payload(base: dict) -> dict:
    payload = copy.deepcopy(base)
    payload["mode"] = "REPLAY"
    payload.pop("seed", None)
    payload["rollouts"] = 1
    for name in ("baseline", "alternate"):
        original = payload["alternatives"][name]["transitions"]
        start = copy.deepcopy(original[0])
        success = copy.deepcopy(next(t for t in original if t["to"] == "SUCCESS"))
        start["probability"]["value"] = 1.0
        success["probability"]["value"] = 1.0
        payload["alternatives"][name]["transitions"] = [start, success]
    return payload


def make_all_metrics_fixed(payload: dict) -> None:
    for alt in payload["alternatives"].values():
        for transition in alt["transitions"]:
            for metric in transition["metrics"].values():
                if metric["distribution"] == "triangular":
                    value = metric["mode"]
                    provenance = metric["provenance"]
                    source_ref = metric["source_ref"]
                    metric.clear()
                    metric.update({
                        "distribution": "fixed",
                        "value": value,
                        "provenance": provenance,
                        "source_ref": source_ref,
                    })


class CounterfactualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_fixed_seed_is_byte_stable(self):
        a = run_payload(copy.deepcopy(self.base))
        b = run_payload(copy.deepcopy(self.base))
        self.assertEqual(a[0], 0)
        self.assertEqual(a[1], b[1])

    def test_different_seed_preserves_schema_and_provenance(self):
        a = copy.deepcopy(self.base)
        b = copy.deepcopy(self.base)
        b["seed"] = 19
        _, _, ra = run_payload(a)
        _, _, rb = run_payload(b)
        self.assertEqual(ra["schema_version"], rb["schema_version"])
        self.assertEqual(ra["provenance_summary"], rb["provenance_summary"])
        self.assertEqual(ra["claim_scope"], "what-if simulation; not causal effect")

    def test_replay_rejects_stochastic_probability(self):
        p = copy.deepcopy(self.base)
        p["mode"] = "REPLAY"
        p.pop("seed", None)
        p["rollouts"] = 1
        make_all_metrics_fixed(p)
        rc, _, body = run_payload(p)
        self.assertEqual(rc, 2)
        self.assertIn("replay requires probability 1.0", body["error"])

    def test_replay_rejects_triangular_metric(self):
        p = make_replay_payload(self.base)
        rc, _, body = run_payload(p)
        self.assertEqual(rc, 2)
        self.assertIn("replay requires fixed metrics", body["error"])

    def test_valid_replay_has_non_observed_claim_scope(self):
        p = make_replay_payload(self.base)
        make_all_metrics_fixed(p)
        rc, _, body = run_payload(p)
        self.assertEqual(rc, 0)
        self.assertEqual(body["claim_scope"], "deterministic replay; not new observed evidence")

    def test_monte_carlo_requires_seed_and_rollouts(self):
        for missing in ("seed", "rollouts"):
            p = copy.deepcopy(self.base)
            p.pop(missing)
            rc, _, body = run_payload(p)
            self.assertEqual(rc, 2)
            self.assertIn("requires", body["error"])

    def test_probability_sum_must_equal_one(self):
        p = copy.deepcopy(self.base)
        p["alternatives"]["baseline"]["transitions"][1]["probability"]["value"] = 0.7
        rc, _, body = run_payload(p)
        self.assertEqual(rc, 2)
        self.assertIn("sum to", body["error"])

    def test_nonterminal_destination_requires_outgoing_transition(self):
        p = copy.deepcopy(self.base)
        p["alternatives"]["baseline"]["transitions"][0]["to"] = "MISSING"
        rc, _, body = run_payload(p)
        self.assertEqual(rc, 2)
        self.assertIn("has no outgoing transitions", body["error"])

    def test_missing_provenance_fails(self):
        p = copy.deepcopy(self.base)
        del p["alternatives"]["baseline"]["transitions"][0]["probability"]["provenance"]
        rc, _, body = run_payload(p)
        self.assertEqual(rc, 2)
        self.assertIn("provenance", body["error"])

    def test_unsupported_distribution_fails(self):
        p = copy.deepcopy(self.base)
        p["alternatives"]["baseline"]["transitions"][0]["metrics"]["latency_seconds"]["distribution"] = "normal"
        rc, _, body = run_payload(p)
        self.assertEqual(rc, 2)
        self.assertIn("unsupported distribution", body["error"])

    def test_loop_is_bounded(self):
        p = copy.deepcopy(self.base)
        for name in ("baseline", "alternate"):
            p["alternatives"][name] = {
                "start_state": "S0",
                "terminal_states": ["SUCCESS"],
                "transitions": [{
                    "from": "S0", "to": "S0",
                    "probability": {"value": 1.0, "provenance": "ASSUMED", "source_ref": "loop:test"},
                    "metrics": {
                        "latency_seconds": {"distribution": "fixed", "value": 1, "provenance": "ASSUMED", "source_ref": "loop:latency"},
                        "uncached_input_tokens": {"distribution": "fixed", "value": 1, "provenance": "ASSUMED", "source_ref": "loop:tokens"},
                        "tool_calls": {"distribution": "fixed", "value": 1, "provenance": "ASSUMED", "source_ref": "loop:tools"}
                    }
                }]
            }
        p["rollouts"] = 3
        p["max_steps"] = 2
        rc, _, body = run_payload(p)
        self.assertEqual(rc, 0)
        self.assertEqual(body["alternatives"]["baseline"]["loop_limit_rate"], 1.0)

    def test_simulation_never_claims_observed_or_causal_effect(self):
        rc, _, body = run_payload(copy.deepcopy(self.base))
        self.assertEqual(rc, 0)
        self.assertNotIn("OBSERVED", body["claim_scope"])
        self.assertEqual(body["claim_scope"], "what-if simulation; not causal effect")

    def test_assumption_driven_result_is_labeled(self):
        _, _, body = run_payload(copy.deepcopy(self.base))
        self.assertTrue(body["assumption_sensitive"])

    def test_multilayer_intervention_disables_isolated_attribution(self):
        p = copy.deepcopy(self.base)
        p["intervention_layers"] = ["ROUTING", "WORKFLOW"]
        _, _, body = run_payload(p)
        self.assertTrue(body["exploratory"])
        self.assertFalse(body["isolated_attribution"])

    def test_script_does_not_mutate_fixture(self):
        before = FIXTURE.read_bytes()
        subprocess.run([sys.executable, str(SCRIPT), str(FIXTURE)], capture_output=True, check=True)
        self.assertEqual(before, FIXTURE.read_bytes())


if __name__ == "__main__":
    unittest.main(verbosity=2)
