# Model-Training Intervention Qualification

Use this reference when a maintained research program is considering model training, finetuning, distillation, adapter updates, loss/objective changes, reward-driven optimization, data expansion, model scaling, or a related parameter-learning intervention.

The purpose is not to make training easier to start. It is to determine whether a named residual uncertainty actually requires parameter change, and if so to reduce the training design to the smallest causally meaningful intervention.

## Governing question

Qualify training relative to the current research state:

```text
observed deficit / uncertainty
  -> validate the evidence and non-training surfaces
  -> isolate the residual learnable deficit
  -> contract the intervention space
  -> TRAINING_CANDIDATE | non-training disposition | STOP
```

The key distinction is:

```text
model error observed
!= training required
!= training admissible
!= training effective
!= model admitted
```

## TrainingInterventionAssessment

Use the smallest representation needed. When a structured assessment is useful:

```yaml
uncertainty_ref: <active uncertainty / research owner>
evidence_refs:
  - <terminal result / dataset / trace / evaluator / benchmark>

disposition:
  type: NO_TRAINING | NON_PARAMETRIC_FIX | CALIBRATION_ONLY | TRAINING_CANDIDATE | LEARNING_SYSTEM_CANDIDATE | STOP_INSUFFICIENT_EVIDENCE

residual:
  observed_deficit: <bounded statement>
  attribution_status: ESTABLISHED | PARTIAL | UNRESOLVED
  learnable_target: <what parameter learning could change, if any>

intervention_delta:
  representation_or_context: NONE | REPAIR_REQUIRED
  readout_or_interface: NONE | REPAIR_REQUIRED
  deterministic_compute: NONE | USE_DETERMINISTIC_PATH
  calibration: NONE | QUALIFY_SEPARATELY
  parameter_learning: NONE | CANDIDATE
  learning_system: NONE | CANDIDATE

next_action:
  type: STOP | REPAIR | CALIBRATE | DESIGN_BOUNDED_TRAINING_EXPERIMENT | DESIGN_LEARNING_SYSTEM_EXPERIMENT
```

These labels route research. They do not grant implementation, training, model, admission, deployment, or activation authority.

## Pre-training diagnosis

Before opening an optimizer, verify in order:

1. **Reference / evaluator validity** — labels, targets, reward/evaluator semantics, split roles, and provenance are sufficient for the intended claim.
2. **Deterministic computability** — if the target can be computed exactly, route it to deterministic code/rules rather than training.
3. **Representation / context sufficiency** — required evidence, scope, dependencies, and semantic context are available and bound correctly.
4. **Readout / interface / numerical integrity** — candidate mapping, token/feature boundaries, score normalization, precision, cache behavior, and inference packaging are not the unresolved cause.
5. **Existing-system sufficiency** — a current model, adapter, prompt/interface treatment, or non-parametric mechanism does not already satisfy the frozen target.
6. **Calibration separation** — a probability-scale or abstention-policy problem is not misclassified as semantic learning.
7. **Residual attribution** — the remaining deficit is plausibly attributable to learnable behavior under the frozen contract.
8. **Training admissibility** — training data, reference independence, retention basis, resource budget, protected evaluation, and model/optimizer authority are qualified enough for the proposed claim.

If the evidence cannot distinguish these explanations, choose `STOP_INSUFFICIENT_EVIDENCE` or the appropriate repair disposition rather than training through ambiguity.

## Derive before search

Partition the adjustable training design into three classes:

```text
Frozen structural contract
  -> semantics, target/evaluator meaning, split roles, protected evidence,
     retention obligations, admissible action space, authority boundaries

Derived variables
  -> quantities mechanically determined from the frozen contract and resource envelope

Residual Experimental Frontier (REF)
  -> only causally unresolved choices whose alternatives can change the named decision
```

A knob is not a research variable merely because software exposes it. Derive what can already be derived. Do not reopen closed, falsified, or architecturally irrelevant choices under a new sweep.

Automated search may operate only inside the frozen REF.

## Stage-attributed training

Treat training as attributed intervention classes rather than one undifferentiated finetune. Depending on the task, useful stages may include:

```text
qualified base / representation
  -> interface or task-format adaptation, if needed
  -> bounded semantic / task specialization
  -> calibration / abstention qualification
  -> verifier- or evaluator-grounded optimization, only when separately eligible
```

This is not a mandatory universal sequence. Skip a stage when its capability is already present or its intervention is irrelevant.

Every reached stage should state the capability or operator property it is intended to buy and compare against the nearest valid parent checkpoint or control.

## Stage report card

Use one frozen held-out basis across comparable stages where possible. Report the dimensions relevant to the task, including:

- task discrimination or semantic quality;
- probabilistic quality when outputs have a probability interpretation;
- abstention / selective risk when selective execution exists;
- hard negatives and boundary cases;
- invariance / robustness relevant to the interface;
- broad retention or non-regression obligations;
- latency, memory, throughput, tokens, compute, and cost when operationally material.

Preserve regressions. A scalar objective may rank treatments inside an experiment but must not erase failed retention, safety, authority, or semantic-validity gates.

## Qualified information accounting

Raw examples, tokens, steps, and FLOPs remain mandatory resource measurements, but they need not equal useful learning exposure.

A study may additionally report the count and composition of **qualified learning information** after accounting for evidence validity, independence, novelty/redundancy, boundary informativeness, and attribution quality.

Do not invent a universal weighting formula. Any numeric weighting must be preregistered, study-local, and reported beside raw counts until independently validated.

## Reward-driven and automated optimization

Supervised proper-scoring or equivalent matched controls should normally be the first comparison when trustworthy targets exist.

Reward-driven, trajectory-level, or reinforcement-style optimization becomes a research candidate only when:

- the reward/evaluator is independently qualified for the intended semantics;
- the signal has sufficient variation and coverage;
- the objective addresses a residual deficit not already answered by simpler matched controls;
- retention and regression gates are frozen;
- protected evaluation remains isolated.

An optimizer score is evidence, not authority. Automated training may nominate a treatment; it cannot weaken a failed gate, rewrite targets, change the protected basis, admit a model, or activate it.

## Relation to Governed Experimental Evolution

This reference determines whether parameter learning is the justified intervention and what residual experimental frontier remains.

Once a concrete intervention is nominated, route the experiment and change lifecycle through the existing Governed Experimental Evolution and evaluation owners rather than creating a separate training-governance lifecycle.

Conceptually:

```text
observation / deficit
  -> training intervention qualification
  -> bounded treatment or STOP
  -> experiment
  -> qualification
  -> admission
  -> activation
```

Keep each transition distinct.

## Specialization boundary

Projects may specialize this method with domain-specific contracts such as typed candidate frontiers, semantic closure, deterministic verifiers, regulated evidence lineage, domain-specific retention gates, or project-specific learning-unit economics.

Those objects remain owned by the project. Do not fold downstream semantic authority into Livingware's generic research methodology merely because the qualification workflow is reusable.
