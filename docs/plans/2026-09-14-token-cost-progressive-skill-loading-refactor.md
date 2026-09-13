# Token-Cost and Progressive Skill Loading Refactor Plan

**Status:** implementation-ready
**Target version:** 6.8.0
**Goal:** Reduce agent input-token cost, prefill latency, and instruction interference without weakening engineering invariants.

## Design principles

1. **Current-state loading, not eventual-relevance loading.** Load a workflow skill only when the agent enters the state governed by that skill.
2. **Replace, do not accumulate.** Debugging, TDD, and completion verification are sequential states; when one exits, its detailed workflow becomes inactive and the next skill receives only a compact handoff.
3. **Progressive disclosure.** Root `SKILL.md` files contain routing, invariants, entry/exit conditions, and stop conditions. Conditional detail, examples, platform rules, browser mechanics, and model compensation live in references.
4. **Prefix-cache-friendly static structure.** Keep stable routing and invariants short and structurally stable. Keep project/session-specific state out of static skill bodies.
5. **No duplicated contracts.** One skill owns each rule. Other skills reference the owner rather than restating the full rule.
6. **Deterministic enforcement over prompt repetition.** Version synchronization, packaging, and other mechanically checkable requirements remain scripts/tests rather than repeated prose.
7. **Compact tool/context handoff.** Pass root cause, intended behavior, affected surface, evidence, and unresolved material risks across states; do not carry whole prior skill bodies or verbose intermediate reports.
8. **Minimum sufficient verification.** Reuse valid unchanged evidence, choose verification by claim/impact radius, and avoid ceremonial reruns.
9. **Parallelize independent work, not dependent reasoning.** Parallel tool/subagent calls are useful when dependencies allow them; do not create extra agent turns solely to satisfy workflow ceremony.
10. **Short structured agent output by default.** Status and handoff records should be concise and machine-readable enough to avoid feeding large narrative reports back into later rounds.

## Progressive workflow contract

### DEBUGGING
Entry: unresolved bug, failed test, unexpected behavior, performance anomaly, or unexplained failure.
Exit: root cause and affected behavior are sufficiently established, or the task ends as diagnosis-only.
Replacement: diagnosis-only -> report; authorized change -> TDD; correctness claim without code change -> verification.

### TDD
Entry: authorized production behavior change, bug fix, or behavior-preserving refactor with sufficiently defined intended behavior/preservation contract.
Exit: focused behavior evidence is green and the implementation is ready for broader completion/integration claims.
Replacement: new unexplained evidence -> debugging; implementation complete enough to claim -> verification.

### VERIFICATION
Entry: an agent is about to claim fixed/correct/complete/integrated/ready-to-merge/release, or a consequential action depends on that claim.
Exit: claim supported, falsified, or scoped down.
Replacement: unexplained defect -> debugging; known implementation gap -> TDD; supported claim -> integration/final report.

At most one of these three skills should govern the current reasoning state except for a brief transition handoff.

## Workstreams

### W1 — Native matcher first; retire mandatory meta-routing
- Do not require `using-superpowers` as a conversation-start or first-hop dispatcher on platforms that already provide native skill discovery/matching.
- Encode mutually exclusive activation conditions directly in each skill frontmatter description so the harness can select the current workflow state without an extra routing skill.
- Retain `using-superpowers` only as a compact compatibility/reference skill for cross-cutting Livingware principles; its description must explicitly say not to load it merely to route ordinary tasks.
- Keep codebase-memory/worktree graph mechanics behind platform/reference guidance instead of an always-loaded routing surface.
- Keep the progressive-loading reference as the canonical state-transition contract for harnesses or adapters that need explicit guidance.

### W2 — Debugging becomes evidence-localization contract
- Keep reproduce -> evidence -> localize -> hypothesis -> falsify -> root cause.
- Remove repeated TDD/completion rules from the root body.
- Keep specialized techniques in existing reference files and load them only when triggered.
- Explicitly exit to a compact handoff rather than carrying the debugging body forward.

### W3 — TDD becomes implementation-test contract
- Keep changed-behavior RED/GREEN and preservation-baseline semantics.
- Keep real-component and real-browser requirements as concise invariants.
- Route detailed browser lifecycle, impact radius, and good-test examples to existing references.
- Do not preload completion verification.

### W4 — Verification becomes claim/evidence contract
- Keep claim -> falsifier -> observed/current evidence -> scoped claim.
- Remove duplicated browser/MVL explanations where another contract owns them; reference them conditionally.
- Explicitly transition back to debugging or TDD based on failure type.

### W5 — Planning and execution stop duplicating downstream contracts
- `writing-plans`: retain plan fields and ownership boundaries; reference testing/verification contracts instead of teaching them again.
- `executing-plans`: treat the approved plan as authoritative dynamic context; load TDD/debugging/verification only when their entry conditions are reached.
- Do not copy MVL/dependency/integration contracts into separate ledgers during execution.

### W6 — Brainstorming progressive disclosure
- Keep spike/bounded/architectural classification and build/reuse/adopt decision at root.
- Keep visual companion, dependency-depth checklists, examples, and scaffolding behind references/triggered reads.
- Do not activate planning or implementation skills until the architectural/bounded path reaches that state.

### W7 — Token-cost regression checks and documentation
- Record before/after byte counts for core skill bodies as a rough static proxy; token/runtime providers may tokenize differently.
- Verify no required skill file becomes empty or loses frontmatter.
- Run existing plugin/version tests.
- Bump all declared manifests to 6.8.0 with the repository version script.
- Update release notes with progressive loading, instruction deduplication, and prefix-cache-friendly structure.

## Acceptance criteria

- Native skill matching is the preferred dispatcher; `using-superpowers` is not a mandatory first-hop skill and explicitly says not to load it merely for routing.
- Debugging, TDD, and verification each define entry, exit, and replacement behavior.
- The three skills no longer require simultaneous loading for an ordinary bug-fix path.
- Detailed browser, impact-radius, codebase-index, and examples remain available by progressive disclosure.
- Planning/execution reference authoritative contracts instead of replicating them.
- No correctness, security, authority, destructive-operation, real-component integration, or real-browser UI invariant is removed.
- Core selected-skill static text is materially smaller than 6.7.0.
- Version manifests are synchronized at 6.8.0 and repository tests relevant to packaging/versioning pass.

## Non-goals

- Changing product governance semantics.
- Weakening TDD, root-cause, real-component, or browser evidence requirements.
- Introducing runtime token accounting tied to one model/provider.
- Rewriting unrelated frontend/design/system-dynamics skills.
