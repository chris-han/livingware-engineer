---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

## MVL Law 1 — Fast-to-Aha

For product MVLs where governance is in the path, treat time-to-first-useful-result as an acceptance criterion. Distinguish recorded default-pass gates from blocking gates; ordinary low-risk journeys must not stop for approval ceremony. A user-intervention gate is allowed only when the User Intervention Necessity Test in `docs/mvl-laws.md` is satisfied after applying any standing user delegation.

Classify every planned gate as either **autonomous** or **user-intervention-required**. Autonomous gates include tests, typecheck, lint, build, contract checks, service/browser fixtures, integration/E2E evidence, deterministic review findings, and ordinary reversible engineering rulings; they advance automatically when satisfied and never require a human checkpoint. A user-intervention-required gate is allowed only when standing delegation plus the User Intervention Necessity Test says the next required action genuinely depends on user-owned judgment, authority, access, credentials, or consequential external action. Do not create approval or checkpoint tasks merely to mark a phase boundary.

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Keep useful step-by-step detail; eliminate duplicated work, not implementation steps. Reference existing specifications, interfaces, fixtures, and shared procedures by exact path and symbol/section. Include inline code when it resolves a real ambiguity, rather than copying an existing implementation or contract into each task.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** If working in an isolated worktree, it should have been created via the `superpowers:using-git-worktrees` skill at execution time.

**Save plans to:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
- (User preferences for plan location override this default)

## Execution Continuity Contract

Every executable multi-step plan MUST declare near the top an **authorized stopping criterion** and any **permitted terminal dispositions**. The plan is a completion contract, not merely an ordered checklist.

Unless explicitly declared otherwise, intermediate tasks, gates, reviews, test/browser/integration passes, commits, and workstream completion are non-terminal progress evidence. After every non-terminal observation, advance to the next dependency-ready obligation. Recoverable failures route to debugging, repair, retry, bounded replanning, or verification rather than back to the user. Concise progress updates are non-blocking and do not wait for acknowledgment. A declared negative or inconclusive outcome may be terminal when its predeclared predicate is satisfied. User involvement is permitted only when the User Intervention Necessity Test is satisfied.

If the authorized scope is intentionally bounded, state it explicitly—for example, “stop after W1 evidence is sealed.” Otherwise an intermediate GREEN MUST NOT be interpreted as plan completion.

When the host provides a persistent objective or goal primitive, keep it as the outer objective. The plan supplies its executable completion contract; it must not create a competing goal authority or mark the host objective complete from an intermediate gate.

## Architecture Delta Before Architecture Work

For a plan that introduces or changes a subsystem, service, store, contract, interface, ownership boundary, cross-component data flow, runtime responsibility, or structural architecture, apply `docs/architecture-delta-principle.md` before creating implementation tasks. Carry forward the design's current-state evidence and Architecture Delta Review rather than re-inventing the architecture from the spec title.

The plan may contain architecture-changing tasks only when the review disposition is `PROCEED_WITH_DELTA`. `UNKNOWN` is an investigation state, not a missing-capability claim; `NO_CHANGE_REQUIRED` is terminal and the plan must not manufacture implementation tasks. Every architecture-changing task must trace to at least one verified delta item, remain inside the declared scope fence, and name the evidence that will close that delta.

This is a machine-verifiable structural gate, not a default human-approval checkpoint. For work with no architecture effect, record `NOT_APPLICABLE` briefly and continue.

## MVL Is the Feature-Development Unit

For product features, plan a **Minimum Viable Loop (MVL)**, not merely an implementation slice.

**MVL is the feature-development unit, not a test unit.** Unit tests, integration tests, browser tests, and E2E tests are verification evidence inside the implementation of an MVL.

The same feature contract must survive every later phase:

