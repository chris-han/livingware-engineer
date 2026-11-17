# Discovery frontier and mandatory pre-experiment gate (conditional detail)

This reference belongs to the `research-methodology` root. Load it when starting or materially revising a maintained research program, nominating a new candidate, or drafting/promoting an experiment. For an already active governed experiment with frozen owner/basis, use the plan, not a repeat of the authoring gate.

## Research Discovery Kanban

Represent research as a derived epistemic graph:

```text
Design Goal
    |
    v
Uncertainty frontier
    |
    +-- U1 CLOSED
    +-- U2 FALSIFIED / RETIRED
    +-- U3 OPEN  <- active frontier
    |      |
    |      v
    |   Experiment
    |      |
    |      v
    |   Evidence-bound result
    |      |
    |      +-- closes U3
    |      +-- narrows U3
    |      +-- exposes one child uncertainty
    |      `-- inconclusive / stop
    |
    `-- U4 BLOCKED_BY U3
```

This graph is **derived state**, not a second authority system. Requirements, architecture/specs, experiment contracts, datasets, code, and terminal evidence keep their existing authoritative owners. The discovery map links to them and projects current epistemic state.

## Required uncertainty-node contract

Each live uncertainty should be representable as:

```yaml
uncertainty_id: U<n>
design_goal: <goal id / statement>
question: <one falsifiable or discriminating question>
why_it_matters: <decision blocked by this uncertainty>
state: OPEN | ACTIVE | BLOCKED | CLOSED | FALSIFIED | RETIRED | UNRESOLVED

competing_explanations:
  - <H1>
  - <H2>
  - ...

already_ruled_out:
  - <hypothesis + exact evidence/scope>

strongest_evidence:
  - <artifact / receipt / source>

owner: <current research owner>
dependencies:
  - <upstream uncertainty ids>

next_discriminating_action:
  type: literature | analysis | probe | experiment | evaluation
  question: <what observation distinguishes explanations?>

outcomes:
  <outcome-A>: <next uncertainty or STOP>
  <outcome-B>: <next uncertainty or STOP>

closure_condition: <evidence required to close this node>
```

Do not create a durable artifact when an existing roadmap/ledger can carry these fields. A project may use Markdown, JSON, issue metadata, a graph database, or another representation; the methodology specifies the semantics, not a storage format.

## MICE-style uncertainty decomposition

Before designing experiments, decompose the explanation space so branches are:

- **Mutually independent/distinguishable enough for the current decision** — do not collapse data quality, routing, representation, scorer/interface behavior, model capability, and policy effects into one "model problem."
- **Collectively explanatory enough** — cover the material alternatives that would lead to different design decisions; do not demand metaphysical completeness.
- **Intervention-friendly** — prefer branches that can be distinguished by changing one causal variable or one justified interaction.
- **Evidence-convergent** — every branch has an observable result capable of eliminating, retaining, or narrowing it.

This is a research decomposition rule, not a requirement that real-world causes be perfectly independent.

## Existing-evidence-first law

When research occurs inside a project with maintained research state, project evidence is the starting point, not optional background.

Before external discovery, model/tool recommendation, candidate nomination, benchmark comparison, or a new experiment proposal:

1. resolve the current owning roadmap/spec or other explicit research owner;
2. inventory directly relevant terminal reports, sealed results, memos/guides, active/stopped/superseded experiments, already-tested candidates, and protected/unopened evidence;
3. bind reused evidence to its production context and classify reuse as `EXACT_REUSE | PARTIAL_REUSE | STALE`;
4. state what the internal evidence already supports, rules out, or leaves unresolved;
5. only then use external literature, benchmarks, repositories, model cards, leaderboards, or OpenResearch-style discovery to fill a named residual evidence gap, challenge a retained hypothesis, or nominate a genuinely non-duplicative candidate.

The governing order is:

```text
current owner + existing project evidence
  -> current uncertainty / evidence gap
  -> external research targeted at that gap
  -> bounded candidate or hypothesis
  -> smallest discriminating experiment, or STOP
```

This is **internal evidence first, evidence quality always**. Project evidence is not privileged merely because it is local: stale, incomparable, exposed, or contract-invalid evidence must be downgraded explicitly. External evidence does not reset a maintained research program to a blank slate.

Every newly proposed candidate must state:

- **evidence gap addressed** — what material uncertainty remains after considering existing evidence;
- **non-duplication delta** — what this candidate can establish that current evidence/candidates cannot;
- **expected information gain** — which explanation or downstream decision can be eliminated, retained, or unlocked.

Novelty, popularity, leaderboard position, availability, or a new paper/repository is not by itself a valid research delta.

### Literature intake qualification

When an external paper is being considered for a maintained research program, do not equate topical relevance with research value. First qualify whether the paper can create a defensible change in the current research state: challenge or support an active hypothesis, introduce a materially new mechanism, change an experiment or gate, supply missing evidence, or alter the next research action. Use `references/literature-qualification.md` for the bounded `ResearchCatalystAssessment` contract and depth-of-reading policy. Use `references/scholar-catalyst-benchmark.md` only when evaluating or benchmarking this qualification behavior against ScholarCatalyst-style positive versus topical-hard-negative cases.

