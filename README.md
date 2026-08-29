# Livingware Engineer

Livingware Engineer is an agentic software-engineering methodology and composable skills framework for coding agents. It is derived from [Superpowers](https://github.com/obra/superpowers), while extending the upstream workflow around one idea:

> **Software is not a sequence of completed tasks. It is living infrastructure that must keep producing useful learning as requirements, users, dependencies, and architecture change.**

A good implementation therefore needs more than locally correct code. It must preserve a coherent feature journey, prove the real architecture exists, expose the real user experience, keep dependencies intentional, and leave behind evidence that tells the next iteration what to change.

Livingware Engineer is designed around six principles:

1. **MVL is the feature-development unit.** A product feature is developed as a Minimum Viable Loop: the smallest real user journey that can be built, tried, measured, improved, and re-tested. MVL is not a test unit; unit tests, integration tests, browser tests, and E2E tests are evidence inside the implementation of an MVL.
2. **Reuse before invention.** During brainstorming, explicitly decide whether to reuse code already in the repository, use the standard library or platform, use an installed dependency, adopt a mature open-source dependency, or build custom code. Prefer the lowest rung that genuinely satisfies the design while keeping product semantics and governing boundaries under local control.
3. **Dependencies are architecture, not setup trivia.** Any new dependency must be discussed during design, declared and pinned in the plan, installed as a prerequisite, and smoke/contract-tested before feature code depends on it.
4. **Test scope follows impact radius, not diff size.** Use `codebase-memory-mcp` when available to inspect callers, consumers, dependency edges, persistence, routes, trust boundaries, and user paths. Escalate from local TDD to focused integration, real-component integration, or vertical/E2E only when the observed production radius requires it.
5. **Mocks cannot prove architecture exists.** Changed in-repo production components that matter to the completion path must appear as their real implementations in at least one integration path. True external systems may be substituted at their explicit boundary.
6. **User-visible frontend work requires a real browser.** In the standard WSL workflow, prefer Windows-host Chrome through CDP on port `9222`. If Chrome is unavailable, the browser gate remains blocked until the user starts the debug instance; mock-only UI tests are not completion evidence.

The methodology keeps many upstream skill IDs and internal compatibility surfaces so Superpowers improvements can still be merged selectively.

## Why "Livingware"?

Traditional software processes tend to treat implementation as a terminal state: requirements become tasks, tasks become code, tests turn green, and the feature is declared done.

Livingware treats implementation as one state in a feedback system:

```text
Intent / hypothesis
        ↓
Smallest real user journey
        ↓
Design: reuse / adopt / build
        ↓
Dependency + environment readiness
        ↓
Implementation with TDD
        ↓
Impact-radius-driven verification
        ↓
Real integration / browser / E2E evidence as required
        ↓
Try with realistic inputs
        ↓
Technical + UX measurement
        ↓
Feedback / diagnosis
        ↓
Improve
        ↓
Comparable re-test
        └──────────────→ next iteration
```

The objective is not maximal process. It is the **smallest credible loop that produces reliable product learning without creating an architectural dead end**.

This is why Livingware distinguishes three different claims:

```text
Task complete
  = local deliverable + local evidence

Implementation complete
  = the required TDD / integration / browser / E2E evidence is green

MVL / feature complete
  = implementation credibility
  + technical measurement
  + UX measurement
  + feedback
  + required evidence-driven improvement
  + comparable re-test
```

## Installation

Install this repository when you want **Livingware Engineer** rather than the upstream `superpowers` package:

```text
https://github.com/chris-han/livingware-engineer.git
```

### Claude Code

Register this repository as its own marketplace:

```bash
/plugin marketplace add chris-han/livingware-engineer
/plugin install livingware-engineer@livingware-engineer
```

The Anthropic official `superpowers` marketplace entry is the upstream package, not Livingware Engineer.

### Antigravity

```bash
agy plugin install https://github.com/chris-han/livingware-engineer.git
```

### Codex App / Codex CLI

For a repository-based install, use this repository's `.codex-plugin/plugin.json` rather than the official `superpowers` marketplace package. The plugin identity is `livingware-engineer`.

### Cursor

Install the plugin from this repository when using repository/plugin development flows. The manifest at `.cursor-plugin/plugin.json` identifies the plugin as `livingware-engineer`.

### Devin CLI

```bash
devin plugins install chris-han/livingware-engineer
```

Update later with:

```bash
devin plugins update livingware-engineer
```

### Factory Droid

```bash
droid plugin marketplace add https://github.com/chris-han/livingware-engineer.git
droid plugin install livingware-engineer@livingware-engineer
```

### Gemini CLI

```bash
gemini extensions install https://github.com/chris-han/livingware-engineer.git
```

Update later with:

```bash
gemini extensions update livingware-engineer
```

### GitHub Copilot CLI

Register this repository rather than the upstream Superpowers marketplace:

```bash
copilot plugin marketplace add chris-han/livingware-engineer
copilot plugin install livingware-engineer@livingware-engineer
```

### Kimi Code

```text
/plugins install https://github.com/chris-han/livingware-engineer.git
```

Detailed docs: [docs/README.kimi.md](docs/README.kimi.md)

### OpenCode

```text
Fetch and follow instructions from https://raw.githubusercontent.com/chris-han/livingware-engineer/refs/heads/main/.opencode/INSTALL.md
```

Detailed docs: [docs/README.opencode.md](docs/README.opencode.md)

### Pi

```bash
pi install git:github.com/chris-han/livingware-engineer
```

The package intentionally continues loading the upstream-compatible internal extension path `.pi/extensions/superpowers.ts`.

### Hermes Agent

```bash
hermes plugins install chris-han/livingware-engineer --enable
```

Restart active Hermes sessions after installation.

## Frontend Design

Livingware Engineer includes a general `frontend-design` skill for product UI work. It composes the engineering workflow with a pinned upstream Impeccable skill for visual craft and anti-slop review. When a project already has a `DESIGN.md`, that project document remains the design authority: its visual language, information architecture, component conventions, and stated consistency objectives override generic design taste. A design-system replacement happens only when the task explicitly calls for one.

## Development Workflow

MVL is not a separate skill. For product features, it is the **feature-development unit carried through the existing workflow**.

1. **brainstorming / design** — define the target user, job-to-be-done, value hypothesis, and smallest real user journey. For each meaningful capability, explicitly discuss reuse vs open-source adoption vs custom implementation.
2. **dependency decision** — identify existing repo capabilities, standard-library/platform options, installed packages, OSS candidates, or justified custom code. Record important trade-offs such as fit, maintenance, license, security, lock-in, adapter cost, and whether the dependency actually shrinks the MVL.
3. **using-git-worktrees** — create an isolated workspace and establish a clean baseline.
4. **writing-plans** — compile the approved design into an implementation plan carrying the same MVL contract, dependency prerequisites, impact-radius evidence, integration contract, realistic trial inputs, metrics, feedback surface, re-test method, and stopping criterion.
5. **dependency readiness** — install/pin any new package or service prerequisite, exercise the real capability the feature needs, and run affected baseline tests before downstream tasks consume it.
6. **subagent-driven-development** or **executing-plans** — implement bounded tasks without redefining the feature locally.
7. **test-driven-development** — enforce RED → GREEN → REFACTOR for changed local behavior.
8. **impact-radius assessment** — use `codebase-memory-mcp` when available (`index_repository`, `search_graph`, `trace_path`, `query_graph`, `search_code`, `get_code_snippet`) to determine the smallest sufficient verification scope.
9. **focused / real-component integration verification** — when the observed impact radius crosses production seams, prove the affected path with real changed in-repo components and production wiring.
10. **real-browser UI verification** — mandatory when frontend behavior is affected; for WSL prefer Windows-host Chrome CDP on `127.0.0.1:9222`.
11. **vertical / end-to-end verification** — when the impact radius or MVL journey crosses architectural boundaries, execute the smallest real journey through the real application path.
12. **technical + UX measurement / feedback / improvement / re-test** — use the same journey and realistic inputs to generate comparable product-learning evidence.
13. **requesting-code-review** — verify specification compliance and code quality.
14. **verification-before-completion** — distinguish task completion, implementation completion, and feature/MVL completion using fresh evidence.
15. **finishing-a-development-branch** — close the implementation lifecycle cleanly.

## MVL: The Feature-Development Unit

For a product feature, every phase preserves one contract:

```text
Target user + JTBD + value hypothesis
              |
              v
Smallest real user journey
              |
              v
Realistic trial inputs
              |
              v
Reuse / adopt / build decision
              |
              v
Plan + dependency readiness
              |
              v
Implementation tasks + local TDD
              |
              v
Impact-radius-driven verification
              |
              v
Integration / browser / vertical E2E as required
              |
              v
Technical + UX measurement
              |
              v
Feedback -> Diagnose -> Improve
              |
              v
Comparable re-test
```

The feature must not fragment as work moves between skills or agents. A task may implement one component, but it does not get to invent a different user path, success criterion, fixture semantics, or integration story merely to make local tests pass.

A product implementation plan therefore carries an **MVL Contract** containing:

- target user and job-to-be-done
- value hypothesis
- smallest real user journey
- realistic trial inputs
- technical success metrics
- UX success metrics
- feedback and telemetry capture
- improvement levers
- re-evaluation surface
- stopping criterion

For maintenance work with no product-learning loop, the plan may state `MVL: not applicable — <reason>` instead of inventing one.

## Reuse Before Build

Livingware incorporates the practical idea behind Ponytail's dependency ladder: **stop at the first rung that genuinely holds**.

```text
1. Do not build the capability if it is unnecessary
2. Reuse code already in the repository
3. Use the standard library or native platform
4. Use an already-installed dependency
5. Adopt a suitable open-source dependency
6. Write the minimum custom code only when the earlier rungs fail
```

This is a brainstorming/design decision, not an implementation shortcut.

When evaluating a new open-source dependency, consider:

- fit to the smallest real user journey
- maturity and maintenance activity
- API stability and upgrade cost
- license compatibility
- security and supply-chain exposure
- transitive dependency weight
- runtime/platform compatibility
- performance and operational footprint
- adapter complexity
- vendor/project lock-in
- whether it removes more complexity than it introduces

Keep locally owned code around product semantics, authority, governance, trust, policy, and irreversible boundaries even when OSS supplies lower-level mechanics.

## Dependencies Are Explicit Prerequisites

A new dependency is not ready merely because it appears in a manifest or lockfile.

Plans should make dependency readiness explicit:

```text
select dependency
  -> pin / declare
  -> install / sync
  -> run smoke or contract test against the real API needed by the feature
  -> run affected baseline tests
  -> only then allow feature code to consume it
```

The plan should record the package/service name, version or commit pin, declaration file, install command, configuration, compatibility constraints, verification command, and cleanup/replacement implications.

Dependency verification answers:

> Can this dependency actually provide the capability the design assumes in this environment?

It is separate from integration testing, which asks whether our own production components work together correctly.

## Impact-Radius-Driven Testing

Livingware deliberately avoids the rule:

```text
any code change -> all integration tests -> full E2E
```

Instead:

```text
changed production surface
      ↓
codebase-memory-mcp impact analysis
      ↓
affected seams / consumers / user paths
      ↓
smallest sufficient verification
```

When `codebase-memory-mcp` is available, index the repository if needed and use graph-oriented discovery such as `search_graph`, `trace_path`, `query_graph`, `search_code`, and `get_code_snippet`.

Suggested impact classes:

```text
R0 — local behavior only
     -> focused TDD / unit-level behavior test

R1 — one production seam
     -> focused integration across that seam

R2 — multi-component production path
     -> real-component integration

R3 — user journey / cross-process / UI path
     -> vertical/E2E + real-browser verification when UI is involved
```

These are test-scope classes, not feature units. **MVL remains the feature-development unit.**

See [skills/test-driven-development/impact-radius-testing.md](skills/test-driven-development/impact-radius-testing.md).

## Real-Component Integration

TDD proves local behavior; it does not prove the production architecture actually exists.

When impact radius requires integration, changed or newly relied-upon in-repo production components on the completion path should participate through their real implementations.

```text
GOOD
real route
  -> real service
  -> real evaluator
  -> real repository
  -> real test persistence

NOT COMPLETION EVIDENCE
real route
  -> MockService
  -> expected response
```

Mocks, fakes, and stubs remain appropriate at true external or nondeterministic boundaries. When substituting an external service, keep the in-repo adapter/client real and substitute the remote side where possible.

## Real-Browser Frontend Verification

Any frontend/UI change requires browser-level verification because DOM simulators and component tests cannot prove the actual rendering, CSS/layout, focus, routing, canvas/graph behavior, or frontend/backend interaction.

For the standard WSL development environment, prefer Windows-host Chrome over CDP:

```text
http://127.0.0.1:9222
```

Treat a persistent CDP browser as shared operator state. Use a fixture-owned page, preserve the natural viewport and existing tabs, and clean up device-metrics overrides, CDP sessions, owned pages, and the automation client in `finally`. Exact synthetic viewports require an isolated browser/profile.

If DOM geometry and the screenshot disagree, inspect protocol layout metrics, screenshot dimensions, site zoom, CDP targets, and stale automation clients before changing CSS. When `9222` is reachable from WSL, keep this work in WSL/CDP; PowerShell is only a launch instruction for an unavailable endpoint. The full contract is in [Shared Chrome CDP Lifecycle](skills/test-driven-development/remote-cdp-browser-lifecycle.md).

If it is unavailable, frontend completion remains blocked. The user should start a separate Windows Chrome debug profile rather than the agent installing a substitute browser inside WSL or downgrading to jsdom/mock-only evidence.

Recommended PowerShell command:

```powershell
Start-Process "$env:ProgramFiles\Google\Chrome\Application\chrome.exe" `
  -ArgumentList '--remote-debugging-port=9222', "--user-data-dir=$env:TEMP\livingware-chrome-debug"
```

Then verify from WSL:

```bash
curl -fsS http://127.0.0.1:9222/json/version
```

## Knowledge- and Data-Backed Features

When feature performance materially depends on a knowledge or data asset, that asset belongs inside the same MVL rather than being treated as unrelated infrastructure.

```text
Ground/acquire source
  -> Build/update knowledge or data asset
  -> Run feature
  -> Human/user review
  -> Evaluate feature + asset
  -> Correct asset/model/code/UX
  -> Re-run
```

The supporting asset does not need to be perfect before the user can try the feature. It needs to be inspectable and correctable enough to support reliable learning.

## What Livingware Optimizes For

Livingware Engineer is intentionally opinionated about several trade-offs:

- **Learning speed over premature completeness** — build the smallest credible loop that can produce an aha moment and measurable evidence.
- **Real architecture over mocked confidence** — use mocks where they isolate true external uncertainty, not where they hide missing internal implementation.
- **Targeted evidence over ritual testing** — use impact radius to choose the narrowest test surface that proves the changed production behavior.
- **Reuse over reinvention** — prefer existing code, platform capabilities, and mature OSS when they simplify the feature without surrendering product semantics or governing boundaries.
- **Explicit prerequisites over hidden setup** — dependencies and environment assumptions belong in the plan and must be proven before downstream work relies on them.
- **Continuity over task fragmentation** — preserve one user journey and one feature contract across design, planning, implementation, integration, evaluation, and re-test.
- **Evidence over completion language** — no success claim outruns the evidence actually collected.

## Upstream Compatibility

Livingware Engineer remains a GitHub fork of `obra/superpowers`. Renaming the repository and plugin does not remove fork ancestry or prevent upstream synchronization.

Recommended remotes for a local clone:

```bash
git remote set-url origin https://github.com/chris-han/livingware-engineer.git
git remote add upstream https://github.com/obra/superpowers.git
```

If `upstream` already exists:

```bash
git remote set-url upstream https://github.com/obra/superpowers.git
```

To review upstream changes:

```bash
git fetch upstream
git log --oneline main..upstream/main
```

Then merge or selectively adapt upstream changes rather than blindly overwriting Livingware-specific behavior.

## Compatibility Naming

Some internal names still contain `superpowers`, including the `using-superpowers` skill and some runtime filenames. These are intentionally retained for upstream compatibility. They are implementation details; the distributed plugin/package identity is **Livingware Engineer**.

## Provenance

Livingware Engineer is derived from **Superpowers**, created by Jesse Vincent / Prime Radiant. The upstream project is available at `obra/superpowers`.

Livingware-specific additions include the cross-cutting MVL feature-development contract, dependency readiness and build-vs-adopt decisions, impact-radius-driven test selection, real-component integration requirements, and real-browser frontend verification.

The MVL feature-development approach was adapted from the Semantier development methodology and embedded across the existing lifecycle rather than exposed as a separate optional skill.

The reuse-before-build discussion is influenced by Ponytail's dependency ladder and generalized here as a design-phase decision framework.

Livingware-specific changes and distribution are maintained in this repository.

## License

MIT License — see [LICENSE](LICENSE).
