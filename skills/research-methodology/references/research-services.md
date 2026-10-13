# Unified research services and normalized improvement

Use this reference when an eligible research action needs training, inference, rollouts, evaluation, or sandbox execution, or when comparing normalized improvement across domains. Reuse the current experiment owner and evidence records.

This is a provider-independent methodology/interface contract. Host adapters supply executable services and enforce authorization; this reference does not install a runtime, certify an adapter, or authorize an experiment.

## Contents

- [Ownership and capabilities](#ownership-and-capabilities)
- [Execution contract](#execution-contract)
- [Code-mediated processing and evidence visibility](#code-mediated-processing-and-evidence-visibility)
- [Permissions, suspension, and recovery](#permissions-suspension-and-recovery)
- [Budget accounting](#budget-accounting)
- [Normalized improvement](#normalized-improvement)
- [Evidence and adoption limits](#evidence-and-adoption-limits)

## Ownership and capabilities

Keep three owners distinct:

| Owner | Responsibility |
| --- | --- |
| Research skill | Select one justified discriminating action, declare scope/budget/stop, interpret evidence, and update the uncertainty frontier |
| Host execution boundary | Validate each request against binding authority, enforce resource limits, execute/cancel/query work, and retain receipts |
| Backend adapter | Map the common contract to the existing CLI, process, MCP tool, or remote API and its native schemas |

Reuse native tools and existing host stores. Provision only the required capabilities; a unified interface does not require five microservices, a new database, a mandatory meta-router, or an autonomous learning daemon. Keep provider credentials at their owning host boundary; do not copy connector tokens into generated scripts, traces, or sandbox artifacts.

| Capability | Input / output | Boundary |
| --- | --- | --- |
| Training | Admitted training-data refs and allowed configuration -> checkpoint ref and training metrics | Preserve the existing training-data admission and mutation-scope contracts |
| Inference | Pinned model/config and task/context refs -> actor output and usage | Preserve model, provider, and decoding identities for comparison |
| Rollout | Declared task/environment/teacher/judge configuration -> trajectories and feedback | Label generated/synthetic evidence; a teacher or judge output is not automatic reference truth |
| Evaluation | Candidate + fixed evaluation basis -> per-case outcomes, aggregate metrics, logs | The candidate cannot alter its own protected cases, scorer, thresholds, or acceptance basis |
| Sandbox | Scoped script/input refs and resource limits -> artifacts, logs, exit state | Host execution, filesystem/network, and effect permissions remain binding |

These are capability categories, not required endpoint names. Distinguish request schema, tool-output schema, and data schema inferred from a sample; an inferred schema does not prove the full result conforms.

## Execution contract

Bind the smallest applicable fields in the existing owning experiment:

```yaml
experiment_id: <existing owner id>
uncertainty_id: <live question>
stage: DEV | QUAL | CONFIRM
experiment_contract_ref: <version/hash>
baseline_ref: <immutable identity>
evaluation_basis_ref: <cases/split/scorer/metric/protocol pins>
capability: training | inference | rollout | evaluation | sandbox
operation_ref: <host action and version>
input_refs: [<artifact refs/hashes>]
configuration_ref: <allowed settings and exact identity>
authority_ref: <binding host permission basis>
budget_ref: <shared envelope, remaining balance and reservation>
request_id: <stable logical request identity>
limits: <timeout, concurrency, compute, network and output limits>
```

Keep native payload schemas behind the adapter; inspect only the schema needed for the next call. Return a bounded receipt with request/job identity, adapter/runtime pins, state, timestamps, usage/cost, raw-result/artifact refs, errors, and provenance.

Support synchronous execution or submit/status/result/cancel handles as the host permits. Distinguish successful execution, actor failure, invalid evaluation, infrastructure failure, denied/unavailable capability, cancellation, and work not run. A missing capability limits that operation; continue independent eligible work when useful. Never report a declared service as available without an actual adapter and permission.

## Code-mediated processing and evidence visibility

Choose a direct call for a small result or simple operation. Use a host-supported code mode when chaining calls or deterministic filtering, joining, counting, or aggregation materially reduces model turns or context cost. Inspect relevant input/output schemas before generating code instead of guessing fields.

Keep exact calculations in code and expose only the decision-relevant projection to the model. Retain original evidence and the transformation/script identity so a reviewer can reconstruct what was included and excluded. A deterministic calculation is exact only relative to its valid inputs and declared coverage.

Batch only independent work within the existing authorized concurrency and budget. Dependent calls remain ordered. A script's permission to execute is not permission for every tool it might call.

For large results, use the host artifact boundary and return, as applicable:

```yaml
raw_result_ref: <immutable artifact identity, or unavailable>
raw_result_hash: <digest with declared algorithm and byte/serialization scope, or unknown>
storage_status: STORED | FAILED | UNAVAILABLE
retention: COMPLETE | PARTIAL | UNKNOWN
original_bytes: <size in the declared encoding/serialization, or unknown>
stored_bytes: <retained size in the same representation, or unknown>
schema_ref: <native or explicitly inferred schema identity>
projection_ref: <script/filter/summary identity>
visibility: FULL | PROJECTED | TRUNCATED | UNAVAILABLE
coverage: <seen ranges/records, omitted scope and denominator>
decision_coverage: COMPLETE_FOR_DECLARED_CLAIM | PARTIAL | UNKNOWN
```

Treat storage status, retained completeness, model visibility, and decision coverage as independent facts. `STORED` means a write succeeded, not that all original bytes survived. Mark a capped artifact `PARTIAL` even if its write succeeded; use `UNKNOWN` when completeness cannot be established. A digest of the retained subset does not authenticate the missing original. Define the source boundary of any `COMPLETE` claim; complete capture of an already-limited tool response does not establish complete upstream retrieval. Report unknown original size explicitly rather than inferring it from stored size.

Keep artifacts within the owning host's authorized session/experiment storage boundary. Bind each retained content part to its call/attempt and stable part identity; different parts or attempts must not overwrite one another. Published references must resolve to the same content after flush/reload and retry. An unavailable artifact store does not authorize a fallback outside that boundary.

Apply per-result and aggregate context budgets according to the host; do not copy another project's token thresholds as universal defaults. Declare the counting unit and its encoding/tokenizer or estimation basis. Count actual context-bearing content across every result and content part, including previews and reference metadata, rather than list length or object count. Account for non-text parts under the host's modality policy; a text-only count is not a total multimodal budget. Enforce storage byte caps on encoded bytes, not character counts, while preserving valid encoding. If required receipt metadata or other irreducible content exceeds the budget, report the overrun/unsatisfied limit explicitly. Head/tail previews and summaries are navigation aids, not proof that all evidence was inspected. Claim complete coverage only when the retained evidence and procedure establish it for the declared claim. Preserve omitted limitations, unresolved candidates, and source/version links.

If storage fails or retention is partial/unknown, report that state and its coverage consequence; do not state that the full result was saved or checked. Retain claim-bearing evidence before a temporary sandbox is retired. Replay uses pinned artifacts and transformations, not live tools, models, or regenerated summaries.

## Permissions, suspension, and recovery

Enforce permissions at each nested tool/service call, including code-mediated calls. Classify effects through the host's explicit capability/action contract; MCP read/write/destructive annotations may inform that classification but missing labels never grant authority. Reuse existing delegation; do not add blanket approval ceremonies.

Use a typed waiting/denied result for an action that needs unresolved authorization. Claim pause-and-resume only when the actual host/adapter path has verified it. If interactive continuation is unsupported, stop that action with the unmet dependency; do not silently skip it, fabricate approval, or restart the whole script.

Before retries or recovery, inspect retained request and effect receipts. Reuse a completed result where valid. Use host-supported idempotency for side effects; otherwise reconcile whether the effect occurred before retrying. Preserve partial results and cancelled/failed attempts. An ambiguous effect outcome requires reconciliation, not a blind retry.

Keep experimental permission distinct from admission and activation. Service completion and improved scores return evidence or a bounded candidate; they do not expand capability, authorize a successor, or activate production changes.

## Budget accounting

Bind one shared envelope for the experiment, including research-agent inference, actor inference, data/rollout generation, training, evaluations and final verification, sandbox use, branches, retries, and failed/cancelled work. Record exclusions or unmeasurable costs explicitly; never report a partial service allocation as total workflow cost.

The executing host must reserve a bounded amount atomically before dispatch, settle actual usage afterward, and release unused reservation. If cost can exceed the reservation, use incremental authorization or an enforceable provider/runtime cap. Concurrent jobs must share the same reservation basis; checking a positive balance and billing later is not a hard cap.

Keep actual spend, outstanding reservation, and released/unexecuted reservation distinct. Cancellation requests do not prove provider billing stopped. Reconcile uncertain charges before reusing balance. If enforcement or cost measurement is unavailable, state the limit and do not claim a hard budget guarantee.

Report token volume, decision-call unit price, model/tool turns, and end-to-end cost separately. A reduction in one does not establish a reduction in the others. Budget exhaustion closes or suspends the current execution according to the frozen stop rule; it does not authorize extra spend or another experiment.

## Normalized improvement

Use RSI-Index optionally for comparable, higher-is-better bounded scores. The paper averages five benchmark gains; Livingware does not mandate those domains or benchmark tasks.

For a frozen domain set B, baseline score s_b^0, candidate score s_b, and declared upper bound u_b:

```text
g_b = (s_b - s_b^0) / (u_b - s_b^0)
G = sum(w_b * g_b), where w_b >= 0 and sum(w_b) = 1
```

The original five-domain RSI-Index uses u_b = 1 and w_b = 1/5. For example, 0.50 -> 0.75 and 0.90 -> 0.95 both close half of the remaining gap. Preserve negative gains; do not clip regressions to zero.

Freeze domains, baseline, metric direction/scale/bounds, weights, denominator, exposure/split treatment, inference/optimization seed policy, and uncertainty procedure before candidate selection or decisive evaluation. Bind both scores to comparable cases, scoring, operational budgets, and protocol. A changed measurement basis requires a comparable re-evaluation or NON_COMPARABLE.

If s_b^0 >= u_b, scores are outside bounds/non-finite, or the baseline/candidate cannot be bound comparably, report UNDEFINED or INVALID as appropriate rather than dividing by zero or inventing a bound. Transform lower-is-better metrics only through a predeclared justified mapping; do not normalize heterogeneous raw costs or latencies directly with this formula.

Keep semantic UNKNOWN/abstention, disputed references, invalid runs, and NOT_RUN distinct from genuine task failure. Apply the frozen valid scoring rule to actor failures. If a required domain has no valid comparable pair, report the full index as UNAVAILABLE; do not silently drop it and renormalize weights. A partial diagnostic aggregate must name its included/excluded domains and cannot be reported as the complete RSI-Index.

Report per-domain raw scores, denominators/coverage, normalized gains, uncertainty, selection exposure, regressions and hard gates alongside G. Near-ceiling baselines can amplify noise; use repeated comparable measurements as the intended inference requires. Report independent final evidence separately from repeatedly consulted validation scores.

Report total cost and decision-relevant information gain separately. Do not treat score gain as causal attribution, improved research efficiency, recursive compounding, qualification, admission, or activation. Demonstrating recursive benefit requires a separate comparison of later improvement cycles that inherit the accepted change against an appropriate reset/frozen control.

## Evidence and adoption limits

- Fanqing Meng et al. (2026), *RSIGym: A Flexible Environment for Recursive Self-Improvement*, arXiv:2610.10310v1, https://doi.org/10.48550/arXiv.2610.10310; code: https://github.com/evolvent-ai/RSIGym. Supports reusable research capabilities, permission/budget-defined improvement spaces, and remaining-gap normalization. Its reported research configurations run once and final tasks were available during development; research-agent inference and final official evaluation are outside the platform-service allocation. The paper does not establish held-out adaptive generalization or improved subsequent research cycles.
- TrueFoundry (2026), *TrueForge Code Mode* and *Create an agent*: https://trueforge.dev/key-features/code-mode and https://trueforge.dev/create-agent/overview. Code inspected at commit 5c22006369f8ef1a663dd4f2c6910b26e579e830: `packages/trueforge-core/src/core/capabilities/builtins/LargeToolResponse.ts` and `packages/trueforge-core/src/core/sandbox/codeMode/CodeModeDispatcher.ts`, https://github.com/truefoundry/trueforge/tree/5c22006369f8ef1a663dd4f2c6910b26e579e830. Supports considering script-local tool-result reduction, output-schema discovery, credential bridging, and result offloading. The inspected processor uses head/tail previews and can fail to save; previews do not establish decision coverage. The dispatcher rejects interactive-handling returns, so it alone does not establish approval suspension/resumption despite the documentation claim. Annotation-based approval can miss unlabelled effects.

Adopt the interface and evidence discipline as methodology. Atomic budget reservations, coverage-preserving projections, and per-call effect checks are Livingware design requirements, not claims that either source or this release implements them. No external dependency, paid run, harness replacement, five-service deployment, automatic fan-out, or measured local benefit follows from updating this reference.
