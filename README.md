# Livingware Engineer

Livingware Engineer is an agentic software-engineering methodology and composable skills framework for coding agents. It is derived from [Superpowers](https://github.com/obra/superpowers) and intentionally keeps many upstream skill IDs and internal compatibility surfaces so upstream improvements remain mergeable.

Livingware Engineer extends the upstream methodology toward governed implementation: explicit prerequisites, dependency readiness, real-component integration verification, architecture/spec conformance, evidence-backed completion, and Minimum Viable Loop (MVL) product learning.

## Installation

Install this repository when you want **Livingware Engineer** rather than the upstream `superpowers` package:

```text
https://github.com/chris-han/livingware-engineer.git
```

### Claude Code

Register this repository as its own marketplace:

```bash
/plugin marketplace add chris-han/livingware-engineer
```

Install the plugin:

```bash
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

Install directly from this repository:

```text
/plugins install https://github.com/chris-han/livingware-engineer.git
```

Detailed docs: [docs/README.kimi.md](docs/README.kimi.md)

### OpenCode

Tell OpenCode:

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

## Basic Workflow

MVL is not a separate skill. For product features, it is the **unit of work carried across the existing workflow**.

1. **brainstorming / design** — define the target user, job-to-be-done, value hypothesis, and smallest real user journey.
2. **using-git-worktrees** — create an isolated workspace and establish a clean baseline.
3. **writing-plans** — compile the approved design into an implementation plan that carries the same MVL contract: realistic trial inputs, technical/UX metrics, feedback capture, improvement levers, re-test surface, stopping criterion, and integration contract.
4. **subagent-driven-development** or **executing-plans** — implement bounded tasks without redefining the feature unit locally.
5. **test-driven-development** — enforce RED → GREEN → REFACTOR for local behavior derived from the planned journey.
6. **real-component integration verification** — prove the same smallest real journey through changed in-repo production components; internal completion-path mocks are forbidden.
7. **real-browser UI verification** — mandatory for frontend work; prefer Chrome CDP on port `9222`, and in WSL require the Windows-host Chrome prerequisite rather than silently downgrading to mock-only UI tests.
8. **vertical / end-to-end verification** — execute the feature's smallest real user journey through the real application path when it crosses architecture boundaries.
9. **technical + UX measurement / feedback / improvement / re-test** — use the same journey and realistic inputs to generate comparable product-learning evidence.
10. **requesting-code-review** — verify spec compliance and code quality.
11. **verification-before-completion** — distinguish task completion, implementation completion, and MVL/feature completion using fresh evidence.
12. **finishing-a-development-branch** — close the implementation lifecycle cleanly.

## MVL as the Cross-Cutting Feature Contract

For a product feature, every phase must preserve one contract:

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
Plan + implementation tasks
              |
              v
TDD behavior evidence
              |
              v
Real-component integration
              |
              v
Real-browser / vertical E2E evidence
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

The feature unit must not fragment as work moves between agents or phases. A task may implement only one component, but it does not get to invent a different user path, success criterion, fixture semantics, or integration story just to make its local tests pass.

Every product implementation plan therefore carries an **MVL Contract** with:

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

The same plan also carries an **Integration Contract** that names:

- real in-repo components required on the completion path
- true external/nondeterministic boundaries that may be substituted
- internal components forbidden from being mocked as completion evidence
- real-browser requirement and preferred Chrome CDP endpoint when frontend work is involved

For maintenance work with no product-learning loop, the plan may state `MVL: not applicable — <reason>` rather than inventing one.

## Livingware Extension Principle

TDD alone proves local behavior; it does not prove that the designed system actually exists. Livingware Engineer therefore treats testing as layered evidence inside the MVL:

```text
Task TDD
  RED -> GREEN -> REFACTOR
       |
       v
Real-component integration
  same planned user journey
  real internal dependencies
       |
       v
Real-browser UI test (when frontend)
  same planned user journey
  real rendered interaction
       |
       v
Vertical / end-to-end slice
  production wiring
       |
       v
Credible working prototype
       |
       v
Try -> Measure -> Feedback -> Diagnose -> Improve -> Re-test
```

An architectural task should not be considered complete merely because mocked unit tests pass. Each changed or newly relied-upon in-repo production component should participate in at least one integration path using its real implementation.

A product feature should not be considered complete merely because its implementation passes all technical gates.

```text
Task complete
  = local deliverable + local evidence

Implementation complete
  = TDD + real integration + real browser when UI + vertical/E2E when needed

MVL / feature complete
  = implementation credibility
  + technical measurement
  + UX measurement
  + feedback
  + required evidence-driven improvement
  + comparable re-test
```

For knowledge- or data-backed features, the supporting asset belongs inside the same learning loop rather than being treated as unrelated infrastructure:

```text
Ground/acquire source
  -> Build/update knowledge or data asset
  -> Run feature
  -> Human/user review
  -> Evaluate feature + asset
  -> Correct asset/model/code/UX
  -> Re-run
```

The objective is the smallest loop that produces reliable product learning, while preserving architectural boundaries needed to avoid an obvious dead end.

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

The cross-cutting **Minimum Viable Loop (MVL)** feature-unit methodology is adapted from the Semantier `mvl-feature-development` approach, but in Livingware Engineer it is intentionally embedded across planning, implementation, integration, browser/E2E verification, measurement, feedback, and re-test rather than exposed as a separate optional skill.

Livingware-specific changes and distribution are maintained in this repository.

## License

MIT License — see [LICENSE](LICENSE).
