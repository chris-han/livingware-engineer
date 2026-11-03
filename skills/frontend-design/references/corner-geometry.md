# Corner Geometry

Read this reference when a task involves rounded-corner transitions, nested rounded surfaces, uneven corner spacing, or clipping/stroke alignment. Apply it within the project's declared design authority.

## Ownership and scope

The project design guide owns adopted visual rules and exceptions. Semantic tokens and shared primitives own executable values. This reference supplies a reusable method, not a new radius scale.

Distinguish **component roles** from **related boundaries**. An independent button inside a card keeps its component radius. Derive an inner radius only when its boundary is intended to follow the surrounding boundary at a uniform inset. Do not replace a project's control/content/panel tokens with a global parent-radius-minus-padding recipe, or enlarge every corner to imitate another platform.

## Continuity: what the terms establish

For regular planar curves joined with a consistent orientation:

| Level | Requirement at the join | Practical meaning |
| --- | --- | --- |
| G1 | Same position and tangent direction | No directional kink; curvature may jump. |
| G2 | G1 plus matching signed curvature | Turning tightness changes continuously. |
| G3 | G2 plus matching curvature change with arc length, dκ/ds | The rate of change of turning tightness is continuous. |

Geometric continuity does not require equal parameter speeds. A straight segment has curvature 0; a circular arc has curvature 1/R in magnitude. A tangent line-to-circle join is therefore G1, not G2. A continuous-corner construction can smooth that transition.

Prefer the existing platform or shared primitive's continuous-corner option when the project's visual language calls for it. “Continuous,” “squircle,” and a design tool's smoothing percentage do not by themselves prove exact G3 continuity. Apple's public continuous-corner API is not evidence that every Apple shape satisfies G3. Neither a continuity grade nor a brand comparison establishes measured aesthetic preference or usability improvement; do not make G3 a universal acceptance gate.

## Nested circular corners

When outer and inner boundaries use circular arcs, have the same inset on both adjoining sides, and their actual radii fit their bounds without clamping:

**inner radius r = outer radius R − boundary inset d**, for **0 ≤ d < R**.

This gives both arcs the same center, keeping the normal gap equal to d from the straight edges through the corner. For R = 24 px and d = 8 px, use r = 16 px. If both radii remain 24 px, the gap on the 45° corner bisector becomes √2 × 8 ≈ 11.31 px while straight-edge spacing is 8 px. This is ideal circular geometry, not a perceptual test.

Measure d between the actual boundaries being compared. From an outer border edge to a content edge, it may include both border width and padding. Account for inset strokes and clipping bounds; a shadow is not the boundary. CSS defines border and padding corner shaping from the corresponding outer radii, with zero-clamping, and may reduce oversized radii to fit a box.

At d = R, the inner arc collapses to a square-corner vertex. When d exceeds R, clamping the inner radius to zero is a practical/CSS convention, not proof of an everywhere constant-width band. Different circular radii at different corners can each use rᵢ = Rᵢ − d when that corner satisfies the assumptions. Unequal horizontal and vertical insets, elliptical corners, or browser radius normalization require their actual geometry; one scalar subtraction cannot guarantee a concentric circular result.

## Continuous curves and implementation

For a general continuous, Bézier, or superellipse contour, an exact parallel boundary is a **normal offset of the outer curve**, where that offset remains regular. Its nominal “corner radius” is not a constant curvature radius. Subtracting padding from a radius parameter or reusing a smoothing percentage does not generally produce an exact offset.

Use the existing native/framework concentric-shape facility or shared primitive when it provides the needed relationship. Otherwise use a documented approximation and check the rendered spacing. Do not introduce a dependency or custom path engine for a small refinement unless the requested result needs it.

Keep fill, border/stroke, content clipping, and focus-outline geometry related to the same shape owner, with each required inset or outward offset respected. A focus ring can sit outside the contour and must remain visible. Preserve established interaction states, hit areas, contrast, and accessibility semantics.

## Apply and verify

1. Find the project rule, semantic radius token, and shared shape primitive. Identify whether the inner element is an independent component or an intended uniform inset.
2. Inspect the actual contour, bounds, border, padding, clipping, and any radius normalization. Choose circular subtraction only when its assumptions hold; otherwise reuse an offset/concentric facility or a justified approximation.
3. Correct the shared owner or the local relationship responsible for the defect. Record an adopted project-wide rule in the maintained design guide; avoid duplicate radius tables or one-off overrides.
4. Inspect the affected component at its normal rendered size and the relevant narrow layout, theme, and interaction state. Check straight-to-corner spacing, clipping seams, border alignment, and focus visibility. Use zoom to diagnose geometry, then judge the normal-size result.
5. Follow the existing verification lane for the actual change. A local corner correction does not itself require a product-wide audit, a new approval step, or an agent behavioral evaluation. Report approximations and observed results without claiming unmeasured preference gains.

## Primary sources and their limits

- [Autodesk Alias: Continuity G0–G3](https://help.autodesk.com/cloudhelp/2026/ENU/Alias-Video-Tutorials/files/essential-concepts/continuity-g0-g1-g2-g3.html) — geometric continuity terminology; the table above is scoped to planar curves.
- [Apple: RoundedCornerStyle](https://developer.apple.com/documentation/swiftui/roundedcornerstyle) — public circular and continuous styles, not a universal G3 guarantee.
- [Apple WWDC25: Get to know the new design system](https://developer.apple.com/videos/play/wwdc2025/356/) — concentric corner relationships and padding within Apple's design system; not a replacement for another project's visual rules.
- [W3C: CSS Backgrounds and Borders, corner shaping](https://www.w3.org/TR/css-backgrounds-3/#corner-shaping) — border/padding radius subtraction and zero-clamping; see “Overlapping Curves” for radius normalization.
- [MIT: Differential geometry of offset curves](https://web.mit.edu/hyperbook/Patrikalakis-Maekawa-Cho/node219.html) — offset geometry defined along the curve normal.
