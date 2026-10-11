# JEVal: optional public development panel

Load only when JEVal is selected for a bounded decision-model evaluation. Apply the shared [decision-model protocol](decision-model-evaluation.md). JEVal is useful public comparison and diagnosis evidence; it is not a universal industry authority or proof of business suitability.

## Source and identity

The dataset owner is [carlosxiang/JEVal on Hugging Face](https://huggingface.co/datasets/carlosxiang/JEVal). A previously used pinned revision is `5d0253c34cf5e371b3ae99c21f0a7170d7289f63`; verify availability, repository identity, license, manifest, files, and content hashes before reuse. Do not silently replace it with latest. Dataset statistics and paper claims are not executable adapter qualification.

Use the project's existing download/cache and manifest owner. An already verified local snapshot can be evaluated offline; this reference does not bundle a downloader, model runtime, dataset, or new dependency. Do not assume a user-specific cache path.

## Declare adapter coverage

Inspect the selected snapshot's actual schema and enum values before transforming examples. Pin state/question construction, allowed options, reference-label decoding, and probability direction.

A native binary `noul` adapter measures only its supported binary subset. Preserve TRUE/FALSE semantics; verify both classes with deterministic fixtures and hard negatives. Never assume TRUE is option index 1 without verifying the schema and adapter.

`choice`, `score`, or other types require their own explicit semantics and qualified adapter. Treat them as unsupported if that adapter is absent; do not coerce them to binary, drop them without accounting, or advertise a binary slice as the full JEVal score. Report snapshot total, supported-type total, selected-panel total, exclusions, and valid/invalid/failure counts separately.

## Panels and exposure

Preserve source row/item identities and normalized-state identity. Build connected groups across repeated source items and equal normalized states; audit near-duplicates and keep entire groups together. Exclude earlier development/calibration panels and their connected duplicates from a fresh transfer panel. Retain an exposure ledger across runs.

Freeze deterministic selection, group assignment, seed, label counts, CAL/EVAL membership and hashes before fitting. An aggregate source revision does not prove split independence. Mark exposed public panels as PUBLIC_DEVELOPMENT; do not rename them sealed confirmation merely because they were freshly sampled.

Fit probability/threshold repairs only on CAL and seal parameters before EVAL inference/reduction. Keep original and repaired predictions on the same EVAL cases, both class recalls, ranking, calibration, baselines, and resource costs. Replay verifies computation, not independent generalization.

## Use the existing project operator

Inspect the repository for an existing JEVal adapter, its help/contract, and its tests. Reuse qualified operators for snapshot integrity, panel freeze, inference, metric reduction, and independent replay. Do not invent a runnable command or install a framework merely because this reference is loaded.

If the operator is missing, route to evaluator design for the smallest supported-type adapter and deterministic schema/mapping/replay checks. Request execution details only when unavailable and necessary; do not launch training, paid calls, or a successor experiment implicitly.

## Interpretation and handoff

- Both-class decision improvement after a CAL-only repair supports a bounded public transfer observation.
- Preserved ranking with collapsed predictions motivates readout/threshold diagnosis; it does not prove global representation health.
- A strong aggregate score can still fail a predeclared class-recall gate.
- Beating a collapsed fine-tuned baseline does not prove fine-tuning beats the original backbone.
- Public-development results leave business suitability unverified. Use a separate real decision distribution and frozen utility/error-cost gates before a deployment claim.

Preserve unsuccessful repairs and their failed gates. Report what was observed, replayed, unsupported, and unverified; leave project-specific scores, thresholds, artifacts, and business policies with the project owner.
