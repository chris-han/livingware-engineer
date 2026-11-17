"""Static research-methodology progressive-disclosure invariants; not live agent evidence."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
SKILL = ROOT / "skills/research-methodology/SKILL.md"
REFS = {
    "discovery": ROOT / "skills/research-methodology/references/discovery-frontier-workflow.md",
    "experiment": ROOT / "skills/research-methodology/references/experiment-qualification-workflow.md",
    "closeout": ROOT / "skills/research-methodology/references/closeout-and-attribution-workflow.md",
}


def test_current_state_router_and_authoring_gate():
    s = SKILL.read_text(encoding="utf-8")
    for phrase in (
        "before substantive research reasoning or external discovery",
        "Do not preload adjacent design, coding, execution, evaluation or closure skills",
        "Existing",
        "EXACT_REUSE | PARTIAL_REUSE | STALE",
        "PRE_EXPERIMENT_CONTEXT_GREEN",
        "PRE_EXPERIMENT_CONTEXT_NOT_READY",
        "even when read earlier",
        "not when executing a frozen active plan",
        "zero or one",
        "No authority promotion",
        "not automatically authorized",
        "never re-run the pre-experiment authoring census",
    ):
        assert phrase.lower() in s.lower(), phrase


def test_references_preserve_research_validity_and_closure():
    d = REFS["discovery"].read_text(encoding="utf-8")
    e = REFS["experiment"].read_text(encoding="utf-8")
    c = REFS["closeout"].read_text(encoding="utf-8")
    for phrase in ("## Mandatory pre-experiment context gate", "PRE_EXPERIMENT_CONTEXT_NOT_READY", "## Existing-evidence-first law", "## MICE-style uncertainty decomposition"):
        assert phrase in d, phrase
    for phrase in ("## Three-part research validation contract", "## Experiment admissibility", "## Evidence discipline", "UNKNOWN", "invalid"):
        assert phrase in e, phrase
    for phrase in ("## Falsification and negative knowledge", "## Closure", "## One-next-question-or-stop rule", "NOMINATED_NOT_AUTHORIZED", "NO_AUTOMATIC_SUCCESSOR"):
        assert phrase in c, phrase


def test_root_references_are_real_and_no_parallel_ledger():
    text = SKILL.read_text(encoding="utf-8")
    for link in re.findall(r"\\]\\(([^)]+)\\)", text):
        if link.startswith(("http:", "https:", "#")):
            continue
        target = (SKILL.parent / link.split("#")[0]).resolve()
        assert target.is_relative_to(ROOT.resolve()), link
        assert target.is_file(), link
    assert "do not create a second ledger" in text
    assert len(text.encode("utf-8")) < 11000, "high-frequency root regressed; inspect what must be eager"
