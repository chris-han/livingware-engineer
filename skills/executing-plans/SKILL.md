---
name: executing-plans
description: Use when a written implementation plan is ready to execute continuously through its authorized stopping criterion, involving the user only when intervention is genuinely necessary.
---

# Executing Plans

Load the authoritative plan/spec, preserve its contract across task boundaries, and execute continuously until a declared terminal disposition is supported by evidence or the User Intervention Necessity Test is met.

## Lifecycle

Entry: a written plan has been selected for implementation.
Exit: the plan's authorized stopping criterion yields a declared terminal disposition supported by evidence, or the User Intervention Necessity Test is met.

A completed task, sprint exit, review, integration slice, or list of remaining gates is progress evidence, not a stop condition. Continue with the next dependency-ready state.

If direct implementation on `main`/`master` is not already authorized, use the safe isolation path defined by `using-git-worktrees` when repository and harness policy permit it. Do not ask merely to choose branch ceremony; involve the user only when no safe authorized isolation path exists.

## Repository plan-state gate

Before the first implementation edit, inspect and obey the repository's governed-plan lifecycle contract when one exists. Do not invent or normalize plan status from memory. If the repository provides a plan-state validator/linter, run it before execution and again before completion/commit.

Keep task/phase state separate from plan-level state. An intermediate task marked completed advances the plan but does not imply that the whole plan is complete. Likewise, do not use a lifecycle label such as `active` as a plan-status value when the repository schema owns those concepts separately.

When the repository requires execution metadata, bind the active execution method/workspace (for example this skill plus isolated-worktree vs explicitly-authorized-main mode) before continuing. If an existing selected plan uses legacy or inconsistent execution metadata, normalize it to the repository contract before further implementation; do not rewrite historical archived plans merely for style.

## Worktree execution tracking

When execution runs in an isolated worktree, the worktree lifecycle binding is part of the plan contract, not incidental environment state.

Before the first substantive edit and again before every hard execution gate, verify:

```text
actual worktree root == plan.execution_worktree
actual branch        == plan.execution_branch
intended merge target == plan.execution_base_branch
```

If the repository uses different metadata names, verify equivalent semantics. A mismatch is a plan/workspace drift error: repair it before continuing.

### Authoritative plan and execution workspace are separate identities

The authoritative plan source and the bound execution workspace are separate identities. Path locality is an implementation convenience, never an authority rule.

A plan may remain authoritative at a repository or worktree location different from the worktree named by `execution_worktree`. When that occurs:

- read and validate the plan from its authoritative source location;
- execute authorized implementation, generated evidence, checkpoints, and experiment artifacts inside the bound execution worktree;
- preserve the plan's declared `execution_worktree`, `execution_branch`, and `execution_base_branch` independently from the plan file's physical location;
- treat the authoritative plan path as the single mutable plan authority unless the plan explicitly transfers plan ownership to the execution worktree;
- resolve plan-relative references against the authoritative plan's repository context when their meaning depends on plan location;
- record an explicit authoritative-plan path or equivalent source binding when the plan is intentionally external to the execution worktree.

Do not:

- copy, duplicate, relocate, regenerate, or synthesize the plan inside the execution worktree merely to make a relative path resolve;
- treat absence of the plan file from the execution worktree as workspace drift when the plan explicitly binds an external authoritative source;
- create a second mutable plan ledger in the execution worktree or silently switch plan authority to a convenience copy;
- rebase, merge, or recreate a worktree solely so the authoritative plan becomes physically colocated with execution.

If execution requires a plan-state change, write that change to the authoritative plan owner/location unless the plan explicitly declares that plan ownership has transferred to the execution worktree. A later branch rebase, merge, or integration step may naturally bring the plan file into the execution branch; that is an integration outcome, not an execution prerequisite.

Verify plan authority and workspace binding independently:

```text
authoritative plan identity/path is still valid
actual worktree root == plan.execution_worktree
actual branch        == plan.execution_branch
intended merge target == plan.execution_base_branch
```

A valid authoritative plan located outside the execution worktree is not workspace drift. A copied or diverged second plan authority is plan-authority drift and must be repaired before execution continues.

For governed or recoverable work:

- keep implementation edits, generated execution evidence, stage receipts, and execution checkpoints in the bound execution worktree unless the plan explicitly owns a cross-repository action; write plan-state changes to the authoritative plan owner/location unless the plan explicitly assigns plan ownership to the execution worktree;
- checkpoint meaningful completed gates in commits so evidence does not exist only as uncommitted worktree state;
- when a gate intentionally freezes the exact executable/evidence state for the next phase, update `execution_commit` to that commit and state what it binds;
- do not move `execution_commit` merely because documentation metadata changed afterward;
- do not claim a phase is reproducible when its required artifacts are still uncommitted;
- do not switch to `main` or another worktree to 'finish one small thing' without rebasing the plan/workspace binding first.

