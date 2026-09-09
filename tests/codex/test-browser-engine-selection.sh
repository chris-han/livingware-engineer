#!/usr/bin/env bash
# Behavioral regression for Codex: frontend browser verification must choose the
# engine by evidence type, auto-start Lightpanda for behavior, and avoid duplicate Chrome runs.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

SCENARIO=$(cat <<'EOF'
You changed a frontend filter interaction. The acceptance criterion is behavioral:
clicking the filter must update application state and the visible DOM result. There
is no screenshot, layout, font, canvas, WebGL/WebGPU, or Chromium-specific rendering
criterion. You are working from WSL. Lightpanda is installed but
http://127.0.0.1:9223 is not currently reachable. Windows Chrome happens to be
running at http://127.0.0.1:9222.

Read AGENTS.md and skills/test-driven-development/SKILL.md before answering.
Explain which real browser you will use, how you will make it available, what you
will run, and how you will clean up. State which browser lane or lanes you would
actually execute. Do not modify files or actually run commands.
EOF
)

cd "$REPO_ROOT"

if ! command -v codex >/dev/null 2>&1; then
    echo "[BLOCKED] codex CLI is not available on PATH"
    exit 127
fi

output=$(timeout 300 codex exec --sandbox read-only "$SCENARIO")

echo "Agent output:"
echo "$output"
echo ""

failures=0

assert_contains() {
    local haystack="$1"
    local pattern="$2"
    local description="$3"
    if printf '%s\n' "$haystack" | grep -Eiq "$pattern"; then
        echo "[PASS] $description"
    else
        echo "[FAIL] $description"
        failures=$((failures + 1))
    fi
}

assert_not_contains() {
    local haystack="$1"
    local pattern="$2"
    local description="$3"
    if printf '%s\n' "$haystack" | grep -Eiq "$pattern"; then
        echo "[FAIL] $description"
        failures=$((failures + 1))
    else
        echo "[PASS] $description"
    fi
}

assert_contains "$output" "Lightpanda" \
    "choose Lightpanda for behavior verification"
assert_contains "$output" "9223" \
    "use the designated Lightpanda CDP endpoint"
assert_contains "$output" "lightpanda serve.*9223|serve.*Lightpanda.*9223" \
    "start Lightpanda when the behavior endpoint is absent"
assert_contains "$output" "PID|process.*started|started.*process|ownership" \
    "record ownership of the started Lightpanda process"
assert_contains "$output" "stop only|kill only|only.*started|leave.*running" \
    "clean up only fixture-owned Lightpanda"
assert_contains "$output" "affected|filter" \
    "run the affected browser test rather than broad duplicate coverage"

# Negative controls: mentioning Chrome to explain why it is unnecessary is valid.
# Fail only when Codex positively proposes executing Chrome for this behavior-only
# acceptance criterion, or proposes executing both browser lanes.
assert_not_contains "$output" "(?:use|run|execute|test|verify|attach to|connect to).{0,40}(?:Chrome|9222)|(?:Chrome|9222).{0,40}(?:use|run|execute|test|verify|attach|connect)(?![^.\n]{0,40}(?:not|no need|unnecessary|skip|avoid))" \
    "keep the behavior-only execution on the Lightpanda lane"
assert_not_contains "$output" "(?:run|execute|test|verify).{0,40}(?:both|Lightpanda.{0,30}(?:and|plus).{0,30}Chrome|Chrome.{0,30}(?:and|plus).{0,30}Lightpanda)" \
    "avoid duplicate execution in both engines"

if [ "$failures" -gt 0 ]; then
    echo ""
    echo "[FAIL] browser engine selection missed $failures required behavior(s)"
    exit 1
fi

echo ""
echo "[PASS] Codex browser engine selection uses Lightpanda for behavior without redundant Chrome"
