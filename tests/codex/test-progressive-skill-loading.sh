#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VERSION="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$ROOT/package.json")"
INSTALL_ROOT="${LIVINGWARE_INSTALL_ROOT:-$HOME/.codex/plugins/cache/livingware-engineer/livingware-engineer/$VERSION}"

fail() { echo "FAIL: $*" >&2; exit 1; }
pass() { echo "PASS: $*"; }
require_text() {
  local file="$1" text="$2" label="$3"
  grep -Fq "$text" "$file" || fail "$label — missing '$text' in $file"
  pass "$label"
}
reject_text() {
  local file="$1" text="$2" label="$3"
  if grep -Fq "$text" "$file"; then fail "$label — unexpected '$text' in $file"; fi
  pass "$label"
}

[[ -d "$INSTALL_ROOT" ]] || fail "installed Livingware $VERSION not found at $INSTALL_ROOT"
pass "installed Livingware $VERSION found"

ROUTER="$INSTALL_ROOT/skills/using-superpowers/SKILL.md"
DEBUG="$INSTALL_ROOT/skills/systematic-debugging/SKILL.md"
TDD="$INSTALL_ROOT/skills/test-driven-development/SKILL.md"
VERIFY="$INSTALL_ROOT/skills/verification-before-completion/SKILL.md"
PROGRESSIVE="$INSTALL_ROOT/skills/using-superpowers/references/progressive-skill-loading.md"

for f in "$ROUTER" "$DEBUG" "$TDD" "$VERIFY" "$PROGRESSIVE"; do
  [[ -f "$f" ]] || fail "missing installed contract: $f"
done
pass "all installed progressive-loading contract files exist"

require_text "$ROUTER" "Do not load merely to route ordinary tasks when native skill matching is available." \
  "using-superpowers is compatibility/reference, not mandatory first-hop routing"
reject_text "$ROUTER" "Use at conversation start to route the task" \
  "old mandatory conversation-start router description is absent"

require_text "$DEBUG" "Use while an unexplained bug, test failure, regression, performance anomaly, or unexpected behavior requires root-cause investigation" \
  "debugging activation is unresolved-root-cause scoped"
require_text "$DEBUG" "## Lifecycle" "debugging defines a lifecycle boundary"
require_text "$DEBUG" "Exit:" "debugging defines an exit condition"
require_text "$DEBUG" "Tool Economy" "debugging defaults to bounded tool use"
require_text "$DEBUG" "Do not activate codebase-memory" "debugging does not pair bounded/local diagnosis with codebase-memory"
require_text "$DEBUG" "references/detailed-playbook.md" "debugging preserves detailed guidance behind progressive disclosure"

require_text "$TDD" "a bug fix with established diagnosis" \
  "TDD requires an established diagnosis for bug-fix implementation"
require_text "$TDD" "Do not use for unresolved root-cause investigation or final completion claims." \
  "TDD excludes debugging and completion states"
require_text "$TDD" "## Lifecycle" "TDD defines a lifecycle boundary"
require_text "$TDD" "Tool Economy" "TDD defaults to bounded tool use"
require_text "$TDD" "A concise implementation-result report is not by itself a completion claim" "TDD result reporting does not trigger verification"
require_text "$TDD" "references/detailed-playbook.md" "TDD preserves detailed guidance behind progressive disclosure"

require_text "$VERIFY" "Use only when a correctness, completion, integration, merge, or release claim is imminent" \
  "verification activates only for an imminent claim"
require_text "$VERIFY" "Do not preload during diagnosis or implementation." \
  "verification explicitly forbids preloading"
require_text "$VERIFY" "## Lifecycle" "verification defines a lifecycle boundary"
require_text "$VERIFY" "Tool Economy" "verification defaults to bounded tool use"
require_text "$VERIFY" "references/detailed-playbook.md" "verification preserves detailed guidance behind progressive disclosure"

require_text "$PROGRESSIVE" "Debugging, TDD, and verification are sequential states, not a default bundle." \
  "progressive contract forbids the default three-skill bundle"
require_text "$PROGRESSIVE" "At most one should govern current reasoning except for a brief handoff." \
  "progressive contract limits active workflow ownership"
require_text "$PROGRESSIVE" "Pass compact state across transitions" \
  "progressive contract requires compact handoff"

# Optional live-harness probe. Kept separate because it requires backend connectivity
# and captures durable JSON/stderr artifacts for diagnosis.
if [[ "${LIVE_CODEX:-0}" == "1" ]]; then
  "$ROOT/tests/codex/live-progressive-skill-probe.sh"
fi

echo "Progressive skill loading contract: PASS"
