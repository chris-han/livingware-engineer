# Impact-Radius Test Selection

Use this reference when deciding how far a code change should escalate beyond local TDD.

## Core Rule

**Choose test scope from production impact radius, not diff size.**

A one-line change can require integration or E2E coverage if it changes a boundary used by multiple production consumers. A large pure-function refactor may require only focused local tests if its observable contract is unchanged.

When Codebase MCP or an equivalent code graph is available, use it before deciding the required test surface.

## Impact-Radius Assessment

For each changed symbol, file, route, schema, dependency, or configuration surface, inspect:

- direct callers
- direct callees / dependencies
- downstream consumers
- dependency-injection and factory wiring
- API routes / handlers / serializers
- persistence, schema, transaction, cache, and migration edges
- events, queues, async callbacks, schedulers, or process boundaries
- authorization / trust boundaries
- frontend routes, components, state consumers, and user interaction paths
- shared libraries or abstractions with broad fan-out

Prefer Codebase MCP queries that expose call graph, dependency graph, references, consumers, or impact analysis. Record the materially affected production path rather than relying on file proximity.

## Test-Scope Decision

Use the smallest test surface that covers the observed impact radius.

```text
Radius R0 — local only
  changed behavior has no meaningful production-boundary impact
  -> focused TDD / unit-level behavior test

Radius R1 — one production seam
  caller/callee contract, adapter, repository, serializer, or component boundary changes
  -> focused integration test across that seam

Radius R2 — multi-component production path
  multiple real in-repo components or persistence/wiring are affected
  -> real-component integration test through the affected path

Radius R3 — user journey / cross-process / UI path
  user-visible behavior or multiple architectural boundaries are affected
  -> vertical/E2E; real-browser verification for UI
```

Do not interpret these as test taxonomy for MVL. **MVL is the feature-development unit.** R0-R3 only select verification scope for a particular implementation change inside that feature.

## Escalation Triggers

Integration evidence is normally required when impact analysis shows any of these:

- caller/callee interface or DTO/schema contract changed
- dependency injection, factory, routing, or registration changed
- repository or persistence semantics changed
- serialization/deserialization changed
- transaction or consistency boundary changed
- process/network boundary changed
- event/async ordering changed
- authorization/trust boundary changed
- frontend/backend interaction changed
- shared component has materially affected downstream consumers
- a production component is newly introduced into the feature path

Vertical/E2E evidence is normally required when impact analysis shows:

- multiple architectural boundaries on the same affected path
- the MVL's smallest real user journey can regress
- frontend behavior is user-visible or interactive
- a cross-process or external-entry-point contract changed

## Avoid Full-Suite Escalation

Do not use this rule:

```text
any code change -> all integration tests -> full E2E
```

Use this instead:

```text
changed production surface
  -> Codebase MCP impact radius
  -> affected seams and consumers
  -> narrowest sufficient verification
```

If existing integration/E2E coverage already traverses the affected seam, run that focused existing test instead of creating another overlapping test.

Run broader suites when blast radius itself is broad or uncertainty is high, such as shared-core changes, schema migrations, auth/security changes, dependency upgrades, release candidates, or highly reused abstractions.

## Plan Contract

For implementation plans, record impact analysis before declaring the Integration Contract:

```yaml
impact_radius:
  source: codebase_mcp
  changed_surfaces:
    - ...
  direct_consumers:
    - ...
  affected_boundaries:
    - ...
  user_paths_at_risk:
    - ...
  radius: R0|R1|R2|R3

integration_contract:
  required_scope: local|focused_integration|real_component_integration|vertical_e2e
  real_components_required:
    - ...
  existing_tests_to_run:
    - ...
  new_tests_required:
    - ...
```

If Codebase MCP is unavailable, use the best available static references, search, call hierarchy, dependency graph, route map, and repository knowledge, and record that the impact assessment is lower confidence.

## Final Principle

> **Escalate test scope only when the observed production impact radius requires more trust than local behavior tests can provide.**
