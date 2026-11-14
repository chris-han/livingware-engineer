"""Instruction-source checks, not behavioral evidence from an executing agent."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "writing-plans" / "SKILL.md"
IA = ROOT / "docs" / "ia-before-ui.md"
VIA = ROOT / "docs" / "verification-impact-analysis-v1.md"


def test_combined_ia_via_contract_is_explicit():
    text = SKILL.read_text(encoding="utf-8")
    for required in (
        "## IA Before UI", "docs/ia-before-ui.md", "GO_FOR_UI", "REVISE_IA",
        "## Impact Radius Before Test Scope", "Verification Impact Analysis",
        "R0 local only", "R3 user/UI/cross-process", "D0 deterministic invariants",
        "D1 focused behavior/integration", "Broad D2/goal E2E",
    ):
        assert required in text, required


def test_plan_orders_ia_and_focused_implementation_before_goal_e2e():
    text = SKILL.read_text(encoding="utf-8")
    ia = text.index("## IA Before UI")
    via = text.index("## Impact Radius Before Test Scope")
    goal = text.index("### Consolidated goal acceptance")
    assert ia < via < goal
    assert "before visual/production tasks" in text[ia:via]
    assert "focused behavior/unit tests" in text[via:goal]
    assert "after all implementation tasks are ready" in text[goal:]
    assert "actual application UI" in text[goal:]
    assert "persisted/backend effects through real internal components" in text[goal:]


def test_plan_header_requires_both_reviews():
    text = SKILL.read_text(encoding="utf-8")
    header = text[text.index("## Plan Document Header"):]
    for required in (
        "## IA-Before-UI Review", "**Applicability:** REQUIRED | NOT_APPLICABLE",
        "**Disposition:** GO_FOR_UI | REVISE_IA | NOT_APPLICABLE",
        "## Verification Impact Analysis", "uncertainty / radius R0–R3",
        "**Focused tests during implementation:**",
        "**Final campaign after implementation readiness:**", "**Omitted broad suites:**",
    ):
        assert required in header, required


def test_ia_gate_is_structural_not_default_human_approval():
    combined = SKILL.read_text(encoding="utf-8") + "\n" + IA.read_text(encoding="utf-8")
    assert "No extra approval turn is implied" in combined
    assert "REVISE_IA" in combined
    assert "duplicated semantic owners" in combined


def test_via_keeps_test_scope_separate_from_mvl_value_evaluation():
    text = VIA.read_text(encoding="utf-8")
    for required in (
        "VIA is not the product evaluation loop", "R0–R3 are not MVL levels",
        "D0 — deterministic invariants", "D1 — local semantic sentinels",
        "D2 — full semantic audits",
    ):
        assert required in text, required


def _run_without_pytest() -> int:
    tests = [test_combined_ia_via_contract_is_explicit,
             test_plan_orders_ia_and_focused_implementation_before_goal_e2e,
             test_plan_header_requires_both_reviews,
             test_ia_gate_is_structural_not_default_human_approval,
             test_via_keeps_test_scope_separate_from_mvl_value_evaluation]
    failures = 0
    for test in tests:
        try:
            test()
        except Exception as exc:
            failures += 1
            print(f"[FAIL] {test.__name__}: {exc}")
    print(f"IA/VIA source contract: {'FAIL' if failures else 'PASS'} ({len(tests)} checks, {failures} failures)")
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(_run_without_pytest())
