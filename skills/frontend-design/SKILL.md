---
name: frontend-design
description: Use when designing, implementing, refactoring, reviewing, auditing, or polishing frontend UI, product interfaces, dashboards, components, visual systems, or information architecture.
---

# Frontend Design

## MVL Law 1 — Fast-to-Aha

**REQUIRED:** Apply `docs/mvl-laws.md` MVL Law 1 first. Preserve governance boundaries, but keep normal low-risk product paths default-pass. Flag approval ceremony that delays the first useful result without changing risk.

## IA Before UI

For every UI design, redesign, extension, audit, or review, apply `docs/ia-before-ui.md` before choosing visual composition or components. Establish or revalidate the JTBD, cognitive-work allocation, task flow, semantic owners, states/recovery and responsive hierarchy; then map the IA to the project's current design document, workbench template and showcase components. Carry the same evidence into implementation and review.

This is a structural engineering gate, not a default human-approval checkpoint. Proceed directly with `GO_FOR_UI` when stop conditions clear; repair `REVISE_IA` before detailed visual design or production UI code. Use the policy's narrow `NOT_APPLICABLE` exception only for changes that preserve IA; bounded scope and “polish” do not excuse task-flow changes.

## Overview

Use Livingware's engineering workflow for the work process and Impeccable for frontend craft. Existing project design context is evidence and constraint, not optional inspiration.

Any request that designs, changes, refactors, audits, or reviews frontend UX/IA (layout, navigation, interaction flows, controls, content hierarchy, readability, responsive behavior, or information architecture) MUST route through this skill before substantive design reasoning or UI edits.

**REQUIRED SUB-SKILL:** Use `impeccable` for visual craft, critique, anti-slop detection, accessibility, responsive behavior, interaction states, and polish.

## Project design authority

Before making design decisions, inspect the target and the project's existing design truth: `DESIGN.md` / `design.md` at the applicable project/package scope when present, then tokens, theme/CSS, shared components, representative screens, and supplied visual references.

When a project has an established `DESIGN.md` (or `design.md`), **DESIGN.md wins** over generic Impeccable recommendations. Treat its declared visual language, information architecture, component conventions, and consistency objectives as acceptance criteria.

Do not replace an existing design system merely because Impeccable would choose a different font, radius, palette, density, layout family, or interaction style. A redesign or replacement visual world requires an explicit request to change the design system itself.

For Asimov projects, read [references/asimov-alignment.md](references/asimov-alignment.md) and inspect the current workbench template, composition showcase, and component showcase. Follow the project's declared source responsibilities; resolve material drift rather than copying stale examples. Do not impose Asimov on unrelated projects.

If no design system exists, use Impeccable's normal brief-inference and new-work process to establish a coherent direction from the product requirements and references.

## Working method

1. State the target user, triggering situation, desired outcome and success criterion; distinguish evidence from assumptions.
2. Allocate remembering, finding, comparing, calculating, configuring and recovery to the system where safe. Preserve the user's necessary judgment and authority; apply Fix → Infer → Recommend → Ask.
3. Establish or revalidate IA under the gate before detailed visual choices; record the review in the existing spec/plan or bounded-task response.
4. Map information roles to exact design-document sections, current template/showcase paths, tokens and shared primitive variants before implementation.
5. Use Impeccable for visual craft inside those constraints, preserving incumbent visual and IA rules during refinements.
6. Verify both the task path and design conformance. Define a task-effort acceptance check; do not equate browser success with measured human cognitive-load reduction.
7. Integrate genuinely reusable patterns into the existing design-system boundary instead of duplicating them locally.

Do not let missing optional Impeccable context files block an established product UI when the repository already provides sufficient product requirements and design authority. Do not run a design-system replacement flow unless the task calls for one.

## Completion contract

For UI code changes, follow `test-driven-development` for real-browser verification in addition to code tests. Test scope follows the observed production impact radius rather than diff size; use the existing Verification Impact Analysis / R0-R3 policy instead of automatically escalating every UI change to the broadest suite. Before completion, verify the affected rendered behavior against the applicable design-system objectives and the IA evidence established before implementation. Use an Impeccable critique/detector pass when it addresses a concrete risk; do not audit the entire product for a local UI change.

A frontend task is not complete when it merely functions; it must also remain coherent with the project's design language and information structure.
