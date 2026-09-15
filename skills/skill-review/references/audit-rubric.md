# Audit Rubric

Score each dimension from 0 to 2, where `0 = healthy`, `1 = review`, and `2 = clear refactor target`.

The canonical ownership model is defined in `../../../docs/skill-runtime-architecture.md`. This rubric evaluates conformance to that model; it does not redefine it.

## Skill dimensions

### 1. Discovery precision
- 0: short, discriminating description with an obvious current-state trigger.
- 1: somewhat broad or keyword-heavy.
- 2: claims a large task class, overlaps several neighboring states, or has strong “pick me” phrasing.

### 2. Progressive disclosure
- 0: root `SKILL.md` contains only guidance normally needed after activation.
- 1: some conditional detail is loaded eagerly.
- 2: root contains multiple long workflows, exhaustive references, examples, schemas, or tool catalogs that apply only sometimes.

### 3. Prescription cost
- 0: instructions focus on outcomes, invariants, and genuinely order-sensitive transitions.
- 1: some unnecessary sequencing or recipe-like behavior.
- 2: a fixed itinerary is imposed where context-conditioned routing should choose the next action.

### 4. Boundary quality
- 0: real safety, authority, destructive, or correctness boundaries are clear and proportionate.
- 1: some boundaries are stronger than their consequences justify.
- 2: frequent approval gates or stop rules compensate for historical model behavior rather than current workflow risk.

### 5. Single-model optimization
- 0: core guidance is model-neutral; model-specific compensation is isolated and scoped.
- 1: some instructions assume one model's strengths/weaknesses but remain mostly portable.
- 2: the main workflow depends on behavior unique to one model or release.

### 6. Multi-model compatibility
- 0: intent, invariants, outputs, and boundaries transfer across supported models.
- 1: some supported models may be over- or under-constrained.
- 2: guidance that helps one supported model likely materially hinders another.

### 7. Evidence for extra scaffolding
- 0: extra scaffolding is tied to observed failures, tests, safety requirements, platform limitations, or documented model behavior.
- 1: rationale is plausible but weakly evidenced or stale.
- 2: scaffolding appears historical, speculative, or duplicated with normal model capability.

Do not penalize detail merely for being detailed. Penalize unsupported universal scaffolding.

### 8. Adapter isolation
- 0: platform/model-specific mappings and compensations live in adapters or conditional references.
- 1: some adapter-specific detail remains in shared guidance.
- 2: shared `SKILL.md` is substantially occupied by isolatable platform/model rules.

### 9. Duplication and collision
- 0: responsibilities are distinct and not restated elsewhere.
- 1: mild duplication.
- 2: substantial overlap with another skill or `AGENTS.md`, creating conflicting or duplicate authority.

### 10. Tool ownership
Ask whether deterministic capability is incorrectly encoded as repeated prose.
- 0: mechanical behavior is owned by script/tool/code plus focused tests; skill only decides when it is relevant.
- 1: some executable semantics are repeated in prose.
- 2: the skill repeatedly asks the model to interpret deterministic mechanics that should have one executable owner.

### 11. Routing versus workflow separation
Ask whether dynamic choice is incorrectly frozen into universal sequence.
- 0: workflow defines admissible transitions and routing chooses by current evidence.
- 1: some branches are unnecessarily hard-coded.
- 2: the skill prescribes one path despite materially different states/observations.

### 12. Policy ownership
Ask whether cross-cutting policy is duplicated inside the skill.
- 0: shared invariants have one canonical owner and are referenced compactly.
- 1: some policy text is repeated.
- 2: skill-local copies could diverge from repository/architecture authority.

### 13. Failure/eval attribution
- 0: a reviewer can identify whether a failure belongs to routing, workflow, tool, policy, implementation, or environment.
- 1: ownership is inferable but ambiguous.
- 2: success/failure is scored globally, encouraging the wrong layer to change.

### 14. Counterfactual evidence provenance
Only score when replay/simulation/inference is used.
- 0: `OBSERVED | REPLAYED | SIMULATED | INFERRED | ASSUMED` are distinguishable and claim scope respects provenance.
- 1: provenance exists but is incomplete or assumptions are not visibly sensitivity-labeled.
- 2: synthetic/replayed evidence can be mistaken for observed independent evidence, or simulation claims causal effect without identification.

## Multi-model review questions

For model-specific instructions ask:

1. Which supported model/platform requires it?
2. What observed failure/eval/test/documented behavior justifies it?
3. Would removing it materially reduce reliability for that target?
4. Does it overconstrain another supported model?
5. Can it move into an adapter, plugin manifest, or conditional reference?
6. Is it still current for supported versions?

Preferred structure:

```text
core skill
  -> model-neutral intent, invariants, boundaries, outputs
references/
  -> workflow-specific depth
platform/model adapters
  -> tool mappings and evidence-backed compensation
```

## AGENTS.md dimensions

### 1. Universal relevance
For every rule ask whether a typo fix, narrow bug fix, and architecture change all need it in context.
- 0: yes, or the rule is a short pointer.
- 1: relevant to many but not most tasks.
- 2: task-specific workflow is universally injected.

### 2. Constitutional value
- 0: architecture authority, security/production boundary, repository invariant, precedence rule, or concise routing pointer.
- 1: useful convention that could move elsewhere.
- 2: runbook, command catalog, long checklist, or generic methodology.

### 3. Verification proportionality
- 0: verification is scoped by affected surface or concrete risk.
- 1: broadly stated testing expectation.
- 2: mandatory broad/repeated verification regardless of change shape.

### 4. Safe autonomy
- 0: safe local work may continue through verification/repair without repeated approval.
- 1: continuation expectations are ambiguous.
- 2: agent is forced to stop at unnecessary intermediate decisions.

### 5. Completion clarity
- 0: completion/stop boundary is clear when persistence matters.
- 1: first-pass completion could be interpreted ambiguously.
- 2: instructions bias toward premature stopping or indefinite exploration.

### 6. Model-specific leakage
- 0: repository-global instructions remain model-neutral; platform/model behavior lives elsewhere.
- 1: a small amount of target-specific advice is universally loaded.
- 2: `AGENTS.md` substantially compensates for one model/client.

### 7. Layer leakage
- 0: `AGENTS.md` contains cross-cutting policy plus concise pointers only.
- 1: some workflow/tool semantics are copied in.
- 2: it acts as a universal router/runbook or duplicates layer-specific owners.

## Verdict guidance

- `KEEP`: low cost and clear value; no material change needed.
- `TRIM`: sound responsibility with avoidable eager context.
- `REFACTOR`: capability remains but activation, layer ownership, progressive disclosure, or isolation needs structural change.
- `MERGE`: overlap makes separate discovery surfaces harmful.
- `REMOVE`: obsolete, redundant, or better handled by normal judgment/tooling without dedicated instruction.

For catalog reviews, temporary working classifications may also use:

```text
KEEP
ROUTING_REFACTOR
WORKFLOW_REFACTOR
TOOL_PROMOTION
POLICY_DEDUP
REFERENCE_RELOCATION
```

Do not create a durable audit ledger by default.

## Priority heuristic

Prioritize:

1. incorrect/dangerous authority or evidence boundaries;
2. synthetic evidence masquerading as observed evidence;
3. deterministic mechanics incorrectly living as prompt prose;
4. routing collisions and wrong-state activation;
5. cross-cutting policy duplication;
6. unsupported model-specific scaffolding;
7. universally loaded `AGENTS.md` bloat;
8. large roots lacking progressive disclosure;
9. duplicate generic methodology;
10. wording-level concision.
