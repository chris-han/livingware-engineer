# Livingware Skill Runtime Architecture

**Status:** accepted implementation basis  
**Date:** 2026-09-15

## Purpose

Livingware Engineer treats a skill as a discoverable entry into a reusable, context-conditioned workflow rather than as a monolithic prompt bundle. Stable executable behavior belongs in tools/operators; stable cross-cutting constraints belong in policy; reusable state transitions belong in workflows; context-dependent choice belongs in routing. Evaluation and learning are attributed to the layer that owns the failure and proceed at different cadences.

This architecture preserves native harness skill discovery, progressive disclosure, token-economics discipline, and explicit human authorization for generalized behavioral learning. It does not introduce a mandatory meta-router, a new orchestration runtime, or an autonomous self-improvement loop.

## Historical lineage

The design deliberately echoes workflow management and process mining:

```text
workflow/BPM
  -> process as executable structure
process mining
  -> actual execution as observable traces
adaptive process management
  -> observed behavior informs future process design
agentic workflows
  -> model selects actions dynamically
Livingware
  -> dynamic routing + invariant operators + layer-specific eval/learning
```

The inherited principle is that the path through a system is itself an observable object. The difference is that an agentic system contains software intelligence between activity nodes, so "the process" must be decomposed into distinct owners rather than represented as one fixed process model.

## Canonical layers

### Tool / Operator

An operator is invariant executable capability. Its semantics should be deterministic or mechanically testable enough that repeated natural-language interpretation is unnecessary.

Examples include repository inspection primitives, version synchronization, a polluter-finding script, a schema validator, or a token-usage analyzer.

The authoritative owner is executable code plus focused tests. A workflow decides when to invoke an operator; it does not restate how the operator works.

Do not create scripts merely for architectural symmetry. Promote behavior into an operator only when it is reusable and mechanical and the executable form is cheaper or more reliable than repeated agent interpretation.

### Policy / Invariant

Policy contains stable constraints that remain true across workflows and cannot simply become executable operators: authority, destructive-operation boundaries, architecture laws, evidence requirements, and similar cross-cutting rules.

Policy constrains routing, workflows, and operators but does not perform ordinary task routing. Keep one authoritative owner and point to it rather than duplicating the rule across skills.

### Workflow

A workflow is reusable state-transition structure. It defines admissible states, transition conditions, evidence required to leave a state, recovery paths, and exit/handoff conditions.

A workflow should express structure such as:

```text
observation
  -> localize uncertainty
  -> choose next distinguishing action
  -> observe result
  -> route again
  -> exit or recover
```

It should not encode every possible command, platform mechanic, or tool implementation.

### Router

Routing is dynamic, context-conditioned choice. Native harness matching owns first-hop skill discovery where the harness already supports it. After entry, routing is recurrent: every meaningful observation can change the next workflow state, operator, reference, or exit decision.

```text
current state + current evidence
        -> route
        -> operator/reference/transition
        -> observation
        -> route again
```

A host with native skill matching must not be wrapped in a second mandatory meta-router merely to reproduce discovery capability.

### Skill

A skill is the user-facing discovery and workflow-entry package. A root `SKILL.md` normally owns only:

- a discriminating activation description;
- the entry/exit lifecycle needed whenever selected;
- hard local invariants that must remain visible;
- the smallest sufficient workflow contract; and
- progressive-disclosure pointers to workflow/reference/operator owners.

Reference knowledge remains reference knowledge. Deterministic mechanics remain executable owners. A skill does not become authoritative merely because it mentions them.

## Placement rule

When adding or moving guidance, decide ownership in this order:

```text
Can the behavior be enforced deterministically and reused?
  YES -> tool/script/test
  NO  -> does it constrain most executions regardless of context?
          YES -> policy/invariant
          NO  -> is it reusable transition/recovery structure?
                  YES -> workflow
                  NO  -> dynamic routing or conditional reference
```

## Execution trace model

Livingware does not require a new persistent trace database, but evaluation should reason about executions using a common conceptual shape:

```text
Episode
  task/context basis
  -> state_0
  -> routing decision_0
  -> operator/reference/transition_0
  -> observation_0
  -> state_1
  -> ...
  -> exit/outcome
```

When available, an evaluation should preserve or reconstruct enough identity to compare alternatives: task/fixture identity, relevant repository state, model/harness version, selected skill/workflow version, operator versions, routing decision point, observations, outcome, latency, token counts, and tool-call counts.

This is an evaluation model, not a requirement to create a new always-on telemetry ledger.

## Failure attribution

Classify the observed problem before changing the framework:

```text
Observed failure
  +-- IMPLEMENTATION -> product/code owner
  +-- ENVIRONMENT    -> fixture/runtime/config owner
  +-- CAPABILITY     -> tool/operator owner
  +-- STEERING
        +-- ROUTING  -> selection/branch/stop owner
        +-- WORKFLOW -> topology/transition/recovery owner
        +-- POLICY   -> cross-cutting invariant owner
```

Rules:

- a routing failure does not authorize a tool change;
- a correct tool should not be mutated because the router chose it badly;
- a workflow loop is not repaired by making skill activation broader;
- a local inconvenience does not justify a policy change;
- a confirmed deterministic operator bug is fixed immediately through its regression contract;
- generalized steering changes remain subject to the behavioral-learning admission rules.

> **Learning authority follows failure attribution. Change the smallest owning layer that explains the evidence.**

## Four evaluation and learning cadences

Cadence describes how readily a layer may be evaluated and revised when evidence exists. It does not create a schedule or autonomous mutation loop.

### Routing clock — fast

