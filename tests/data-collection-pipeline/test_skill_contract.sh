#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SKILL="$ROOT/skills/data-collection-pipeline/SKILL.md"
RECOVERY="$ROOT/skills/data-collection-pipeline/references/access-recovery.md"
CRAWLEE="$ROOT/skills/data-collection-pipeline/references/crawlee-python-adapter.md"
FREEZE="$ROOT/skills/data-collection-pipeline/scripts/freeze_artifact.py"
VERIFY="$ROOT/skills/data-collection-pipeline/scripts/verify_frozen.py"

for f in "$SKILL" "$RECOVERY" "$CRAWLEE" "$FREEZE" "$VERIFY"; do
  [[ -f "$f" ]] || { echo "FAIL: missing $f"; exit 1; }
done

grep -Fq "An entry-point failure is evidence about that entry point, not about source existence." "$SKILL"
grep -Fq "Alternate-source lane" "$SKILL"
grep -Fq "Same-site alternate-entry lane" "$SKILL"
grep -Fq "retry_on_blocked=False" "$SKILL"
grep -Fq "retry_on_blocked=True" "$SKILL"
grep -Fq "401" "$SKILL"
grep -Fq "403" "$SKILL"
grep -Fq "429" "$SKILL"
grep -Fq "Livingware owns acquisition strategy" "$SKILL"
grep -Fq "Crawlee Python" "$SKILL"
grep -Fq "max_session_rotations=0" "$CRAWLEE"
grep -Fq "max_request_retries=0" "$CRAWLEE"
grep -Fq "ignore_http_error_status_codes=[401, 403, 429]" "$CRAWLEE"
grep -Fq "max_session_rotations=1" "$CRAWLEE"
grep -Fq "Never auto-escalate `401`" "$CRAWLEE"
grep -Fq "The point is not to bypass authentication controls." "$RECOVERY"
if grep -Fq "fetch_and_freeze.py" "$SKILL"; then
  echo "FAIL: custom HTTP acquisition operator should not remain in the skill"
  exit 1
fi
python3 "$ROOT/tests/data-collection-pipeline/test_freeze_and_verify.py"
python3 "$ROOT/tests/data-collection-pipeline/test_tender_law_historical_fixture.py"
python3 "$ROOT/tests/data-collection-pipeline/test_ccgp_blocked_recovery.py"
echo "PASS: data-collection-pipeline skill contract"
