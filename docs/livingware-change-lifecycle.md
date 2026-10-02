# Livingware Qualified Change Lifecycle

**Status:** canonical methodology contract  
**Release:** 6.13.6  
**Owner relationship:** extends `docs/livingware-evaluation-architecture.md` and `skills/governed-experimental-evolution`; it does not create a second runtime, evaluator authority, deployment authority, or autonomous self-modification service.

## Purpose

Livingware converts operational evidence into bounded, testable, economically justified change candidates without allowing the learning process to grant itself runtime authority.

The canonical lifecycle is:

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

The governing invariant is:

```text
observation != truth
experiment != qualification
qualification != admission
admission != activation
```

A learning system may propose change. Only the owning governance/deployment authority may grant production authority.

## Authority layers

- **Observation authority** may state what was observed under pinned provenance. It may not declare the correct interpretation.
- **Experimental authority** may state what happened under a frozen experiment contract. It may not prescribe production adoption.
- **Qualification authority** may decide whether a result satisfies predeclared scientific or technical gates. It may not activate the result.
- **Runtime authority** exists only after explicit admission, activation, and version binding.

No component may create evidence, judge its own evidence, and grant itself runtime authority.

## Canonical artifacts

The lifecycle may be instantiated in repository-native files, fixtures, databases, plans, or CI evidence. It does not require a new service or database.

### LearningObservation

Minimum fields:

```text
observation_id
decision_or_episode_ref
runtime_pins
frontier_or_choice_surface
selected_action_or_candidate
outcome
evidence_refs
authority_refs
provenance
observed_at
```

An observation is evidence, not a training label and not authority.

### AttributionResult

Classify the smallest plausible owning layer before changing anything:

```text
FRONTIER_DEFECT
CONTEXT_DEFECT
REPRESENTATION_DEFECT
SERIALIZATION_DEFECT
RULE_ENGINE_DEFECT
INFERENCE_CONFIG_DEFECT
CALIBRATION_DEFECT
MODEL_SELECTION_DEFECT
MODEL_CAPACITY_DEFECT
EVALUATOR_DEFECT
AUTHORITY_DEFECT
ENVIRONMENT_DEFECT
IMPLEMENTATION_DEFECT
UNKNOWN
```

Do not infer `MODEL_CAPACITY_DEFECT` from a bad score or from a larger model improving it. Rule out materially plausible lower-authority explanations first.

### ChangeHypothesis

A hypothesis must name:

```text
source observations
attribution class
causal claim
affected surface
expected effect
alternative explanations
falsification condition
non-regression constraints
evidence basis
```

"Train more" or "try a bigger model" is not a causal hypothesis.

### ExperimentCandidate

An experiment must declare before execution:

```text
hypothesis ref
intervention type
mutation surface
dataset / case basis
model / config refs
evaluation basis
primary metric
secondary metrics
non-regression gates
seed policy
budget envelope
expected quality gain
expected information gain
cost
risk
reversibility
stop condition
```

Changing the basis after seeing results creates a new experiment version.

### ScientificResult

Assessment records what happened, including per-seed results, regressions, integrity checks, cost, and whether the causal hypothesis was supported, rejected, or remains inconclusive.

### QualificationResult

Qualification is a deterministic disposition over the frozen experiment contract:

```text
PASS | FAIL | INCONCLUSIVE
```

`PASS` creates qualification evidence only. It does not create admission or activation authority.

### ChangeCandidate

A qualified change proposed for admission must bind:

```text
qualification result
affected runtime surface
target version
rollback target
blast radius
reversibility
deployment requirements
governance requirements
```

## State machine

### S0 OBSERVED

Entry requires enough provenance to identify the relevant execution, configuration, evaluation contract, and evidence.

Failure paths:

```text
missing provenance -> REJECTED_INVALID_OBSERVATION
non-replayable basis -> HOLD_REPLAY_REPAIR
material duplicate -> ARCHIVED_LOW_VALUE
```

No mutation authority is granted.

### S1 ATTRIBUTED

Guard:

```text
OBSERVED -> ATTRIBUTED
requires replayable/material evidence + pinned attribution basis
```

Route non-learning defects to their natural owner. `UNKNOWN` attribution is deferred rather than coerced into a model-training explanation.

### S2 HYPOTHESIZED

Guard:

```text
ATTRIBUTED -> HYPOTHESIZED
requires bounded surface + causal mechanism + falsification condition
```

Failure paths:

```text
untestable -> REJECTED_UNTESTABLE
too broad -> RETURN_TO_ATTRIBUTION
insufficient evidence -> DEFERRED
```

### S3 EXPERIMENT_READY

Construct a bounded experiment frontier. Include `NO_CHANGE` as a valid candidate.

Prefer interventions in increasing authority/cost order when they remain plausible:

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

Parameter updates are not the default response to failure.

Use a value-of-experiment comparison:

```text
VoE =
  expected quality gain
  + expected information gain
  - compute cost
  - control/review cost
  - risk
```

If no candidate has positive value under the current evidence and budget, close with `NO_CHANGE`.

