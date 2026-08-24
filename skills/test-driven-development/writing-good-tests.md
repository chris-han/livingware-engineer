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

  Did the integration test fail because wiring/implementation was incomplete?
    no  → prove the test can catch the missing/broken connection

  Does it now pass through production wiring?
    yes → integration gate satisfied
```

## Principle 4: Prove the UI in a Real Browser

Any frontend/UI change requires browser-level verification because DOM simulators and component tests do not prove browser behavior, CSS/layout, routing, focus, rendering, canvas/graph behavior, or frontend/backend integration.

**Mandatory UI rule:**

> If the user can see it or interact with it, the changed path must be exercised in a real browser before completion.

### Prefer Windows-host Chrome on Port 9222 for WSL

The normal coding environment may be WSL with no Linux Chrome installed. In that environment, prefer the developer's Windows-host Chrome through CDP rather than installing a separate browser inside WSL.

Preferred endpoint:

```text
http://127.0.0.1:9222
```

Browser priority:

```text
1. Windows-host Chrome via CDP at 127.0.0.1:9222
2. project-standard real-browser runner already provided by the project
3. fresh local browser only if one is actually installed in the coding environment
```

### When `9222` is unavailable

Probe first:

```bash
curl -fsS http://127.0.0.1:9222/json/version
```

If the probe fails, **do not silently fall back to mock-only UI evidence and do not mark the frontend complete**. Remind the user that Windows Chrome must be started with remote debugging enabled.

Provide these instructions:

```powershell
Start-Process "$env:ProgramFiles\Google\Chrome\Application\chrome.exe" `
  -ArgumentList '--remote-debugging-port=9222', "--user-data-dir=$env:TEMP\livingware-chrome-debug"
```

If Chrome is under the x86 Program Files directory:

```powershell
Start-Process "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe" `
  -ArgumentList '--remote-debugging-port=9222', "--user-data-dir=$env:TEMP\livingware-chrome-debug"
```

Command Prompt equivalent when Chrome is on `PATH`:

```cmd
start chrome --remote-debugging-port=9222 --user-data-dir="%TEMP%\livingware-chrome-debug"
```

Explain that the separate `--user-data-dir` is required for modern Chrome remote debugging and intentionally isolates the debug browser from the user's normal profile.

After the user starts Chrome, retry the WSL probe. If Windows Chrome is running but WSL still cannot reach `127.0.0.1:9222`, report a WSL/Windows host-network reachability issue. Do not install Chrome inside WSL merely to bypass this configured test prerequisite.

### UI Evidence Rules

A UI test used as completion evidence must:
- load the real frontend application in a real browser engine
- navigate to the changed route or surface
- use the real changed in-repo frontend components
- perform the relevant user interaction when behavior is interactive
- use the real backend/integration path when that path is part of the feature
- assert a visible or interactive final outcome
- check browser console/runtime failures where practical
- capture screenshot, rendered DOM, accessibility tree, or equivalent evidence when useful
- prove it can fail on incomplete UI behavior or wiring, then pass after the implementation

For visual changes, verify the rendered result at the relevant viewport(s). Testing only class names, props, tokens, or snapshots is insufficient.

For interactive changes, perform the actual interaction: click, type, select, drag, focus, keyboard navigation, route transition, graph/canvas action, etc.

```text
✅ UI completion evidence
Windows Chrome via CDP -> real app -> real route -> real component tree -> real interaction -> visible final state

❌ Not sufficient
jsdom -> mocked child components -> expect(className).toContain('active')
```

### UI Gate Function

```
IF production change affects frontend/UI:
  Is Windows Chrome on 127.0.0.1:9222 reachable from WSL?
    yes → attach and run browser verification
    no  → instruct user to start Windows Chrome in debug mode
          and keep completion BLOCKED

  Does the test load the real app?
    no → invalid UI completion evidence

  Does it exercise the changed visible/interactive path?
    no → add the user interaction/render verification

  Are changed in-repo UI components mocked?
    yes → invalid completion evidence

  Did the browser test prove the broken/incomplete behavior can fail?
    no → strengthen it before claiming completion
```

## Tests Ship With the Implementation

The TDD cycle — failing test, minimal implementation, refactor — is what local behavioral correctness means. Architectural completeness requires the integration gate in addition to local TDD. Frontend completeness additionally requires the real-browser gate.

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
| Change frontend/UI behavior | Run a real-browser UI test |
| Windows Chrome reachable at `9222` | Attach to it from WSL |
| `9222` unavailable in WSL | Instruct the user to start Windows Chrome in debug mode; keep completion blocked |
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
- WSL frontend work marked complete while Windows Chrome `9222` remained unavailable
- A Linux browser was installed solely to bypass the configured Windows-host Chrome prerequisite
