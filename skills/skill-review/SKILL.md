---
name: skill-review
description: Review SKILL.md and AGENTS.md instructions for activation noise, unnecessary always-on context, weak progressive disclosure, obsolete or unsupported model scaffolding, and unclear decision or completion boundaries.
---

# Skill Review

Use this skill to audit agent instruction surfaces such as `SKILL.md`, `AGENTS.md`, repository agent guidance, or an installed skill set.

The goal is not brevity for its own sake. Minimize always-loaded instruction cost while preserving constraints whose violation has a concrete consequence and retaining extra scaffolding when supported models demonstrably need it.

## Review method

1. Inventory the instruction surfaces in scope and identify the supported model/platform mix when known.
2. Review skill descriptions before bodies. Flag descriptions that are broad, overlapping, contradictory, or have excessive “pick me” energy.
3. For each skill, separate routing information, selected-workflow guidance, conditional detail that should move behind progressive disclosure, genuine invariants or safety boundaries, and model/platform-specific compensation.
4. Review `AGENTS.md` as universally loaded repository context. Ask whether each instruction is needed for nearly every task or should instead be a contextual pointer or adapter-specific rule.
5. Flag obsolete or unsupported model-compensation rules, especially blanket requirements to map the repository, read large doc stacks, ask for approval at every step, run broad tests, brainstorm, plan, or follow a fixed itinerary regardless of task shape.
6. For retained scaffolding, ask what evidence justifies it, which supported model needs it, whether it harms another supported model, and whether it can move into an adapter or conditional reference.
7. Check decision and completion boundaries. Preserve real authority and safety limits; remove unnecessary stop gates. Where useful, state safe autonomy and a concrete definition of done.
8. Produce a prioritized audit with concrete rewrite recommendations. Prefer deleting or relocating whole classes of unnecessary instruction over merely shortening sentences.

## Behavioral learning is opt-in maintenance

Do not automatically run a behavioral eval corpus, agent-configuration regression suite, or workflow-learning loop as part of ordinary skill review, CI, version bumps, or completion. Those activities consume model turns and tokens for long-horizon framework improvement rather than current-task correctness.

An agent may suggest a targeted behavioral-learning run only when enough relevant evidence has accumulated to make the expected learning value plausibly exceed its token and review cost. The suggestion must name: (1) the accumulated evidence, (2) the suspected repeated or systemic workflow pattern, and (3) the concrete framework decision an eval could improve. If those cannot be named, do not suggest a run.

A suggestion never authorizes execution. The user must explicitly initiate the run. Once initiated, start with the smallest relevant scenario subset and expand only when findings or release risk justify it. Learning output may propose rule changes, but must not autonomously modify shared workflow policy.

Read `references/budgeted-behavioral-learning.md` only when evaluating whether to suggest or conduct such a maintenance run.

## Principles

- Apply MVL Law 1 first: flag unconditional workflow stops that could remain recorded and inspectable while defaulting to pass-through. Preserve true security, authority, destructive-operation, and irreversible-external-action boundaries.
- Keep skill descriptions as short as possible while still discriminating when the skill should be used.
- Avoid overlapping activation surfaces unless the distinction is obvious from the descriptions.
- Prefer progressive disclosure. Multi-workflow skills should use the root `SKILL.md` as a minimal router into references, scripts, or workflow-specific files.
- Avoid elaborate itineraries when capable models can infer reasonable steps. Prescribe sequences only where order matters, deviation creates concrete risk, or evidence shows a supported model requires the extra scaffolding.
- Treat `AGENTS.md` as a repository constitution, not a universal runbook.
- Preserve hard invariants: security, authority, destructive-operation limits, deterministic correctness requirements, architecture laws, and other boundaries with real consequences.
- Verification should be proportionate to the affected surface unless the repository has a concrete reason for stronger coverage.
- Do not require approval at every intermediate step for safe local work. Make stop conditions explicit where they matter.
- Define completion for workflows that should continue through implementation, inspection, and repair.
- Prefer model-neutral, outcome- and invariant-oriented guidance in shared skills. Retain model-specific compensation when evidence supports it, but isolate it in platform/model adapters or conditional references when possible.
- Do not assume guidance optimized for one strong model is automatically optimal for weaker or differently-behaving supported models.

## Output

For substantial audits, return:

- instruction inventory and effective scope,
- supported model/platform mix when known,
- highest-risk issues first,
- per-skill verdict: `KEEP`, `TRIM`, `REFACTOR`, `MERGE`, or `REMOVE`,
- `AGENTS.md` findings split into `KEEP ALWAYS LOADED`, `ROUTE`, and `RELOCATE/REMOVE`,
- activation-collision findings,
- progressive-disclosure opportunities,
- single-model optimization findings,
- multi-model compatibility findings,
- evidence assessment for extra scaffolding,
- model/platform rules that should move into adapter references,
- decision-boundary and persistence findings,
- a concrete target structure or patch plan.

Use `references/audit-rubric.md` for systematic scoring. Read `references/article-principles.md` when the review should be explicitly grounded in Eric Provencher's “Rethinking skills and prompts for GPT-6 Astra”.
