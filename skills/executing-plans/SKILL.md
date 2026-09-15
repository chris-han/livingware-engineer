---
name: executing-plans
description: Use when a written implementation plan is ready to execute continuously through its authorized stopping criterion, involving the user only when judgment is genuinely necessary.
---

# Executing Plans

Load the authoritative plan/spec, preserve its contract across task boundaries, and execute continuously until the declared stopping criterion is satisfied or a genuine non-delegable human decision is required.

## Lifecycle

Entry: a written plan has been selected for implementation.
Exit: the plan's authorized stopping criterion is supported by evidence, or the Human Judgment Necessity Test is met.

A completed task, sprint exit, review, integration slice, or list of remaining gates is progress evidence, not a stop condition. Continue with the next dependency-ready state.

Never start implementation directly on `main`/`master` without explicit user consent. Preserve any stronger repository-specific branch/worktree rule.

## Human Judgment Necessity Test

Apply standing user delegation first. Stop for human judgment only when all three are true:

1. a real decision is required before the next action can proceed;
2. the decision is not already delegated and cannot be resolved from binding plan/spec/policy, observed evidence, established convention, executable checks, or a safe reversible default; and
3. choosing wrong has a material, not-cheaply-reversible consequence.

Examples include genuinely subjective product intent, a non-delegable legal/compliance determination, sensitive-data disclosure, irreversible/destructive action, or consequential external/production state change.

Ordinary implementation ambiguity, failed tests, review findings, unavailable local fixtures, phase transitions, or incomplete gates do not satisfy this test by themselves.

## Plan and MVL continuity

Treat the plan as authoritative dynamic context. Preserve its target/stopping criterion, prerequisites, dependency contract, impact/integration scope, required real components, permitted substitutes, forbidden mocks, and authority boundaries.

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
