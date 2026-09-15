# Verification Impact Analysis v1

Status: Active engineering verification policy

Verification Impact Analysis (VIA) selects the smallest verification surface capable of falsifying the claim implied by a change. It exists to reduce CI time, agent latency, and token cost without weakening evidence.

## Principle

Test scope follows observed production impact radius, not diff size and not habit.

```text
changed production surface
  -> relationship-aware impact analysis
  -> affected seams, consumers, trust boundaries, and user paths
  -> smallest sufficient verification
  -> broader verification only when blast radius or uncertainty requires it
```

Prefer a current code graph when it materially improves confidence. `codebase-memory-mcp` can supply `search_graph`, `trace_path`, `query_graph`, `search_code`, and `get_code_snippet`. Whole-repository indexing is not a prerequisite for a bounded change; when graph evidence is unavailable, use targeted static/source evidence and state the lower confidence.

## Radius classes

- `R0` — local behavior only: focused TDD/unit-level behavior evidence.
- `R1` — one production seam: focused integration across the affected seam.
- `R2` — multi-component production path: real-component integration through the affected path.
- `R3` — user journey, UI, cross-process, or multiple architectural boundaries: vertical/E2E evidence; real-browser verification for affected UI behavior.

Broad suites are justified when impact is itself broad or uncertain: shared-core changes, schema migrations, auth/security boundaries, dependency upgrades, release candidates, highly reused abstractions, or unresolved fan-out.

## Stratified verification cadence

VIA composes with a three-cadence verification model:

- `D0 — deterministic invariants`: cheap mechanical checks that protect contracts and may run on every relevant mutation.
- `D1 — local semantic sentinels`: focused behavior/integration checks selected from the current impact radius during implementation.
- `D2 — full semantic audits`: broad or expensive suites reserved for commit/release/high-risk/periodic triggers or when VIA identifies broad uncertainty.

Do not promote every D1 change to D2 merely because automation makes it possible. The purpose of VIA is to spend verification where additional evidence changes confidence.

## Required evidence

For a material change, record enough evidence to answer:

```yaml
verification_impact:
  source: codebase-memory-mcp | equivalent | manual-fallback
  changed_surfaces: [...]
  direct_consumers: [...]
  affected_boundaries: [...]
  user_paths_at_risk: [...]
  uncertainty: low | medium | high
  radius: R0 | R1 | R2 | R3
  selected_tests: [...]
  omitted_broad_suites:
    - suite: ...
      reason: unaffected | redundant | deferred-to-D2
```

The record may live in the implementation plan or task tracker; do not create a separate report when the repository already has an adequate coordination surface.

## Relationship to MVL evaluation

VIA is not the product evaluation loop and R0-R3 are not MVL levels. VIA chooses implementation verification evidence. MVL evaluation measures whether the feature produced the intended value and learning. A feature can be locally verified yet fail its MVL outcome, and an MVL experiment must not weaken the verification needed to establish that the implementation itself is real and correctly wired.

## Relationship to IA-before-UI

`docs/ia-before-ui.md` asks whether a user-facing structure is conceptually correct before production UI coding begins. VIA asks how broadly the resulting code must be verified. For material UI changes the order is:

```text
IA-before-UI
  -> implementation / focused TDD
  -> VIA
  -> affected real-browser/integration evidence
```

Neither gate requires human approval by default.
