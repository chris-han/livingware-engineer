#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CREATOR="$ROOT/skills/writing-skills/SKILL.md"
REVIEW="$ROOT/skills/skill-review/SKILL.md"
REFERENCE="$ROOT/docs/skill-token-economics.md"

fail() { echo "FAIL: $*" >&2; exit 1; }
pass() { echo "PASS: $*"; }
require() {
  local file="$1" text="$2" label="$3"
  grep -Fq "$text" "$file" || fail "$label"
  pass "$label"
}

[[ -f "$REFERENCE" ]] || fail "canonical token-economics reference exists"
pass "canonical token-economics reference exists"

require "$CREATOR" "Do not load unnecessary context" "creator prioritizes context elimination"
require "$CREATOR" "Prevent activation collisions" "creator checks activation collisions"
require "$CREATOR" "Keep the root contract minimal" "creator requires compact roots and progressive disclosure"
require "$CREATOR" "Design tool economy" "creator treats tool behavior as token cost"
require "$CREATOR" "Only then compress wording" "creator makes lexical compression the last optimization"
require "$CREATOR" "../../docs/skill-token-economics.md" "creator uses canonical token-economics reference"

require "$REVIEW" "Audit token economics across the whole agent loop" "review audits whole-loop economics"
require "$REVIEW" "fixed startup/context cost from selected-skill and tool-loop cost" "review separates fixed and workflow costs"
require "$REVIEW" "mandatory meta-routing" "review flags redundant meta-routing"
require "$REVIEW" "large unbounded tool responses" "review flags tool-output amplification"
require "$REVIEW" "single run or a large host repository" "review requires comparable repeated measurement"
require "$REVIEW" "../../docs/skill-token-economics.md" "review uses canonical token-economics reference"

echo "Skill token-economics contracts: PASS"
