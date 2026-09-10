---
name: using-superpowers
description: Use at conversation start to route the task to relevant skills
---

# Using Superpowers

If dispatched as a subagent for a specific task, follow that task's selected workflow instead of restarting this router.

## Minimum Sufficient Engineering

Choose the smallest change, verification surface, and review process that satisfies the request. Reuse existing code, contracts, tests, and recovery state. Added complexity or durable artifacts need a current consumer or demonstrated risk. Preserve correctness, security, required permissions, data integrity, product/runtime audit requirements, and explicit repository requirements.

Verification exists to catch mistakes, not to create proof that work happened. Review follows risk: ordinary changes need affected verification plus a quick diff scan; architectural changes get one structured review at the coherent integration boundary; high-risk changes require deliberate failure-mode review and rollback/recovery consideration. Do not add another review merely because a workflow phase changed.

## Route the Task

- **Explanation, inspection, or review:** answer or inspect within the requested scope. Do not automatically start brainstorming, planning, implementation, or delegation.
- **Bug diagnosis or repair:** use systematic-debugging; a diagnosis request alone does not authorize implementing a fix.
- **Implementation:** use brainstorming to resolve material design choices; an explicit, fully specified, reversible bounded change can use its existing authorization. Use the TDD/testing workflow for behavior changes, bug fixes, and behavior-preserving refactors.
- **Approved multi-step plan:** use the authorized execution workflow. Preserve detailed steps and the plan's sprint integration/review units.
- **Completion or integration:** use verification-before-completion for required scope and valid result reuse, then finishing-a-development-branch for the authorized integration action.

Honor explicitly requested skills. Otherwise select skills whose descriptions directly match the task; load additional skills/references when a concrete need arises. Read a selected skill before acting on it. An ordinary question or targeted read is not a reason to activate every plausibly related process.

Keep announcements and status concise. Track actionable milestones and recovery state, not a separate todo for every checklist sentence. Do not generate duplicate reports or clean-check narration.

## Active Worktree Graph

When codebase-memory MCP is available for structural code discovery, resolve the active checkout with `git rev-parse --show-toplevel`. At session start/resume and after switching worktrees, use `list_projects` to match its exact root, not merely the repository name or main checkout. If absent, use `index_repository` on that active root as a separate project; do not repoint main's index. Inspect `index_status` before relying on the graph and reuse a healthy existing index instead of forcing a rebuild.

Check affected paths with `check_index_coverage`; read source for uncovered or stale ranges, including uncommitted changes not yet indexed. If indexing is unavailable or fails, state the limitation and continue with targeted source reads, never substituting main's graph as worktree truth. Literal and documentation lookups can still use direct reads/search without indexing.

## Platform Adaptation

Read the matching adapter when tool mapping or platform behavior is needed:

- Codex: `references/codex-tools.md`
- Pi: `references/pi-tools.md`
- Antigravity: `references/antigravity-tools.md`
- Hermes Agent: `references/hermes-tools.md`

## Precedence

User and repository instructions take precedence over these workflow defaults. Stop for missing permission, material unresolved design choices, security risk, destructive operations, or irreversible external actions that require approval. Safe in-scope work continues without repeated approval turns.
