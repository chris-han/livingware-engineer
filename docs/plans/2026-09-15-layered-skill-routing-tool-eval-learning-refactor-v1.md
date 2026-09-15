# Layered Skill Routing, Tool, Eval, and Learning Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Status:** implementation-ready

**Goal:** Refactor Livingware Engineer so a user-facing skill is a dynamically routed workflow package rather than a monolithic instruction bundle: invariant executable behavior lives in tools/operators and deterministic tests, non-executable cross-cutting invariants live in policy, context-dependent choice lives in routing/workflows, and evaluation plus learning are attributed to the owning layer at different cadences.

**Architecture:** Keep native harness skill matching as the first dispatcher and do not add a mandatory meta-router or autonomous runtime. Treat routing as recurrent: after each meaningful observation, the active workflow may choose another operator, reference, workflow state, or exit. Preserve the existing progressive-disclosure/token-economics architecture and the human-authorized behavioral-learning boundary; this refactor changes ownership and evaluation semantics, not the user's authorization model.

**Tech Stack:** Markdown skill contracts, existing Bash/Python utilities and tests, existing Codex live probe, repository-native skill discovery. No new dependency or orchestration framework.

**Spec / source contracts:**
- `docs/plans/2026-09-14-token-cost-progressive-skill-loading-refactor.md`
- `docs/plans/2026-09-11-workflow-learning-trigger-refactor.md`
- `docs/skill-token-economics.md`
- `skills/skill-review/references/budgeted-behavioral-learning.md`
- `AGENTS.md`

**MVL:** not applicable — this is a repository/framework architecture refactor, not a product feature. The acceptance unit is preserved routing behavior, clearer ownership, layer-specific evals, and no material token-cost regression.

## Architectural Decision

The word **skill** remains the user-facing discovery/packaging abstraction, but it is no longer treated as the primitive owner of every rule.

```text
User intent + current evidence
          |
          v
Native harness skill matching
          |
          v
Dynamic router <----------------------------+
          |                                  |
          v                                  |
Workflow state                               |
          |                                  |
          +--> Tool / operator --> observation+
          |
          +--> Conditional reference
          |
          +--> Exit / handoff

Cross-cutting policy constrains every layer but does not perform ordinary routing.
```

Canonical responsibilities:

1. **Tool / operator — invariant executable capability.** If behavior can be made deterministic, mechanically checked, and reused without semantic judgment, its contract belongs in executable code plus focused tests. Existing `scripts/` and skill-local `scripts/` already provide this surface; this plan does not require moving them into a new directory merely to satisfy a taxonomy.
2. **Policy / invariant — stable non-executable constraint.** Security, authority, destructive-operation boundaries, architecture laws, and other cross-cutting constraints that cannot simply become a tool stay in the smallest authoritative policy surface, normally `AGENTS.md` or an owned canonical reference.
3. **Workflow — reusable state-transition structure.** A workflow defines admissible states, transitions, evidence required to leave a state, recovery paths, and exit conditions. It does not re-document tool internals.
4. **Router — dynamic context-conditioned choice.** Routing decides which workflow state, operator, reference, or exit is appropriate now. Routing is recurrent, not only a one-time skill-selection event.
5. **Skill — discovery and workflow entry package.** `SKILL.md` owns a discriminating activation description, minimal lifecycle/entry contract, hard local invariants that must be visible whenever selected, and pointers to workflow/reference/tool owners. It should not duplicate deterministic tool behavior or future-state workflows.

### Placement rule

When editing any instruction, ask in this order:

```text
Can this rule be enforced deterministically?
  YES -> tool/script/test owns it
  NO  -> does it constrain all/most executions regardless of context?
          YES -> policy/invariant owner
          NO  -> is it a reusable state transition or ordered recovery path?
                  YES -> workflow
                  NO  -> dynamic routing/reference detail
```

Reference knowledge that does not itself decide or execute remains progressively loaded reference material.

## Four Cadences

Cadence means **how readily a layer may be evaluated and revised when evidence exists**. It does not create a schedule, daemon, CI behavioral gate, autonomous learning loop, or automatic mutation.

