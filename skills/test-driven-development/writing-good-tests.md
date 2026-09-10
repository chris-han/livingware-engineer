# Writing Good Tests

**Load this reference when:** writing or changing tests, adding mocks, adding cleanup/helper methods for tests, or verifying frontend behavior.

## Overview

A test exists to catch a specific break. Four principles govern everything here:

```
1. Every test names the break it catches
2. Every test exercises the real thing
3. Architectural completion requires real-component integration
4. Frontend completion requires real-browser evidence
```

Strict TDD produces the first two naturally: a test written first and watched failing against real code has already proven it can fail, and only earns a mock when the real dependency proves slow or external.

The third principle closes a different failure mode: a set of locally correct components can still be miswired, omitted, or replaced with mocks. Unit-level TDD cannot prove the production architecture exists. Real-component integration must do that.

The fourth principle closes the frontend equivalent: component tests, jsdom, snapshots, and mocked children can all pass while the actual browser renders or behaves incorrectly. User-visible frontend work therefore requires a real browser.

## Principle 1: Name the Break

Before writing the test body, answer: **what production change should make this test fail — and is that change a bug or a decision?** A test earns its place by catching a wrong branch, missing side effect, wrong argument, boundary case, or broken contract.

**Derive expectations independently.** Use literals and hand-checked fixtures; table-driven tests with literal `want` values are the preferred shape. An expectation computed by the code under test — or its helpers — passes no matter what that code does:

```typescript
// ❌ Mirror assertion: the same builder computes both sides — always true
const expected = buildSearchQuery({ tag: 'urgent' });
expect(buildSearchQuery({ tag: 'urgent' })).toBe(expected);

// ✅ Hand-derived literal
expect(buildSearchQuery({ tag: 'urgent' })).toBe('tag:"urgent"');
```

**No change detectors.** If only intentional decisions can fail a test — a constant's value, exact message wording, private structure — it fires on redesign and sleeps through bugs. Test the behavior that depends on the decision: not `expect(MAX_RETRIES).toBe(5)` but "a failing call is retried 5 times and the 6th attempt never happens."

**Behavior, not text.** Asserting that a script, skill, or config contains an exact line proves only that the source is the source. Run scripts against controlled inputs and assert outputs, side effects, or exit codes. Documents that instruct agents are tested by the consuming agent's behavior; prose for humans earns no test at all.

**Your code, not the framework.** Test the contract your code makes at its boundaries — the route you register, the query you emit, the payload you produce. Upstream mechanics are their maintainers' tests to write. When upstream behavior genuinely surprised you, write one narrow characterization test naming the assumption. The same boundary applies inside your code: constructors, getters, constants, and trivial forwarding earn tests only when they validate, normalize, default, derive, enforce, or cause side effects — otherwise assert the first consumer-visible result that depends on them.

### Gate Function

```
BEFORE writing the test body:
  Name the production change that would make this test fail.

  Cannot name one            → redesign around an observable behavior
  "The source text changed"  → run the artifact and assert its effects
  Only intentional decisions → change detector; test the behavior
                               that depends on the decision

  Confirm the expected value is derived without the code under test.
  IF it reuses the code's logic or helpers:
    Replace it with a literal or hand-checked fixture
```

## Principle 2: Exercise the Real Thing

**The mock earns no assertions.** A mock assertion passes when the mock is present and fails when it is absent — it says nothing about the component. Assert the real component's behavior; if the mock is what you are checking, unmock it or delete the assertion.

```typescript
// ✅ Real behavior
expect(screen.getByRole('navigation')).toBeInTheDocument();

// ❌ Mock existence
expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
```

**Mock at the right level.** Learn every side effect of the real method before replacing it; mock the slow or external operation and keep what the test depends on real. When unsure, run the test against the real implementation first and observe what actually needs to happen.

```typescript
// ❌ The mock swallows the config write that duplicate detection reads
vi.mock('ToolCatalog', () => ({
  discoverAndCacheTools: vi.fn().mockResolvedValue(undefined)
}));

// ✅ Mock only the slow server startup; the config write stays real
vi.mock('MCPServerManager');
```

**Make doubles specific.** When arguments, call counts, or ordering are part of the contract, assert them — a fake that accepts anything verifies nothing. Give each branch its own fixture or spy, so the wrong branch cannot satisfy the expectation.

**Mirror real data completely.** Mock the complete structure as it exists in reality — all documented fields — not just the ones your test reads. Partial mocks fail silently when downstream code reads an omitted field: the test passes while integration breaks.

**Production classes carry production methods only.** Cleanup that only tests need lives in test utilities, never as a `destroy()` on the production class. Ask: is this method called only from tests? Does this class own this resource's lifecycle? Wrong answers → test utility.

**Prefer real components over complex mocks.** When mock setup outgrows the test logic, mocks miss methods the real components have, or tests break when the mock changes, switch to an integration test with real components.

### Gate Function

