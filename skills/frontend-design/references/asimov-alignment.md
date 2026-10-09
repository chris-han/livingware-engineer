# Asimov workbench alignment

Read this reference only when the target project uses Asimov. The project's current `DESIGN.md` / `design.md` and its designated implementations own the design; this reference is a discovery and alignment procedure, not a second design system.

## Inspect current sources

Locate and read the applicable document and actual implementations before choosing geometry or components. In the established Asimov workspace, discovery anchors are:

- `DESIGN.md`: design philosophy, reference implementation, workbench geometry, information architecture, supported layout variants, and component rules;
- `src/asimov.css`: the single physical Asimov stylesheet and `--asimov-*` token owner;
- `src/screens/knowledge-base/graph/showcase/semantica-showcase2-screen.tsx`: current analytical shell and responsive composition;
- `src/screens/knowledge-base/graph/showcase/semantica-showcase-screen.tsx`: graph/data/control behavior reference;
- `src/routes/AsimovShowcase.tsx`: shared component variants and interaction states;
- `src/components/ui`: canonical wrappers, behavior and accessibility; `src/components/ui/icon.tsx`: canonical icon boundary.

These are discovery anchors, not assumed files in every repository. Follow renamed/project-local owners. If an installed `asimov-ui-design` skill is available, use it for regional detail while preserving current project authority. Report stale bundled guidance rather than allowing it to override the target's current design policy.

## Map IA to composition

First complete JTBD, cognitive-work allocation, task flow, ownership and recovery under `docs/ia-before-ui.md`. Then record the exact source path/section and shared component or class for each major information role:

| Information role | Mapping to verify |
| --- | --- |
| Identity and active context | Orientation header and existing context selectors |
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

Use the selected browser evidence lanes to check the actual task path, keyboard/focus return, state/recovery, desktop and narrow/short layouts, and drawer behavior against the chosen reference. Inspect the affected bilingual, long-content, theme and reduced-motion states where relevant. Keep current behavior and rendering requirements; optional QuickE2E exploration does not replace deterministic replay or rendering evidence.

Report separately: design-source conformance, automated task-path evidence, and any human usability measurement. A matching screenshot proves neither task success nor reduced human cognitive workload.
