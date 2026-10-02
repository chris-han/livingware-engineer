# Livingware Evaluation Architecture

**Status:** proposed implementation basis  
**Date:** 2026-09-23  
**Architecture owner relationship:** complements `docs/skill-runtime-architecture.md`; does not replace it

## Purpose

Livingware evaluation is the discipline for discovering, measuring, qualifying, and learning from failures in agentic software systems whose behavior can change through routing, workflows, tools/operators, policy, context, and model behavior.

The system under evaluation is not only a final LLM response. It is an execution path:

```text
task/context
  -> routing
  -> skill/workflow
  -> tool/operator actions
  -> observations
  -> outcome
  -> evidence
```

Evaluation therefore asks not only whether an outcome was good, but whether the system selected the right capability, followed an appropriate path, respected invariants, produced sufficient evidence, and attributed any failure to the smallest durable owner.

This document adds an evaluation layer to the accepted runtime architecture. It does not create a second runtime, mandatory meta-router, persistent telemetry service, or autonomous self-improvement loop.

## Core invariants

### 1. Observation precedes taxonomy when the failure space is not yet known

Do not begin with a generic failure taxonomy merely because familiar labels exist. Start from representative traces and free-form expert observations, then induce candidate failure modes from evidence.

```text
ObservedTrace
  -> FailureObservation
  -> FailureModeCandidate
  -> qualification
  -> reusable failure mode
```

A candidate taxonomy is a learning artifact, not authority.

### 2. Evaluator output is measurement evidence, not behavioral authority

An evaluator may detect regressions, measure behavior, estimate prevalence, or generate learning observations. It may not by itself redefine routing semantics, mutate a workflow, expand tool capability, change policy, or authorize promotion.

```text
evaluator verdict != runtime authority
```

Any behavioral change still follows failure attribution, the smallest durable owner, and the repository's existing admission rules.

### 3. Deterministic evaluation first

If a claim can be decided mechanically, use code, schema validation, execution tests, parsers, exact comparisons, or other deterministic operators.

Use interpreted evaluation only when the claim genuinely requires semantic judgment. Hybrid evaluators may compose exact and interpreted predicates, but each component must retain its own provenance.

### 4. Evaluation claims must be bounded

Each evaluator should decide one explicit claim or one bounded typed frontier. Avoid holistic evaluators such as "is this trace good?"

The default atomic frontier is:

```text
PASS | FAIL | UNKNOWN | NOT_APPLICABLE
```

A domain-specific bounded frontier may replace it when the task semantics require multiple mutually distinguishable choices.

### 5. Evidence provenance is mandatory

Reuse the accepted provenance model from `docs/skill-runtime-architecture.md`:

```text
OBSERVED | REPLAYED | SIMULATED | INFERRED | ASSUMED
```

Generated, replayed, simulated, or inferred evidence must never be silently promoted to observed evidence.

### 6. Learning authority follows failure attribution

Evaluation discovers and measures; attribution determines what may change.

```text
Observed failure
  +-- IMPLEMENTATION -> product/code owner
  +-- ENVIRONMENT    -> fixture/runtime/config owner
  +-- CAPABILITY     -> tool/operator owner
  +-- STEERING
        +-- ROUTING
        +-- WORKFLOW
        +-- POLICY
```

A routing failure does not authorize a tool mutation. A workflow topology failure does not justify broader skill activation. A local inconvenience does not justify policy change.

### 7. Synthetic cases repair coverage; they do not manufacture evidence

Synthetic generation is used to fill known coverage gaps, construct hard negatives, or exercise rare combinations. The useful unit is not dataset size but qualified coverage of the declared evaluation space.

```text
coverage model
  -> uncovered cell
  -> synthetic candidate case
  -> execute real system
  -> verify intended condition
  -> admit as an eval case
```

The generated prompt/scenario remains synthetic provenance even when its resulting execution is observed.

### 8. Evaluation itself is versioned and re-qualified

Failure modes, evaluator prompts/models, deterministic checks, fixtures, and thresholds can become stale as the runtime changes. Re-qualify interpreted evaluators and re-run failure discovery after material changes to routing, workflows, tools, policy, model/provider, or task distribution.

No evaluator is assumed permanently valid.

## Canonical evaluation flow

