# Layered Skill Runtime and Counterfactual Evaluation — Acceptance

**Date:** 2026-09-15  
**Disposition:** COMPLETE  
**Plan:** `docs/plans/2026-09-15-layered-skill-runtime-counterfactual-eval-refactor-v2.md`  
**Architecture owner:** `docs/skill-runtime-architecture.md`

## Result

The v2 refactor is implemented on `main`.

Livingware now treats a skill as a discoverable workflow-entry package rather than the owner of every rule. Deterministic executable capability belongs to tools/operators; stable cross-cutting non-executable constraints belong to policy; reusable state transitions belong to workflows; current-state choice belongs to recurrent routing. Evaluation and learning are attributed to the owning layer and use distinct cadences.

The implementation also adds bounded process-style what-if evaluation without creating a new agent runtime, process engine, simulation database, or autonomous learning loop.

## Implemented architecture

```text
native harness discovery
        -> skill entry
        -> recurrent router
        -> workflow state
        -> operator / conditional reference / transition
        -> observation
        -> route again
        -> exit / handoff
```

Failure/change ownership is:

```text
IMPLEMENTATION -> product/code owner
ENVIRONMENT    -> fixture/runtime/config owner
CAPABILITY     -> tool/operator owner
STEERING
  -> ROUTING
  -> WORKFLOW
  -> POLICY
```

The governing rule is:

> Learning/change authority follows failure attribution and the smallest durable owner.

## Counterfactual evaluation MVL

Implemented `scripts/simulate-workflow-counterfactual.py` using Python standard library only.

Supported evaluation modes:

- `REPLAY` — deterministic recomputation; claim scope is explicitly not new observed evidence.
- `MONTE_CARLO` — seeded finite-state what-if simulation; claim scope is explicitly not causal effect.
- `REAL_REEXECUTION` — intentionally remains an external workflow/evaluation boundary. The simulator cannot fake real execution.

Evidence provenance is preserved as:

```text
OBSERVED | REPLAYED | SIMULATED | INFERRED | ASSUMED
```

The simulator validates frozen comparison identity, layer/decision point, probabilities, metric distributions, provenance/source references, loop bounds, and stochastic seed/rollout requirements. It supports only bounded `fixed` and `triangular` metric distributions in this MVL, reports success/failure/loop-limit plus latency/token/tool-call summaries, flags assumption-sensitive comparisons, and disables isolated-attribution claims for multi-layer interventions.

Different alternatives receive independent deterministic RNG streams derived from the declared seed so changing one branch does not perturb another branch's random sequence.

## Skill/runtime refactors

### `systematic-debugging`

The root skill now owns activation, lifecycle, root-cause-before-fix, tool economy, and progressive-disclosure pointers. Dynamic debugging topology lives in `references/workflow-routing.md`. `find-polluter.sh` remains an executable operator whose mechanics are owned by code/tests.

### `executing-plans`

The root skill now owns continuous plan execution, authority boundary, plan/MVL continuity, dependency boundary, real-path invariant, compact handoff, and completion transition. State topology lives in `references/workflow-routing.md`:

```text
PLAN_REVIEW
  -> PREREQUISITES
  -> TASK_EXECUTION
  -> INTEGRATION
  -> MVL_CLOSURE when applicable
  -> COMPLETION_HANDOFF
```

Unexplained failure routes to `systematic-debugging`; authorized behavior change routes to `test-driven-development`; completion claims route to `verification-before-completion`. These downstream workflows are no longer preloaded/re-owned by plan execution.

### Skill creation and review

`writing-skills` now applies a layer-ownership creation gate before adding a skill. `skill-review` routes substantial layer evaluation to `references/layered-evaluation.md`; the audit rubric now checks tool ownership, routing/workflow separation, policy duplication, failure attribution, and counterfactual evidence provenance.

Behavioral learning remains explicitly human-initiated. Replay/simulation/inference/assumption may narrow or falsify candidate changes but cannot count as materially independent observed evidence for generalized learning.

## Packaging correction found during verification

The existing Codex packaging tests exposed two stale/unsafe fork assumptions while closing this refactor:

