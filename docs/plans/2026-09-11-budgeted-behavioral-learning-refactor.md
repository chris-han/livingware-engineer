# Budgeted Behavioral Learning Refactor Plan

## Goal

Add a low-frequency, human-initiated behavioral-learning lane to Livingware Engineer without turning behavioral evals into automatic CI, routine completion work, or a new source of token waste.

## Design decision

Behavioral evaluation is framework maintenance, not default execution. The agent may suggest a targeted run only after repeated or systemic evidence has accumulated and only when it can name the evidence, suspected framework-level pattern, and concrete decision the run could improve. A suggestion does not authorize execution; the user explicitly initiates the run.

## Scope

1. Add one concise always-loaded core principle stating that framework learning is budgeted and never starts autonomously.
2. Put the operational rules behind progressive disclosure in `skills/skill-review`, because skill/agent-instruction review is the natural owner of framework-level behavior evaluation.
3. Define a small trigger policy: repeated independent failures, repeated user correction, interacting core-rule changes, systemic workflow evidence, or a substantive release boundary.
4. Require smallest-relevant-corpus-first execution after human initiation, with expansion only when evidence or release risk justifies the cost.
5. Keep policy mutation human-adopted: eval output may propose rule changes but cannot autonomously rewrite shared workflow policy.
6. Bump the plugin version consistently across repository manifests.

## Non-goals

- Do not add an automated behavioral-eval corpus runner.
- Do not add a CI gate, cron job, hook, or version-bump trigger for behavioral evals.
- Do not create a new evidence ledger, learning database, or persistent workflow telemetry system.
- Do not pause ordinary engineering while waiting for a learning decision.
- Do not introduce a token-budget service or automatic budget estimator.

## Acceptance

- Ordinary development contains no new automatic eval step.
- The agent can recommend learning only when it can state accumulated evidence, suspected systemic pattern, and expected decision value.
- Explicit user initiation is required before any behavioral eval or learning run.
- Initiated runs start with the smallest relevant scenario subset and reuse existing observations where possible.
- Shared policy changes remain human-adopted.
- Version manifests agree on the new release number.
