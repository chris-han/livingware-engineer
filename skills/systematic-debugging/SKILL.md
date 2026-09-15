---
name: systematic-debugging
description: Use while an unexplained bug, test failure, regression, performance anomaly, or unexpected behavior requires root-cause investigation. For bounded/local failures, do not also activate repository-graph discovery unless direct source inspection leaves material relationship uncertainty.
---

# Systematic Debugging

## Lifecycle

Entry: an observed failure is still unexplained.
Exit: root cause and affected behavior are sufficiently established, or diagnosis-only work is complete.

After exit, stop carrying this workflow forward. Hand off only compact diagnostic state to the next workflow selected by the user's task. Re-enter only when new contradictory evidence makes the failure unexplained again.

## Core invariant

Do not fix before evidence establishes the root cause.

The minimum contract is:

1. establish the smallest reliable observation or reproduction;
2. inspect the directly implicated error/output/source/recent change;
3. localize the current uncertainty;
4. choose one falsifiable hypothesis and the cheapest safe distinguishing probe;
5. trace bad behavior to its source rather than patching a downstream symptom;
6. keep diagnosis separate from implementation authority.

If the issue is not reproducible, external, timing-dependent, or environmental, state the evidence and uncertainty instead of guessing.

## Tool economy

For bounded/local failures, use directly implicated tests/source/errors/diffs first. Add graph/index discovery only after direct inspection leaves a material caller/dependency/ownership question unresolved. Prefer focused commands and bounded results.

Executable mechanics remain owned by their scripts/tests. For example, `find-polluter.sh` is an operator; this skill decides when it is relevant but does not duplicate how it works.

## Progressive disclosure

Load only what the current state needs:

- `references/workflow-routing.md` when the next debugging state/branch is non-obvious;
- `root-cause-tracing.md` for deep call/data-flow tracing;
- `condition-based-waiting.md` for timing/race failures;
- `defense-in-depth.md` only after root cause is known and layered validation is justified;
- `../test-driven-development/remote-cdp-browser-lifecycle.md` for browser/CDP capture-state problems;
- `references/detailed-playbook.md` only when the compact contract is insufficient for a complex, repeated, or high-risk investigation.

Do not preload a future implementation or completion workflow while diagnosis is unresolved.
