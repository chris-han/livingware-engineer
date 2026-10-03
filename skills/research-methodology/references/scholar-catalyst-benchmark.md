# ScholarCatalyst Benchmark Adapter

Use this reference only when evaluating literature-intake or research-catalyst qualification behavior against the ScholarCatalyst benchmark or a structurally similar dataset.

ScholarCatalyst is an external benchmark for retrieving papers that researchers judged as capable of inspiring or advancing a research project. Treat it as benchmark evidence, not as Livingware research authority.

## What to reuse

Prefer reusing three surfaces from the upstream project:

1. **dataset / labels** — research questions, positive documents, hard negatives, and author rationales where available;
2. **candidate retrieval plumbing** — sparse/dense/scientific retriever baselines for constructing candidate frontiers;
3. **evaluation harness** — ranking metrics and trajectory-level coverage measurements.

Do not adopt the upstream agentic-search loop as the Livingware research workflow. It is a comparison baseline.

## Mapping to Livingware

Use this conceptual mapping:

```text
ScholarCatalyst research question
  -> active research question / uncertainty

retrieved or touched papers
  -> candidate frontier

positive catalyst paper
  -> decision-relevant positive

topically related hard negative
  -> relevance-without-catalyst negative

trajectory recall
  -> candidate-frontier coverage evidence

final ranking quality
  -> downstream qualification / ordering evidence
```

Do not collapse frontier construction and qualification into one score when the experiment is intended to diagnose them separately.

## Preferred benchmark decomposition

Measure two stages independently:

```text
Stage A — candidate formation
P(gold catalyst enters candidate frontier)

Stage B — candidate qualification
P(select / score catalyst correctly | catalyst is in frontier)
```

For retrieval runs, preserve standard ranking metrics such as Recall@K and nDCG@K.

For candidate qualification, add decision-centric metrics as justified by the evaluator output, for example:

- AUROC / AUPRC for binary catalyst discrimination;
- Brier score and NLL for probabilistic scores;
- ECE or another declared calibration measure;
- selective risk / coverage for abstaining evaluators;
- positive-versus-hard-negative score margin;
- latency, token cost, and compute cost per candidate.

Do not report a calibration metric when the model output is not a probability with a declared interpretation.

## Minimal first experiment

Before integrating the full corpus, prefer a bounded hard-negative experiment:

```text
research question
  + author-labelled positive catalyst
  + topically related hard negatives
  -> candidate-conditioned assessment
```

Compare the smallest useful set of baselines, such as:

```text
semantic similarity
vs
standard reranker
vs
generative judge
vs
candidate-conditioned decision scorer
```

The first defensible architectural question is whether the proposed decision scorer separates catalyst positives from topical hard negatives better or more efficiently than similarity-based baselines. If not, stop before broad adoption.

## Runtime integration boundary

ScholarCatalyst should normally remain an external benchmark/adaptor rather than a runtime dependency.

A production research-intake workflow may implement the general contract in `literature-qualification.md`, but it should not require ScholarCatalyst labels, taxonomies, or code at runtime.

Author rationales may be used as evidence for evaluator analysis, failure discovery, or bounded learning observations. Do not copy their rationale taxonomy into a project ontology unless a separate design decision establishes that need.

## Evidence and license notes

Pin the exact upstream dataset/repository revision used by an experiment and preserve split, query, candidate, model, scorer, and evaluator identities.

Check the upstream dataset and code licenses before redistribution, commercial training, or product embedding. Benchmark use does not itself authorize product-data use.

## Suggested comparison with agentic search

If cost/serving economics are part of the research question, compare:

```text
agentic search / deep research
vs
retrieval + qualification
vs
retrieval + batched/shared-prefix qualification
```

Measure quality and candidate-frontier coverage alongside latency, tool calls, tokens, and compute. The benchmark can support claims about the tested workload only; do not generalize to all research tasks without independent evidence.
