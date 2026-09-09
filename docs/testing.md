# Testing Livingware Engineer

Livingware Engineer uses three distinct test layers. A feature is not complete merely because local TDD tests pass.

For product features, all test layers are evidence inside one **Minimum Viable Loop (MVL)**. They must verify the same smallest real user journey declared by the plan rather than becoming disconnected component exercises.

## Test Strategy

### L1 — TDD Behavior Tests

Purpose: prove local behavior and regressions at the smallest useful scope.

Requirements:
- write the test first and watch it fail for the expected reason
- implement the minimum production code required to make it pass
- assert observable behavior, not mock call existence
- use real production code wherever practical
- mocks are allowed only at slow, nondeterministic, or genuinely external boundaries
- for product features, derive behavior from the plan's MVL journey and realistic trial inputs rather than inventing test-only semantics

TDD answers:

> Does this component behave correctly in isolation?

It does **not** prove that the production architecture is actually wired together.

### L2 — Real-Component Integration Tests

Purpose: prove that the production components introduced, modified, or relied upon by the implementation actually work together **for the same smallest real journey defined by the MVL plan**.

**Mandatory rule:**

> When the assessed impact requires integration (R1–R3), affected in-repo components on that path must participate as their real production implementations. R0 local-only changes may use focused behavior tests. See [impact-radius selection](../skills/test-driven-development/impact-radius-testing.md); use [verification-before-completion](../skills/verification-before-completion/SKILL.md) for valid result reuse.

For product features, the integration test must also preserve the plan's MVL contract:
- same target user / job-to-be-done
- same smallest real journey
- same realistic trial inputs or a documented representative subset
- same user-visible or externally observable outcome
- same critical technical success conditions

Do not create an integration test that merely proves components can call one another if it does not exercise the feature journey the user is supposed to try.

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
- substitute a synthetic test journey for the MVL journey merely because it is easier to automate

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

> Does the architecture described by the implementation actually exist and work as connected production code for the feature journey we intend users to try?

### L3 — Vertical / End-to-End Tests

Purpose: prove a meaningful user-visible or externally observable path through the system.

Use this layer when the implementation spans multiple architectural boundaries, gateways, persistence surfaces, processes, runtime components, **or any frontend/UI behavior**.

For product features, the vertical/E2E test is the executable form of the MVL's smallest real user journey. Do not choose a different happy path solely because it is easier to automate.

A vertical test should exercise the real application entry point where practical and verify the final observable result. Genuine external systems may still be substituted at their external boundary.

End-to-end testing answers:

> Can the implemented system deliver the intended behavior through its real production path?

## Frontend / UI Test Mandate

Any change that creates, modifies, or can regress user-visible frontend behavior requires executable browser-based UI verification before completion.

**Mandatory rule:**

> Frontend code is not complete until the changed UI path has been exercised in a real browser.

For a product feature, the browser path should be the same user journey named in the MVL contract, not a separate UI-only demonstration.

This applies to changes involving, for example:
- React/Vue/Svelte components
- routes, pages, dialogs, menus, forms, tables, graphs, canvases, and visualization surfaces
- CSS/layout/theme behavior that affects user interaction or visibility
- frontend state management that changes rendered behavior
- frontend/backend wiring that changes what the user can see or do
- keyboard, pointer, focus, navigation, accessibility, or responsive interaction behavior

### Browser Selection and Lifecycle

Follow the [browser selection and CDP lifecycle contract](../skills/test-driven-development/remote-cdp-browser-lifecycle.md), which owns engine choice, endpoint setup, process ownership, and cleanup. Choose by what the acceptance criterion must prove, not by which browser happens to be running.

A missing browser blocks only a gate assigned to that evidence lane. Do not substitute DOM simulators or mocked components for required real-browser verification.

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
- follow the selected test cycle: fail-then-pass for new behavior/defects; adequate green-before/green-after coverage for behavior-preserving refactors