```text
Target user + job + value hypothesis
  -> smallest real user journey
  -> realistic trial inputs
  -> prerequisites / dependencies
  -> Architecture Delta when architecture-affecting
  -> IA-before-UI when material user-facing structure changes
  -> implementation
  -> TDD
  -> Verification Impact Analysis
  -> real-component integration when impact radius requires it
  -> real-browser UI verification when applicable
  -> technical + UX measurement
  -> feedback / diagnosis
  -> improvement
  -> comparable re-test
```

Do not create a plan whose terminal state is only "code complete" or "tests pass" when the work is a product feature. Implementation correctness is necessary evidence inside the MVL; it is not the feature-development unit itself.

Every feature plan MUST define, near the top:

- **Target user / job-to-be-done**
- **Value hypothesis** — what useful change this feature is expected to create
- **Smallest real user journey** — the narrowest end-to-end path that demonstrates that value
- **Realistic trial inputs**
- **Technical success metrics**
- **UX success metrics**
- **Feedback / telemetry capture**
- **Improvement levers** — code, model, prompt, rules, data, knowledge, UI, workflow, thresholds, configuration, architecture
- **Re-evaluation method** — same surface used before and after improvement
- **Stopping criterion for this MVL iteration**

These are not a separate skill or optional appendix. They are part of the plan contract and constrain task design, dependency readiness, test design, integration scope, and completion evidence.

### Product Value Validation

For product features whose justification depends on user value, adoption, activation, retention, workflow insertion, or market pull, apply the Product Value Validation contract in `references/product-value-validation.md` before implementation tasks are admitted.

The review must distinguish:

- **problem evidence** from an internal assumption;
- **value proposition** from implementation description;
- **Aha** from onboarding or technical completion;
- **behavioral/economic evidence** from stated preference;
- **feature success** from product-market fit.

Record the strongest supported value-evidence level (`E0` through `E5`), a falsifiable value hypothesis, the first observable Aha event and time-to-Aha target when meaningful, counter-evidence that would weaken the hypothesis, and the product-level PMF signal the feature may contribute to without claiming that the feature itself establishes PMF.

Use `READY_TO_PLAN`, `VALIDATE_FIRST`, or `NOT_APPLICABLE`. `VALIDATE_FIRST` changes the plan target to the smallest useful validation experiment; it is not a human-approval checkpoint. For verified defects, behavior-preserving refactors, dependency/platform maintenance, mandatory security/legal/contractual work, architecture-integrity work, or technical qualification with no user-value claim, record `NOT_APPLICABLE` with the authoritative requirement source or reason rather than inventing a value proposition.

For non-product maintenance work where no user-learning loop exists, state `MVL: not applicable — <reason>` rather than inventing one.

## IA Before UI

Before production UI implementation, determine whether the work introduces or materially changes user-facing information architecture. If it does, apply `docs/ia-before-ui.md` and record an `IA-Before-UI Review` before implementation tasks begin.

The review must establish the user task/domain model, canonical semantic owners, region hierarchy, Fast-to-Aha path, state/recovery ownership, action semantics, responsive constraints, shared-pattern reuse, and planned verification evidence. Its disposition is `GO_FOR_UI` only when all stop conditions are clear; unresolved duplicated semantic ownership, implementation-model leakage, ambiguous action semantics, missing state ownership, or responsive ambiguity yields `REVISE_IA` and blocks production UI implementation until the IA is repaired.

This is a machine-verifiable structural engineering gate, not a default human-approval checkpoint. Pure visual-token fixes, renderer-performance work, implementation-only refactors, and accessibility corrections with no IA change may record `NOT_APPLICABLE` with a brief reason.

## Impact Radius Before Test Scope

Verification Impact Analysis (VIA) chooses the smallest verification surface capable of falsifying the implementation claim. Do **not** choose integration/E2E scope from diff size or intuition alone.

Use relationship-aware discovery when it materially improves the impact assessment. Prefer an available current code graph; check coverage and fall back to targeted source for gaps. Do not make whole-repository indexing a prerequisite for a bounded change. Useful graph tools include:

- `search_graph`
- `trace_path`
- `query_graph`
- `search_code`
- `get_code_snippet`

