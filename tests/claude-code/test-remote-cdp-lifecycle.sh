#!/usr/bin/env bash
# Behavioral regression: shared Chrome CDP debugging must preserve the operator's
# natural viewport and distinguish application layout from capture-surface state.
#
# RED evidence: the Semantier UI debugging session that motivated this test
# repeatedly changed CSS after DOM right-edge equality was already proven. A stale
# Playwright process had left a 1024x768 viewport override on persistent Chrome,
# and PowerShell was invoked from WSL even though CDP was reachable.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

SCENARIO=$(cat <<'EOF'
You are debugging a responsive web page from WSL using the user's already-running,
persistent Windows Chrome at http://127.0.0.1:9222. The page's JavaScript metrics
show documentElement.getBoundingClientRect().right === innerWidth, but screenshots
still show a large blank strip on the right. A previous Playwright script called
page.setViewportSize({width: 1024, height: 768}) and may still be alive.

Read these Livingware Engineer skills before answering:
- skills/systematic-debugging/SKILL.md
- skills/test-driven-development/SKILL.md
- skills/verification-before-completion/SKILL.md

Give the exact investigation and browser-lifecycle procedure you would follow.
The operator has work open in Chrome, so preserve their tabs and natural viewport.
Do not modify files or actually connect to Chrome.
EOF
)

cd "$REPO_ROOT"
output=$(run_claude "$SCENARIO" 300 "Read")

echo "Agent output:"
echo "$output"
echo ""

failures=0

assert_contains "$output" "Page.getLayoutMetrics\|layout metrics" \
    "compare browser layout metrics with the screenshot surface" || failures=$((failures + 1))
assert_contains "$output" "pixel dimensions\|screenshot dimensions" \
    "inspect actual screenshot dimensions" || failures=$((failures + 1))
assert_contains "$output" "site zoom\|zoom setting\|zoom level" \
    "check persistent per-site zoom" || failures=$((failures + 1))
assert_contains "$output" "stale.*Playwright\|Playwright.*process\|Node.*process" \
    "inspect stale automation ownership" || failures=$((failures + 1))
assert_contains "$output" "fixture-owned\|dedicated.*tab\|new.*page" \
    "use a dedicated owned page" || failures=$((failures + 1))
assert_contains "$output" "clearDeviceMetricsOverride\|clear.*device metrics" \
    "clear any CDP device-metrics override" || failures=$((failures + 1))
assert_contains "$output" "finally\|try/finally" \
    "make cleanup unconditional" || failures=$((failures + 1))
assert_contains "$output" "disconnect" \
    "disconnect without closing shared Chrome" || failures=$((failures + 1))
assert_contains "$output" "do not.*setViewportSize\|never.*setViewportSize\|avoid.*setViewportSize" \
    "forbid persistent viewport mutation" || failures=$((failures + 1))
assert_contains "$output" "PowerShell" \
    "address the WSL host-boundary constraint" || failures=$((failures + 1))
assert_contains "$output" "do not.*PowerShell\|no.*PowerShell\|without.*PowerShell" \
    "keep diagnostics in WSL/CDP while the endpoint is reachable" || failures=$((failures + 1))

if [ "$failures" -gt 0 ]; then
    echo ""
    echo "[FAIL] remote CDP lifecycle behavior missed $failures required safeguard(s)"
    exit 1
fi

echo ""
echo "[PASS] remote CDP lifecycle behavior preserved shared-browser state"
