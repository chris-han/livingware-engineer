# Skill Token Economics

This document captures the token-economics principles validated during the Livingware Engineer 6.8.x Codex optimization work. It is a design and review reference, not a fixed performance SLA.

## Optimization order

Optimize in this order:

1. **Do not load unnecessary context.** A token that never enters context is cheaper than a cached token.
2. **Load only the current workflow state.** Do not preload downstream skills because they may become relevant later.
3. **Avoid activation collisions.** Overlapping descriptions can cause multiple skills or tool families to activate for one bounded task.
4. **Keep root skills compact.** Put entry/exit conditions, hard invariants, and the minimum execution contract in `SKILL.md`; move examples, long checklists, platform mechanics, browser procedures, and model compensation behind references.
5. **Avoid redundant runtime capability.** If the harness already performs skill discovery/matching, do not add a mandatory meta-router that reimplements it.
6. **Control tool economics.** Broad repository indexing, graph discovery, large listings, long histories, and repeated test/status commands can dominate context cost even when the skill body is small.
7. **Reuse evidence.** Do not rerun or restate valid unchanged tests, diffs, or verification evidence merely because the workflow phase changed.
8. **Reduce serial turns.** Combine independent read-only checks and avoid one-action-per-turn ceremony. Parallelize independent work when the harness supports it.
9. **Bound tool output.** Use focused paths, result limits, exact ranges, and concise structured output instead of returning large repository or log payloads.
10. **Only then shorten wording.** Lexical compression is the last optimization, not the first.

## Skill architecture

A frequently selected skill should normally contain only:

- a precise activation description,
- entry and exit conditions when stateful,
- hard invariants whose violation has a concrete consequence,
- the smallest sufficient workflow contract,
- explicit progressive-disclosure pointers,
- tool-economy rules when broad discovery is a plausible failure mode.

Conditional material belongs in references. Examples include browser/CDP lifecycle rules, detailed debugging playbooks, impact-radius procedures, long examples, rationalization lists, platform-specific tool mapping, and weaker-model compensation.

## Activation design

Descriptions are part of the runtime economics because they determine what is selected.

- Describe the state that requires the skill, not every adjacent task it could possibly help with.
- Make neighboring workflow states mutually distinguishable when possible.
- State important exclusions when they prevent observed collisions, for example: unresolved diagnosis vs implementation vs completion claim.
- Do not give descriptions excessive “pick me” breadth.
- Do not activate repository-graph or other expensive discovery skills for bounded/local work unless direct inspection leaves material structural uncertainty.

A skill should not orchestrate another skill merely because the workflow may eventually reach it. Leave the current skill at its exit condition and let native matching select the next state.

## Tool-cost review

Prompt size is only one component of agent cost. Review the whole loop:

```text
static context
+ selected skill body
+ tool schemas
+ tool request/response payloads
+ repeated context across serial turns
+ generated output/reasoning
```

Ask:

- Did the agent read a large skill body that could have been a conditional reference?
- Did it attempt a stale or nonexistent skill path before the real one?
- Did it index or map a repository that was already bounded to one or two files?
- Did it enumerate all projects when the active project was known?
- Did a tool return tens of kilobytes when a focused snippet would suffice?
- Were tests, status, diff, and source reads split across more turns than necessary?
- Was completion verification activated merely to summarize implementation results?
- Was valid evidence rerun after no relevant state changed?

## Prefix caching

Stable static prefixes are useful, but cache optimization comes after context elimination. Keep system instructions, tool definitions, and frequently reused root contracts structurally stable so they can benefit from prefix caching. Do not preserve unnecessary context merely because it may be cached.

## Measurement

Use realistic live probes when optimizing a high-frequency skill. Prefer an isolated fixture when measuring skill overhead so a large host repository does not contaminate the result.

Track at least:

- skill-selection accuracy,
- cross-skill activation rate,
- unnecessary tool-family activation rate,
- median latency,
- input count,
- cached-input count,
- uncached-input count,
- output count,
- reasoning-output count.

Use repeated runs and medians. Single-run counts can vary with model execution paths.

## Empirical lesson from Livingware 6.8.x

The largest improvements came from architecture, not sentence trimming:

- native matcher instead of a mandatory meta-router,
- current-state skill loading instead of preloading debugging/TDD/verification together,
- compact root contracts with detailed playbooks behind progressive disclosure,
- bounded source/test inspection instead of automatic codebase-memory discovery,
- preventing ordinary implementation-result reporting from triggering completion verification.

In the isolated Codex probe, these changes materially reduced uncached input and latency while preserving correct skill selection and engineering invariants. See `docs/benchmarks/2026-09-14-codex-progressive-skill-token-baseline.md` for the recorded benchmark and variance notes.

## Stop condition

Do not optimize a skill indefinitely. Stop reducing context when further cuts would remove hard correctness, security, authority, integration, browser, or evidence invariants, or when remaining cost is dominated by model/runtime/tool behavior outside the skill body.
