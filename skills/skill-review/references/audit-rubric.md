# Audit Rubric

Score each dimension from 0 to 2, where `0 = healthy`, `1 = review`, and `2 = clear refactor target`.

## Skill dimensions

### 1. Discovery precision
- 0: short, discriminating description with an obvious trigger.
- 1: somewhat broad or keyword-heavy.
- 2: claims a large task class, overlaps several other skills, or has strong “pick me” phrasing.

### 2. Progressive disclosure
- 0: root `SKILL.md` contains only the guidance normally needed after activation.
- 1: some conditional detail is loaded eagerly.
- 2: root contains multiple long workflows, exhaustive references, examples, schemas, or tool catalogs that apply only sometimes.

### 3. Prescription cost
- 0: instructions focus on outcomes, invariants, and genuinely order-sensitive steps.
- 1: some unnecessary sequencing or recipe-like behavior.
- 2: fixed itinerary is imposed across tasks even when competent models could choose an approach safely.

### 4. Boundary quality
- 0: real safety, authority, destructive, or correctness boundaries are clear and proportionate.
- 1: some boundaries are stronger than their consequences justify.
- 2: frequent approval gates or stop rules appear to compensate for historical model behavior rather than current workflow risk.

### 5. Single-model optimization
Evaluate whether the instruction set is tuned around the quirks of one specific model generation.
- 0: core guidance is model-neutral; any model-specific compensation is isolated and clearly scoped.
- 1: some instructions assume one model's strengths or weaknesses but remain mostly portable.
- 2: the skill's main workflow depends on behavior unique to one model or release.

### 6. Multi-model compatibility
Evaluate whether the skill remains usable across the supported agent/model mix.
- 0: intent, invariants, outputs, and boundaries transfer cleanly across supported models.
- 1: some supported models may be over- or under-constrained.
- 2: guidance that helps one supported model is likely to materially hinder another.

### 7. Evidence for extra scaffolding
Treat additional recipes, reminders, approval gates, verification steps, or explicit sequencing as justified only when there is a concrete reason to retain them.
- 0: extra scaffolding is tied to observed failures, tests, safety requirements, platform limitations, or documented model behavior.
- 1: rationale is plausible but not evidenced or no longer current.
- 2: scaffolding appears historical, speculative, or duplicated with normal model capability.

Do not penalize scaffolding merely because it is detailed. Penalize unsupported universal scaffolding.

### 8. Adapter isolation
Evaluate whether model- or platform-specific instructions can be moved out of shared skill context.
- 0: model/platform-specific tool mappings and compensations live in adapter, plugin, or platform references.
- 1: some adapter-specific details remain in shared skill guidance.
- 2: shared `SKILL.md` is substantially occupied by model/platform-specific rules that could be isolated.

### 9. Duplication and collision
- 0: responsibilities are distinct and not restated elsewhere.
- 1: mild duplication.
- 2: substantial overlap with another skill or with `AGENTS.md`, creating conflicting or duplicated sources of truth.

## Multi-model review questions

For any instruction that appears model-specific, ask:

1. Which supported model or platform requires it?
2. What observed failure, evaluation, test, or documented behavior justifies it?
3. Would removing it materially reduce reliability for that target?
4. Does the same rule overconstrain another supported model?
5. Can the rule move into a model/platform adapter, plugin manifest, or conditional reference instead of shared `SKILL.md` or `AGENTS.md`?
6. Is the rule still current for the model versions actually supported?

Prefer this structure when model-specific compensation is necessary:

```text
core skill
  -> model-neutral intent, invariants, boundaries, outputs

references/
  -> workflow-specific depth

platform/model adapters
  -> tool mappings and evidence-backed behavioral compensation
```

## AGENTS.md dimensions

### 1. Universal relevance
For every rule ask: would a typo fix, narrow bug fix, and architecture change all need this in context?
- 0: yes, or the rule is a short pointer.
- 1: relevant to many but not most tasks.
- 2: task-specific workflow is universally injected.

### 2. Constitutional value
- 0: architecture authority, security/production boundary, repository invariant, precedence rule, or concise routing pointer.
- 1: useful convention that could plausibly move elsewhere.
- 2: runbook, command catalog, long checklist, or generic methodology.

### 3. Verification proportionality
- 0: verification guidance is scoped by affected surface or concrete risk.
- 1: broadly stated testing expectation.
- 2: mandatory full-suite, repo-wide, browser-wide, or repeated verification regardless of change size.

### 4. Safe autonomy
- 0: safe local work may continue through relevant verification and repair without repeated approval.
- 1: continuation expectations are ambiguous.
- 2: agent is forced to stop at unnecessary intermediate decisions.

### 5. Completion clarity
- 0: completion or stop boundary is clear when persistence matters.
- 1: first-pass completion could be interpreted ambiguously.
- 2: instructions explicitly bias toward premature stopping or indefinite exploration.

### 6. Model-specific leakage
- 0: `AGENTS.md` contains only repository-wide constraints and concise routing; model-specific behavior lives elsewhere.
- 1: a small amount of model/platform-specific advice is universally loaded.
- 2: repository-global instructions contain substantial compensation for one model or client.

## Verdict guidance

- `KEEP`: low cost and clear value; no material change needed.
- `TRIM`: sound responsibility, but description/body contains avoidable eager context.
- `REFACTOR`: capability should remain but activation semantics, progressive disclosure, or model-specific isolation need structural change.
- `MERGE`: major overlap makes separate discovery surfaces harmful.
- `REMOVE`: capability is obsolete, redundant, or better handled by normal model judgment without dedicated instruction.

## Priority heuristic

Prioritize findings in this order:

1. incorrect or dangerous boundaries,
2. unsupported model-specific scaffolding that harms other supported models,
3. broad activation collisions,
4. universally loaded `AGENTS.md` bloat,
5. model/platform rules that should move into adapters,
6. large roots lacking progressive disclosure,
7. duplicate generic methodology,
8. wording-level concision.
