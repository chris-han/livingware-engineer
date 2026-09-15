#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CREATOR="$ROOT/skills/writing-skills/SKILL.md"
REVIEW="$ROOT/skills/skill-review/SKILL.md"
TOKEN_REF="$ROOT/docs/skill-token-economics.md"
ARCH_REF="$ROOT/docs/skill-runtime-architecture.md"
LEARNING_REF="$ROOT/skills/skill-review/references/budgeted-behavioral-learning.md"
LAYERED_EVAL="$ROOT/skills/skill-review/references/layered-evaluation.md"

fail() { echo "FAIL: $*" >&2; exit 1; }
pass() { echo "PASS: $*"; }
require() {
  local file="$1" text="$2" label="$3"
  grep -Fiq "$text" "$file" || fail "$label"
  pass "$label"
}

[[ -f "$TOKEN_REF" ]] || fail "canonical token-economics reference exists"
[[ -f "$ARCH_REF" ]] || fail "canonical layered runtime architecture exists"
[[ -f "$LAYERED_EVAL" ]] || fail "layered evaluation reference exists"
pass "canonical architecture/evaluation references exist"

require "$CREATOR" "skill is a discoverable entry package for a reusable, context-conditioned workflow" "creator defines skill as workflow entry package"
require "$CREATOR" "TOOL / SCRIPT / TEST" "creator routes deterministic mechanics to executable owners"
require "$CREATOR" "POLICY / INVARIANT OWNER" "creator routes stable constraints to policy owner"
require "$CREATOR" "nearest competing state/skill" "creator checks neighboring routing state"
require "$CREATOR" "do not load unnecessary context" "creator prioritizes context elimination"
require "$CREATOR" "../../docs/skill-runtime-architecture.md" "creator uses canonical layered architecture"
require "$CREATOR" "../../docs/skill-token-economics.md" "creator uses canonical token economics"

require "$REVIEW" "TOOL/OPERATOR" "review separates operator ownership"
require "$REVIEW" "references/layered-evaluation.md" "review routes detailed eval to canonical reference"
require "$REVIEW" "simulation narrows search; real execution remains the judge" "review preserves simulation evidence boundary"
require "$REVIEW" "../../docs/skill-runtime-architecture.md" "review points to canonical layered architecture"
require "$REVIEW" "../../docs/skill-token-economics.md" "review points to canonical token economics"

require "$TOKEN_REF" "routing/discovery context" "token model measures routing context"
require "$TOKEN_REF" "selected workflow context" "token model measures selected workflow context"
require "$TOKEN_REF" "optional simulation/replay cost" "token model measures counterfactual cost"
require "$TOKEN_REF" "OBSERVED | REPLAYED | SIMULATED | INFERRED | ASSUMED" "token economics preserves evidence provenance"

require "$LEARNING_REF" "ten thousand rollouts" "learning contract rejects synthetic-volume independence"
require "$LEARNING_REF" "REAL_REEXECUTION" "learning contract distinguishes real re-execution"

echo "Layered skill/token-economics contracts: PASS"
