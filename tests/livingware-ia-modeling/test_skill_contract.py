import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills" / "livingware-ia-modeling" / "SKILL.md"
REF = ROOT / "skills" / "livingware-ia-modeling" / "references" / "sysml-inspired-kernel.md"


class SkillContractTests(unittest.TestCase):
    def test_skill_files_exist(self):
        self.assertTrue(SKILL.exists())
        self.assertTrue(REF.exists())

    def test_skill_preserves_core_modeling_invariants(self):
        text = SKILL.read_text(encoding="utf-8")
        required = [
            "Definition -> Usage / Occurrence -> Evidence -> Evaluation",
            "Do not collapse definition and instance graphs",
            "authority",
            "governance",
            "SysML v2 is a modeling reference",
            "Do not make SysML v2 a runtime dependency",
        ]
        for phrase in required:
            self.assertIn(phrase, text)

    def test_reference_covers_normative_complexity(self):
        text = REF.read_text(encoding="utf-8")
        for term in ["scope", "condition", "exception", "qualification", "precedence", "temporal interval"]:
            self.assertIn(term, text)
        for term in ["SATISFIED_BY", "VIOLATED_BY", "ELIGIBLE_FOR"]:
            self.assertIn(term, text)


if __name__ == "__main__":
    unittest.main()
