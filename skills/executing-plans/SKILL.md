---
name: executing-plans
description: Use when a written implementation plan is ready to execute continuously through its authorized stopping criterion, involving the user only when intervention is genuinely necessary.
---

# Executing Plans — Active Plan Delivery

**Enter** once a written governed plan is authorized and selected for actual implementation. Load the authoritative plan/spec, freeze the stated user-visible goal and acceptance, then execute continuously until the plan's declared terminal predicate **and required integration/retirement** are proved or the User Intervention Necessity Test truly applies. Intermediate task PASS, review, successful test, merge, checkpoint or session boundary is not the goal.

**Exit** at terminal evidence and owner-safe integration/retirement, or an actual user-owned missing decision; preserve the unfinished outer goal when a negative/inconclusive plan disposition closes only its bounded research/engineering scope. Do not preload verification, debugging, new design, research or branch-finishing instructions before those states are entered.

## Parallel implementation and candidate authorization

Default to **one** implementation path. Multiple concurrent implementation agents or competing implementation candidates require explicit prior approval for that run: disclose agent/candidate counts, scope, comparison criteria, credible total token/compute/review costs or enforceable caps, and stopping conditions. An approved goal or an agent-written plan does not authorize parallelism. Existing explicit approval covering these limits need not be requested again. Sequential normal repair/tests and bounded ordinary review are not competing-candidate runs. Never exceed approved limits autonomously. See [full authorization mechanics](references/detailed-execution-workflow.md#parallel-implementation-and-candidate-authorization) only when parallel implementation is proposed.

## Plan authority and workspace

Read the repository's plan lifecycle rules. Before implementation edits, run its declared plan-state linter/validator when present. Keep status distinct from lifecycle; do not infer execution authorization from a draft or historical archive.

- **One authoritative plan:** its mutable copy lives where the repository specifies (Livingware default main checkout). Implementation worktrees do not own a second plan; preserve concurrent main edits.
- **Worktree isolation:** use `using-git-worktrees` when required by dirty state, risk, or the plan. Verify actual worktree root, branch and integration target match the plan at entry and hard execution gates. Never switch worktrees silently or retire someone else's resources.
- **Recoverable state:** keep meaningful checkpoints and qualified refs in the existing plan; use existing Git/test/CI evidence, not new per-PASS logs, receipts or `.artifacts` progress journals. No parallel tracker.
- **Exceptions:** for complex worktree handoff, submodule two-level pointer integration, frozen execution SHA or unusual ownership drift, read [execution details](references/detailed-execution-workflow.md#worktree-execution-tracking) only for the affected boundary.

## Execute the smallest validated path

Use the plan's current product surface, implementation host, required acceptance environment, actual owners and verified predecessor evidence. Do not reinterpret a web-browser pass as Windows-native proof, or let an available tool silently add a new platform/phase.

Implement the necessary change along the known call path, checking actual dependencies and real production seams. Expand repository discovery, architecture review, installation or test scope only after a demonstrated mismatch, changed contract, failing assertion, protected risk or unresolved owner makes expansion necessary. Prefer targeted source and concise diagnostic excerpts over full histories, graph indexing and repeated unchanged logs.

Apply [Verification Impact Analysis](../../docs/verification-impact-analysis-v1.md) proportionately: focused tests while coding; one goal-level integrated real-component/browser E2E when required, **after** the candidate is integration-ready. A bounded early UI smoke must answer an actual named risk. Preserve real tenant/security/financial/replay authority and domain correctness; mocks cannot prove substituted in-repo architecture. Rerun only failed or invalidated checks; reuse unchanged results after merge when equivalent.

## Continuous delivery and recovery

After each meaningful observation choose the next dependency-ready authorized step. A failure triggers the smallest diagnostic or repair/retest loop, not automatic human handoff or a duplicate test campaign. Do not repeatedly ask “should I continue?” Routine tool calls, tests and checkpoints need no ceremonial narration; communicate substantial independently useful progress, material risks, or blockers subject to host/user update rules.

If the next workflow state is genuinely ambiguous, read [workflow routing](references/workflow-routing.md) and load only its current-state owner; do not preload debugging, TDD, or verification together.

Only actual unavailable user-owned access, authorization, consequential external effect, or a materially unresolved choice after safe delegated recovery satisfies the **User Intervention Necessity Test** (`docs/mvl-laws.md`). A proven negative/inconclusive terminal is legitimate within its frozen predicate; do not claim it also proves the outer customer goal.

For nonroutine execution economics compare complete loop cost, not just tokens: reuse [execution economics](references/execution-economics.md) and [token-efficient policy](../using-superpowers/references/token-efficient-execution.md) only when needed. No automatic telemetry reporting, huge model/CDP traces or speculative performance claim; inaccessible token counts are UNKNOWN.

## Goal-preserving recovery — STOP has the burden of proof

**Keep the outcome and acceptance conditions fixed; let the implementation path change.** Distinguish four different dispositions instead of promoting a failed prerequisite into whole-goal failure:

- `PATH_FAILED` — one selected approach, tool, environment or prerequisite fails. Diagnose its actual mismatch and pursue the smallest other **authorized** route; Plan A/Plan B examples are not an exhaustive menu.
- `GATE_BLOCKED` — one required acceptance gate cannot currently pass without a protected external dependency. Preserve that gate as unverified and **continue dependency-independent, materially useful work** toward the same goal.
- `GOAL_BLOCKED` — the goal is still unverified **and** no remaining authorized, dependency-ready work can materially advance it; the exact missing external access, authority, credential or non-delegable decision is identified.
- `GOAL_VERIFIED` — the whole declared outcome, required real-path evidence and integration obligations are satisfied. A code change, test count or recovered route alone is not this state.

**Before declaring `GOAL_BLOCKED`, prove the stop condition rather than just listing failed paths.** Recheck the original goal and remaining gates; distinguish genuine financial/identity/provider limits from repairable engineering faults. Evaluate the smallest safe alternative within scope and the next independently executable gate (including source, authorization, delegated-tool and deterministic verification work when live provider access is absent). Perform that work if useful; do not ask for permission already delegated. If nothing remains, name the exact unavailable input, the alternatives ruled out, the independent work already completed or legitimately inapplicable, and the condition that would resume execution. Record this briefly in the **existing plan**, not a separate STOP dossier.

**Counterexample:** A model provider cannot be admitted, but a protected agent's delegated tool interface and idempotency can still be implemented and tested without model calls. The provider gate is `GATE_BLOCKED`; stopping the whole goal before that independent work is done is premature. This does **not** permit fabricated paid inference, model-selection traces, source evidence, credentials, funds, or bypassed security. Do not explore unlimited speculative alternatives: select bounded, outcome-relevant work, and respect real user-owned limits and explicitly terminal negative/research predicates.

## Completion transition (not an eager skill)

At the actual goal/merge/release boundary, use `verification-before-completion` only to resolve evidence sufficiency. Once implementation is ready and the authorized integration action is known, enter `finishing-a-development-branch` for integration and owned retirement, applying [plan integration and retirement](../finishing-a-development-branch/references/plan-integration-and-retirement.md). Preserve the plan's actual `execution_commit`/integrated SHA and any required parent/submodule gitlink. Do not rerun a satisfied E2E on a skill transition or create a second completion matrix.

For detailed exceptional branch/plan recovery, see [full execution workflow](references/detailed-execution-workflow.md); do not load it for an ordinary bounded task.
