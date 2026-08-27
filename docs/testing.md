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

> Any in-repo production component introduced, modified, or relied upon by an implementation plan must participate in at least one integration test using its real production implementation.

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

### Preferred Browser Harness

The preferred browser is a **Windows-host Chrome instance exposed to WSL through Chrome DevTools Protocol on port `9222`**.

Preferred endpoint from the coding environment:

```text
http://127.0.0.1:9222
```

Browser-test priority:

```text
1. Windows-host Chrome reachable from WSL on port 9222
2. Project-standard real-browser harness only when the project already provides one
3. Fresh local browser only when the coding environment actually has one installed
```

For the standard WSL workflow, do **not** assume Chrome is installed inside WSL and do not install another browser merely to bypass the preferred Windows Chrome test path.

### Shared Chrome Lifecycle

The persistent `9222` instance is operator-owned shared state. Browser tests must use a dedicated fixture-owned page, preserve the natural viewport/window, and avoid `setViewportSize`, device-metrics emulation, or window-bound mutations. Exact synthetic viewport coverage belongs in an isolated browser/profile.

Cleanup must run in `finally`: clear fixture-created metrics overrides, detach CDP sessions, close only fixture-owned pages, disconnect the client transport, and ensure the automation process exits. Completion evidence must confirm the shared endpoint remains reachable and operator tabs remain intact.

When `9222` is reachable from WSL, use WSL/CDP for probing, diagnostics, and cleanup. Do not execute PowerShell merely because Chrome is Windows-hosted. The PowerShell commands below are user-facing launch instructions only for an unavailable endpoint.

If DOM geometry says the app fills `innerWidth` but a screenshot shows unexplained blank space, compare in-page metrics, `Page.getLayoutMetrics`, screenshot pixel dimensions, per-origin site zoom, CDP targets, and stale automation processes before changing CSS. See [the shared Chrome lifecycle reference](../skills/test-driven-development/remote-cdp-browser-lifecycle.md).

### If Chrome on `9222` Is Unavailable

If the agent cannot reach the Chrome DevTools endpoint, it must treat browser availability as a **user-provided test prerequisite**, not silently downgrade the test.

The agent must:

1. Test the endpoint, for example:

   ```bash
   curl -fsS http://127.0.0.1:9222/json/version
   ```

2. If unavailable, tell the user that Windows Chrome needs to be started in remote-debug mode.
3. Provide the Windows launch instruction below.
4. Explain that the debug instance uses a separate profile and does not use the user's normal Chrome profile.
5. Ask the user to run the command and confirm Chrome is open; then retry `9222` and continue the UI test.
6. **Do not claim frontend completion while the required real-browser gate is blocked.**

Recommended Windows PowerShell command:

```powershell
Start-Process "$env:ProgramFiles\Google\Chrome\Application\chrome.exe" `
  -ArgumentList '--remote-debugging-port=9222', "--user-data-dir=$env:TEMP\livingware-chrome-debug"
```

If Chrome is installed under the x86 Program Files directory:

```powershell
Start-Process "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe" `
  -ArgumentList '--remote-debugging-port=9222', "--user-data-dir=$env:TEMP\livingware-chrome-debug"
```

Command Prompt equivalent when `chrome.exe` is on `PATH`:

```cmd
start chrome --remote-debugging-port=9222 --user-data-dir="%TEMP%\livingware-chrome-debug"
```

Modern Chrome requires remote debugging to use a non-default `--user-data-dir`; the dedicated `livingware-chrome-debug` profile is intentional and should be kept separate from the user's normal browser profile.

After Chrome starts, verify from WSL:

```bash
curl -fsS http://127.0.0.1:9222/json/version
```

If Windows Chrome is running but WSL cannot reach `127.0.0.1:9222`, report that as a WSL/Windows host-network reachability problem rather than installing Chrome inside WSL or substituting a mock browser test. Resolve host reachability first, then run the UI gate.

Do **not** silently downgrade a required UI test into jsdom, snapshot-only, shallow-render, mocked component, or source-inspection evidence.

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
real Windows Chrome over CDP
  -> real app route
  -> real rendered component tree
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
- [ ] each new TDD test was observed failing before implementation
- [ ] all changed in-repo production components are exercised by at least one real-component integration test
- [ ] no changed in-repo component is mocked on the integration path being used as completion evidence
- [ ] production wiring / DI / routing is used where practical
- [ ] persistence behavior uses a real test store when persistence is part of the feature
- [ ] external substitutions are explicitly identified and occur only at true external boundaries
- [ ] at least one integration test was observed failing because the implementation or wiring was incomplete
- [ ] the integration suite passes after implementation
- [ ] for product features, integration/E2E evidence exercises the same smallest real journey and realistic inputs declared by the MVL plan
- [ ] a vertical / E2E test exists when the change crosses multiple architectural boundaries or delivers user-visible behavior
- [ ] **any frontend/UI change has real-browser UI test evidence**
- [ ] **Windows Chrome on port `9222` was preferred for WSL frontend work**
- [ ] **if `9222` was unavailable, the user was given the Windows debug-launch instructions and UI completion remained blocked until a real browser became reachable**
- [ ] **UI tests exercise the changed user-visible interaction through the real rendered application**
- [ ] all relevant existing tests still pass

If a plan cannot satisfy the integration gate because a required internal dependency is missing, the dependency must be installed or implemented first. Mocking the missing production component is not a substitute for completing the prerequisite.

If a frontend plan cannot satisfy the UI gate because Windows Chrome is not reachable, browser availability is a test-environment prerequisite. Remind the user to start Chrome with remote debugging; do not replace the browser gate with mocked component tests and call the work complete.

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
