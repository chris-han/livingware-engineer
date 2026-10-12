# Left navigation redesign

Use this playbook for a persistent or collapsible authenticated left navigation sidebar. Distinguish global navigation from a screen-local context rail: global navigation changes destination; a context rail changes the object or dataset inside one destination. Do not merge them merely because both appear on the left.

## Inspect before editing

Record every destination, group, label, icon, badge, nested branch, utility action, current-route rule, expanded-branch rule, responsive state, and keyboard contract. Include the identity header, global workspace context, footer/account controls, overflow behavior, tooltips, accessible names, and loading/empty/error/disabled behavior.

Compare the sidebar with the project's current production navigation/workbench and, where maintained, `semantica-showcase` and `AsimovShowcase`. Follow the declared design guide when examples disagree. Preserve destination semantics even when visual structure changes.

## Compose the sidebar

Use a stable vertical anatomy when the available content supports it:

1. Identity zone: product mark and optional collapse action.
2. Context zone: current workspace or bounded operating context when it is truly global.
3. Primary navigation: task-oriented destinations, grouped only when grouping improves scanning.
4. Flexible spacer or scroll boundary: keep primary navigation usable with dense or bilingual labels.
5. Utility zone: settings, help, system status, or account controls according to product ownership.

Keep one dominant active-route signal. Use a stable recessed surface, border/indicator, and readable foreground; do not combine several competing accents. Inactive hover must use a restrained background box without changing indentation, position, dimensions, or type weight. Avoid green-filled navigation rows unless the current project reference explicitly establishes that treatment.

## Expanded and collapsed behavior

- Preserve the same destinations and ordering in both modes.
- Use icon plus label when expanded. In collapsed mode, keep icons centered in stable slots and provide accessible names plus tooltips.
- Use Phosphor `CaretRight` and `CaretDown` for hierarchical disclosure through the shared icon boundary.
- Separate branch expansion from route activation when they are distinct actions.
- Restore labels automatically when space returns if collapse is responsive; preserve user preference when collapse is explicitly user-controlled.
- On narrow screens, prefer an accessible temporary drawer or explicit disclosure over compressing the primary stage.

## Typography and metadata

- Keep destination labels and actions in the UI font.
- Use the mono value role only for counts, versions, status values, IDs, or other data-bearing metadata.
- Keep badges compact and rectangular; do not use pill-shaped decorative tags.
- Ensure English and Chinese labels fit without truncating the only meaningful distinction between destinations.

## Implementation rules

- Reuse local navigation, tooltip, disclosure, button, and icon primitives.
- Put reusable sidebar anatomy in a shared component; keep route definitions and product-specific authorization outside the design system.
- Use existing `--asimov-*` tokens and the root Asimov scope. Do not add a route-local palette or copied `showcase-ref-*` selectors.
- Preserve scroll position and avoid remounting the application shell during ordinary navigation.
- Do not use persistent shadows, gradients, glow, oversized radii, scale-on-hover, or `!important`.

## Verification matrix

Verify every destination and nested-route active state; pointer and keyboard activation; focus visibility in both themes; expanded, collapsed, and narrow layouts; accessible names and focus restoration; long English and Chinese labels; counts, empty groups, and overflow; absence of hover/selection layout shift; and sufficient remaining width for the primary stage and any screen-local rails.
