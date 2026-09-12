---
name: system-dynamics-modeling
description: Explore, construct, critique, and simulate causal-loop and stock-flow models for feedback-driven systems. Use for system dynamics, feedback loops, business-model dynamics, system archetypes, leverage points, scenario testing, sensitivity analysis, or questions about behavior over time. Match numerical precision to evidence maturity; do not treat exploratory models as forecasts.
---

# System Dynamics Modeling

Turn a dynamic problem into the least-precise model that can answer the user's actual question. Combine Design Thinking's divergence and convergence with system dynamics' behavior-over-time, feedback, stock-flow, delay, and policy-testing disciplines.

## Choose the epistemic stage first

Classify the model from the available evidence, state the classification briefly, and do not force maturity:

- **E0 — Open exploration:** the problem, actors, value, or boundary is still changing. Use behavior-over-time sketches, candidate variables, competing causal hypotheses, and learning questions. No numerical simulation.
- **E1 — Directional structure:** important stocks, flows, polarities, loops, delays, and limits are plausible but uncalibrated. Build CLDs and, when useful, a provisional SFD. Use qualitative trajectories or explicitly normalized illustrative indices, never point forecasts.
- **E2 — Bounded experiment:** equations, units, initial conditions, and defensible ranges exist for the decision horizon. Run scenarios and sensitivity analysis; report ranges and structural assumptions.
- **E3 — Calibrated use:** model structure and parameters have been checked against observations for the intended domain. Forecast only within the validated boundary and carry uncertainty, calibration error, and invalidation conditions.

Read [epistemic-stages.md](references/epistemic-stages.md) when deciding whether simulation is admissible or when interpreting an early-stage business model.

## Integrate Design Thinking

Treat modeling as a double divergence/convergence process, not a march toward equations:

1. **Discover / diverge:** establish the decision or learning purpose, stakeholders, reference behavior over time, system boundary, time horizon, and rival explanations. For business-model work, explore value creation, delivery, capture, retention, capability accumulation, constraints, and externalities without assuming all belong in the final model.
2. **Define / converge:** choose the focal outcome, boundary, time horizon, minimum model, and explicit exclusions. Identify the observation that would distinguish the leading causal hypotheses.
3. **Develop / diverge:** create two or more materially different structural or policy hypotheses when uncertainty is structural. Look for reinforcing and balancing loops, delays, nonlinearities, limits, unintended consequences, and actors optimizing different objectives.
4. **Deliver / converge:** select the smallest model capable of answering the question. At E0–E1, deliver a map and learning agenda. At E2–E3, formalize, simulate, stress-test, and specify what evidence would update or reject the model.

Do not make every request interactive. Ask only for missing facts that materially change the boundary, structure, or admissible precision. When the user requests a direct draft, author a clearly labeled provisional model and expose assumptions for correction. When they want coaching, elicit their variables and reflect their language.

## Build and critique the model

For the detailed grammar, validation checks, loop naming, archetype matching, and diagram conventions, read [modeling-grammar.md](references/modeling-grammar.md).

Maintain these invariants:

- A stock accumulates and has units; a flow changes a stock and has units per time.
- Every stock equation balances inflows and outflows. Units must be dimensionally consistent.
- A causal link states direction under a named ceteris-paribus assumption; polarity is not moral valence.
- A loop sign follows the product of link polarities. Label reinforcing loops `R` and balancing loops `B`, and state which behavior or metric each loop amplifies or regulates.
- Place delays on particular causal or material links. A generic claim that “the system has delay” is insufficient.
- Keep exogenous inputs, decisions, goals, constraints, and observed outcomes distinct.
- Do not force an archetype. “No clear archetype” is a valid result.
- Keep the north-star outcome separate from diagnostic and local optimization metrics. A loop may improve a local metric while degrading the system outcome.

## Quantify only when admissible

Numerical simulation requires all of the following, or an explicit statement that the run is illustrative rather than predictive:

- a decision question and time horizon;
- stocks with initial values and units;
- flows or derivatives with equations and units per time;
- parameter provenance or defensible ranges;
- explicit delay treatment and time step small enough for the fastest relevant dynamic;
- boundary assumptions and omitted mechanisms;
- at least one comparison scenario and one sensitivity or stress test;
- outputs tied to decision thresholds, not merely attractive curves.

If these are missing, remain at E0 or E1. Never fill missing parameters with apparently precise guesses. If an illustrative run would help, use normalized values, broad ranges, or symbolic analysis; label the result **illustrative dynamics—not a forecast**.

At E2–E3, read [simulation-protocol.md](references/simulation-protocol.md). The bundled standard-library runner can execute small deterministic continuous-time models:

```bash
python scripts/simulate.py model.json --scenario baseline
```

Use it only when its Euler integration and expression grammar fit the model. Do not bend discrete-event, stochastic, agent-based, optimization, or game-theoretic problems into this runner; recommend the appropriate method instead.

## Deliver the result

Scale the output to the stage. Include only useful sections:

1. **Purpose and maturity:** decision/learning question, horizon, boundary, E0–E3 stage, and why.
2. **Reference behavior:** the observed or hypothesized pattern over time.
3. **Model:** variables with units and roles; CLD; SFD/equations only when justified.
4. **Feedback account:** each `R`/`B` loop, delay, affected metric, and expected dominance conditions.
5. **Competing hypotheses:** structural alternatives that could explain the same behavior.
6. **Scenarios and results:** ranges, sensitivity, thresholds, and failure modes; no spurious decimal precision.
7. **Leverage and learning:** intervention candidates, side effects, leading indicators, and the cheapest observation or experiment that would reduce the most consequential uncertainty.

Prefer compact Mermaid diagrams. Use separate CLD and SFD diagrams when combining them would obscure material flow or feedback. Preserve the user's variable names where possible, and distinguish user-provided facts, sourced evidence, assumptions, and model-generated implications.
