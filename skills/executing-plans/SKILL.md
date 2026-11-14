---
name: executing-plans
description: Use when a written implementation plan is ready to execute continuously through its authorized stopping criterion, involving the user only when intervention is genuinely necessary.
---

# Executing Plans

Load the authoritative plan/spec, preserve its contract across task boundaries, and execute continuously until a declared terminal disposition is supported by evidence or the User Intervention Necessity Test is met.

## Lifecycle

Entry: a written plan has been selected for implementation.
Exit: the plan's authorized stopping criterion and applicable integration/retirement obligations are proved, or the User Intervention Necessity Test is met.

A completed task, sprint exit, review, integration slice, or list of remaining gates is progress evidence, not a stop condition. Continue with the next dependency-ready state.

If direct implementation on `main`/`master` is not already authorized, use the safe isolation path defined by `using-git-worktrees` when repository and harness policy permit it. Do not ask merely to choose branch ceremony; involve the user only when no safe authorized isolation path exists.

## Parallel implementation and candidate authorization

Default to one implementation path. Before starting multiple implementation agents concurrently or generating multiple competing implementations of the same task, disclose the proposal and obtain explicit prior user approval for that run. Complexity, high risk, independent tasks, available parallel tools, or potential speedup are not authorization. Discussing design alternatives is allowed; do not start their implementation before approval. Generating candidates sequentially, in separate worktrees, or through nested delegation does not bypass this rule.

The proposal must explain the concrete uncertainty or bottleneck, why a single implementation or sequential validation is insufficient, the intended agent and candidate counts and scope, common acceptance criteria, and how results will be compared, selected, and integrated. Assess total incremental cost against the single-path baseline: model calls/tokens and estimated fees, compute/runtime resources, duplicated testing, coordination, and human review and integration effort. State a budget ceiling and stopping conditions before launch. When costs cannot be reliably estimated, disclose the uncertainty and propose enforceable call/token/runtime/resource caps; unknown cost is not zero cost. Do not launch without a bounded cost basis the user has accepted.

Approval of the development goal, an agent-authored plan, generic autonomy, silence, or approval of an unrelated run does not authorize this strategy. Explicit user approval of a plan that discloses this run and its limits counts; do not ask twice for the same authorized scope. Keep the approval and limits in the existing plan or tracker, or reference the existing user instruction; do not create a parallel authorization ledger.

Stay within the approved agent/candidate counts, scope, and budget. Before increasing those counts, expanding the scope, or incurring costs expected to exceed the approved ceiling, obtain renewed explicit user approval. Stop launching additional work at the limit or stopping condition; an autonomous implementation ruling cannot enlarge authorization. Without approval, continue with the single-path or sequential approach when feasible; report a blocker only when no authorized path remains. This explicit authorization boundary takes precedence over generic continuous-execution or delegated-autonomy defaults.

This rule does not require extra approval for ordinary tests, sequential delegation along one implementation path, ordinary repair of that implementation, or the existing risk-based review process. It is not a blanket approval checkpoint for all development work.

## Execution economics and evidence reuse

Honor the repository's development lane. Follow [development before container integration](../../docs/verification-impact-analysis-v1.md#development-before-container-integration): source/dev implementation and focused checks first; freeze an integration-ready candidate before application-container work. Missing dev packages do not justify moving development into Docker.