```text
EvaluationTarget
      |
      v
EvalCase / observed episode
      |
      v
ObservedTrace
      |
      +--------------------------+
      | known failure claim?     |
      |                          |
      no                         yes
      |                          |
      v                          v
Failure discovery          EvaluatorCandidate
      |                          |
      v                          v
FailureModeCandidate     EvaluatorQualification
      |                          |
      +-----------+--------------+
                  |
                  v
           bounded verdict
                  |
                  v
          FailureAttribution
                  |
                  v
           LearningCandidate
                  |
                  v
      retain / revise / reject
```

## Livingware Eval IR

The Eval IR is a conceptual contract. It does not require a new persistent database or service. JSON, Markdown, fixtures, existing traces, or test code may instantiate it.

### `EvaluationTarget`

Identifies what is being evaluated.

```yaml
target_id: string
target_kind: ROUTING | WORKFLOW | TOOL | POLICY | SKILL_RUNTIME | HARNESS_COMPOSITION | OUTCOME | EVIDENCE
version_pins:
  repository: optional
  skill: optional
  workflow: optional
  operator: optional
  policy: optional
  model_or_harness: optional
```

`OUTCOME` and `EVIDENCE` are evaluation surfaces, not learning owners. Any failure found there must still be attributed to an owning layer.

### `EvalCase`

A bounded scenario with enough context to make a claim reproducible.

```yaml
case_id: string
target_id: string
task_or_fixture_identity: string
input_basis: object
expected_claims:
  - claim_id
provenance: OBSERVED | REPLAYED | SIMULATED | INFERRED | ASSUMED
source_parent: optional
coverage_dimensions: optional
```

### `ObservedTrace`

Reuses the runtime episode model and preserves enough evidence to reconstruct decisions.

```yaml
case_id: string
episode_id: string
state_transitions: [...]
routing_decisions: [...]
actions: [...]
observations: [...]
outcome: object
evidence: [...]
runtime_pins: object
cost:
  latency: optional
  tokens: optional
  tool_calls: optional
```

### `EvaluationClaim`

The smallest semantic assertion the evaluator decides.

```yaml
claim_id: string
description: string
evaluator_kind: DETERMINISTIC | INTERPRETED | HYBRID
frontier:
  - PASS
  - FAIL
  - UNKNOWN
  - NOT_APPLICABLE
required_inputs: [...]
```

### `FailureObservation`

A local observation recorded before root-cause or taxonomy commitment.

```yaml
observation_id: string
case_id: string
evidence_span_or_step: optional
note: string
observer: HUMAN | AGENT | DETERMINISTIC_CHECK
provenance: OBSERVED | REPLAYED | SIMULATED | INFERRED | ASSUMED
```

### `FailureModeCandidate`

A proposed reusable pattern supported by multiple observations.

```yaml
mode_id: string
name: string
definition: string
supporting_observations: [...]
counterexamples: [...]
coverage_status: DISCOVERY | PARTIAL | SATURATED
status: CANDIDATE | QUALIFIED | REJECTED
```

A failure mode must not be created solely to preserve an existing evaluator.

### `FailureAttribution`

Connects observed behavior to the smallest durable owner.

```yaml
attribution_id: string
case_id: string
owner:
  kind: IMPLEMENTATION | ENVIRONMENT | CAPABILITY | ROUTING | WORKFLOW | POLICY
  identity: string
basis: [...]
confidence_or_uncertainty: optional
status: PROPOSED | QUALIFIED
```

### `EvaluatorCandidate`

Defines how one claim is measured.

```yaml
evaluator_id: string
claim_id: string
kind: DETERMINISTIC | INTERPRETED | HYBRID
implementation_or_prompt_ref: string
version_pins: object
required_inputs: [...]
frontier: [...]
status: CANDIDATE | QUALIFIED | RETIRED
```

### `EvaluatorQualification`

Evidence that an evaluator is fit for a declared use.

For deterministic evaluators, qualification normally consists of focused positive/negative fixtures, hard negatives, reproducibility, and contract tests.

For interpreted evaluators, qualification should normally include disjoint development and held-out data, disagreement inspection, confusion-matrix measures such as TPR/TNR for binary claims, and calibration/selective-risk measures when probabilities or abstention are exposed.

```yaml
qualification_id: string
evaluator_id: string
dataset_or_fixture_ref: string
split_contract: optional
metrics: object
hard_negatives: [...]
invariance_checks: [...]
limitations: [...]
disposition: QUALIFIED | QUALIFIED_BOUNDED | NOT_QUALIFIED
```

