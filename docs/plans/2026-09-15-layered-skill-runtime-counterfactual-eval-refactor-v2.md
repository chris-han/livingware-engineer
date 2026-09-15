# Layered Skill Runtime and Counterfactual Evaluation Refactor v2

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Status:** implementation-ready  
**Supersedes:** `docs/plans/2026-09-15-layered-skill-routing-tool-eval-learning-refactor-v1.md`  
**Architecture owner:** `docs/skill-runtime-architecture.md`

**Goal:** Refactor Livingware Engineer into a layered skill runtime where skills are discoverable workflow-entry packages, deterministic capability lives in operators, stable cross-cutting rules live in policy, context-sensitive progression lives in recurrent routing/workflows, and eval/learning are attributed to those layers at different cadences. Add a bounded offline what-if evaluation capability—deterministic replay, real re-execution, and seeded Monte Carlo—without creating an autonomous runtime or allowing synthetic evidence to authorize learning.

**Architecture:** Preserve native harness matching as first-hop discovery. After entry, route recurrently on observations. Treat process traces as evaluation objects. Counterfactual evaluation intervenes on exactly one declared layer at a frozen decision point, records evidence provenance, and can prioritize or falsify candidates; generalized learning still requires real materially independent observed evidence and explicit human authorization.

**Tech stack:** existing Markdown skills/references, Bash/Python standard library, existing Codex live probe, repository-native skill discovery. No new runtime dependency or simulation framework.

**MVL:** not applicable — framework/repository refactor. Acceptance is preserved routing behavior, clear layer ownership, useful counterfactual evaluation, and no material attributable token/tool-loop regression.

## Binding design rules

1. `Tool / Operator` owns invariant executable mechanics and deterministic regression tests.
2. `Policy / Invariant` owns stable cross-cutting non-executable constraints.
3. `Workflow` owns reusable state transitions, recovery, and exit/handoff structure.
4. `Router` owns current-state context-conditioned choice and is recurrent after observations.
5. `Skill` remains the user-facing discovery/entry package; root `SKILL.md` stays compact.
6. Native harness matching remains first-hop discovery where available; do not add a mandatory meta-router.
7. Learning authority follows failure attribution; change the smallest owning layer.
8. Routing, workflow, tool semantic evolution, and policy evolution have progressively slower admission cadence; confirmed tool correctness defects are fixed immediately.
9. Counterfactual evidence is explicitly typed as `OBSERVED | REPLAYED | SIMULATED | INFERRED | ASSUMED`.
10. Replay/simulation may guide candidate choice but may not count as a materially independent observed episode for generalized behavioral learning.
11. `REAL_REEXECUTION` against a declared comparable fixture is experimental observed evidence, not simulation.
12. Causal-effect claims are outside this MVL; seeded Monte Carlo is what-if simulation, not causal identification.
13. No new persistent trace/learning/simulation database, scheduled eval, behavioral CI gate, or automatic policy/tool mutation.

## Failure attribution

Preserve the first-stage classification and refine only `STEERING`:

```text
Observed failure
  +-- IMPLEMENTATION -> code/product owner
  +-- ENVIRONMENT    -> fixture/runtime/config owner
  +-- CAPABILITY     -> tool/operator owner
  +-- STEERING
        +-- ROUTING
        +-- WORKFLOW
        +-- POLICY
```

A routing failure cannot authorize a tool change. A tool bug cannot justify routing prose. A workflow topology problem is not fixed by broader activation. A local inconvenience cannot justify a policy mutation.

## Counterfactual comparison contract

Every what-if evaluation must declare:

```text
layer: ROUTING | WORKFLOW | TOOL | POLICY
decision_point
original_choice
alternate_choice
frozen_basis:
  fixture/input identity
  repository/input state
  workflow/policy version pins
  operator version pins
  model/harness/config pins when material
mode: REPLAY | REAL_REEXECUTION | MONTE_CARLO
seed: required for MONTE_CARLO
rollouts: required for MONTE_CARLO
metric provenance
```

Changing more than one semantic layer in one branch is allowed for exploratory simulation only; it cannot support single-layer attribution without additional isolating comparisons.

## Impact radius

**Radius:** R2. The change affects core skill contracts, skill authoring/review, Codex routing probes, behavioral-learning guidance, and new offline evaluation scripts/tests. It does not add a production agent-runtime service or external dependency.

## Integration contract

