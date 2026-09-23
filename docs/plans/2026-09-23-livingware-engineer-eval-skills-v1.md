# Livingware Engineer Eval Skills v1

**Status:** active  
**Date:** 2026-09-23  
**Architecture owner:** `docs/livingware-evaluation-architecture.md`  
**Runtime owner:** `docs/skill-runtime-architecture.md`  
**Reference inspiration:** `ai-evals-course/evals-skills` — product-specific error discovery, evaluator design/validation, review interfaces, and coverage-oriented synthetic data

## Goal

Add a Livingware-native evaluation skill family for agentic software systems without creating a second runtime, a new persistent evaluation service, or automatic self-improvement authority.

The v1 architecture evaluates not only final outputs but the full path through routing, workflows, tools/operators, policy, outcomes, and evidence. Failure discovery remains evidence-first; evaluator outputs remain non-authoritative; learning/change authority follows failure attribution.

## Architecture delta

Existing Livingware already owns:

- layered runtime semantics and recurrent routing;
- failure attribution across implementation/environment/capability/routing/workflow/policy;
- evidence provenance: `OBSERVED | REPLAYED | SIMULATED | INFERRED | ASSUMED`;
- counterfactual replay, real re-execution, and Monte Carlo semantics;
- budgeted behavioral learning;
- skill instruction-surface review;
- deterministic repository tests and behavioral fixtures.

The verified gap is an explicit evaluation discipline connecting those capabilities:

```text
trace / case
  -> failure discovery
  -> bounded evaluation claim
  -> evaluator design
  -> evaluator qualification
  -> failure attribution
  -> regression witness
  -> learning candidate
```

This plan fills that gap only.

## Non-goals

- no foundation-model benchmark framework;
- no persistent eval database;
- no always-on annotation server;
- no mandatory meta-router;
- no second counterfactual engine;
- no universal quality score;
- no universal evaluator threshold;
- no automatic routing/workflow/tool/policy mutation;
- no replacement for `skill-review`, TDD, or `verification-before-completion`.

## W0 — Freeze architecture and owner boundaries

- [x] Add `docs/livingware-evaluation-architecture.md`.
- [x] Define evaluator non-authority.
- [x] Reuse existing evidence provenance unchanged.
- [x] Reuse existing failure attribution unchanged.
- [x] Freeze synthetic generation as coverage repair rather than evidence manufacturing.
- [x] Freeze `skill-review` as instruction-surface owner.
- [x] Freeze counterfactual semantics under `docs/skill-runtime-architecture.md`.

Gate: `LIVINGWARE_EVAL_ARCHITECTURE_BOUNDARY_GREEN`.

## W1 — Add Livingware Eval IR and skill family

Add the conceptual Eval IR:

- [x] `EvaluationTarget`
- [x] `EvalCase`
- [x] `ObservedTrace`
- [x] `EvaluationClaim`
- [x] `FailureObservation`
- [x] `FailureModeCandidate`
- [x] `FailureAttribution`
- [x] `EvaluatorCandidate`
- [x] `EvaluatorQualification`
- [x] `RegressionWitness`
- [x] `LearningCandidate`

Add six progressive-disclosure skills:

- [x] `evaluating-livingware`
- [x] `discovering-failures`
- [x] `designing-evaluators`
- [x] `qualifying-evaluators`
- [x] `generating-eval-cases`
- [x] `evaluating-skill-runtime`

Gate: `LIVINGWARE_EVAL_IR_AND_SKILLS_GREEN`.

## W2 — Contract tests and zero-runtime proof

- [x] Add `tests/eval-skills/test_eval_skills_contract.py`.
- [x] Assert the six skills exist with architecture references.
- [x] Assert evaluator non-authority, provenance, synthetic coverage, and no universal threshold.
- [x] Assert `evaluating-skill-runtime` does not replace `skill-review`.
- [x] Add `tests/eval-skills/fixtures/routing-whatif-eval-ir-v1.json`.
- [x] Map the existing `routing-whatif-v1.json` counterfactual fixture into the Eval IR without adding a database/runtime.

Gate: `LIVINGWARE_EVAL_ZERO_RUNTIME_INTEGRATION_GREEN` after tests execute successfully.

## W3 — Discoverability and packaging

- [ ] Add a compact README section for the evaluation skill family.
- [ ] Verify existing plugin packaging discovers the six new skill directories without manifest duplication.
- [ ] Run repository skill/package contract tests relevant to Codex/Hermes and any generic skill discovery checks.

Gate: `LIVINGWARE_EVAL_DISCOVERABILITY_GREEN`.

## W4 — Dogfood on existing Livingware skills

Use `evaluating-skill-runtime` on at least two different behavior classes:

1. `systematic-debugging` — trigger/routing/workflow/exit behavior.
2. one skill with a materially different lifecycle, such as `verification-before-completion` or `writing-plans`.

For each:

- [ ] define should-activate and should-not-activate cases;
- [ ] include one neighboring-skill collision case;
- [ ] include one hard negative;
- [ ] capture real or accepted fixture evidence;
- [ ] attribute any failure before proposing changes;
- [ ] create at least one `RegressionWitness` only if a qualified failure is found.

This phase validates that the Eval IR is useful rather than merely structurally consistent.

Gate: `LIVINGWARE_EVAL_DOGFOOD_GREEN`.

## W5 — Evaluator qualification proof

Qualify at least:

- [ ] one deterministic evaluator;
- [ ] one interpreted evaluator, if a genuinely semantic claim is found during dogfood.

For interpreted qualification:

- [ ] keep shaping examples disjoint from held-out measurement;
- [ ] report confusion matrix and class-specific behavior;
- [ ] test ordering/permutation invariance when the frontier permits order leakage;
- [ ] pin evaluator/model/prompt versions;
- [ ] declare `QUALIFIED | QUALIFIED_BOUNDED | NOT_QUALIFIED`;
- [ ] record limitations and `UNKNOWN`/defer behavior.

Do not create an LLM judge merely to satisfy this milestone. If all dogfood claims are mechanically decidable, record `NOT_APPLICABLE_INTERPRETED_EVALUATOR`.

Gate: `LIVINGWARE_EVALUATOR_QUALIFICATION_GREEN`.

## Completion

The plan may close when W0-W3 are green and W4 proves the architecture on existing Livingware behavior. W5 is required only when an interpreted evaluator is genuinely necessary.

Terminal dispositions:

```text
COMPLETE
COMPLETE_NO_INTERPRETED_EVALUATOR_REQUIRED
BLOCKED_BY_REAL_EVIDENCE_GAP
REVISE_ARCHITECTURE
```