1. marketplace/package tests still expected upstream `superpowers` branding although the canonical plugin is `livingware-engineer`;
2. `.codex-plugin/plugin.json` lacked explicit `"hooks": {}`, allowing Codex fallback hook discovery to potentially pick up the Claude SessionStart hook.

The test expectations now match Livingware identity and the manifest explicitly suppresses Codex hook auto-discovery. The reproducible zip/tar package contract remains intact.

## Catalog audit disposition

Core/high-frequency skills were reviewed against the layered model.

- `systematic-debugging` — `WORKFLOW_REFACTOR`: implemented.
- `executing-plans` — `WORKFLOW_REFACTOR` + `POLICY_DEDUP`: implemented.
- `writing-skills` — `ROUTING/OWNERSHIP_REFACTOR`: implemented.
- `skill-review` — `EVAL/OWNERSHIP_REFACTOR`: implemented.
- `test-driven-development` — `KEEP`; already has narrow activation, lifecycle, tool economy, and progressive disclosure.
- `verification-before-completion` — `KEEP`; already claim-scoped and current-state loaded.
- `using-superpowers` — `KEEP`; compatibility/reference surface, not mandatory meta-router.
- `brainstorming` — `KEEP` for this refactor; long content is primarily design/domain workflow, not a demonstrated deterministic-tool ownership defect.
- `writing-plans` — `KEEP` for this refactor; detailed plan contract is an intentional output/workflow specification and already points to downstream owners for several specialized contracts.
- `subagent-driven-development` — `KEEP` for this refactor; orchestration-specific detail remains useful and no measured routing/token regression justified a broad rewrite.

No mass namespace or directory migration was performed.

## Deterministic verification

GitHub Actions run `34923983391` on commit `6c62ac90551e09d6670e19a4119fe687988f2733` completed successfully.

The same integration job passed:

- `bash tests/codex/test-progressive-skill-loading.sh`
- `bash tests/writing-skills/test-token-economics.sh`
- `bash tests/systematic-debugging/test-find-polluter.sh`
- `python3 tests/counterfactual/test-workflow-counterfactual.py`
- `bash tests/codex/test-marketplace-manifest.sh`
- `bash tests/codex/test-package-codex-plugin.sh`

The counterfactual suite covers deterministic fixed-seed output, seed variation, replay restrictions, Monte Carlo requirements, probability closure, state closure, provenance requirements, unsupported distributions, loop bounding, non-causal claim scope, assumption sensitivity, multi-layer attribution, and non-mutation of the fixture.

The progressive-loading contract test was made portable: it validates an installed plugin cache when present and validates repository source in a clean CI checkout; `LIVINGWARE_REQUIRE_INSTALLED=1` preserves strict installed-cache verification for installation-specific runs.

## Live-model evidence boundary

A fresh three-repeat live Codex token/routing benchmark was not produced by this execution environment because the GitHub runner has no authenticated Codex CLI/model runtime, and the local CodexPro bridge was unavailable during implementation. No synthetic replacement was used.

Therefore:

- the recorded `2026-09-14` live Codex benchmark remains the historical token/routing baseline;
- this acceptance makes no new empirical latency/token-improvement claim;
- deterministic routing/collision contracts and simulator/package behavior are proven by the green CI run;
- the updated live probe is ready to report `routing`, `behavior`, `runtime`, and token usage separately when run in an authenticated Codex environment.

This limitation does not block the refactor's correctness claim because the implementation does not assert a new live token-performance improvement. It preserves the prior token-economics boundary and adds deterministic regression coverage for the new architecture.

## Final disposition

The implementation satisfies the architectural and repository scope of the v2 plan:

- no mandatory meta-router was introduced;
- current-state progressive loading is preserved;
- workflow topology and deterministic operators have distinct owners;
- routing and behavioral evidence are separable in the live probe;
- layered evaluation and learning admission are explicit;
- bounded replay/Monte Carlo what-if evaluation exists with strict provenance and non-causal claim scope;
- simulated evidence cannot promote itself into empirical recurrence/admission;
- `executing-plans` no longer re-owns downstream debugging/TDD/verification mechanics;
- deterministic integration and packaging gates are green;
- no persistent simulation/learning database, scheduled behavioral eval, or automatic policy/tool mutation was introduced.

**Status: COMPLETE.**
