# Research closure, attribution and specialist routing (conditional detail)

Load at research terminal interpretation/closeout or when a specific falsified hypothesis, successor choice or re-evaluation claim requires careful disposition. Do not preload for ordinary literature intake or while the current experiment is running.

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
Coverage achieved / gaps and protocol deviations
Hypotheses eliminated
Hypotheses retained
Bounded conclusion + scope
Attribution / change target and owner, or retain / reject / STOP
Comparable re-evaluation evidence / pending status / non-comparability
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
- treat benchmark presence as claim coverage, reproducibility as validity, or a recorded lesson as demonstrated improvement;
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
Benchmark / evidence coverage: claims -> cases/population; gaps; development/protected split
Auditable evaluation protocol: reference; baseline/controls; denominator; scoring/uncertainty; failure handling; frozen decisions; provenance
Result-driven improvement / decision loop: attribution -> bounded change/owner -> comparable re-evaluation, or retain/reject/STOP
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
Coverage achieved / gaps:
Protocol validity / deviations:
What is now ruled out:
What remains possible:
Design implication:
Result attribution:
Change target / owner, or retain / reject / STOP:
Comparable re-evaluation result / pending status / non-comparability:
Primary follow-up:
Authority boundary:
```

The measure of progress is not the number of experiments completed. It is the amount of decision-relevant uncertainty removed without losing provenance, alternatives, or scope.