For visual-only changes, browser verification must inspect the rendered result at the natural viewport; use an isolated browser/profile for exact synthetic viewport coverage. A unit test that merely checks CSS class names is not sufficient completion evidence.

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
real browser selected for the required evidence lane
  -> real app route
  -> real component tree / DOM
  -> real user interaction
  -> visible final state
```

## MVL Test Alignment

For product features, the plan's MVL Contract is the shared source of truth for all completion evidence.

Before writing integration, browser, or E2E tests, compare the test against the plan:

```text
MVL plan                         Test evidence
---------------------------------------------------------------
Target user / JTBD          ->   test actor / scenario
Smallest real journey       ->   integration/E2E path
Realistic trial inputs      ->   fixtures / seeded data
Technical success metrics   ->   assertions / measured outputs
UX success metrics          ->   browser/user-task observations
Feedback capture            ->   telemetry/correction assertions
Re-test surface             ->   stable repeatable test/eval command
```

If those columns no longer describe the same feature, stop and reconcile the plan or test. Do not let local implementation convenience redefine the MVL.

The test suite establishes **implementation credibility**. Product learning then uses the same journey and trial inputs for technical/UX measurement, feedback, diagnosis, improvement, and comparable re-test.

```text
Implementation credible
  = TDD + real integration + real browser when UI + vertical/E2E when needed

MVL complete
  = credible implementation
  + technical measurement
  + UX measurement
  + feedback
  + required evidence-driven improvement
  + comparable re-test
```

## Completion Gate

Before an architectural implementation is marked complete:

- [ ] L1 TDD behavior tests exist for changed behavior
- [ ] the change-specific test cycle in test-driven-development is satisfied
- [ ] all changed in-repo production components are exercised by at least one real-component integration test
- [ ] no changed in-repo component is mocked on the integration path being used as completion evidence
- [ ] production wiring / DI / routing is used where practical
- [ ] persistence behavior uses a real test store when persistence is part of the feature
- [ ] external substitutions are explicitly identified and occur only at true external boundaries
- [ ] new behavior/wiring defects have a failing integration control; behavior-preserving refactors retain adequate passing integration coverage
- [ ] the integration suite passes after implementation
- [ ] for product features, integration/E2E evidence exercises the same smallest real journey and realistic inputs declared by the MVL plan
- [ ] a vertical / E2E test exists when the change crosses multiple architectural boundaries or delivers user-visible behavior
- [ ] **any frontend/UI change has real-browser UI test evidence**
- [ ] **browser selection and cleanup follow the canonical CDP lifecycle contract**
- [ ] **any unavailable required browser is reported against its selected evidence lane, not unrelated UI work**
- [ ] **UI tests exercise the changed user-visible interaction through the real rendered application**
- [ ] all relevant existing tests still pass

If a plan cannot satisfy the integration gate because a required internal dependency is missing, the dependency must be installed or implemented first. Mocking the missing production component is not a substitute for completing the prerequisite.

If the browser required by the selected evidence lane is unavailable, follow the canonical lifecycle contract to start it or report the missing prerequisite. Keep that gate unverified; continue independent work without replacing required real-browser checks with mocks.

## Integration Contract in Implementation Plans

Implementation plans should explicitly declare their integration contract before coding begins and tie it to the MVL contract:

```yaml
mvl_contract:
  target_user: ...
  job_to_be_done: ...
  smallest_real_journey: ...
  realistic_trial_inputs: ...
  technical_metrics: ...
  ux_metrics: ...
  feedback_capture: ...
  re_test_surface: ...

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
    environment: wsl
    preferred_browser: windows_chrome_cdp
    preferred_browser_endpoint: http://127.0.0.1:9222
    unavailable_action: instruct_user_to_start_windows_chrome_debug
    completion_blocked_until_browser_verified: true
```

This prevents an implementation agent from silently replacing an inconvenient dependency, unavailable browser, or intended user journey with an easier test double/scenario and then claiming the design is complete.

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
