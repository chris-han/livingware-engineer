# Experiment evaluation protocol and evidence qualification (conditional detail)

Load when a specific empirical experiment, evaluator, benchmark, training intervention, or evidence interpretation needs depth beyond the root. The root's mandatory three-part validation and actual-scientific-authority boundaries remain in force.

## Three-part research validation contract

Every research proposal MUST state **what evidence covers, how its conclusions can be checked, and how each result changes the next decision**. Make these three parts explicit in the existing owning plan or memo; reuse qualified evidence and protocols by reference instead of creating another document or benchmark.

For empirical research and system-improvement proposals, all three parts are required before decisive evaluation. For literature, theoretical, or exploratory work, specify the proportionate evidence basis, review/proof/probe method, and decision loop; explain any inapplicable benchmark or statistical element. Exploration may form hypotheses, but evidence used to form a claim is not independent confirmation of it.

### 1. Benchmark / evidence coverage

- Map each claim or capability to representative tasks, cases, or evidence, the target population, and explicit uncovered scope. Use an existing benchmark, native case corpus, deterministic tests, literature, or proof obligations as the claim requires; do not force a public leaderboard or a new benchmark.
- Include relevant positive, negative, boundary, and failure cases. For usage-derived cases, state sampling, frequency/severity, and selection bias; a collection of reported failures alone does not establish production-wide performance.
- Separate development/diagnostic cases from protected evaluation evidence. Identify frozen dataset/case versions, splits, leakage risks, and any freshness or distribution limits before interpreting aggregate scores.

### 2. Auditable evaluation protocol

- Establish that the reference, evaluator, and metrics actually test the claim and are independent enough for the inference. Reproducible scoring alone does not establish validity; inspect disagreements and reference gaps before attributing a model or system deficit.
- Freeze the comparison basis before inspecting decisive/protected outcomes: baseline and intervention, material variables and controls, population and full denominator, scoring/aggregation, uncertainty treatment, resource budget, and success/failure/inconclusive/stop rules. Declare any adaptive or sequential decision rule in advance.
- Distinguish semantic `UNKNOWN`/abstention, missing or disputed reference, invalid apparatus/run, and actor failure. Preserve their counts and treatment; do not silently drop them or turn them all into zero. Count genuine task failures under the declared valid scoring rule.
- Preserve the identities, raw outputs, reduction procedure, exclusions, deviations, and provenance required by **Evidence discipline** so another reviewer can reconstruct the conclusion and its limits. State material reproduction limits explicitly.

### 3. Result-driven improvement / decision loop

- Before execution, map possible results to retained/eliminated hypotheses and zero or one next decision. At closeout, connect the actual evidence to attribution, the smallest justified change target and its owner, and a comparable re-evaluation or an evidence-supported retain/reject/STOP disposition.
- Attribute before adapting: distinguish data/reference, evaluator, implementation, representation/ontology, model, routing/workflow, and policy causes. Real-use corrections are candidate evidence, not automatic ground truth or authority to change the ontology. Preserve unresolved attribution when evidence cannot distinguish causes.
- If a change is justified, specify the bounded candidate/version, regression coverage, comparison basis, and retain/revert/stop rule. Keep failure-driven diagnostic cases useful for regression while reserving fresh independent or properly protected evidence for broader improvement claims. Do not repeatedly tune against a supposedly held-out set.
- If a benchmark, ontology, label, scorer, or acceptance-contract change alters the measurement basis, version that basis and re-evaluate both baseline and candidate under it where valid. Otherwise report non-comparability; a score increase across different bases is not evidence of improvement.
- Record a proposed or completed change and its re-evaluation status separately. Claim improvement only when comparable evidence supports the stated quality/cost/scope claim; an updated memo, completed experiment, or proposed repair is insufficient. Negative or inconclusive evidence may complete the decision loop without a change or another run.

This contract specifies research completeness, not an autonomous optimization mandate. Preserve the one-next-question-or-stop rule, existing ownership, and the separation of evaluation, implementation, admission, and activation authority.


## Experiment admissibility

A research experiment is eligible only when all are true:

- it addresses a named live uncertainty;
- benchmark/evidence coverage, an auditable evaluation protocol, and the result-driven decision loop are explicit under the three-part contract;
- the expected outcomes are defined before protected results are inspected;
- the changed variable(s) are explicit;
- nuisance/confound controls are adequate for the claim;
- references/evaluators are independent enough for the intended inference;
- evidence and measurement identities can be retained;
- success, failure, uncertainty, and stop conditions are frozen;
- each material outcome maps to zero or one primary next question;
- the experiment has a finite budget;
- it does not duplicate an already-qualified experiment without a specific non-duplication delta.

Prefer the smallest experiment that can produce the first defensible decision-changing insight.

## Evidence discipline

Separate:

```text
external source result
!= model inference
!= project-specific direct evidence
!= adopted research law
```

For claim-bearing evidence, preserve as applicable:

- source/dataset identity and lineage;
- split/population identity;
- model/scorer/evaluator identity;
- governing experiment/measurement contract;
- code/config/runtime identity where material;
- raw results sufficient to reproduce reduction;
- uncertainty method;
- exclusions and invalid-run treatment;
- production time and immutable hashes/commits;
- governing scope and explicit non-claims.

A result does not become current evidence merely because it is reported now.