Follow [goal-level E2E, task-level focused verification](../../docs/verification-impact-analysis-v1.md#goal-level-e2e-task-level-focused-verification). Complete all implementation tasks with focused tests and necessary local integration; assemble the real candidate and prepare services/fixtures, then run one consolidated UI-driven E2E campaign before claiming the goal. Explicit target ordering belongs inside final acceptance, not automatically between implementation tasks. A bounded early diagnostic smoke needs a concrete unresolved boundary risk or explicit requirement; it is not routine E2E.

Use the latest checkpoint, relevant diff and existing assertions/results. Do not rebuild the requirement-to-evidence mapping, reload full history, or emit a new receipt for each passing task. Update only meaningful recovery state, remaining gaps and references to reusable results in the existing tracker. After a failure, rerun the failed and invalidated paths, expanding only for demonstrated impact. Reuse unchanged integrated results through merge and completion; do not equate necessary regression checks with waste or mark a flaky failure as a pass.

When a task is materially cross-boundary or the user requests an efficiency comparison, consult [Execution Economics](references/execution-economics.md) and the cross-cutting [Token-Efficient Execution Policy](../using-superpowers/references/token-efficient-execution.md) only for the unresolved economic question. Consume the plan's bounded failure review without reopening settled discovery. For CDP, use deterministic scripts and bounded summaries; leave raw logs locally and inspect only relevant failure excerpts.

When telemetry is accessible, report planning/review, input/output/cache tokens, total accounting convention, wall time, repeat source reads and test/rework counts; when it is not, report `UNKNOWN` rather than guessing. Compare with a prior baseline only after verified terminal completion and with task/risk comparability disclosed. Lower tokens without equivalent correctness is not improvement. Economic instrumentation must not block routine autonomous execution or expose secrets.

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

The single mutable plan authority belongs in the repository’s main-branch checkout, separate from any bound implementation worktree. Draft, activate, update, and archive it there; a copy in a branch worktree is a historical snapshot, not another authority. Preserve concurrent main-checkout edits. Explicit user or repository instructions for a different authority location take precedence.

A plan may remain authoritative at a repository or worktree location different from the worktree named by `execution_worktree`. When that occurs:

- read and validate the plan from its authoritative source location;
- execute authorized implementation and necessary recovery/test artifacts inside the bound execution worktree;
- preserve the plan's declared `execution_worktree`, `execution_branch`, and `execution_base_branch` independently from the plan file's physical location;
- treat the main-checkout plan path as the single mutable plan authority;
- resolve plan-relative references against the authoritative plan's repository context when their meaning depends on plan location;
- record an explicit authoritative-plan path or equivalent source binding when the plan is intentionally external to the execution worktree.

Do not:

- copy, duplicate, relocate, regenerate, or synthesize the plan inside the execution worktree merely to make a relative path resolve;
- treat absence of the plan file from the execution worktree as workspace drift when the plan explicitly binds an external authoritative source;
- create a second mutable plan ledger in the execution worktree or silently switch plan authority to a convenience copy;
- rebase, merge, or recreate a worktree solely so the authoritative plan becomes physically colocated with execution.

If execution requires a plan-state change, write it to the authoritative main-checkout plan, preserving concurrent edits. A later branch rebase, merge, or integration step may naturally bring the plan file into the execution branch; that is an integration outcome, not an execution prerequisite.

Verify plan authority and workspace binding independently:

```text
authoritative plan identity/path is still valid
actual worktree root == plan.execution_worktree
actual branch        == plan.execution_branch
intended merge target == plan.execution_base_branch
```

A valid authoritative plan located outside the execution worktree is not workspace drift. A copied or diverged second plan authority is plan-authority drift and must be repaired before execution continues.

For governed or recoverable work:

- keep implementation edits and required execution/recovery evidence in the bound execution worktree unless the plan owns a cross-repository action; write plan-state changes to the authoritative main-checkout plan;
- checkpoint meaningful recovery boundaries in commits so load-bearing evidence is preserved; do not create a report or evidence commit for every PASS;
- when a gate intentionally freezes the exact executable/evidence state for the next phase, update `execution_commit` to that commit and state what it binds;
- do not move `execution_commit` merely because documentation metadata changed afterward;
- do not claim a phase is reproducible when its required artifacts are still uncommitted;
- do not switch to `main` or another worktree to 'finish one small thing' without rebasing the plan/workspace binding first.

At a terminal plan disposition, apply [Plan integration and retirement](../finishing-a-development-branch/references/plan-integration-and-retirement.md) and route to `finishing-a-development-branch`. An isolated GREEN or negative disposition does not close workspace obligations. Integrate eligible implementation or negative-outcome evidence, verify the target and retire the owned worktree/branch before marking whole-plan completion. Honor preservation/PR exceptions only when bound to an actual user instruction or repository policy; an agent-written plan clause cannot create that authority.

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

Apply [first real loop before breadth](../../docs/mvl-laws.md#engineering-execution-first-real-loop-before-breadth): implement toward the real journey, use focused checks during the task list, and reserve the consolidated E2E campaign for integration readiness. Diagnose the first concrete failing boundary without turning each task into a full UI run. Preserve necessary security/correctness prerequisites and final acceptance.

After every non-terminal observation, choose the next dependency-ready required action and continue. A GREEN checkpoint advances plan state; it does not return control to the user. A RED or unverified checkpoint normally creates debugging, repair, retry, replanning, or verification work.

**Silent-by-default execution:** do not emit a user-visible update for each tool call, test, commit, normal fix, successful checkpoint or phase transition. Routine passing output needs no additional durable narration. Communicate a meaningful independently useful milestone on an extended run, a material risk/scope/outcome change, or a genuine blocker; use one compact update and continue unless user intervention is necessary. Obey explicit host/user progress requirements. Do not end updates with “Should I continue?” or wait for acknowledgment.

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

Read `references/workflow-routing.md` only when the next state is non-obvious:

```text
plan review -> prerequisites -> implementation tasks + focused tests
           -> integration-ready candidate -> consolidated goal verification
           -> MVL closure when applicable -> completion handoff
```

Route by current evidence rather than preloading future workflows:

- unexplained failure -> `systematic-debugging`;
- authorized changed behavior -> `test-driven-development`;
- final goal/integration/merge/release claim needing an evidence check -> `verification-before-completion`;
- required UI campaign or bounded UI diagnostic -> the existing browser lifecycle contract;
- branch completion -> `finishing-a-development-branch` when supported and authorized.

Routine focused-test/task progress does not activate the completion verifier. The downstream owner defines its mechanics; do not duplicate debugging, TDD, verification, browser, review, packaging or version-sync procedures here.

## Real-path invariant

When the claim crosses component boundaries, prove the smallest affected production path through the real in-repo components that matter. Substitute only genuine external or nondeterministic boundaries where the plan permits it. A mock of the internal architecture cannot prove that architecture is integrated.

Reuse valid unchanged evidence. Rerun checks invalidated by changed code/config/dependencies/fixtures/environment/acceptance; do not rerun expensive evidence merely because workflow state changed.

## Compact handoff

Across workflow transitions carry only current plan/task state, binding behavior, affected surface, valid result reference, unresolved material risk and next action. Do not carry complete prior skill bodies, broad repository dumps, duplicate matrices or test narration.

## Completion

At the final goal/integration/merge/release claim, use `verification-before-completion` to check sufficiency of existing results and remaining gaps—not to launch a second campaign. Apply its Plan completion gate and authorized integration/retirement obligations. Do not preload it or invoke it for ordinary task progress. An unchanged merge reuses valid results; a changed merge needs affected checks.

Keep incomplete requirements visible; a green command list or completed implementation slice cannot close the plan or host goal. A declared negative/inconclusive disposition closes only the scope supported by its predicate and evidence. Evidence boundaries are not human approval checkpoints.
