---
name: executing-plans
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks, preserve the feature's MVL contract across task boundaries, and report the actual evidence state when complete.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

**Note:** Tell your human partner that Livingware Engineer works much better with access to subagents. If subagents are available, use superpowers:subagent-driven-development instead of this skill.

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
- Integration Contract: real components, permitted substitutes, forbidden mocks, UI/browser requirement

Every task should advance that same loop. Local task success is not permission to mark the feature complete.

## The Process

### Step 1: Load and Review Plan
1. Ensure an isolated workspace: use superpowers:using-git-worktrees to create one or verify the existing one.
2. Read the plan file and its linked spec.
3. For a product feature, extract the MVL Contract and Integration Contract into the execution todo/ledger so they survive context changes.
4. Review critically for gaps or contradictions.
5. Confirm the smallest real journey is actually implementable by the listed tasks and that required production dependencies exist.
6. If the plan has a critical gap that makes the intended journey unknowable, raise it with the human partner before starting. Otherwise, create todos and proceed.

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress.
2. Follow each step exactly.
3. Use TDD for changed behavior.
4. Run the task verifications as specified.
5. Check that the task's output still matches the shared MVL journey and interfaces; do not invent a local alternate flow just to make tests pass.
6. Mark as completed only when its implementation and required evidence are complete.

### Step 3: Prove the Integrated MVL Journey

After component tasks are green, do **not** jump directly to branch completion for product features.

Run the plan's closure evidence in this order as applicable:

1. **Real-component integration** — exercise the smallest real journey through the changed/relied-upon production components. Internal completion-path mocks are forbidden.
2. **Real-browser UI verification** — mandatory for frontend/UI work. Prefer the configured Chrome CDP endpoint, commonly `127.0.0.1:9222`. In WSL, if that browser prerequisite is unavailable, tell the user how to start host Chrome in debug mode and keep UI completion blocked until real-browser evidence exists.
3. **Vertical/E2E verification** — when the user-value claim crosses multiple architecture boundaries.
4. **Baseline / technical + UX measurement** — run the declared stable evaluation surface with realistic trial inputs.
5. **Feedback capture verification** — prove telemetry, corrections, or explicit feedback are actually captured where the plan requires them.
6. **Improvement + comparable re-test** — when the plan's stopping criterion requires closing a full learning iteration, make the evidence-driven change and rerun the same evaluation surface.

Keep these distinctions explicit:

```text
Task complete          = local deliverable + local evidence
Implementation complete = TDD + real integration + browser/E2E where applicable
MVL complete           = implementation credibility + measurement + feedback + required improvement + comparable re-test
```

### Step 4: Complete Development

After all required implementation and MVL closure evidence is satisfied according to the plan's stopping criterion:
- invoke `verification-before-completion` and verify every claimed gate with fresh evidence
- then announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use superpowers:finishing-a-development-branch
- Follow that skill to verify tests, present options, and execute the chosen branch action.

## When to Stop and Ask for Help

**STOP executing immediately when:**
- an irreversible/destructive or security-sensitive action needs approval
- a required production dependency is missing and cannot be installed/implemented within the plan
- the plan/spec is so contradictory that every path forward would redefine the user journey
- required WSL host-browser verification is blocked because Chrome debug mode is not running; provide startup instructions and wait for that prerequisite before claiming UI completion

For ordinary implementation ambiguity, prefer a documented ruling consistent with the spec and MVL Contract rather than fragmenting the feature into local guesses.

## When to Revisit Earlier Steps

Return to plan review when:
- the partner updates the plan/spec
- the value hypothesis or smallest real journey materially changes
- integration evidence proves the planned architecture cannot deliver the journey
- measurement/feedback shows the current iteration needs an explicit plan adjustment before the re-test

A changed MVL contract is a plan/spec change, not a local implementation tweak.

## Remember
- Review plan critically first
- Preserve one MVL contract from planning through integration and re-test
- Follow task steps exactly
- Don't skip verifications
- Internal mocks cannot prove the architecture exists
- Frontend work requires real-browser evidence
- Integration/E2E completion is not automatically MVL completion
- Evidence before claims
- Never start implementation on main/master without explicit user consent
