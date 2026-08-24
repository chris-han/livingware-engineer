# Testing Livingware Engineer

Livingware Engineer uses three distinct test layers. A feature is not complete merely because local TDD tests pass.

## Test Strategy

### L1 — TDD Behavior Tests

Purpose: prove local behavior and regressions at the smallest useful scope.

Requirements:
- write the test first and watch it fail for the expected reason
- implement the minimum production code required to make it pass
- assert observable behavior, not mock call existence
- use real production code wherever practical
- mocks are allowed only at slow, nondeterministic, or genuinely external boundaries

TDD answers:

> Does this component behave correctly in isolation?

It does **not** prove that the production architecture is actually wired together.

### L2 — Real-Component Integration Tests

Purpose: prove that the production components introduced, modified, or relied upon by the implementation actually work together.

**Mandatory rule:**

> Any in-repo production component introduced, modified, or relied upon by an implementation plan must participate in at least one integration test using its real production implementation.

Integration tests must:
- traverse the changed production path through real in-repo components
- use production constructors, dependency injection, routing, adapters, repositories, or wiring where practical
- use a real test persistence implementation such as temporary SQLite, filesystem sandbox, containerized database, or equivalent when the persistence layer is part of the behavior
- fail when an internal component is replaced, omitted, miswired, or violates its boundary contract
- be observed failing before the implementation or wiring fix when the test is introduced for new behavior
- pass only after the production path is correctly implemented

Integration tests must not:
- replace an in-repo production service with a mock, fake, stub, or hard-coded answer when that service is part of the architecture being verified
- assert only that mocks were called
- recreate the production path entirely inside test fixtures
- treat a mocked internal architecture as evidence that the design was implemented

Permitted substitutions are limited to true external or nondeterministic boundaries, for example:
- remote LLM providers
- third-party SaaS APIs
- payment gateways
- external email/SMS systems
- expensive remote vector services

When those boundaries are substituted, the test should keep the in-repo adapter/client real and substitute only the remote side where possible.

Examples:

```text
GOOD
real API route
  -> real domain service
  -> real evaluator
  -> real repository
  -> temporary SQLite database
```

```text
GOOD
real workflow service
  -> real provider adapter
  -> local HTTP stub standing in for third-party SaaS
```

```text
NOT ACCEPTABLE AS INTEGRATION EVIDENCE
real API route
  -> MockDomainService
  -> expected payload
```

```text
NOT ACCEPTABLE AS INTEGRATION EVIDENCE
real DecisionService
  -> FakeSemanticMatcher(return="expected")
```

Integration testing answers:

> Does the architecture described by the implementation actually exist and work as connected production code?

### L3 — Vertical / End-to-End Tests

Purpose: prove a meaningful user-visible or externally observable path through the system.

Use this layer when the implementation spans multiple architectural boundaries, gateways, persistence surfaces, processes, runtime components, **or any frontend/UI behavior**.

A vertical test should exercise the real application entry point where practical and verify the final observable result. Genuine external systems may still be substituted at their external boundary.

End-to-end testing answers:

> Can the implemented system deliver the intended behavior through its real production path?

## Frontend / UI Test Mandate

Any change that creates, modifies, or can regress user-visible frontend behavior requires executable browser-based UI verification before completion.

**Mandatory rule:**

> Frontend code is not complete until the changed UI path has been exercised in a real browser.

This applies to changes involving, for example:
- React/Vue/Svelte components
- routes, pages, dialogs, menus, forms, tables, graphs, canvases, and visualization surfaces
- CSS/layout/theme behavior that affects user interaction or visibility
- frontend state management that changes rendered behavior
- frontend/backend wiring that changes what the user can see or do
- keyboard, pointer, focus, navigation, accessibility, or responsive interaction behavior

### Preferred Browser Harness

When a remote-debuggable Chrome instance is available, **prefer connecting to Chrome DevTools Protocol on port `9222`** rather than launching an isolated browser instance.

Preferred endpoint:

```text
http://127.0.0.1:9222
```

The browser test should reuse the real running application/session through that Chrome instance when practical. This is preferred because it validates the actual local runtime, authenticated/session state, browser environment, and visible integration path instead of a synthetic test-only browser setup.

Browser-test priority:

```text
1. Existing remote Chrome on 127.0.0.1:9222
2. Project-standard real-browser harness (Playwright/Puppeteer/etc.)
3. Fresh local browser instance if remote Chrome is unavailable
```

Do **not** silently downgrade a required UI test into jsdom, snapshot-only, shallow-render, mocked component, or source-inspection evidence.

If `9222` is unavailable, record that fact and use the next real-browser option. Lack of remote Chrome is not permission to skip UI verification.

### UI Test Requirements

