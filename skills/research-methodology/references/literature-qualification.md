# Literature Qualification

Use this reference when an external paper, benchmark, repository, model card, or similar research artifact is already relevant enough to inspect, but the open question is whether it deserves deeper research attention.

The purpose is not to score paper quality. It is to estimate whether the candidate can cause a defensible state transition in the maintained research program.

## Governing question

Qualify the candidate relative to the current research state (S_t):

```text
candidate artifact + current research state
  -> assess decision-relevant delta
  -> choose bounded disposition
  -> allocate reading / evaluation depth
```

A useful conceptual test is:

```text
Catalyst(candidate | S_t)
  := candidate can materially change a live hypothesis,
     mechanism assumption, experiment, gate, evidence basis,
     or next research action.
```

Do not treat this as a numerically calibrated probability unless an evaluator has been independently qualified for that use.

## ResearchCatalystAssessment

Use the smallest representation needed for the task. When a structured assessment is useful, use:

```yaml
candidate_ref: <paper / repo / benchmark / model-card identity>

disposition:
  type: CATALYST | EVIDENCE | CONTEXT | SKIP
  confidence: <optional calibrated confidence>

delta:
  hypothesis: NONE | SUPPORT | CHALLENGE | NEW
  mechanism: NONE | KNOWN | NEW
  experiment: NONE | MODIFY | NEW
  gate: NONE | STRENGTHEN | WEAKEN | REOPEN
  next_action: NONE | MODIFY | REPRIORITIZE | NEW

evidence_refs:
  - <section / figure / dataset / code / artifact ref>

reason_codes:
  - <bounded machine-stable reason when useful>

learning_eligible: <true | false>
```

The labels mean:

- **CATALYST** — evidence is strong enough that the current research state or next discriminating action should change.
- **EVIDENCE** — contributes material support, challenge, boundary evidence, or calibration without changing the research direction by itself.
- **CONTEXT** — useful background or conceptual context, but no current decision-relevant delta is established.
- **SKIP** — topical or interesting but no bounded information value for the active frontier is established.

The disposition is a research-routing judgment, not implementation, admission, activation, or product authority.

## Qualification sequence

Before qualifying an external candidate:

1. Reconstruct the current owner, active uncertainty, strongest existing evidence, already-tested candidates, and closed/falsified branches.
2. Identify the candidate's claimed mechanism, evidence, benchmark, or implementation contribution.
3. Compare that contribution against the current frontier, not against generic topic similarity.
4. Ask whether the candidate changes a live hypothesis, mechanism assumption, experiment, gate, evidence basis, or next action.
5. Record the smallest disposition justified by the evidence.
6. Allocate investigation depth proportionally to expected decision value.

If project context is unavailable, do not invent a project-specific catalyst judgment. Report the candidate's general contribution and mark the project-relative decision unresolved.

## Reading-depth policy

Prefer progressive expenditure:

```text
SKIP
  -> title / abstract / metadata sufficient once non-value is established

CONTEXT
  -> abstract + selected sections needed for accurate indexing

EVIDENCE
  -> targeted full-text reading of claim-bearing sections and provenance

CATALYST
  -> deep read as needed + explicit research-state delta
     + smallest discriminating follow-up or STOP
```

This is a token/attention allocation policy, not a command to under-read evidence. Escalate whenever the cheaper layer cannot support the claimed disposition.

A useful qualitative objective is:

```text
research intake efficiency
  ~= decision-relevant uncertainty reduced
     / (reading + retrieval + evaluation cost)
```

Do not manufacture precision for this quantity without a real value-of-information model.

## Hard negatives

A high-value research intake evaluator must distinguish:

```text
topically relevant
!= decision relevant
!= catalyst
```

Hard negatives should therefore include papers that share vocabulary, methods, tasks, or citations with the active research topic but do not change the current research decision. This is more informative than random unrelated negatives.

When qualifying an evaluator for this behavior, route to the evaluation skill family. The research skill consumes evaluator evidence; it must not become its own evaluator or learning authority.

## Learning boundary

A literature assessment may produce an observation or learning candidate, but it must not autonomously mutate the research methodology.

Conceptually:

```text
external candidate
  -> ResearchCatalystAssessment
  -> evidence-bound observation
  -> independent attribution / evaluation
  -> bounded change candidate or SKIP
```

Keep assessment, admission, and activation separate. External taxonomies and benchmark labels remain evidence/reference surfaces, not semantic authority for the project.
