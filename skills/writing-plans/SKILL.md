---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

## MVL Law 1 — Fast-to-Aha

For product MVLs where governance is in the path, treat time-to-first-useful-result as an acceptance criterion. Distinguish recorded default-pass gates from blocking gates; ordinary low-risk journeys must not stop for approval ceremony. A user-intervention gate is allowed only when the User Intervention Necessity Test in `docs/mvl-laws.md` is satisfied after applying any standing user delegation.

Classify every planned gate as either **autonomous** or **user-intervention-required**. Autonomous gates include tests, typecheck, lint, build, contract checks, service/browser fixtures, integration/E2E evidence, deterministic review findings, and ordinary reversible engineering rulings; they advance automatically when satisfied and never require a human checkpoint. A user-intervention-required gate is allowed only when standing delegation plus the User Intervention Necessity Test says the next required action genuinely depends on user-owned judgment, authority, access, credentials, or consequential external action. Do not create approval or checkpoint tasks merely to mark a phase boundary.

Apply [first real loop before breadth](../../docs/mvl-laws.md#engineering-execution-first-real-loop-before-breadth) as an implementation priority, not a mandate for early or per-task E2E. Follow [goal-level E2E, task-level focused verification](../../docs/verification-impact-analysis-v1.md#goal-level-e2e-task-level-focused-verification): complete the implementation task list with focused checks, prepare the integrated candidate, then schedule one consolidated real-UI campaign before goal completion. Earlier UI smoke needs a named unresolved risk or explicit requirement and remains bounded diagnostic evidence.

## Overview

Write an implementation plan that names the affected files/owners, changes, focused tests, dependencies and final user-visible outcome. Keep tasks independently testable, DRY and YAGNI. Reference existing specifications, interfaces, fixtures and procedures rather than copying them into every task. Include inline code only when it resolves a real ambiguity.

**Communication:** deliver the useful plan or material decision directly; do not generate a ceremonial status message to announce skill use. Follow explicit host progress requirements.

**Context:** create any isolated implementation worktree through `using-git-worktrees` at execution time.

**Save plans to:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`, unless the user/repository specifies another location.

**Plan authority:** Keep the single mutable plan in the repository’s main-branch checkout, in the repository-required location. Draft, activate, update and archive it there; bind an implementation worktree separately. A branch-worktree copy is historical, not another authority. Preserve concurrent main edits. Explicit user/repository location rules take precedence.

## Execution Continuity Contract

Every executable multi-step plan MUST declare an **authorized stopping criterion** and **permitted terminal dispositions** near the top. A plan is a completion contract, not merely a checklist.

Bind the stopping criterion to [Plan integration and retirement](../finishing-a-development-branch/references/plan-integration-and-retirement.md): name the integration target, required merged-result verification and owned-resource retirement. A preservation, qualification-only or PR-handoff exception must cite its user/repository authority; isolation alone does not authorize it. Push and production activation remain separate boundaries.

Unless explicitly bounded, intermediate tasks, reviews, focused tests, commits and implementation milestones are non-terminal. Advance to the next dependency-ready obligation; route recoverable failures to repair/retest or bounded replanning, not a routine human checkpoint. Progress updates do not wait for acknowledgment. A predeclared negative/inconclusive outcome is terminal only when its predicate is proved.

For a bounded scope, state it explicitly. Otherwise an intermediate GREEN MUST NOT be interpreted as plan completion. A host persistent goal remains the outer objective; do not create competing goal authority or close it from an intermediate gate.

## Requirement Basis Before Task Decomposition

Consume the effective requirement basis under [the shared requirements workflow contract](../requirements-clarification/references/requirements-workflow.md). Reuse source/version references, accepted dispositions, assumptions, unresolved questions and affected acceptance criteria. Resolve material conflicts before dependent actions; independent safe work may continue. Do not reopen settled answers or copy the conversation into a new ledger.

For features with long-running elicitation/modeling/review, carry runtime state ownership, checkpoint/reload and receipt-recovery requirements into implementation and acceptance. Coding-plan progress is not product-workflow persistence, and completing a task grants no runtime admission authority.

## Risk-based pre-execution failure review

For R2/R3 or cross-owner tasks involving async state, identity/profile/tenant boundaries, caches, timeouts, native lifecycle or external adapters, perform one bounded adversarial review before activation. Freeze the small relevant owner map and evidence census; examine cold/warm, profile-change, delayed response, failure, empty result, auth and timeout counterexamples as applicable. Use fresh scoped review context when useful, not a competing implementation. Record material findings as `REVISE | TEST_EARLY | ACCEPT_WITH_REASON` in the existing plan.

`TEST_EARLY` selects the cheapest necessary contract/seam check; it does not require a full UI journey before each task or sprint. A native/UI diagnostic smoke is allowed only for a named risk or explicit requirement. Final E2E remains after the implementation list is integration-ready. Load [Pre-Execution Failure Review](references/pre-execution-failure-review.md) only for details not resolved here; the shared VIA policy owns cadence.

This is autonomous and proportionate, not a universal approval gate or token quota. Skip it for ordinary bounded fixes and stop when no new material risk remains. For requested economics comparisons, the historical [Windows baseline](../../docs/engineering-economics/2026-11-07-windows-provider-query-only-baseline.md) is a reference with comparability limitations, not proof of causal savings.

## Architecture Delta Before Architecture Work

For subsystem, service, store, interface, ownership or structural data-flow changes, apply `docs/architecture-delta-principle.md` using the design's current-state evidence rather than reinventing architecture from the title.

Only `PROCEED_WITH_DELTA` admits architecture-changing tasks. `UNKNOWN` requires investigation, not a missing-capability claim; `NO_CHANGE_REQUIRED` is terminal and must not manufacture implementation. Each architecture-changing task traces to a verified delta item, stays inside its scope fence and names closing evidence. Record `NOT_APPLICABLE` for work without architecture effects. This is structural verification, not a human-approval ceremony.

## MVL Is the Feature-Development Unit

Plan a **Minimum Viable Loop (MVL)** for product features. **MVL is the feature-development unit, not a test unit.** Tests are evidence inside that loop.

Preserve the same contract through requirements, design, implementation, focused tests, final real-component/UI verification, measurement, feedback, improvement and comparable retest. Do not stop at code complete or green unit tests when the feature outcome remains unproved.

Every feature plan defines near the top:

- **Target user / job-to-be-done** and **value hypothesis**.
- **Smallest real user journey**, **realistic trial inputs**, prerequisites and dependencies.
- **Technical success metrics**, **UX success metrics** and **feedback / telemetry capture**.
- **Improvement levers**, **re-evaluation method** and **stopping criterion for this MVL iteration**.

These constrain implementation, integration and acceptance. For non-product maintenance without a learning loop, use `MVL: not applicable — <reason>` rather than inventing one.

### Product Value Validation

For value/adoption/activation/retention/workflow-insertion or market-pull claims, apply `references/product-value-validation.md` before admitting implementation tasks. Distinguish problem evidence from assumptions, value from implementation, Aha from onboarding, behavioral/economic evidence from stated preference, and feature success from PMF.

Record evidence level `E0`–`E5`, falsifiable hypothesis, observable Aha and meaningful time-to-Aha target, counter-evidence, and the PMF signal without claiming the feature establishes PMF. Use `READY_TO_PLAN`, `VALIDATE_FIRST` or `NOT_APPLICABLE`. `VALIDATE_FIRST` narrows to a useful experiment, not a human-approval gate. Verified defects, behavior-preserving refactors, platform maintenance, mandated security/legal/contractual work, architecture integrity or qualification without a value claim may be `NOT_APPLICABLE` with the authoritative reason.

## IA Before UI

For UI design/review, carry forward or establish the `IA-Before-UI Review` from `docs/ia-before-ui.md` before visual/production tasks. Start with JTBD and cognitive-work allocation, then task flow, hierarchy, current design sources and shared primitives. For Asimov, use `skills/frontend-design/references/asimov-alignment.md`, not a generic layout or stale showcase.

Only `GO_FOR_UI` admits material production UI tasks. Missing workload allocation, duplicated semantic owners, implementation-model leakage, ambiguous actions, missing state ownership, responsive ambiguity or missing design-source mapping yields `REVISE_IA`; repair the IA first. Use the policy's narrow `NOT_APPLICABLE` exception for IA-preserving corrections with a reason. No extra approval turn is implied.

Reuse the applicable IDs from `skills/frontend-design/references/ia-ux-checklist.md` when context, hierarchy, disclosure, state or recovery changes. Bind UI tasks and final browser acceptance to the same sources, JTBD and effort target. Keep human usability unmeasured without human evidence; do not waive explicitly required benefit measurements. Do not copy the full checklist into each task.

## Impact Radius Before Test Scope

Use Verification Impact Analysis (VIA) to select the smallest surface that can falsify the change claim, not diff size or habit. Inspect relevant callers/consumers, wiring, routes, persistence/schema, async and trust boundaries. Use an available current code graph only when useful; targeted source is enough for bounded known changes and whole-repository indexing is not a prerequisite.

```text
R0 local only             -> focused behavior/unit tests
R1 one seam               -> focused real seam integration
R2 multiple components    -> real-component integration
R3 user/UI/cross-process  -> goal-level E2E and required real-browser evidence
```

D0 deterministic invariants and D1 focused behavior/integration run during development. Broad D2/goal E2E runs on the integration-ready candidate, not after every task, commit or sprint. Impact radius selects required coverage, not mandatory repetition. Read `docs/verification-impact-analysis-v1.md` and `../test-driven-development/impact-radius-testing.md` only for unresolved scope details.

### Consolidated goal acceptance

Schedule one campaign after all implementation tasks are ready and before declaring the goal achieved. For UI goals, begin at the actual application UI, use deterministic CDP/qualified adapter actions and verify persisted/backend effects through real internal components. Include the required applications and ordering inside this campaign; do not turn Windows-first acceptance into an inferred ban on implementing Workspace earlier. Explicit user/repository restrictions still win.

Specify required journey(s), candidate/environment, observable success, bounded runner limits and the existing result location. Keep one run reference capable of covering multiple assertions. No per-task full E2E, fresh requirement-to-evidence matrix or one evidence file per requirement. Reuse established coverage; final review checks remaining gaps and invalidated paths. Rerun failed/affected scenarios only, broadening for demonstrated shared impact. Unchanged merge results reuse evidence; the actual final candidate must be covered.

Use the existing browser lifecycle and VIA output budgets; do not plan an LLM turn for every click, full DOM dump or routine screenshot. Required final acceptance, financial/security audit records and user-controlled authorization remain intact.

## Dependency and Prerequisite Contract

Declare a new or materially changed dependency before feature code relies on it: name, pin/range/commit/image, reason, manifest/lock owner, setup command, non-secret configuration, compatibility and runtime/build/test/security/license implications. Specify a real dependency smoke/contract check and removal of a replaced dependency when applicable.

```text
select -> declare/pin -> install -> prove minimum real behavior -> build consumer
```

Manifest presence or successful installation is not readiness. Do not fake an in-repo component to unblock its consumer; implement/install it and exercise its real contract. A permitted external/nondeterministic substitute must retain the real in-repo adapter. Dependency readiness is separate from final E2E; do not turn it into a whole-product browser run. Avoid undeclared ad-hoc installs during execution.

## Scope and File Structure

Split genuinely independent projects when needed, but keep the smallest user loop coherent and do not broaden architecture/governance/platform support speculatively. Map files and owners before tasks: prefer focused files, existing patterns and real interface boundaries; co-locate responsibilities that change together.

## Task Right-Sizing

A task carries its own focused test cycle and independently testable deliverable. Fold setup/configuration/documentation into the deliverable that needs it. Task boundaries must not leave final integration reconstructing a journey from incompatible assumptions. Ordinary task progress needs a focused result, not a separate review/evidence package or repeated E2E.

## Plan Document Header

Use relevant review blocks below once, or reference an already-valid owner. Do not mechanically duplicate all fields when a short applicable delta or `NOT_APPLICABLE` with reason is sufficient.

```markdown
## Product Value Validation
**Applicability:** REQUIRED | NOT_APPLICABLE
**Target user / triggering situation:** ...
**Job-to-be-done:** ...
**Current workaround / cost:** ...
**Evidence provenance / level:** OBSERVED | INFERRED | ASSUMED; E0–E5
**Value proposition / hypothesis:** ...
**Start / Aha event / target time-to-Aha / pre-Aha friction:** ...
**Positive evidence / counter-evidence:** ...
**Minimum validation / PMF signal / claim boundary:** ...
**Disposition:** READY_TO_PLAN | VALIDATE_FIRST | NOT_APPLICABLE

## Architecture Delta Review
**Applicability:** REQUIRED | NOT_APPLICABLE
**Intent / evidence basis / observed architecture:** ...
**Required properties / verified delta / scope fence:** ...
**Closing evidence:** ...
**Disposition:** PROCEED_WITH_DELTA | NO_CHANGE_REQUIRED | INVESTIGATE_UNKNOWN | REFRESH_CONTEXT | REDUCE_SCOPE | NOT_APPLICABLE

## IA-Before-UI Review
**Applicability:** REQUIRED | NOT_APPLICABLE
**User task / JTBD:** ...
**Cognitive-work allocation:** ...
**Primary domain objects / canonical semantic owners:** ...
**Task flow / proposed region hierarchy:** ...
**Design-source mapping:** exact current design sections, template/showcase paths and shared primitives
**Fast-to-Aha / task-effort check:** ...
**States/recovery ownership / responsive constraints:** ...
**Verification evidence / stop conditions / blocking findings:** ...
**Disposition:** GO_FOR_UI | REVISE_IA | NOT_APPLICABLE

## Verification Impact Analysis
**Source / changed surfaces / direct consumers / affected boundaries:** ...
**User paths at risk / uncertainty / radius R0–R3:** ...
**Focused tests during implementation:** ...
**Final campaign after implementation readiness:** journey, candidate, required targets/order, bounded runner, existing result location
**Omitted broad suites:** only material omissions and reasons
```

Architecture-changing tasks require a verified nonempty delta and `PROCEED_WITH_DELTA`; `NO_CHANGE_REQUIRED` stops architecture change, `INVESTIGATE_UNKNOWN` gathers evidence, `REFRESH_CONTEXT` reconstructs current state and `REDUCE_SCOPE` narrows the candidate. Material UI work requires `GO_FOR_UI`. VIA still selects test scope for non-UI/non-architecture work. These dispositions are not extra human approvals.

## Self-Review

Check spec/MVL continuity, applicable value/architecture/IA dispositions, real dependency readiness, VIA and integration credibility, concrete tasks without unresolved placeholders, explicit stopping criterion and authority. Confirm intermediate gates cannot close the goal, user-intervention gates satisfy the necessity test, and final E2E is consolidated after implementation readiness with bounded output and delta-only reruns. Preserve the host goal as the outer objective. Missing required reviews or unsupported dispositions mean the plan needs repair, not additional ceremonial reporting.

## Execution Handoff

Preserve current user requirements, confirmed changes, constraints, consequential rationale and acceptance via precise existing sources. Keep assumptions distinct from accepted decisions; fill missing information rather than copying conversations or creating another ledger.

For concurrent implementation agents or competing implementations, apply [Parallel implementation and candidate authorization](../executing-plans/SKILL.md#parallel-implementation-and-candidate-authorization). Keep counts, comparison criteria, cost basis, budget/stopping limits and actual approval reference in the existing plan. Default to one implementation path; a plan cannot authorize its own parallel strategy.

After saving, continue with the already-authorized execution approach. Autonomous gates advance automatically; ask only when the User Intervention Necessity Test is met.
