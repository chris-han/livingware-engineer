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

## Continuous execution and progress reporting

After every non-terminal observation, choose the next dependency-ready required action and continue. A GREEN checkpoint advances plan state; it does not return control to the user. A RED or unverified checkpoint normally creates debugging, repair, retry, replanning, or verification work.

For long-running work, progress updates may be one or two concise sentences after a meaningful milestone, material finding, or recovery-state change. They are observational, not approval checkpoints: do not end them with “Should I continue?”, do not wait for acknowledgment, and do not narrate every routine task or test.

A predeclared negative or inconclusive terminal disposition is legitimate closure when its predicate is satisfied. It is not a reason to retry indefinitely or ask whether the user wants to continue.

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
