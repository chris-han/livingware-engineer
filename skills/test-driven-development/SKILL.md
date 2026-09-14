---
name: test-driven-development
description: Use when implementing an authorized behavior change, a bug fix with established diagnosis, or a behavior-preserving refactor. Do not use for unresolved root-cause investigation or final completion claims.
---

# Test-Driven Development

## Lifecycle

Entry: intended changed behavior or the preservation contract is defined well enough to implement.
Exit: focused behavior evidence is green and the implementation is ready for any broader completion/integration claim.
Do not retain debugging instructions after diagnosis is established, and do not preload final verification while implementation is active.

## Core Contract

Choose the cycle that matches the change:

- New/changed behavior: establish a meaningful failing behavioral test, implement the minimum change, then make it green.
- Bug fix: use a defect reproducer or negative control that fails for the diagnosed defect, then fix and make it green.
- Behavior-preserving refactor: establish adequate passing characterization/regression coverage first, refactor, then preserve the same observable behavior.

Tests should assert real behavior. Mock only true external/nondeterministic boundaries when necessary. Do not use an internal mock as evidence that an architectural path exists.

For architectural changes, at least one completion path must exercise changed in-repo production components through real wiring. For frontend/UI changes, completion requires the affected real-browser behavior/render evidence appropriate to the change.

## Tool Economy

For a bounded change with known files and diagnosis, read those files and run the focused test directly. Do not enumerate repositories, build a code graph, inspect whole-workspace impact, or load browser/integration procedures unless the observed impact radius requires them.

Use relationship-aware discovery only when callers, downstream consumers, wiring, persistence, trust boundaries, or user paths are genuinely uncertain. Keep search/result limits tight and prefer existing focused tests over broad suites during the RED/GREEN loop.

## Progressive Disclosure

Load details only when triggered:

- `writing-good-tests.md` when test design, mocking, or oracle quality is nontrivial.
- `impact-radius-testing.md` when integration/E2E scope is uncertain.
- `remote-cdp-browser-lifecycle.md` only for frontend/browser evidence.
- `references/detailed-playbook.md` only when the compact contract is insufficient for a complex/high-risk implementation.

After focused implementation evidence is green, leave this workflow. Let a completion claim match verification rather than carrying this body forward.