```
BEFORE adding a mock or test helper:
  List the real method's side effects; keep the ones the test
  depends on real — mock the slow/external level below them.

  Mock responses mirror the complete real structure.

  A method only tests call lives in test utilities, not production.

  About to assert on the mock itself?
    Unmock it or delete the assertion.
```

## Principle 3: Prove the Architecture Exists

A passing unit suite can still describe a system that does not exist in production. For architectural work, test doubles must not replace the very components the design claims to connect.

**Mandatory integration rule:**

> Every in-repo production component introduced, modified, or relied upon by the implementation must participate in at least one test using its real implementation.

The integration test should follow the changed production path through real wiring, real adapters, real repositories, and real persistence where those are part of the feature. Substitute only true external boundaries.

```text
✅ Integration evidence
real route -> real service -> real evaluator -> real repository -> temp SQLite

❌ Not integration evidence
real route -> MockService -> expected response
```

A fake database may be acceptable only when the database itself is not part of the behavior under test and the repository remains real. If persistence semantics matter, use a real test instance: temporary SQLite, ephemeral filesystem, containerized service, or equivalent.

When an internal dependency is missing, do not mock past the gap. Treat it as a prerequisite: install or implement the dependency, then run the real-component test.

### Integration Gate Function

```
FOR each changed production path:
  List every in-repo component on that path.
  Mark each one REAL or SUBSTITUTED.

  Any in-repo component SUBSTITUTED?
    → integration evidence invalid unless the component itself is the external boundary

  Any external dependency substituted?
    → keep the in-repo adapter/client real; substitute the remote side

  Apply the test cycle selected by test-driven-development:
    new behavior/defect → observe the intended failure, then green
    behavior-preserving refactor → adequate baseline remains green

  Does it now pass through production wiring?
    yes → integration gate satisfied
```

## Principle 4: Prove the UI in a Real Browser

Any frontend/UI change requires browser-level verification because DOM simulators and component tests do not prove browser behavior, CSS/layout, routing, focus, rendering, canvas/graph behavior, or frontend/backend integration.

**Mandatory UI rule:**

> If the user can see it or interact with it, the changed path must be exercised in a real browser before completion.

### Authenticated Frontend Fixture Rule

When a frontend/browser test requires an authenticated user, establish authentication with an isolated disposable test identity created through the application's real test persistence/repository path. Use deterministic temporary username/password credentials and then exercise the real login UI or real application auth path.

Preferred path:

```text
real test DB/repository -> temporary user -> username/password login -> real app -> affected UI path
```

Do not use QR-code login, device pairing, SMS/email OTP, OAuth approval, or another human/external interactive login mechanism merely to establish an authenticated test fixture. Those flows add nondeterministic external dependencies unrelated to the behavior under test.

Interactive authentication mechanisms are exercised only when that authentication mechanism itself is the behavior being tested.

Fixture requirements:
- prefer the application's real repository/service or supported test fixture path over raw SQL so password hashing, identity invariants, tenant/org binding, and required side effects remain real
- raw database setup is acceptable only when it faithfully creates the same persisted state and the repository/service path is unavailable or materially inappropriate
- credentials must exist only in the test environment, be unique/disposable, and be cleaned up by fixture lifecycle or isolated in disposable test persistence
- do not reuse developer, staging, production, or long-lived shared credentials
- after fixture creation, authentication verification still follows the browser evidence lane below

### Browser Selection and Lifecycle

Follow [remote-cdp-browser-lifecycle.md](remote-cdp-browser-lifecycle.md) for the required evidence lane, endpoint setup, process ownership, and cleanup.

Use the browser by evidence type:
- **BEHAVIOR:** use Lightpanda at `http://127.0.0.1:9223` for login interaction, clicks, typing, selection, navigation, DOM/state transitions, frontend/backend wiring, and other non-pixel behavior. If the Lightpanda endpoint is not running, start the installed Lightpanda CDP server according to the lifecycle contract and stop only the process the test owns.
- **RENDERING:** use remote Windows Chrome at `http://127.0.0.1:9222` for pixel/layout/CSS/canvas/WebGL/WebGPU/visual correctness and rendered screenshot evidence.
- **BOTH:** run both only when the acceptance criterion genuinely requires independent behavior and rendering evidence. Do not duplicate the same scenario in both engines merely for reassurance.

Only the selected lane's missing browser can block its gate.

### UI Evidence Rules

A UI test used as completion evidence must:
- load the real frontend application in the selected real browser engine
- navigate to the changed route or surface
- use the real changed in-repo frontend components
- perform the relevant user interaction when behavior is interactive
- use the real backend/integration path when that path is part of the feature
- assert a visible or interactive final outcome
- check browser console/runtime failures where practical
- capture screenshot, rendered DOM, accessibility tree, or equivalent evidence when useful
- use the test cycle selected by test-driven-development: fail-then-pass for new behavior/defects, adequate green-before/green-after coverage for behavior-preserving refactors

