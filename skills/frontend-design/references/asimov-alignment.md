# Asimov workbench alignment

Read this reference only when the target project uses Asimov. The project's declared design guide and designated implementations own the design; this reference is a discovery and alignment procedure, not a second design system. The Asimov guidance is bundled with `frontend-design`; do not require a separately installed `asimov-ui-design` skill, a ChatGPT-only skill URI, or a version-specific cache path.

## Inspect current sources

Locate and read the applicable document and actual implementations before choosing geometry or components. Repository instructions identify the maintained design guide; its declared precedence wins. For example, the current Semantier repository uses `docs/operational/design.md` as its single UI design law and `hermes-workspace/src/styles.css` as its sole application stylesheet; `docs/canonical/architecture.md` separately owns runtime semantics. Do not revive retired guide or stylesheet files. In other Asimov workspaces, possible discovery anchors are:

- the declared design guide, sometimes `DESIGN.md` or `design.md`: philosophy, reference implementation, geometry, information architecture, supported layouts, and component rules;
- the declared stylesheet, sometimes `src/styles.css` or `src/asimov.css`: physical implementation of the project's `--asimov-*` tokens;
- `src/screens/knowledge-base/graph/showcase/semantica-showcase2-screen.tsx`: current analytical shell and responsive composition;
- `src/screens/knowledge-base/graph/showcase/semantica-showcase-screen.tsx`: graph/data/control behavior reference;
- `src/routes/AsimovShowcase.tsx`: shared component variants and interaction states;
- `src/components/ui`: canonical wrappers, behavior and accessibility; `src/components/ui/icon.tsx`: canonical icon boundary.

These are discovery anchors, not assumed files in every repository. Follow renamed/project-local owners. Apply the current written laws within their UI scope and inspect physical implementations for conformance; a stale showcase or stylesheet does not override declared authority. Keep permissions, domain states and runtime meaning with their existing semantic owners.

## Preserve the incumbent design

Classify the request before changing composition: refinement preserves the incumbent structure unless a demonstrated defect requires a change; redesign can replace composition within the requested region while preserving product truth, behavior, destinations and accessibility. Asimov applies to authenticated product surfaces unless the user explicitly expands scope to marketing.

Use the smallest supported composition for the job. Preserve stable geometry across hover, focus and selection; express selection with the project's surface, border, indicator or icon treatment. Use existing tokens and shared wrappers for spacing, typography, icons and control states. Keep natural-language chrome in the UI font and data-bearing values in the designated value role. Do not introduce route-local skins, copied private showcase selectors, decorative shadows/glow/gradients, oversized rounding, layout-shifting hover or `!important`.

## Regional guidance

For nested canvas/workbench headers or breadcrumb changes, read [asimov-canvas-header.md](asimov-canvas-header.md). Inspect the project’s current global brand and route/context owners before changing local orientation.

For a persistent or collapsible global left navigation sidebar, read [asimov-left-navigation.md](asimov-left-navigation.md). Keep regional guidance conditional; ordinary workbench changes do not require loading every playbook. Add a regional reference only when a demonstrated pattern is reusable, rather than documenting a one-off workaround as a system rule.

## Map IA to composition

First complete JTBD, cognitive-work allocation, task flow, ownership and recovery under `docs/ia-before-ui.md`. Then record the exact source path/section and shared component or class for each major information role:

| Information role | Mapping to verify |
| --- | --- |
| Global product identity / local location / active context | Global navigation, route-owned orientation header and existing context selectors, respectively |
| Structural navigation / inventory | Canonical left context panel; distinguish it from global product navigation |
| Primary task and result | Flexible center stage with task-local controls |
| Selected-object evidence / assistance | Current Inspector and Chat owner |
| Progress and system state | Canonical status/footer surface, distinct from navigation |

The current Showcase2 analytical template uses `context-main`: a structural left panel and flexible center, with the workspace-global collapsible `INSPECTOR | CHAT` drawer. Do not recreate the retired route-local permanent right Inspector from an older three-column example. Verify this against the target's current sources; specialized or legacy compositions require the applicable documented reason. Choose the smallest supported layout that serves the job.

Keep the center usable when the drawer opens/closes, preserve selection and canvas/view context, and use the template's responsive and scroll ownership. Verify footer/status visibility and reachable controls at compact width and short height. Do not hide a missing space/layout decision by shrinking the whole interface or forcing users to pan through unused canvas.

## Reuse showcase components

Map controls to existing wrappers and demonstrated variants rather than approximating their appearance. Inspect the relevant current contracts for selectors, inputs, secret fields, number steppers, sliders, segmented toggles, panels, property rows, and empty/state surfaces. Reuse canonical tokens for spacing, geometry, typography and interaction state.

Do not copy showcase-private selectors, create a route-local palette, hardcode a second geometry system, add a duplicate Inspector, or expose renderer tuning as a normal business decision. Preserve high semantic density with low perceptual entropy: every visible cue must clarify state, relation or action, or reduce cognitive work.

## Verify the mapping

Use the selected browser evidence lanes to check the actual task path, keyboard/focus return, state/recovery, desktop and narrow/short layouts, and drawer behavior against the chosen reference. Batch desktop and narrow visual inspection, fix the resulting defects together, and use at most one confirmation pass for visual polish; necessary correctness repairs still follow the affected verification contract. Inspect the affected bilingual, long-content, theme and reduced-motion states where relevant. Keep current behavior and rendering requirements; optional QuickE2E exploration does not replace deterministic replay or rendering evidence.

Report separately: design-source conformance, automated task-path evidence, and any human usability measurement. A matching screenshot proves neither task success nor reduced human cognitive workload.