Evaluate selection, false/missed activation, collision, branch choice, stop choice, unnecessary tool-family activation, latency, and token cost. Cheap targeted routing evals are appropriate whenever routing behavior materially changes.

### Workflow clock — medium

Evaluate transition quality, convergence, recovery, looping, handoff, and capability-floor preservation. Generalized topology changes require repeated materially independent steering evidence or an explicit architecture change.

### Tool clock — slow semantic evolution; immediate correctness repair

Evaluate contract correctness, determinism, compatibility, failure handling, output bounds, and performance. New semantics or expanded capability are versioned and deliberately admitted. A proven correctness defect does not wait for the slower learning cadence.

### Policy clock — slowest

Evaluate invariant preservation, bypass resistance, authority/admissibility consequences, and cross-workflow effects. Policy changes require explicit architecture/governance reasoning because their impact radius is broad.

```text
routing adaptation frequency
  > workflow evolution frequency
  > tool semantic evolution frequency
  > policy evolution frequency
```

## Counterfactual / what-if evaluation

Process simulation is useful because it asks not only "what happened?" but "what could have happened under a different process choice?" Livingware supports this as an evaluation technique while keeping synthetic evidence distinct from observed evidence.

### Evidence provenance

Every result used in a counterfactual comparison must be classifiable as one of:

- `OBSERVED` — produced by a real execution against the declared fixture/environment;
- `REPLAYED` — deterministically recomputed from frozen observed inputs and deterministic operators;
- `SIMULATED` — generated by an explicit transition/probability model;
- `INFERRED` — estimated by a model or analytical approximation rather than directly generated by the system under test;
- `ASSUMED` — supplied as a scenario parameter without empirical support in the current comparison basis.

Never relabel `REPLAYED`, `SIMULATED`, `INFERRED`, or `ASSUMED` output as an observed episode.

### Intervention contract

A counterfactual comparison must name:

```text
layer: ROUTING | WORKFLOW | TOOL | POLICY
decision_point: exact branch/state being changed
original_choice: actual or baseline choice
alternate_choice: candidate choice
frozen_basis:
  task/fixture identity
  repository/input state
  relevant workflow/policy versions
  operator versions
  model/harness/config pins where material
mode: REPLAY | MONTE_CARLO | REAL_REEXECUTION
seed: required for stochastic simulation
rollouts: required for Monte Carlo
metric_provenance: OBSERVED | REPLAYED | SIMULATED | INFERRED | ASSUMED
```

A comparison that changes multiple semantic layers simultaneously cannot claim attribution to one layer unless separate evidence isolates their effects.

### Supported modes

#### REPLAY

Use when the alternative path can be recomputed from a frozen basis and deterministic operator outputs. Replay is useful for path cost, deterministic contract behavior, and transition consistency. It is not new empirical generalization evidence.

#### REAL_REEXECUTION

Run the alternate route/workflow against the same bounded fixture or other deliberately comparable environment. This is an experiment, not simulation; its outputs are `OBSERVED`. It is the preferred way to validate a promising simulated alternative when practical.

#### MONTE_CARLO

Use seeded zero-dependency simulation when branch outcomes, latency, token cost, retries, or failures are represented by explicit empirical or assumed distributions. The simulator must preserve provenance for every distribution and report empirical-supported and assumption-driven metrics separately.

Monte Carlo can estimate sensitivity and rank candidate alternatives. It must not make causal claims merely because one simulated branch has a better expected value.

### Causal counterfactuals are not part of the current MVL

A statement such as "route B would have caused success for the same episode" requires explicit causal assumptions or a structural causal model. Ordinary LLM generation, replay, or Monte Carlo over correlations is insufficient. The current implementation may use the term **what-if simulation** or **counterfactual evaluation**, but it must not claim identified causal effects.

## Simulation admission boundary

Simulation narrows search; reality remains the judge.

```text
observed problem
  -> attributed layer
  -> candidate alternative
  -> replay / simulation for prioritization or falsification
  -> real bounded re-execution when practical
  -> matched behavioral eval
  -> materially independent observed eval for generalized learning
  -> human-authorized retain / reject
```

Simulation results may:

- expose impossible or dominated workflow alternatives;
- estimate token/latency/tool-call consequences;
- rank candidate routing/workflow changes;
- identify sensitivity to assumptions; and
- guide which real eval is worth paying for.

Simulation results may not by themselves:

- satisfy the materially independent empirical case required for generalized behavioral learning;
- authorize a policy or tool semantic mutation;
- turn prediction confidence into correctness or authority; or
- bypass normal verification of the real execution path.

## Token economics

The process path is part of cost. Evaluate at least:

```text
static context
+ selected workflow context
+ conditional references
+ tool schemas
+ tool request/response payloads
+ serial model turns
+ reasoning/output tokens
+ retries and reruns
```

For what-if simulation, also include simulation cost itself. Do not spend more tokens or runtime exploring counterfactuals than the uncertainty or prospective saving justifies. Prefer cheap replay first, then bounded Monte Carlo, then real re-execution for alternatives that remain plausible.

## Implementation invariants

1. Native harness matching remains first-hop discovery where available.
2. No mandatory meta-router is introduced.
3. No new durable learning/simulation database is introduced for this refactor.
4. Routing, workflow, tool, and policy evals remain separately attributable.
5. Simulation provenance is mechanically visible in test/eval output.
6. Simulation cannot count as independent observed evidence for generalized learning.
7. Behavioral learning remains explicitly human-initiated under the existing budgeted-learning contract.
8. Causal claims are forbidden unless a future design introduces and validates explicit causal identification semantics.
