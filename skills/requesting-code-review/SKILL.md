---
name: requesting-code-review
description: Use when an architectural or high-risk change needs deliberate review, when a fresh perspective is useful, or when review is explicitly requested
---

# Requesting Code Review

Review is a risk-control mechanism, not a completion ceremony. Use the lightest review that addresses the actual failure risk, and do not repeat review of unchanged work.

## Review Levels

### Ordinary Change

Examples: local bug fix with a clear reproducer, copy or styling change, small isolated helper, behavior-preserving refactor with adequate coverage.

Required:
- run the affected verification
- inspect the diff once for unintended scope, accidental files, and obvious regressions

Do not dispatch a separate reviewer merely because the task is complete or ready to merge.

### Architectural Change

Examples: new service boundary, persistence-shape change, new runtime abstraction, dependency replacement, multi-component wiring change.

Required:
- review once at the coherent integration boundary
- check interfaces, ownership, coupling, data flow, dependency decisions, and the assembled production path against the plan/spec
- confirm the integration verification covers the architecture actually introduced

A structured self-review is sufficient when the change is understandable in current context. Dispatch a fresh reviewer when context separation materially improves judgment or the plan explicitly selected a reviewer.

### High-Risk Change

Examples: authentication/authorization, security-sensitive code, destructive migration, financial calculation, irreversible external action, production deployment logic, or changes whose failure could corrupt or lose data.

Required before completion:
- identify the dangerous failure mode explicitly
- run the focused negative control, regression, or real integration path that would expose it
- inspect rollback, recovery, or containment implications where relevant
- perform a deliberate fresh-context review when judgment risk is material; a reviewer subagent is useful here because it provides independent context, not organizational authority

A small diff can be high-risk. A large isolated change can be ordinary. These review categories are independent of the R0–R3 test-impact radius.

## If Dispatching a Reviewer

Use a reviewer only when it adds a distinct check rather than duplicating verification already performed.

**1. Get the review-unit SHAs:**

```bash
BASE_SHA=<recorded-entry-commit-for-the-review-unit>
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch one reviewer:**

Use the template at [code-reviewer.md](code-reviewer.md) with:
- `{DESCRIPTION}` — what changed and why
- `{PLAN_OR_REQUIREMENTS}` — binding requirement/spec
- `{BASE_SHA}` — start of the coherent review unit
- `{HEAD_SHA}` — end of the coherent review unit

Do not send the reviewer the session history. Give it the diff plus the requirements and concrete risks that justify the review.

**3. Act on findings:**
- required correctness or security defects block completion
- optional polish does not become a mandatory loop
- push back on an incorrect finding with code, tests, or contract evidence
- re-review only the changed fix surface unless a fix invalidates broader assumptions

## Operating Rule

> Review only when the cost of a plausible mistake is meaningfully higher than the cost of reviewing it.

Do not create a review artifact when there are no findings that need to survive the current session. Git and the verification results already record ordinary development state.
