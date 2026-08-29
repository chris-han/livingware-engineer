---
name: frontend-design
description: Use when designing, implementing, refactoring, reviewing, auditing, or polishing frontend UI, product interfaces, dashboards, components, visual systems, or information architecture.
---

# Frontend Design

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
2. Reuse project tokens, primitives, and recurring structures before adding page-local styling.
3. Preserve incumbent visual and information-architecture rules during refinements and feature extensions.
4. Use Impeccable to detect generic AI defaults, weak hierarchy, decorative structure, inconsistent geometry, accessibility defects, and other frontend slop.
5. When a recurring visual or information structure is introduced, integrate it into the project's existing design-system boundary rather than duplicating it locally.

Do not let missing optional Impeccable context files block an established product UI when the repository already provides sufficient product requirements and design authority. Do not run a design-system replacement flow unless the task calls for one.

## Completion contract

For UI code changes, follow `test-driven-development` for real-browser verification in addition to code tests. Before completion, verify the rendered result against every consistency objective declared by the project's design system and run the relevant Impeccable critique/detector pass when available.

A frontend task is not complete when it merely functions; it must also remain coherent with the project's design language and information structure.
