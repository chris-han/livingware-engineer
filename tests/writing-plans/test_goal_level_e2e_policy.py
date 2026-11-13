"""Static policy regressions only; no model calls, UI runs or savings claims."""
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
POLICY = "docs/verification-impact-analysis-v1.md"


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def require(text, *parts):
    for part in parts:
        assert part in text, f"missing contract: {part}"


def test_goal_cadence():
    require(read(POLICY), "E2E is a goal-completion gate, not a per-task completion gate",
            "Finish all implementation tasks", "one consolidated E2E campaign",
            "before declaring the goal achieved", "not a trigger")
    for skill in ("writing-plans", "executing-plans", "verification-before-completion"):
        require(read(f"skills/{skill}/SKILL.md"),
                "verification-impact-analysis-v1.md#goal-level-e2e-task-level-focused-verification")


def test_diagnostics_do_not_waive_acceptance():
    require(read(POLICY), "bounded diagnostic smoke", "named unresolved UI/native risk",
            "not full E2E", "Keep necessary local security",
            "no required condition remains failed or unverified")
    assert "Put a bounded real-path smoke before broad validation" not in read("docs/mvl-laws.md")


def test_incremental_evidence():
    require(read(POLICY), "One run may prove many acceptance conditions",
            "Do not create one evidence file per requirement",
            "second ledger", "current checkpoint", "Read the original acceptance source",
            "not at every phase", "stop testing and reporting")


def test_rerun_scope_and_provenance():
    require(read(POLICY), "failed scenarios plus paths invalidated by the repair",
            "not restart the whole campaign by default", "a new commit hash alone",
            "actual integrated candidate", "financial, security and replay evidence")


def test_cdp_real_ui_and_output_budget():
    require(read(POLICY), "actual application UI", "backend effects and persistence",
            "at most 20 lines", "at most 80 relevant diagnostic lines",
            "never share authentication/storage", "otherwise say `UNKNOWN`")
    require(read("skills/test-driven-development/remote-cdp-browser-lifecycle.md"),
            "not every click", "native Electron journey", "Do not copy cookies",
            "not every interaction", "process whose ownership the fixture can prove")


def test_thin_verifier_and_closure():
    text = read("skills/verification-before-completion/SKILL.md")
    assert len(text.split()) <= 450, "entry expanded; move conditional detail to reference"
    require(text, "Do not preload during implementation", "routine task/test progress",
            "## Plan completion gate", "merged-result verification",
            "worktree removal and execution-branch retirement", "outer-goal completion",
            "only for a specific unresolved", "not a newly rebuilt matrix")


def test_reference_targets_exist():
    paths = [POLICY, "docs/mvl-laws.md",
             "skills/writing-plans/SKILL.md", "skills/executing-plans/SKILL.md",
             "skills/executing-plans/references/workflow-routing.md",
             "skills/verification-before-completion/SKILL.md",
             "skills/verification-before-completion/references/detailed-playbook.md",
             "skills/test-driven-development/remote-cdp-browser-lifecycle.md"]
    for path in paths:
        for target in re.findall(r"\]\(([^)]+)\)", read(path)):
            if "://" in target or target.startswith("#"):
                continue
            local = target.split("#", 1)[0]
            assert (ROOT / path).parent.joinpath(local).resolve().is_file(), (path, target)


def test_declared_versions_are_synchronized():
    config = json.loads(read(".version-bump.json"))
    assert len(config["files"]) == 10
    for item in config["files"]:
        if item["path"].endswith(".yaml"):
            match = re.search(r"^version:\s*(\S+)\s*$", read(item["path"]), re.MULTILINE)
            assert match, item["path"]
            value = match.group(1)
        else:
            value = json.loads(read(item["path"]))
            for part in item["field"].split("."):
                value = value[int(part)] if part.isdigit() else value[part]
        assert value == config["version"], (item["path"], value)


def main():
    global ROOT
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, help="Optional snapshot for negative-control checks")
    args = parser.parse_args()
    if args.root:
        ROOT = args.root.resolve()
    tests = [test_goal_cadence, test_diagnostics_do_not_waive_acceptance,
             test_incremental_evidence, test_rerun_scope_and_provenance,
             test_cdp_real_ui_and_output_budget, test_thin_verifier_and_closure,
             test_reference_targets_exist, test_declared_versions_are_synchronized]
    failures = 0
    for test in tests:
        try:
            test()
        except Exception as exc:
            failures += 1
            print(f"[FAIL] {test.__name__}: {exc}")
    print(f"Goal-level E2E policy: {'FAIL' if failures else 'PASS'} ({len(tests)} source checks, {failures} failures)")
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
