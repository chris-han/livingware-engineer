# Budgeted Behavioral Learning

Behavioral evaluation and workflow learning are opt-in maintenance activities. They are not correctness gates for ordinary development and must not run automatically in CI, after skill edits, during version bumps, on a schedule, or merely because spare token budget exists.

## Suggestion gate

The agent may suggest a targeted workflow-learning eval only when all three conditions are satisfied:

1. **Recurrence** — the same underlying workflow behavior has appeared in at least two materially independent failure episodes, or the user has independently corrected the same behavior more than once.
2. **Systemic scope** — existing evidence plausibly points to a shared skill, instruction, routing rule, review policy, or interaction between them rather than a local defect.
3. **Actionable uncertainty** — the agent can name one concrete workflow decision a targeted eval could resolve.

If any condition is `NO` or cannot be established cheaply from existing evidence, stay silent and continue normal work.

### High-impact exception

A single event may justify a suggestion without recurrence only when all are true:

- the cause is clearly framework-level;
- waiting for recurrence would expose the user or system to material risk; and
- a targeted eval can test a concrete policy correction.

Token waste, one unnecessary test, one premature stop, one unnecessary review, or one wrong routing choice do not qualify by themselves.

### Anti-noise rule

Accumulated changes, elapsed time, release cadence, corpus availability, general suspicion, or spare token budget are never sufficient reasons to suggest learning. Do not suggest an eval merely because it has not run recently.

## Recurring failure

A failure is recurring when the same underlying workflow behavior appears in at least two materially independent failure episodes. Match the behavioral pattern, not exact wording or surface symptoms.

Examples include premature stopping, unnecessary reviewer dispatch, duplicate artifact generation, over-broad testing, incorrect evidence-lane routing, or artificial RED requirements for behavior-preserving refactors.

Do not count retries of one unresolved task, downstream symptoms of one mistake, parallel agents sharing faulty state, or repeated failures from one unchanged broken fixture, dependency, environment, or configuration as separate occurrences.

## Material independence

Treat two occurrences as materially independent only if every prompt below is `YES`:

1. **Did the earlier task or execution end before the later occurrence began?**
2. **Was the later occurrence reached without reusing the earlier occurrence's faulty intermediate state or downstream output?**
3. **Was every known local cause from the earlier occurrence absent, fixed, or independently re-created in the later occurrence?**
4. **Did the shared workflow rule execute again rather than merely continue the earlier execution?**

Decision:

```text
YES to all four -> INDEPENDENT
Any NO          -> SAME FAILURE EPISODE
UNKNOWN         -> treat as NO unless cheaply resolved
```

Different agents, models, harnesses, repositories, execution paths, user journeys, or elapsed time do not override this test.

### Handling UNKNOWN

Resolve `UNKNOWN` only when existing evidence can answer it with small incremental effort and the answer could change whether a workflow-learning suggestion is permitted. Do not create new logs, traces, reports, experiments, broad searches, or evidence artifacts merely to prove independence. If meaningful extra work or token cost would be required, keep `UNKNOWN` and treat the occurrences as one failure episode.

## Systemic attribution

After recurrence is established, ask whether existing evidence plausibly attributes the behavior to a shared workflow rule. If the answer is `NO` or `UNKNOWN`, fix the local cause and do not suggest learning. Do not perform a broad framework investigation solely to convert `UNKNOWN` into `YES`.

Typical local explanations include a task-specific misunderstanding, broken fixture, malformed plan, repository-specific convention, transient service failure, or implementation defect already contained by a regression test.

## Actionable eval question

Before suggesting learning, the agent must be able to complete:

> A targeted eval would help decide whether __________.

If no single concrete policy decision can fill the blank, stay silent.

## Suggestion format

Keep the suggestion minimal:

```text
Observed pattern: <minimal concrete evidence>
Suspected shared cause: <skill/rule/interaction>
Targeted eval question: <one policy decision>
```

Then ask whether the user wants to run that targeted eval. Do not automatically generate a learning report, corpus plan, scenario inventory, retrospective, or policy patch.

## Human initiation and budget discipline

A suggestion never authorizes execution. The user must explicitly initiate the run. Once initiated:

1. select the smallest scenario subset that can falsify the suspected pattern;
2. reuse existing observations instead of regenerating equivalent evidence;
3. expand only when initial findings or material interaction risk justify the added cost;
4. report behavior deltas and proposed rule changes concisely; and
5. treat shared-policy changes as proposals requiring human adoption, never autonomous mutations.

A full corpus is exceptional. Do not create a continuous self-improvement loop.