1. **Routing clock — fast.** Cheap targeted selection/branch/stop evals may run when routing behavior changes or a concrete routing failure is being investigated. Evaluate route precision, false activation, missed activation, collisions, unnecessary tool-family activation, branch quality, stop quality, token cost, and latency.
2. **Workflow clock — medium.** Change workflow topology, ordering, recovery, escalation, or handoff rules only when repeated materially independent steering evidence or an explicit architecture change justifies it. Evaluate convergence, loop avoidance, recovery quality, state transitions, and capability-floor preservation.
3. **Tool clock — slow for semantic evolution, immediate for confirmed correctness defects.** New capability or changed operator semantics require a stable contract, deterministic tests, compatibility review, and versioned admission. A proven implementation bug is fixed immediately through the normal defect/regression path; “slow” never means leaving a correctness bug unfixed.
4. **Policy clock — slowest.** Cross-cutting invariants change only through explicit architecture/governance reasoning and cross-workflow regression evidence because a policy change can alter many workflows at once.

The intended ordering is:

```text
routing adaptation frequency
    > workflow evolution frequency
    > tool semantic evolution frequency
    > policy/invariant evolution frequency
```

All shared behavioral learning remains human-authorized under the existing budgeted-learning contract.

## Failure Attribution Before Learning

Preserve the current first-stage classification and add layer attribution rather than replacing it:

```text
Observed failure
  |
  +--> IMPLEMENTATION -> code/product owner + regression test
  +--> ENVIRONMENT    -> fixture/runtime/config owner
  +--> CAPABILITY     -> tool/operator owner
  +--> STEERING       -> attribute further:
                          ROUTING
                          WORKFLOW
                          POLICY
```

Rules:

- A routing failure does not authorize a tool change.
- A tool/capability defect does not authorize new routing prose unless independent evidence shows a routing problem too.
- A workflow loop or bad transition is not repaired by widening skill descriptions.
- A policy change is not justified by one local workflow inconvenience.
- The existing recurrence/material-independence rule continues to govern shared steering learning; confirmed tool correctness bugs follow their normal deterministic regression path.
- **Learning authority follows failure attribution.** Change the smallest owning layer that can explain the evidence.

## Impact Radius

**Source:** targeted repository inspection of the current skill, test, and benchmark surfaces.

**Changed surfaces:** `AGENTS.md`, skill authoring/review contracts, progressive-loading/token-economics documentation, selected canary skills, existing Codex routing probes, and behavioral-learning guidance.

**Direct consumers:** native skill matchers, Codex/Claude/Gemini-compatible skill loaders, contributors creating/reviewing skills, and existing live probe/test scripts.

**Affected boundaries:** skill discovery, workflow transition, tool invocation choice, completion/exit behavior, evaluation ownership, and learning admission.

**Radius:** R2 — multiple repository components and harness-facing skill contracts, but no production application runtime or external service boundary.

## Integration Contract

**Required scope:** focused repository tests + existing live Codex routing/usage probe.

**Real components required:** actual `SKILL.md` files, repository scripts/tests, and native Codex skill matching for the live probe.

**Permitted substitutes:** none for the repository-owned routing contracts under test; unavailable external/model runtime may be reported as an environment failure rather than simulated.

**Forbidden mocks:** a fake skill matcher cannot prove native-routing behavior; synthetic token counts cannot replace the existing live usage probe when token-cost claims are made.

**UI test:** not applicable.

## Global Constraints

- Preserve native matcher first; do not reintroduce `using-superpowers` as a mandatory first-hop router.
- Preserve progressive disclosure: current-state guidance only; future-state skills remain unloaded.
- Preserve hard security, authority, destructive-operation, architecture, real-component, browser-evidence, and correctness invariants.
- Do not add an autonomous learning loop, telemetry ledger, scheduled eval, automatic policy mutation, or behavioral CI gate.
- Do not create a new top-level tool framework merely to rename existing scripts. “Tool/operator” is an ownership role; migrate physical layout only when a concrete consumer requires it.
- Do not make model-specific workarounds part of the shared core unless current evidence requires them; isolate them behind platform/model references.
- Do not optimize prompt bytes at the cost of extra tool calls, retries, weaker routing, or weaker verification.

## Workstream W0 — Freeze the Current Behavioral and Token Baseline

