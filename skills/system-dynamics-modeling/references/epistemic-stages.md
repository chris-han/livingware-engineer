# Epistemic stages and precision policy

## Stage decision

Use the lowest stage whose entry conditions are satisfied.

### E0 — Open exploration

Use when the focal problem, stakeholder value, business boundary, or intended decision is still unsettled. Outputs may include a stakeholder/value map, behavior-over-time hypotheses, candidate causal variables, rival loop structures, boundary critique, and discovery experiments.

Do not simulate. Numbers may describe known observations, but do not turn them into an uncalibrated dynamic forecast.

### E1 — Directional structure

Use when a coherent causal boundary and at least one feedback loop can be named, but equations or parameters are not defensible. Validate polarity, loop closure, delays, stocks/flows, and likely loop dominance. Use qualitative labels such as rising, saturating, oscillating, overshooting, or collapsing.

A normalized `0–1` or `0–100` run is allowed only when it exposes a structural consequence that is difficult to reason about statically. Label every chart and conclusion **illustrative dynamics—not a forecast**, and avoid exact outcome claims.

### E2 — Bounded experiment

Use when equations, units, initial conditions, parameter sources or ranges, and the decision horizon are explicit. The model can compare policies and locate thresholds within its boundary. Require sensitivity analysis and report ranges rather than a single favored trajectory.

### E3 — Calibrated use

Use only when simulated behavior has been compared with relevant observed behavior, important parameters are estimated or externally supported, and validation covers the intended operating regime. State holdout or back-test limitations, residual errors, uncertainty, and conditions that invalidate extrapolation.

## Business-model exploration

Early business-model design is usually E0 or E1 because the value proposition, adoption mechanism, willingness to pay, delivery capability, and competitive response co-evolve. Use Design Thinking to keep three uncertainties separate:

- **Desirability:** whose problem changes, how behavior changes, and what evidence shows value.
- **Feasibility:** which capabilities, resources, delays, quality constraints, and learning curves govern delivery.
- **Viability:** how value is captured, costs accumulate, retention/reinvestment behaves, and limits or externalities appear.

These are prompts, not mandatory model sectors. The final model should retain only variables that affect the focal behavior and decision.

Do not translate a speculative canvas into a revenue forecast. First identify testable mechanisms: for example, whether retained users increase referrals, whether service load degrades quality, or whether accumulated operational learning reduces cost or cycle time. Each mechanism should have an observable discriminating signal.

## Precision rules

- Match significant digits to input precision and decision relevance.
- Distinguish empirical distributions, expert ranges, assumptions, and convenience values.
- Do not assign probabilities without a basis. Use scenario envelopes when probabilities are unknown.
- A wide range is not a defect when it truthfully represents uncertainty.
- Structural uncertainty cannot be repaired by narrower parameter ranges. Compare alternative structures.
- Simulation demonstrates consequences of assumptions; it does not validate those assumptions.
