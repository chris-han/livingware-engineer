# IA-before-UI + Verification Impact Analysis MVL Acceptance — 2026-09-15

## Scope

This record closes the Livingware Engineer 6.9.3 acceptance slice for the combined planning workflow:

```text
requirement / MVL hypothesis
  -> IA-before-UI when applicable
  -> implementation
  -> focused TDD
  -> Verification Impact Analysis
  -> smallest sufficient integration/browser/E2E evidence
  -> MVL measurement and re-test
```

The acceptance question is whether the planner preserves IA-before-UI as a structural pre-implementation gate for material user-facing changes while using Verification Impact Analysis only to choose the smallest sufficient post-change verification surface.

## Deterministic contract evidence

Command:

```bash
python3 tests/writing-plans/test_ia_via_plan_contract.py
```

Observed result after commit `f4613b38b8ca1700da120da117f89fe63a16eda9`:

```text
[PASS] test_combined_ia_via_contract_is_explicit
[PASS] test_plan_template_orders_ia_before_implementation_and_via_before_integration
[PASS] test_plan_header_requires_both_reviews
[PASS] test_ia_gate_is_structural_not_default_human_approval
[PASS] test_via_keeps_test_scope_separate_from_mvl_value_evaluation
IA/VIA deterministic contract: PASS
```

This establishes that:

- IA-before-UI is explicit in the planner contract;
- IA precedes production UI implementation;
- Verification Impact Analysis follows implementation and precedes integration-scope selection;
- IA is a structural engineering gate rather than a default human-approval checkpoint;
- duplicate semantic ownership is an explicit `REVISE_IA` condition;
- VIA R0-R3 / D0-D2 scope selection remains distinct from MVL product-value evaluation.

## Live Codex MVL evidence

Command:

```bash
CODEX_PROBE_TIMEOUT=180 \
bash tests/codex/live-ia-via-mvl-probe.sh
```

Observed artifact root:

```text
.artifacts/ia-via-mvl-probe/20260915T132733Z
```

Observed results:

| Scenario | Behavior | Runtime | Duration |
| --- | --- | --- | ---: |
| `ui-ia-change` | PASS | PASS | 94 s |
| `local-r0-maintenance` | PASS | PASS | 59 s |
| `duplicate-semantic-owner` | PASS | PASS | 61 s |

The probe therefore demonstrated three distinct routing/planning outcomes:

1. a legitimate material UI information-architecture change receives an IA-before-UI disposition and UI-appropriate verification scope;
2. a bounded non-UI maintenance change remains `R0` without unnecessary browser/E2E expansion;
3. conflicting semantic ownership returns `REVISE_IA` rather than planning production UI implementation around the conflict.

## Related packaging portability evidence

The focused Codex package test also passed on a deliberately restricted PATH excluding `jq`, `unzip`, `zip`, `tar`, and `shasum`:

```bash
bash tests/codex/test-package-codex-plugin.sh
```

Result:

```text
All Codex package portability tests passed
```

This is source-tooling evidence and does not alter the IA/VIA runtime acceptance decision.

## Disposition

```text
DETERMINISTIC CONTRACT: PASS
LIVE MVL:              PASS
PACKAGING PORTABILITY: PASS

6.9.3 IA/VIA ACCEPTANCE: GREEN
```

No additional synthetic acceptance runs are required for this slice. Further evidence should come from real Semantier planning work: whether IA-before-UI reduces semantic/layout rework and whether VIA reduces unnecessary verification cost while preserving defect detection.
