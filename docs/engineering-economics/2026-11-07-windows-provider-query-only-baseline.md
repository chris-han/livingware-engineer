# Baseline — Semantier Windows Provider-query-only Model Discovery (2026-11-07)

**Purpose:** retain an evidence-bounded historical denominator for testing the *hypothesis* that focused adversarial plan review, earlier real-component/native smoke, stage-context compaction and impact-based reruns reduce total cost without weakening acceptance.

**Evidence source:** archived Semantier plan `docs/plans/archive/2026-11-07-windows-provider-query-only-model-discovery-v1.md` in `/home/chris/repo/semantier-runtime`, especially W0–W3 checkpoints and terminal notes; user-provided completion and usage summary. This is not a complete raw Codex turn/tool transcript.

| Field | Baseline |
| --- | --- |
| Outcome | Local development GREEN; Hermes and parent main integration, native Windows synthetic acceptance |
| Total reported tokens | **860,727** (approximate user-reported aggregate; inclusion of cached tokens and planning unspecified) |
| Elapsed | **144 min** (2 h 24 min, user-reported) |
| Approximate aggregate rate | **5,977 tokens/min**, descriptive only; not a throughput or efficiency benchmark |
| Model / effort / token unit accounting | **UNKNOWN** |
| Input vs output vs cached token split | **UNKNOWN** |
| Actual API spend / prices | **UNKNOWN**; do not invent dollar cost |
| Baseline plan | `2026-11-07-windows-provider-query-only-model-discovery-v1` |
| Hermes integrated commit | `6e7aa7300d826f5f44c0663c95db2eedd309ed9a` |
| Parent pointer commit | `7c650c455e` |
| Parent archival main | `d69ab6c6291331610fb500894c353e1c9622f0af` |
| Release/production qualification | **Not performed** |

## Observed checkpoint and test evidence

- W0: reviewed four upstream PRs and inspected producer/cache/RPC/REST/native readiness owners. No evidence that the same work was needlessly repeated within this run.
- Early W1: focused Python runs **45** then **47** passed after changing producer/cache contracts.
- W1–W3: **320 UI** and **80 Python** passes at a pre-style-repair state; **89 focused UI** after native-discovered UI defects.
- Frozen/merged candidate: **361 UI** and **77 Python** passes; desktop typecheck and scoped lint.
- Final impacted follow-up: **111 UI** and **77 Python** passes; **10 parent integration/qualification tests**; native Windows synthetic cold/warm launch, refreshed/empty/failure snapshots, scoped profile switch, Main Apply and Composer selection. Unchanged portions of the earlier 361 UI evidence were explicitly reused; do not add all pass counts as unique tests.

## Root cause / rework observations

1. **Cold Apply timeout:** a client timeout occurred before the backend persisted successfully; 30-second request budget was extended to an existing 60-second budget. Detected in native journey, then fixed and retested.
2. **Warm-cache profile switching:** after early integration, the Composer could display cached results without promptly refreshing the new profile; the execution worktree had to be recreated and the native fixture retested.
3. **Repeated testing:** several focused and broad runs occurred at different code SHAs and scopes. These are not proven unnecessary reruns; late discovered boundary defects suggest earlier test design and ordering could reduce cost.
4. **Context-loading overhead:** no per-read/per-turn token or tool ledger for this run was retained; do not attach specific token counts or savings percentages to rereads, tests or review.

## Hypothesis and next-run comparison

**Hypothesis (unproven):** when applicable, a single evidence-based pre-execution failure review with early lifecycle counterexamples, focused test selection, compact stage receipts and one suitably frozen broad regression reduces post-integration rework and total tokens to comparable verified completion.

For the next eligible cross-component implementation, capture actual model/effort, token accounting definitions, planning-review tokens, implementation tokens, cached-input tokens, tool time, raw outcome, acceptance coverage, late rework and test rerun reasons. At completion, report total-to-verified-GREEN and wall time against **860,727 tokens / 144 min**, only with explicit comparability caveats; do not present a percentage as causal evidence for a different-sized task.

**Do not weaken correctness to beat the benchmark:** a non-GREEN or reduced-acceptance successor is not an efficiency improvement. One next run is a paired historical comparison for learning, not a controlled causal study. See [execution economics](../../skills/executing-plans/references/execution-economics.md) and [pre-execution failure review](../../skills/writing-plans/references/pre-execution-failure-review.md).
