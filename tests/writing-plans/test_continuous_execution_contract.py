from pathlib import Path
R=Path(__file__).resolve().parents[2]
def t(p): return (R/p).read_text()
def test_contract():
 assert "Execution Continuity Contract" in t("skills/writing-plans/SKILL.md")
 assert "intermediate GREEN MUST NOT be interpreted as plan completion" in t("skills/writing-plans/SKILL.md")
 assert "A GREEN checkpoint advances plan state; it does not return control to the user." in t("skills/executing-plans/SKILL.md")
 assert "Repository plan-state gate" in t("skills/executing-plans/SKILL.md")
 assert "plan-state validator/linter" in t("skills/executing-plans/SKILL.md")
 assert "Keep task/phase state separate from plan-level state." in t("skills/executing-plans/SKILL.md")
 assert "User Intervention Necessity Test" in t("docs/mvl-laws.md")
 assert "Progress reporting is observational, not a synchronization barrier." in t("docs/mvl-laws.md")
 assert "ask for consent before creating one" not in t("skills/using-git-worktrees/SKILL.md")
 assert "progress summaries waste their time" not in t("skills/subagent-driven-development/SKILL.md")
 assert "When a Codex `/goal` is active" in t("skills/using-superpowers/references/codex-tools.md")

def test_plan_integration_authority_contract():
 policy=t("skills/finishing-a-development-branch/references/plan-integration-and-retirement.md")
 assert "## Plan integration and retirement" in t("docs/mvl-laws.md")
 for invariant in (
  "local merge into `main`",
  "Agent-authored plan text is not an independent authorization source",
  "push, publication, deployment, admission or activation",
  "unqualified production changes",
  "exception's actual user instruction or repository policy",
 ):
  assert invariant in policy, invariant
 for skill in ("writing-plans", "executing-plans", "finishing-a-development-branch", "verification-before-completion", "using-git-worktrees"):
  assert "references/plan-integration-and-retirement.md" in t(f"skills/{skill}/SKILL.md"),skill


def test_plan_completion_requires_retirement_evidence():
 finish=t("skills/finishing-a-development-branch/SKILL.md")
 assert "For plan execution, use the default integration-and-retirement path" in finish
 assert "Only non-plan work without a delegated integration action uses the menu below" in finish
 verify=t("skills/verification-before-completion/SKILL.md")
 assert "merged-result verification" in verify
 assert "worktree removal and execution-branch retirement" in verify
 worktree=t("skills/using-git-worktrees/SKILL.md")
 assert "`MERGED` alone is not plan completion" in worktree


def test_parallel_candidate_authorization_source_contract():
 # Source-contract checks only: these do not establish runtime enforcement.
 source = t("skills/executing-plans/SKILL.md")
 policy = source.split("## Parallel implementation and candidate authorization\n", 1)[1].split("\n## ", 1)[0]
 for invariant in (
  "Default to one implementation path",
  "explicit prior user approval for that run",
  "single-path baseline",
  "model calls/tokens and estimated fees",
  "human review and integration effort",
  "budget ceiling and stopping conditions",
  "unknown cost is not zero cost",
  "silence",
  "agent-authored plan",
  "renewed explicit user approval",
  "an autonomous implementation ruling cannot enlarge authorization",
  "sequential delegation along one implementation path",
  "ordinary repair of that implementation",
  "existing risk-based review process",
  "nested delegation does not bypass this rule",
 ):
  assert invariant in policy, invariant


def test_parallel_authorization_entrypoints_share_owner():
 reference = "../executing-plans/SKILL.md#parallel-implementation-and-candidate-authorization"
 for skill in ("writing-plans", "dispatching-parallel-agents", "subagent-driven-development"):
  path = R / "skills" / skill / "SKILL.md"
  assert reference in path.read_text(), skill
  assert (path.parent / reference.split("#", 1)[0]).resolve().is_file(), skill
 parallel = t("skills/dispatching-parallel-agents/SKILL.md")
 assert '"Dispatch authorized?" -> "Parallel dispatch" [label="yes"]' in parallel
 assert '"Dispatch authorized?" -> "Sequential agents" [label="no"]' in parallel
 assert '"Can they work in parallel?" -> "Parallel dispatch"' not in parallel
 assert "must not silently expand into parallel fixes" in parallel
 subagents = t("skills/subagent-driven-development/SKILL.md")
 assert "a cap you would have asked to exceed" not in subagents
 assert "A ruling cannot expand parallel/candidate authorization or its cost limits." in subagents


if __name__ == '__main__':
    test_contract()
    test_plan_integration_authority_contract()
    test_plan_completion_requires_retirement_evidence()
    test_parallel_candidate_authorization_source_contract()
    test_parallel_authorization_entrypoints_share_owner()
    print('Continuous execution, parallel authorization and plan integration contract: PASS')
