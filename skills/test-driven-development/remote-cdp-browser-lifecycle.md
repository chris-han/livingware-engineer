# Browser Evidence Selection and Lifecycle

Use this contract for real-browser verification. Resolve the target product surface, delivery phase, project-owned runner/browser configuration, execution host and required evidence first; do not infer them from available tools, output format or developer OS.

## Campaign timing and token budget

Follow [goal-level E2E, task-level focused verification](../../docs/verification-impact-analysis-v1.md#goal-level-e2e-task-level-focused-verification). Run the consolidated UI campaign after all implementation tasks are integration-ready, not after each task. Earlier browser use is a bounded diagnostic for a named unresolved risk or an explicit requirement, not routine full acceptance.

Start acceptance from the actual UI. Batch deterministic actions/assertions in the existing CDP/Playwright runner; use the LLM for test design and exceptions, not every click. Read targeted DOM/accessible state and necessary network fields. Keep raw traces locally; return the scoped verdict and failing assertion, using the policy's default 20-line summary/80-line diagnostic budgets. Expand only relevant excerpts. Capture screenshots for failures or required visual assertions/key checkpoints, not every interaction. Bound actions, timeouts and retries; never weaken assertions or silently retry to green.

Reuse the same controlled CDP connection where safe, but keep account/profile/session isolation and real authentication. Do not copy cookies or credentials to save setup cost. A required native Electron journey must use the actual native application; Lightpanda, Chrome or an embedded billing webview cannot stand in for another application's required Settings/Composer journey. Explicit acceptance targets take precedence over the generic engine defaults below.

## Select evidence, product surface and environment

- **BEHAVIOR:** exercise the real affected UI, state transitions and backend wiring through the project's configured qualified browser/runner (normally an owned headless browser). A non-rendering engine is eligible only if its required DOM/API behavior is actually supported.
- **RENDERING:** use a qualified real rendering browser with the needed CSS, font, screenshot, canvas or GPU capabilities. This does not imply a different host or another browser run when the same engine can establish both claims.
- **NATIVE APPLICATION:** desktop/mobile-native behavior requires the actual native application at the environment named by the project acceptance. A browser or an embedded webview is not proof of the host app's native shell, installation, session integration or file-save behavior.
- **COMBINED:** use one journey to prove multiple behavior/rendering assertions when sufficient. Run distinct engines/hosts only for a specified compatibility, platform, graphics or native-app claim. Report unsupported capabilities, not invented PASS.

The project's AGENTS/spec/runner owns concrete browser executables, ports, startup commands, WSL/Windows/macOS host boundary and target application. Examples such as Lightpanda, Chrome or Electron are options, never global defaults. If absent, inspect the existing runner and choose the least intrusive compatible owned browser; do not install/start another engine merely because an example mentions it. A different product frontend or next-phase integration is not a fallback target.

## Process ownership and cleanup

Reuse a qualified project-controlled browser if safe; keep operator-owned windows, tabs, context, profile, viewport, zoom and listeners unchanged. Create a fixture-owned page/context, and close only fixture-owned resources in a finally block. Never kill processes by port/name. A fixture-started browser must record its process identity and stop only the process whose ownership the fixture can prove; a shared browser stays running.

For shared CDP, use its documented disconnect (not a potentially destructive close), verify ownership before cleanup, and isolate authentication/session state. Exact viewport tests use an isolated owned browser/profile; do not set a persistent device-metrics/window override on an operator-owned browser. Use finite timeouts, minimize repeated log polling and keep the tool process terminating on completion.

## Diagnose rendering versus capture

If geometry and screenshot disagree, compare in-page viewport/element bounds, protocol layout metrics, screenshot dimensions, device pixel ratio, zoom and stale automation clients **on the same target**. Change one variable at a time; terminate only owned clients. Do not jump from a mismatch to a new host or browser without a specific missing capability or reproduced failure.

## Execution-host boundary

Portable frontend development and test authoring remain on the project's declared development host. A remote browser/CDP endpoint does not make that browser's host the default execution host or authorize new Windows/native scratch directories. Cross-host execution requires an explicit target-platform acceptance claim or a capability that cannot be established on the selected host. Prefer project-scoped configuration for executable/endpoint details; do not encode local ports, paths or machine names in this shared skill.

## Optional QuickE2E Exploration and Test Authoring

Use an already-installed, project-qualified QuickE2E adapter when a new or changing user journey benefits from exploratory navigation or Playwright test generation. Direct Playwright/CDP authoring remains the default for known deterministic paths. QuickE2E is an optional external authoring tool, not a Livingware runtime dependency; do not install it, switch providers, or add a mandatory exploration gate merely to run existing tests.

Before exploration:

- Read the project's adapter README and qualification evidence. Bind the exact QuickE2E version, local bridge/provider configuration, application revision, and supported browser interactions. A disposable-form qualification does not qualify an authenticated product journey.
- Derive acceptance criteria and expected results from the JTBD/product contract and an independent oracle. Name the exact source, build, verification, answer, or equivalent domain identities the journey must preserve.
- Declare finite limits for actions, model calls, retries/repairs, elapsed time, and input/output tokens where observable. Enforce them in the runner/bridge; stop on exhaustion. If a required limit cannot be enforced, use direct deterministic authoring. Record unavailable usage or provider cost as UNKNOWN, never zero.
- Use the existing qualified local CLI/provider bridge when supplied by the project. Keep credentials out of prompts, exported code, traces, and committed artifacts. Establish disposable authentication through the real application fixture/login path in [writing-good-tests.md](writing-good-tests.md); browser-storage injection or API interception must not substitute for internal production wiring.

Run the bounded journey through exact accessible labels on real routes and real internal services. Use the adapter's actually qualified engine on a fixture-owned page and the project-selected execution host. Preserve shared-browser ownership and cleanup; use an isolated profile for synthetic viewport coverage. Do not assume that different CDP engines support identical interactions.

Export a successful journey to Playwright, then review it as authored code:

1. Replace brittle selectors and incidental waits with stable accessible locators and observable state transitions.
2. Strengthen assertions against independent expected outcomes and exact domain identities. Reaching a success screen does not prove arithmetic, authorization, persistence, ontology/evidence binding, or tenant isolation.
3. Reject hidden login shortcuts, internal-service mocks, API interception, model-derived expected values, swallowed failures, and silent assertion weakening or self-healing.
4. Replay the reviewed test in a fresh authenticated context with the model bridge stopped or inaccessible to the replay process. Keep required dataset/version identities fixed; explicitly reconstruct disposable fixtures where needed. A replay requiring model calls is not deterministic acceptance evidence.

Do not stop an operator-owned bridge just to prove model-free replay; isolate the replay's model access instead. Confirm the replay performs no model calls and use its actual assertions to determine which acceptance requirements it proves.

Exploration failure, an unsupported interaction, or budget exhaustion is a handoff to direct Playwright/CDP authoring for the affected path, not permission to weaken acceptance or silently change browser lanes. Preserve the specific failure and only the useful exported artifacts at their existing project owner; do not create a parallel evidence ledger.

QuickE2E exploration does not replace required affected behavior/rendering/native-app checks or independently authored negative/security/arithmetic/concurrency tests. Keep missing lanes and unexercised assertions explicitly unverified. Avoid duplicate exploration/replay when adequate unchanged tests already cover the contract.

Record exploration failures, actions, retries, model calls, observed input/output tokens, elapsed time, provider cost or UNKNOWN, and exported/replayed artifact identities in the existing test evidence. Separate exploration cost from replay cost. Do not claim faster authoring, lower cost, improved agent behavior, or human benefit without comparable observed evidence.

## Cleanup Evidence

At completion, record which browser/engine and application were actually used, the selected host and why it was required, whether operator-owned browser state remained intact, and whether only fixture-owned processes/pages/CDP sessions were retired. Do not manufacture separate per-engine evidence lanes, duplicate journeys or new logs when existing runner receipts suffice.
