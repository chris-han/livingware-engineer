# IA-Before-UI Engineering Gate

For every UI design, redesign, extension, or design review, establish or revalidate information architecture (IA) before choosing visual composition or components. Apply this to bounded changes and design-only work as well as new screens, routes, workbenches, navigation, semantic controls, panels, drawers, state surfaces, and ordinary user task flows.

This is an engineering-process gate, not a product-runtime governance gate and not a blanket human-approval requirement. Record the review in the existing design, plan, or bounded-task response; do not create a second IA ledger. Reuse a current review when the task, flow, ownership, and design sources remain unchanged.

## Design sequence

1. Read the relevant project requirements and current `DESIGN.md` / `design.md` (including the target package's document) to establish constraints.
2. Define the JTBD and allocate cognitive work between the system and the user.
3. Design the task flow, semantic owners, information hierarchy, states, and recovery.
4. Map that IA to the project's documented template, live showcase, shared components, and tokens.
5. Clear the stop conditions, then produce detailed visual design or production UI code.

Reading design constraints first does not mean choosing a template before understanding the job. A visually polished mockup cannot substitute for IA. For design reviews, assess the same sequence before recommending cosmetic changes.

## Required review

Record:

- **JTBD:** target user, triggering situation, desired outcome, current workaround/friction, and observable success; distinguish observed user evidence from inferred or assumed needs;
- primary domain objects and user-facing concepts;
- canonical semantic owner for every major state/action;
- **Cognitive-work allocation:** what the user currently must remember, find, compare, calculate, configure, decide, or recover; what the system will do; what judgment remains with the user and why;
- proposed task flow, region hierarchy, primary/secondary actions, and placement rationale;
- ordinary Fast-to-Aha path to the first useful result;
- loading, empty, partial, stale, forbidden, error, retry/recovery, disabled/submitting and relevant lifecycle states;
- separation of navigation/selection from mutation, admission, activation, execution, or other authority-changing actions;
- **Design-source mapping:** exact document sections, current template/showcase source paths, shared primitive/variant and token owners for each major region/control; record source revision when available and any unresolved drift;
- compact-width, short-height, keyboard, localization, long-identifier and reduced-motion constraints where relevant;
- deterministic/browser evidence that will prove the implemented IA is structurally correct, plus a task-level check for the intended reduction in user effort.

Keep the allocation and source mapping concise and traceable; do not duplicate an existing JTBD or MVL contract.

## Offload cognitive work to the system

Use **Fix → Infer → Recommend → Ask** within existing authority: automatically resolve deterministic, safe problems; infer reversible defaults from available context and expose their basis; recommend a next action with relevant evidence; ask only for missing information or judgment that materially changes the outcome. Do not turn uncertain inference into a fact or silently perform an authority-changing action.

Prefer recognition over recall, computed summaries/comparisons over manual reconciliation, retained context over repeated entry, validated inputs over avoidable errors, and explicit recovery over asking users to reconstruct lost state. Keep selection, filters, progress and the next useful action legible. Use progressive disclosure for infrequent detail without hiding uncertainty, consequences or necessary evidence.

Avoid exporting implementation choices, internal IDs, engine settings, or orchestration steps into the ordinary user journey unless they support a real user decision. Fewer controls are not automatically less cognitive work: preserve task-relevant density and make relationships and state understandable.

Define a proportionate acceptance check before implementation, such as required decisions before first value, repeated inputs, manual cross-panel comparisons, navigation detours, or recovery steps. Record a baseline when available and a target tied to the JTBD; label walkthrough estimates as inferred. Browser success or an AI walkthrough does not establish measured human cognitive-load reduction.

## Align with the existing design system

Treat `DESIGN.md` / `design.md` as the project policy over generic visual taste. Follow its declared source responsibilities for CSS/tokens, composition templates, shared primitive behavior, and showcase variants. If sources disagree, inspect the current authoritative implementation, record the drift, and resolve it from project authority before claiming conformance; do not copy whichever example is easiest.

When no design system exists, record that finding and establish a minimal design direction from the JTBD and IA; do not invent missing source paths or require an unrelated template.

For Asimov projects, read `skills/frontend-design/references/asimov-alignment.md`. Use the current workbench template for region composition and the component showcase for primitives/states. Do not assume every project uses Asimov or copy the largest showcase layout into a smaller task.

## Stop conditions

Disposition is `REVISE_IA` and detailed visual design / production UI coding stops when any of these is unresolved:

- the JTBD, desired outcome, or primary domain object cannot be stated clearly;
- avoidable remembering, comparison, calculation, configuration, or recovery is assigned to the user without a reason the system cannot own it;
- implementation vocabulary is exposed where a domain concept should be used;
- two surfaces compete as semantic owner for the same object/state/action/lifecycle;
- a new shell, rail, drawer, uploader, viewer, selector, or control system duplicates an existing canonical owner without an explicit replacement decision;
- semantic controls are placed for renderer/layout convenience rather than point-of-use meaning;
- navigation/selection is conflated with semantic mutation or authority-changing action;
- required state/recovery behavior has no clear owner;
- responsive behavior would hide or ambiguously relocate a required semantic control;
- approval/configuration ceremony delays the first useful result without changing risk, authority, reversibility, or consequence;
- a required design source is uninspected, a template/component mapping is missing, or material design-source drift remains unresolved;
- no verification method can distinguish structurally correct IA from a merely plausible screenshot.

When all applicable checks pass, disposition is `GO_FOR_UI` and implementation proceeds directly. Repair `REVISE_IA` autonomously when evidence and existing authorization suffice; it is not an automatic request for user approval. If required sources are unavailable, finish the useful JTBD/IA work and name the exact missing source without claiming alignment.

Pure visual-token corrections, implementation-only refactors, renderer-performance work, and accessibility fixes that do not alter information architecture may record `NOT_APPLICABLE` with one sentence identifying the preserved task, hierarchy, and action semantics. This exception waives a new IA design, not inspection of applicable design sources or verification of the affected UI. A task being small, urgent, or described as polish does not exempt a navigation, hierarchy, action, or task-flow change.

## Combined development sequence

IA and verification impact analysis solve different problems and should be composed rather than substituted for one another:

```text
requirement / problem
  -> architecture + semantic-owner impact
  -> JTBD + cognitive-work allocation
  -> IA-before-UI review + project design-source mapping
  -> implementation plan (when scope requires one)
  -> implementation / focused TDD
  -> Verification Impact Analysis from observed production impact radius
  -> smallest sufficient integration/browser/E2E evidence + task-effort check
  -> completion claim
```

IA-before-UI asks whether we are implementing the right user-facing structure. Verification Impact Analysis asks how much evidence the resulting code change needs. Neither implies running a broad suite or requesting human approval by default.
