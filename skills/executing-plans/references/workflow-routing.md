# Executing Plans Workflow Routing

Use this reference after `executing-plans` is active when the next execution state is not obvious from the approved plan and current evidence. The plan remains authoritative dynamic context; this file owns transition structure, not downstream debugging/TDD/verification mechanics.

## State model

```text
PLAN_REVIEW
  -> PREREQUISITES
  -> TASK_EXECUTION
  -> INTEGRATION
  -> MVL_CLOSURE (product feature only)
  -> COMPLETION_HANDOFF
```

Any material observation may route backward or sideways:

```text
unexplained failure -> systematic-debugging
known behavior change -> test-driven-development
completion claim -> verification-before-completion
plan/spec contradiction -> PLAN_REVIEW
new load-bearing dependency -> PREREQUISITES
```

Do not preload those skills before their entry conditions are reached.

## PLAN_REVIEW

Entry: a written plan is selected for execution.

Confirm only the execution-critical contract:

- target/stopping criterion;
- authoritative spec/plan relationship;
- prerequisites and new dependencies;
- impact/integration scope;
- required real components and forbidden mocks;
- user/repository authority boundaries.

If a critical gap can be resolved from standing delegation, repository evidence, established convention, or a safe reversible default, resolve it and continue. Stop for human judgment only under the root skill's Human Judgment Necessity Test.

Route to `PREREQUISITES` when a load-bearing dependency/setup gate exists; otherwise route to `TASK_EXECUTION`.

## PREREQUISITES

Satisfy declared dependency/setup gates before consumers rely on them. Mechanical install/version/smoke-test details remain owned by the plan, manifests, scripts, and tests; do not duplicate them here.

Route to:
- `TASK_EXECUTION` when prerequisites are green;
- `systematic-debugging` when a prerequisite failure is unexplained;
- `PLAN_REVIEW` when evidence proves the declared dependency contract itself is wrong.

## TASK_EXECUTION

Execute dependency-ready tasks continuously. Use the current task's preservation/behavior contract and smallest sufficient tests.

Route to:
- `test-driven-development` for authorized changed behavior;
- `systematic-debugging` for new unexplained evidence;
- next dependency-ready task when local evidence is green;
- `INTEGRATION` at the coherent sprint/integration boundary.

A completed task is progress evidence, not a user checkpoint.

## INTEGRATION

Exercise the affected production path according to the plan's impact radius. Use real in-repo components required by the claim; substitute only genuinely external/nondeterministic boundaries where permitted.

For UI/browser work, use the existing browser lifecycle contract rather than duplicating it here.

Route to:
- `systematic-debugging` for unexplained integration failure;
- `test-driven-development` for a known implementation gap;
- `MVL_CLOSURE` when the plan is a product MVL requiring measurement/feedback/re-test;
- `COMPLETION_HANDOFF` for maintenance/non-product work once required integration is supported.

## MVL_CLOSURE

Preserve the same target user/value hypothesis/smallest real journey from the plan. Run only the declared measurement, feedback, evidence-driven improvement, and comparable re-test required by the stopping criterion.

Do not invent a learning loop for maintenance work.

Route to:
- earlier states when measurement exposes an implementation or plan defect;
- `COMPLETION_HANDOFF` when the MVL stopping criterion is satisfied.

## COMPLETION_HANDOFF

Invoke `verification-before-completion` for the exact claims being made. When supported, hand off to `finishing-a-development-branch` for the already-authorized branch action.

Do not carry the executing-plans workflow body into completion verification.

## Compact transition handoff

Across states carry only:

```text
current plan/task state
binding intended/preserved behavior
relevant evidence already obtained
changed/affected surface
unresolved material risk
next state entry reason
```

Do not carry complete prior skill bodies or duplicate test output.
