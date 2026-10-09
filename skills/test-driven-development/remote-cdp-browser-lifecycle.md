# Browser CDP Lifecycle: Lightpanda and Shared Chrome

Use this contract for real-browser verification from WSL. Select the browser by the evidence the test must prove rather than treating every frontend test as a Chrome test.

## Select the Browser by Evidence

- **BEHAVIOR tests** — interaction, navigation, frontend state, DOM-visible results, application wiring, and browser-executed JavaScript — use Lightpanda at `http://127.0.0.1:9223` by default.
- **RENDERING tests** — visual appearance, layout, paint, fonts, screenshots, canvas/WebGL/WebGPU output, or Chromium-specific rendering behavior — use Windows-host Chrome at `http://127.0.0.1:9222`.
- Run the affected browser tests only, unless project instructions require a broader surface.
- Do not run the same scenario in both browsers unless the acceptance criterion actually requires both behavioral and rendering evidence, or a browser-specific compatibility question is under investigation.
- Never use Chrome merely because Lightpanda is not already running. Start Lightpanda when the behavior lane needs it.

## Lightpanda Behavior Lifecycle

Probe the designated Lightpanda endpoint first:

```bash
curl -fsS http://127.0.0.1:9223/json/version
```

If it is unavailable and the `lightpanda` binary is installed, start the CDP server instead of asking the user to remember the browser prerequisite:

```bash
lightpanda serve --host 127.0.0.1 --port 9223
```

Automation or a fixture may background that command, record its PID, wait until `/json/version` responds, and then run the test. Ownership is strict:

- If Lightpanda was already reachable, treat it as developer-owned and do not stop it.
- If the test fixture started Lightpanda, stop only that recorded process during unconditional cleanup.
- Do not kill Lightpanda by name or port; terminate only the process whose ownership the fixture can prove.
- If the binary is unavailable, report the missing behavior-test prerequisite. Do not silently substitute Windows Chrome as a generic behavior fallback.

Lightpanda is headless and has no graphical rendering surface. Passing behavior tests therefore does not constitute rendering evidence.

## Preserve Shared Chrome State

Windows Chrome on `127.0.0.1:9222` is the rendering lane and is persistent operator-owned state.

- Treat the existing browser, contexts, windows, tabs, zoom, and natural viewport as operator-owned state.
- Create a dedicated fixture-owned page for the test. Never reuse the first existing page merely because it is convenient.
- Do not call `page.setViewportSize`, `Emulation.setDeviceMetricsOverride`, `Browser.setWindowBounds`, or an equivalent persistent display override on the shared browser.
- If the acceptance criterion requires an exact synthetic viewport, launch an isolated browser/profile instead of attaching to the persistent endpoint.
- Close only pages created by the fixture. Never close an existing context, window, tab, or the shared browser.
- Put cleanup in `finally`: clear any device-metrics override created by the fixture, detach CDP sessions, close fixture-owned pages, and disconnect the automation transport.
- Do not assume a library's `close()` means “disconnect.” Use its documented disconnect operation; if semantics are ambiguous, let the harness end the client connection after explicit page/session cleanup and confirm Chrome remains reachable.
- Give scripts finite timeouts and ensure their Node/Playwright/Puppeteer process exits. A stale client can keep emulation state active after the test appears finished.

## Diagnose Layout Versus Capture State

When DOM geometry is correct but the screenshot is not, do not guess at CSS.

1. Capture in-page values such as `innerWidth`, `outerWidth`, `devicePixelRatio`, `visualViewport.width`, and document/body bounding rectangles.
2. Capture protocol-level `Page.getLayoutMetrics` from the same target.
3. Record the screenshot's actual pixel dimensions and compare it with the CSS and visual viewport.
4. List CDP targets and automation processes. Identify stale Node, Playwright, Puppeteer, or browser-inspection clients before terminating only the proven owner.
5. Check persistent per-origin site zoom and browser zoom state.
6. Change one variable at a time, then rerun the same measurements and screenshot.

Equality between a document's right edge and `innerWidth` proves only that the application fills the current CSS viewport. It does not prove that the CSS viewport matches the natural window, the visual viewport, or the screenshot surface.

## WSL Host Boundary

Keep Lightpanda behavior testing and Chrome rendering diagnostics in WSL/CDP while their designated endpoints are reachable. Do not invoke PowerShell merely because the rendering browser runs on Windows.

