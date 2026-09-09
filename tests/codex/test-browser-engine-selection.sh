#!/usr/bin/env bash
# Behavioral regression for Codex: frontend browser verification must choose the
# engine by evidence type and independently read both instruction layers.

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

Before answering, independently read BOTH of these repository files from the current
workspace:
1. AGENTS.md
2. skills/test-driven-development/SKILL.md

Do not rely on one file as a substitute for the other. If either file cannot be read,
say so and report NO for that layer below rather than pretending it was checked.

Explain which real browser you will use, how you will make it available, what you
will run, and how you will clean up. Do not modify files or actually run commands.

End your answer with exactly these three machine-readable lines, once each:
READ_AGENTS=<YES|NO>
READ_TDD_SKILL=<YES|NO>
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

assert_exact_once() {
    local haystack="$1"
    local line="$2"
    local description="$3"
    local count
    count=$(printf '%s\n' "$haystack" | grep -Fxc "$line" || true)
    if [ "$count" -eq 1 ]; then
        echo "[PASS] $description"
    else
        echo "[FAIL] $description"
        failures=$((failures + 1))
    fi
}

assert_exact_once "$output" "READ_AGENTS=YES" \
    "read AGENTS.md independently"
assert_exact_once "$output" "READ_TDD_SKILL=YES" \
    "read TDD SKILL.md independently"

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
assert_exact_once "$output" "EXECUTION_LANES=BEHAVIOR:LIGHTPANDA" \
    "keep the behavior-only execution on the Lightpanda lane"

marker_count=$(printf '%s\n' "$output" | grep -Ec '^(READ_AGENTS|READ_TDD_SKILL|EXECUTION_LANES)=' || true)
if [ "$marker_count" -eq 3 ]; then
    echo "[PASS] emit exactly three instruction/lane decision markers"
else
    echo "[FAIL] emit exactly three instruction/lane decision markers"
    failures=$((failures + 1))
fi

if [ "$failures" -gt 0 ]; then
    echo ""
    echo "[FAIL] browser engine selection/readability missed $failures required behavior(s)"
    exit 1
fi

echo ""
echo "[PASS] Codex independently reads both instruction layers and uses Lightpanda for behavior without redundant Chrome"
