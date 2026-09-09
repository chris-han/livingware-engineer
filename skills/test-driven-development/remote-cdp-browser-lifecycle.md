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
