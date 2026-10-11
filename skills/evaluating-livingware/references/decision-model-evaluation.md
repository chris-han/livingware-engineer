# Bounded decision-model evaluation

Use for an explicitly selected typed decision model or probabilistic evaluator. This reference specializes the existing [evaluation architecture](../../../docs/livingware-evaluation-architecture.md); measurement remains evidence, not authority. Benchmark-specific mechanics belong in project adapters; [JEVal](jeval.md) is an optional example.

## Freeze the comparison before execution

Declare the task, allowed outputs, reference-label source and uncertainty, decision distribution, consequential error costs, hypothesis, budget, and stop condition. Pin data revision/hash, model/checkpoint/head, tokenizer, input transformation, option-to-label mapping, scorer, runtime, precision, seeds, and decoding where applicable. Preserve logits/probabilities and typed predictions separately.

Compare on identical cases against the unmodified model and cheap constant/majority baselines. If claiming fine-tuning benefit, include the original backbone with the same adapter and calibration opportunity. A repaired model beating its collapsed version does not establish superiority to the original model.

Preserve source IDs and exposure history. Group repeated source items, equal normalized states, related documents/episodes, and known near-duplicates before splitting; keep connected groups in one split. Document unresolved leakage. Use training/DEV for shaping, CAL for fitted thresholds or probability transforms, and held-out EVAL/QUAL for measurement. Seal an independent CONFIRM population for a final claim after development. Looking at a hold-out and selecting a repair turns that evidence into development evidence for the successor.

## Separate validity, discrimination, decisions, and confidence

Report the full input denominator, supported types, valid outputs, invalid outputs, runtime failures, exclusions, and explicit unknown/abstention behavior. Invalid answers count as failures on supported answer-required tasks; intentional abstentions need coverage and selective-risk reporting. Unsupported tasks are coverage limitations, never silent successes or ordinary incorrect answers.

For binary decisions report class counts, confusion matrix, both class recalls, balanced accuracy, and predicted-class frequency. For multiclass decisions report per-class behavior and an appropriate macro metric. Report ranking metrics such as AUROC/PR-AUC when applicable, including their undefined cases. A single-class decision collapse can coexist with useful ranking.

For probabilities report Brier score or log loss, reliability bins with counts, and ECE with its binning convention. Calibration alone cannot establish usefulness: an uninformative predictor can be well calibrated. Confidence describes uncertainty under a particular distribution; it is not correctness or authority. Do not require exact empirical agreement in a finite confidence bin.

Declare gates from the actual error costs and safety/coverage needs before inspecting EVAL. There is no universal balanced-accuracy, recall, or ECE threshold. Include uncertainty intervals and paired improvement estimates; account for grouped observations, seeds, and multiple candidate selection. Small class counts limit conclusions.

Check option-order and paraphrase stability, long/context-boundary cases, out-of-scope behavior, and subgroup failures when material. Measure end-to-end p50/p95 latency, throughput under declared load, failure rate, inference cost, and one-time repair cost on comparable hardware/runtime conditions.

## Offline attribution before adaptation

Start with replay of saved outputs and inspect class/score distributions, label direction, normalization, threshold, prompt/input transforms, adapter compatibility, and checkpoint identity. Separate preprocessing/scorer faults from discrimination, calibration, readout, or representation hypotheses.

When compatible saved features and heads exist, compare frozen backbone-by-head combinations on identical inputs. Verify feature dimension, normalization, token-position selection, coordinate compatibility, and reconstruction of original logits first. Head swaps across incompatible representations are inconclusive.

For a verified linear scalar readout, `z = w^T h + b`; paired frozen-feature/head interventions can isolate readout contribution within that computation. They do not by themselves identify a training cause or prove behavior on a new distribution.

A threshold or intercept change can restore class decisions while leaving ranking unchanged. Fit any repair only on CAL, record its objective/parameters and failures, freeze it before EVAL, and replay from saved probabilities/logits. Fitting on held-out labels invalidates the transfer claim. Distinguish threshold repair from probability calibration; an intercept-only logistic fit is still a fitted calibration operation, even without backbone retraining.

Internal observations are optional diagnostics. Record exactly which layer, token position, normalization, and sample were captured. Final-layer features do not expose intermediate layers. Linear probes, logit/tuned lenses, and attention are not causal explanations; a trained probe/lens needs separate fitting and validation data. Use controlled interventions to support stronger attribution. Do not invent unavailable activation evidence.

## Prove value on the real decision distribution

Select a concrete business decision and a labeled sample from its actual population, with expert adjudication or explicit label uncertainty. Preserve natural prevalence for utility measurement; if stratifying rare errors, report sampling weights and separate stress-test results.

Freeze raw, repaired, and existing-production baselines before a group/time-separated real-use hold-out. Fit on a separate real-use CAL population if allowed; distinguish direct public-to-business transfer from business-fitted repair. Predeclare cost-weighted utility, class-specific limits, abstention/coverage policy, latency and cost constraints, and the minimum useful gain.

Run paired offline or authorized shadow comparisons; estimate uncertainty in utility improvement and consequential error changes. Report distribution shifts and disagreement slices. A useful outcome requires a verifiable benefit under those declared constraints, not merely a public score increase. If evidence is inconclusive, retain advisory/bounded status and state the smallest next distinguishing test. Production changes follow the existing project release authority.

## Closeout

Record identities, exposure/split ledger, fitted parameters, denominators, per-class/ranking/calibration metrics, baseline deltas with uncertainty, resource cost, replay verification, attribution limits, and retain/reject/inconclusive disposition. Keep project reports and learned numeric gates in their project owner; do not turn one successful repair into a framework-wide default.
