---
name: mvl-feature-development
description: Plan, implement, or review product features as Minimum Viable Loops (MVLs). Use for feature plans, prototypes, vertical slices, UX flows, AI capabilities, data/knowledge-backed features, integrations, and feature reviews. Require a closed learning loop from working prototype through technical evaluation, UX evaluation, feedback capture, improvement, and re-evaluation. Combine this with Livingware Engineer's TDD, real-component integration, and real-browser UI completion gates.
---

# MVL Feature Development

Treat the atomic unit of product development as a closed learning loop, not a list of implementation tasks.

## Definition

MVL = working prototype + measurable technical evaluation + measurable UX evaluation + feedback capture + at least one explicit improvement cycle.

A feature is not MVL-complete merely because code, tests, UI, backend, and persistence work end to end.

Use this canonical loop:

`Prototype -> Try -> Measure -> Feedback -> Diagnose -> Improve -> Re-test`

## Required Loop

For every feature, plan and verify these stages:

1. **Prototype** — build the smallest real user journey that demonstrates the intended value.
2. **Try** — make it possible for the target user to exercise the feature with realistic inputs.
3. **Measure technically** — define feature-specific quality, reliability, latency, cost, failure, accuracy, or other engineering metrics.
4. **Measure UX** — define task completion, time and effort, confusion, correction burden, usefulness, trust, reuse intent, or other user-performance metrics appropriate to the feature.
5. **Capture feedback** — collect explicit user feedback plus useful behavioral, quality, and error telemetry.
6. **Diagnose and improve** — identify which implementation levers can change from the evidence: code, model, prompt, rules, knowledge, data, UI, workflow, thresholds, architecture, or configuration.
7. **Re-evaluate** — rerun the same evaluation surface so the new result is comparable to the baseline.

## Planning Contract

Whenever creating or reviewing a feature plan, include a visible **Implementation Status Checklist** near the top and an explicit **MVL Closed Loop** section or equivalent content.

The status checklist must summarize:

- prerequisite/dependency readiness
- implementation entry/authorization when applicable
- major implementation milestones
- TDD gate
- real-component integration gate
- real-browser UI gate when frontend behavior is involved
- vertical/E2E gate when the feature crosses multiple boundaries
- specification/document synchronization when the project governs those artifacts
- final evidence
- stop/go outcome

Check an item only when both implementation and its required evidence are complete.

The MVL Closed Loop content must include:

- target user and job-to-be-done
- smallest working prototype journey
- realistic trial inputs
- technical success metrics
- UX success metrics
- baseline or initial benchmark
- feedback and telemetry capture mechanism
- improvement levers
- re-evaluation method
- stopping criterion for the current MVL iteration

If any item is missing, identify the loop as incomplete. Do not treat implementation completion as feature completion.

## Livingware Evidence Contract

MVL product learning sits above implementation correctness. The feature must first satisfy the relevant Livingware Engineer test gates.

```text
Local behavior
  -> TDD RED / GREEN / REFACTOR

Architecture
  -> real-component integration

Frontend / UI
  -> real-browser verification
  -> prefer Chrome CDP on 9222 when available

Cross-boundary user journey
  -> vertical / E2E verification

Then:
  -> Try / Measure / Feedback / Improve / Re-test
```

### TDD

Use `test-driven-development` for changed production behavior. New behavior should be proven by a failing test before implementation.

### Real-component integration

Any changed in-repo production component must participate as its real implementation in at least one integration path used as completion evidence. Do not mock through missing internal dependencies.

### Frontend/UI

Any user-visible frontend change requires a real-browser test. When the coding environment is WSL and Chrome is expected on the Windows host, prefer attaching through Chrome DevTools Protocol on port `9222`. If that endpoint is unavailable, treat browser availability as a prerequisite and instruct the user to start Windows Chrome in remote-debugging mode rather than silently substituting jsdom or mock-only component tests.

### Vertical/E2E

Use a vertical or end-to-end test when the feature crosses multiple architectural boundaries or when the user-value claim depends on the full application path.

