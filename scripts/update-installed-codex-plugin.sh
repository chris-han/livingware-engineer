#!/usr/bin/env bash
set -euo pipefail

marketplace_name="${1:-livingware-engineer}"
plugin_name="${2:-livingware-engineer}"

if ! command -v codex >/dev/null 2>&1; then
  echo "codex CLI not found in PATH" >&2
  exit 1
fi

codex plugin marketplace upgrade "$marketplace_name"
codex plugin add "$plugin_name@$marketplace_name"
codex plugin list --marketplace "$marketplace_name"

echo
printf 'Updated %s from marketplace %s without uninstalling it.
' "$plugin_name" "$marketplace_name"
echo "Start a new Codex thread/session to load the refreshed plugin contents."
