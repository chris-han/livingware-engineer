#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BRAINSTORM="$ROOT/skills/brainstorming/SKILL.md"
ARCH="$ROOT/docs/skill-runtime-architecture.md"

fail() { echo "FAIL: $*" >&2; exit 1; }
pass() { echo "PASS: $*"; }
require() {
  local file="$1" text="$2" label="$3"
  grep -Fiq "$text" "$file" || fail "$label"
  pass "$label"
}

DESCRIPTION="$(sed -n '3s/^description: //p' "$BRAINSTORM")"
[[ -n "$DESCRIPTION" ]] || fail "brainstorming description exists"

for term in architecture contracts "existing repo"; do
  [[ "$DESCRIPTION" == *"$term"* ]] || fail "brainstorming description routes code-relevant $term design"
done
pass "brainstorming description covers architecture/contracts/existing-repo design"

[[ "$DESCRIPTION" == *"purely conceptual"* ]] || fail "brainstorming description excludes purely conceptual research"
pass "brainstorming description keeps conceptual-research negative boundary"

require "$BRAINSTORM" "Reclassify when a conceptual or research discussion begins proposing code-level" \
  "brainstorming reclassifies conceptual-to-code transitions"
require "$BRAINSTORM" "inspect the current project state before proposing the architectural delta" \
  "brainstorming requires repo-first grounding before architecture delta"
require "$BRAINSTORM" "Architecture design is not a parallel unguided mode" \
  "brainstorming rejects a parallel architecture-design mode"

require "$ARCH" "Conceptual-to-engineering reclassification invariant" \
  "runtime architecture owns conceptual-to-engineering reclassification"
require "$ARCH" "named contract, interface, service, store, object, or subsystem" \
  "runtime architecture names code-level transition signals"
require "$ARCH" "native skill matching should expose the matching design workflow at that point" \
  "runtime architecture preserves progressive disclosure at the transition"
require "$ARCH" "must not require an always-on meta-router" \
  "runtime architecture preserves no-meta-router rule"

echo "Architecture routing contract: PASS"
