from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARCH = ROOT / "docs" / "livingware-evaluation-architecture.md"
SKILLS = {
    "evaluating-livingware",
    "discovering-failures",
    "designing-evaluators",
    "qualifying-evaluators",
    "generating-eval-cases",
    "evaluating-skill-runtime",
}
IR_FIXTURE = ROOT / "tests" / "eval-skills" / "fixtures" / "routing-whatif-eval-ir-v1.json"
COUNTERFACTUAL_FIXTURE = ROOT / "tests" / "counterfactual" / "fixtures" / "routing-whatif-v1.json"
DOGFOOD_FIXTURE = ROOT / "tests" / "eval-skills" / "fixtures" / "skill-runtime-dogfood-v1.json"
LIVE_SUMMARY_FIXTURE = ROOT / "tests" / "eval-skills" / "fixtures" / "live-probe-summary-v1.tsv"
LIVE_COMPILER = ROOT / "scripts" / "compile-live-skill-eval.py"


def test_eval_skill_family_exists_with_discriminating_metadata():
    for name in SKILLS:
        path = ROOT / "skills" / name / "SKILL.md"
        assert path.exists(), name
        text = path.read_text(encoding="utf-8")
        assert f"name: {name}" in text
        assert "description:" in text
        assert "livingware-evaluation-architecture.md" in text


def test_architecture_freezes_non_authority_and_provenance_contracts():
    text = ARCH.read_text(encoding="utf-8")

    assert "Evaluator output is measurement evidence, not behavioral authority" in text
    assert "Synthetic cases repair coverage; they do not manufacture evidence" in text
    assert "Learning authority follows failure attribution" in text

    for provenance in ("OBSERVED", "REPLAYED", "SIMULATED", "INFERRED", "ASSUMED"):
        assert provenance in text

    for obj in (
        "EvaluationTarget",
        "EvalCase",
        "ObservedTrace",
        "EvaluationClaim",
        "FailureObservation",
        "FailureModeCandidate",
        "FailureAttribution",
        "EvaluatorCandidate",
        "EvaluatorQualification",
        "RegressionWitness",
        "LearningCandidate",
    ):
        assert obj in text


def test_architecture_does_not_create_second_runtime_or_universal_threshold():
    text = ARCH.read_text(encoding="utf-8").lower()

    assert "does not create a second runtime" in text
    assert "no repository-wide universal tpr/tnr threshold" in text
    assert "persistent evaluation database" in text
    assert "mandatory meta-router" in text


def test_skill_runtime_eval_preserves_skill_review_boundary():
    runtime = (ROOT / "skills" / "evaluating-skill-runtime" / "SKILL.md").read_text(
        encoding="utf-8"
    )

    assert "skill-review" in runtime
    assert "Do not use this skill to duplicate" in runtime


def test_evaluator_design_prefers_deterministic_checks_and_supports_unknown():
    text = (ROOT / "skills" / "designing-evaluators" / "SKILL.md").read_text(
        encoding="utf-8"
    )

    assert "DETERMINISTIC" in text
    assert "INTERPRETED" in text
    assert "HYBRID" in text
    assert "PASS | FAIL | UNKNOWN | NOT_APPLICABLE" in text
    assert "Prefer schema validation" in text


def test_eval_ir_can_reference_existing_counterfactual_fixture_without_new_runtime():
    assert COUNTERFACTUAL_FIXTURE.exists()
    data = json.loads(IR_FIXTURE.read_text(encoding="utf-8"))

    assert data["schema_version"] == "livingware.eval-ir.v1"
    assert data["evaluation_target"]["target_kind"] == "ROUTING"
    assert data["eval_case"]["provenance"] == "SIMULATED"
    assert data["eval_case"]["source_parent"] == (
        "tests/counterfactual/fixtures/routing-whatif-v1.json"
    )
    assert data["evaluation_claim"]["evaluator_kind"] == "DETERMINISTIC"

    source = json.loads(COUNTERFACTUAL_FIXTURE.read_text(encoding="utf-8"))
    assert source["layer"] == "ROUTING"
    assert source["mode"] == "MONTE_CARLO"
    assert source["seed"] == data["eval_case"]["input_basis"]["seed"]
    assert source["rollouts"] == data["eval_case"]["input_basis"]["rollouts"]



