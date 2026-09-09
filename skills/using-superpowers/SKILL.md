---
name: using-superpowers
description: Use at conversation start to route the task to relevant skills
---

# Using Superpowers

If dispatched as a subagent for a specific task, follow that task's selected workflow instead of restarting this router.

## Minimum Sufficient Change

Choose the smallest change and verification surface that satisfies the request. Reuse existing code, contracts, tests, and recovery state. Added complexity or durable artifacts need a current consumer or demonstrated risk. Preserve correctness, security, authority, data integrity, and explicit repository requirements.

## Route the Task

- **Explanation, inspection, or review:** answer or inspect within the requested scope. Do not automatically start brainstorming, planning, implementation, or delegation.
- **Bug diagnosis or repair:** use systematic-debugging; a diagnosis request alone does not authorize implementing a fix.
- **Implementation:** use brainstorming to resolve material design choices; an explicit, fully specified, reversible bounded change can use its existing authorization. Use TDD for behavior changes.
- **Approved multi-step plan:** use the authorized execution workflow. Preserve detailed steps and the plan's sprint integration/review units.
- **Completion or integration:** use verification-before-completion for required scope and valid result reuse, then finishing-a-development-branch for the authorized integration action.

Honor explicitly requested skills. Otherwise select skills whose descriptions directly match the task; load additional skills/references when a concrete need arises. Read a selected skill before acting on it. An ordinary question or targeted read is not a reason to activate every plausibly related process.

Keep announcements and status concise. Track actionable milestones and recovery state, not a separate todo for every checklist sentence. Do not generate duplicate reports or clean-check narration.

## Platform Adaptation

Read the matching adapter when tool mapping or platform behavior is needed:

- Codex: `references/codex-tools.md`
- Pi: `references/pi-tools.md`
- Antigravity: `references/antigravity-tools.md`
- Hermes Agent: `references/hermes-tools.md`

## Precedence

User and repository instructions take precedence over these workflow defaults. Stop for missing authority, material unresolved design choices, security risk, destructive operations, or irreversible external actions that require approval. Safe in-scope work continues without repeated approval turns.
