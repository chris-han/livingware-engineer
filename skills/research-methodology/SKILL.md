---
name: research-methodology
description: Use when doing substantive research: reviewing evidence, comparing literature or systems, forming/refining hypotheses, designing or running experiments, interpreting results, or deciding what research should happen next. Keeps research anchored to a design goal and contracts uncertainty through a shared Discovery Kanban / Uncertainty Convergence Graph.
---

# Research Methodology

Use this skill for research work whose purpose is to reduce uncertainty before a design, architecture, product, or scientific decision. It is the orchestration layer above literature review, hypothesis generation, experimental design, statistics, and evaluation skills. Do not duplicate those specialist operations here; route to them when needed.

The objective is not "do more research." It is:

> **Converge on the smallest defensible design by reducing one named uncertainty at a time, preserving what has already been ruled out, and stopping when no further experiment has positive decision value.**

## Core research law

Every substantial research action MUST answer four questions before work begins:

1. **Design goal** — what eventual design/decision is this research trying to make possible?
2. **Current uncertainty** — what exact unresolved question prevents that goal from being settled?
3. **Discriminating action** — what is the smallest evidence-producing action whose possible outcomes distinguish the live explanations?
4. **Convergence effect** — how will each possible outcome contract the uncertainty frontier, route to exactly one next question, or stop?

If an experiment cannot change the state of a named uncertainty, do not run it.

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

## Experiment admissibility

A research experiment is eligible only when all are true:

- it addresses a named live uncertainty;
- the expected outcomes are defined before protected results are inspected;
- the changed variable(s) are explicit;
- nuisance/confound controls are adequate for the claim;
- references/evaluators are independent enough for the intended inference;
- evidence and measurement identities can be retained;
- success, failure, uncertainty, and stop conditions are frozen;
- each material outcome maps to zero or one primary next question;
- the experiment has a finite budget;
- it does not duplicate an already-qualified experiment without a specific non-duplication delta.

Prefer the smallest experiment that can produce the first defensible decision-changing insight.

## Evidence discipline

Separate:

```text
external source result
!= model inference
!= project-specific direct evidence
!= adopted research law
```

For claim-bearing evidence, preserve as applicable:

- source/dataset identity and lineage;
- split/population identity;
- model/scorer/evaluator identity;
- governing experiment/measurement contract;
- code/config/runtime identity where material;
- raw results sufficient to reproduce reduction;
- uncertainty method;
- exclusions and invalid-run treatment;
- production time and immutable hashes/commits;
- governing scope and explicit non-claims.

A result does not become current evidence merely because it is reported now.

## Falsification and negative knowledge

Never delete or silently reopen a falsified branch.

A falsified/retired hypothesis records:

- what claim was tested;
- exact scope/population;
- evidence that closed it;
- whether it is `FALSIFIED`, `NOT_SUPPORTED_WITHIN_SCOPE`, `SUPERSEDED`, or merely `UNRESOLVED`;
- what materially new evidence would be required to reopen it.

Failed trials are durable evidence, but a failed experiment is not automatically a falsified hypothesis.

## Closure

Research closes when the evidence supports one bounded disposition and the discovery state is updated.

Minimum closeout:

```text
Design goal
Uncertainty addressed
Evidence produced + provenance
Result / uncertainty interval
Hypotheses eliminated
Hypotheses retained
Bounded conclusion + scope
Primary follow-up: NONE | exactly one bounded question
Successor state: NOMINATED_NOT_AUTHORIZED | NO_AUTOMATIC_SUCCESSOR | BLOCKED
```

Use `UNRESOLVED` when intervals, reference quality, support, or confounds prevent a defensible branch.

A terminal experiment does not authorize implementation, admission, activation, deployment, or another experiment. Those remain owned by the destination workflow.

## One-next-question-or-stop rule

After closeout:

- choose **zero** next questions when the design decision is sufficiently resolved, the evidence basis is inadequate without a specific repair, or no remaining experiment has positive bounded information value;
- choose **one** primary next question when evidence identifies the smallest unresolved boundary that can change the design decision;
- do not fan out into several speculative experiments just because several are interesting.

Parallel research is allowed only for genuinely independent uncertainty nodes with separate owners/evidence and no shared protected basis that would invalidate independence.

A useful conceptual objective is:

```text
next experiment value
  ~= expected decision-relevant uncertainty reduced
     + downstream decisions unlocked
     - evidence/compute/time cost
     - duplication/confound risk
```

Do not pretend this quantity is numerically calibrated unless the project has a real value-of-information model.

## Specialist routing

This skill decides **what research operation is justified next**. Delegate the operation itself when a specialist skill exists:

- literature/system comparison -> literature-review / research skill;
- hypothesis formation -> hypothesis-generation;
- experiment construction -> experimental-design;
- statistical inference -> statistics/data-analysis;
- system/evaluator qualification -> evaluation skills;
- engineering design after research resolves a project choice -> brainstorming/design workflow.

Return to this skill after the specialist operation to update the uncertainty frontier.

## Anti-patterns

Do not:

- begin external discovery or nominate a new model/tool/candidate before reconstructing the maintained project evidence state;
- treat a new paper, benchmark, leaderboard result, repository, or model family as permission to reset the research program;
- start with a preferred solution and collect confirming papers;
- open a new experiment because a previous result was "interesting";
- repeat a closed experiment under a new name;
- treat model/provider comparison as diagnosis when data/interface/representation uncertainty is unresolved;
- treat aggregate accuracy as causal attribution;
- let protected test evidence leak into hypothesis or threshold formation;
- convert `UNKNOWN` into failure or zero;
- create multiple competing research ledgers;
- let the discovery map become implementation or governance authority;
- continue optimizing after the design-relevant uncertainty has closed.

## Output for a new research action

Before substantive execution, produce or update the smallest sufficient discovery context:

```text
Design goal:
Current frontier:
This thread addresses:
Already closed / ruled out:
Evidence reusable:
Evidence gap addressed:
Candidate non-duplication delta:
Competing explanations:
Discriminating action:
Possible outcomes -> next state:
Stop condition:
Owner:
```

Then perform only the research needed to resolve that node.

## Output at closeout

```text
Uncertainty:
Disposition:
Evidence:
What is now ruled out:
What remains possible:
Design implication:
Primary follow-up:
Authority boundary:
```

The measure of progress is not the number of experiments completed. It is the amount of decision-relevant uncertainty removed without losing provenance, alternatives, or scope.