Passing these gates means the implementation is credible enough to learn from; it does not itself close the MVL.

## Scope Discipline

Prefer the smallest loop that can generate reliable product learning.

Do not require complete platform architecture, production-scale hardening, exhaustive edge cases, full governance machinery, broad ontology completion, or generalized multi-domain support unless they are necessary to test the feature's core value or are required by risk/compliance.

Build enough architecture so the prototype can evolve without an obvious dead end, but do not substitute architecture completeness for user learning.

## Governance Rule

Treat governance as an architectural constraint and future tightening path, not automatic friction for every safe early feature trial.

For prototypes and MVLs:

- preserve important state, authority, and trust boundaries where practical
- preserve provenance/versionability when structurally important
- avoid irreversible shortcuts that make later tightening expensive
- keep risky side effects sandboxed, reversible, simulated, or explicitly confirmed
- require stronger governance when production side effects, regulatory obligations, security, financial risk, or the feature's purpose demands it

Governance does not excuse bypassing the Livingware test gates.

## Evaluation Design

Use both technical and UX evaluation. Unit, integration, and browser tests establish correctness but are not by themselves an MVL evaluation loop.

Prefer stable evaluation surfaces so iterations are comparable:

- a small frozen benchmark, fixture set, or repeatable scenario set
- realistic user trial inputs
- an explicit baseline before improvement
- versioned metric output where useful
- representative user tasks rather than only component tests

Choose metrics based on the feature's actual failure economics. Do not optimize a headline metric while degrading usability or task completion.

## Feedback Design

Capture enough evidence to answer:

- What failed?
- Where did it fail?
- Was the problem technical quality, data/knowledge quality, latency, interaction design, misunderstanding, or workflow fit?
- What change is most likely to improve the next run?

Use explicit feedback, corrections, interaction telemetry, error traces, evaluation results, and observed user behavior as appropriate. Tie telemetry to a learnable feature hypothesis.

## Knowledge- or Data-Backed Features

When feature performance materially depends on a knowledge or data asset, include construction and correction of that asset inside the MVL rather than treating it as unrelated infrastructure.

Examples include knowledge graphs, ontologies, retrieval corpora, mappings, taxonomies, rule libraries, labeled datasets, recommendation inventories, and domain dictionaries.

Use this generalized loop when applicable:

`Ground/acquire source -> Build/update asset -> Run feature -> Human/user review -> Evaluate feature + asset -> Correct asset/model/code/UX -> Re-run`

Evaluate both the supporting asset and the end-user feature. The asset does not need to be perfect before users can try the feature; it needs to be inspectable and correctable enough to support learning.

## Implementation Order

Default to this sequence:

1. identify the target user, job, and value hypothesis
2. prove the narrowest real user journey
3. satisfy TDD/integration/browser evidence required for that journey
4. instrument technical and UX outcomes
5. establish a repeatable evaluation baseline
6. capture useful feedback and corrections
7. close one measurable improvement cycle
8. only then broaden scope or harden architecture/governance beyond what the next learning step requires

If an existing feature already works but lacks evaluation or feedback, close the loop before adding adjacent capabilities.

## Review Heuristic

When reviewing a plan or implementation, ask:

- Can a real target user try the feature now?
- Has local behavior been proven with TDD?
- Are changed internal components proven through real integration?
- If UI is involved, has the user path been exercised in a real browser?
- Do we know whether it works technically?
- Do we know whether the UX works for the intended task?
- Can we observe why it fails or underperforms?
- Can the evidence change the next implementation?
- Can we rerun the same evaluation and demonstrate improvement?

If the last two answers are no, the feature is not yet a closed MVL.

## Final Rule

```text
Implementation complete != Feature complete

Implementation credibility
  = TDD + real integration + real browser when UI + vertical/E2E when needed

MVL complete
  = credible working prototype
  + measurable technical result
  + measurable UX result
  + feedback
  + explicit improvement
  + comparable re-test
```

This skill is adapted from the Semantier `mvl-feature-development` methodology and generalized for Livingware Engineer.
