---
name: frontend-design
description: Use for frontend user-task flows, information architecture, semantic ownership, design-system-constrained UI implementation and UX reviews. For standalone Impeccable visual-craft commands with unchanged IA, use impeccable instead; not for backend-only tasks.
---

# Frontend Design

## MVL Law 1 — Fast-to-Aha

**REQUIRED:** Apply `docs/mvl-laws.md` MVL Law 1 first. Preserve governance boundaries, but keep normal low-risk product paths default-pass. Flag approval ceremony that delays the first useful result without changing risk.

## IA Before UI

For new UI, material task-flow/IA changes, or a review disputing existing IA, apply `docs/ia-before-ui.md` before visual choices. Establish or revalidate the JTBD, cognitive-work allocation, task flow, semantic owners, states/recovery and responsive hierarchy, and bind the current project design. For an IA-preserving fix or visual refinement, reuse the established IA; do not reconstruct a full IA contract.

This is a structural engineering gate, not a default human-approval checkpoint. Proceed directly with `GO_FOR_UI` when stop conditions clear; repair `REVISE_IA` before detailed visual design or production UI code. Use the policy's narrow `NOT_APPLICABLE` exception only for changes that preserve IA; bounded scope and “polish” do not excuse task-flow changes.

When task context, information order, cross-panel coordination, disclosure, or recovery changes, read [IA/UX principles](references/ia-ux-principles.md) and select the applicable [review checks](references/ia-ux-checklist.md). Use [source evidence](references/ia-ux-evidence.md) for rationale or literature review. Keep the current scope visible before scoped actions even when it is resolved automatically; retain necessary judgment, uncertainty and authority. For linked overview/outcome, judgment/process and evidence views, apply the P06 continuous-reading contract and C41–C46 checks in those references: define owner-supplied relations, exact versions/occurrences, forward/reverse navigation, coordinated selection and return/recovery before layout. These are conditional references within the existing gate, not another checklist ledger or approval step.

## Overview

Use Livingware's engineering workflow for the work process and Impeccable for frontend craft. Existing project design context is evidence and constraint, not optional inspiration.

Route material UX/IA, semantic ownership, task-flow, and design-system integration decisions through this skill. Explicit Impeccable craft/critique/polish commands with unchanged IA may start in `impeccable`; if they expose a material IA or semantic change, return here before implementing that change.

**CONDITIONAL VISUAL CRAFT:** Use `impeccable` when visual composition, typography, color, accessibility critique, motion, or visual polish is a substantive outcome or a concrete risk requires its craft checks. Do not load it for pure IA, routine data/control wiring, semantics-preserving UI fixes, or deterministic implementation verification. Reuse the same project design authority and incumbent evidence; avoid duplicating setup, IA discovery, full-site critique, or browser verification between skills.

## Project design authority

Before making design decisions, inspect the target and the project's declared design authority at the applicable project/package scope, then tokens, theme/CSS, shared components, representative screens, and supplied visual references. `DESIGN.md` / `design.md` are discovery examples, not required filenames; follow repository instructions when the maintained guide lives elsewhere.

When a project has an established `DESIGN.md` (or `design.md`), **DESIGN.md wins** over generic Impeccable recommendations. Treat its declared visual language, information architecture, component conventions, and consistency objectives as acceptance criteria.

Do not replace an existing design system merely because Impeccable would choose a different font, radius, palette, density, layout family, or interaction style. A redesign or replacement visual world requires an explicit request to change the design system itself.

Treat current CSS and screenshots as evidence that may contain the reported regression. Resolve them against declared design authority and explicit user corrections before preserving them. Generic advice to tint neutrals, warm a surface, soften contrast, or add brand color never authorizes replacing an established palette. Verify the resolved tokens in every affected theme, including legacy aliases and canvas consumers, rather than fixing only the photographed element.

For rounded-corner transitions, nested rounded surfaces, or corner clipping/stroke alignment, read [corner geometry](references/corner-geometry.md). Apply its geometry within the project's declared radius roles; preserve semantic tokens and derive radii only for boundaries intended to form a uniform inset.

For Asimov projects, read [references/asimov-alignment.md](references/asimov-alignment.md) and inspect the current workbench template, composition showcase, and component showcase. For canvas-header or breadcrumb work, follow its conditional canvas-orientation playbook. This reference and its regional playbooks are bundled here; a separate `asimov-ui-design` skill is not required. Follow the project's declared source responsibilities; resolve material drift rather than copying stale examples. Do not impose Asimov on unrelated projects.

If no design system exists and a visual system must be created, enter Impeccable's new-work process after the relevant task/IA decision. Absence of a `DESIGN.md` filename alone is not proof of missing product design authority.

## Working method

1. State the target user, triggering situation, desired outcome and success criterion; distinguish evidence from assumptions.
2. Allocate remembering, finding, comparing, calculating, configuring and recovery to the system where safe. Preserve the user's necessary judgment and authority; apply Fix → Infer → Recommend → Ask.
3. Establish or revalidate IA under the gate before detailed visual choices; record the review in the existing spec/plan or bounded-task response.
4. Map information roles to exact design-document sections, current template/showcase paths, tokens and shared primitive variants before implementation.
5. If visual craft is in scope, enter Impeccable only for that scoped phase; preserve the existing IA, tokens, and design authority. Otherwise continue without it.
6. Verify both the task path and design conformance. Define a task-effort acceptance check; do not equate browser success with measured human cognitive-load reduction.
7. Integrate genuinely reusable patterns into the existing design-system boundary instead of duplicating them locally.

Do not let missing optional Impeccable context files block an established product UI when the repository already provides sufficient product requirements and design authority. Do not run a design-system replacement flow unless the task calls for one.

## Completion contract

For UI code changes, follow `test-driven-development` for real-browser verification in addition to code tests. Test scope follows the observed production impact radius rather than diff size; use the existing Verification Impact Analysis / R0-R3 policy instead of automatically escalating every UI change to the broadest suite. Before completion, verify the affected rendered behavior against the applicable design-system objectives and the IA evidence established before implementation. Use an Impeccable critique/detector pass when it addresses a concrete risk; do not audit the entire product for a local UI change.

A frontend task is not complete when it merely functions; it must also remain coherent with the project's design language and information structure.
