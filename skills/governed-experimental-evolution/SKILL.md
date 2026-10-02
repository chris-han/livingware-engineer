---
name: governed-experimental-evolution
description: Use when a failure is already attributed and you need to convert operational evidence into bounded change hypotheses, select experiments, train or tune a system, compare interventions, qualify multi-seed evidence, or freeze a DEV/QUAL/CONFIRM capability claim without letting the optimizer mutate its own evaluation or activation authority.
---

# Governed Experimental Evolution

Use evidence to evolve a system without turning score improvement into authority.

Read:

- `../../docs/livingware-change-lifecycle.md` for the canonical observation-to-activation state machine, authority boundaries, experiment selection, training-data admission, and multi-seed qualification.
- `../../docs/livingware-evaluation-architecture.md` for Eval IR, evaluator non-authority, provenance, and failure attribution.

## Preconditions

Require a bounded claim, a fit measurement instrument, a supported failure attribution with alternatives, a declared mutation surface, and a replayable baseline.

If the failure space is immature, use `discovering-failures`. If the evaluator is not fit, use `designing-evaluators` or `qualifying-evaluators`.

Do not infer `MODEL_CAPACITY_FAILURE` from a bad score or from a larger model improving it. First evaluate materially plausible lower-authority explanations.

## Qualified-change lifecycle

Use the smallest applicable segment of:

```text
OBSERVED
  -> ATTRIBUTED
  -> HYPOTHESIZED
  -> EXPERIMENT_READY
  -> EXPERIMENTING
  -> ASSESSED
  -> QUALIFIED
  -> ADMITTED
  -> SHADOW
  -> ACTIVATED
```

This skill owns bounded experimentation and qualification mechanics. It does not grant admission or activation authority.

```text
observation != label
experiment result != qualification
qualification != admission
admission != activation
```

If a host repository owns admission, deployment, governance, or activation, stop at the appropriate handoff artifact and follow that owner.

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

Route failures to the smallest durable owner before constructing an intervention.

## Mutation authority

- `M0`: automatically mutable inside DEV — low-authority experimental knobs.
- `M1`: experiment mutable — representation/projection, context contraction, scorer/readout, calibration, model choice; requires QUAL before admission.
- `M2`: governed semantic surface — frontier/predicate semantics, UNKNOWN meaning, admissibility, authority/precedence, ontology, acceptance-policy semantics; propose only, never autonomously activate.
- `M3`: sealed experimental authority — CONFIRM corpus/labels, frozen thresholds/protocol, historical run records, manifest hashes; mutation invalidates the campaign.

The candidate under optimization must not control the basis that judges its own admission.

## Form a falsifiable hypothesis

Before an experiment, state:

```text
source observations
attribution class
causal mechanism
affected surface
expected effect
alternative explanations
falsification condition
non-regression constraints
```

"Train more" is not a causal hypothesis.

## Build the experiment frontier

Include `NO_CHANGE`.

Prefer the lowest-authority plausible intervention before higher-cost or harder-to-reverse mutation:

```text
NO_CHANGE
INFERENCE_CONFIG
SERIALIZATION
REPRESENTATION
DATA_REBALANCE
CALIBRATION
PARAMETER_UPDATE
MODEL_SCALE
```

Compare candidates by expected quality gain and information gain against compute, review/control cost, risk, and reversibility. If no candidate has positive value, close with `NO_CHANGE`.

Before execution freeze:

```text
hypothesis
evaluation basis
primary metric
secondary metrics
non-regression gates
seed policy
budget
stop condition
```

Changing these after seeing results creates a new experiment version.

## Training-data admission

When parameter learning is selected, runtime evidence must pass a separate admission boundary before becoming gradient-bearing data.

Require replay/integrity, model-owned attribution, sufficient evidence quality, and no leakage from sealed confirmation material.

For repeated samples of a bounded case:

```text
all correct -> regression anchor
all wrong   -> diagnostic pool
mixed       -> decision-boundary candidate
```

Normally train on qualified boundary, hard-negative, and abstention candidates, not indiscriminately on every runtime observation.

An all-wrong case is diagnostic until missing frontier support, representation defects, evaluator/label defects, and other plausible causes are ruled out.

## One-intervention loop

```text
baseline
  -> inspect attributed failure
  -> state causal hypothesis
  -> choose one bounded intervention
  -> DEV
  -> QUAL when worth promoting
  -> RETAIN | REVERT | INCONCLUSIVE | INVALID_EXPERIMENT | INVALID_EVAL | NO_CHANGE
```

Use a composite intervention only when components cannot meaningfully be isolated, and mark attribution strength as limited. Persist negative and reverted trials.

## Multi-seed qualification

Freeze seed policy before execution. Do not search seeds.

Use multiple optimization/training seeds when training stochasticity is material and multiple inference/evaluation seeds when decision stochasticity is material.

Qualification evidence should expose per-seed results, central tendency, harmful worst-case behavior, and hard non-regression checks. Exact counts and thresholds belong to the host experiment contract.

A single favorable run may generate a hypothesis; it does not justify admission.

## Intervention lineage

Preserve at least:

```text
intervention_id
parent_baseline_id
target_failure_class
causal_claim + expected metric effect
mutation authority class + surface
before/after/diff identity
data/case basis identity
evaluation basis identity
seed policy
DEV run refs
QUAL run refs
metric deltas + uncertainty
regressions
cost
disposition
```

## Qualification gate

A typical bounded gate is:

```text
INTEGRITY_PASS
AND PRIMARY_EFFECT_PASS
AND MULTI_SEED_CONSISTENCY_PASS
AND NO_HARD_REGRESSION
AND ATTRIBUTION_SUPPORTED
AND MUTATION_AUTHORITY_VALID
AND BUDGET_VALID
```

Score improvement alone is insufficient.

Return:

```text
PASS | FAIL | INCONCLUSIVE
```

`PASS` creates a qualified change candidate. It does not activate it.

## Admission, shadow, activation

If the host repository has an owner for these states, hand off there.

- **ADMITTED** means an authorized owner accepted the qualified change for deployment consideration.
- **SHADOW** means the candidate may observe production-context behavior without controlling production effects.
- **ACTIVATED** is the only state that grants runtime authority.
- **ROLLED_BACK** and **SUPERSEDED** preserve historical lineage; they do not erase prior runs.

## Exit

Exit with one of:

- admitted working-baseline intervention;
- qualified change candidate awaiting admission;
- reverted/rejected intervention;
- inconclusive/invalid experiment;
- `NO_CHANGE`;
- frozen architecture ready for CONFIRM;
- `CONFIRMED`;
- `NOT_CONFIRMED` with development reopened under a future independent confirmation campaign.

Never continue experimenting merely because experimentation is possible.