**Required:** deterministic repository tests + real existing skill files/scripts + explicit live Codex probe for native-routing claims + deterministic seeded simulator tests.

**Forbidden substitutes:** fake matcher for native routing; synthetic token counts for live token-cost claims; simulated rollouts presented as observed independent behavioral evidence.

## W0 — Freeze current progressive-loading baseline

**Read:**
- `docs/benchmarks/2026-09-14-codex-progressive-skill-token-baseline.md`
- `tests/codex/live-progressive-skill-probe.sh`
- `tests/codex/test-progressive-skill-loading.sh`

- [ ] Confirm current routing invariants: baseline -> no workflow skill; unexplained failure -> `systematic-debugging`; established diagnosis implementation -> `test-driven-development`; completion claim -> `verification-before-completion`.
- [ ] Retain the 6.8.3 median uncached-input values as variance-aware comparison references, not SLAs.
- [ ] Run:

```bash
bash tests/codex/test-progressive-skill-loading.sh
bash tests/writing-skills/test-token-economics.sh
```

- [ ] If Codex CLI is available, run one smoke pass:

```bash
CODEX_PROBE_RETRIES=1 CODEX_PROBE_TIMEOUT=180 \
  bash tests/codex/live-progressive-skill-probe.sh
```

## W1 — Canonical layered runtime documentation

**Files:**
- Keep/update: `docs/skill-runtime-architecture.md`
- Modify: `AGENTS.md`
- Modify: `docs/skill-token-economics.md`

- [ ] Verify `docs/skill-runtime-architecture.md` remains the single detailed architecture owner for layer placement, recurrent routing, failure attribution, four cadences, trace semantics, counterfactual modes, and simulation admission boundaries.
- [ ] Add one compact `AGENTS.md` principle: change/learning authority follows failure attribution and the smallest durable owner; simulation cannot substitute for real evidence where the claim is empirical.
- [ ] Keep `AGENTS.md` constitutional; do not copy the four-clock model or simulator schema into it.
- [ ] Keep token economics separated into routing context, selected workflow context, references, tool schema/payload cost, simulation cost, and real re-execution cost. Optimization order is existing evidence -> replay -> bounded simulation -> real re-execution when uncertainty justifies it.
- [ ] Run `bash tests/writing-skills/test-token-economics.sh`.

## W2 — Skill creator/reviewer enforce layer ownership

**Files:**
- Modify: `skills/writing-skills/SKILL.md`
- Modify: `skills/skill-review/SKILL.md`
- Modify: `skills/skill-review/references/audit-rubric.md`
- Modify: `tests/writing-skills/test-token-economics.sh`

- [ ] Define skill as discovery/entry package for reusable context-conditioned workflow, not as the owner of every mechanic/reference.
- [ ] Add creation gate: deterministic mechanic -> tool; repository-wide constraint -> policy owner; knowledge only -> reference; reusable context-conditioned workflow -> skill.
- [ ] Preserve SDO: descriptions say when, not how.
- [ ] Require high-frequency skills to identify nearest competing state/skill when the boundary is non-obvious.
- [ ] Extend review rubric with layer-mixing checks and simulation-evidence provenance check.
- [ ] Assert through existing token-economics tests that creator/reviewer point to the canonical architecture rather than duplicating it.
- [ ] Run:

```bash
bash tests/writing-skills/test-token-economics.sh
bash tests/codex/test-progressive-skill-loading.sh
```

## W3 — Separate routing evidence from behavior evidence

**Files:**
- Modify: `tests/codex/live-progressive-skill-probe.sh`
- Modify: `docs/skill-token-economics.md` only if the implemented metrics require clarification.

- [ ] Add required-skill and forbidden-neighboring-skill expectations per scenario.
- [ ] Emit separate fields:

```text
routing = pass | fail | unobserved
behavior = pass | fail
runtime = pass | backend-failure | timeout | error
usage = token counts
```

- [ ] Existing collision rules:
  - unexplained failure forbids TDD and verification;
  - implementation forbids debugging and verification;
  - completion claim forbids debugging and TDD;
  - baseline forbids all three when observable.
- [ ] Keep live behavioral eval manual, not CI.
- [ ] Run deterministic loading tests and one explicit live pass.

## W4 — Canary: systematic debugging

**Files:**
- Modify: `skills/systematic-debugging/SKILL.md`
- Create: `skills/systematic-debugging/references/workflow-routing.md`
- Retain executable owner: `skills/systematic-debugging/find-polluter.sh`
- Retain test owner: `tests/systematic-debugging/test-find-polluter.sh`

