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

Gate: `LIVINGWARE_EVAL_ZERO_RUNTIME_INTEGRATION_GREEN` — GREEN in GitHub Actions run 186.

## W3 — Discoverability and packaging

- [x] Add a compact README section for the evaluation skill family.
- [x] Verify existing plugin packaging discovers the six new skill directories without manifest duplication. Codex points to the whole `skills/` tree; Hermes registers every `skills/*/SKILL.md` dynamically.
- [x] Run repository skill/package contract tests relevant to Codex/Hermes and any generic skill discovery checks. GitHub Actions run 186 completed GREEN, including Livingware eval skill contracts, counterfactual evaluator, progressive skill loading, and Codex package contracts.

Gate: `LIVINGWARE_EVAL_DISCOVERABILITY_GREEN` — GREEN in GitHub Actions run 186.

## W4 — Dogfood on existing Livingware skills

Use `evaluating-skill-runtime` on at least two different behavior classes:

1. `systematic-debugging` — trigger/routing/workflow/exit behavior.
2. one skill with a materially different lifecycle, such as `verification-before-completion` or `writing-plans`.

For each:

- [x] define should-activate and should-not-activate cases;
- [x] include one neighboring-skill collision case;
- [x] include one hard negative;
- [x] capture accepted deterministic repository-contract evidence;
- [x] preserve live native-harness activation cases separately as `UNVERIFIED` rather than inferring them from static contracts;
- [x] attribute any qualified failure before proposing changes; no qualified deterministic-contract failure was found;
- [x] create a `RegressionWitness` only if a qualified failure is found; none was created because no qualified failure was found.

Dogfood artifact: `tests/eval-skills/fixtures/skill-runtime-dogfood-v1.json`.

This phase proves the Eval IR against two materially different skill lifecycles at the deterministic contract layer. It does **not** claim that native model/harness activation behavior is verified.

Gate: `LIVINGWARE_EVAL_DOGFOOD_CONTRACT_GREEN` — GREEN in GitHub Actions run 186.  
Remaining empirical gate: `LIVINGWARE_EVAL_NATIVE_HARNESS_ACTIVATION_UNVERIFIED`.

## W5 — Evaluator qualification proof

Qualify at least:

- [x] one deterministic evaluator: the repository contract evaluator in `tests/eval-skills/test_eval_skills_contract.py`, exercised in GitHub Actions run 186;
- [x] one interpreted evaluator, if a genuinely semantic claim is found during dogfood — `NOT_APPLICABLE_INTERPRETED_EVALUATOR` for the current bounded dogfood because all qualified claims are mechanically decidable.

For interpreted qualification:

- [x] keep shaping examples disjoint from held-out measurement — not applicable because no interpreted evaluator is introduced;
- [x] report confusion matrix and class-specific behavior — not applicable for deterministic contract checks;
- [x] test ordering/permutation invariance when the frontier permits order leakage — not applicable for deterministic contract checks;
- [x] pin evaluator/model/prompt versions — no model/prompt evaluator exists in this slice;
- [x] declare `QUALIFIED | QUALIFIED_BOUNDED | NOT_QUALIFIED` — deterministic contract evaluator is `QUALIFIED`;
- [x] record limitations and `UNKNOWN`/defer behavior — live native-harness activation remains explicitly outside the deterministic evaluator's claim.

Do not create an LLM judge merely to satisfy this milestone. Current disposition: `NOT_APPLICABLE_INTERPRETED_EVALUATOR`.

Gate: `LIVINGWARE_EVALUATOR_QUALIFICATION_GREEN` for the deterministic evaluator slice.

## W6 — Native harness empirical runner

- [x] Reuse `tests/codex/live-progressive-skill-probe.sh` rather than creating a second routing probe.
- [x] Add `tests/eval-skills/live-skill-runtime-eval.sh` as the Livingware Eval entrypoint.
- [x] Add `scripts/compile-live-skill-eval.py` as the deterministic summary-to-Eval-IR operator.
- [x] Compile live executions as `livingware.eval-run.v1` with `OBSERVED` provenance.
- [x] Bind each live artifact to production run id, repository commit, Livingware version, and Codex CLI version.
- [x] Preserve routing, behavior, and runtime as separate claims.
- [x] Map missing required explicit skill-load evidence to `UNKNOWN` instead of inferring routing from output behavior.
- [x] Treat the no-workflow baseline differently: verified absence of forbidden workflow skills is positive routing evidence.
- [x] Add deterministic compiler fixtures and CI coverage.
- [x] GitHub Actions run 194 is GREEN for the compiler/eval contracts and existing repository contracts.
- [ ] Execute the runner against the current branch in an authenticated Codex environment and admit the resulting `eval-run.json` as current empirical evidence.

Current command:

```bash
CODEX_PROBE_RETRIES=1 \
CODEX_PROBE_TIMEOUT=180 \
bash tests/eval-skills/live-skill-runtime-eval.sh
```

Historical note: Livingware 6.9.2 had GREEN live Codex routing for baseline, debugging, implementation, and completion-claim scenarios. That evidence is a regression reference only and does not close the current branch's empirical gate.

Gate: `LIVINGWARE_EVAL_NATIVE_HARNESS_RUNNER_READY` — GREEN.  
Empirical gate remains: `LIVINGWARE_EVAL_NATIVE_HARNESS_ACTIVATION_UNVERIFIED`.

## Completion

The architecture/skill implementation slice is complete: W0-W3 are GREEN, W4 is GREEN at the deterministic contract layer, and W5 is GREEN for the deterministic evaluator slice. Native harness activation remains an explicit empirical follow-up and is not represented as completed evidence.

Terminal dispositions:

```text
COMPLETE
COMPLETE_NO_INTERPRETED_EVALUATOR_REQUIRED
BLOCKED_BY_REAL_EVIDENCE_GAP
REVISE_ARCHITECTURE
```
