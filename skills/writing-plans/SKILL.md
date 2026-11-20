---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans — Minimal Executable Contract

**Enter:** accepted requirements/design require a genuine multi-step implementation plan. **Do not activate for an already specified bounded reversible fix, routine debugging, or a completion claim.** Design judgment belongs to `brainstorming` before planning; active implementation belongs to `executing-plans` afterward; verify only on the actual completion boundary.

## Purpose and authority

Write the smallest plan that names affected owners/files, dependencies, current behavior, necessary delta, tests, user-visible goal and exact **authorized stopping criterion**. Record permitted **terminal dispositions** near the top. The plan is a completion contract; a task PASS, sprint, test or code commit is non-terminal unless its declared outcome is actually met.

Preserve one mutable plan in the repository's declared authoritative checkout/location (default `docs/superpowers/plans/YYYY-MM-DD-<feature>.md` only if no project policy specifies otherwise). Execution/worktrees are separate. Reuse existing requirements/specifications and source evidence by reference, not by copying chat, logs, whole tests or a second task ledger.

## Plan minimal frontier

- **What is known:** current owner and real call path; checked source, usable fixtures, already qualified evidence and exact claim limitations.
- **What changes:** smallest source/contract delta and applicable implementation/testing owner; name any real integration and changed downstream caller.
- **What unlocks expansion:** a demonstrated error, changed contract, unknown owner, protected boundary or material risk. No speculative repo-wide search, new infrastructure or hypothetical test campaign.
- **Which surface:** distinguish user-visible frontend/product and delivery phase from implementation host, browser and platform-specific acceptance. Never imply a Windows/native capability from a web-only test or file format.
- **Requirements:** preserve effective accepted requirements and constraints; when materially unclear use [requirements workflow](../requirements-clarification/references/requirements-workflow.md), not an automatic elicitation round.

## Applicable engineering checks

### MVL and user value

For real product features, define the smallest user task, target user and first useful result, value hypothesis, eligible evidence, feedback/recovery, and a bounded outcome claim. Low-risk exploration stays Fast-to-Aha/default-pass. Maintenance/security/internal deterministic fixes may record `MVL: NOT_APPLICABLE` without inventing business evidence. Only value/market-pull claims need [product value validation](references/product-value-validation.md), if that reference is actually present and applicable.

### Architecture and UI

For a material architecture/cross-owner/storage change, apply `docs/architecture-delta-principle.md` and bind the verified delta to tasks. UNKNOWN is an investigation, not proof of missing architecture; `NO_CHANGE_REQUIRED` never creates implementation scope. For material UI task-flow/IA work, follow `docs/ia-before-ui.md` and `frontend-design`; record `GO_FOR_UI | REVISE_IA | NOT_APPLICABLE` in the plan, reusing existing IA for unchanged paths. Do not preload the UI craft tool merely because the plan mentions a UI stage.

### Verification Impact Analysis

Choose tests by the actual changed production impact radius (R0–R3), not diff size. Focused behavior/component checks run during implementation. Required real-component and browser verification runs at the goal/integration boundary, normally as **one consolidated E2E campaign** on the integrated candidate; rerun only failed/invalidated paths. Retain security/authority and actual final-acceptance requirements. Link [Verification Impact Analysis](../../docs/verification-impact-analysis-v1.md) only for unresolved scope; do not create per-PASS receipts or parallel coverage matrices.

### Preconditions, risky transitions and cost

A genuinely new dependency must be named/pinned and its minimum real behavior proven before consumer code relies on it; do not build a fake in-repo replacement. For cross-owner/high-risk, asynchronous, native-lifecycle, tenant/identity, or irreversible changes, do one bounded [pre-execution failure review](references/pre-execution-failure-review.md); skip for routine local edits. Autonomous tests, reversible decisions and ordinary repair are not user-approval gates. Parallel competing implementations need the explicit [authorization boundary](../executing-plans/SKILL.md#parallel-implementation-and-candidate-authorization).

## Plan output and handoff

Tasks should be independently testable, preserve source/owner and relevant dependencies, and converge on the real user outcome. Reuse an existing plan/review block; add only applicable scope, risk, architecture, IA and acceptance deltas. Do not mechanically fill template sections or write a standalone plan for each micro-step. For detailed template options, scope decomposition and exceptional requirements, read [planning reference](references/detailed-plan-workflow.md) only when actually needed.

**At the planning exit:** save the one authoritative plan, freeze current owner/requirements/evidence references, the integration target, target surface, stop/disposition conditions and execution authorization. Then leave this skill and invoke `executing-plans` only when actual implementation begins. Do not load final verification or branch retirement before that state.
