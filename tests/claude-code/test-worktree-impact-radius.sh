#!/usr/bin/env bash
# Behavioral regression: small, reversible changes in a clean checkout should
# stay in place; broader changes should still use worktree isolation.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/test-helpers.sh"

CLAUDE_PROMPT_TIMEOUT="${CLAUDE_PROMPT_TIMEOUT:-120}"

echo "=== Worktree Impact Radius Test ==="

bounded_output=$(run_claude 'IMPORTANT: Choose the workspace strategy now.

The repository is on main and git status is clean. The approved change is a
single existing React component plus its focused regression test. It changes
no schema, dependency, public API, deployment configuration, or generated
artifact, and it is straightforward to revert.

Use the using-git-worktrees skill. State exactly one decision and do not ask a
question. Answer using exactly:
Decision: <work in place OR create worktree>
Reason: <one sentence>' "$CLAUDE_PROMPT_TIMEOUT")

assert_contains "$bounded_output" 'Decision:.*work in place' \
  "Clean bounded change stays in place"

broad_output=$(run_claude 'IMPORTANT: Choose the workspace strategy now.

The repository is on main and git status is clean. The approved work changes
an API contract, database migration, frontend consumer, deployment workflow,
and browser acceptance journey across two repositories.

Use the using-git-worktrees skill. State exactly one decision and do not ask a
question. Answer using exactly:
Decision: <work in place OR create worktree>
Reason: <one sentence>' "$CLAUDE_PROMPT_TIMEOUT")

assert_contains "$broad_output" 'Decision:.*create worktree' \
  "Broad cross-boundary change uses isolation"

echo "=== Worktree Impact Radius Test Passed ==="
