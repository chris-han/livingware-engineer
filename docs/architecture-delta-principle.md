# Architecture Delta Principle

**Status:** normative policy / invariant  
**Version:** 1.0  
**Date:** 2026-09-16

## Purpose

Architecture work begins by proving what must change, not by assuming that a new design is required. In an existing system, a proposed architecture change is admissible only when current evidence establishes a bounded difference between the required architectural properties and the observed architecture.

```text
Observed architecture + required properties
  -> semantic comparison
  -> verified architecture delta
  -> minimal candidate change
  -> verification evidence
```

This policy prevents architecture-by-assumption, duplicate capabilities, technology-driven rewrites, stale-state refactors, and attractive changes outside the actual requirement.

## Core invariant

Let `A_observed` be the architecture reconstructed from current admissible evidence and `A_required` the minimum architectural properties required by the declared outcome and constraints.

```text
Delta_A = A_required - A_observed
ProposedChange subset-of Resolve(Verified(Delta_A))
```

Four rules are normative:

1. **Evidence before delta.** A current-state claim must be supported by current repository/runtime/contract evidence relevant to the task.
2. **Unknown is not missing.** `UNKNOWN` creates an investigation obligation, never an implementation obligation.
3. **Empty delta stops change.** `Delta_A = empty` yields `NO_CHANGE_REQUIRED`; do not manufacture a refactor.
4. **Closure requires evidence.** Changed code does not close a delta; the declared closing condition must be verified.

## Applicability

Run an Architecture Delta Probe before proposing an architecture-affecting change in an existing project: new or replaced subsystems, services, stores, contracts, interfaces, ownership boundaries, cross-component data flows, runtime responsibilities, or structural refactors.

A bounded implementation that does not change architecture may record `NOT_APPLICABLE`. A greenfield project can have an empty observed implementation, but the probe must still separate required properties from preferred implementation mechanisms and confirm that an equivalent owned capability does not already exist in the repository or platform context.

## Required inputs

The probe requires the smallest sufficient evidence set, not a whole-repository audit:

- **Intent** — desired outcome, scope, success conditions, and material non-goals, expressed independently of a chosen technology or implementation.
- **Observed architecture** — current relevant capabilities, contracts, boundaries, runtime paths, and constraints reconstructed from code, tests, configuration, schemas/contracts, accepted architecture records, and runtime evidence where material.
- **Required properties** — minimum architectural properties necessary to satisfy the intent and binding invariants.
- **Evidence basis** — exact current sources supporting the observed-state claims, with revision/freshness when material.
- **Existing invariants** — contracts, authority boundaries, compatibility requirements, and other properties the change must preserve unless explicitly superseded.

Prefer executable/current evidence over descriptive or historical text when they conflict. A stale document can identify an investigation target but cannot establish current implementation state by itself.

## Architecture Delta Probe

For each required property, classify the observed state as exactly one of:

```text
SATISFIED
PARTIAL
UNSATISFIED
UNKNOWN
CONFLICTING
```

Only `PARTIAL` and `UNSATISFIED` create delta items.

- `SATISFIED` — existing semantics already meet the property; no architecture change is justified for that property.
- `PARTIAL` — some required semantics exist; the delta contains only the missing portion.
- `UNSATISFIED` — admissible evidence establishes that the required property is absent.
- `UNKNOWN` — evidence is insufficient; investigate before designing a change.
- `CONFLICTING` — current evidence disagrees materially; reconcile or refresh the working context before designing a change.

Different implementation technology, naming, package structure, or storage mechanism is not itself a delta when the existing implementation satisfies the required semantics and constraints.

## Minimal delta record

Keep the record proportional to the work. It may live in the design/spec rather than a separate artifact.

```text
Architecture Delta Review
Intent: <solution-independent outcome>
Evidence basis: <current code/contracts/tests/runtime/docs used>
Observed architecture: <relevant current capability/boundary>
Required properties:
  R1 <property> -> SATISFIED | PARTIAL | UNSATISFIED | UNKNOWN | CONFLICTING
Verified delta: <only PARTIAL/UNSATISFIED gaps>
Scope fence / does not change: <existing owners and boundaries preserved>
Closing evidence: <observable proof for each delta item>
Disposition: <one value below>
```

Allowed dispositions:

```text
PROCEED_WITH_DELTA
NO_CHANGE_REQUIRED
INVESTIGATE_UNKNOWN
REFRESH_CONTEXT
REDUCE_SCOPE
CONFLICTING_EVIDENCE
NOT_APPLICABLE
```

Only `PROCEED_WITH_DELTA` permits architecture-changing implementation work. `NOT_APPLICABLE` permits ordinary non-architecture work to continue. `NO_CHANGE_REQUIRED` is a successful terminal result, not a failed design exercise.

## Admissibility checks

Before `PROCEED_WITH_DELTA`, all of the following must hold:

1. current-state evidence is sufficient and fresh for the affected architecture surface;
2. intent is separable from the proposed solution;
3. every required property has a classification;
4. no `UNKNOWN` or unresolved `CONFLICTING` property is represented as a missing capability;
5. the delta is non-empty;
6. every proposed change resolves at least one verified delta item;
7. every delta item has an observable closing condition;
8. existing invariants are preserved or explicitly superseded by the governing requirement;
9. the proposed scope does not exceed the smallest evidence-supported change envelope.

If a nearby cleanup, abstraction, dependency replacement, or refactor does not satisfy a delta item or block its closure, classify it as follow-up debt rather than expanding the current architecture change.

## Failure cases

- **Architecture by assumption** — design begins before current-state reconstruction.
- **Duplicate capability** — a new subsystem duplicates an existing semantically adequate owner.
- **Technology-driven delta** — a preferred database/framework/package is treated as a requirement without an unmet property that demands it.
- **Stale-state delta** — the gap existed historically but current implementation already closed it.
- **Unknown presented as missing** — absence of evidence is turned into implementation work.
- **Over-delta refactor** — a bounded gap is used to justify a broader rewrite.
- **Zero-delta work** — the system already satisfies the requirement but work continues for activity's sake.

## Relationship to other Livingware contracts

Architecture Delta answers **what must change**. It precedes Engineering/Verification Impact Analysis, which answers **what may be affected and what evidence is sufficient to falsify the implementation claim**. IA-before-UI remains a specialization for user-facing information architecture and runs when the verified delta includes a material UI/IA change.

```text
Working context / current evidence
  -> Architecture Delta Probe
  -> minimal candidate change
  -> impact analysis
  -> implementation
  -> verification
  -> delta closure
```

The probe is a machine-verifiable structural gate, not a default human-approval checkpoint. Reuse current Working Context and repository evidence; do not introduce a new durable ledger, architecture service, or mandatory whole-repository scan merely to implement this policy.
