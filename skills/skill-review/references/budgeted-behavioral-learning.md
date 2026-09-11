# Budgeted Behavioral Learning

Behavioral evaluation and workflow learning are opt-in maintenance activities. They are not correctness gates for ordinary development and must not run automatically in CI, after every skill edit, during routine version bumps, or merely because a corpus exists.

## When an agent may suggest a run

A suggestion is justified only when accumulated evidence indicates a plausible framework-level pattern rather than an isolated task defect. Strong signals include:

- the same workflow failure appears independently two or more times;
- the user repeatedly corrects the same agent behavior;
- several recent changes affect the same core instruction surfaces and interaction risk is now material;
- a real task reveals behavior that cannot reasonably be explained as one implementation bug;
- a larger Livingware release is approaching after substantive workflow changes.

Do not suggest a run for a one-off mistake, copy edit, local typo, already-contained regression, or simply because evals have not run recently.

Before suggesting, the agent must be able to state all three:

1. the accumulated evidence;
2. the suspected repeated or systemic pattern;
3. the concrete workflow or policy decision the eval could improve.

If any of the three is missing, continue normal work without suggesting learning.

## Human initiation boundary

The agent may recommend a run; it may not start one autonomously. Explicit user initiation is required because the work primarily spends tokens and review attention on long-horizon framework quality rather than the correctness of the current task.

Do not turn the recommendation into an approval ceremony for ordinary work. Current development continues under existing rules unless the user separately asks to run the maintenance evaluation.

## Budget discipline after initiation

Once explicitly initiated:

1. select the smallest scenario subset that can falsify the suspected pattern;
2. reuse existing observations instead of regenerating equivalent evidence;
3. expand to a broader corpus only when initial findings, cross-skill interaction risk, or release risk justify the additional cost;
4. report behavior deltas and likely rule changes concisely;
5. treat proposed policy changes as proposals requiring human adoption, not autonomous mutations.

A full corpus is exceptional, not the default. Do not create a continuous self-improvement loop that repeatedly evaluates, rewrites, and re-evaluates Livingware without a new explicit user instruction.

## Canonical flow

```text
normal engineering
  -> no behavioral eval

repeated/systemic evidence accumulates
  -> agent may suggest one targeted learning run
  -> ordinary engineering does not pause

human explicitly initiates
  -> smallest relevant scenario subset
  -> inspect behavioral deltas
  -> expand only if justified
  -> propose policy changes
  -> human decides adoption
```

## Cost test

Use the same total-cost principle as the rest of Livingware Engineer: a learning run is justified only when its expected reduction in future workflow failure, wasted work, or recurring token cost plausibly exceeds the tokens, tool calls, review time, and maintenance it consumes.
