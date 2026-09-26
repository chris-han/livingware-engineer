# Product Value Validation for Feature Plans

Use this reference when `writing-plans` is planning a product feature whose justification depends on user value, adoption, activation, retention, workflow insertion, or market pull.

The purpose is not to add product-management ceremony. It is to prevent implementation confidence from outrunning value evidence.

## Applicability

Apply this validation when the plan introduces or materially changes:

- a user-visible capability or workflow;
- onboarding or first-use behavior;
- a new product surface;
- a commercially meaningful behavior;
- a feature explicitly justified by customer value, Fast-to-Aha, adoption, retention, expansion, or PMF.

Record `NOT_APPLICABLE` rather than fabricating a value hypothesis for:

- verified defect repair;
- behavior-preserving refactoring;
- dependency/platform maintenance;
- mandatory security, legal, contractual, or architecture-integrity work whose requirement is already authoritative;
- technical qualification/research whose purpose is not a user-value claim.

A requirement source may make implementation necessary without proving market demand. Preserve that distinction.

## Evidence ladder

Use the strongest level actually supported. Never promote evidence because a plan needs a stronger narrative.

```text
E0 ASSUMED
  internal hypothesis only

E1 QUALITATIVE_SIGNAL
  observed interviews, switch stories, direct problem evidence, or equivalent qualitative evidence

E2 BEHAVIORAL_SIGNAL
  users take a meaningful action that demonstrates interest or value, not merely stated preference

E3 REPEATED_BEHAVIOR
  repeated or retained use around the same job

E4 ECONOMIC_SIGNAL
  willingness to pay expressed through actual purchase, renewal, expansion, committed budget, or equivalent economic behavior

E5 MARKET_PULL
  repeatable pull across a defined segment, supported by retention/expansion/economic evidence rather than a single customer
```

Evidence provenance must remain explicit. `ASSUMED`, `INFERRED`, `SIMULATED`, and `OBSERVED` are not interchangeable.

## V0 — Job / problem reality

State the triggering situation before naming the feature.

```text
When <situation/change event>,
<target user> needs to <job>,
because <material consequence>.
Current workaround: <what they do now>.
Problem evidence: <observed/inferred/assumed basis>.
```

When evidence is empirical, prefer concrete past behavior over hypothetical preference questions.

Useful signals include:

- a recent switch or change event;
- a repeated workaround;
- measurable delay, rework, risk, or coordination cost;
- existing budget or labor already spent on the problem;
- a recurring decision whose failure has material consequences.

A feature is not justified merely because the problem is conceptually plausible.

## V1 — Value proposition compression

Express the value without implementation language:

```text
For <target user>,
when <triggering situation>,
this capability enables <useful outcome>,
unlike <current alternative/workaround>.
```

Then apply a Box-style compression test:

- Can the user-facing value be explained without naming internal architecture, models, schemas, databases, agents, or frameworks?
- Can a qualified user recognize why the outcome matters?
- Is the primary value clear without listing a collection of features?

If the proposition can only be explained as implementation, return to the job/problem statement.

## V2 — Aha contract

Define the first observable moment at which the user experiences the proposed value.

```text
Start event:
Aha event:
User can now do/decide:
Required pre-Aha actions:
Avoidable pre-Aha friction:
Target time-to-Aha:
```

The Aha event is not onboarding completion, successful rendering, a model response, or a passing backend call unless that event itself is the user value.

Prefer a first credible value event such as:

- a user discovers a material fact they could not easily see before;
- a user completes a previously expensive job materially faster;
- a user can make a decision with new trusted evidence;
- a user avoids a known failure mode through the feature.

For enterprise products, consider a **Time to First Actionable Finding** or equivalent domain-specific measure when that better captures value than generic activation.

## V3 — Falsifiable validation contract

Every product-value hypothesis must name what evidence would weaken or reject it.

```text
Hypothesis:
Positive evidence:
Counter-evidence / falsifier:
Measurement surface:
Minimum sufficient experiment:
```

Examples of suitable validation methods include:

- JTBD / switch interviews for problem reality;
- prototype or usability tests for comprehension and task fit;
- fake-door or landing-page behavior for demand signals;
- observed use for activation;
- cohort retention for repeated value;
- expansion and economic behavior for market pull.

Do not substitute stated preference for behavior when the claim is behavioral.

Choose the smallest experiment capable of discriminating the current uncertainty. A feature plan may legitimately terminate in a validation experiment instead of implementation.

## V4 — PMF claim boundary

Feature-level success does not establish product-market fit.

A feature plan may state which product-level signal it is expected to influence, for example:

- retention around the target job;
- repeated workflow insertion;
- customer-initiated expansion;
- willingness to pay;
- renewal or expansion revenue;
- a PMF survey among qualified active users.

Record:

```text
PMF-relevant signal:
Current evidence:
Expected contribution:
Claim boundary:
```

The default claim boundary is:

> This feature may contribute evidence toward product-market fit; this feature plan does not by itself establish PMF.

Do not turn a usability win, successful demo, interview preference, or technical completion into a PMF claim.

## Planning dispositions

Use one disposition:

- `READY_TO_PLAN` — the value basis is sufficient for the requested implementation scope.
- `VALIDATE_FIRST` — material value uncertainty remains and a smaller validation experiment is the appropriate next plan.
- `NOT_APPLICABLE` — product-value validation is not relevant; record the authoritative requirement source or reason.

`VALIDATE_FIRST` is not a human-approval checkpoint. It changes the executable plan target from feature implementation to the smallest useful validation experiment.

## Minimum plan block

```markdown
## Product Value Validation

**Applicability:** REQUIRED | NOT_APPLICABLE
**Target user / triggering situation:** ...
**Job-to-be-done:** ...
**Current workaround / cost:** ...
**Evidence provenance:** OBSERVED | INFERRED | ASSUMED | ...
**Evidence level:** E0 | E1 | E2 | E3 | E4 | E5
**Value proposition:** ...
**Start event:** ...
**Aha event:** ...
**Target time-to-Aha:** ...
**Pre-Aha friction:** ...
**Hypothesis:** ...
**Positive evidence:** ...
**Counter-evidence / falsifier:** ...
**Minimum validation surface:** ...
**PMF-relevant signal:** ...
**Claim boundary:** ...
**Disposition:** READY_TO_PLAN | VALIDATE_FIRST | NOT_APPLICABLE
```

Keep this block concise. Link existing evidence rather than duplicating interview transcripts, analytics, research reports, or requirement documents.