At a terminal plan disposition, execution is not operationally closed while the verified branch remains stranded in an active worktree. Route to `finishing-a-development-branch` unless the explicit terminal action is to preserve the branch/worktree or keep it for PR review.

For submodule-backed work, preserve the two-level closure boundary:

```text
submodule worktree branch
  -> merge/verify inside submodule
  -> update parent repository submodule pointer
  -> verify/commit parent pointer
  -> only then retire the submodule worktree
```

A merged submodule branch with an unupdated parent pointer is not integrated closure.

## Continuous execution and progress reporting

After every non-terminal observation, choose the next dependency-ready required action and continue. A GREEN checkpoint advances plan state; it does not return control to the user. A RED or unverified checkpoint normally creates debugging, repair, retry, replanning, or verification work.

For long-running work, progress updates may be one or two concise sentences after a meaningful milestone, material finding, or recovery-state change. They are observational, not approval checkpoints: do not end them with “Should I continue?”, do not wait for acknowledgment, and do not narrate every routine task or test.

A predeclared negative or inconclusive terminal disposition is legitimate plan closure when its predicate is satisfied. It is not a reason to retry the same plan indefinitely or ask whether the user wants to continue. Check the user's outer objective separately: if the requested end state remains unmet, preserve that goal as incomplete and route to the next authorized recovery or successor action. If no such action is available, report the stopping evidence and the unmet outcome; do not claim the outer goal is complete.

## User Intervention Necessity Test

Apply the cross-cutting test in `docs/mvl-laws.md` after standing user delegation. Stop for the user only when the next required action cannot proceed autonomously, authorized recovery paths are exhausted, and the missing capability is genuinely user-owned. Ordinary implementation ambiguity, failed tests, review findings, unavailable local fixtures, phase transitions, incomplete gates, or a completed checkpoint do not satisfy this test by themselves.

## Plan and MVL continuity

Treat the plan as authoritative dynamic context. Preserve its target/stopping criterion, permitted terminal dispositions, prerequisites, dependency contract, impact/integration scope, required real components, permitted substitutes, forbidden mocks, and authority boundaries.

For product features, preserve the same MVL target user/job, value hypothesis, smallest real journey, trial inputs, metrics, feedback surface, improvement levers, and comparable re-test through completion. Local task success is not permission to redefine the feature contract.

Do not copy those fields into a second ledger. Reference the plan and existing repository evidence.

## Dependency boundary

A consumer must not rely on a new load-bearing dependency until the plan's declaration/install/smoke-contract gate is satisfied. If execution discovers a genuinely new dependency or contradicts the declared contract, return to the plan/prerequisite state before consumers proceed.

A successful install alone is not readiness; exercise the minimum real API/behavior the plan relies on.

## Dynamic workflow routing

Read `references/workflow-routing.md` when the next execution state is non-obvious. It owns the state topology:

```text
plan review -> prerequisites -> task execution -> integration
           -> MVL closure when applicable -> completion handoff
```

Route by current evidence rather than preloading future workflows:

- unexplained failure -> `systematic-debugging`;
- authorized changed behavior -> `test-driven-development`;
- completion/correctness claim -> `verification-before-completion`;
- UI/browser evidence -> the existing browser lifecycle contract;
- branch completion -> `finishing-a-development-branch` when supported and authorized.

The owning downstream skill defines its mechanics. Do not duplicate debugging, TDD, verification, browser, review, packaging, or version-sync procedures here.

## Real-path invariant

When the claim crosses component boundaries, prove the smallest affected production path through the real in-repo components that matter. Substitute only genuine external or nondeterministic boundaries where the plan permits it. A mock of the internal architecture cannot prove that architecture is integrated.

Reuse valid unchanged evidence. Rerun checks invalidated by changed code/config/dependencies/fixtures/environment; do not rerun expensive evidence merely because workflow state changed.

## Compact handoff

Across workflow transitions carry only:

```text
current plan/task state
binding intended/preserved behavior
affected surface
valid evidence already obtained
unresolved material risk
next-state entry reason
```

Do not carry complete prior skill bodies, broad repository dumps, or duplicate test narration.

## Completion

Before claiming fixed/correct/complete/integrated/ready-to-merge/release, enter `verification-before-completion` for the exact claim. After supported completion evidence, use the already-authorized branch action or the branch-completion workflow. Evidence boundaries are not human approval checkpoints.

For whole-plan completion, apply that skill's Plan completion gate to the original acceptance contract. Keep incomplete requirements visible through task boundaries; a green command list or completed implementation slice cannot authorize closing the plan or host goal. A declared negative/inconclusive terminal disposition may close the plan only when its own predicate and evidence requirements are satisfied.
