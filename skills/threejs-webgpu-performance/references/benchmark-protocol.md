# Three.js / WebGPU Benchmark Protocol

Use this reference when a renderer performance change needs an explicit frozen experiment contract.

## Template

```markdown
# <Experiment Name>

## Hypothesis
Exact change:
Expected removed cost:
Current evidence that this cost is dominant:

## Scope
Allowed implementation boundary:
Explicitly out of scope:
Visual/semantic invariants:

## Fixtures
- small:
- representative/stress:
- dense:
- large:
- real dataset(s):

## Frozen baseline
Commit/ref:
Browser/GPU:
Viewport/devicePixelRatio:
Warm-up policy:

## Timing metrics
- frame CPU median / p95
- render/submission CPU median / p95
- effects CPU median / p95
- layout/force CPU median / p95
- coefficient of variation or equivalent dispersion

## Mechanical metrics
Choose counters that test the ownership boundary:
- object/draw count
- geometry/material/texture creates
- buffer uploads / dirty marks
- graph-data rebinds
- prepare/rebuild counts
- proxy creates/deletes
- atlas rebuilds/uploads
- matrix/color writes and skips

## Frozen acceptance thresholds
Minimum representative improvement:
Selection anti-regression:
Camera anti-regression:
Running anti-regression:
p95 anti-regression:
Mechanical invariants:

## Paired run sequence
1. Warm up separately.
2. baseline -> candidate
3. baseline -> candidate
4. baseline -> candidate
5. Preserve raw evidence for every run.

## Disposition
- ACCEPT_AND_STOP
- ACCEPT_AND_CONTINUE
- REJECT
- REPROFILE

## Stop rule
Stop when:

## Negative evidence
Rejected behavior/failure mode:
Evidence path:
Reason not to repeat the approach:
```

## Controlled ablation

When render CPU is broad, measure the same mounted scene while selectively removing one class at a time, for example `all -> labels removed -> edges removed -> nodes removed`. Use deltas to rank object-class submission cost. Keep separately timed effects outside the render bucket when the runtime measures them independently.

## Warm-up discipline

Record WebGPU pipeline/shader initialization separately. If a suspected one-time cost repeats after warm-up, treat it as a runtime regression. A longer benchmark transport timeout may be used to observe the cost, but evaluator thresholds must remain unchanged.

## Scale gating

Test candidate economics at multiple scales. If a scale threshold is introduced, derive it from evidence and make the below-threshold path avoid candidate ownership and bookkeeping.

## Resource lifecycle

For resident resources, steady-state creates/deletes should normally be zero after warm-up unless the experiment explicitly requires streaming or eviction. Key resources by stable semantic identity when upstream framework object identity can change.