UI completion evidence must:
- run against a real browser engine
- navigate through the changed user-visible path
- use the real frontend bundle and real in-repo frontend components
- use the real backend/integration path where that behavior is part of the change
- exercise meaningful user interaction, not only page load
- assert the final visible or interactive outcome
- verify browser console/runtime errors are absent for the tested flow where practical
- capture screenshot, DOM state, accessibility state, or equivalent evidence when useful for the change
- be observed failing when the UI behavior or wiring is incomplete, then passing after the implementation

For visual-only changes, browser verification must inspect the rendered result at the relevant viewport(s); a unit test that merely checks CSS class names is not sufficient completion evidence.

For interaction changes, the browser test must execute the interaction itself: click, type, select, drag, keyboard navigation, route change, graph interaction, etc.

### What Does Not Count as UI Completion Evidence

```text
NOT SUFFICIENT
React component unit test with mocked children
```

```text
NOT SUFFICIENT
jsdom test asserting className="active"
```

```text
NOT SUFFICIENT
snapshot changed and test passes
```

```text
SUFFICIENT SHAPE
real Chrome
  -> real app route
  -> real rendered component tree
  -> real user interaction
  -> visible final state
```

## Completion Gate

Before an architectural implementation is marked complete:

- [ ] L1 TDD behavior tests exist for changed behavior
- [ ] each new TDD test was observed failing before implementation
- [ ] all changed in-repo production components are exercised by at least one real-component integration test
- [ ] no changed in-repo component is mocked on the integration path being used as completion evidence
- [ ] production wiring / DI / routing is used where practical
- [ ] persistence behavior uses a real test store when persistence is part of the feature
- [ ] external substitutions are explicitly identified and occur only at true external boundaries
- [ ] at least one integration test was observed failing because the implementation or wiring was incomplete
- [ ] the integration suite passes after implementation
- [ ] a vertical / E2E test exists when the change crosses multiple architectural boundaries or delivers user-visible behavior
- [ ] **any frontend/UI change has real-browser UI test evidence**
- [ ] **remote Chrome at `127.0.0.1:9222` was preferred when available**
- [ ] **UI tests exercise the changed user-visible interaction through the real rendered application**
- [ ] all relevant existing tests still pass

If a plan cannot satisfy the integration gate because a required internal dependency is missing, the dependency must be installed or implemented first. Mocking the missing production component is not a substitute for completing the prerequisite.

If a frontend plan cannot satisfy the UI gate because no browser is available, browser availability is a test-environment prerequisite. Do not replace the browser gate with mocked component tests and call the work complete.

## Integration Contract in Implementation Plans

Implementation plans should explicitly declare their integration contract before coding begins:

```yaml
integration_contract:
  real_components_required:
    - ComponentA
    - ComponentB
    - RepositoryC

  permitted_test_substitutes:
    - external_llm_gateway
    - third_party_api

  forbidden_mocks:
    - ComponentA
    - ComponentB
    - RepositoryC

  ui_test:
    required: true
    preferred_browser_endpoint: http://127.0.0.1:9222
    fallback: project_standard_real_browser
```

This prevents an implementation agent from silently replacing an inconvenient dependency with a test double and then claiming the design is complete.

## Existing Repository Test Surfaces

Livingware Engineer itself has two repository-level test families:

- **`tests/`** — plugin and runtime code tests, including Bash + Node + Python integration tests for brainstorm-server JS, OpenCode plugin loading, Codex plugin sync, Kimi wiring, and related utilities.
- **`evals/`** — agent behavior evaluations using real LLM sessions. The Drill harness drives real Claude Code / Codex / Gemini CLI sessions, with actor and verifier roles judging skill compliance.

### Plugin tests

Live in `tests/`. Currently:

- `tests/brainstorm-server/` — node test suite for the brainstorm server JS code.
- `tests/opencode/` — bash tests for OpenCode plugin loading, bootstrap caching, and tool registration.
- `tests/codex-plugin-sync/` — bash sync verification.
- `tests/kimi/` — bash/Python checks for Kimi plugin manifest wiring.
- `tests/claude-code/test-helpers.sh`, `analyze-token-usage.py` — utilities used by remaining bash tests.
- `tests/claude-code/test-subagent-driven-development.sh` — agent-can-describe-SDD test.
- `tests/claude-code/test-subagent-driven-development-integration.sh` — extended SDD integration with token analysis.
- `tests/claude-code/test-worktree-native-preference.sh` — RED-GREEN-REFACTOR validation for worktree skill.
- `tests/explicit-skill-requests/` — multi-turn and skill-name-prompted tests not covered by Drill.

Run plugin tests via the relevant directory's `run-*.sh` or `npm test`.

## Skill Behavior Evals

Live in `evals/`. Drill is the harness; scenarios live at `evals/scenarios/*.yaml`. See `evals/README.md` for setup. Quick start:

```bash
cd evals
uv sync --extra dev
export ANTHROPIC_API_KEY=sk-...
uv run drill run triggering-test-driven-development -b claude
```

Drill scenarios are slow and run real LLM sessions. They are not part of CI today; the natural follow-up is a tiered model with a fast subset on PR and a full sweep nightly or on demand.
