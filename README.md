# Livingware Engineer

Livingware Engineer is an agentic software-engineering methodology and composable skills framework for coding agents. It is derived from [Superpowers](https://github.com/obra/superpowers) and intentionally keeps many upstream skill IDs and internal compatibility surfaces so upstream improvements remain mergeable.

Livingware Engineer extends the upstream methodology toward governed implementation: explicit prerequisites, dependency readiness, real-component integration verification, architecture/spec conformance, and evidence-backed completion.

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
2. **using-git-worktrees** — create an isolated workspace and establish a clean baseline.
3. **writing-plans** — compile the approved design into executable implementation tasks.
4. **subagent-driven-development** or **executing-plans** — implement bounded tasks with review checkpoints.
5. **test-driven-development** — enforce RED → GREEN → REFACTOR for local behavior.
6. **real-component integration verification** — prove changed in-repo components are wired through their production implementations; mocks are allowed only at explicitly permitted external boundaries.
7. **requesting-code-review** — verify spec compliance and code quality.
8. **verification-before-completion** — require current evidence before claiming completion.
9. **finishing-a-development-branch** — close the implementation lifecycle cleanly.

## Livingware Extension Principle

TDD alone proves local behavior; it does not prove that the designed system actually exists. Livingware Engineer therefore treats testing as layered evidence:

```text
Task TDD
  RED -> GREEN -> REFACTOR
       |
       v
Real-component integration
  real internal dependencies
       |
       v
Vertical / end-to-end slice
  production wiring
       |
       v
Architecture + spec closure
       |
       v
Evidence-backed completion
```

An architectural task should not be considered complete merely because mocked unit tests pass. Each changed or newly relied-upon in-repo production component should participate in at least one integration path using its real implementation.

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

Then merge or selectively adapt upstream changes rather than blindly overwriting Livingware-specific governance behavior.

## Compatibility Naming

Some internal names still contain `superpowers`, including the `using-superpowers` skill and some runtime filenames. These are intentionally retained for upstream compatibility. They are implementation details; the distributed plugin/package identity is **Livingware Engineer**.

## Provenance

Livingware Engineer is derived from **Superpowers**, created by Jesse Vincent / Prime Radiant. The upstream project is available at `obra/superpowers`. Livingware-specific changes and distribution are maintained in this repository.

## License

MIT License — see [LICENSE](LICENSE).