Assess the changed production surface for callers, callees, downstream consumers, DI/factory wiring, routes, persistence/schema edges, async/event boundaries, trust boundaries, frontend consumers, and user paths.

Classify the observed radius:

```text
R0 local only        -> focused TDD / unit-level behavior test
R1 one seam          -> focused integration across that seam
R2 multi-component   -> real-component integration through affected path
R3 user/cross-boundary/UI -> vertical/E2E + real-browser verification for UI
```

Use the **smallest sufficient verification scope**. Do not wake the full integration/E2E stack for a small local change whose graph impact is R0.

Preserve the verification cadence distinction:

- D0 deterministic invariants — cheap mechanical checks on every relevant mutation;
- D1 local semantic sentinels — focused behavior/integration selected from current impact radius;
- D2 broad semantic audits — broad or expensive suites for release, high-risk, periodic, or genuinely broad/uncertain changes.

Read `docs/verification-impact-analysis-v1.md` and `../test-driven-development/impact-radius-testing.md` for the detailed policy.

## Dependency and Prerequisite Contract

A new feature may rely on a package, service, runtime, browser, database, CLI, model, plugin, system library, or other prerequisite that does not yet exist in the project. **The plan must make that dependency explicit before feature code depends on it.**

Do not let implementation agents discover and install dependencies ad hoc in the middle of a task.

For every new or materially changed dependency, the plan must record:

- exact package/tool/service name
- exact version, compatible range, commit, image tag, or other pin when practical
- why it is needed for this MVL journey
- where it will be declared (`pyproject.toml`, `package.json`, lockfile, Docker image, system setup, plugin manifest, etc.)
- exact install/setup command
- required configuration/environment variables without embedding secrets
- compatibility constraints with the existing stack
- whether it changes runtime, build, test, deployment, licensing, security, or platform assumptions
- a **dependency smoke/contract test** proving the real dependency is usable before feature code relies on it
- cleanup/removal steps if an obsolete dependency is being replaced

Dependency readiness is a prerequisite gate:

```text
select dependency
  -> declare/pin it
  -> install it
  -> prove it loads/connects/executes
  -> prove the minimum API/behavior the feature relies on
  -> only then build feature code on top of it
```

A package merely appearing in a manifest or lockfile is **not** sufficient evidence. The plan must specify an executable check appropriate to the dependency.

If the dependency itself is an in-repo production component or local service, do not fake it merely to unblock development. Install or implement the prerequisite first, then verify it with the real implementation.

If a dependency is genuinely external or nondeterministic, a local/sandbox substitute may stand in for the remote side, but the in-repo adapter/client must remain real where practical.

**Dependency test scope is separate from feature integration scope.** A new dependency always needs enough smoke/contract evidence to prove it is usable, while broader integration/E2E still follows the R0–R3 impact-radius decision.

## Scope Check

If the spec covers multiple independent subsystems, it should have been broken into sub-project specs during brainstorming. If it wasn't, suggest breaking this into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

For a product feature, prefer the smallest loop that can generate reliable learning. Do not broaden architecture, governance, ontology, edge-case coverage, or generalized platform support beyond what is required to make the smallest real journey credible and learnable.

## File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns.

## Task Right-Sizing

A task is the smallest implementation unit that carries its own focused test cycle and an independently testable deliverable. Fold setup, configuration, scaffolding, and documentation into the task whose deliverable needs them. Group related tasks for integrated sprint review; use an earlier task review when its risk or an explicit repository requirement warrants it. Small implementation steps are not separate review gates.

Task boundaries MUST preserve the MVL journey. Do not decompose the work in a way that leaves the final integration task reconstructing a user path from mutually inconsistent local assumptions.

## Plan Document Header

Every plan must include the relevant review blocks before implementation tasks:

