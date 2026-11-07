# Risk-Based Pre-Execution Failure Review

Use this reference when a plan crosses two or more independently owned components, asynchronous state, credential/profile scope, caches, external adapters, or an R2/R3 native user journey. Skip it for clear R0/R1 fixes unless an actual risk warrants review.

**Goal:** find costly false assumptions *before* implementation, not maximize planning tokens or create another approval stage. This is an autonomous, evidence-based plan-review pass under the existing plan authority. If review finds no material issue, proceed; never force spending an arbitrary token quota. The first experimental review ceiling may be roughly 10% of the expected task tokens, but it is an optional soft budget, not a success condition or a requirement to spend it.

## Review contract

1. **Freeze a small owner map:** original user outcome; existing and missing behavior; exact producer, cache, RPC, UI, persistence and runtime owners; what has already been implemented or disproven; current source/commit identity. Avoid rereading full repository/skill bundles when the scoped source map is still valid.
2. **Independent failure pass:** an independent reviewer or fresh narrow context, when available, examines the *same plan* and source anchors. This is review, not permission to launch competing implementation agents or duplicate prototypes.
3. **Falsify boundary assumptions:** seek concrete counterexamples for startup/connection-ready, cold/warm cache, profile/tenant/source change, in-flight response ordering, cancellation, retry/error, success-empty versus failed fetch, auth changes, timeout mismatch, success-after-client-timeout, historical saved state, deployment/installer and restored sessions as applicable. Don't demand irrelevant cases.
4. **Classify findings:** for each material finding record the exact assumption, source witness or uncertainty, expected failure, minimal early discriminator, owning task, and disposition `REVISE | TEST_EARLY | ACCEPT_WITH_REASON`. Prefer the top three high-cost failure modes; cap review narration.
5. **Move the earliest useful test forward:** each material R2/R3 lifecycle risk should have a focused real-component/native synthetic smoke **before the first broad integration/merge where practicable**. Final full/native verification and integration obligations are unchanged. A missing native environment is a qualification gap, not a reason to fabricate proof.
6. **Stop review on diminishing value:** once owner map is coherent, material findings have dispositions and early tests, proceed to activation/execution automatically. Re-review only when the user changes requirements or contradictory evidence appears.

## Compact plan-local result

```yaml
pre_execution_failure_review:
  applicability: REQUIRED  # or SKIPPED with reason
  source_basis: [source files + commit]
  review_result: READY | REVISED | BOUNDED_GAP
  top_findings:
    - risk: cross-profile async refresh
      witness: real event/owner path or UNKNOWN
      disposition: TEST_EARLY
      early_test: profile A warm -> B connection delayed -> one B refresh
  pre_merge_native_smoke: path or NOT_APPLICABLE
  test_scope_basis: VIA R2/R3 reference
```

## Historical motivation, not proof of impact

The Semantier Windows Provider-query-only implementation (2026-11-07) detected a cold Apply timeout and a warm-cache profile-switch refresh race only during late native testing and post-integration. Earlier counterexample-based review *might* have found these risks; the historical trace cannot establish how many tokens that would save. See [the baseline](../../../docs/engineering-economics/2026-11-07-windows-provider-query-only-baseline.md).

Do not count review as beneficial simply because it is longer. Evaluate whether it reduces post-integration rework and total tokens to a comparable, verified outcome.