- [ ] Root skill keeps activation, lifecycle, root-cause-before-fix invariant, tool economy, and progressive-disclosure pointers.
- [ ] Workflow reference expresses recurrent state transitions, not a universal recipe.
- [ ] `find-polluter.sh` remains an operator; workflow decides when to call it and does not duplicate its mechanics.
- [ ] Do not preload TDD/verification.
- [ ] Run:

```bash
bash tests/systematic-debugging/test-find-polluter.sh
bash tests/codex/test-progressive-skill-loading.sh
```

- [ ] Run explicit live unexplained-failure scenario through the existing probe and verify positive selection + forbidden-collision evidence.

## W5 — Layered evaluation and learning admission

**Files:**
- Modify: `skills/skill-review/SKILL.md`
- Modify: `skills/skill-review/references/audit-rubric.md`
- Keep/refine: `skills/skill-review/references/budgeted-behavioral-learning.md`
- Create: `skills/skill-review/references/layered-evaluation.md`

- [ ] Define eval questions by layer: routing selection/branch/stop/cost; workflow convergence/recovery/loops; tool contract/determinism/compatibility; policy invariant/bypass/cross-workflow consequence.
- [ ] Preserve existing `CAPABILITY | STEERING | IMPLEMENTATION | ENVIRONMENT` first-stage classification, then refine `STEERING` to `ROUTING | WORKFLOW | POLICY`.
- [ ] Preserve simulation rule: `REPLAYED`, `SIMULATED`, `INFERRED`, and `ASSUMED` results can motivate/falsify/prioritize but cannot satisfy materially independent observed evidence for generalized shared steering learning.
- [ ] `REAL_REEXECUTION` counts as observed evidence only when it really executes the declared comparable fixture/environment.
- [ ] Keep behavioral-learning execution human-initiated.
- [ ] Run:

```bash
bash tests/writing-skills/test-token-economics.sh
```

## W6 — Counterfactual/what-if evaluation MVL

**Files:**
- Create: `scripts/simulate-workflow-counterfactual.py`
- Create: `tests/counterfactual/test-workflow-counterfactual.py`
- Create: `tests/counterfactual/fixtures/routing-whatif-v1.json`
- Modify: `docs/skill-runtime-architecture.md` only if implementation evidence exposes an ambiguity.

**Dependencies:** Python standard library only.

### W6.1 — Exact fixture/schema contract

Use one finite-state process model per alternative. Do not invent probability distributions at runtime.

```json
{
  "schema_version": "livingware.counterfactual.v1",
  "layer": "ROUTING",
  "decision_point": "after-direct-source-inspection",
  "baseline_choice": "broad-graph-discovery",
  "alternate_choice": "focused-source-followup",
  "frozen_basis": {
    "fixture_id": "routing-whatif-v1",
    "repository_state": "fixture:1",
    "workflow_version": "systematic-debugging:v-current",
    "policy_version": "livingware:current",
    "operator_versions": {
      "focused-read": "fixture:1",
      "graph-discovery": "fixture:1"
    }
  },
  "mode": "MONTE_CARLO",
  "seed": 7,
  "rollouts": 10000,
  "max_steps": 16,
  "alternatives": {
    "baseline": {
      "start_state": "S0",
      "terminal_states": ["SUCCESS", "FAILURE"],
      "transitions": []
    },
    "alternate": {
      "start_state": "S0",
      "terminal_states": ["SUCCESS", "FAILURE"],
      "transitions": []
    }
  }
}
```

Each transition has this exact conceptual shape:

```json
{
  "from": "S0",
  "to": "S1",
  "probability": {
    "value": 0.8,
    "provenance": "OBSERVED",
    "source_ref": "fixture-observation:baseline-route"
  },
  "metrics": {
    "latency_seconds": {
      "distribution": "triangular",
      "low": 20,
      "mode": 30,
      "high": 50,
      "provenance": "OBSERVED",
      "source_ref": "fixture-observation:latency"
    },
    "uncached_input_tokens": {
      "distribution": "fixed",
      "value": 12000,
      "provenance": "ASSUMED",
      "source_ref": "scenario-assumption:token-cost"
    },
    "tool_calls": {
      "distribution": "fixed",
      "value": 2,
      "provenance": "REPLAYED",
      "source_ref": "trace-replay:tool-count"
    }
  }
}
```

