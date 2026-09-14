---
name: systematic-debugging
description: Use while an unexplained bug, test failure, regression, performance anomaly, or unexpected behavior requires root-cause investigation
---

# Systematic Debugging

## Lifecycle

Entry: an observed failure is still unexplained.
Exit: root cause and affected behavior are sufficiently established, or diagnosis-only work is complete.
After exit, stop carrying this workflow forward. Implementation may match TDD; a completion claim may match verification. Re-enter only when new evidence makes the failure unexplained again.

## Core Contract

Do not fix before you have evidence for the root cause.

1. Reproduce or establish the observed failure from the smallest reliable evidence.
2. Read the actual error/output and recent relevant change before forming a fix.
3. Localize the failing boundary or data flow; gather only evidence that distinguishes remaining hypotheses.
4. Form one falsifiable hypothesis and test it with the smallest safe probe.
5. Trace a bad value/behavior to its source rather than patching the downstream symptom.
6. Report diagnosis separately from implementation authority.

If the issue is not reproducible, external, timing-dependent, or environmental, state the evidence and uncertainty rather than guessing.

## Tool Economy

For a bounded/local failure, inspect the directly implicated test, source, error, and recent diff first. Do not index a repository, enumerate code-graph projects, or run broad structural discovery by default. Use code graphs or wider repository mapping only when callers, dependencies, ownership, or impact radius are materially unclear and direct source inspection cannot answer the question efficiently.

Prefer one focused command/result over multiple overlapping discovery calls. Keep tool output bounded; do not feed large repository listings, histories, or unrelated logs back into the next turn.

## Progressive Disclosure

Load only the reference needed by the observed problem:

- `root-cause-tracing.md` for deep call/data-flow tracing.
- `condition-based-waiting.md` for timing/race failures.
- `defense-in-depth.md` after root cause is known and layered validation is justified.
- `../test-driven-development/remote-cdp-browser-lifecycle.md` for browser/CDP capture-state problems.
- `references/detailed-playbook.md` only when the compact contract is insufficient for a complex, repeated, or high-risk investigation.

Do not preload TDD or verification while diagnosis is still unresolved.
