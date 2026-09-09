---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always
---

# Verification Before Completion

## Overview

**Core principle:** Evidence before claims, always.

For product features, completion has two different levels and they must never be conflated:

```text
Implementation complete
  = local behavior verified
  + real-component integration verified
  + real-browser UI verification when applicable
  + vertical/E2E verification when required

MVL complete
  = implementation complete
  + technical measurement
  + UX measurement
  + feedback capture
  + required evidence-driven improvement
  + comparable re-test against the same surface
```

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

Freshness is tied to the verified state, not the message boundary. Reuse an observed passing result when the relevant code, tests, dependencies, configuration, fixtures, and execution environment are unchanged and the result/output is available to inspect. If any relevant state changed or its identity is uncertain, rerun the affected checks. Live or time-sensitive external claims require a current check.

Run focused tests during implementation and expensive integration at coherent sprint exits, with earlier checks for demonstrated boundary risk. Before claiming integrated completion, verify the final assembled state with the required affected integration/browser checks. A focused pass is not a full-suite pass.

Use test output and version history as development evidence. Report the outcome, verification scope/results, and remaining gaps concisely. Do not create duplicate evidence packages, intermediate reports, or status ledgers unless the user or repository explicitly requires them. Required product audit/replay, persistence, and recovery contracts remain intact.

For a product feature, if the plan declares an MVL Contract, you also cannot claim the **feature/MVL** is complete merely because implementation tests pass.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What exact level are you claiming?
   - task complete
   - implementation complete
   - MVL / feature complete

2. IDENTIFY: What evidence proves that claim?

3. RUN OR REUSE: Execute the required affected checks, or inspect an existing
   result that meets the unchanged-state rule above. Run the full selected
   command; do not extrapolate from partial output or narrower coverage.

4. READ: Full output, check exit codes, failures, and measured results.

5. VERIFY: Does the evidence confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence

6. For product features, compare evidence to the plan's MVL Contract:
   - same target user / JTBD?
   - same smallest real journey?
   - same realistic trial inputs?
   - same technical + UX metrics?
   - feedback captured?
   - required improvement made?
   - same re-test surface rerun?

7. ONLY THEN: Make the claim.

Skip any step = not verified.
```

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Observed output: 0 failures for the claimed scope and unchanged verified state | Stale or unavailable result, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |
| Architecture implemented | Real-component integration through production wiring | Unit tests with internal mocks |
| Frontend complete | Real-browser verification of changed user path | jsdom, snapshots, mocked children |
| Shared-browser UI evidence | Natural viewport, fixture-owned page, cleanup proof, shared Chrome still reachable | Screenshot from an overridden or stale automation target |
| Implementation complete | TDD + integration + browser/E2E as applicable | One green test layer |
| MVL / feature complete | Implementation credibility + measurement + feedback + required improvement + comparable re-test | E2E passing |

## MVL Continuity Check

When the plan has an MVL Contract, re-read it before completion and verify continuity across the lifecycle:

```text
Plan                              Fresh completion evidence
----------------------------------------------------------------
Target user / JTBD           ->   same actor / scenario
Smallest real journey        ->   same integration/E2E path
Realistic trial inputs       ->   same or documented representative fixtures
Technical metrics            ->   current measured outputs
UX metrics                    ->   current browser/user-task evidence
Feedback capture              ->   evidence it recorded usable data
Improvement lever             ->   actual change justified by evidence
Re-test surface               ->   same surface rerun after improvement
Stopping criterion            ->   explicitly satisfied or explicitly not met
```

If the right side does not match the left side, do not claim MVL completion. Either the implementation drifted or the plan/spec needs revision.

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Treating a screenshot as valid without verifying shared-browser viewport and cleanup state
- Thinking "just this once"
- Tired and wanting work over
- Calling a product feature complete because integration/E2E is green while measurement/feedback/re-test are still open
- Using a different test journey than the plan's smallest real journey without documenting a plan/spec change
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | A focused check proves only its covered scope, not untested boundaries or a full-suite claim |
| "The E2E test passes, so the feature is done" | E2E proves the path works; MVL completion also requires learning-loop evidence declared by the plan |

## Key Patterns

**Tests:**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**Regression tests (TDD Red-Green):**
```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**Shared Chrome browser evidence:**
```
✅ Same target measured and captured → natural viewport confirmed → no active fixture override → owned page/session/client cleaned → shared endpoint still reachable
❌ Screenshot captured after setViewportSize → stale automation process left attached → operator tabs or browser state changed
```

Use the lifecycle checklist in [../test-driven-development/remote-cdp-browser-lifecycle.md](../test-driven-development/remote-cdp-browser-lifecycle.md) whenever completion evidence attaches to a persistent browser.

**Build:**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**Requirements:**
```
✅ Re-read plan → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

**Product MVL:**
```
✅ Re-read MVL Contract → run same user journey / metrics / feedback / re-test surface → report implementation state and MVL state separately
❌ "Browser + integration pass, feature complete"
```

**Agent delegation:**
```
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion/correctness