For visual changes, verify the rendered result in remote Chrome at the shared browser's natural viewport. Use an isolated Chrome/profile for exact synthetic viewport coverage when necessary. Testing only class names, props, tokens, or snapshots is insufficient.

For interactive changes that do not depend on rendered pixels, perform the actual interaction through Lightpanda: click, type, select, route transition, focus, keyboard navigation, DOM/state changes, and other supported browser behavior.

```text
✅ UI completion evidence
selected browser lane -> real app -> real route -> real component tree -> real interaction/render -> observable final state

❌ Not sufficient
jsdom -> mocked child components -> expect(className).toContain('active')
```

### UI Gate Function

```
IF production change affects frontend/UI:
  Create any required authenticated fixture through real test persistence.
  Use temporary username/password credentials unless auth itself is under test.

  Select the evidence lane:
    behavior  -> Lightpanda :9223
    rendering -> remote Chrome :9222
    both      -> only when acceptance requires both

  Start/connect and clean up according to remote-cdp-browser-lifecycle.
  Missing required selected browser → keep that gate unverified.

  Does the test load the real app?
    no → invalid UI completion evidence

  Does it exercise the changed visible/interactive path?
    no → add the user interaction/render verification

  Are changed in-repo UI components mocked?
    yes → invalid completion evidence

  Does coverage satisfy the selected behavior-change or preservation cycle?
    no → close that gap before claiming completion
```

## Tests Ship With the Implementation

Use the change-specific test cycle in [test-driven-development](SKILL.md): new behavior and bug fixes need a meaningful failure; behavior-preserving refactors need adequate passing coverage before and after. Architectural and frontend completion additionally require their affected real integration/browser gates.

Ship the tests the behavior needs and only those: trivial code and human prose earn none, and a test written solely to satisfy process costs maintenance forever.

## The Mutation Check

Before finishing, mentally mutate the production code; at least one test should fail for each realistic mutation:

- Wrong constant or argument
- Wrong branch handler
- Missing state change or side effect
- Empty or default return
- Missing validation for zero, empty, nil, unauthorized, or malformed input
- Internal production component disconnected or replaced with a stub
- Production DI/routing points to the wrong implementation
- UI route points to the wrong component
- Click/keyboard handler removed
- Rendered data missing despite backend success
- CSS/layout change makes the target invisible or unusable

A mutation nothing catches marks the behavior as unprotected — or the test as tautological.

## Quick Reference

| When you... | Do |
|-------------|-----|
| Write any test | Name the break it catches — a bug, not a decision |
| Build an expected value | Derive it by hand; never with the code under test |
| Test a script or document | Run it / pressure-test its consumer; never grep its text |
| Reach for a dependency test | Test your boundary contract, not their documented mechanics |
| Want to assert on a mocked element | Test the real component, or unmock it |
| Are about to mock a method | Learn its side effects; mock the slow/external level |
| Build a mock response | Mirror the real structure completely |
| Need cleanup only tests use | Put it in test utilities |
| Watch mock setup balloon | Switch to an integration test with real components |
| Finish architectural work | Run at least one real-component integration path |
| A required internal dependency is missing | Implement/install it; do not mock past it |
| Need an authenticated frontend fixture | Create a disposable user in real test persistence; login with temporary username/password |
| Auth flow itself is not under test | Do not use QR/device/OTP/OAuth merely to establish the fixture |
| Change frontend/UI behavior | Run a real-browser UI test |
| Verify browser behavior | Use Lightpanda `:9223` |
| Verify rendering/pixels | Use remote Chrome `:9222` |
| Need both browser lanes | Run both only when acceptance genuinely requires both |
| Finish a test file | Run the mutation check |

## Warning Signs

- Setup and assertion share the same object, guaranteeing equality
- The test can fail only through a panic, crash, or missing selector
- The test fails on every intentional change, never on accidental breakage
- Expected values are hidden behind loops, builders, or helpers
- The test greps source text, or asserts a removed symbol stays removed
- The test would still matter if only the framework remained
- The test exists for coverage, checking no side effect or outcome
- An assertion checks a `*-mock` test ID, or fails if you remove the mock
- A method is called only from test files
- Mock setup is more than half the test, or you can't explain why the mock is needed
- Mocking "just to be safe"
- An architectural component exists only as a mock in tests
- The integration test bypasses production DI, routing, repository, or service wiring
- A missing dependency was replaced by a fake so the plan could be marked complete
- Frontend work completed with no browser test
- UI evidence is only jsdom, snapshots, shallow rendering, mocked components, source inspection, or CSS class assertions
- Authenticated frontend setup depends on QR scanning, device pairing, OTP, OAuth approval, or long-lived shared credentials when authentication itself is not under test
- Behavior-only frontend work routed to Chrome merely because Lightpanda was not already running
- Rendering correctness claimed from Lightpanda behavior evidence
- The same browser scenario run in both engines without an acceptance or compatibility reason
- Required browser evidence claimed while its selected lane remained unavailable
- A browser installed merely to bypass the configured evidence-lane contract
