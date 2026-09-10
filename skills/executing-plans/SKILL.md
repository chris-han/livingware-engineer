---
name: executing-plans
description: Use when you have a written implementation plan to execute continuously through its authorized stopping criterion, involving the user only when judgment is genuinely necessary
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks, preserve the feature's MVL contract across task boundaries, and report the actual evidence state when complete.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

Honor the already authorized execution mode. Use subagent-driven-development when delegation is selected and useful; tool availability alone does not override an inline execution choice.

**Continuous execution:** A verified task, sprint exit, review, integration slice, or list of remaining gates is progress evidence, not a stop condition. Record or reuse the evidence and immediately execute the next dependency-ready item. Continue until the plan's stopping criterion is satisfied or the Human Judgment Necessity Test below is met.

## Human Judgment Necessity Test

Apply standing user delegation first. Do not ask the user to re-approve ordinary technical choices, phase transitions, review outcomes, implementation gates, refactors, test runs, browser checks, or other in-scope engineering work they have already delegated.

Stop for human judgment only when all three are true:
1. a real decision is required before the next action can proceed;
2. the decision is not already delegated and cannot be resolved from the binding spec/policy, observed evidence, established conventions, executable checks, or a safe reversible default; and
3. choosing wrong has a material, not-cheaply-reversible consequence, such as genuinely subjective product intent, a non-delegable legal/compliance determination, sensitive-data disclosure, irreversible/destructive action, or consequential external/production state change.

Before asking, state the exact decision, viable options, material consequence, and why delegation plus evidence or reversibility cannot resolve it. Otherwise make the smallest reversible in-scope ruling and continue. Remaining work, remaining gates, a completed checkpoint/review, or ordinary technical uncertainty never satisfy this test by themselves.

## MVL Continuity Rule

For product features, the plan's **MVL Contract is binding across the whole execution**. It is not a task-specific note and must not be silently narrowed or reinterpreted while implementing individual components.

Before coding, identify from the plan:

- target user / job-to-be-done
- value hypothesis
- smallest real user journey
- realistic trial inputs
- technical and UX metrics
- feedback/telemetry surface
- improvement levers
- re-test surface and stopping criterion
- Prerequisites and Dependencies: required packages/tools/services, exact install/setup, compatibility assumptions, dependency verification
- Impact Radius and Integration Contract: real components, permitted substitutes, forbidden mocks, UI/browser requirement

Every task should advance that same loop. Local task success is not permission to mark the feature complete.

## Dependency Readiness Rule

A downstream feature task may not rely on a new package, service, runtime, database, CLI, plugin, browser, system library, or other prerequisite until the plan's dependency gate is satisfied.

For each new load-bearing dependency:

1. verify the dependency is explicitly declared in the plan
2. add/pin it in the repository-owned manifest or setup surface
3. install/sync it using the exact planned command
4. run the planned smoke/contract test against the real dependency or real in-repo adapter
5. run any baseline tests affected by the dependency change
6. only then execute feature code that consumes it

Do not install undeclared dependencies ad hoc just because an implementation task needs them. If a dependency is discovered mid-execution, update the plan/prerequisite contract first (or record a ruling consistent with the spec when your execution mode permits), then install and verify it before proceeding.

A successful package install is not proof of readiness. The dependency gate is green only when the minimal real API/behavior the feature relies on has been exercised successfully.

## The Process

### Step 1: Load and Review Plan
1. Use superpowers:using-git-worktrees to choose in-place or isolated work; preserve an adequate existing workspace.
2. Read the plan file and its linked spec.
3. Reference the plan's MVL, dependency, impact, and integration sections from the existing recovery tracker; do not copy them into another ledger.
4. Review critically for gaps or contradictions.
5. Confirm the smallest real journey is actually implementable by the listed tasks.
6. Confirm every load-bearing external or package prerequisite has an explicit declaration/install/verification path before any consumer task.
7. If the plan has a critical gap, first resolve it from standing delegation, the binding spec, repository evidence, established conventions, or the smallest reversible ruling. Ask the human partner only if the Human Judgment Necessity Test is met. Otherwise, create todos and proceed.

### Step 2: Execute Prerequisites

Before feature consumers run, execute every prerequisite/dependency task in dependency order.

