from pathlib import Path
R=Path(__file__).resolve().parents[2]
def t(p): return (R/p).read_text()
def test_contract():
 assert "Execution Continuity Contract" in t("skills/writing-plans/SKILL.md")
 assert "intermediate GREEN MUST NOT be interpreted as plan completion" in t("skills/writing-plans/SKILL.md")
 assert "A GREEN checkpoint advances plan state; it does not return control to the user." in t("skills/executing-plans/SKILL.md")
 assert "User Intervention Necessity Test" in t("docs/mvl-laws.md")
 assert "Progress reporting is observational, not a synchronization barrier." in t("docs/mvl-laws.md")
 assert "ask for consent before creating one" not in t("skills/using-git-worktrees/SKILL.md")
 assert "progress summaries waste their time" not in t("skills/subagent-driven-development/SKILL.md")
 assert "When a Codex `/goal` is active" in t("skills/using-superpowers/references/codex-tools.md")

if __name__ == '__main__':
    test_contract()
    print('Continuous execution contract: PASS')
