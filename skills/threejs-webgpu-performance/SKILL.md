---
name: threejs-webgpu-performance
description: Use when profiling, optimizing, refactoring, or reviewing Three.js/WebGPU rendering performance, especially dynamic 3D scenes, graphs, labels, instancing, post-processing, interaction latency, or CPU/GPU ownership boundaries.
---

# Three.js / WebGPU Performance Engineering

## Lifecycle

Entry: a Three.js/WebGPU scene has a measured or suspected performance problem, or a renderer architecture change is proposed for performance reasons.

Exit: the dominant cost is identified and a bounded candidate is accepted/rejected by frozen evidence, or diagnosis is complete and no justified optimization remains.

Stop carrying this skill once the bottleneck has moved outside the renderer area under investigation. Re-enter only when new evidence identifies another rendering-performance problem.

## Core Contract

Do not optimize from visual intuition. Measure the dominant cost first.

1. Reproduce the slow user-visible state or transition with a representative fixture.
2. Separate layout/force CPU, effects CPU, render/submission CPU, and total frame CPU.
3. Record median, p95, dispersion, object/mutation counts, and lifecycle counters relevant to the hypothesis.
4. Use controlled ablation when needed: labels, edges, nodes, effects, residual renderer cost.
5. State one bounded optimization hypothesis and freeze acceptance and anti-regression thresholds before implementation.
6. Change one ownership or update boundary at a time.
7. Separate warm-up from steady state.
8. Prefer paired same-session baseline/candidate runs when browser/GPU timing can drift.
9. Preserve rejected candidates and negative evidence.
10. Stop when another subsystem becomes the dominant measured cost.

Never weaken evaluator thresholds after seeing candidate results merely to make the candidate pass.

## Design Laws

### Stable semantics own resources

Key persistent rendering resources by stable semantic identity such as node, edge, or entity id, not transient `Object3D`, `Sprite`, React, or framework callback identity when those objects may be replaced.

### Visibility is not ownership

Prefer resident resources with cheap visibility state:

```text
out of view -> visible=false
back in view -> visible=true
```

Avoid create/delete churn on camera movement unless memory evidence justifies eviction.

### Structural and presentation clocks are different

Topology preparation should not be invalidated by selection, hover, theme, ordinary appearance, or camera changes. Treat graph identity, layout, visibility, appearance, interaction, camera, and GPU-frame animation as different update clocks.

### Batch CPU work as well as GPU draws

Instancing is incomplete if application code still performs heavy per-object maintenance. Prefer high-frequency callbacks that queue changed state, one synchronization point that applies changed transforms, and one dirty mark per logical batch. Skip unchanged matrices, colors, uniforms, textures, and visibility state.

### Batch only where scale justifies it

Batching has fixed coordination cost. Establish an evidence-backed scale threshold rather than forcing one renderer path across every scene size.

### Hidden legacy work must actually stop

`visible=false` removes draw cost, not application CPU. When replacing a render path, also stop geometry reconstruction, transform updates, material updates, and other maintenance for the replaced object.

### WebGPU residency is a hypothesis

Do not move work to storage buffers, compute, TSL, or GPU-derived transforms merely because WebGPU permits it. Verify the current CPU cost is material and benchmark interaction transitions as well as steady state.

### Labels are a subsystem

For label-heavy scenes, measure labels separately. Consider contextual visibility, viewport culling, stable ownership, resident proxies, shared texture/material ownership, and only then atlas or instanced-billboard batching if evidence justifies the complexity.

## Workflow

### Diagnose

Use the smallest representative benchmark. If render CPU dominates, do not optimize force/layout. If labels dominate, do not start with edge shaders. Follow measured cost.

For an unexplained anomaly, use `systematic-debugging` until root cause is established.

### Freeze the experiment

Before code changes, record the exact hypothesis, allowed implementation boundary, fixtures, baseline ref, timing and mechanical metrics, minimum improvement, median/p95 anti-regression limits, and stopping/rollback rules.

Use `references/benchmark-protocol.md` when a formal experiment contract is useful.

### Implement minimally

Prefer the lowest-complexity candidate that tests the hypothesis. Remove duplicate hidden-object maintenance before rewriting shaders; coalesce dirty marks before moving transforms to GPU; make proxies resident before building a text atlas; add scale-gated batching before replacing every edge path.

### Verify mechanics

Use `test-driven-development` for behavior contracts and focused mechanical assertions such as graph prepare count, batch rebuild count, buffer dirty-mark count, texture/material/geometry creates, proxy creates/deletes, graph-data rebinds, atlas rebuilds/uploads, and matrix/color writes/skips.

### Benchmark

Separate warm-up from measured repeats. Prefer paired same-session runs:

```text
baseline -> candidate
baseline -> candidate
baseline -> candidate
```

Compare median, p95, dispersion, and mechanical counters. Treat timed-out or incomplete evidence as incomplete unless the timeout itself is the bounded failure under test.

### Decide mechanically

Use an explicit disposition such as `ACCEPT_AND_STOP`, `ACCEPT_AND_CONTINUE`, `REJECT`, or `REPROFILE`. Do not keep optimizing the same subsystem after the dominant bottleneck moves elsewhere.

## Symptom Routing

- High render CPU, low layout/effects CPU -> controlled labels/edges/nodes ablation -> object ownership, draw submission, batching.
- High p95 with acceptable median -> profile the exact selected/camera/running transition -> transition-specific rebuild, upload, synchronization, or cold pipeline.
- Proxy creates/deletes after warm-up -> compare semantic identity with transient object identity -> resource lifetime boundary.
- High buffer-update activity -> count writes, skips, dirty marks, and uploads -> queue/flush and dirty-mark coalescing.
- Labels dominate -> measure visible labels, draw objects, materials/textures, proxy mutations -> culling, resident proxies, shared atlas/material, then batching.
- Edges dominate -> split straight from exceptional edges, count geometry/matrix work -> hidden-work removal, queued transforms, scale-gated instancing.
- Warm-up high but steady state normal -> prewarm or amortize initialization without distorting steady-state evaluation.
- Cost repeats after warm-up -> treat it as a runtime regression, not compilation.
- Candidate helps large scenes but hurts small ones -> introduce an evidence-backed scale threshold and eliminate candidate bookkeeping below it.

## Completion Contract

A Three.js/WebGPU performance change is not complete because one FPS number improved. Before acceptance, establish representative median improvement, relevant p95/interaction anti-regression, mechanical ownership/update invariants, preserved visual/semantic behavior, separated warm-up evidence, preserved negative evidence, and an explicit reason to stop or continue.
