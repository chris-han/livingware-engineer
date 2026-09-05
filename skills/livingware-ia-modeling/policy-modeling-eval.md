# Behavioral Eval: Conditional Institutional Policy

## Prompt

Model the following institutional policy as a governed ContextGraph candidate:

> Employees may purchase project materials before contract signature only when the project manager has approved an emergency exception. The purchase must be supported by an invoice and the exception expires after 30 days.

Return the semantic definitions, usages/occurrences if any, relation families, reified constraints/requirements, evidence requirements, authority metadata that must remain explicit, and any conclusions that must be deferred to evaluation.

## Pass Criteria

A passing response must:

- separate reusable definitions from concrete occurrences;
- model the emergency permission as a structured requirement/constraint rather than a single `MAY_PURCHASE` edge;
- represent the invoice as an evidence requirement, not proof that a particular purchase is compliant;
- preserve the 30-day temporal condition explicitly;
- keep authority/governance independent from topology;
- defer `compliant`, `satisfied`, `violated`, or equivalent conclusions to evaluation;
- avoid requiring SysML as the runtime representation.

## Known RED Attempt

On 2026-09-05, an attempted clean Codex baseline could not complete because the Codex transport repeatedly timed out/reconnected. This file records the intended behavioral eval so RED/GREEN can be rerun when the harness is reachable; it does not claim a completed baseline result.
