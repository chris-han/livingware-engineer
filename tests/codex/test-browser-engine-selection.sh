#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TDD_SKILL="$ROOT_DIR/skills/test-driven-development/SKILL.md"
WRITING_GOOD_TESTS="$ROOT_DIR/skills/test-driven-development/writing-good-tests.md"
REMOTE_LIFECYCLE="$ROOT_DIR/skills/test-driven-development/remote-cdp-browser-lifecycle.md"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

assert_contains() {
  local file="$1"
  local expected="$2"
  grep -Fq -- "$expected" "$file" || fail "$file missing expected text: $expected"
}

assert_not_contains() {
  local file="$1"
  local unexpected="$2"
  if grep -Fq -- "$unexpected" "$file"; then
    fail "$file unexpectedly contains: $unexpected"
  fi
}

# Browser evidence lanes remain explicit and non-duplicative.
assert_contains "$WRITING_GOOD_TESTS" 'BEHAVIOR:'
assert_contains "$WRITING_GOOD_TESTS" 'Lightpanda at `http://127.0.0.1:9223`'
assert_contains "$WRITING_GOOD_TESTS" 'RENDERING:'
assert_contains "$WRITING_GOOD_TESTS" 'remote Windows Chrome at `http://127.0.0.1:9222`'
assert_contains "$WRITING_GOOD_TESTS" 'run both only when the acceptance criterion genuinely requires independent behavior and rendering evidence'

# Authenticated browser fixtures must not depend on human/external login setup.
assert_contains "$WRITING_GOOD_TESTS" '### Authenticated Frontend Fixture Rule'
assert_contains "$WRITING_GOOD_TESTS" 'real test DB/repository -> temporary user -> username/password login -> real app -> affected UI path'
assert_contains "$WRITING_GOOD_TESTS" 'Do not use QR-code login, device pairing, SMS/email OTP, OAuth approval, or another human/external interactive login mechanism merely to establish an authenticated test fixture.'
assert_contains "$WRITING_GOOD_TESTS" 'Interactive authentication mechanisms are exercised only when that authentication mechanism itself is the behavior being tested.'
assert_contains "$WRITING_GOOD_TESTS" 'prefer the application'
assert_contains "$WRITING_GOOD_TESTS" 'real repository/service or supported test fixture path over raw SQL'
assert_contains "$WRITING_GOOD_TESTS" 'do not reuse developer, staging, production, or long-lived shared credentials'

# Canonical references should continue to route frontend testing through the lifecycle contract.
assert_contains "$TDD_SKILL" 'remote-cdp-browser-lifecycle.md'
assert_contains "$WRITING_GOOD_TESTS" 'remote-cdp-browser-lifecycle.md'

# Guard against collapsing the policy back into one browser-for-everything advice.
assert_not_contains "$WRITING_GOOD_TESTS" 'use Chrome for all frontend tests'
assert_not_contains "$WRITING_GOOD_TESTS" 'use Lightpanda for rendering correctness'

echo "PASS: browser evidence selection and authenticated fixture policy"
