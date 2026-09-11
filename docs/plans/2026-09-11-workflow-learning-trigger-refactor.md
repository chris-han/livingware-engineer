# Workflow Learning Trigger Refactor Plan

## Goal

Make workflow-learning suggestions precise, low-noise, and cheap: the agent may recommend a targeted eval only when existing evidence shows a recurring, materially independent, plausibly systemic workflow problem and the eval can answer one concrete policy question. Behavioral evals remain explicitly human-initiated.

## Constraints

- No automatic evals, CI gates, hooks, schedules, corpus generation, telemetry, learning ledger, or automatic policy mutation.
- No new default incident, intent, learning, or evidence artifact.
- Reuse evidence already present in tasks, tests, Git, and explicit user corrections.
- If recurrence or attribution cannot be established cheaply, stay silent.
- Keep detailed trigger logic behind progressive disclosure; keep `AGENTS.md` concise.

## Required behavior

A normal learning suggestion requires all three:

1. **Recurrence:** the same underlying workflow behavior appears in at least two materially independent failure episodes, or the user independently corrects the same behavior more than once.
2. **Systemic scope:** existing evidence plausibly points to a shared skill, instruction, routing rule, review policy, or interaction rather than a local defect.
3. **Actionable uncertainty:** one concrete policy decision can be tested by a targeted eval.

A single event may bypass recurrence only when it is clearly framework-level, waiting for recurrence creates material risk, and a targeted eval can test a concrete correction.

Accumulated changes, elapsed time, release cadence, corpus availability, spare token budget, or general suspicion never suffice by themselves.

## Material-independence rule

Two occurrences count as independent only when all four answers are `YES`:

1. Did the earlier task or execution end before the later occurrence began?
2. Was the later occurrence reached without reusing the earlier occurrence's faulty intermediate state or downstream output?
3. Was every known local cause from the earlier occurrence absent, fixed, or independently re-created later?
4. Did the shared workflow rule execute again rather than merely continue the earlier execution?

Any `NO` means one failure episode. `UNKNOWN` is treated as `NO` unless existing evidence can resolve it with small incremental cost and the answer would change whether a learning suggestion is allowed. Do not create new evidence solely to resolve independence.

## Implementation

1. Make `skills/skill-review/references/budgeted-behavioral-learning.md` the single detailed owner for recurrence, material independence, `UNKNOWN`, systemic attribution, the high-impact exception, actionable eval questions, and the suggestion format.
2. Reduce `skills/skill-review/SKILL.md` to routing plus the opt-in invariant; do not duplicate detailed trigger logic.
3. Keep `AGENTS.md` to one compact framework-learning principle referencing repeated materially independent evidence, shared-rule attribution, concrete eval value, human initiation, and smallest-relevant scope.
4. Do not add runtime code or behavioral-eval infrastructure.
5. Bump all release manifests consistently from `6.5.27` to `6.5.28`.

## Sanity cases

- Same unresolved task retried twice -> one episode; stay silent.
- Two completed independent tasks both stop prematurely -> recurrence candidate.
- Two agents fail from the same broken fixture -> one episode.
- Same behavior reappears in a fresh execution after the local cause was removed -> independent recurrence candidate.
- Independence cannot be established cheaply -> treat as one episode; stay silent.
- One clearly dangerous framework-level failure -> high-impact exception may permit a targeted-eval suggestion.

## Completion criteria

- One detailed policy owner exists.
- Root instruction surfaces do not duplicate the binary decision logic.
- `UNKNOWN` has deterministic low-cost handling.
- Ordinary local failures do not trigger learning suggestions.
- Suggestions remain human-authorized and targeted.
- No new default output or automatic learning activity exists.
- Every version manifest reports `6.5.28`.