def test_skill_runtime_dogfood_distinguishes_contract_evidence_from_live_routing():
    data = json.loads(DOGFOOD_FIXTURE.read_text(encoding="utf-8"))

    assert data["schema_version"] == "livingware.eval-dogfood.v1"
    assert data["dogfood_disposition"]["contract_level"] == "QUALIFIED"
    assert data["dogfood_disposition"]["native_harness_activation"] == "UNVERIFIED"
    assert data["dogfood_disposition"]["regression_witness_created"] is False

    targets = {target["skill"]: target for target in data["targets"]}
    assert {"systematic-debugging", "verification-before-completion"} <= set(targets)

    for skill, target in targets.items():
        classes = {case["class"] for case in target["cases"]}
        assert "SHOULD_ACTIVATE" in classes
        assert "SHOULD_NOT_ACTIVATE" in classes
        assert "HARD_NEGATIVE" in classes
        assert "CONTRACT" in classes

        contract_cases = [
            case for case in target["cases"]
            if case["evidence_lane"] == "DETERMINISTIC_REPOSITORY_CONTRACT"
        ]
        live_cases = [
            case for case in target["cases"]
            if case["evidence_lane"] == "LIVE_HARNESS_REQUIRED"
        ]
        assert contract_cases and all(case["status"] == "QUALIFIED" for case in contract_cases)
        assert live_cases and all(case["status"] == "UNVERIFIED" for case in live_cases)

        skill_text = (ROOT / target["contract_ref"]).read_text(encoding="utf-8")
        expected = contract_cases[0]["expected"]
        assert expected["entry_contains"] in skill_text
        assert expected["exit_contains"] in skill_text


def test_live_eval_compiler_preserves_routing_epistemics():
    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / "eval-run.json"
        subprocess.run(
            [
                "python3",
                str(LIVE_COMPILER),
                str(LIVE_SUMMARY_FIXTURE),
                str(output),
                "--probe-exit-code",
                "0",
            ],
            check=True,
            cwd=ROOT,
        )
        data = json.loads(output.read_text(encoding="utf-8"))

    assert data["schema_version"] == "livingware.eval-run.v1"
    assert data["evidence_provenance"] == "OBSERVED"
    assert data["overall_disposition"] == "QUALIFIED_BOUNDED"

    cases = {case["task_or_fixture_identity"]: case for case in data["cases"]}

    # No workflow skill is the expected baseline, so explicit absence is evidence.
    assert cases["baseline"]["evaluation"]["routing"]["frontier"] == "PASS"

    # When a skill is required, absence of an explicit skill-load event is unknown,
    # not success inferred from behavior and not an automatic failure.
    assert (
        cases["completion-claim"]["evaluation"]["routing"]["frontier"]
        == "UNKNOWN"
    )
    assert cases["completion-claim"]["evaluation"]["behavior"]["frontier"] == "PASS"


def test_live_eval_compiler_respects_source_probe_failure():
    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / "eval-run.json"
        subprocess.run(
            [
                "python3",
                str(LIVE_COMPILER),
                str(LIVE_SUMMARY_FIXTURE),
                str(output),
                "--probe-exit-code",
                "1",
            ],
            check=True,
            cwd=ROOT,
        )
        data = json.loads(output.read_text(encoding="utf-8"))

    assert data["overall_disposition"] == "FAIL"
    assert data["probe_exit_code"] == 1

def main():
    tests = [
        test_eval_skill_family_exists_with_discriminating_metadata,
        test_architecture_freezes_non_authority_and_provenance_contracts,
        test_architecture_does_not_create_second_runtime_or_universal_threshold,
        test_skill_runtime_eval_preserves_skill_review_boundary,
        test_evaluator_design_prefers_deterministic_checks_and_supports_unknown,
        test_eval_ir_can_reference_existing_counterfactual_fixture_without_new_runtime,
        test_skill_runtime_dogfood_distinguishes_contract_evidence_from_live_routing,
        test_live_eval_compiler_preserves_routing_epistemics,
        test_live_eval_compiler_respects_source_probe_failure,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")


if __name__ == "__main__":
    main()