Supported metric distributions in v1 are intentionally bounded:

```text
fixed(value)
triangular(low, mode, high)
```

Branching probability is represented only by transition probability, not by a second Bernoulli distribution. For every nonterminal state, outgoing probabilities must sum to `1.0` within `1e-9`. `tool_calls` is rounded to a nonnegative integer after sampling; latency/tokens must remain nonnegative. Unknown distributions or missing provenance fail validation.

### W6.2 — REPLAY mode

- [ ] `REPLAY` requires all transitions to have probability `1.0` from each visited nonterminal state and all metrics to use `fixed` distributions.
- [ ] Replay walks the declared process path, sums metrics, records terminal state, and emits provenance without random sampling.
- [ ] Replay rejects stochastic transition probabilities, triangular metrics, seed/rollout-dependent semantics, or unbounded loops.

### W6.3 — MONTE_CARLO mode

- [ ] Seeded `random.Random(seed)` only; do not rely on global random state.
- [ ] Each rollout starts at the alternative's declared start state and samples one outgoing transition according to declared probabilities.
- [ ] Sample transition metrics, accumulate latency/tokens/tool calls, and stop only at declared terminal state or `max_steps`.
- [ ] Exceeding `max_steps` records a `LOOP_LIMIT` failure outcome rather than hanging.
- [ ] Report per alternative: success rate, failure rate, loop-limit rate, median and mean latency, median and mean uncached-input tokens, median and mean tool calls.
- [ ] Report baseline-minus-alternate deltas and a provenance summary for every metric family.
- [ ] If any input contributing to a claimed improvement is `ASSUMED` or `INFERRED`, label that conclusion `assumption_sensitive=true`.
- [ ] `claim_scope` must be exactly compatible with `what-if simulation; not causal effect` for Monte Carlo output.

### W6.4 — REAL_REEXECUTION boundary

Do not implement a generic real-execution engine in the simulator. `REAL_REEXECUTION` is a workflow/eval mode that invokes the existing real harness/fixture externally and records its result as `OBSERVED`. The simulator may consume those observations as later fixture inputs, but must not fake them.

### W6.5 — Validation and output

- [ ] Input validation fails closed for missing layer, decision point, choices, frozen-basis identifiers, provenance/source refs, terminal states, invalid probability sums, unsupported distribution, negative metric parameters, or missing seed/rollouts in Monte Carlo.
- [ ] A comparison changing multiple declared semantic layers is marked `exploratory=true` and `isolated_attribution=false`.
- [ ] Output is JSON only and includes schema version, input digest, mode, seed/rollouts when relevant, per-alternative summaries, deltas, provenance summary, assumption sensitivity, isolated-attribution flag, and claim scope.
- [ ] Normalize object key order and numeric rounding so fixed fixture + fixed seed yields byte-stable output.
- [ ] Keep output ephemeral; no persistent simulation ledger/database.

### W6.6 — Required tests

- [ ] fixed fixture + fixed seed -> byte-stable normalized result;
- [ ] different seed -> permitted numeric variance but identical schema/provenance semantics;
- [ ] replay rejects stochastic transition probability;
- [ ] replay rejects triangular metric;
- [ ] Monte Carlo rejects missing seed or rollouts;
- [ ] outgoing probabilities not summing to 1 fail;
- [ ] missing provenance/source ref fails;
- [ ] unsupported distribution fails;
- [ ] process loop is bounded by `max_steps` and reported, not hung;
- [ ] simulated output cannot be marked `OBSERVED`;
- [ ] output cannot claim causal effect;
- [ ] assumption-driven superiority is visibly labeled;
- [ ] multi-layer intervention cannot claim isolated attribution;
- [ ] simulator does not modify skills, policies, source, or repository state.

Run:

```bash
python3 tests/counterfactual/test-workflow-counterfactual.py
```

Expected: all pass.

## W7 — Refactor `executing-plans` after canaries are green

**Dependency:** W3-W6 green.

**Files:**
- Modify: `skills/executing-plans/SKILL.md`
- Create: `skills/executing-plans/references/workflow-routing.md`
- Review only unless evidence requires change: `skills/subagent-driven-development/SKILL.md`

- [ ] Root owns activation, continuous-execution lifecycle, plan/MVL continuity, human-judgment boundary, and canonical pointers.
- [ ] Workflow reference owns state transitions: plan review -> prerequisites -> feature task -> integration -> MVL closure -> branch completion, including routes back to debugging/TDD on contradictory observations.
- [ ] Do not duplicate debugging/TDD/verification/browser/dependency workflows.
- [ ] Reference deterministic owners for mechanical operations.
- [ ] Preserve explicit consent requirement for implementation directly on main/master.

