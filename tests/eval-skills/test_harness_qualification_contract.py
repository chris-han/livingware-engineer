from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "harness-qualification-contract.md"
ARCH = ROOT / "docs" / "livingware-evaluation-architecture.md"

def test_harness_contract_has_required_categories_and_gates():
    text = DOC.read_text(encoding="utf-8")
    for category in [f"I{i}" for i in range(8)]:
        assert re.search(rf"\b{category}\b", text)
    for gate in ["H0", "H1", "H2"]:
        assert gate in text
    for record in ["HarnessIdentity", "HarnessImpact", "harness_qualification"]:
        assert record in text

def test_harness_contract_keeps_non_compensable_invariants():
    text = DOC.read_text(encoding="utf-8")
    assert "authority violations                = 0" in text
    assert "replay-identity violations          = 0" in text
    assert "Component qualification does not imply composition qualification" in text

def test_eval_architecture_links_harness_qualification():
    text = ARCH.read_text(encoding="utf-8")
    assert "Harness Qualification" in text
    assert "harness-qualification-contract.md" in text