There is no repository-wide universal TPR/TNR threshold. Qualification gates must be explicit and proportional to the risk and intended use of the evaluator.

### `RegressionWitness`

A durable case that prevents a qualified failure mode from silently returning.

```yaml
witness_id: string
mode_id: string
case_ref: string
expected_claim: string
owner: string
provenance: string
```

### `LearningCandidate`

A proposed behavioral change produced only after attribution.

```yaml
candidate_id: string
attribution_ref: string
owner_layer: ROUTING | WORKFLOW | TOOL | POLICY
proposed_delta: string
supporting_evidence: [...]
counterfactual_evidence: optional
admission_status: PROPOSED | QUALIFIED | REJECTED
```

A learning candidate is never auto-applied merely because an evaluator reports `FAIL`.

## Harness Qualification

Harness/runtime composition is a first-class evaluation target. A change to context construction, memory, tool surface, skill routing, control flow, provider/model policy, or workflow runtime can alter effective behavior even when individual components remain locally qualified.

The canonical impact categories, H0/H1/H2 gates, default thresholds, waiver rules, and qualification identity are defined in [Harness Qualification Contract](harness-qualification-contract.md).

The Eval IR adds three composition-level records:

### `HarnessIdentity`

```yaml
harness_version: string
routing_version: string | null
workflow_version: string | null
tool_surface_version: string | null
context_policy_version: string | null
memory_policy_version: string | null
provider_policy_version: string | null
model_id: string | null
model_revision: string | null
environment_version: string | null
```

### `HarnessImpact`

```yaml
category: I0 | I1 | I2 | I3 | I4 | I5 | I6 | I7
context_changed: boolean
tools_changed: boolean
tool_schema_changed: boolean
memory_changed: boolean
skills_changed: boolean
routing_changed: boolean
control_flow_changed: boolean
provider_or_model_policy_changed: boolean
workflow_runtime_changed: boolean
authority_surface_changed: boolean
replay_shape_changed: boolean
reasons: []
```

### `HarnessQualification`

```yaml
qualification_id: string
baseline_identity: HarnessIdentity
candidate_identity: HarnessIdentity
impact: HarnessImpact
required_gates: [H0, H1, H2]
suite_refs: []
metrics: {}
disagreements: []
provenance_refs: []
disposition: QUALIFIED | QUALIFIED_WITH_WAIVER | NOT_QUALIFIED | BLOCKED_PENDING_H2
waiver_ref: string | null
```

Harness qualification measures a composition but does not become a new learning owner. A failure should still be attributed to the smallest durable ROUTING, WORKFLOW, TOOL/CAPABILITY, POLICY, IMPLEMENTATION, or ENVIRONMENT owner when evidence supports that reduction. Use `HARNESS_INDUCED_FAILURE` only for composition/interface failures that cannot yet be reduced safely.

> Component qualification does not imply composition qualification.

## Failure discovery loop

When the failure taxonomy is immature, alternate breadth and depth.

```text
Breadth
  sample diverse traces
  include random exploration
  find new failure observations

Depth
  refine one candidate failure mode
  scan reviewed + unreviewed traces
  propose additional instances
  seek counterexamples / hard negatives
```

Agent-suggested instances are proposals. Human/domain review or deterministic qualification remains required before those suggestions become ground truth.

Criteria drift is expected: as reviewers learn the domain, earlier traces may need re-review.

## Coverage-directed eval case generation

Define the smallest useful coverage model for the target. Example dimensions may include:

```text
task class
x ambiguity
x risk
x environment state
x tool availability
x prior state
x expected routing
```

Prefer real observed cases when they already cover the cell. Generate synthetic candidates only for missing or weakly represented regions.

Separate scenario construction from surface realization:

```text
coverage tuple
  -> validate tuple realism
  -> render task/input
  -> execute through real pipeline
  -> inspect trace
```

Do not mix source-parent relatives across held-out splits when that would leak nearly identical cases.

## Evaluator qualification

### Deterministic evaluator

Required evidence should normally include:

- positive fixtures;
- negative fixtures;
- at least one hard negative for important boundaries;
- deterministic repeatability;
- version-pinned contract tests; and
- explicit `UNKNOWN` behavior when required evidence is unavailable.

### Interpreted evaluator

Use domain-grounded labels and keep prompt/examples disjoint from held-out measurement.

