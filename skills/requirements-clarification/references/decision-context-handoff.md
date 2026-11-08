# Structured decision-context handoff

Use when a calling agent or host has an existing decision-context schema, typed contract or context-formation service. The [shared requirements workflow](requirements-workflow.md) owns discovery, source preservation, dispositions and sufficiency. This reference owns only the handoff guidance; the host owns its schema, state and authority.

## Separate conversation from the machine contract

Discuss goals, examples and ambiguities with the user in natural language. Incrementally map useful results into the existing owner's structured representation. A user need not learn the schema or fill a form.

1. Resolve the applicable contract, version, producer/validator and downstream consumer from authoritative source. Reuse that contract; do not invent a competing generic decision-context schema.
2. Preserve evidence/source references, accepted requirements, proposals, uncertainty and disagreement using supported fields or linked artifacts. Keep interpretation separate from source text. Do not invent ontology terms, field names, identifiers, hashes or approval states to make an object look complete.
3. Submit candidate inputs through the owner's supported formation path. Let that owner derive protected identity, provenance closure, scope and authority. Preserve its returned artifact/reference and exact version.
4. Validate structure with the actual owner validator when available, then separately check whether the context is sufficient for the named next decision. Passing schema validation does not establish factual correctness, completeness, admission or authority.
5. Hand the consuming agent the typed value or exact reference required by its contract. Clearly distinguish candidate, validated and operative states using the owner's vocabulary. Context preparation does not itself select, approve or commit a decision.

When an essential fact is unknown, use the contract's unknown/unresolved representation. If a material distinction cannot be represented or a required producer is unavailable, retain the useful candidate work at the existing owner, name the precise contract/capability gap, and avoid claiming an operative handoff. Continue independent in-scope work; do not manufacture a successful object or demand a second ledger.

Stop at the smallest context sufficient for the current bounded decision or learning step. This does not require eliminating every uncertainty; it does require retaining mandatory evidence, dependencies, conflicts and authority conditions for that step.

## Semantier binding: reuse the implemented owner

This is an optional source map for Semantier, not a dependency for other hosts. The source snapshot below was checked at commit `8868000bfc6d05e93c93e743cf78c72f1e0c46c3`; resolve the task's applicable current contract before use.

- Conceptual **Decision Context** is realized by `WorkingContext` in `src/contracts/semantic_kernel.py`, as specified by ADR-0027. Retain that type; the session-level `RuntimeTaskContext` family and transport payload are different owners.
- Relevant elicitation results first enter the existing evidence/context-formation path. A `PROPOSED ContextGraph` must follow the existing governed admission path before it can supply an operative `WorkingContext`.
- `WorkingContextProjectionService` projects from one exact admitted graph. Its reasoning path derives node/evidence closure, scope, responsibility and selection policy through the existing owner; the elicitation skill must not fabricate those values or infer authorization from conversational agreement.
- Decision intent is owned by `task_ref`, `task_goal` and `ContextGraph.intent`; world/time and institutional/physical/social assertions remain in their graph/ontology/evidence owners. Material uncertainty uses the existing intent/unresolved-question path. Do not add ad hoc culture, constraint or approval fields to `WorkingContext`.
- Deliver the actual returned value/reference with its identity when the supported path has run. A schema-shaped JSON draft, transcript or summary is not an admitted world or an operative projection. `DecisionRecord` remains a separate contract with its own purpose and authority requirements.

Authoritative source map:

- [ADR-0027: conceptual naming and authority boundaries](https://github.com/chris-han/semantier-runtime/blob/8868000bfc6d05e93c93e743cf78c72f1e0c46c3/docs/adr/ADR-0027-context-accessibility-ontology-and-runtime-naming-boundary.md)
- [WorkingContext and ContextGraph contracts](https://github.com/chris-han/semantier-runtime/blob/8868000bfc6d05e93c93e743cf78c72f1e0c46c3/src/contracts/semantic_kernel.py)
- [Working Context runtime contract](https://github.com/chris-han/semantier-runtime/blob/8868000bfc6d05e93c93e743cf78c72f1e0c46c3/docs/derived/working-context-runtime-contract-v1.md)
- [Existing projection service](https://github.com/chris-han/semantier-runtime/blob/8868000bfc6d05e93c93e743cf78c72f1e0c46c3/src/services/working_context_projection_service.py)

These links establish source ownership. This guidance does not establish that a particular harness exposes the producer, that a new conversation-ingestion adapter exists, or that end-to-end runtime behavior has been exercised.
