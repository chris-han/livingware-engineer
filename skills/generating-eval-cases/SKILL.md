---
name: generating-eval-cases
description: Use when evaluation coverage is missing or unbalanced and you need to create realistic cases that target explicit coverage gaps rather than generating a large generic synthetic benchmark.
---

# Generating Eval Cases

Generate cases to repair declared coverage gaps.

Read `../../docs/livingware-evaluation-architecture.md` for `EvalCase`, provenance, and the synthetic-evidence boundary.

## Workflow

1. Define the smallest useful coverage dimensions for the target.
2. Inventory existing observed cases before generating anything.
3. Mark uncovered or weakly covered cells.
4. Construct abstract scenario tuples for those cells.
5. Validate the tuples for realism and relevance.
6. Render each tuple into a concrete task/input separately from tuple construction.
7. Execute the real system and capture the resulting trace.
8. Verify that the intended condition was actually exercised before admitting the case.

Example dimensions:

```text
task class
x ambiguity
x risk
x environment state
x tool availability
x prior state
x expected routing
```

## Case-generation rules

- Separate tuple generation from surface wording to reduce mode collapse.
- Prefer real observed cases when they cover the cell adequately.
- Create hard negatives around decision boundaries.
- Preserve `source_parent` so close variants do not leak across held-out splits.
- Avoid synthetic domain artifacts when no qualified reviewer can judge realism.
- Generated input provenance remains synthetic even if its subsequent runtime execution is observed.

## Anti-patterns

- "Generate 100 test prompts" without a coverage model.
- Counting dataset size as evidence of coverage.
- Generating only happy paths.
- Using near-duplicates across train/dev/test.
- Treating simulated or generated scenarios as independent observed production episodes.

## Output

Produce a coverage map plus admitted `EvalCase` records, including provenance, source parent, intended coverage cell, and the evidence that the real execution exercised the intended condition.
