#!/usr/bin/env bash
# Behavioral regression for local Codex CLI instruction-response routing: frontend
# browser verification must choose the engine by evidence type.

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

You are executing the browser-verification step of an already-approved
implementation plan in a separate local Codex session. Enter through the normal
executing-plans workflow and evaluate the repository-local workflow skills rooted
at the current Codex working directory, not stale installed plugin copies. Use
read-only local instruction discovery as needed by that normal workflow.

Explain which real browser you will use, how you will make it available, what you
will run, and how you will clean up. Do not start browsers, run tests, modify files,
or execute commands other than read-only local instruction discovery.

End your answer with exactly one machine-readable line, once:
EXECUTION_LANES=<lane decision>

Do not emit READ_AGENTS or READ_TDD_SKILL markers. This response eval checks the
instruction-routing decision; it does not prove file reads or browser execution.

For this scenario, use BEHAVIOR:LIGHTPANDA when only the behavior lane should run,
RENDERING:CHROME when only the rendering lane should run, or BOTH when both are required.
EOF
)

cd "$REPO_ROOT"

if ! command -v codex >/dev/null 2>&1; then
    echo "[BLOCKED] codex CLI is not available on PATH"
    exit 127
fi

# Force the subprocess root to this repository so normal local Codex instruction
# discovery and skill routing apply.
output=$(timeout 300 codex exec --cd "$REPO_ROOT" --sandbox read-only "$SCENARIO")

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

assert_not_contains "$output" '^READ_(AGENTS|TDD_SKILL)=' \
    "omit obsolete self-reported file-read markers"

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

marker_count=$(printf '%s\n' "$output" | grep -Ec '^EXECUTION_LANES=' || true)
if [ "$marker_count" -eq 1 ]; then
    echo "[PASS] emit exactly one lane decision marker"
else
    echo "[FAIL] emit exactly one lane decision marker"
    failures=$((failures + 1))
fi

if [ "$failures" -gt 0 ]; then
    echo ""
    echo "[FAIL] local Codex browser engine routing missed $failures required behavior(s)"
    exit 1
fi

echo ""
echo "[PASS] local Codex routes behavior verification to Lightpanda without redundant Chrome"
