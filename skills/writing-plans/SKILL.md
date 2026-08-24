---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Context:** If working in an isolated worktree, it should have been created via the `superpowers:using-git-worktrees` skill at execution time.

**Save plans to:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
- (User preferences for plan location override this default)

## MVL Is the Planning Unit

For product features, plan a **Minimum Viable Loop (MVL)**, not merely an implementation slice.

The same feature contract must survive every later phase:

```text
Target user + job + value hypothesis
  -> smallest real user journey
  -> realistic trial inputs
  -> implementation
  -> TDD
  -> real-component integration
  -> real-browser UI verification when applicable
  -> technical + UX measurement
  -> feedback / diagnosis
  -> improvement
  -> comparable re-test
```

Do not create a plan whose terminal state is only "code complete" or "tests pass" when the work is a product feature. Implementation correctness is necessary evidence inside the MVL; it is not the feature unit itself.

Every feature plan MUST define, near the top:

- **Target user / job-to-be-done**
- **Value hypothesis** — what useful change this feature is expected to create
- **Smallest real user journey** — the narrowest end-to-end path that demonstrates that value
- **Realistic trial inputs**
- **Technical success metrics**
- **UX success metrics**
- **Feedback / telemetry capture**
- **Improvement levers** — code, model, prompt, rules, data, knowledge, UI, workflow, thresholds, configuration, architecture
- **Re-evaluation method** — same surface used before and after improvement
- **Stopping criterion for this MVL iteration**

These are not a separate skill or optional appendix. They are part of the plan contract and constrain task design, test design, integration scope, and completion evidence.

For non-product maintenance work where no user-learning loop exists, state `MVL: not applicable — <reason>` rather than inventing one.

## Scope Check

If the spec covers multiple independent subsystems, it should have been broken into sub-project specs during brainstorming. If it wasn't, suggest breaking this into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

For a product feature, prefer the smallest loop that can generate reliable learning. Do not broaden architecture, governance, ontology, edge-case coverage, or generalized platform support beyond what is required to make the smallest real journey credible and learnable.

## File Structure

Before defining tasks, map out which files will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Design units with clear boundaries and well-defined interfaces. Each file should have one clear responsibility.
- You reason best about code you can hold in context at once, and your edits are more reliable when files are focused. Prefer smaller, focused files over large ones that do too much.
- Files that change together should live together. Split by responsibility, not by technical layer.
- In existing codebases, follow established patterns. If the codebase uses large files, don't unilaterally restructure - but if a file you're modifying has grown unwieldy, including a split in the plan is reasonable.

This structure informs the task decomposition. Each task should produce self-contained changes that make sense independently.

## Task Right-Sizing

A task is the smallest unit that carries its own test cycle and is worth a fresh reviewer's gate. When drawing task boundaries: fold setup, configuration, scaffolding, and documentation steps into the task whose deliverable needs them; split only where a reviewer could meaningfully reject one task while approving its neighbor. Each task ends with an independently testable deliverable.

Task boundaries MUST preserve the MVL journey. Do not decompose the work in a way that leaves the final integration task reconstructing a user path from mutually inconsistent local assumptions.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

**Spec:** [path to the spec/design doc this plan implements — the plan argues from the spec, so the spec travels with it; executors read both]

## MVL Contract

**Target user / JTBD:** [who is trying to accomplish what]
**Value hypothesis:** [what useful change should happen]
**Smallest real journey:** [entry point -> meaningful action -> visible/useful outcome]
**Trial inputs:** [realistic fixtures/scenarios]
**Technical metrics:** [quality/reliability/latency/cost/etc.]
**UX metrics:** [completion/effort/confusion/correction/usefulness/trust/etc.]
**Feedback capture:** [telemetry, explicit feedback, corrections, traces]
**Improvement levers:** [what can change after evidence]
**Re-test surface:** [repeatable benchmark/user journey]
**Stopping criterion:** [what closes this iteration]

## Integration Contract

**Real components required:** [changed/relied-upon in-repo components that must appear real in integration]
**Permitted substitutes:** [true external/nondeterministic boundaries only]
**Forbidden mocks:** [internal components on the completion path]
**UI test:** [required? preferred Chrome CDP endpoint if applicable]

## Global Constraints

[The spec's project-wide requirements — version floors, dependency limits, naming and copy rules, platform requirements — one line each, with exact values copied verbatim from the spec. Every task's requirements implicitly include this section.]

---
```

For maintenance/non-product work, replace the MVL Contract block with `MVL: not applicable — <reason>` but keep the Integration Contract whenever architectural wiring is involved.

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Interfaces:**
- Consumes: [what this task uses from earlier tasks — exact signatures]
- Produces: [what later tasks rely on — exact function names, parameter and return types. A task's implementer sees only their own task; this block is how they learn the names and types neighboring tasks use.]

**MVL contribution:** [which part of the smallest real journey / metric / feedback surface this task enables]

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## Mandatory Closure Tasks for Product Features

The plan must contain explicit closure work for the MVL, not leave it implicit:

1. **Real-component integration** — run the smallest real journey through required production components with no internal completion-path mocks.
2. **Real-browser UI verification** — mandatory for frontend/UI behavior; prefer the configured Chrome CDP endpoint (commonly `127.0.0.1:9222`) when available.
3. **Baseline measurement** — run the declared technical and UX evaluation surface on realistic inputs.
4. **Feedback capture verification** — prove the planned telemetry/feedback/correction surface actually records useful evidence.
5. **Improvement cycle** — make at least one evidence-driven change when the iteration requires MVL closure.
6. **Comparable re-test** — rerun the same evaluation surface and record before/after evidence.

A plan that ends after integration or E2E testing is implementation-complete, not MVL-complete.

## No Placeholders

Every step must contain the actual content an engineer needs. These are **plan failures** — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — the engineer may be reading tasks out of order)
- Steps that describe what to do without showing how (code blocks required for code steps)
- References to types, functions, or methods not defined in any task

## Self-Review

After writing the complete plan, look at the spec with fresh eyes and check the plan against it. This is a checklist you run yourself — not a subagent dispatch.

**1. Spec coverage:** Skim each section/requirement in the spec. Can you point to a task that implements it? List any gaps.

**2. MVL continuity:** Can you trace the same target user, smallest journey, trial inputs, metrics, feedback surface, improvement lever, and re-test criterion from the plan header into concrete tasks and closure evidence? If not, the feature unit fragmented during planning.

**3. Integration credibility:** Does every changed/relied-upon internal production component appear in the Integration Contract as real, and is there a task that exercises the production path without mocking those components?

**4. Placeholder scan:** Search your plan for red flags — any of the patterns from the "No Placeholders" section above. Fix them.

**5. Type consistency:** Do the types, method signatures, and property names you used in later tasks match what you defined in earlier tasks? A function called `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a bug.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement or MVL contract item with no task/evidence path, add it.

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `docs/superpowers/plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use superpowers:subagent-driven-development
- Fresh subagent per task + two-stage review
- The controller owns MVL continuity across task boundaries; individual implementers do not redefine the feature contract.

**If Inline Execution chosen:**
- **REQUIRED SUB-SKILL:** Use superpowers:executing-plans
- Batch execution with checkpoints for review
- Preserve the MVL Contract and Integration Contract unchanged unless the spec itself is revised.
