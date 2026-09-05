---
name: livingware-ia-modeling
description: Use when modeling institutional domains, ContextGraphs, ontology/schema candidates, graph projections, policy or legal knowledge, or other semantic graphs where definitions, occurrences, constraints, evidence, authority, and evaluation must remain distinct.
---

# Livingware IA Modeling

## Overview

Use a SysML v2-inspired semantic modeling discipline to construct governed semantic graphs and ContextGraphs without turning them into arbitrary entity-edge graphs. Here, IA means **Institutional Architecture**.

SysML v2 is a modeling reference, not the canonical ontology, runtime representation, or authority source. Preserve the host system's evidence, authority, governance, temporal, and evaluation contracts.

## Core Principle

Model **what a thing means** separately from **where it occurs**, and model **what is observed** separately from **what is concluded**.

```text
Definition -> Usage / Occurrence -> Evidence -> Evaluation
                   |                    |
                   +---- Authority -----+
```

A graph edge is not automatically a fact, rule, or compliance conclusion.

## Modeling Workflow

1. **Identify definitions first.** Extract reusable semantic types: entities, events, relationships, claims, requirements, constraints, evidence classes, and projections.
2. **Identify usages or occurrences.** Instantiate definitions only when the source describes a concrete actor, event, document, state, case, or runtime situation.
3. **Type relationships by semantic family.** Prefer a small stable relation kernel over LLM-invented predicates.
4. **Reify constraints and requirements.** If meaning depends on scope, conditions, exceptions, qualifications, precedence, or time, represent it as a structured semantic object instead of a simple edge.
5. **Separate observation from claim.** Observations become evidence candidates; they do not become institutional truth merely because they were retrieved or extracted.
6. **Attach authority independently.** Semantic Tier, jurisdiction, source role, governance state, and effectivity constrain how a semantic object may be used; topology does not grant authority.
7. **Represent evaluated conclusions as outputs.** Compliance, satisfaction, violation, eligibility, risk, and projection results are derived claims with lineage, not primitive relationships.
8. **Preserve provenance and versioning.** Every admitted semantic object that can influence evaluation should remain traceable to source anchors and governed versions.

## Semantic Kernel

Prefer these abstract families before inventing domain-specific structures:

- `Definition`: Entity, Event, Relationship, Claim, Requirement, Constraint, Evidence, Projection.
- `Usage/Occurrence`: concrete instance, event occurrence, claim instance, constraint application, evidence item, projection result.
- `Feature`: typed property, role, value, state, interface, participation slot.
- `Relationship`: specialization, composition, reference, participation, dependency, allocation, succession, support, derivation.

Domain predicates should specialize these families rather than create an unconstrained relation vocabulary.

## Hard Invariants

- Do not collapse definition and instance graphs.
- Do not encode a conditional rule as `A -> REQUIRES -> B` when scope, exception, qualification, or time materially affects meaning.
- Do not encode `SATISFIED_BY`, `COMPLIANT_WITH`, `VIOLATES`, `ELIGIBLE_FOR`, or similar evaluated conclusions as source facts unless the source itself explicitly asserts that conclusion and its authority is preserved.
- Do not infer institutional authority from graph position, centrality, retrieval rank, confidence, or model output.
- Do not let retrieval memory, LLM extraction, or a SysML-inspired structure bypass the host system’s governance boundary.
- Do not make SysML v2 a runtime dependency unless a separate architecture decision explicitly requires it.

## Output Contract

For each modeling task, produce enough structure to answer:

1. What are the reusable definitions?
2. What are the concrete usages or occurrences?
3. Which relationships are structural versus behavioral versus normative versus evidential?
4. Which conditions, exceptions, scopes, qualifications, and temporal rules must be reified?
5. What evidence supports each claim?
6. What authority and governance state applies?
7. Which conclusions are derived only during evaluation?

If any answer is unclear, mark it as an unresolved modeling question rather than hiding the ambiguity in an edge label.

For the detailed relation families, reference patterns, and examples, read `references/sysml-inspired-kernel.md`.

## Common Mistakes

**Triple-first modeling:** extracting nouns and verbs directly into nodes and edges. Fix by identifying definitions and occurrences before relations.

**Conclusion-as-edge:** writing `Requirement -> SATISFIED_BY -> Component`. Fix by modeling implementation, evidence, and an evaluation result separately.

**Authority-through-topology:** treating a legal source and a user suggestion as equivalent graph neighbors. Fix by attaching independent authority metadata and precedence rules.

**LLM predicate explosion:** generating dozens of near-synonymous relation names. Fix by specializing a small relation family and preserving domain language as labels or metadata.