### S4 EXPERIMENTING

Experiments execute only inside their declared mutation boundary and budget. Experimental checkpoints and configurations have no production authority.

Failure paths:

```text
budget exhausted -> EXPERIMENT_TERMINATED
invalid provenance -> EXPERIMENT_INVALID
contamination -> EXPERIMENT_INVALID
infrastructure failure -> EXPERIMENT_ABORTED
training/optimization failure -> EXPERIMENT_FAILED
```

Invalid or aborted experiments do not produce qualification evidence.

### S5 ASSESSED

Guard:

```text
EXPERIMENTING -> ASSESSED
requires all required runs accounted for
and identities/hashes/basis/seed policy verified
```

Assessment answers "what happened?" not "should production adopt it?"

### S6 QUALIFIED

Qualification must cover, as applicable:

1. identity/provenance/integrity;
2. predeclared primary effect;
3. multi-seed consistency;
4. hard non-regression constraints;
5. cost/budget validity.

A single favorable run is hypothesis evidence, not admission evidence.

### S7 ADMITTED

Admission belongs to the owning project/governance/deployment surface, not the optimizer.

Guard:

```text
QUALIFIED -> ADMITTED
requires PASS
+ architecture compatibility
+ authority compatibility
+ rollback path
+ explicit deployment scope
+ resolved operational ownership
```

Admission may reject a scientifically qualified change for architecture, authority, migration, cost, or operational reasons.

### S8 SHADOW

Shadow execution may observe production-context behavior but must not control production effects unless separately authorized.

For decision systems, compare at least:

```text
active right / shadow right
active right / shadow wrong
active wrong / shadow right
both wrong
same decision / materially different calibration
different abstention
```

### S9 ACTIVATED

Activation is the only transition that grants runtime authority.

Bind the active artifact/configuration to exact versions/hashes plus rollback target and effective interval. Historical executions remain bound to the versions that actually governed them.

### Rollback and supersession

```text
ACTIVATED -> ROLLED_BACK
candidate state -> SUPERSEDED
```

Rollback and supersession are append-oriented lifecycle events. They do not erase prior evidence or mutate historical runs.

## Training-data admission

When the intervention is parameter learning, runtime data is not automatically training data.

Require:

1. replay/integrity;
2. failure attribution to the model-owned surface;
3. sufficient evidence quality;
4. novelty or unresolved decision value;
5. no use of evaluation-only or sealed confirmation material.

For repeated samples or rollouts of a bounded decision case:

```text
all correct -> regression anchor, normally no gradient
all wrong   -> diagnostic pool, normally no gradient
mixed       -> decision-boundary candidate
```

An all-wrong group may indicate missing frontier support, representation failure, label/evaluator error, or genuine capacity failure; diagnose before training.

A useful prioritization measure may combine:

```text
attribution
x novelty
x decision relevance
x boundary entropy
x evidence quality
```

This is a prioritization heuristic, not semantic authority.

## Multi-seed evaluation

Seed policy is frozen before execution.

Use multiple training or optimization seeds when stochastic optimization is material and multiple inference/evaluation seeds when stochastic decision behavior is material. Avoid seed search.

Admission evidence should include per-seed results, central tendency, harmful worst-case checks, and explicit non-regression gates. Exact seed counts and thresholds are project-specific and must be declared by the owning experiment contract.

## Confirmation boundary

Preserve the existing DEV -> QUAL -> FREEZE -> CONFIRM contract from Governed Experimental Evolution.

A CONFIRM population, labels, thresholds, evaluator basis, and frozen protocol are sealed authority surfaces. They cannot be tuned by the candidate they judge. A failed CONFIRM campaign cannot be patched and rerun while still claiming independence.

## Failure states

Prefer typed dispositions over generic `FAILED`:

```text
REJECTED_INVALID_OBSERVATION
REJECTED_BAD_PROVENANCE
REJECTED_UNTESTABLE
DEFERRED_NEEDS_EVIDENCE
DEFERRED_BUDGET
EXPERIMENT_ABORTED
EXPERIMENT_FAILED
EXPERIMENT_INVALID
QUALIFICATION_FAILED
QUALIFICATION_INCONCLUSIVE
ADMISSION_REJECTED
SHADOW_REGRESSION
SHADOW_INCONCLUSIVE
ACTIVATION_FAILED
ROLLED_BACK
SUPERSEDED
NO_CHANGE
```

Failure is evidence. It does not automatically authorize another experiment.

## Livingware laws

1. **Evidence before hypothesis.**
2. **Attribution before intervention.**
3. **Hypothesis before experiment.**
4. **Fixed basis before execution.**
5. **Information before compute.**
6. **Qualification before admission.**
7. **Admission before activation.**
8. **Shadow before risk-bearing authority when practical.**
9. **Replay before trust.**
10. **No self-authorizing learner.**
11. **NO_CHANGE is a valid successful disposition.**
12. **Activation never rewrites history.**

The optimization target is not mutation frequency or benchmark score. It is useful, qualified decision improvement per total learning/change cost, subject to architecture and authority constraints.
