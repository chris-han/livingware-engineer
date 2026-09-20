---
name: using-superpowers
description: Reference for Livingware-wide engineering principles and compatibility on harnesses that need explicit routing guidance. Do not load merely to route ordinary tasks when native skill matching is available.
---

# Livingware Core Principles

Prefer the platform's native skill discovery and matching. Skills should be selected directly from precise frontmatter descriptions; this skill is not a mandatory first hop.

## Minimum Sufficient Engineering

Choose the smallest change, context, verification surface, and review process that satisfies the request. Reuse existing code, contracts, tests, evidence, and recovery state. Preserve correctness, security, authority, permissions, data integrity, required audit semantics, and explicit repository requirements.

Safe reversible in-scope work continues without repeated approval. Stop only for missing authority, material unresolved design choices, security risk, destructive operations, or irreversible external actions that require human judgment.

## Evidence Reuse Discipline

Evidence is temporal and contract-bound. A result reported now must not be assumed to have been produced under the current acceptance or evaluation contract. Before reusing prior test, benchmark, qualification, or experiment evidence, bind it to the actual production context: production time when available, artifact/result hash, governing contract or plan version/hash, and the relevant code, configuration, fixture, model, dependency, and environment identities.

If the governing contract changed after the evidence was produced, classify reuse as `EXACT_REUSE`, `PARTIAL_REUSE`, or `STALE`. Reuse only the claims still established by unchanged semantics. Newly introduced or strengthened requirements remain unverified until directly supported. Reporting time is not production time, and a later summary is not a substitute for inspecting available source evidence when chronology or contract identity affects the claim.

## Progressive Loading

Load a workflow skill only when its own entry condition is satisfied. Do not preload downstream skills because they may become relevant later. Debugging, TDD, and verification are sequential states, not a bundle. When a state exits, pass a compact handoff and stop consulting or restating its detailed instructions.

Read [Progressive Skill Loading](references/progressive-skill-loading.md) only when an adapter or workflow transition needs explicit state guidance.

## Context Cost Discipline

Keep stable instructions short and structurally stable for prefix caching. Keep session-specific state in compact handoffs. Prefer focused tool output, reusable evidence, and deterministic checks over repeated prose. Parallelize independent work when useful; do not add agent turns solely for ceremony.

Platform-specific tool mapping and codebase-index mechanics belong in the matching reference adapter, not this core skill.

## Precedence

User and repository instructions take precedence over these defaults.
