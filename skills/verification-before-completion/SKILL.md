---
name: verification-before-completion
description: Use only when a correctness, completion, integration, merge, or release claim is imminent and needs current evidence. For bounded/local claims, use existing focused evidence directly; do not also activate codebase-memory or repository-graph discovery. Do not preload during diagnosis or implementation.
---

# Verification Before Completion

## Lifecycle

Entry: a correctness, completion, integration, merge, or release claim is imminent.
Exit: the claim is supported, falsified, or narrowed to what the evidence establishes.
An unexplained failure returns to debugging; a known implementation gap returns to implementation/TDD. Do not keep verification active during ordinary implementation loops.

## Core Contract

Before making a claim:

1. Name the exact scope of the claim.
2. Apply `docs/verification-impact-analysis-v1.md`: identify the observed production impact radius and the smallest verification surface capable of falsifying the claim.
3. Run that check, or reuse an observed result only when the relevant code, tests, dependencies, configuration, fixtures, and environment are unchanged.
4. Read the actual result and state only what it establishes.

A focused pass is not a full-suite or integrated pass. Architectural claims require real-component evidence through the affected production path. Frontend completion requires affected real-browser evidence. A declared MVL is complete only when its own stopping criterion is satisfied; do not invent MVL requirements for work that has none.

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

- Use `../test-driven-development/impact-radius-testing.md` when the verification radius is uncertain.
- Use `../test-driven-development/remote-cdp-browser-lifecycle.md` only for browser-render/interaction claims.
- Use the plan's MVL contract only when the plan explicitly declares one.
- Load `references/detailed-playbook.md` only for complex, high-risk, delegated, architectural, or release claims where the compact contract is insufficient.

Evidence decides the claim; verification is not a reason to generate extra reports or stop for approval when no human judgment is required.