**Purpose:** Establish that the refactor begins from the 6.8.x progressive-loading behavior rather than silently changing its invariants.

**Files:**
- Read: `docs/benchmarks/2026-09-14-codex-progressive-skill-token-baseline.md`
- Read: `tests/codex/live-progressive-skill-probe.sh`
- Read: `tests/codex/test-progressive-skill-loading.sh`
- No production changes in this workstream.

- [ ] Confirm the existing baseline invariants: baseline selects no workflow skill; unexplained failure selects `systematic-debugging`; established-diagnosis implementation selects `test-driven-development`; completion claim selects `verification-before-completion`.
- [ ] Record the existing 6.8.3 median uncached-input reference values for comparison only: baseline 5,611; debugging 24,747; TDD 20,055; verification 14,437. Treat them as variance-aware references, not hard SLAs.
- [ ] Run the deterministic progressive-loading tests before modifying routing contracts:

```bash
bash tests/codex/test-progressive-skill-loading.sh
bash tests/writing-skills/test-token-economics.sh
```

Expected: both pass.

- [ ] If Codex CLI is available and the environment is comparable, run one pre-change live smoke pass; reuse the recorded 2026-09-14 three-run baseline rather than generating a redundant new benchmark when nothing relevant has changed:

```bash
CODEX_PROBE_RETRIES=1 CODEX_PROBE_TIMEOUT=180 \
  bash tests/codex/live-progressive-skill-probe.sh
```

Expected: all four current scenarios pass or an external runtime/backend failure is clearly classified.

**Commit:** none.

## Workstream W1 — Establish the Canonical Layered Runtime Model

**Files:**
- Create: `docs/skill-runtime-architecture.md`
- Modify: `AGENTS.md`
- Modify: `docs/skill-token-economics.md`

**Produces:** one authoritative vocabulary and placement rule for Tool/Operator, Policy, Workflow, Router, and Skill.

- [ ] Create `docs/skill-runtime-architecture.md` with the architecture decision, recurrent-routing loop, placement rule, four cadences, and failure-attribution model from this plan.
- [ ] State explicitly that native harness matching owns first-hop discovery while workflow routing owns subsequent context-conditioned decisions; a host with native matching must not be wrapped in a second mandatory router.
- [ ] Define the operator-promotion rule: deterministic/repeatable mechanics move to scripts/tools/tests when doing so removes prompt interpretation without creating unnecessary infrastructure.
- [ ] Define the exception: cross-cutting non-executable invariants remain policy; they are not duplicated into every tool.
- [ ] Add one compact `AGENTS.md` principle: learning/change authority follows failure attribution and the smallest durable owner. Do not copy the four-clock model or routing decision tree into `AGENTS.md`.
- [ ] Extend `docs/skill-token-economics.md` so token review distinguishes routing context, selected workflow context, tool schema/payload cost, and references. Make clear that moving stable behavior into tools is useful only when the tool call/schema/output costs less than repeated natural-language steering across the workflow.
- [ ] Run:

```bash
bash tests/writing-skills/test-token-economics.sh
```

Expected: pass.

- [ ] Commit:

```bash
git add AGENTS.md docs/skill-runtime-architecture.md docs/skill-token-economics.md
git commit -m "docs: define layered skill runtime architecture"
```

## Workstream W2 — Make Skill Creation and Review Enforce Layer Ownership

**Files:**
- Modify: `skills/writing-skills/SKILL.md`
- Modify: `skills/skill-review/SKILL.md`
- Modify: `skills/skill-review/references/audit-rubric.md`
- Modify: `tests/writing-skills/test-token-economics.sh`

**Produces:** authoring/review guidance that treats skills as workflow packages and rejects layer mixing.

