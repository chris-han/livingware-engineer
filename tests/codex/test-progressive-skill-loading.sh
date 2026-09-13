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
require_text "$DEBUG" "## Lifecycle Boundary" "debugging defines a lifecycle boundary"
require_text "$DEBUG" "Exit:" "debugging defines an exit condition"

require_text "$TDD" "a bug fix with established diagnosis" \
  "TDD requires an established diagnosis for bug-fix implementation"
require_text "$TDD" "Do not use for unresolved root-cause investigation or final completion claims." \
  "TDD excludes debugging and completion states"
require_text "$TDD" "## Lifecycle Boundary" "TDD defines a lifecycle boundary"

require_text "$VERIFY" "Use only when a correctness, completion, integration, merge, or release claim is imminent" \
  "verification activates only for an imminent claim"
require_text "$VERIFY" "Do not preload during diagnosis or implementation." \
  "verification explicitly forbids preloading"
require_text "$VERIFY" "## Lifecycle Boundary" "verification defines a lifecycle boundary"

require_text "$PROGRESSIVE" "Debugging, TDD, and verification are sequential states, not a default bundle." \
  "progressive contract forbids the default three-skill bundle"
require_text "$PROGRESSIVE" "At most one should govern current reasoning except for a brief handoff." \
  "progressive contract limits active workflow ownership"
require_text "$PROGRESSIVE" "Pass compact state across transitions" \
  "progressive contract requires compact handoff"

# Optional real-harness smoke probe. It is intentionally not part of the deterministic
# default gate because it requires live Codex backend connectivity and can fail for
# network/auth reasons unrelated to skill routing.
if [[ "${LIVE_CODEX:-0}" == "1" ]]; then
  command -v codex >/dev/null || fail "LIVE_CODEX=1 but codex CLI is unavailable"
  tmp="$(mktemp -d)"
  trap 'rm -rf "$tmp"' EXIT

  echo "Running live Codex routing probes (network/auth required)..."
  prompts=(
    "A unit test started failing after a dependency update. Diagnose root cause only; do not modify files."
    "The root cause is established: normalizePath now rejects an empty string. Implement the authorized bug fix with a regression test."
    "Implementation and focused tests are green. Determine whether it is valid to claim the fix is complete and ready to merge."
  )
  expected=("systematic-debugging" "test-driven-development" "verification-before-completion")

  for i in 0 1 2; do
    out="$tmp/probe-$i.jsonl"
    timeout "${LIVE_CODEX_TIMEOUT:-180}" codex exec --json --ephemeral --sandbox read-only \
      "${prompts[$i]} Before doing any work, state the single Livingware workflow skill that governs the current state as SKILL=<name>." \
      >"$out" 2>"$tmp/probe-$i.err" || {
        cat "$tmp/probe-$i.err" >&2 || true
        fail "live Codex probe $i did not complete"
      }
    grep -Fq "SKILL=${expected[$i]}" "$out" || {
      cat "$out" >&2
      fail "live probe $i did not select ${expected[$i]}"
    }
    pass "live probe $i selected ${expected[$i]}"
  done
fi

echo "Progressive skill loading contract: PASS"
