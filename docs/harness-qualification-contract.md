# Harness Qualification Contract

**Status:** canonical generic contract  
**Version:** 1.0  
**Owner relationship:** specialization of `docs/livingware-evaluation-architecture.md`; host repositories may tighten thresholds but must not weaken hard invariants.

## Purpose

A harness is part of the effective decision system, not a passive transport layer. Changes to context construction, tools, memory, skill routing, control flow, provider/model policy, or workflow runtime can change behavior even when model weights and application code are unchanged.

```text
EffectiveSystem
=
Model
+ Routing
+ Workflow
+ Tool Surface
+ Policy
+ Context / Memory
+ Harness
+ Environment
```

Therefore:

> Component qualification does not imply composition qualification.

Qualification scope follows semantic impact, not file count or repository size.

## Impact categories

Every harness change declares one primary category and any secondary categories.

| Category | Meaning | Default gates |
|---|---|---|
| I0 | internal refactor; no observable semantic change | H0 + smoke H1 |
| I1 | presentation, UI, logging, telemetry only | H0 + targeted smoke |
| I2 | tool implementation change with stable schema/semantics | H0 + affected H1; H2 on drift |
| I3 | tool surface or skill-routing change | H0 + H1 + affected H2 |
| I4 | context, memory, session, retrieval, compression, pruning | H0 + H1 + affected H2 |
| I5 | retry, stop, delegation, branch/merge, orchestration | H0 + H1 + affected H2 |
| I6 | model-facing prompt/provider/decoding/scorer policy | H0 + H1 + H2 |
| I7 | cross-cutting I3-I6 change or attribution cannot be isolated | H0 + representative H1 + full relevant H2 |

Unknown impact defaults upward to the stricter plausible category.

## Harness identity

Every material qualification binds:

```yaml
harness_identity:
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

A model name alone is not a sufficient qualification identity.

## Impact vector

```yaml
harness_impact:
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

## H0 — Contract conformance

H0 is deterministic and cheap. It proves architectural invariants before behavioral measurement.

Check, where applicable:

- schema and tool-surface compatibility;
- routing/event-family parity;
- authority and policy boundaries;
- required governance or state-transition writes;
- replay and provenance shape;
- forbidden direct mutation/activation paths;
- deterministic structured-output contracts.

Default hard thresholds:

```text
schema conformance                   = 100%
required invariant/event coverage   = 100%
authority violations                = 0
forbidden execution/mutation paths  = 0
missing required provenance         = 0
replay-identity violations          = 0
```

Any hard-invariant violation is H0 FAIL. No averaging or compensating score is allowed.

## H1 — Behavioral invariance

H1 uses a frozen representative suite for affected surfaces. It measures whether the candidate harness changes effective behavior without running the entire expensive qualification population.

Representative cases should include positive, negative, boundary, hard-negative, abstention/UNKNOWN where meaningful, tool-mediated, and long-context cases where relevant.

Measure as applicable:

- final and typed decision agreement;
- routing/activation agreement;
- stop/retry/delegation behavior;
- tool selection and tool-call count;
- context/memory selection;
- calibration and selective-risk metrics;
- latency, tokens, retries, and other decision-economy costs;
- replay reproducibility and long-horizon context integrity.

Default thresholds, unless the host contract is stricter:

```text
hard invariant violations             = 0
critical-case decision agreement       = 100%
ordinary frozen-case agreement         >= 98%
task-success degradation               <= 2 percentage points
false forbidden-route/tool invocation  = 0 for P0 cases
Brier degradation                      <= 0.02 absolute
ECE degradation                        <= 0.02 absolute
NLL degradation                        <= 5%
median tool-call increase              <= 15%
median input-token increase            <= 15%
median wall-time increase              <= 20%
```

Economy drift above threshold may receive an explicit bounded waiver when correctness and hard invariants remain green; authority, replay, and forbidden-path failures are non-waivable.

H1 dispositions:

```text
PASS_INVARIANT
PASS_WITH_APPROVED_DRIFT
ESCALATE_H2
FAIL
```

## H2 — Qualification

H2 asks whether the new runtime composition is still qualified for the affected capability. It uses the host's current qualification population and acceptance contract rather than a generic repository-wide score.

H2 is mandatory for I4-I7 and for any lower category whose H1 exceeds threshold or produces unattributed behavioral drift.

H2 must preserve the target's existing decomposition. For example, structural routing and semantic discrimination must not be collapsed into one aggregate accuracy when they are distinct owners.

At minimum H2 fails on:

- any hard governance/policy/authority invariant failure;
- any required domain qualification gate failure;
- required robustness/invariance failure;
- calibration gate failure where calibration is contractual;
- replay-determinism failure;
- critical long-horizon context-integrity failure.

Improvements in one metric do not compensate for a P0 regression.

## Cross-harness invariance

For material model-facing changes, compare at least two semantically equivalent harness presentations when feasible:

```text
minimal/direct
typed/structured
tool-mediated
compressed-context
```

The case meaning and admissible evidence basis stay fixed. Additional evidence may justify a different answer only when the contract explicitly permits it.

Default cross-harness thresholds:

```text
critical cases final-decision agreement = 100%
ordinary cases final-decision agreement >= 98%
```

Differences that arise only from wording, formatting, or harmless trace shape are not semantic regressions.

## Qualification record

```yaml
harness_qualification:
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

## Learning and mutation boundary

Harness qualification measures a composition. It does not authorize arbitrary mutation of every participating component.

If a regression is observed:

```text
observe
-> attribute
-> identify smallest durable owner
-> produce RegressionWitness
-> only then propose a LearningCandidate
```

Use `HARNESS_INDUCED_FAILURE` when the failure is caused by composition/interface interaction and cannot be reduced to an already-supported ROUTING, WORKFLOW, TOOL/CAPABILITY, POLICY, IMPLEMENTATION, or ENVIRONMENT owner.

## Core laws

1. Harness version is part of decision provenance.
2. Model weights alone do not define a qualified agentic system.
3. Model-visible context or control-flow changes are semantic-impact changes until proved otherwise.
4. Regression measures decision invariants, not exact prose.
5. Qualification scope follows semantic impact.
6. Authority, replay, and forbidden-path failures are non-compensable.
7. Efficiency is evaluated only after correctness and admissibility.
8. A previously qualified combination remains the baseline until its replacement qualifies.
9. No harness update may silently change qualified behavior without evidence.
10. Component qualification does not imply composition qualification.