**Durable external-evidence retention is mandatory when literature changes project research state.** When external literature materially supports or changes a project hypothesis, taxonomy, roadmap claim, design/architecture rationale, or adopted principle, retain that evidence in the owning research memo/guide in the same research change. Record a stable bibliographic citation (at minimum author/title/year plus DOI or another durable source identifier when available), the exact premise the source supports, and explicit limits/non-claims. The owning roadmap, ADR, or equivalent decision record MUST link to that evidence owner; evidence must not exist only in chat, transient search results, or model memory. Keep `external evidence != project synthesis != validated hypothesis != adopted design/architecture law != authority transition`. Decision records should reference the evidence owner and state only the implications actually adopted rather than duplicating a literature review.

### Model-training intervention qualification

When parameter learning is being considered, do not infer `training required` from an observed model error or benchmark gap. First separate reference/evaluator validity, deterministic computability, representation/context sufficiency, readout/interface/numerical integrity, existing-system sufficiency, calibration, residual attribution, and training admissibility. Use `references/model-training-qualification.md` to choose the smallest non-training repair, bounded training candidate, learning-system candidate, or evidence-supported STOP, and to contract any eligible training design to a Residual Experimental Frontier before automated search.

### Harness, weight, and search intervention placement

When agent improvement could change evidence/context, execution scaffolding, weights, or exploration diversity, use `references/intervention-placement-and-search.md`. Diagnose evidence sufficiency, execution integrity, and residual content quality before choosing a lever; first failure signals and aggregate plateaus are not causal attribution. Use harness-by-weights cross-evaluation when claiming transfer into parameters. Keep fresh-context branching optional and budgeted within one owned experiment; do not enable automatic fan-out or a default Fork-and-Flush schedule without local evidence and existing authorization.

## Unified experiment execution

When an eligible action invokes training, inference, rollouts, evaluation, or sandbox execution, use `references/research-services.md` for a provider-independent service contract, scoped permissions, shared budget accounting, code-mediated result reduction, evidence visibility, and optional RSI-Index reporting. Reuse host adapters and existing experiment records; load only the capabilities and schemas required by the current action.

The skill selects and interprets the experiment; the host execution boundary enforces each call. A documented interface does not prove service availability, budget enforcement, complete evidence inspection, or resumable approval. Improved scores remain evidence, not admission or activation authority.

## Start-of-thread protocol

Before opening a new research thread or experiment:

1. Resolve the current design goal and current research owner from the nearest authoritative roadmap/spec.
2. Load the current discovery context:
   - closed uncertainties;
   - falsified/retired hypotheses;
   - active/open uncertainties;
   - blocked downstream questions;
   - protected/unopened evidence;
   - active experiments and owners;
   - directly relevant terminal/sealed evidence and already-tested candidates.
3. Complete the existing-evidence-first census before substantive external discovery.
4. Identify exactly one primary uncertainty this thread addresses.
5. Search for existing current, archived, or parallel work that already owns or resolved it.
6. Bind reused evidence to its production context. Classify reuse as `EXACT_REUSE | PARTIAL_REUSE | STALE` when contracts changed.
7. For every new candidate, state the evidence gap addressed, non-duplication delta, and expected information gain.
8. If no new information delta exists, stop instead of reopening work.

A new conversation is not a new research program. Cross-thread state belongs to the shared discovery graph.

## Mandatory pre-experiment context gate

Before drafting, creating, promoting, or authorizing any new research or experiment plan, reload the maintained research state even if it was already read earlier in the same thread.

The gate MUST reload and re-read:

1. the current owning roadmap/spec or other explicit research owner;
2. the latest directly relevant research memo or guide that may have changed the framing;
3. the latest terminal reports and sealed results that could change the active frontier;
4. the already-tested candidate/model/tool census, including negative and superseded results;
5. the currently active uncertainty node, including its competing explanations, dependencies, and closure condition.

Then restate the smallest sufficient context before plan drafting:

```text
Pre-experiment context gate:
Owner:
Roadmap:
Latest memo / guide:
Terminal / sealed evidence:
Tested candidates:
Reuse classification:
Active uncertainty:
Already closed / ruled out:
Single next discriminating action:
Possible outcomes -> next state:
Gate: PRE_EXPERIMENT_CONTEXT_GREEN | PRE_EXPERIMENT_CONTEXT_NOT_READY
```

`PRE_EXPERIMENT_CONTEXT_GREEN` is valid only when the owner, roadmap, memo/guide, terminal evidence, tested-candidate census, reuse classifications, and active uncertainty are mutually consistent enough to identify exactly one next discriminating action or STOP.

If any required context is missing, stale, ambiguous, contradictory, or cannot be bound to its production context, the gate is `PRE_EXPERIMENT_CONTEXT_NOT_READY`. In that state:

- do not draft a new experiment plan;
- do not promote an existing draft as the next experiment;
- do not let the downstream plan itself substitute for the missing research context;
- repair the maintained roadmap/memo/discovery state first.

A new conversation, a recently written plan, or an already-loaded skill does not waive this reload. The purpose of the gate is to prevent a locally coherent plan from drifting away from the maintained research program after new evidence changes the frontier.

