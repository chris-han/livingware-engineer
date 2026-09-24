---
name: designing-evaluators
description: Use when a specific failure mode or behavioral claim is known and you need to design the smallest deterministic, interpreted, or hybrid evaluator that measures it without becoming a second authority.
---

# Designing Evaluators

Design one evaluator for one bounded claim or typed frontier.

Read `../../docs/livingware-evaluation-architecture.md` for `EvaluationClaim`, `EvaluatorCandidate`, frontier semantics, and evaluator non-authority.

## Decision order

Ask in this order:

```text
Can the claim be decided mechanically?
  yes -> DETERMINISTIC
  no  -> does it require both exact and interpreted predicates?
           yes -> HYBRID
           no  -> INTERPRETED
```

Prefer schema validation, parsers, execution tests, exact comparisons, repository/runtime inspection, or other deterministic mechanisms whenever they can decide the claim reliably.

## Claim design

Each evaluator must state:

- the exact claim;
- the required inputs;
- the bounded output frontier;
- what `UNKNOWN` means;
- what evidence is intentionally out of scope; and
- the runtime/semantic owner whose behavior is being measured.

Default atomic frontier:

```text
PASS | FAIL | UNKNOWN | NOT_APPLICABLE
```

Use a domain-specific typed frontier only when the actual decision semantics require it.

## Interpreted evaluator rules

- Use domain-grounded examples, not generic quality labels.
- Include boundary and hard-negative examples.
- Pass only the smallest sufficient context.
- Pin prompt/model/scorer versions when material.
- Keep decision output structured.
- If probabilities or confidence are emitted, define abstention/UNKNOWN semantics before qualification.
- Do not silently use the evaluator's critique or rationale as authority.

## Hybrid evaluator rule

Keep component results visible. Do not collapse an exact failure into a model opinion or hide interpreted uncertainty behind an exact-looking composite score.

## Output

Create an `EvaluatorCandidate` contract containing:

```text
claim
kind: DETERMINISTIC | INTERPRETED | HYBRID
frontier
required inputs
implementation/prompt reference
version pins
expected failure boundaries
qualification plan
non-authority statement
```

Then use `qualifying-evaluators` for interpreted or materially composite evaluators.