## W8 — Bounded catalog audit

Review high-frequency skills first: TDD, verification, writing-plans, brainstorming, using-superpowers, subagent-driven-development.

Classify only for the current review:

```text
KEEP
ROUTING_REFACTOR
WORKFLOW_REFACTOR
TOOL_PROMOTION
POLICY_DEDUP
REFERENCE_RELOCATION
```

- [ ] Apply only fixes with clear owner/cost benefit.
- [ ] Every tool promotion needs a deterministic test before deleting prose.
- [ ] Every routing change gets smallest positive/negative/collision evidence.
- [ ] Generalized workflow-learning claims follow W5; simple dedup/refactor does not require artificial behavioral-learning ceremony.
- [ ] Do not create a durable audit ledger unless a real consumer emerges.

## W9 — Final verification and disposition

Run repository-local deterministic checks:

```bash
bash tests/codex/test-progressive-skill-loading.sh
bash tests/writing-skills/test-token-economics.sh
bash tests/systematic-debugging/test-find-polluter.sh
python3 tests/counterfactual/test-workflow-counterfactual.py
```

Run explicit skill-request integration using the existing runner when its required model/runtime is available:

```bash
bash tests/explicit-skill-requests/run-all.sh
```

Run relevant platform/plugin checks for surfaces actually changed. At minimum, if Codex packaging/sync files changed, use the existing Codex tests rather than a nonexistent generic `tests/plugin-loader` suite:

```bash
bash tests/codex/test-marketplace-manifest.sh
bash tests/codex/test-package-codex-plugin.sh
```

Then run three comparable live Codex probe repetitions using the existing isolated fixture shape:

```bash
for i in 1 2 3; do
  CODEX_PROBE_RETRIES=1 CODEX_PROBE_TIMEOUT=180 \
    bash tests/codex/live-progressive-skill-probe.sh || exit 1
done
```

Expected:

- current-state routing remains correct;
- forbidden neighboring skill activation is absent when observable;
- behavior oracles remain green;
- bounded scenarios do not acquire a mandatory meta-router or broad codebase-memory path;
- simulation tests are deterministic under fixed seed and preserve provenance;
- no simulation result is treated as independent observed learning evidence;
- median token/latency is compared to the 2026-09-14 baseline with trace attribution, not single-run thresholds.

If token/runtime regression appears, attribute it to routing collision, extra workflow context, tool schema/payload, serial turns, repeated evidence, simulation overhead, or model/runtime variance before changing the owning layer.

## Acceptance criteria

The refactor is complete when:

- skill/tool/policy/workflow/router ownership is mechanically understandable and documented once;
- native matching remains first-hop discovery;
- routing is recurrent and separately evaluable from behavior;
- creator/reviewer can identify layer-mixing and nearest competing routing states;
- systematic-debugging and executing-plans demonstrate the new split;
- routing/workflow/tool/policy evals have distinct admission cadence;
- counterfactual evaluator supports deterministic replay and seeded BPM-style finite-state Monte Carlo what-if simulation with explicit provenance;
- simulator has no causal mode and never upgrades synthetic evidence to observed evidence;
- real re-execution remains the preferred empirical validation of promising alternatives;
- generalized learning still requires materially independent observed evidence and human authorization;
- no persistent simulation/learning database, scheduled eval, or autonomous mutation loop is added;
- final deterministic and live routing/token checks pass without material attributable regression.

## Non-goals

- a production workflow orchestration engine;
- a second skill router;
- causal inference or structural-causal-model implementation;
- resource/queue scheduling simulation in this MVL;
- automatic discovery of probability distributions from all agent traces;
- automatic policy/tool mutation;
- persistent process-mining/event-log infrastructure;
- mass rewriting every skill in one release.

## Execution order / stop rule

Execute W0 -> W1 -> W2 -> W3 -> W4 -> W5 -> W6. Only proceed to W7 after the canary routing, layered-eval, and counterfactual-evaluator tests are green. W8 is bounded cleanup. W9 closes the refactor.

If the layered split or simulator increases total token/tool-loop cost without producing measurable evaluation value, narrow the abstraction before migrating more skills. Do not compensate with more always-loaded instructions or a universal router.
