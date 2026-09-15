from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "writing-plans" / "SKILL.md"
IA = ROOT / "docs" / "ia-before-ui.md"
VIA = ROOT / "docs" / "verification-impact-analysis-v1.md"


def test_combined_ia_via_contract_is_explicit():
    text = SKILL.read_text(encoding="utf-8")
    assert "## IA Before UI" in text
    assert "docs/ia-before-ui.md" in text
    assert "GO_FOR_UI" in text
    assert "REVISE_IA" in text
    assert "## Impact Radius Before Test Scope" in text
    assert "Verification Impact Analysis" in text
    assert "R0 local only" in text
    assert "R3 user/cross-boundary/UI" in text
    assert "D0 deterministic invariants" in text
    assert "D2 broad semantic audits" in text


def test_plan_template_orders_ia_before_implementation_and_via_before_integration():
    text = SKILL.read_text(encoding="utf-8")
    lifecycle = text.index("Target user + job + value hypothesis")
    ia = text.index("-> IA-before-UI", lifecycle)
    implementation = text.index("-> implementation", ia)
    via = text.index("-> Verification Impact Analysis", implementation)
    integration = text.index("-> real-component integration", via)
    assert lifecycle < ia < implementation < via < integration


def test_plan_header_requires_both_reviews():
    text = SKILL.read_text(encoding="utf-8")
    header = text[text.index("## Plan Document Header"):]
    assert "## IA-Before-UI Review" in header
    assert "**Applicability:** REQUIRED | NOT_APPLICABLE" in header
    assert "**Disposition:** GO_FOR_UI | REVISE_IA | NOT_APPLICABLE" in header
    assert "## Verification Impact Analysis" in header
    assert "**Uncertainty:** low | medium | high" in header
    assert "**Radius:** R0 | R1 | R2 | R3" in header
    assert "**Omitted broad suites:**" in header


def test_ia_gate_is_structural_not_default_human_approval():
    skill = SKILL.read_text(encoding="utf-8")
    ia = IA.read_text(encoding="utf-8")
    combined = skill + "\n" + ia
    assert "not a default human-approval checkpoint" in combined
    assert "REVISE_IA" in combined
    assert "duplicated semantic ownership" in combined


def test_via_keeps_test_scope_separate_from_mvl_value_evaluation():
    text = VIA.read_text(encoding="utf-8")
    assert "VIA is not the product evaluation loop" in text
    assert "R0-R3 are not MVL levels" in text
    assert "D0 — deterministic invariants" in text
    assert "D1 — local semantic sentinels" in text
    assert "D2 — full semantic audits" in text


def _run_without_pytest() -> int:
    tests = [
        test_combined_ia_via_contract_is_explicit,
        test_plan_template_orders_ia_before_implementation_and_via_before_integration,
        test_plan_header_requires_both_reviews,
        test_ia_gate_is_structural_not_default_human_approval,
        test_via_keeps_test_scope_separate_from_mvl_value_evaluation,
    ]
    failures = 0
    for test in tests:
        try:
            test()
        except Exception as exc:
            failures += 1
            print(f"[FAIL] {test.__name__}: {exc}")
        else:
            print(f"[PASS] {test.__name__}")
    if failures:
        print(f"IA/VIA deterministic contract: FAIL ({failures} test(s))")
        return 1
    print("IA/VIA deterministic contract: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(_run_without_pytest())