```markdown
## Product Value Validation

**Applicability:** REQUIRED | NOT_APPLICABLE
**Target user / triggering situation:** ...
**Job-to-be-done:** ...
**Current workaround / cost:** ...
**Evidence provenance:** OBSERVED | INFERRED | ASSUMED | ...
**Evidence level:** E0 | E1 | E2 | E3 | E4 | E5
**Value proposition:** ...
**Start event:** ...
**Aha event:** ...
**Target time-to-Aha:** ...
**Pre-Aha friction:** ...
**Hypothesis:** ...
**Positive evidence:** ...
**Counter-evidence / falsifier:** ...
**Minimum validation surface:** ...
**PMF-relevant signal:** ...
**Claim boundary:** ...
**Disposition:** READY_TO_PLAN | VALIDATE_FIRST | NOT_APPLICABLE

## Architecture Delta Review

**Applicability:** REQUIRED | NOT_APPLICABLE
**Intent:** ...
**Evidence basis:** ...
**Observed architecture:** ...
**Required properties:** ...
**Verified delta:** ...
**Scope fence / does not change:** ...
**Closing evidence:** ...
**Disposition:** PROCEED_WITH_DELTA | NO_CHANGE_REQUIRED | INVESTIGATE_UNKNOWN | REFRESH_CONTEXT | REDUCE_SCOPE | NOT_APPLICABLE

## IA-Before-UI Review

**Applicability:** REQUIRED | NOT_APPLICABLE
**User task:** ...
**Primary domain objects:** ...
**Canonical semantic owners:** ...
**Proposed region hierarchy:** ...
**Fast-to-Aha path:** ...
**States/recovery ownership:** ...
**Responsive constraints:** ...
**Verification evidence:** ...
**Stop conditions checked:** PASS | BLOCKED
**Blocking findings:** none | ...
**Disposition:** GO_FOR_UI | REVISE_IA | NOT_APPLICABLE

## Verification Impact Analysis

**Source:** codebase-memory-mcp | equivalent | manual fallback
**Changed surfaces:** ...
**Direct consumers:** ...
**Affected boundaries:** ...
**User paths at risk:** ...
**Uncertainty:** low | medium | high
**Radius:** R0 | R1 | R2 | R3
**Selected tests:** ...
**Omitted broad suites:** ...
```

For architecture-affecting work, only `PROCEED_WITH_DELTA` may precede implementation tasks; `NO_CHANGE_REQUIRED` is terminal, `INVESTIGATE_UNKNOWN` requires evidence gathering, `REFRESH_CONTEXT` requires current-state reconstruction, and `REDUCE_SCOPE` requires a smaller candidate change. For non-architecture work, Architecture Delta may be `NOT_APPLICABLE`. For non-UI work, IA may be `NOT_APPLICABLE`, but VIA still selects test scope. For material UI work, `GO_FOR_UI` must precede implementation. These are machine-verifiable structural dispositions and do not imply human approval ceremony.

## Self-Review

After writing the plan, check:

1. Spec coverage.
2. MVL continuity.
3. Product Value Validation applicability, evidence level, Aha contract, falsifier, PMF claim boundary, and disposition.
4. Dependency readiness.
5. Architecture Delta applicability, evidence, minimality, and disposition.
6. IA-before-UI applicability and disposition.
7. Verification Impact Analysis and R0–R3 scope.
8. Integration credibility.
9. Placeholder scan.
10. Type consistency.
11. Authorized stopping criterion and permitted terminal dispositions are explicit.
12. Intermediate gates cannot be mistaken for terminal states.
13. Any user-intervention gate satisfies the User Intervention Necessity Test.
14. A host persistent goal/objective, when present, remains the outer objective.

If required Product Value Validation is missing or has unresolved material value uncertainty while claiming `READY_TO_PLAN`, if architecture-affecting work lacks a verified non-empty delta, if a material UI change lacks an IA review, or if VIA is missing/unsupported, the plan is incomplete.

## Execution Handoff

After saving the plan, continue with the execution approach already authorized by the user. Autonomous gates advance automatically; involve the user only when the User Intervention Necessity Test is met.
