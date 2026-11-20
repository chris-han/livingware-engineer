---
name: verification-before-completion
description: Use at an imminent final goal, integration, merge or release claim when evidence sufficiency needs checking. Do not preload during implementation or invoke for routine task/test progress.
---

# Verification Before Completion

**Reuse → verify the delta → stop.** This is a claim check, not a second test campaign or evidence-production workflow.

1. Name the claim and read the latest checkpoint plus relevant change. Reuse existing assertions/results when their relevant source, configuration, dependencies, fixtures, environment and acceptance contract still apply. Inspect only missing, failed, changed or uncertain coverage; read original requirements when coverage is absent, ambiguous or changed.
2. Apply [Verification Impact Analysis](../../docs/verification-impact-analysis-v1.md#goal-level-e2e-task-level-focused-verification). Tasks use focused tests. Required UI E2E runs once as a consolidated campaign after all implementation tasks are integration-ready, before goal completion; consume that result here. Do not restart it for a skill transition or unchanged merge. Rerun only failed or invalidated paths unless wider impact is demonstrated.
3. Check the actual assertions and outcomes, not just a green command or another agent's claim. A required connected UI journey starts in the real UI and proves effects through real internal components. Keep unverified conditions visible; never infer PASS from mocks, labels or screenshots alone.

## Plan completion gate

Confirm every required condition is covered using existing results and remaining gaps, not a newly rebuilt matrix or one file per requirement. Apply [Plan integration and retirement](../finishing-a-development-branch/references/plan-integration-and-retirement.md), including merged-result verification and worktree removal and execution-branch retirement where required. Plan disposition and outer-goal completion remain distinct; a negative outcome does not establish the goal.

Report only the scoped verdict, gaps and existing result reference. Sufficient evidence ends verification; failures return to repair, not an endless audit. Preserve required financial/security/replay records and explicit user requirements. Stop for human input only under the User Intervention Necessity Test.

Load [the detailed playbook](references/detailed-playbook.md) only for a specific unresolved validity, acceptance, artifact-review or closure question. No eager graph discovery, full-history reread, duplicate reports or raw CDP log dumps. Human usability and token savings remain unmeasured without actual measurements.
