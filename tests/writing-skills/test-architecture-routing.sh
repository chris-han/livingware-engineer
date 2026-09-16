#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BRAINSTORM="$ROOT/skills/brainstorming/SKILL.md"
PLANS="$ROOT/skills/writing-plans/SKILL.md"
ARCH="$ROOT/docs/skill-runtime-architecture.md"
DELTA="$ROOT/docs/architecture-delta-principle.md"
WORKFLOW="$ROOT/.github/workflows/layered-runtime-ci.yml"

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
require "$BRAINSTORM" "docs/architecture-delta-principle.md" \
  "brainstorming loads canonical Architecture Delta policy"
require "$BRAINSTORM" "Architecture Delta Probe" \
  "brainstorming requires an Architecture Delta Probe before architecture change"
require "$BRAINSTORM" "NO_CHANGE_REQUIRED" \
  "brainstorming treats empty delta as a terminal no-change result"
require "$BRAINSTORM" "Architecture design is not a parallel unguided mode" \
  "brainstorming rejects a parallel architecture-design mode"

require "$DELTA" "Unknown is not missing" \
  "Architecture Delta policy separates unknown from missing"
require "$DELTA" "Empty delta stops change" \
  "Architecture Delta policy stops zero-delta work"
require "$DELTA" 'Only `PARTIAL` and `UNSATISFIED` create delta items' \
  "Architecture Delta policy bounds delta-producing states"
require "$DELTA" 'Only `PROCEED_WITH_DELTA` permits architecture-changing implementation work' \
  "Architecture Delta policy has a deterministic proceed disposition"
require "$DELTA" "what must change" \
  "Architecture Delta remains upstream of impact analysis"

require "$PLANS" "## Architecture Delta Before Architecture Work" \
  "writing-plans consumes the Architecture Delta contract"
require "$PLANS" "## Architecture Delta Review" \
  "plan header carries the Architecture Delta review"
require "$PLANS" "**Disposition:** PROCEED_WITH_DELTA | NO_CHANGE_REQUIRED | INVESTIGATE_UNKNOWN | REFRESH_CONTEXT | REDUCE_SCOPE | NOT_APPLICABLE" \
  "plan header exposes bounded Architecture Delta dispositions"
require "$PLANS" "must not manufacture implementation tasks" \
  "writing-plans forbids implementation work for an empty delta"

require "$ARCH" "Conceptual-to-engineering reclassification invariant" \
  "runtime architecture owns conceptual-to-engineering reclassification"
require "$ARCH" "named contract, interface, service, store, object, or subsystem" \
  "runtime architecture names code-level transition signals"
require "$ARCH" "native skill matching should expose the matching design workflow at that point" \
  "runtime architecture preserves progressive disclosure at the transition"
require "$ARCH" "must not require an always-on meta-router" \
  "runtime architecture preserves no-meta-router rule"

require "$WORKFLOW" "bash tests/writing-skills/test-architecture-routing.sh" \
  "CI executes the Architecture Delta/routing deterministic contract"

echo "Architecture routing + delta contract: PASS"
