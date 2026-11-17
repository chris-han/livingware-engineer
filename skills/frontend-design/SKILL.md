---
name: frontend-design
description: "Single Livingware frontend design skill derived from Impeccable 4.9.2. Use for frontend IA/JTBD and cognitive-work allocation, design systems, UI creation or redesign, user-task flows, evidence-linked workbenches, critique, accessibility, visual craft, responsive layout, polish and explicit Impeccable design commands. Not for backend-only or routine semantics-preserving frontend wiring."
version: 4.9.2
license: Apache 2.0
allowed-tools:
  - Bash(npx impeccable *)
  - Bash(skills/impeccable/scripts/impeccable *)
---

This skill gives you the tools and permission to make design that earns the name out-of-distribution craft. Work as an award-winning design director would: production-grade code, a clear POV, a deep grasp of what the client and its users need, and exceptional craft.

Core principles:
- Finish the job. No hedging, no shortcuts: the deliverable is complete, except assets the user must provide.
- Scale ambition to the surface's mode (see Modes). Persuade and Experience get full commitment: bold, distinct work with a point of view. On Operate and Read, ambition shows as precision and restraint, and patterns the visitor already knows earn their place.
- Verify by looking at the rendered result at the sizes it ships at, and batch the checks: fix what one look shows before looking again, rather than screenshotting after every tweak.

## Livingware IA and semantic ownership — extensions beyond Impeccable 4.9.2

This is **one discoverable skill**, not a two-skill handoff. Impeccable's 4.9.2 visual, product-mode, command and tooling workflows are the base; the following non-duplicative system-engineering duties extend them. The sibling `skills/impeccable/` contains only retained internal toolkit resources and Apache-2.0 provenance, **no second SKILL.md**.

- **Scope/activation:** apply the [IA-Before-UI contract](../../docs/ia-before-ui.md) for a new or materially changed task flow, information hierarchy, contextual navigation, evidence relationships or semantic/action owners. A scoped visual refinement with unchanged IA reuses the existing decision (`NOT_APPLICABLE` with reason); a routine deterministic frontend wiring fix does not require a design workflow. Record `GO_FOR_UI | REVISE_IA | NOT_APPLICABLE` only in the existing plan/spec or bounded task answer, never a separate ledger.
- **Job and cognitive work:** bind the real user JTBD, triggering context, first useful result, and what is observed versus assumed. Allocate routine finding, remembering, comparison/calculation, configuration and recovery to the system where safe (Fix → Infer → Recommend → Ask); preserve accountable human judgment. Fast-to-Aha means reversible/low-risk exploration is default-pass, not weakened real authorization.
- **Authority and meaning:** identify the canonical owner of organization/workspace, task, selected object, source/evidence, result, and consequential actions. Differentiate navigation/selection from mutation, execution, institutional admission and activation. Preserve tenant/security boundaries, source attribution, legal/business uncertainty, versioned provenance, and valid recovery rather than inferring authority from visual state.
- **Evidence continuity:** for linked overview/outcome, judgment/process and underlying evidence, use exact owner-issued object/version/occurrence relationships, forward and reverse navigation, stable focal context, missing-link/UNKNOWN behavior, async stale-response isolation and keyboard/compact return. Consult [IA/UX principles](references/ia-ux-principles.md) and [affected checks](references/ia-ux-checklist.md) selectively (P06/C41–C46 when relevant); never create a parallel checklist database or universal three-panel layout.
- **Design authority precedence:** the project's established design specification, visual system, tokens, application architecture and verified user corrections prevail over generic Impeccable suggestions. An absent `DESIGN.md` or `PRODUCT.md` does not erase an existing valid project owner or require a new visual world/init interview. Use the applicable [Asimov alignment](references/asimov-alignment.md) only for a project that actually uses Asimov.
- **Verification and claims:** reuse existing tests and design evidence; select verification by changed behavior / Verification Impact Analysis (R0–R3). New material user-path changes require an appropriately scoped real-browser check, not a full-product audit by default. A successful UI/browser journey does not prove human cognitive relief or normative/legal accuracy; mark those claims unmeasured without independent evidence. Do not automatically dispatch multiple implementation agents, new product-design interview rounds, duplicate screenshots or unrequested whole-site critique.

### Toolkit location and cost control

The bundled 4.9.2 launcher is at **`<installed-Livingware-skills-dir>/impeccable/scripts/impeccable`** (Windows: `impeccable.cmd`), a sibling of this `frontend-design` directory. It is an *internal executable*, not a second skill. When upstream text says `<skill-base-dir>`, resolve it to that sibling toolkit directory, not this root's directory; when it shows a `<toolkit-base-dir>/scripts/impeccable` fallback, substitute the actual installed toolkit path. Run setup at most once, and only when its design tooling is necessary. Loading a playbook is conditional on current work; do not preload all playbooks, invoke `init` when equivalent product context exists, or poll repeated unchanged diagnostics. Retain upstream command verbs under this single skill; explicit user requests to manage Impeccable hooks or shortcuts are separately scoped and must not silently create another discoverable skill entry.

## Setup