A typical lifecycle is:

```text
human/domain labels
  -> train examples for prompt or scorer shaping
  -> dev set for iteration
  -> held-out test for final qualification
```

For binary claims, record the full confusion matrix and at least TPR/TNR. For typed frontiers, record per-class behavior and candidate-order/permutation invariance where order could leak semantics. For probabilistic outputs, add calibration and selective-risk measures.

Run the held-out qualification under pinned evaluator/model versions. A materially changed prompt, model, frontier, or evidence contract creates a new evaluator version.

## Skill family

The evaluation architecture is exposed through seven discoverable skills:

- `evaluating-livingware` — entry/router for substantial Livingware evaluation work;
- `discovering-failures` — evidence-first error discovery and failure-mode induction;
- `designing-evaluators` — deterministic/interpreted/hybrid evaluator design;
- `qualifying-evaluators` — evaluator validation and bounded qualification;
- `generating-eval-cases` — coverage-directed case generation;
- `evaluating-skill-runtime` — behavior evaluation of skill trigger/routing/workflow/actions/evidence/exit contracts, including cross-harness invariance when the runtime surface changes.
- `governed-experimental-evolution` — bounded DEV/QUAL/CONFIRM evolution after failure attribution.

These are workflow-entry packages, not new authority owners.

## Boundary with existing repository owners

### `skill-review`

`skill-review` audits instruction surfaces: activation noise, layer mixing, progressive disclosure, token/tool-loop cost, unsupported scaffolding, and ownership placement.

`evaluating-skill-runtime` evaluates observed or reproducible behavior of a skill execution.

```text
instruction architecture audit -> skill-review
runtime behavior eval         -> evaluating-skill-runtime
```

### `verification-before-completion`

Completion verification proves a declared implementation/task/feature claim for the current work. It is not a generalized evaluator-design or failure-taxonomy workflow.

### Counterfactual evaluation

The accepted counterfactual model in `docs/skill-runtime-architecture.md` remains authoritative. The evaluation skills may invoke replay, real re-execution, or Monte Carlo after a layer and decision point are declared; they do not redefine those semantics.

### TDD and repository tests

TDD remains the implementation workflow for changed local behavior. Eval skills may generate regression witnesses that become tests, but they do not replace RED -> GREEN -> REFACTOR.

## Non-goals

This architecture does not introduce:

- a persistent evaluation database;
- an always-on annotation service;
- an automatic self-improvement daemon;
- a mandatory meta-router;
- a second counterfactual engine;
- automatic skill/policy/tool mutation from evaluator output;
- one universal quality score;
- one universal evaluator threshold;
- foundation-model benchmarking as a repository concern.

## Acceptance criteria for v1

The first implementation is complete when:

1. the six skills exist with discriminating descriptions and progressive disclosure to this document;
2. repository tests prove their metadata and key non-authority/provenance contracts;
3. `skill-review` remains the instruction-surface owner and is not duplicated;
4. existing counterfactual provenance semantics remain unchanged;
5. at least one existing skill runtime fixture can be represented as the Eval IR without a new service or database; and
6. README documentation makes the evaluation skill family discoverable without turning it into always-loaded process.


## Governed Experimental Evolution

Governed Experimental Evolution (GEE) controls how evaluation evidence may produce experimental changes without turning a hillclimber, evaluator, or benchmark into behavioral authority.

The governing invariant is:

```text
improvement = evidence
improvement != authority
```

The lifecycle is:

```text
Observation
  -> typed failure attribution
  -> hypothesis
  -> InterventionCandidate
  -> DEV
  -> QUAL
  -> admit/reject working baseline
  -> architecture freeze
  -> sealed CONFIRM
  -> confirmed / not confirmed
```

### DEV / QUAL / CONFIRM

**DEV** is discovery-only. Historically exposed, generated, mined, counterexample, hard-negative, and permitted production-derived cases may be used repeatedly. DEV improvement is candidate evidence, not qualification.

**QUAL** is development qualification. It tests whether a DEV-discovered intervention survives the current contract, regressions, invariance checks, calibration requirements, and other declared gates. Because QUAL may be consulted repeatedly during development, QUAL evidence is not sealed confirmatory evidence.

