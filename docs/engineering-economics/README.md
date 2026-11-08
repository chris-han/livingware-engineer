# Execution Economics Evidence Index

Livingware measures **verified outcome and cost together**. Do not claim a faster or cheaper workflow from lower tokens alone, task-mismatched comparisons, incomplete acceptance or unverified source identity.

| Record | Evidence level | Reported tokens | Wall time | Comparison |
| --- | --- | ---: | --- | --- |
| [Windows Provider-query-only implementation baseline](2026-11-07-windows-provider-query-only-baseline.md) | Local engineering GREEN; historical baseline | 860,727 | 144m | Baseline |
| [Observation 01: Qwen BYOK production recovery](2026-11-08-qwen-byok-production-recovery-observation.md) | Production GREEN; post-optimization observation | 301,595 | 65m31s | **NOT_COMPARABLE** |

[Observation 01 structured receipt](2026-11-08-qwen-byok-production-recovery-receipt.yaml) · [Blank next-run measurement template](next-implementation-receipt.template.yaml) · [Execution economics contract](../../skills/executing-plans/references/execution-economics.md)

**Accounting limitations:** The original baseline lacks token-category/model breakdown; Qwen recovery used retained previously qualified images and excludes earlier repair/failed rollout work. Neither enables a causal percent-savings claim. Future controlled comparisons must specify task scope, acceptance equivalence, model/effort, token accounting convention, planning/verification costs and post-integration rework.
