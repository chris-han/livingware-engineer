# Livingware Engineer for Kimi Code

Complete guide for using Livingware Engineer with [Kimi Code](https://github.com/MoonshotAI/kimi-code).

## Installation

Install this repository directly:

```text
/plugins install https://github.com/chris-han/livingware-engineer.git
```

For unreleased validation against `dev`, pin the branch explicitly:

```text
/plugins install https://github.com/chris-han/livingware-engineer/tree/dev
```

Kimi Code applies plugin changes to new sessions. After installing, updating, enabling, disabling, or reloading the plugin, start a fresh session with `/new`.

## How It Works

The Kimi plugin manifest lives at `.kimi-plugin/plugin.json` and identifies the distributed plugin as `livingware-engineer`.

The repository intentionally retains the upstream-compatible `using-superpowers` session-start skill and related internal skill terminology. Those names are implementation compatibility surfaces, not the distributed plugin identity.

The manifest:

1. Points Kimi Code at the existing `skills/` directory.
2. Loads `using-superpowers` at session start through `sessionStart.skill`.
3. Provides Kimi-specific tool mapping through `skillInstructions`.

## Updating

Use Kimi Code's plugin manager, or reinstall from the repository URL above. Start a fresh session with `/new` after updating.

## Troubleshooting

### Plugin not loading

1. Run `/plugins info livingware-engineer` and check diagnostics.
2. Make sure the plugin is enabled.
3. Start a fresh session with `/new` after install or update.

### Direct GitHub install used an old release

Kimi Code may resolve a bare repository URL to the latest GitHub release. To test unreleased changes, install the branch explicitly:

```text
/plugins install https://github.com/chris-han/livingware-engineer/tree/dev
```

### Skills not triggering

1. Confirm `/plugins info livingware-engineer` shows the plugin enabled.
2. Start a fresh session with `/new`.
3. Try the acceptance prompt: `Let's make a react todo list`. A working install should load `brainstorming` before writing code.
