---
name: governed-experimental-evolution
description: Use when a failure is already attributed and you need to iteratively test system changes, hillclimb a bounded surface, compare interventions, or freeze a DEV/QUAL/CONFIRM capability claim without letting the optimizer mutate its own evaluation authority.
---

# Governed Experimental Evolution

Use evaluation evidence to evolve a system without turning score improvement into authority.

Read `../../docs/livingware-evaluation-architecture.md` for the canonical GEE contract.

## Preconditions

Require a bounded claim, a fit measurement instrument, a supported failure attribution with alternatives, a declared mutation surface, and a replayable baseline. If the failure space is immature, use `discovering-failures`. If the evaluator is not fit, use `designing-evaluators` or `qualifying-evaluators`.

## Stage contract

```text
DEV     -> discover and iterate; improvement is candidate evidence only
QUAL    -> development qualification; may be consulted repeatedly
FREEZE  -> freeze system + evaluator + thresholds + manifests
CONFIRM -> sealed independent evidence; no tuning from the result
```

A failed CONFIRM run closes that campaign. If development reopens, that confirmation population is historically exposed and a later confirmatory claim requires a new independent campaign.

## Failure classes

```text
REFERENCE_FAILURE
STRUCTURAL_ADMISSIBILITY_FAILURE
PROJECTION_FAILURE
FRONTIER_FAILURE
SEMANTIC_DISCRIMINATION_FAILURE
CALIBRATION_FAILURE
ROBUSTNESS_FAILURE
SCORER_PROTOCOL_FAILURE
MODEL_CAPACITY_FAILURE
INFRASTRUCTURE_FAILURE
EVALUATION_DESIGN_FAILURE
```

Do not infer `MODEL_CAPACITY_FAILURE` from a bad score or from a larger model improving it. First evaluate materially plausible lower-authority explanations.

## Mutation authority

- `M0`: automatically mutable inside DEV — low-authority experimental knobs.
- `M1`: experiment mutable — representation/projection, context contraction, scorer/readout, calibration, model choice; requires QUAL before admission.
- `M2`: governed semantic surface — frontier/predicate semantics, UNKNOWN meaning, admissibility, authority/precedence, ontology, acceptance-policy semantics; propose only, never autonomously activate.
- `M3`: sealed experimental authority — CONFIRM corpus/labels, frozen thresholds/protocol, historical run records, manifest hashes; mutation invalidates the campaign.

The candidate under optimization must not control the basis that judges its own admission.

## One-intervention loop

```text
baseline
  -> inspect attributed failure
  -> state causal hypothesis
  -> change one bounded surface
  -> DEV
  -> QUAL when worth promoting
  -> RETAIN | REVERT | INCONCLUSIVE | INVALID_EXPERIMENT | INVALID_EVAL
```

Use a composite intervention only when components cannot meaningfully be isolated, and mark attribution strength as limited. Persist negative and reverted trials.

## Intervention lineage

Preserve at least:

```text
intervention_id
parent_baseline_id
target_failure_class
causal_claim + expected metric effect
mutation authority class + surface
before/after/diff identity
DEV run refs
QUAL run refs
metric deltas + uncertainty
regressions
disposition
```

## Admission gate

```text
DEV_PASS
AND QUAL_PASS
AND NO_HARD_REGRESSION
AND ATTRIBUTION_SUPPORTED
AND MUTATION_AUTHORITY_VALID
```

Score improvement alone is insufficient.

## Exit

Exit with an admitted working-baseline intervention, a reverted/rejected intervention, an inconclusive/invalid experiment, a frozen architecture ready for CONFIRM, `CONFIRMED`, or `NOT_CONFIRMED` with development reopened under a future independent confirmation campaign.
