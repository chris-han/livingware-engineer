# Simulation protocol

## Before execution

Record the model purpose, horizon, boundary, equations, units, initial values, parameter sources/ranges, integration method, time step, and scenarios. Mark each input as observed, sourced, estimated, or assumed.

Run these checks:

1. dimensional consistency;
2. equilibrium and extreme-condition behavior;
3. time-step sensitivity;
4. conservation or stock-bound constraints where applicable;
5. baseline reproduction of the intended reference mode;
6. at least one adverse or counterfactual scenario;
7. one-at-a-time or global sensitivity on consequential uncertain parameters;
8. alternative structures when causal uncertainty is material.

## Interpreting results

Compare mechanisms and decision thresholds before comparing final values. Report the range across defensible assumptions, which loops dominate each phase, and where policies create delayed side effects. Separate:

- model input;
- simulated implication;
- empirical observation;
- decision judgment.

Do not call an intervention a leverage point merely because changing its parameter creates a large response. Consider controllability, delay, implementation cost, reversibility, distributional effects, and whether the response survives structural alternatives.

## Bundled runner format

`scripts/simulate.py` uses explicit Euler integration and Python's standard library. It is suitable only for small deterministic continuous-time teaching or exploratory models.

```json
{
  "simulation": {"start": 0, "stop": 12, "dt": 0.1},
  "stocks": {"customers": {"initial": 100, "nonnegative": true}},
  "parameters": {"acquisition_rate": 12, "churn_fraction": 0.04},
  "auxiliaries": {"churn": "customers * churn_fraction"},
  "flows": {
    "acquisition": {"equation": "acquisition_rate", "affects": {"customers": 1}},
    "loss": {"equation": "churn", "affects": {"customers": -1}}
  },
  "scenarios": {
    "baseline": {},
    "retention": {"parameters": {"churn_fraction": 0.025}}
  }
}
```

Expressions may use stock, parameter, auxiliary, and `time` names with arithmetic and the functions `abs`, `min`, `max`, `exp`, `log`, and `sqrt`. Auxiliary definitions are evaluated in declared order. Scenario overrides may replace parameters or stock initial values.

Run:

```bash
python scripts/simulate.py model.json --scenario retention --output results.csv
```

The runner rejects unknown names, unsafe syntax, non-finite values, bad stock references, and steps that do not divide the horizon. Validate time-step sensitivity manually. Use a mature system-dynamics package when higher-order integration, calibration, stochastic processes, discrete events, optimization, or large models matter.