1. Run `<toolkit-base-dir>/scripts/impeccable context` once per session, where `<toolkit-base-dir>` is the sibling `skills/impeccable` toolkit directory resolved from this loaded `frontend-design` skill; keep cwd at the user's project. That base directory resolves every `<toolkit-base-dir>/scripts/impeccable <verb>` command in this skill and its references, and `<toolkit-base-dir>/scripts` is the fallback only when the runtime reports no base directory. On a Windows shell without `sh`, call `<toolkit-base-dir>/scripts/impeccable.cmd` instead. The launcher runs a self-contained binary that ships next to it or is downloaded once on first run; no Node or other runtime is required. Pass a named source file or route as `--target <path>`. It loads PRODUCT.md, DESIGN.md, the matching surface brief, and native-platform guidance when applicable; follow its directives and do not rerun it.
2. Load the request's playbook: its Commands-table reference for an explicit/implied sub-command, or [reference/new-work.md](../impeccable/reference/new-work.md) for a new surface, a replacement visual world, or a build from an approved comp. Some playbooks come in parts; read the part this request needs in the same step, not when the playbook later mentions it: [reference/new-work-world.md](../impeccable/reference/new-work-world.md) when a visual world is created or replaced (a redesign, a new look, or no established world), [reference/new-work-comp.md](../impeccable/reference/new-work-comp.md) for a build from an approved comp or on a comp-led build path, and [reference/critique-rubric.md](../impeccable/reference/critique-rubric.md) for a critique whose Assessment A runs in this context (a native platform, or no sub-agent tool); a delegated Assessment A gets the rubric's path in its prompt instead. Inspect target and incumbent visual truth before editing. When the app cannot run, start with committed visual-regression goldens or screenshot fixtures; verify target and freshness against current tokens, CSS, components, or assets, resolve conflicts, and compare theme/variant captures.
3. After resolving analysis and direction, read [reference/craft-floor.md](../impeccable/reference/craft-floor.md) immediately before any UI edit, including small refinements. It carries the quality floor, the absolute bans, and the reflexes no detector catches. Do not load it for planning-only work.

**Launcher unavailable:** On refusal or failure, send a separate message **before the next tool call**: “Context loading did not run; I’ll read the existing project context directly.” Then read existing PRODUCT.md and DESIGN.md without inventing missing context, follow applicable steps 2–3, including reading [reference/craft-floor.md](../impeccable/reference/craft-floor.md) immediately before any UI edit, and continue through permitted tools. This applies to planning and editing; launcher failure alone does not block either.

## How to design

- **The brief wins.** Honor pinned aesthetics, eras, materials, fonts, and palettes even when they conflict with a saturated-pattern warning. Redirecting a clear brief toward your taste is failure.
- **Refinement preserves; redesign replaces.** Refinement keeps the incumbent identity, behavior, copy, and everything outside scope. Ask before replacing factual copy or adding claims. Redesign keeps product truth, content, function, native affordances, and constraints, but treats the old look as evidence and anti-reference; choose a replacement world in new-work and replace DESIGN.md. Never split the difference into polish on the discarded look.
- **Loaded symbols stay out of the decoration.** A subject's world does not license emblems tied to militarism, supremacy, or hate movements as motifs, badges, or ornament, such as the Rising Sun flag's rays, the Confederate battle flag, or Nazi-era insignia and their stylised variants; reach for that world's neutral forms instead. Content that documents such a symbol as fact stays as it is.
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
| `live` | Iterate | Visual variant mode: pick elements in the browser, iterate on alternatives | [reference/live.md](../impeccable/reference/live.md) |
| `generate [n] [action] [element]` | Iterate | Variants, versions, or alternatives of a named element to choose from in the live browser; no manual picking | [reference/generate.md](../impeccable/reference/generate.md) |

Routing:

- **No argument:** read [routing.md](../impeccable/reference/routing.md) and present its context-aware menu; never auto-run a command.
- **Explicit or clearly implied request to run a command:** load its reference (native variant on native platforms) and follow it. Ask once if two commands fit.
- **Workflow or command-selection question:** read [Workflow questions](../impeccable/reference/routing.md#workflow-questions).
- **Otherwise:** treat the request as general design work. Missing PRODUCT.md routes a new surface or replacement world through init, then new-work; a narrow refinement of existing code proceeds on the incumbent implementation as `impeccable context` directs, offering init afterward rather than blocking on it.
- `teach` aliases `init`. `craft` is a deprecated alias for ordinary new-work and adds nothing. `shape` owns task discovery, then enters new-work only for visual-world and surface-concept decisions.

After init writes PRODUCT.md, resume without rerunning `impeccable context`; init loads the native platform reference itself when the platform it recorded is `ios`, `android`, or `adaptive`.

**Pin / Unpin:** `<toolkit-base-dir>/scripts/impeccable pin <pin|unpin> <command>` creates or removes a standalone `/<command>` shortcut. Report the script's result concisely; relay stderr verbatim on error.

**Hooks:** `/impeccable hooks <on|off|status|ignore-rule|ignore-file|ignore-value|reset>` manages the design detector hook for this project (auto-runs the detector after UI file edits and surfaces findings). Load [reference/hooks.md](../impeccable/reference/hooks.md) when the user invokes it with any argument.

**Doctor:** `/impeccable doctor` reports and repairs drift between this project's Impeccable artifacts (PRODUCT.md, DESIGN.md and its sidecar, config, surface briefs, the hook) and what this version reads. Load [reference/doctor.md](../impeccable/reference/doctor.md) when the user invokes it, or when they ask what is out of date, stale, or needs refreshing. A `CONTEXT_STALE` directive in Setup's output is the cheap subset of the same report; act on it there per its own instructions rather than running doctor unasked.

**Foundations:** `/impeccable foundations` runs `<toolkit-base-dir>/scripts/impeccable foundations` and walks the user through the product-foundations roadmap (secrets, 404 page, icons, CI and more); `/impeccable foundations <id>` fixes that one item. Load [reference/foundations.md](../impeccable/reference/foundations.md) when the user invokes it.

**Never repair drift as a side effect of a design task.** A `CONTEXT_STALE` finding is reported, not acted on, unless the user asks. The one exception is a finding marked `auto`, which the next write to that file performs anyway.