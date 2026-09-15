# Layered Skill Routing, Tool, Eval, and Learning Refactor v1

**Status:** superseded  
**Superseded by:** `docs/plans/2026-09-15-layered-skill-runtime-counterfactual-eval-refactor-v2.md`

This plan established the initial Tool/Policy/Workflow/Router/Skill split, recurrent routing, layer-specific evaluation/learning cadence, canary refactors, and token-regression closure strategy.

The v2 plan is now authoritative. It preserves those decisions and adds the implementation-ready counterfactual/what-if evaluation contract: explicit evidence provenance (`OBSERVED | REPLAYED | SIMULATED | INFERRED | ASSUMED`), deterministic replay, real bounded re-execution, seeded Monte Carlo simulation, and the rule that synthetic evidence may prioritize or falsify candidates but cannot substitute for materially independent observed evidence in generalized learning.

Do not implement from this v1 file. Use the v2 plan and `docs/skill-runtime-architecture.md` as the current architecture basis.
