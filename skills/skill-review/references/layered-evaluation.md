# Layered Evaluation

Use this reference when a skill, workflow, operator, or shared policy needs evaluation beyond a local correctness check. The canonical architecture lives in `../../../docs/skill-runtime-architecture.md`; this file owns evaluation questions, not runtime architecture.

## Evaluation order

Always answer these questions in order:

1. **What failed or changed?** Separate observed behavior from interpretation.
2. **Which layer owns the correction?** Attribute before proposing a patch.
3. **What is the smallest comparison that could falsify the proposed correction?**
4. **What evidence provenance supports the comparison?** Preserve `OBSERVED | REPLAYED | SIMULATED | INFERRED | ASSUMED`.
5. **What claim is justified?** Do not promote simulation or replay into observed evidence.

## Routing evaluation — fast cadence

Routing owns current-state selection: skill activation, branch choice, reference/tool choice, and stop/exit choice.

Evaluate:

- required-skill selection and missed activation;
- false activation and nearest-neighbor collision;
- branch choice after a material observation;
- unnecessary tool-family or reference activation;
- premature stop or failure to exit;
- route reversals caused by weak state discrimination;
- latency, uncached-input cost, tool-call count, and serial-turn amplification attributable to routing.

Prefer cheap positive/negative/collision scenarios and bounded trace replay. A routing failure does not authorize changing a correct tool contract.

## Workflow evaluation — medium cadence

Workflow owns reusable transition topology, recovery, convergence, handoff, and exit structure.

Evaluate:

- whether transition preconditions are explicit enough to distinguish states;
- convergence versus loops or oscillation;
- recovery after contradictory evidence;
- preservation of capability and correctness floors;
- whether downstream workflows are loaded only after their entry condition;
- handoff sufficiency: enough state to continue without carrying the entire prior skill body;
- whether a universal sequence has frozen a decision that should remain dynamic.

Use replay or seeded what-if simulation when it cheaply exposes dominated or looping topologies. Generalized workflow changes still require the admission rules in `budgeted-behavioral-learning.md`.

## Tool / operator evaluation — slow semantic evolution, immediate bug repair

Tools own invariant executable mechanics.

Evaluate:

- contract correctness;
- deterministic behavior where promised;
- input validation and failure handling;
- compatibility and versioned semantics;
- bounded output and latency;
- absence of hidden semantic policy inside a supposedly mechanical operator;
- focused regression coverage.

A confirmed correctness defect is fixed immediately under a regression test. New semantics or expanded capability are deliberate tool evolution and should not be smuggled in as a routing fix.

## Policy / invariant evaluation — slowest cadence

Policy owns stable cross-cutting constraints.

Evaluate:

- invariant preservation across representative workflows;
- bypass resistance;
- authority, admissibility, destructive-operation, evidence, and architecture consequences;
- unintended blocking or process ceremony introduced by the invariant;
- cross-workflow impact and rollback/recovery implications;
- whether a local workflow inconvenience is being mistaken for a policy defect.

Policy changes need explicit architecture/governance reasoning. A local optimization result is not enough.

## Counterfactual evaluation

Counterfactual evaluation is a comparison technique, not a fifth learning layer.

Allowed modes:

- `REPLAY`: deterministic recomputation from a frozen basis; output is `REPLAYED`.
- `MONTE_CARLO`: seeded what-if simulation over explicit transition/metric assumptions; output is `SIMULATED` and is not a causal-effect estimate.
- `REAL_REEXECUTION`: actual bounded execution of the alternate path using the real harness/fixture; output is `OBSERVED`.

For attribution, change one semantic layer at a time. Multi-layer alternatives are exploratory and cannot claim isolated layer effect without additional comparisons.

Simulation may rank alternatives, expose impossible paths, estimate cost, or identify assumption sensitivity. It cannot by itself satisfy materially independent observed evidence for generalized shared learning.

## Minimum evaluation report

For a substantial evaluation report only:

```text
Observed issue / change:
Failure class: CAPABILITY | STEERING | IMPLEMENTATION | ENVIRONMENT
Attributed layer: ROUTING | WORKFLOW | TOOL | POLICY | n/a
Comparison question:
Evidence provenance:
Result:
Claim scope:
Next owner/action:
```

Keep this report ephemeral unless a repository or user requirement needs a durable artifact. Git, tests, and existing evidence surfaces remain the normal record.
