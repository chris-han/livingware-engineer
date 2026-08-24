# Installing Livingware Engineer for OpenCode

## Prerequisites

- [OpenCode.ai](https://opencode.ai) installed

## Installation

Add Livingware Engineer to the `plugin` array in your `opencode.json` (global or project-level):

```json
{
  "plugin": ["livingware-engineer@git+https://github.com/chris-han/livingware-engineer.git"]
}
```

Restart OpenCode. The plugin installs through OpenCode's plugin manager and registers all skills.

## Compatibility note

The distributed package is `livingware-engineer`. Some internal filenames and skill IDs still contain `superpowers` to preserve compatibility with the upstream `obra/superpowers` codebase. Do not treat those internal names as installation coordinates.

## Usage

Use OpenCode's native `skill` tool:

```text
use skill tool to list skills
use skill tool to load brainstorming
```

## Updating

If a restart does not pick up the newest commit, clear OpenCode's package cache or reinstall the plugin. To pin a branch or tag:

```json
{
  "plugin": ["livingware-engineer@git+https://github.com/chris-han/livingware-engineer.git#main"]
}
```

## Windows install fallback

```powershell
npm install livingware-engineer@git+https://github.com/chris-han/livingware-engineer.git --prefix "$HOME\.config\opencode"
```

Then use:

```json
{
  "plugin": ["~/.config/opencode/node_modules/livingware-engineer"]
}
```

## Getting Help

- Issues: https://github.com/chris-han/livingware-engineer/issues
- Full documentation: https://github.com/chris-han/livingware-engineer/blob/main/docs/README.opencode.md
