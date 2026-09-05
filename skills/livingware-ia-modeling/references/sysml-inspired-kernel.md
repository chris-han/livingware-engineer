# SysML v2-Inspired Semantic Kernel for Livingware IA Modeling

This reference explains how to borrow selected SysML v2 modeling ideas without making SysML the host runtime model.

## 1. Reference Boundary

Use SysML v2 as a semantic modeling discipline for:

- definition versus usage/occurrence separation,
- specialization and typed feature modeling,
- explicit relationship semantics,
- requirement and constraint reification,
- behavioral participation and succession,
- viewpoint-aware projection of a richer semantic model.

Do not import SysML concepts mechanically into every domain. A tax rule is not a `Part`, a legal exception is not a `Port`, and an accounting event is not automatically a SysML `Action`. Preserve domain semantics and use SysML only as a metamodeling guide.

## 2. Definition / Usage Separation

A definition answers what kind of thing something is. A usage or occurrence answers where that meaning is instantiated.

Example:

```text
PurchaseEventDef
EmployeeDef
ProjectDef
EmergencyExceptionDef
InvoiceDef

purchase_471 : PurchaseEventDef
employee_18  : EmployeeDef
project_33   : ProjectDef
exception_7  : EmergencyExceptionDef
invoice_92   : InvoiceDef
```

Do not create a new semantic type merely because a document mentions a new individual. Do not create an occurrence when the source is describing a general rule or reusable concept.

## 3. Relation Families

Use a bounded relation kernel. Domain predicates may specialize these families.

### Structural

- `specializes`: one definition refines another.
- `composes`: a whole owns a semantically meaningful part.
- `references`: one object points to another without ownership.
- `has_feature`: a definition or occurrence exposes a typed property or role.

### Participation and behavior

- `participates_in`: an entity plays a role in an event or activity.
- `has_role`: names that participation role, such as buyer, approver, recipient, issuer.
- `precedes` / `succeeds`: temporal or behavioral ordering.
- `transitions_to`: state transition when state semantics are explicit.
- `allocated_to`: assigns a responsibility, capability, function, or requirement to a carrier.

### Normative

Normative relationships usually require a reified object rather than a direct edge.

- `governs`: an authority artifact governs a semantic scope.
- `applies_to`: a requirement or constraint applies to a defined or instantiated scope.
- `constrains`: a constraint limits a feature, event, state, or action.
- `requires_evidence`: an obligation requires a specific evidence class or evidence condition.
- `has_exception`: links a rule to a structured exception definition.
- `has_qualification`: links a rule to an additional qualification.

### Evidential and derivational

- `supports`: evidence supports a claim.
- `contradicts`: evidence or a governed claim contradicts another claim.
- `derived_from`: a claim or projection is derived from one or more inputs.
- `observed_as`: an occurrence or state is represented by an observation or evidence item.

Avoid using evidential edges to imply institutional authority.

## 4. Reify Rules That Carry Logic

A simple triple is insufficient when meaning depends on any of these:

- scope,
- condition,
- exception,
- qualification,
- precedence,
- cardinality,
- temporal interval,
- threshold,
- jurisdiction,
- authority role.

Instead of:

```text
Employee --MAY_PURCHASE_BEFORE_CONTRACT--> Material
```

prefer:

```text
RequirementDefinition: PreContractEmergencyPurchase
  subject_role       -> Employee
  action             -> PurchaseProjectMaterial
  temporal_condition -> BeforeContractSignature
  permission_condition -> ApprovedEmergencyException
  evidence_requirement -> Invoice
  exception_effectivity -> 30 days
```

A concrete case then becomes a requirement usage or constraint application over occurrences.

## 5. Observation, Evidence, Claim, Evaluation

Keep these distinct:

```text
Observation
  raw or normalized statement about a source or world state

EvidenceCandidate
  observation with enough provenance to be considered for admission

Evidence
  admitted evidential object with source/provenance and bounded use

Claim
  proposition asserted by a source, user, agent, or governed artifact

EvaluationResult
  derived claim produced by applying governed semantics to evidence and state
```

Example:

```text
invoice_92 exists                     -> observation
invoice_92 anchored to source record  -> evidence candidate
invoice_92 admitted for purchase_471  -> evidence
purchase_471 has valid invoice        -> claim
purchase_471 satisfies evidence rule  -> evaluation result
```

Do not collapse this chain into one `HAS_INVOICE=true` property when provenance and admissibility matter.

## 6. Authority Is Orthogonal to Topology

Every normative or interpretive object should be able to carry independent authority metadata such as:

```yaml
authority:
  semantic_tier: T2 | T3 | T4 | T5 | T6
  jurisdiction: string | null
  authority_role: binding | interpretive | empirical | suggestion
  governance_state: proposed | validated | approved | active | deprecated
  effective_from: date | null
  effective_to: date | null
  source_refs: []
```

A T2 regulation and a T6 agent suggestion can both refer to the same `PurchaseEventDef`; that shared topology does not make them equal in authority.

## 7. Evaluation Is a Projection Over Governed State

Do not pre-store evaluated relations as if they were stable world facts.

Avoid:

```text
Requirement --SATISFIED_BY--> Component
Rule --VIOLATED_BY--> Event
Person --ELIGIBLE_FOR--> Benefit
```

Prefer:

```text
EvaluationResult
  evaluated_subject -> occurrence or scope
  evaluated_against -> requirement / constraint / projection definition
  evidence_refs     -> admitted evidence
  result            -> satisfied | violated | eligible | ineligible | indeterminate
  semantic_pins     -> governed versions
  justification_ref -> explanation / proof trace
```

This preserves replay when requirements, evidence, or semantic versions change.

## 8. Graph Views Are Projections, Not Separate Truths

A rich semantic model may support multiple ContextGraph views:

- `GRAPH`: definitions, usages, features, relations.
- `EVIDENCE`: observations, evidence, source anchors, support chains.
- `LINEAGE`: extraction, admission, derivation, supersession, replay pins.
- `COMPARE`: definition/version/candidate differences.
- `EVALUATE`: constraints applied to occurrences and evidence.

Do not duplicate truth into five independent graphs. Treat them as governed projections over common canonical semantic objects.

## 9. Modeling Checklist

Before accepting a graph candidate, verify:

1. Definitions and occurrences are separated.
2. Relation names belong to a stable semantic family or explicitly specialize one.
3. Conditional and temporal logic is reified rather than hidden in edge labels.
4. Evidence has provenance and is not synonymous with a claim.
5. Authority metadata is independent of graph topology.
6. Evaluation conclusions are derived outputs.
7. Unknown semantics remain explicit rather than being guessed into the model.
8. The representation remains usable without a SysML runtime dependency.
