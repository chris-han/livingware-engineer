---
name: frontend-design
description: Use when designing, implementing, refactoring, reviewing, auditing, or polishing frontend UI, product interfaces, dashboards, components, visual systems, or information architecture.
---

# Frontend Design

## MVL Law 1 — Fast-to-Aha

**REQUIRED:** Apply `docs/mvl-laws.md` MVL Law 1 first. Preserve governance boundaries, but keep normal low-risk product paths default-pass. Flag approval ceremony that delays the first useful result without changing risk.

## IA Before UI

For a new or materially changed user-facing structure, run `docs/ia-before-ui.md` before the first production UI implementation hunk. The review must establish the user task/domain model, canonical semantic owners, region hierarchy, ordinary Fast-to-Aha path, state/recovery ownership, action semantics, responsive composition, shared-pattern reuse, and verification evidence.

This is a structural engineering gate, not a default human-approval checkpoint. If all stop conditions clear, proceed directly with `GO_FOR_UI`. If the review finds duplicated semantic ownership, implementation-model leakage, unresolved action meaning, missing state ownership, or responsive ambiguity, disposition is `REVISE_IA` and the IA must be repaired before styling or component implementation continues.

Pure visual-token corrections, renderer-performance work, implementation-only refactors, and accessibility fixes that do not alter IA may mark the gate `NOT_APPLICABLE` with a brief rationale.

## Overview

Use Livingware's engineering workflow for the work process and Impeccable for frontend craft. Existing project design context is evidence and constraint, not optional inspiration.

**REQUIRED SUB-SKILL:** Use `impeccable` for visual craft, critique, anti-slop detection, accessibility, responsive behavior, interaction states, and polish.

## Project design authority

Before making design decisions, inspect the target and the project's existing design truth: `DESIGN.md` when present, then tokens, theme/CSS, shared components, representative screens, and supplied visual references.

When a project has an established `DESIGN.md`, **DESIGN.md wins** over generic Impeccable recommendations. Treat its declared visual language, information architecture, component conventions, and consistency objectives as acceptance criteria.

Do not replace an existing design system merely because Impeccable would choose a different font, radius, palette, density, layout family, or interaction style. A redesign or replacement visual world requires an explicit request to change the design system itself.

If no design system exists, use Impeccable's normal brief-inference and new-work process to establish a coherent direction from the product requirements and references.

## Working method

1. Identify the screen's actual user task and information roles before choosing components.
2. For material IA changes, clear the IA-before-UI gate before production UI coding.
3. Reuse project tokens, primitives, and recurring structures before adding page-local styling.
4. Preserve incumbent visual and information-architecture rules during refinements and feature extensions.
5. Use Impeccable to detect generic AI defaults, weak hierarchy, decorative structure, inconsistent geometry, accessibility defects, and other frontend slop.
6. When a recurring visual or information structure is introduced, integrate it into the project's existing design-system boundary rather than duplicating it locally.

Do not let missing optional Impeccable context files block an established product UI when the repository already provides sufficient product requirements and design authority. Do not run a design-system replacement flow unless the task calls for one.

## Completion contract

For UI code changes, follow `test-driven-development` for real-browser verification in addition to code tests. Test scope follows the observed production impact radius rather than diff size; use the existing Verification Impact Analysis / R0-R3 policy instead of automatically escalating every UI change to the broadest suite. Before completion, verify the affected rendered behavior against the applicable design-system objectives and the IA evidence established before implementation. Use an Impeccable critique/detector pass when it addresses a concrete risk; do not audit the entire product for a local UI change.

A frontend task is not complete when it merely functions; it must also remain coherent with the project's design language and information structure.
