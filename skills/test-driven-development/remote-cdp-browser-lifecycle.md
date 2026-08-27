# Shared Chrome CDP Lifecycle

Use this contract when attaching automation to a developer-owned persistent Chrome, including Windows-host Chrome at `127.0.0.1:9222` from WSL.

## Preserve Shared Browser State

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

When `http://127.0.0.1:9222` is reachable from WSL, keep probing, diagnostics, automation, and cleanup in WSL/CDP. Do not invoke PowerShell merely because Chrome runs on Windows.

Only when the endpoint is unavailable should you ask the user to start the Windows debug instance with a host-side command. After it is reachable, return to the WSL/CDP path.

## Cleanup Evidence

Before completion, verify all of the following:

- the shared Chrome endpoint is still reachable;
- no device-metrics override from the fixture remains active;
- fixture-owned pages and CDP sessions are gone;
- the automation process has exited;
- operator-owned tabs remain open;
- the final evidence was captured at the natural viewport, or in a separately launched isolated browser when an exact viewport was required.