- [ ] Replace the broad “skill is a reference guide” definition in `skills/writing-skills/SKILL.md` with the layered model: skill = discovery/entry package for a reusable workflow; references remain knowledge; deterministic mechanics should become tools/scripts/tests.
- [ ] Add a creation gate before adding a new skill: if the proposed behavior is purely deterministic capability, add/extend a tool; if it is project-specific policy, use the repository instruction owner; if it is only reference knowledge, add a reference; create a skill only for a reusable context-conditioned workflow/discovery surface.
- [ ] Preserve the existing `name`/`description` compatibility requirements and SDO rule that descriptions say **when**, not **how**.
- [ ] Add nearest-competing-skill thinking to authoring: every high-frequency skill must identify at least one adjacent state it must not capture when that boundary is non-obvious.
- [ ] Refactor `skills/skill-review/SKILL.md` so its root body routes to owned references rather than repeating the full layered evaluation model. Keep the opt-in behavioral-learning invariant in the root.
- [ ] Extend `audit-rubric.md` with four new review questions without creating a second scoring framework:
  1. Is deterministic capability incorrectly encoded as repeated prose?
  2. Is dynamic routing incorrectly frozen into a universal sequence?
  3. Does the skill duplicate policy owned elsewhere?
  4. Can the reviewer identify the owner of each failure/eval signal?
- [ ] Update `tests/writing-skills/test-token-economics.sh` to assert the new canonical architecture reference exists and that the skill author/reviewer point to it without copying a second authoritative model.
- [ ] Run:

```bash
bash tests/writing-skills/test-token-economics.sh
bash tests/plugin-loader/test-plugin-loading.sh
```

Expected: pass.

- [ ] Commit:

```bash
git add skills/writing-skills/SKILL.md \
        skills/skill-review/SKILL.md \
        skills/skill-review/references/audit-rubric.md \
        tests/writing-skills/test-token-economics.sh
git commit -m "refactor: separate skill workflow and tool ownership"
```

## Workstream W3 — Split Routing Evaluation from Workflow/Tool Evaluation

**Files:**
- Modify: `tests/codex/live-progressive-skill-probe.sh`
- Modify: `docs/skill-runtime-architecture.md`
- Modify: `docs/skill-token-economics.md`

**Produces:** the existing live probe can measure required selection and forbidden collisions separately from downstream behavioral success.

- [ ] Extend each probe scenario with an explicit **required skill** and **forbidden neighboring skills** rather than treating “expected skill observed” as sufficient routing evidence.
- [ ] Preserve the current behavior oracle as a separate signal. A run should be able to report:

```text
routing = pass/fail/unobserved
behavior = pass/fail
usage = counts
runtime = pass/backend-failure/timeout/error
```

Do not collapse these into one status because a behavioral success can hide a routing collision.

- [ ] For the existing three workflow scenarios, encode at least these forbidden collisions:
  - unexplained failure: forbid `test-driven-development` and `verification-before-completion`;
  - established-diagnosis implementation: forbid `systematic-debugging` and `verification-before-completion`;
  - completion claim: forbid `systematic-debugging` and `test-driven-development`.
- [ ] For the baseline `Reply with exactly: OK` case, treat any activation of those three workflow skills as a routing failure when observable.
- [ ] Keep behavioral eval execution manual/explicit. Do not add the live Codex probe to CI.
- [ ] Document routing metrics separately from workflow outcome and token metrics in `docs/skill-token-economics.md`.
- [ ] Run the shell/static tests that do not require Codex, then one explicit live run:

```bash
bash tests/codex/test-progressive-skill-loading.sh
CODEX_PROBE_RETRIES=1 CODEX_PROBE_TIMEOUT=180 \
  bash tests/codex/live-progressive-skill-probe.sh
```

Expected: required routing remains correct, no forbidden neighboring skill is observed, and current behavioral oracles still pass.

- [ ] Commit:

```bash
git add tests/codex/live-progressive-skill-probe.sh \
        docs/skill-runtime-architecture.md \
        docs/skill-token-economics.md
git commit -m "test: separate routing and behavior evaluation"
```

## Workstream W4 — Canary Refactor 1: Systematic Debugging

**Files:**
- Modify: `skills/systematic-debugging/SKILL.md`
- Create: `skills/systematic-debugging/references/workflow-routing.md`
- Read/retain: `skills/systematic-debugging/find-polluter.sh`
- Read/retain: `skills/systematic-debugging/test-find-polluter.sh`
- Modify if needed for references only: `skills/systematic-debugging/references/detailed-playbook.md`

**Produces:** one small skill demonstrating the target split without inventing a new runtime.

