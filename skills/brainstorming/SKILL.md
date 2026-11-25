---
name: brainstorming
description: Use when a software/project discussion needs design decisions about behavior, architecture, contracts, interfaces, services, stores, or subsystems, including when a conceptual discussion starts proposing code-level structure in an existing repo. Do not use for purely conceptual research with no project design decision.
---

# Brainstorming — Design Decisions

**Enter** only when product/software behavior, architecture, interface, contract or ownership still needs design judgment. Pure conceptual research belongs to its research owner. **Exit** with the minimal approved design/spec, a `NO_CHANGE_REQUIRED` conclusion, a bounded feasibility answer, or a specific user-owned decision that blocks safe action. Do not preload planning, implementation, or verification skills while design is unresolved.

## Choose the smallest path

- **Spike:** answer a feasibility question using a bounded, safe probe; output is a finding, not durable implementation. No new plan or spec.
- **Bounded change:** inspect the existing owner/flow, state a brief reversible approach, then continue authorized work using the engineering workflow. No ceremonial design approval, new plan document, or repeated interview.
- **Architectural decision:** for new systems or material cross-owner/contract changes, inspect the observed repository first. Apply `docs/architecture-delta-principle.md` and classify the required properties as `SATISFIED | PARTIAL | UNSATISFIED | UNKNOWN | CONFLICTING`. Only evidenced PARTIAL/UNSATISFIED creates an implementation delta; UNKNOWN triggers targeted inspection; an empty delta means `NO_CHANGE_REQUIRED`. Present alternatives, resolve the consequential choice, then preserve the accepted design at the repository's authoritative spec owner. Use [detailed design workflow](references/detailed-design-workflow.md) only if the architectural path needs its examples, review rubric, or additional process.

**Authorization:** an explicit fully specified reversible request already authorizes its bounded implementation. Ask only for material unresolved design choice, expanded authority/scope, destructive or irreversible action, or a real protected boundary not covered by standing delegation. Approval to inspect/spike is not approval to ship speculative code. Low-risk exploration stays default-pass.

## Context, requirements and design economy

Use the current goal and nearest current implementation/requirements source, not a repository-wide census by default. For material requirements ambiguity/conflict use [shared requirements contract](../requirements-clarification/references/requirements-workflow.md); do not repeat settled questions. Once a conversation turns into concrete code-level architecture, check actual source and contracts before proposing an alternative.

For every meaningful proposed capability choose the least costly fitting option: **not build → reuse existing code → native/standard platform → existing dependency → qualified mature dependency → minimal custom implementation**. New dependencies need actual contract/owner, pinning, smoke checks and maintenance rationale. Preserve existing trust and product semantics. Before proposing additional hardening, edge-case handling or future-proofing, identify the binding requirement or credible failure on the intended path and check whether an existing control already covers it. Prefer the least costly adequate treatment; omit speculative extensions. Prevent credible threats at real trust boundaries without requiring a prior incident; do not weaken binding security, integrity, or correctness. No separate risk matrix for ordinary changes.

If the current design materially changes UI task/IA, apply `docs/ia-before-ui.md` and enter `frontend-design` only for the relevant IA/craft phase. Reuse established IA for an unchanged-IA visual or deterministic fix. Preserve JTBD, cognitive-work allocation, semantic owner, task states/recovery and actual design authority; do not load unrelated visual playbooks.

## Design deliverable and transition

For a material architectural change, record the **user-visible goal**, verified architecture delta, unchanged owners/boundaries, alternatives/reuse decision, chosen contract, risk and observable closing evidence in the existing spec (default `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` unless repository policy differs). Obtain explicit approval only for a real material decision or newly changed approved scope. Run one concise spec consistency check; do not create a second evidence/approval ledger.

**Stop this skill when design is settled.** Then enter `writing-plans` only if a multi-step implementation plan is genuinely required; a bounded reversible edit may proceed directly through focused engineering checks. The next skill is selected by current state, not preloaded. No auto-issued planning approval, UI critique, or final verification during brainstorming.
