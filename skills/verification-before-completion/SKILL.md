---
name: verification-before-completion
description: Use only when a correctness, completion, integration, merge, or release claim is imminent and needs current evidence. For bounded/local claims, use existing focused evidence directly; do not also activate codebase-memory or repository-graph discovery. Do not preload during diagnosis or implementation.
---

# Verification Before Completion

## Lifecycle

Entry: a correctness, completion, integration, merge, or release claim is imminent.
Exit: the claim is supported, falsified, or narrowed to what the evidence establishes.
If evidence reveals an unexplained failure or a known implementation gap, exit this workflow and hand off only the compact state needed by the next appropriate workflow. Do not keep verification active during ordinary implementation loops.

## Core Contract

Before making a claim:

1. Name the exact scope of the claim.
2. Apply `docs/verification-impact-analysis-v1.md`: identify the observed production impact radius and the smallest verification surface capable of falsifying the claim.
3. Run that check, or reuse an observed result only when the relevant code, tests, dependencies, configuration, fixtures, and environment are unchanged.
4. Read the actual result and state only what it establishes.

A focused pass is not a full-suite or integrated pass. Architectural claims require real-component evidence through the affected production path. Frontend completion requires affected real-browser evidence. A declared MVL is complete only when its own stopping criterion is satisfied; do not invent MVL requirements for work that has none.

## Plan completion gate

For a plan or declared acceptance contract, passing commands is necessary evidence, not proof that the contract was exercised. Before changing completion state:

1. Read the original acceptance requirements, including referenced specifications and deliverables. Map each requirement to current evidence and the specific assertion or reviewed artifact that proves it; classify it as proved, failed, or unverified. Use the existing plan/work log when recovery requires persistence, not a second ledger.
2. Inspect the evidence's meaning: fixture, exact inputs, assertions, forbidden substitutions, repeat counts, benchmark baseline, and thresholds must match the requirement. Test names, green summaries, and metadata validators cannot establish coverage by themselves.
3. For a required connected journey, verify its transitions through the real components on the required shared state, including restart/reopen when specified. Separate passing tests of disconnected pieces do not prove the journey. Classify tests by the boundaries they exercise, not their directory or filename; reuse valid integration evidence without rerunning by ceremony.
4. Any failed or unverified requirement keeps the plan and goal incomplete. Continue authorized work or report the exact external blocker; do not narrow the stopping criterion to the implemented subset.
5. Only after every requirement is proved, update plan/goal completion status and archive or hand off as required. Run lifecycle checks on that final metadata. Never mark complete merely to satisfy a checker. If an earlier completion claim is disproved, retract it and restore available status surfaces to incomplete before continuing; report any status the host cannot reopen.

Governance hashes and review bindings attest to review; refreshing them does not perform it. Inspect each affected document against its changed sources before refreshing only those reviewed bindings. Do not refresh unrelated bindings merely to make a global check green.

## Verification Impact Analysis

Use the existing impact-radius classes rather than escalating by habit:

- `R0` local behavior -> focused behavior evidence
- `R1` one production seam -> focused integration
- `R2` multi-component path -> real-component integration
- `R3` user/UI/cross-process path -> vertical/E2E and affected real-browser evidence

Use broader suites when the impact or uncertainty is genuinely broad, not merely because a completion claim is being made. For expensive validation, preserve the cadence distinction in VIA: cheap deterministic invariants (`D0`), local semantic sentinels (`D1`), and broad semantic audits (`D2`).

## Tool Economy

Start from already-produced implementation evidence. For a bounded/local claim, do not activate codebase-memory, rediscover the repository, enumerate code-graph projects, reread unrelated history, or rerun broad checks merely for ceremony. Inspect the focused diff/state and execute only checks that can falsify the claim or whose prior evidence was invalidated.

Use broader graph/integration/browser discovery only when the claim itself crosses those boundaries or existing evidence cannot establish scope. When relationship-aware discovery is needed, prefer the available current code graph and targeted `codebase-memory-mcp` queries over whole-repository rereading.

## Progressive Disclosure

Keep auxiliary procedures behind the detailed playbook unless the current claim specifically requires them. Load `references/detailed-playbook.md` only for complex, high-risk, delegated, architectural, browser-specific, or release claims where the compact contract is insufficient. Use the plan's MVL contract only when the plan explicitly declares one.

Evidence decides the claim; verification is not a reason to generate extra reports or stop for approval when no human judgment is required.
