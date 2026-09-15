# Skill Token Economics

This document captures the token-economics principles validated during the Livingware Engineer 6.8.x Codex optimization work and refined by the layered skill-runtime design. It is a design and review reference, not a fixed performance SLA.

The canonical ownership and counterfactual-evaluation model lives in `docs/skill-runtime-architecture.md`. Token economics measures the whole execution/evaluation loop; it does not redefine layer semantics.

## Optimization order

Optimize in this order:

1. **Do not load unnecessary context.** A token that never enters context is cheaper than a cached token.
2. **Load only the current workflow state.** Do not preload downstream skills because they may become relevant later.
3. **Avoid activation collisions.** Overlapping descriptions can cause multiple skills or tool families to activate for one bounded task.
4. **Keep root skills compact.** Put activation, entry/exit conditions, hard local invariants, and the minimum execution contract in `SKILL.md`; move workflow depth, examples, long checklists, platform mechanics, browser procedures, and model compensation behind progressive disclosure.
5. **Move genuinely deterministic mechanics to executable owners.** Prefer scripts/tools/tests when they remove repeated interpretation and their invocation/schema/output cost is lower than carrying the rule as prose across the workflow.
6. **Avoid redundant runtime capability.** If the harness already performs skill discovery/matching, do not add a mandatory meta-router that reimplements it.
7. **Control tool economics.** Broad repository indexing, graph discovery, large listings, long histories, and repeated test/status commands can dominate context cost even when the skill body is small.
8. **Reuse evidence.** Do not rerun or restate valid unchanged tests, diffs, or verification evidence merely because the workflow phase changed.
9. **Reduce serial turns.** Combine independent read-only checks and avoid one-action-per-turn ceremony. Parallelize independent work when the harness supports it.
10. **Bound tool output.** Use focused paths, result limits, exact ranges, and concise structured output instead of returning large repository or log payloads.
11. **Use counterfactual evaluation only when its expected information value exceeds its cost.** Prefer deterministic replay before stochastic simulation and simulation before expensive real re-execution when the cheaper stage can eliminate alternatives.
12. **Only then shorten wording.** Lexical compression is the last optimization, not the first.

## Layered cost model

Review cost by owner rather than treating one `SKILL.md` as the whole system:

```text
fixed/static context
+ routing/discovery context
+ selected workflow context
+ conditional references
+ tool schemas
+ tool request/response payloads
+ repeated context across serial turns
+ generated reasoning/output
+ retries/re-execution
+ optional simulation/replay cost
```

A local optimization is not an improvement if it shifts cost into more routing mistakes, tool calls, retries, or verification turns.

## Skill architecture

A frequently selected root skill should normally contain only:

- a precise activation description,
- entry and exit conditions when stateful,
- hard local invariants whose violation has a concrete consequence,
- the smallest sufficient workflow contract,
- explicit progressive-disclosure pointers,
- tool-economy rules when broad discovery is a plausible failure mode.

Reusable transition depth belongs in workflow references. Conditional knowledge belongs in references. Deterministic mechanics belong in executable owners when promotion is justified. Cross-cutting non-executable invariants belong to their policy owner.

## Activation design

Descriptions are part of runtime economics because they determine what is selected.

- Describe the current state that requires the skill, not every adjacent task it might eventually help with.
- Make neighboring workflow states mutually distinguishable when possible.
- State exclusions when they prevent observed collisions, such as unresolved diagnosis vs implementation vs completion claim.
- Do not give descriptions excessive “pick me” breadth.
- Do not activate repository-graph or other expensive discovery for bounded/local work unless direct inspection leaves material structural uncertainty.

A skill should not orchestrate another skill merely because the workflow may eventually reach it. Leave the current skill at its exit condition and let native matching/current-state routing select the next owner.

## Operator-promotion economics

Moving prose into a tool is beneficial only when the total loop becomes cheaper or more reliable.

Prefer an executable operator when:

- behavior is deterministic or mechanically testable;
- it is reused across multiple episodes/workflows;
- natural-language interpretation causes variance or repeated instruction cost;
- the tool can return bounded output; and
- a focused regression test can own its contract.

