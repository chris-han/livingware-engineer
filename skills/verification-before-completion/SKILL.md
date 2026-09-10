---
name: verification-before-completion
description: Use before claiming work is correct, complete, fixed, or passing, or before an integration/release action whose safety depends on that claim
---

# Verification Before Completion

Before claiming correctness or completion:

1. **Name the scope of the claim.** Distinguish a focused task, integrated implementation, and completion of a declared MVL Contract.
2. **Identify the check that can falsify it.** Choose the smallest check capable of catching the mistake; cover real component boundaries when the claim depends on them.
3. **Run that check, or reuse a valid unchanged-state result.** Run the full selected command, not a partial substitute.
4. **Read the result and update the actual state.** Inspect the output, exit code, failures, and relevant measurements. A failed or unverified required check means the claimed scope is not complete. Record/report passing scope and remaining gaps concisely, then continue immediately to the next actionable repair or verification step unless the Human Judgment Necessity Test in `docs/mvl-laws.md` is met. Reporting status is never itself a stop condition.

## Result Validity and Scope

Reuse an observed passing result when the relevant code, tests, dependencies, configuration, fixtures, and execution environment are unchanged and the result/output is available to inspect. If relevant state changed or its identity is uncertain, rerun affected checks. Live or time-sensitive external claims require a current check.

Run focused tests during implementation and expensive integration at coherent sprint exits, with earlier checks for demonstrated boundary risk. Before claiming integrated completion, verify the final assembled state with the required affected integration/browser checks. A focused pass is not a full-suite pass.

Do not rerun checks merely to send a progress update, delegate an independent task, express a non-technical acknowledgment, or enter another workflow phase.

Verification decides technical claims, not whether execution should pause. A green gate advances automatically. A red gate normally creates repair/debug work. An unverified gate creates the next verification action. None of these require user judgment unless the remaining decision passes the Human Judgment Necessity Test.

Use existing test output and version history. Do not create duplicate verification packages, intermediate reports, or status ledgers unless the user or repository explicitly requires them. Required product audit/replay, persistence, and recovery contracts remain intact.

## Match the Check to the Claim

| Claim | Required result | Does not establish it |
|-------|-----------------|-----------------------|
| Tests pass | Observed zero failures for the claimed scope and valid verified state | “Should pass,” unavailable or stale output |
| Linter clean / build succeeds | The corresponding command completes successfully | A different tool passing or partial output |
| Bug fixed | Original symptom reproduced by a test/control, then passing after the fix | Code changed or unrelated tests passing |
| Behavior preserved | Adequate characterization/regression coverage passes before and after | An artificial RED phase or current-only pass |
| Requirements met | Check the actual requirements against implemented behavior and applicable results | Tests passing without covering the requirements |
| Architecture implemented | Real-component integration through production wiring | Unit tests that mock the internal architecture |
| Frontend complete | Real-browser verification of the changed user path | jsdom, snapshots, mocked children, or source inspection alone |
| Delegated work complete | Inspect the actual diff and applicable verification results | The agent's success assertion alone |

Use the test cycle selected by `superpowers:test-driven-development`: meaningful failing behavior/control for new behavior and bug fixes; adequate green-before/green-after coverage for behavior-preserving refactors. Inspect delegated results under the same reuse rule; an independent inspection does not automatically require rerunning unchanged checks.

## Browser Results

Before attaching a completion claim to a persistent browser, use the [browser selection and lifecycle contract](../test-driven-development/remote-cdp-browser-lifecycle.md). It owns engine selection, startup, process ownership, shared-browser protection, and cleanup.

For shared Chrome rendering checks, measure and capture the same target at its natural viewport, confirm no active fixture override, clean up owned pages/sessions/clients, and confirm the shared endpoint remains reachable. A screenshot from an overridden or stale target does not establish the intended rendering result.

## Declared MVL Completion

Implementation completion requires verified local behavior, real-component integration where applicable, real-browser UI verification for frontend changes, and vertical/E2E verification when required.

When the plan declares an MVL Contract, passing implementation checks alone does not establish MVL completion. Compare results with that contract:

- Same target user / JTBD and smallest real journey.
- Same realistic trial inputs, or documented representative fixtures.
- Required technical and UX measurements.
- Feedback capture that records usable data.
- Required improvement justified by those results.
- Comparable re-test on the same surface after improvement.
- The declared stopping criterion satisfied.

If these remain open or the journey has drifted, report implementation and MVL status separately. Resolve the mismatch with the plan/spec before claiming MVL completion; do not introduce an MVL process for work that has no such contract.
