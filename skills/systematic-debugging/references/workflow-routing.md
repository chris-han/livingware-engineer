# Systematic Debugging Workflow Routing

Use this reference only after `systematic-debugging` is active and the compact root contract is insufficient to choose the next debugging state.

The workflow is recurrent, not a fixed itinerary:

```text
observed failure
  -> establish smallest reliable observation
  -> localize current uncertainty
  -> choose the cheapest distinguishing probe/operator/reference
  -> observe result
  -> update state
  -> route again
  -> root cause established / diagnosis-only exit
```

## States and transitions

### OBSERVE

Entry: failure is reported but the smallest reliable reproduction/evidence is not yet established.

Route to:
- `LOCALIZE` when the failure is concrete enough to reason about;
- `ENVIRONMENT` when evidence points to runtime/fixture/config rather than product behavior;
- exit as `UNRESOLVED` when reproduction is impossible and further probes would be speculative.

### LOCALIZE

Entry: failure is observed but the responsible boundary/data flow is not yet known.

Prefer directly implicated source, test, error, and recent relevant diff. Use repository graph/index discovery only when direct inspection leaves a material caller/dependency/ownership question unresolved.

Route to:
- `HYPOTHESIS` when one bounded causal hypothesis can be stated;
- `TRACE` for a bad value/behavior that must be followed upstream;
- `TIMING` for race/timing evidence;
- `POLLUTION` for order-dependent/shared-state failures where the existing `find-polluter.sh` operator applies.

### HYPOTHESIS

Entry: one falsifiable explanation exists.

Choose the smallest safe probe that can distinguish it from remaining alternatives. Do not implement a fix as the probe unless the probe itself is explicitly diagnostic and reversible.

Route to:
- `ROOT_CAUSE` when evidence establishes the source mechanism and affected behavior;
- `LOCALIZE` when falsified or when new evidence changes the boundary;
- `ENVIRONMENT` when the cause moves outside product/code behavior.

### TRACE

Use `root-cause-tracing.md` for deep call/data-flow tracing. Exit back to `LOCALIZE` or `ROOT_CAUSE`; do not carry the trace playbook forward after its question is resolved.

### TIMING

Use `condition-based-waiting.md` for timing/race failures. Exit back to `HYPOTHESIS`, `LOCALIZE`, or `ROOT_CAUSE` based on evidence.

### POLLUTION

Use the executable `find-polluter.sh` operator when the hypothesis is that one test/input contaminates another. The script/test own its mechanics; this workflow owns only the decision to invoke it and interpretation of the result.

### ROOT_CAUSE

Exit condition: the source mechanism and affected behavior are sufficiently established to support the requested diagnosis or authorized implementation handoff.

Handoff only compact state:

```text
root cause
intended/preserved behavior
affected surface
supporting evidence
material unresolved risk
```

Do not carry this workflow body into TDD or completion verification. Re-enter debugging only if new contradictory evidence makes the failure unexplained again.

## Invariant

No branch may turn “we need a next step” into “apply a plausible fix.” Evidence must establish the root cause before implementation routing.