Do not promote behavior when the script/tool schema and returned payload cost more than a short stable rule, or when the decision fundamentally requires contextual judgment.

## Tool-cost review

Ask:

- Did the agent read a large skill/workflow body that could have been conditional?
- Did it attempt a stale or nonexistent skill path before the real one?
- Did it index/map a repository already bounded to one or two files?
- Did it enumerate all projects when the active project was known?
- Did a tool return tens of kilobytes when a focused snippet would suffice?
- Were tests, status, diff, and source reads split across more turns than necessary?
- Was completion verification activated merely to summarize implementation results?
- Was valid evidence rerun after no relevant state changed?
- Did moving a rule into a tool reduce interpretation variance but add a larger schema/payload tax?

## Counterfactual evaluation economics

Counterfactual evaluation is maintenance/evaluation work, not a default step in ordinary development.

Use the cheapest mode that can materially reduce uncertainty:

```text
existing observed evidence
  -> deterministic REPLAY
  -> bounded seeded MONTE_CARLO when uncertainty remains
  -> REAL_REEXECUTION for promising alternatives when practical
```

Do not generate large simulation campaigns merely because they are cheaper than model calls. Ten thousand rollouts from one modeled basis are still one modeled basis and cannot replace materially independent observed evidence.

Track simulation cost separately from predicted savings:

- CPU/runtime used by replay or rollout;
- fixture/model construction cost;
- tokens used to generate/interpret parameters;
- artifact/output size returned to the agent;
- number of alternatives eliminated before real evaluation;
- avoided real executions/tool calls, when defensibly measurable.

Prefer summary statistics and sensitivity/provenance reports over feeding raw rollout traces back into the model context.

## Evidence reuse and provenance

Cost reduction cannot blur evidence status. Preserve `OBSERVED | REPLAYED | SIMULATED | INFERRED | ASSUMED` provenance as defined by the architecture.

Replayed/simulated results can reduce the number of real candidates worth testing. They cannot be counted as independent observed episodes for generalized behavioral learning, so do not optimize by replacing required empirical validation with synthetic volume.

## Prefix caching

Stable static prefixes are useful, but cache optimization comes after context elimination. Keep system instructions, tool definitions, and frequently reused root contracts structurally stable so remaining context can benefit from prefix caching. Do not preserve unnecessary context merely because it may be cached.

## Measurement

Use realistic live probes when optimizing a high-frequency skill. Prefer an isolated fixture when measuring skill overhead so a large host repository does not contaminate the result.

Track at least:

- required-skill selection accuracy,
- forbidden/cross-skill activation rate,
- unnecessary tool-family activation rate,
- route/branch reversals when observable,
- median latency,
- input count,
- cached-input count,
- uncached-input count,
- output count,
- reasoning-output count,
- bounded tool-output volume when material.

When evaluating counterfactual tooling also track:

- replay/simulation runtime,
- rollout count and seed,
- provenance mix,
- alternatives eliminated,
- real re-executions still required.

Use repeated runs and medians for live model behavior. Single-run counts can vary with model execution paths. Seeded simulator output should be deterministic for a fixed fixture/seed after normalization.

## Empirical lesson from Livingware 6.8.x

The largest improvements came from architecture, not sentence trimming:

- native matcher instead of a mandatory meta-router,
- current-state skill loading instead of preloading debugging/TDD/verification together,
- compact root contracts with detailed playbooks behind progressive disclosure,
- bounded source/test inspection instead of automatic codebase-memory discovery,
- preventing ordinary implementation-result reporting from triggering completion verification.

In the isolated Codex probe, these changes materially reduced uncached input and latency while preserving correct skill selection and engineering invariants. See `docs/benchmarks/2026-09-14-codex-progressive-skill-token-baseline.md` for the recorded benchmark and variance notes.

The next optimization frontier is path economics: better routing attribution, fewer unnecessary tool families/turns, and selective what-if evaluation that reduces expensive real experiments without pretending simulation is reality.

## Stop condition

Stop reducing context or adding evaluation machinery when marginal savings/information no longer justify complexity or runtime cost. Never remove hard correctness, security, authority, integration, browser, evidence-provenance, or learning-admission invariants merely to lower token counts.
