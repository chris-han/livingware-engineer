# Modeling grammar and structural review

## Minimum structure

Start with a reference mode: one or more variables whose behavior over time motivates the work. Then identify:

- **Stocks:** accumulations measurable at an instant.
- **Inflows/outflows:** rates that increase or decrease stocks.
- **Auxiliaries:** intermediate functions or decision rules.
- **Parameters:** quantities held constant within a run.
- **Exogenous inputs:** time series or shocks outside the chosen boundary.
- **Information links:** influences on decisions or rates; they do not move conserved material.
- **Delays:** information, perception, decision, pipeline, or material delays attached to a link or structure.

The bathtub test helps distinguish levels from rates: if time stopped, a stock would remain measurable; a flow would not continue accumulating.

## Structural validation

Check:

1. Every stock has an initial condition and a net rate equation.
2. Each equation is dimensionally consistent.
3. Material is neither created nor lost unintentionally across connected stocks.
4. Feedback paths close; a chain that never returns is not a loop.
5. Link polarity is stated relative to other variables being held constant.
6. Goals, gaps, and actions form a balancing loop only when action responds to the gap.
7. Nonlinear limits, thresholds, saturation, and capacity are explicit when they drive behavior.
8. Delays are located and, for quantitative work, represented rather than merely mentioned.
9. The boundary does not hide a material cost, externality, competitor response, or actor incentive needed to explain the reference mode.
10. The model can be simplified without losing the behavior or decision it exists to explain.

## Feedback reporting

For each loop, report:

```text
R1 or B1 — descriptive name
Path: A +(or -)> B ... > A
Regime: when the loop is expected to dominate
Delay: location and approximate character
Metric effect: what the loop amplifies, suppresses, or regulates
Evidence: observed | sourced | assumed | disputed
```

The same link may be embedded in multiple loops. Loop dominance can change over time; do not describe all loops as equally active.

## Archetypes as hypotheses

Use archetypes to generate questions, not as proof. Common candidates include:

- Limits to Growth: reinforcing growth activates a delayed constraint.
- Growth and Underinvestment: capacity investment lags because standards or expectations suppress investment.
- Fixes That Fail: a corrective action produces a delayed consequence that worsens the original problem.
- Shifting the Burden: a fast symptomatic response erodes or displaces a slower fundamental response.
- Drifting Goals: pressure closes a gap by changing the target rather than improving actual performance.
- Escalation: actors respond to relative position and mutually amplify action.
- Success to the Successful: an allocation rule compounds early advantage between competitors for a resource.
- Tragedy of the Commons: individually rational use degrades a shared finite resource.
- Balancing Process with Delay: corrective action arrives late and creates overshoot or oscillation.

Say “no clear archetype” when the required structure is absent. Compare rival archetypes when they imply different observations or interventions.

## Diagram conventions

For a CLD, show causal direction, `+`/`-` polarity, delay marks, and `R`/`B` loop labels. For an SFD, show stocks, inflows, outflows, sources/sinks, and the information links that control rates. Do not merge the two if the result becomes visually ambiguous.

Use Mermaid for compact communication, but do not imply that a Mermaid flowchart is itself an executable stock-flow model. Equations and units remain authoritative for simulation.
