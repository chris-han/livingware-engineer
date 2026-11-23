#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CREATOR="$ROOT/skills/writing-skills/SKILL.md"
REVIEW="$ROOT/skills/skill-review/SKILL.md"
EXECUTING="$ROOT/skills/executing-plans/SKILL.md"
DESIGN="$ROOT/skills/brainstorming/SKILL.md"
PLANNING="$ROOT/skills/writing-plans/SKILL.md"
FINAL="$ROOT/skills/verification-before-completion/SKILL.md"
EXECUTING_ROUTING="$ROOT/skills/executing-plans/references/workflow-routing.md"
TOKEN_REF="$ROOT/docs/skill-token-economics.md"
ARCH_REF="$ROOT/docs/skill-runtime-architecture.md"
LEARNING_REF="$ROOT/skills/skill-review/references/budgeted-behavioral-learning.md"
LAYERED_EVAL="$ROOT/skills/skill-review/references/layered-evaluation.md"

fail() { echo "FAIL: $*" >&2; exit 1; }
pass() { echo "PASS: $*"; }
require() {
  local file="$1" text="$2" label="$3"
  if ! grep -Fiq "$text" "$file"; then
    if [[ "$file" == "$EXECUTING" ]]; then
      grep -Fiq "$text" "$ROOT/skills/executing-plans/references/detailed-execution-workflow.md" || fail "$label"
    else
      fail "$label"
    fi
  fi
  pass "$label"
}

for file in "$TOKEN_REF" "$ARCH_REF" "$LAYERED_EVAL" "$EXECUTING_ROUTING"; do
  [[ -f "$file" ]] || fail "required layered architecture/reference missing: $file"
done
pass "canonical architecture/evaluation/workflow references exist"

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

require "$EXECUTING" "references/workflow-routing.md" "executing-plans routes transition topology to workflow reference"
require "$EXECUTING" 'unexplained failure -> `systematic-debugging`' "executing-plans delegates unresolved diagnosis"
require "$EXECUTING" 'authorized changed behavior -> `test-driven-development`' "executing-plans delegates implementation behavior"
require "$EXECUTING" 'final goal/integration/merge/release claim needing an evidence check -> `verification-before-completion`' "executing-plans delegates completion claims"
require "$EXECUTING_ROUTING" "PLAN_REVIEW" "execution workflow owns explicit state topology"
require "$EXECUTING_ROUTING" "Do not preload these skills." "execution workflow preserves current-state loading"

require "$TOKEN_REF" "routing/discovery context" "token model measures routing context"
require "$TOKEN_REF" "selected workflow context" "token model measures selected workflow context"
require "$TOKEN_REF" "optional simulation/replay cost" "token model measures counterfactual cost"
require "$TOKEN_REF" "OBSERVED | REPLAYED | SIMULATED | INFERRED | ASSUMED" "token economics preserves evidence provenance"

require "$LEARNING_REF" "ten thousand rollouts" "learning contract rejects synthetic-volume independence"
require "$LEARNING_REF" "REAL_REEXECUTION" "learning contract distinguishes real re-execution"

# Progressive phase entry is a routing invariant, not a word-count contest.
require "$DESIGN" "Do not preload planning, implementation, or verification skills" "design remains the active phase until settled"
require "$PLANNING" "Do not preload the UI craft tool" "planning does not preload visual craft"
require "$PLANNING" 'invoke `executing-plans` only when actual implementation begins' "planning exits before execution"
require "$EXECUTING" "Do not preload verification" "execution does not preload completion verification"
require "$EXECUTING" "No parallel tracker." "execution reuses the plan as authority"
require "$FINAL" "Do not preload during implementation" "final verification is a claim check only"
for detail in \
 "$ROOT/skills/brainstorming/references/detailed-design-workflow.md" \
 "$ROOT/skills/writing-plans/references/detailed-plan-workflow.md" \
 "$ROOT/skills/executing-plans/references/detailed-execution-workflow.md"; do
  [[ -f "$detail" ]] || fail "on-demand workflow reference missing: $detail"
done
pass "conditional references preserve deeper workflow contracts without eager loading"

echo "Layered skill/token-economics contracts: PASS"
