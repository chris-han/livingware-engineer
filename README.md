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

1. **brainstorming** — refine requirements and design before coding.
2. **mvl-feature-development** — define the smallest learnable user journey, technical/UX metrics, baseline, feedback mechanism, improvement levers, and re-test criterion.
3. **using-git-worktrees** — create an isolated workspace and establish a clean baseline.
4. **writing-plans** — compile the approved design and MVL contract into executable implementation tasks.
5. **subagent-driven-development** or **executing-plans** — implement bounded tasks with review checkpoints.
6. **test-driven-development** — enforce RED → GREEN → REFACTOR for local behavior.
7. **real-component integration verification** — prove changed in-repo components are wired through their production implementations; mocks are allowed only at explicitly permitted external boundaries.
8. **real-browser UI verification** — mandatory for frontend work; prefer Chrome CDP on port `9222`, and in WSL require the Windows-host Chrome prerequisite rather than silently downgrading to mock-only UI tests.
9. **vertical / end-to-end verification** — prove the meaningful user-visible path when the change crosses architectural boundaries.
10. **MVL evaluation** — run the realistic trial, measure technical and UX outcomes, capture feedback, improve, and re-run the same evaluation surface.
11. **requesting-code-review** — verify spec compliance and code quality.
12. **verification-before-completion** — require current evidence before claiming completion.
13. **finishing-a-development-branch** — close the implementation lifecycle cleanly.

## Livingware Extension Principle

TDD alone proves local behavior; it does not prove that the designed system actually exists. Livingware Engineer therefore treats testing as layered evidence, and feature development as a learning loop above that evidence:

```text
Task TDD
  RED -> GREEN -> REFACTOR
       |
       v
Real-component integration
  real internal dependencies
       |
       v
Real-browser UI test (when frontend)
  real rendered interaction
       |
       v
Vertical / end-to-end slice
  production wiring
       |
       v
Architecture + spec closure
       |
       v
Credible working prototype
       |
       v
Try -> Measure -> Feedback -> Diagnose -> Improve -> Re-test
       |
       v
MVL-complete feature iteration
```

An architectural task should not be considered complete merely because mocked unit tests pass. Each changed or newly relied-upon in-repo production component should participate in at least one integration path using its real implementation.

A feature should not be considered complete merely because its implementation passes all technical gates. **Implementation completion and feature completion are different claims.** The `mvl-feature-development` skill requires a real target user journey, technical and UX evaluation, feedback capture, at least one explicit improvement, and a comparable re-test.

## Minimum Viable Loop (MVL)

Livingware Engineer includes `skills/mvl-feature-development/SKILL.md`, generalized from the Semantier MVL methodology.

Canonical loop:

```text
Prototype -> Try -> Measure -> Feedback -> Diagnose -> Improve -> Re-test
```

An MVL plan should identify:

- target user and job-to-be-done
- smallest working prototype journey
- realistic trial inputs
- technical success metrics
- UX success metrics
- baseline / initial benchmark
- feedback and telemetry capture
- improvement levers
- re-evaluation method
- stopping criterion

For knowledge- or data-backed features, the supporting asset belongs inside the learning loop rather than being treated as unrelated infrastructure:

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

The **Minimum Viable Loop (MVL)** feature-development layer is adapted from the Semantier `mvl-feature-development` methodology and generalized for use across product codebases.

Livingware-specific changes and distribution are maintained in this repository.

## License

MIT License — see [LICENSE](LICENSE).