- [ ] Keep `SKILL.md` responsible for activation, entry/exit, the root-cause-before-fix invariant, tool-economy boundary, and progressive-disclosure pointers.
- [ ] Move context-dependent branch detail into `references/workflow-routing.md`. The workflow reference must express state transitions rather than a universal recipe: establish observation -> localize -> choose next distinguishing probe/reference/operator -> evaluate observation -> continue/exit.
- [ ] Treat `find-polluter.sh` as an operator: its executable behavior and test remain the authoritative owner. The workflow decides **when** it is useful; the skill must not duplicate its implementation semantics.
- [ ] Do not turn every debugging command into a new script. Promote behavior to a tool only when it is deterministic, reusable, and cheaper/more reliable than repeated agent interpretation.
- [ ] Verify the refactor does not broaden the skill description or preload TDD/verification.
- [ ] Run:

```bash
bash skills/systematic-debugging/test-find-polluter.sh
bash tests/codex/test-progressive-skill-loading.sh
```

Expected: pass.

- [ ] Run the explicit live unexplained-failure scenario through the existing probe and verify both positive selection and forbidden-collision checks.
- [ ] Commit:

```bash
git add skills/systematic-debugging/SKILL.md \
        skills/systematic-debugging/references/workflow-routing.md
git commit -m "refactor: split debugging workflow from operators"
```

## Workstream W5 — Canary Refactor 2: Skill Review and Layered Learning

**Files:**
- Modify: `skills/skill-review/SKILL.md`
- Modify: `skills/skill-review/references/audit-rubric.md`
- Modify: `skills/skill-review/references/budgeted-behavioral-learning.md`
- Create: `skills/skill-review/references/layered-evaluation.md`

**Produces:** explicit eval ownership and cadence without autonomous learning infrastructure.

- [ ] Create `layered-evaluation.md` as the detailed owner for evaluation questions by layer:
  - routing: selection, false/missed activation, collision, branch, stop, tool-family activation, token/latency cost;
  - workflow: transition quality, convergence, recovery, loops, handoff, capability floor;
  - tool/operator: contract correctness, determinism, error handling, compatibility, latency/output bounds, regression;
  - policy: invariant preservation, bypass resistance, cross-workflow consequence, authority/admissibility.
- [ ] Make evaluation answer two distinct questions in order: **what failed?** and **which layer owns the correction?**
- [ ] Update `budgeted-behavioral-learning.md` to preserve its current first-stage `CAPABILITY | STEERING | IMPLEMENTATION | ENVIRONMENT` classification, then map:
  - `CAPABILITY` -> tool/operator evaluation or normal capability owner;
  - `STEERING` -> `ROUTING | WORKFLOW | POLICY` attribution before proposing shared learning;
  - `IMPLEMENTATION` -> product/code regression path;
  - `ENVIRONMENT` -> fixture/runtime/config path.
- [ ] State explicitly that recurrence/material independence remains required for generalized shared steering changes except the existing high-impact exception.
- [ ] State explicitly that a confirmed deterministic tool correctness defect does **not** wait for recurrence; fix it under its contract/regression test. Semantic tool expansion/evolution remains slower and versioned.
- [ ] Encode the four cadences as evidence/admission cadence, never as an automatic schedule.
- [ ] Keep `SKILL.md` compact: it should route substantial audits to `audit-rubric.md`, layered eval to `layered-evaluation.md`, and learning admission to `budgeted-behavioral-learning.md`.
- [ ] Run:

```bash
bash tests/writing-skills/test-token-economics.sh
bash tests/explicit-skill-requests/test-explicit-skill-requests.sh
```

Expected: pass.

- [ ] Commit:

```bash
git add skills/skill-review/SKILL.md \
        skills/skill-review/references/audit-rubric.md \
        skills/skill-review/references/budgeted-behavioral-learning.md \
        skills/skill-review/references/layered-evaluation.md
git commit -m "refactor: separate routing workflow tool learning clocks"
```

## Workstream W6 — Refactor Large Orchestration Skills Only After the Canaries Are Green