For each dependency prerequisite:
1. declare/pin it in the correct manifest/configuration surface
2. install/sync the environment
3. run the dependency smoke/contract test
4. verify the expected real capability exists
5. run the relevant existing baseline tests
6. record the exact version/pin and evidence

If the dependency itself is an in-repo production component or local service, use its real implementation. Do not fake it to get past the prerequisite gate.

If the dependency is genuinely external or nondeterministic, keep the in-repo adapter/client real and substitute only the remote side when the plan explicitly permits that.

### Step 3: Execute Feature Tasks

For each feature task:
1. Mark as in_progress.
2. Confirm its declared prerequisite tasks are green.
3. Follow each step exactly.
4. Use TDD for changed behavior.
5. Run focused step tests and the plan's sprint-exit integration/review gates. Use `verification-before-completion` for scope and unchanged-state result reuse.
6. Check that the task's output still matches the shared MVL journey and interfaces; do not invent a local alternate flow just to make tests pass.
7. Do not add a new dependency without first adding/updating its prerequisite contract and verification.
8. Mark as completed only when its implementation and required evidence are complete.

### Step 4: Prove the Integrated MVL Journey

After component tasks are green, do **not** jump directly to branch completion for product features.

Run the plan's closure evidence in this order as applicable:

1. **Dependency verification** — confirm all load-bearing packages/services/tools remain installed, pinned, and smoke/contract-tested.
2. **Focused or real-component integration** — according to the plan's R0–R3 impact radius, exercise the affected production path through the required real in-repo components. Internal completion-path mocks are forbidden.
3. **Real-browser UI verification** — follow the [browser selection and lifecycle contract](../test-driven-development/remote-cdp-browser-lifecycle.md). Only an unavailable browser required by the selected evidence lane blocks that gate; Chrome availability does not block Lightpanda behavior verification.
4. **Vertical/E2E verification** — when R3 impact or the user-value claim crosses multiple architecture boundaries.
5. **Baseline / technical + UX measurement** — run the declared stable evaluation surface with realistic trial inputs.
6. **Feedback capture verification** — prove telemetry, corrections, or explicit feedback are actually captured where the plan requires them.
7. **Improvement + comparable re-test** — when the plan's stopping criterion requires closing a full learning iteration, make the evidence-driven change and rerun the same evaluation surface.

Keep these distinctions explicit:

```text
Task complete           = local deliverable + local evidence
Dependency ready        = declared/pinned + installed + required API smoke-tested
Implementation complete = dependency readiness + TDD + required integration + browser/E2E where applicable
MVL complete            = implementation credibility + measurement + feedback + required improvement + comparable re-test
```

### Step 5: Complete Development

After all required implementation and MVL closure evidence is satisfied according to the plan's stopping criterion:
- invoke `verification-before-completion` and verify every claimed gate with fresh evidence
- then announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use superpowers:finishing-a-development-branch
- Follow that skill to verify tests, present options, and execute the chosen branch action.

## When to Stop and Ask for Help

Stop for the human only when the Human Judgment Necessity Test is met. Missing dependencies, failed tests, unavailable browser/service fixtures, review findings, or incomplete gates are engineering work: debug, install/start what is authorized, repair, choose a reversible fallback where permitted, or continue independent work. They are not human-approval conditions by themselves.

For ordinary implementation ambiguity, make a documented reversible ruling consistent with the spec and MVL Contract and keep going.

## When to Revisit Earlier Steps

Return to plan review when:
- the partner updates the plan/spec
- a new dependency is discovered or an existing dependency version/contract must change
- the value hypothesis or smallest real journey materially changes
- integration evidence proves the planned architecture cannot deliver the journey
- measurement/feedback shows the current iteration needs an explicit plan adjustment before the re-test

A changed MVL contract or load-bearing dependency contract is a plan/spec change, not a local implementation tweak.

## Remember
- Review plan critically first
- Preserve one MVL contract from planning through integration and re-test
- Make dependencies explicit before consumers rely on them
- Install and smoke/contract-test new dependencies before feature implementation
- Follow task steps exactly
- Don't skip verifications
- Internal mocks cannot prove the architecture exists
- Frontend work requires real-browser evidence
- Integration/E2E completion is not automatically MVL completion
- Evidence before claims
- Never start implementation on main/master without explicit user consent