**CONFIRM** is sealed confirmation. Before CONFIRM, freeze the model, prompt, representation, scorer, frontier semantics, evaluator contract, acceptance thresholds, code/runtime pins, and confirmation manifest. CONFIRM cases and reference labels must not participate in intervention selection, prompt/scorer shaping, threshold tuning, model selection, or failure-taxonomy construction.

A CONFIRM failure closes that confirmation run. Reopening development makes the used confirmation population historically exposed; a later confirmatory claim requires a new independent confirmation campaign. Do not patch against a failed CONFIRM population and continue calling it sealed.

### Typed experimental failure classes

Use the smallest supported class and preserve alternatives when attribution is uncertain:

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

These classes complement the durable owner attribution in `FailureAttribution`. The typed class explains what failed experimentally; owner attribution still determines what repository/runtime surface may change.

`MODEL_CAPACITY_FAILURE` is admissible only after materially plausible structural, projection, frontier, scorer/protocol, calibration, robustness, reference, and infrastructure explanations have been evaluated. A bad score alone is not evidence that a larger model is required.

`EVALUATION_DESIGN_FAILURE` invalidates the measurement claim rather than becoming a target-system failure.

### Intervention lineage

Every retained or rejected intervention preserves:

```yaml
intervention:
  intervention_id: string
  parent_baseline_id: string
  hypothesis:
    target_failure_class: string
    causal_claim: string
    expected_metric_effect: string
  mutation:
    authority_class: M0 | M1 | M2 | M3
    surface: string
    before_hash: string
    after_hash: string
    diff_hash: string
  evaluation:
    dev_run_refs: []
    qual_run_refs: []
  effect:
    primary_metric_delta: optional
    secondary_metric_deltas: optional
    uncertainty: optional
    regressions: []
  disposition: RETAIN | REVERT | INCONCLUSIVE | INVALID_EXPERIMENT | INVALID_EVAL
```

Default to one attributable intervention per round. Composite interventions are allowed only when components cannot meaningfully be isolated and must declare weaker attribution. Negative and reverted trials remain durable evidence. Historical experimental truth is append-oriented: corrections supersede rather than rewrite prior runs.

### Authority-bounded mutation surfaces

- **M0 — automatically mutable in DEV:** low-authority experimental knobs such as prompt wording/order, non-semantic formatting, runtime effort, and batch parameters.
- **M1 — experiment mutable:** representation/projection mechanics, context contraction, scorer/readout protocol, calibration method, and model choice. These require QUAL before working-baseline admission.
- **M2 — governed semantic surface:** predicate/frontier semantics, `UNKNOWN` meaning, structural admissibility, authority/precedence semantics, ontology primitives, and acceptance-policy semantics. An optimizer may propose a candidate but must not autonomously activate it.
- **M3 — sealed experimental authority:** CONFIRM corpus/reference labels, frozen acceptance thresholds/protocol, historical run records, and manifest hashes. Mutation invalidates the campaign.

The candidate under optimization must not control the basis that judges its own admission.

### Admission gate

```text
DEV_PASS
AND QUAL_PASS
AND NO_HARD_REGRESSION
AND ATTRIBUTION_SUPPORTED
AND MUTATION_AUTHORITY_VALID
```

Score improvement alone is insufficient. Evaluator qualification and intervention qualification remain distinct: `qualifying-evaluators` establishes measurement fitness; GEE governs whether a change survives DEV/QUAL and may enter a frozen confirmation campaign.

### Replay identity

Material GEE runs should pin repository/code identity, model/tokenizer identity where relevant, prompt/representation/projection/scorer versions, dataset/reference manifest hashes, acceptance-policy hash, runtime environment, and seed policy. A result without sufficient pins may remain diagnostic evidence but must not silently become qualification or confirmation evidence.

## Qualified Change Lifecycle Handoff

Evaluation produces measurement and attribution evidence. When attributed evidence is used to change the system, the subsequent lifecycle is owned by [Livingware Qualified Change Lifecycle](livingware-change-lifecycle.md).

```text
FailureAttribution / LearningCandidate
  -> ChangeHypothesis
  -> ExperimentCandidate
  -> ScientificResult
  -> QualificationResult
  -> ChangeCandidate
  -> external admission / shadow / activation authority
```

Evaluation does not gain admission or activation authority through this handoff. Training-data admission, experiment selection, multi-seed qualification, rollback, and the `NO_CHANGE` disposition are defined by the qualified-change lifecycle and operationalized by `governed-experimental-evolution`.

