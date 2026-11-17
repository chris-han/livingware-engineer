---
name: frontend-design
description: Single Livingware frontend design skill, derived from Impeccable. Use for user-task/IA design, visual craft, UI creation, UX critique, accessibility, layout, typography, frontend reviews and polish. Not for backend-only work or routine frontend wiring with unchanged IA and no design decision.
version: 4.1.2
---

# Frontend Design — Impeccable-derived Livingware edition

Single discoverable Livingware skill for product UX/IA and frontend craft. Derived from the existing vendored Impeccable 4.1.2 design workflow (upstream: https://github.com/pbakaus/impeccable), extended with Livingware cognitive-work allocation, semantic-owner and evidence-continuity requirements. Preserve the existing Impeccable reference scripts and design commands as **internal resources**, not another discoverable skill. Use one current-state path and do not invoke the same discovery, setup, IA gate or visual audit twice.

Core principles:
- **MVL Law 1 — Fast-to-Aha:** Governance is ambient by default and interruptive only by exception. In Operate surfaces, preserve status, provenance, and escalation while keeping low-risk exploration/reversible transitions default-pass.
- Go all out. No hedging, no shortcuts. The deliverable must be complete (except assets the user must provide).
- Dream big and bold. Distinct, beautiful, outstanding and highly inspiring work.
- Verify in bounded passes, not a loop, and the ceiling covers the whole cycle: screenshots, defect scans, micro-edits, and rebuilds alike. Build fully, inspect once with a batched round (desktop and mobile together on the web; the shipped device classes on a native platform), fix everything it shows in one batch, confirm with at most one more round, and stop polishing. Open-ended self-QA burns the user's money doing worse what the finish handoffs do better.

## Architecture and IA: one workflow, two types of responsibility

- **Existing product design authority wins.** Resolve the target project's established `DESIGN.md`, Semantier design spec, tokens, semantic owners and current components before styling. Do not replace an incumbent visual system merely to follow Impeccable defaults. A missing `DESIGN.md` filename is not evidence of no design system.
- **Material task-flow / IA decisions:** apply [IA-Before-UI](../../docs/ia-before-ui.md) before visual design; record `GO_FOR_UI | REVISE_IA | NOT_APPLICABLE` in the existing plan/spec or bounded task answer, not a second ledger. For local IA-preserving polish or frontend wiring, reuse the previously settled task/IA; do not start a new discovery interview. An ordinary deterministic UI bug with no design decision belongs to the engineering workflow, not this design skill.
- **Livingware unique IA obligations:** establish the user JTBD and first useful outcome; allocate remembering, finding, comparison/calculation, safe defaults and recovery to the system (Fix → Infer → Recommend → Ask); identify canonical owners of workspace, task, source, selection, result and each consequential action. Keep navigation separate from mutation/admission/activation, preserve tenant and authority boundaries, and expose provenance, uncertainty and reversible recovery. Apply [IA/UX principles](references/ia-ux-principles.md) and [focused review checks](references/ia-ux-checklist.md) only where task semantics or coordination change.
- **Evidence-linked workbenches:** when overview/outcome, judgment/process and source/evidence coexist, bind exact object/version/occurrence identities and owner-issued relations, forward/reverse navigation, stale-response isolation, missing-reference/UNKNOWN handling and accessible recovery; use the conditional P06/C41–C46 checks rather than another standing panel layout or checklist.
- **Asimov projects only:** conditionally consult [Asimov alignment](references/asimov-alignment.md) and current project component/workbench showcases; do not impose Asimov elsewhere.
- **Evidence and exit:** browser acceptance can establish functionality and design conformance, not human cognitive relief or legal/domain correctness. Use the existing Verification Impact Analysis R0–R3 and the minimal real browser path relevant to the change; do not restart a test or audit after an unchanged handoff. The project design authority is the only source for palette, geometry and semantic state, even where Impeccable recommends otherwise.

## Setup (Impeccable craft tools, on demand)

The internal Impeccable toolkit is retained under the sibling `skills/impeccable/` directory (scripts and references only; **no `SKILL.md`**). It is not a second skill to activate. On a design task that actually needs its craft tools, run `node <livingware-skills-root>/impeccable/scripts/context.mjs --target <path>` once, using the installed Livingware skill root to resolve the absolute script path and the user's project as cwd. Reuse any already loaded product/design context. Do not run for a purely semantic/IA planning decision or routine deterministic frontend fix.

For an explicit or clearly implied design command, load just its [Impeccable reference](../impeccable/reference/routing.md) or named playbook below; for a new visual surface load [new-work](../impeccable/reference/new-work.md). Read [craft-floor](../impeccable/reference/craft-floor.md) only before visual code edits. Avoid duplicate context interviews, whole-site audits or fresh `PRODUCT.md`/`DESIGN.md` files when existing authoritative product/design sources suffice. Command scripts remain the upstream-derived toolkit; this root owns routing and the IA gate.

## How to design

- **The brief wins.** Honor pinned aesthetics, eras, materials, fonts, and palettes even when they conflict with a saturated-pattern warning. Redirecting a clear brief toward your taste is failure.
- **Refinement preserves; redesign replaces.** Refinement keeps the incumbent identity, behavior, copy, and everything outside scope. Ask before replacing factual copy or adding claims. Redesign keeps product truth, content, function, native affordances, and constraints, but treats the old look as evidence and anti-reference; choose a replacement world in new-work and replace DESIGN.md. Never split the difference into polish on the discarded look.
- **Visual authority is evidence, not a filename.** Missing DESIGN.md alone does not make a project greenfield; new-work decides whether to preserve, expand, or replace the incumbent world.

## Modes

The mode names what the visitor's success looks like on this surface.

- **Persuade:** the visitor decides and acts; design is the product. Landing pages, marketing, campaigns, pricing. Earn attention and action. Ship real imagery when the brief needs it; follow the committed world, not category habit.
- **Operate:** the visitor completes a task. App UI, dashboards, editors, admin, settings, tools. Scanability, consistency, native expectations, and the real usage scene outrank expression. Brand lives in precise details.
- **Read:** the visitor understands something. Docs, articles, guides, help, changelogs. Structure for comprehension, then make the reading experience worth staying in.
- **Experience:** the visitor is inside the work itself. Portfolios, galleries, showcases. Let the artifact lead from the first viewport; the interface recedes.

Choose the mode from the requested surface, not the product, and persist it only in that surface brief. A tool's landing page is still Persuade; a fashion house's documentation is still Read; a docs index is Read, not Persuade. See [new-work.md](../impeccable/reference/new-work.md) for new surfaces and [operate.md](../impeccable/reference/operate.md) for deeper Operate/Read guidance.

## Commands

| Command | Category | Description | Reference |
|---|---|---|---|
| `craft [feature]` | Build | Deprecated alias for an ordinary new-work request | [reference/craft.md](../impeccable/reference/craft.md) |
| `shape [feature]` | Build | Plan UX/UI before writing code | [reference/shape.md](../impeccable/reference/shape.md) |
| `init` | Build | Capture durable product context in PRODUCT.md | [reference/init.md](../impeccable/reference/init.md) |
| `document` | Build | Generate DESIGN.md from existing project code | [reference/document.md](../impeccable/reference/document.md) |
| `extract [target]` | Build | Pull reusable tokens and components into design system | [reference/extract.md](../impeccable/reference/extract.md) |
| `critique [target]` | Evaluate | UX design review with heuristic scoring | [reference/critique.md](../impeccable/reference/critique.md) |
| `audit [target]` | Evaluate | Technical quality checks (a11y, perf, responsive) | [reference/audit.md](../impeccable/reference/audit.md) · native: [reference/audit.native.md](../impeccable/reference/audit.native.md) |
| `polish [target]` | Refine | Final quality pass before shipping | [reference/polish.md](../impeccable/reference/polish.md) |
| `bolder [target]` | Refine | Amplify safe or bland designs | [reference/bolder.md](../impeccable/reference/bolder.md) |
| `quieter [target]` | Refine | Tone down aggressive or overstimulating designs | [reference/quieter.md](../impeccable/reference/quieter.md) |
| `distill [target]` | Refine | Strip to essence, remove complexity | [reference/distill.md](../impeccable/reference/distill.md) |
| `harden [target]` | Refine | Production-ready: errors, i18n, edge cases | [reference/harden.md](../impeccable/reference/harden.md) |
| `onboard [target]` | Refine | Design first-run flows, empty states, activation | [reference/onboard.md](../impeccable/reference/onboard.md) |
| `animate [target]` | Enhance | Add purposeful animations and motion | [reference/animate.md](../impeccable/reference/animate.md) |
| `colorize [target]` | Enhance | Add strategic color to monochromatic UIs | [reference/colorize.md](../impeccable/reference/colorize.md) |
| `typeset [target]` | Enhance | Improve typography hierarchy and fonts | [reference/typeset.md](../impeccable/reference/typeset.md) |
| `layout [target]` | Enhance | Fix spacing, rhythm, and visual hierarchy | [reference/layout.md](../impeccable/reference/layout.md) |
| `delight [target]` | Enhance | Add personality and memorable touches | [reference/delight.md](../impeccable/reference/delight.md) |
| `overdrive [target]` | Enhance | Push past conventional limits | [reference/overdrive.md](../impeccable/reference/overdrive.md) |
| `clarify [target]` | Fix | Improve UX copy, labels, and error messages | [reference/clarify.md](../impeccable/reference/clarify.md) |
| `adapt [target]` | Fix | Adapt for different devices and screen sizes | [reference/adapt.md](../impeccable/reference/adapt.md) · native: [reference/adapt.native.md](../impeccable/reference/adapt.native.md) |
| `optimize [target]` | Fix | Diagnose and fix UI performance | [reference/optimize.md](../impeccable/reference/optimize.md) |
| `live` | Iterate | Visual variant mode: pick elements in the browser, generate alternatives | [reference/live.md](../impeccable/reference/live.md) |

Routing:

- **Ordinary frontend request:** follow the user's concrete IA/design outcome directly. Do not present the legacy Impeccable command menu, require init, or trigger a fresh design interview when the target and design authority are already settled.
- **Explicit or clearly implied visual-craft command:** load only the corresponding playbook above; for an open-ended request to browse available design commands, read [routing.md](../impeccable/reference/routing.md) and present the options without automatically executing them. The playbook command names are modes of **this frontend-design skill**, not independently discoverable skills.
- **New visual surface or replacement world:** use the existing [new-work](../impeccable/reference/new-work.md) procedure after any material IA gate; for a narrow refinement retain incumbent product/design truth.
- `teach` aliases `init`; `craft` is a deprecated alias. `shape` is useful for unresolved task/design direction, not a mandatory round for already specified work.

After init writes PRODUCT.md, resume without rerunning `context.mjs`. **Do not create standalone pinned Impeccable skill shortcuts**; the single discovery entry remains `frontend-design`. The internal [hooks](../impeccable/reference/hooks.md) and [doctor](../impeccable/reference/doctor.md) procedures are conditional tools only when explicitly requested; do not run them as automatic setup, drift repair, or completion checks.
