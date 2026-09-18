#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SKILL="$ROOT/skills/data-collection-pipeline/SKILL.md"
REF="$ROOT/skills/data-collection-pipeline/references/access-recovery.md"
SCRIPT="$ROOT/skills/data-collection-pipeline/scripts/fetch_and_freeze.py"
VERIFY="$ROOT/skills/data-collection-pipeline/scripts/verify_frozen.py"

for f in "$SKILL" "$REF" "$SCRIPT" "$VERIFY"; do [[ -f "$f" ]] || { echo "FAIL: missing $f"; exit 1; }; done
grep -Fq "An entry-point failure is evidence about that entry point, not about source existence." "$SKILL"
grep -Fq "Alternate-source lane" "$SKILL"
grep -Fq "Same-site alternate-entry lane" "$SKILL"
grep -Fq "Do not serially exhaust one before trying the other" "$SKILL"
grep -Fq "DISCOVERED" "$SKILL"
grep -Fq "OFFLINE_VERIFIED" "$SKILL"
grep -Fq "The point is not to bypass authentication controls." "$REF"
grep -Fq "fetch_and_freeze.py" "$SKILL"
grep -Fq "verify_frozen.py" "$SKILL"
python3 "$ROOT/tests/data-collection-pipeline/test_fetch_and_freeze.py"
echo "PASS: data-collection-pipeline skill contract"
