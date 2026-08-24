# Livingware Engineer for OpenCode

Complete guide for using Livingware Engineer with [OpenCode.ai](https://opencode.ai).

## Installation

Add Livingware Engineer to the `plugin` array in your `opencode.json` (global or project-level):

```json
{
  "plugin": ["livingware-engineer@git+https://github.com/chris-han/livingware-engineer.git"]
}
```

Restart OpenCode. The plugin installs through OpenCode's plugin manager and registers all skills.

OpenCode uses its own plugin install. If you also use Claude Code, Codex, or another harness, install Livingware Engineer separately for each one.

## Upstream-compatible internals

The distribution identity is `livingware-engineer`, but some internal runtime files and skill IDs still contain `superpowers`, including `.opencode/plugins/superpowers.js` and `using-superpowers`. These are deliberately retained to reduce divergence from `obra/superpowers` and make upstream synchronization safer.

## Updating

OpenCode installs Livingware Engineer through a git-backed package spec. If a restart does not pick up the newest commit, clear OpenCode's package cache or reinstall the plugin.

To pin a specific branch or tag:

```json
{
  "plugin": ["livingware-engineer@git+https://github.com/chris-han/livingware-engineer.git#main"]
}
```

## Windows install fallback

If OpenCode cannot install the git-backed plugin directly, try system npm:

```powershell
npm install livingware-engineer@git+https://github.com/chris-han/livingware-engineer.git --prefix "$HOME\.config\opencode"
```

Then use the installed package path in `opencode.json`:

```json
{
  "plugin": ["~/.config/opencode/node_modules/livingware-engineer"]
}
```

## Usage

Use OpenCode's native `skill` tool to list or load skills:

```text
use skill tool to list skills
use skill tool to load brainstorming
```

## Getting Help

- Issues: https://github.com/chris-han/livingware-engineer/issues
- Repository: https://github.com/chris-han/livingware-engineer
- OpenCode docs: https://opencode.ai/docs/
