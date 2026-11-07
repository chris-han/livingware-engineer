# Execution Economics: Measured Costs, Checkpoints, and Comparable Outcomes

Use when the user wants a token-economy comparison, or when an implementation is large/cross-boundary enough that repeated discovery and reruns materially affect cost. Never add instrumentation gates that delay an ordinary low-risk task; use host/runner usage receipts when available and report absent fields as `UNKNOWN`, not zero.

## Stage checkpoint and context discipline

At each meaningful completed gate, store or link one **compact** checkpoint in the owning plan/evidence path:

```yaml
stage: W2
source_commit: exact_sha
requirements_basis: plan_or_spec_anchor
completed: [source_owner, contracts]
unresolved_risk: [race, stale_cache]
verified:
  - test_suite: exact_name
    commit: exact_sha
    result: pass|fail|not_run
next_discriminating_action: exact_step
reuse_evidence: [prior_verified_receipt_ids]
```

Carry only changed findings, source references and the next dependency-ready step into a resumed context; never preload whole prior chats, skill bodies, massive file dumps or duplicate test logs. Reopen raw evidence when SHA changes, confidence expires or a new causal question actually requires it. Do not delete authority records, suppress failures or replace real checks with summaries.

## Test economics without sacrificing correctness

- Apply Verification Impact Analysis (R0–R3). Fast deterministic checks and focused TDD on each local change; targeted boundary/integration tests as the production path grows.
- For a cross-boundary lifecycle/async change, test the highest-risk *real-component/native synthetic journey before first expensive integration* where feasible. Include identity transitions, cold/warm startup, cancellation, failure, success-empty, timeout and late success when relevant.
- At a reasonably frozen integrated candidate, run the planned broad suite **once** (or more when its actual impact requires it). After a narrow patch, rerun affected tests and boundary consumers; cite reusable unchanged-suite evidence by exact commit and assessed impact. Never reuse stale evidence for changed lines or affected seams.
- Do not classify necessary regression reruns as waste. Record for each notable test: `commit, suite, scope, reason (first_check|changed_code|reproduction|merge|release), duration, outcome, evidence_reuse`.
- A failed or flaky test needs diagnosis; a pass on unchanged base can qualify causality, but not silently convert an unresolved failure into a passing acceptance gate.

## Economy receipt: what to capture

For each task, record `task_id, plan_ref, baseline_id, model/version, effort, tool/harness version, repo SHA, scope/risk, goal/acceptance, start/end`. For each stage (when available): `input_tokens, output_tokens, cache_read_tokens, cache_write_tokens, total_reported_tokens, token_definition, wall_seconds, tool_calls, repeated_same_sha_file_reads, test_invocations, native_fixture_setups, post_integration_rework_cycles`. Distinguish provider-billed input from cache reads and host-displayed total; do not sum overlapping fields or invent dollars without actual price/rate and usage. Keep sanitized aggregate receipts; do not persist secrets, private model reasoning, or raw private session transcripts merely to measure costs.

If telemetry cannot be collected automatically, keep a small end-of-run receipt with available totals and `null` for unknown fields. Do **not** claim exact token attribution from a stage history or a test-count table.

## Compare against a baseline

Historical reference: [Semantier Windows Provider-query-only baseline](../../../docs/engineering-economics/2026-11-07-windows-provider-query-only-baseline.md).

Use a before/after comparison **only after terminal evidence**, using the same accounting convention and a clearly stated task-comparability class. Measure:

- `total_tokens_to_verified_outcome` including planning and review when metered, versus separately reported implementation tokens where planning is not metered;
- `wall_minutes_to_verified_outcome`;
- `pre_activation_review_tokens / total_tokens` and material risks found;
- `post_integration_rework_cycles`, duplicate same-SHA full-file reads, avoidable test invocations and native setup repetitions;
- `real_native_acceptance`, regression coverage, remaining blockers and resulting scope.

For comparable outcomes only: `token_ratio = next_total / baseline_total`, `reduction_percent = (1 - token_ratio)*100`; similarly for elapsed time. Do not call a smaller task a gain without a matched scope. For unmatched tasks, report raw figures and risk/scope notes; no causality or efficiency percentage.

Keep the iteration verdict `IMPROVED | REGRESSED | INCONCLUSIVE | NOT_COMPARABLE` with evidence. A lower token count with missing acceptance is NOT an improvement. One subsequent task is a directional case study, not a statistically established improvement.
