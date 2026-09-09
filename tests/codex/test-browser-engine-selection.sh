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
will run, and how you will clean up. Do not modify files or actually run commands.

End your answer with exactly one machine-readable lane decision line using this form:
EXECUTION_LANES=<lane decision>
For this scenario, use BEHAVIOR:LIGHTPANDA when only the behavior lane should run,
RENDERING:CHROME when only the rendering lane should run, or BOTH when both are required.
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
assert_contains "$output" "^EXECUTION_LANES=BEHAVIOR:LIGHTPANDA$" \
    "keep the behavior-only execution on the Lightpanda lane"

lane_count=$(printf '%s\n' "$output" | grep -Ec '^EXECUTION_LANES=' || true)
if [ "$lane_count" -eq 1 ]; then
    echo "[PASS] emit exactly one browser lane decision"
else
    echo "[FAIL] emit exactly one browser lane decision"
    failures=$((failures + 1))
fi

if [ "$failures" -gt 0 ]; then
    echo ""
    echo "[FAIL] browser engine selection missed $failures required behavior(s)"
    exit 1
fi

echo ""
echo "[PASS] Codex browser engine selection uses Lightpanda for behavior without redundant Chrome"
