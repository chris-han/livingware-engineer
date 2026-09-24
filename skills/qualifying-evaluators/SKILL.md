---
name: qualifying-evaluators
description: Use when an evaluator or judge already exists and you need to establish whether it is fit for a declared use with held-out evidence, hard negatives, invariance checks, calibration, or explicit limitations.
---

# Qualifying Evaluators

Treat an evaluator as a measurement instrument that requires its own evidence.

Read `../../docs/livingware-evaluation-architecture.md` for `EvaluatorQualification` and the non-authority rule.

## Deterministic evaluator qualification

Verify:

- positive fixtures;
- negative fixtures;
- hard negatives for important boundaries;
- repeatability;
- explicit missing-evidence / `UNKNOWN` behavior when applicable;
- version-pinned contract tests; and
- no hidden interpreted branch presented as deterministic.

## Interpreted evaluator qualification

Use domain-grounded labeled data and keep development examples disjoint from held-out measurement.

A typical split is:

```text
training examples -> prompt/scorer shaping
dev               -> iteration and disagreement analysis
held-out test     -> final qualification measurement
```

Do not copy train/dev/test percentages mechanically when data is scarce; preserve disjointness and enough positive/negative or per-class cases to support the declared claim.

For binary claims, report the confusion matrix and at least TPR/TNR. Raw accuracy alone is insufficient under class imbalance.

For typed frontiers, report per-class behavior and test candidate-order/permutation invariance when ordering could leak semantics.

For probabilistic outputs, include the calibration/selective-risk measures appropriate to the contract.

## Qualification gate

The evaluator contract must declare its gate. There is no repository-wide universal 90% threshold.

Possible dispositions:

```text
QUALIFIED
QUALIFIED_BOUNDED
NOT_QUALIFIED
```

A bounded qualification must state where the evaluator is trusted and where it must return `UNKNOWN`, defer, or remain advisory.

## Requalification triggers

Requalify after material changes to:

- prompt/rubric;
- model/scorer;
- frontier;
- evidence inputs;
- runtime behavior distribution; or
- the failure-mode definition itself.

## Invariants

- Held-out evidence is not used to tune the evaluator after measurement.
- Model confidence is not authority.
- Evaluator qualification does not authorize a routing/workflow/tool/policy change.
- Preserve evidence and dataset provenance.

## Output

Record metrics, disagreements, hard negatives, invariance checks, limitations, version pins, and the qualification disposition.
