# Executing Plans Workflow Routing

Use this reference after `executing-plans` is active when the next execution state is not obvious from the approved plan and current evidence. The plan remains authoritative dynamic context; this file owns transitions, not downstream mechanics. [Verification Impact Analysis](../../../docs/verification-impact-analysis-v1.md#goal-level-e2e-task-level-focused-verification) owns test cadence and evidence economy.

## State model

```text
PLAN_REVIEW -> PREREQUISITES
            -> TASK_EXECUTION (focused checks)
            -> INTEGRATION_READY (all implementation tasks complete)
            -> GOAL_VERIFICATION (one consolidated E2E campaign when required)
            -> MVL_CLOSURE (when declared)
            -> COMPLETION_HANDOFF
```

Unexplained failure routes to `systematic-debugging`; a known behavior change to `test-driven-development`; a plan contradiction to `PLAN_REVIEW`; a new load-bearing dependency to `PREREQUISITES`. Do not preload these skills.

## PLAN_REVIEW

Confirm only the execution-critical contract: goal/stopping criterion, authoritative spec, prerequisites, required real components/forbidden substitutes, scope and authority. Reuse established context; resolve gaps from existing authority or evidence before interrupting the user. Go to prerequisites when needed, otherwise task execution.

## PREREQUISITES

Satisfy declared dependency/setup checks before consumers rely on them. Existing scripts/manifests own the mechanics. An unexplained failure goes to debugging; an incorrect dependency contract goes back to plan review. A healthy dependency is not goal E2E success.

## TASK_EXECUTION

Implement dependency-ready tasks with focused behavior/contract and necessary local real-component tests. A completed task advances to the next task, not to another E2E campaign or a user checkpoint. Permit a bounded early UI diagnostic only for a specific unresolved risk or explicit requirement. Do not claim whole-goal completion from local GREEN.

## INTEGRATION_READY

After all implementation tasks are complete, assemble the candidate and check services, dependencies, fixtures and required application targets. Missing implementation returns to task execution. Cheap readiness checks are not the final journey and do not replace it.

## GOAL_VERIFICATION

For a UI goal, use one consolidated CDP-driven campaign starting from the real application UI and exercising real internal services, persisted state and required account boundaries. For non-UI goals, use their actual entry point. Preserve explicitly required target ordering inside this campaign. Use the browser lifecycle contract for owned sessions, bounded output and cleanup; do not duplicate it here.

On failure, return to diagnosis/repair and repeat only failed or invalidated paths, broadening only for demonstrated impact. Keep reusable results and unresolved gaps in the existing checkpoint. Move to MVL closure only when declared measurement obligations remain; otherwise proceed to completion handoff.

## MVL_CLOSURE

Preserve the same target user, value hypothesis and journey. Perform only the measurement, feedback, justified improvement and comparable retest required by the declared contract. Do not invent a learning loop for maintenance. Changed implementation invalidates affected evidence, not automatically the entire campaign.

## COMPLETION_HANDOFF

Use `verification-before-completion` for final evidence sufficiency, not to launch another campaign. Then use the authorized integration/retirement path. A changed merge needs affected verification; an unchanged merge reuses valid evidence. Failed or unverified requirements keep the goal incomplete.

## Compact transition handoff

Carry only current plan/task state, binding behavior, relevant result reference, changed surfaces, unresolved risk and next action. Do not carry complete prior skill bodies, whole logs or duplicate matrices. Routine passing checks need no new durable report.
