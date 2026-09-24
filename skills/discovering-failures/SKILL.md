---
name: discovering-failures
description: Use when you have agent, workflow, or skill traces but do not yet have a trustworthy failure taxonomy and need evidence-first error discovery before designing evaluators or learning changes.
---

# Discovering Failures

Discover failure modes from execution evidence before freezing a taxonomy or writing evaluators.

Read `../../docs/livingware-evaluation-architecture.md` for `FailureObservation`, `FailureModeCandidate`, evidence provenance, and the breadth/depth loop.

## Workflow

1. Inspect a diverse set of complete traces, not only final outputs.
2. Record free-form `FailureObservation` notes before assigning a reusable category.
3. Sample for breadth: include cluster/feature representatives and some random exploration.
4. When a pattern appears, switch to depth: refine its definition, seek additional instances, counterexamples, and hard negatives.
5. Revisit earlier traces when reviewer criteria change.
6. Promote a pattern to a `FailureModeCandidate` only when multiple observations support a reusable boundary.
7. Attribute the failure only after the observed pattern is sufficiently clear.

## Annotation rule

Initial review should favor free-text observations over a preloaded checklist. A pre-existing taxonomy may be shown as reference when the task is regression verification, but it must not force novel observations into existing labels.

Agent-suggested instances are proposals, not ground truth.

## Failure-mode record

For each candidate, preserve:

```text
name
definition
supporting observations
counterexamples
hard negatives
coverage regions reviewed
known blind spots
candidate status
```

## Invariants

- Observation != failure mode.
- Failure mode != root cause.
- Root cause != learning action.
- Do not invent a failure category to justify an existing evaluator.
- Do not estimate prevalence from a diversity-biased discovery sample.
- Preserve `OBSERVED | REPLAYED | SIMULATED | INFERRED | ASSUMED` provenance.

## Exit

Exit when the relevant failure space is sufficiently explicit to design a bounded evaluator or when evidence shows no reusable failure mode yet. Hand evaluator construction to `designing-evaluators`.