Only when a RENDERING test actually requires Windows Chrome and `http://127.0.0.1:9222` is unavailable should you ask the user to start the Windows debug instance with a host-side command. Chrome availability must not block a BEHAVIOR test that belongs on Lightpanda.

## Optional QuickE2E Exploration and Test Authoring

Use an already-installed, project-qualified QuickE2E adapter when a new or changing user journey benefits from exploratory navigation or Playwright test generation. Direct Playwright/CDP authoring remains the default for known deterministic paths. QuickE2E is an optional external authoring tool, not a Livingware runtime dependency; do not install it, switch providers, or add a mandatory exploration gate merely to run existing tests.

Before exploration:

- Read the project's adapter README and qualification evidence. Bind the exact QuickE2E version, local bridge/provider configuration, application revision, and supported browser interactions. A disposable-form qualification does not qualify an authenticated product journey.
- Derive acceptance criteria and expected results from the JTBD/product contract and an independent oracle. Name the exact source, build, verification, answer, or equivalent domain identities the journey must preserve.
- Declare finite limits for actions, model calls, retries/repairs, elapsed time, and input/output tokens where observable. Enforce them in the runner/bridge; stop on exhaustion. If a required limit cannot be enforced, use direct deterministic authoring. Record unavailable usage or provider cost as UNKNOWN, never zero.
- Use the existing qualified local CLI/provider bridge when supplied by the project. Keep credentials out of prompts, exported code, traces, and committed artifacts. Establish disposable authentication through the real application fixture/login path in [writing-good-tests.md](writing-good-tests.md); browser-storage injection or API interception must not substitute for internal production wiring.

Run the bounded journey through exact accessible labels on real routes and real internal services. For a Chrome-qualified adapter, use a fixture-owned page on Windows Chrome CDP while preserving all shared-browser ownership and cleanup rules above. Use an isolated browser/profile for exact synthetic viewport coverage. Do not assume QuickE2E supports Lightpanda merely because both expose CDP.

Export a successful journey to Playwright, then review it as authored code:

1. Replace brittle selectors and incidental waits with stable accessible locators and observable state transitions.
2. Strengthen assertions against independent expected outcomes and exact domain identities. Reaching a success screen does not prove arithmetic, authorization, persistence, ontology/evidence binding, or tenant isolation.
3. Reject hidden login shortcuts, internal-service mocks, API interception, model-derived expected values, swallowed failures, and silent assertion weakening or self-healing.
4. Replay the reviewed test in a fresh authenticated context with the model bridge stopped or inaccessible to the replay process. Keep required dataset/version identities fixed; explicitly reconstruct disposable fixtures where needed. A replay requiring model calls is not deterministic acceptance evidence.

Do not stop an operator-owned bridge just to prove model-free replay; isolate the replay's model access instead. Confirm the replay performs no model calls and use its actual assertions to determine which acceptance requirements it proves.

Exploration failure, an unsupported interaction, or budget exhaustion is a handoff to direct Playwright/CDP authoring for the affected path, not permission to weaken acceptance or silently change browser lanes. Preserve the specific failure and only the useful exported artifacts at their existing project owner; do not create a parallel evidence ledger.

QuickE2E Chrome exploration does not replace required Lightpanda BEHAVIOR acceptance, Chrome RENDERING checks, or independently authored negative/security/arithmetic/concurrency tests. Keep missing lanes and unexercised assertions explicitly unverified. Avoid duplicate exploration/replay when adequate unchanged tests already cover the contract.

Record exploration failures, actions, retries, model calls, observed input/output tokens, elapsed time, provider cost or UNKNOWN, and exported/replayed artifact identities in the existing test evidence. Separate exploration cost from replay cost. Do not claim faster authoring, lower cost, improved agent behavior, or human benefit without comparable observed evidence.

## Cleanup Evidence

Before completion, verify the lifecycle appropriate to the browser that was actually used.

For Lightpanda:

- the behavior test ran through `127.0.0.1:9223`;
- a pre-existing Lightpanda process was left running;
- or, if the fixture started Lightpanda, only that recorded process was stopped;
- the automation client exited cleanly.

For shared Chrome:

- the shared Chrome endpoint is still reachable;
- no device-metrics override from the fixture remains active;
- fixture-owned pages and CDP sessions are gone;
- the automation process has exited;
- operator-owned tabs remain open;
- the final rendering evidence was captured at the natural viewport, or in a separately launched isolated browser when an exact viewport was required.
