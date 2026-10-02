---
name: evaluating-livingware
description: Use when evaluating an agentic software system, skill runtime, workflow, routing policy, tool behavior, or evidence quality and you need to decide which Livingware evaluation workflow applies.
---

# Evaluating Livingware

Use this as the entry skill for substantial Livingware evaluation work. It routes the current evaluation state; it is not a mandatory runtime meta-router.

Read `../../docs/livingware-evaluation-architecture.md` for the Eval IR, evaluator non-authority rule, provenance contract, and failure-attribution boundary.

## Route by current state

1. Identify the `EvaluationTarget`, the behavior or claim being evaluated, and any existing cases/traces/evaluators.
2. If there are no representative cases or traces, use `generating-eval-cases` to create coverage-directed cases, then execute the real system.
3. If traces exist but the failure taxonomy is immature or disputed, use `discovering-failures`.
4. If a known failure claim has no evaluator, use `designing-evaluators`.
5. If an interpreted evaluator exists but its reliability is not established, use `qualifying-evaluators`.
6. If the target is the observed behavior of a skill lifecycle, use `evaluating-skill-runtime`.
7. If the change alters harness composition — context, memory, tool surface, skill routing, control flow, provider/model policy, or workflow runtime — classify impact and select H0/H1/H2 using `../../docs/harness-qualification-contract.md`.
8. If a failure is attributed and the task is to iteratively change the system, compare interventions, hillclimb, or freeze a capability claim, use `governed-experimental-evolution`.
9. Use replay, real re-execution, or simulation only under the counterfactual contract in `../../docs/skill-runtime-architecture.md`.

Load only the skill required by the current state. Do not eagerly load the entire family.

## Required first questions

Resolve from available evidence before asking the user:

- What target is being evaluated?
- What exact claim or bounded frontier matters?
- Is the problem discovery, evaluator design, evaluator qualification, coverage, runtime behavior, or governed experimental evolution?
- What evidence provenance is available?
- Is the target a component or a harness/runtime composition, and what is the candidate `HarnessIdentity`?
- Which existing repository owner would own a confirmed failure?

## Invariants

- Evaluation does not authorize mutation.
- Deterministic checks precede interpreted judges when the property is mechanically decidable.
- `UNKNOWN` is a valid result when evidence is insufficient.
- Synthetic cases repair coverage; they do not become observed evidence by declaration.
- Learning authority follows failure attribution and the smallest durable owner.
- Component qualification does not imply composition qualification; material harness changes require impact-classified H0/H1/H2 evidence.
- Do not use this skill for ordinary code review, local TDD, or completion verification.

## Output

Return or create the smallest sufficient evaluation plan:

```text
Target
Claim / frontier
Available evidence + provenance
Selected evaluation workflow
Required cases / traces
Evaluator status
Failure-attribution boundary
Closing evidence
```