**Files:**
- Modify: `skills/executing-plans/SKILL.md`
- Create: `skills/executing-plans/references/workflow-routing.md`
- Modify/reference canonical owners instead of copying them: `AGENTS.md`, `docs/mvl-laws.md`, `skills/test-driven-development/impact-radius-testing.md`, `skills/test-driven-development/remote-cdp-browser-lifecycle.md`, `skills/verification-before-completion/SKILL.md`
- Review, but do not automatically rewrite: `skills/subagent-driven-development/SKILL.md`

**Produces:** a large skill that demonstrates dynamic workflow routing without re-owning downstream policies and capabilities.

- [ ] Do not start W6 until W3-W5 tests and live routing evidence are green. This is a machine-verifiable dependency, not a human approval gate.
- [ ] Reduce `executing-plans/SKILL.md` to activation, continuous-execution lifecycle, plan/MVL continuity invariant, human-judgment stop boundary, and pointers to the dynamic workflow reference/canonical contracts.
- [ ] Move state-transition detail into `references/workflow-routing.md`: load/review plan -> prerequisite-ready path -> feature task path -> integration path -> MVL closure when applicable -> completion/branch handoff; include transitions back to debugging/TDD when observations invalidate the current state.
- [ ] Do not copy the full debugging, TDD, verification, browser, dependency, or review workflow into the executing-plans workflow. At a transition, let native matching/current-state loading select the owning skill or reference.
- [ ] Where a mechanical step already has a script/test owner (version sync, packaging validation, browser lifecycle helper, etc.), reference/invoke that owner rather than restating command semantics in the root skill.
- [ ] Preserve the existing rule that implementation on main/master requires explicit consent; this refactor does not alter authority.
- [ ] Review `subagent-driven-development/SKILL.md` for the same layer-mixing pattern. Refactor it only if the canary architecture clearly removes duplicated routing/policy text; otherwise record no change and avoid broadening this workstream.
- [ ] Run affected skill/request/loading tests and the existing progressive-loading suite.
- [ ] Commit:

```bash
git add skills/executing-plans/SKILL.md \
        skills/executing-plans/references/workflow-routing.md
git commit -m "refactor: make plan execution a routed workflow"
```

Include `skills/subagent-driven-development/SKILL.md` in the commit only if it was materially changed and independently verified.

## Workstream W7 — Catalog-Wide Layer Audit Without a Mass Rewrite

**Files:**
- Use: `skills/skill-review/SKILL.md`
- Update only skills that show a clear layer-ownership defect under the new rubric.
- Do not create a second inventory/ledger file; Git diff and the existing plan are the record.

**Produces:** bounded follow-up fixes rather than a repository-wide mechanical rewrite.

- [ ] Review high-frequency/core skills first: `test-driven-development`, `verification-before-completion`, `writing-plans`, `brainstorming`, `using-superpowers`, `subagent-driven-development`.
- [ ] For each, classify findings as:

```text
KEEP
ROUTING_REFACTOR
WORKFLOW_REFACTOR
TOOL_PROMOTION
POLICY_DEDUP
REFERENCE_RELOCATION
```

Do not persist this classification as a new long-lived ledger unless a concrete consumer needs it; apply clear fixes directly and use commit/diff history as evidence.

- [ ] Apply only changes with a concrete owner/cost benefit. Do not move files purely to create visually symmetric directories.
- [ ] For each `TOOL_PROMOTION`, require a focused deterministic test before deleting the corresponding natural-language instruction.
- [ ] For each routing change, add or update positive/negative/collision evidence in the smallest existing routing probe surface.
- [ ] For each workflow change, use the opt-in behavioral-learning rules when the change claims generalized learning rather than simple deduplication/refactoring.
- [ ] Run only tests invalidated by actual changes plus the final integration suite in W8.

**Commit:** group coherent related changes; do not combine unrelated skill migrations into one large commit.

## Workstream W8 — Final Verification, Token Regression, and Disposition

**Files:**
- Modify only if evidence requires it: `docs/benchmarks/2026-09-14-codex-progressive-skill-token-baseline.md` should remain the historical baseline.
- Create a new benchmark file only if the implementation materially changes measured routing/token behavior and the user wants the new result retained; do not overwrite the historical baseline.
- Update release/version files only at actual release time using existing repository version tooling.

- [ ] Run the repository-relevant deterministic suite:

```bash
bash tests/codex/test-progressive-skill-loading.sh
bash tests/writing-skills/test-token-economics.sh
bash tests/explicit-skill-requests/test-explicit-skill-requests.sh
bash tests/plugin-loader/test-plugin-loading.sh
bash skills/systematic-debugging/test-find-polluter.sh
```

Expected: all pass.

- [ ] Run three comparable live probe repetitions to evaluate routing/collision behavior and token variance using the same isolated fixture shape as the 2026-09-14 baseline:

```bash
for i in 1 2 3; do
  CODEX_PROBE_RETRIES=1 CODEX_PROBE_TIMEOUT=180 \
    bash tests/codex/live-progressive-skill-probe.sh || exit 1
done
```

Expected:
- all current-state routing scenarios pass;
- no forbidden neighboring workflow skill is observed when routing evidence is available;
- behavioral oracles remain green;
- no new mandatory meta-router or broad codebase-memory activation appears in bounded scenarios;
- median uncached-input/latency is compared with the 2026-09-14 reference using trace attribution, not a single-run threshold.

- [ ] Inspect any token regression before changing prompt text. Attribute it to one of: routing collision, extra workflow context, tool schema/payload, serial turns, repeated evidence, model/runtime variance. Change only the owning layer.
- [ ] Verify `AGENTS.md` remains constitutional and does not contain the detailed four-clock/runbook material.
- [ ] Verify no automated behavioral-learning trigger, scheduled eval, telemetry ledger, or automatic tool/policy mutation was introduced.
- [ ] Verify the canonical architecture has one owner (`docs/skill-runtime-architecture.md`) and `writing-skills`, `skill-review`, and core skills point to it instead of restating it independently.
- [ ] If release packaging/version changes are part of the implementation session, use the existing version script and run the repository's version/plugin checks. Do not invent a version number in this plan.

## Acceptance Criteria

The refactor is complete when all of the following are true:

- “Skill” is documented and implemented as a discovery/workflow package, not the owner of every invariant and mechanic.
- Native harness matching remains the preferred first-hop dispatcher; no mandatory meta-router returns.
- Routing is explicitly recurrent after observations, while workflows own state transitions and tools own deterministic executable behavior.
- Cross-cutting non-executable invariants remain in policy rather than being forced into tools or duplicated into every skill.
- The skill creator and skill review rubric can detect routing/workflow/tool/policy layer-mixing.
- The live Codex probe reports routing evidence separately from behavioral outcome and can detect forbidden neighboring skill activation.
- `systematic-debugging` demonstrates the target split with a compact root, routed workflow detail, and existing deterministic operator ownership.
- `skill-review` has separate routing/workflow/tool/policy eval ownership and preserves human-authorized learning.
- `executing-plans` no longer acts as a monolithic owner of downstream debugging/TDD/verification mechanics.
- Failure attribution precedes learning; routing evidence cannot mutate tools, and tool defects cannot silently expand routing policy.
- Routing, workflow, tool, and policy changes have distinct evaluation/admission cadences without scheduled or autonomous learning.
- Existing progressive-loading, explicit-skill, packaging, and canary tool tests pass.
- The three-run live comparison preserves selection behavior and shows no material attributable token/tool-loop regression versus the recorded 2026-09-14 baseline.

## Non-Goals

- Building a new agent orchestration engine or state-machine runtime.
- Replacing native skill discovery with a custom router.
- Moving every existing script into a new `tools/` directory.
- Converting all judgment into deterministic tooling.
- Automatically learning or mutating routing/workflows/tools/policies from telemetry.
- Creating a persistent failure/learning ledger, EvoDAG, or duplicate evidence store.
- Rewriting every skill in one release.
- Weakening existing security, authority, MVL, TDD, real-component, browser, or claim/evidence correctness boundaries.

## Implementation Order / Stop Rule

Execute W0 -> W1 -> W2 -> W3 -> W4 -> W5. Only proceed to the large `executing-plans` refactor in W6 after the canary routing and layered-eval evidence is green. W7 is bounded cleanup, not a requirement to touch every skill. W8 closes the refactor.

If a canary shows that the layered split increases token/tool-loop cost or makes native routing less reliable, fix or narrow the abstraction at the canary layer before migrating more skills. Do not compensate by adding a universal router or more always-loaded instructions.
