---
name: skill-review
description: Review SKILL.md and AGENTS.md instructions for activation noise, layer mixing, weak progressive disclosure, token/tool-loop cost, unsupported scaffolding, and unclear decision or completion boundaries.
---

# Skill Review

Use this skill to audit agent instruction surfaces such as `SKILL.md`, `AGENTS.md`, repository guidance, or an installed skill set.

The goal is not brevity for its own sake. Minimize always-loaded instruction cost while preserving hard constraints and assigning every rule to its smallest durable owner.

## Review method

1. Inventory the instruction surfaces in scope and the supported model/platform mix when known.
2. Review descriptions before bodies. Flag broad, overlapping, contradictory, or excessive “pick me” activation language.
3. Classify each instruction by owner using `../../docs/skill-runtime-architecture.md`: `TOOL/OPERATOR`, `POLICY`, `WORKFLOW`, `ROUTING`, or conditional `REFERENCE`.
4. Flag deterministic mechanics repeated as prose, dynamic choices frozen into universal sequences, cross-cutting policy duplicated into skills, and references eagerly loaded without current need.
5. Review `AGENTS.md` as constitutional always-loaded context. Route task-specific runbooks elsewhere.
6. Check neighboring-state boundaries and likely activation collisions.
7. Audit whole-loop token economics: routing context, selected workflow context, references, tool schemas/payloads, serial turns, repeated evidence, and unnecessary simulation/re-execution.
8. Check decision and completion boundaries. Preserve real authority/safety limits; remove ceremonial stops.
9. Attribute observed failures before proposing learning or structural changes.
10. Return prioritized changes with one authoritative owner for each rule.

## Detailed evaluation

For substantial evaluation or failure attribution, read `references/layered-evaluation.md`. It owns evaluation questions for routing, workflow, tool/operator, and policy layers, including counterfactual evidence provenance.

For systematic scoring, read `references/audit-rubric.md`.

## Token economics

Read `../../docs/skill-token-economics.md` for frequently loaded skills, overlapping activation, or unexpectedly high latency/context cost. Optimize architecture before wording: eliminate unnecessary loading, prevent collisions, bound tool output, reuse evidence, reduce serial turns, then improve cache stability and wording.

A smaller prompt that causes extra tool turns, weaker verification, more retries, or repeated real executions is not an optimization.

## Behavioral learning is opt-in maintenance

Do not run behavioral evals or shared workflow learning automatically. When repeated/systemic steering evidence makes learning relevant, read `references/budgeted-behavioral-learning.md`. It owns recurrence, material independence, evidence sufficiency, marginal future-impact admission, historical execution-basis preservation, counterfactual/simulation admission, and human initiation.

`REPLAYED`, `SIMULATED`, `INFERRED`, or `ASSUMED` evidence may narrow a real eval but cannot become materially independent observed evidence. `REAL_REEXECUTION` counts as `OBSERVED` only when the declared real comparable fixture/environment actually runs.

## Principles

- Skill is a discovery/workflow-entry package, not the owner of every invariant and mechanic.
- Native harness matching is the preferred first-hop dispatcher where available.
- Routing is recurrent after observations; workflow owns reusable transition structure; tools own deterministic mechanics; policy owns stable cross-cutting constraints.
- Learning/change authority follows failure attribution and the smallest durable owner.
- Prefer progressive disclosure and current-state loading.
- Preserve security, authority, destructive-operation, architecture, real-component, browser-evidence, and correctness invariants.
- Keep model/platform compensation isolated when possible and require evidence for universal scaffolding.
- Simulation narrows search; real execution remains the judge for empirical claims.

## Output

For substantial audits, return:

- effective instruction inventory and supported platform/model mix when known;
- highest-risk findings first;
- per-skill verdict: `KEEP`, `TRIM`, `REFACTOR`, `MERGE`, or `REMOVE`;
- layer-owner findings: `TOOL`, `POLICY`, `WORKFLOW`, `ROUTING`, `REFERENCE`;
- activation/collision and progressive-disclosure findings;
- token-economics findings across context, tools, turns, simulation, and re-execution;
- evidence provenance and failure attribution where learning is proposed;
- `AGENTS.md` findings split into `KEEP ALWAYS LOADED`, `ROUTE`, and `RELOCATE/REMOVE`;
- a concrete target structure or patch plan.

Read `references/article-principles.md` only when the review should explicitly use Eric Provencher's “Rethinking skills and prompts for GPT-6 Astra”.
