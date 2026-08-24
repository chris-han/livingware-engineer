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

## MVL Is the Feature-Development Unit

For product features, plan a **Minimum Viable Loop (MVL)**, not merely an implementation slice.

**MVL is the feature-development unit, not a test unit.** Unit tests, integration tests, browser tests, and E2E tests are verification evidence inside the implementation of an MVL.

The same feature contract must survive every later phase:

```text
Target user + job + value hypothesis
  -> smallest real user journey
  -> realistic trial inputs
  -> prerequisites / dependencies
  -> implementation
  -> TDD
  -> real-component integration when impact radius requires it
  -> real-browser UI verification when applicable
  -> technical + UX measurement
  -> feedback / diagnosis
  -> improvement
  -> comparable re-test
```

Do not create a plan whose terminal state is only "code complete" or "tests pass" when the work is a product feature. Implementation correctness is necessary evidence inside the MVL; it is not the feature-development unit itself.

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

These are not a separate skill or optional appendix. They are part of the plan contract and constrain task design, dependency readiness, test design, integration scope, and completion evidence.

For non-product maintenance work where no user-learning loop exists, state `MVL: not applicable — <reason>` rather than inventing one.

## Impact Radius Before Test Scope

Do **not** choose integration/E2E scope from diff size or intuition alone.

When `codebase-memory-mcp` is available, use it before finalizing the Integration Contract. If the repository is not indexed, run `index_repository` first. Prefer graph-oriented tools such as:

- `search_graph`
- `trace_path`
- `query_graph`
- `search_code`
- `get_code_snippet`

Assess the changed production surface for callers, callees, downstream consumers, DI/factory wiring, routes, persistence/schema edges, async/event boundaries, trust boundaries, frontend consumers, and user paths.

Classify the observed radius:

```text
R0 local only        -> focused TDD / unit-level behavior test
R1 one seam          -> focused integration across that seam
R2 multi-component   -> real-component integration through affected path
R3 user/cross-boundary/UI -> vertical/E2E + real-browser verification for UI
```

Use the **smallest sufficient verification scope**. Do not wake the full integration/E2E stack for a small local change whose graph impact is R0.

Read `../test-driven-development/impact-radius-testing.md` for the detailed policy.

## Dependency and Prerequisite Contract

A new feature may rely on a package, service, runtime, browser, database, CLI, model, plugin, system library, or other prerequisite that does not yet exist in the project. **The plan must make that dependency explicit before feature code depends on it.**

Do not let implementation agents discover and install dependencies ad hoc in the middle of a task.

For every new or materially changed dependency, the plan must record:

- exact package/tool/service name
- exact version, compatible range, commit, image tag, or other pin when practical
- why it is needed for this MVL journey
- where it will be declared (`pyproject.toml`, `package.json`, lockfile, Docker image, system setup, plugin manifest, etc.)
- exact install/setup command
- required configuration/environment variables without embedding secrets
- compatibility constraints with the existing stack
- whether it changes runtime, build, test, deployment, licensing, security, or platform assumptions
- a **dependency smoke/contract test** proving the real dependency is usable before feature code relies on it
- cleanup/removal steps if an obsolete dependency is being replaced

Dependency readiness is a prerequisite gate:

```text
select dependency
  -> declare/pin it
  -> install it
  -> prove it loads/connects/executes
  -> prove the minimum API/behavior the feature relies on
  -> only then build feature code on top of it
```

A package merely appearing in a manifest or lockfile is **not** sufficient evidence. The plan must specify an executable check appropriate to the dependency, for example:

```text
Python library  -> import real package + exercise required API
Node package    -> import/instantiate real package + required behavior
Database        -> real connection + migration/query smoke test
CLI/tool        -> version + minimal real command
Browser/CDP     -> endpoint reachable + real browser session attach
External SDK    -> real in-repo adapter against local/sandbox remote boundary
Plugin          -> load/register + expected capability visible
```

If the dependency itself is an in-repo production component or local service, do not fake it merely to unblock development. Install or implement the prerequisite first, then verify it with the real implementation.

If a dependency is genuinely external or nondeterministic, a local/sandbox substitute may stand in for the remote side, but the in-repo adapter/client must remain real where practical.

**Dependency test scope is separate from feature integration scope.** A new dependency always needs enough smoke/contract evidence to prove it is usable, while broader integration/E2E still follows the R0–R3 impact-radius decision.

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

A task is the smallest implementation unit that carries its own test cycle and is worth a fresh reviewer's gate. When drawing task boundaries: fold setup, configuration, scaffolding, and documentation steps into the task whose deliverable needs them; split only where a reviewer could meaningfully reject one task while approving its neighbor. Each task ends with an independently testable deliverable.

**Exception for feature prerequisites:** if a new dependency is load-bearing for multiple later tasks, make dependency declaration/install/verification an explicit prerequisite task before those consumers. Do not duplicate install steps in every downstream task.

Task boundaries MUST preserve the MVL journey. Do not decompose the work in a way that leaves the final integration task reconstructing a user path from mutually inconsistent local assumptions.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Install/declare required dependency" - step when applicable
- "Run dependency smoke/contract test" - step when applicable
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

## Prerequisites and Dependencies

**New dependencies:** [exact package/tool/service + version/pin, or none]
**Declaration files:** [pyproject/package.json/lockfile/Docker/etc.]
**Install/setup commands:** [exact commands]
**Configuration:** [required non-secret settings/env names]
**Compatibility constraints:** [runtime/platform/version assumptions]
**Dependency verification:** [exact smoke/contract test command + expected result]
**Replaced dependencies / cleanup:** [if applicable]

## Impact Radius

**Source:** codebase-memory-mcp | equivalent | manual fallback
**Indexed:** [true/false/not-applicable]
**Changed surfaces:** [symbols/files/routes/schema/config]
**Direct consumers:** [callers/consumers]
**Affected boundaries:** [DI/routes/persistence/events/trust/UI/etc.]
**User paths at risk:** [if any]
**Graph evidence:** [relevant search_graph / trace_path / query_graph findings]
**Radius:** R0 | R1 | R2 | R3

## Integration Contract

**Required scope:** local | focused_integration | real_component_integration | vertical_e2e
**Real components required:** [changed/relied-upon in-repo components that must appear real in integration]
**Permitted substitutes:** [true external/nondeterministic boundaries only]
**Forbidden mocks:** [internal components on the completion path]
**Existing tests to run:** [focused existing coverage]
**New tests required:** [only gaps not already covered]
**UI test:** [required? preferred Chrome CDP endpoint if applicable]

## Global Constraints

[The spec's project-wide requirements — version floors, dependency limits, naming and copy rules, platform requirements — one line each, with exact values copied verbatim from the spec. Every task's requirements implicitly include this section.]

---
```

For maintenance/non-product work, replace the MVL Contract block with `MVL: not applicable — <reason>` but still declare prerequisites/dependencies, perform Impact Radius assessment, and keep the Integration Contract whenever production wiring may be affected.

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

**Prerequisites:** [earlier dependency/setup task(s) that must already be green]

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

### Dependency Prerequisite Task Shape

When a new dependency is load-bearing, use an explicit early task like:

````markdown
### Task 0: Install and Verify [Dependency]

**Files:**
- Modify: `pyproject.toml` / `package.json` / relevant manifest
- Modify: lockfile
- Test: `tests/integration/test_<dependency>_availability.py` (or equivalent)

- [ ] **Step 1: Add/pin the dependency**
- [ ] **Step 2: Install/sync the environment**
- [ ] **Step 3: Write the smallest real smoke/contract test for the API the feature will rely on**
- [ ] **Step 4: Run the dependency test and verify it passes with the real package/service**
- [ ] **Step 5: Run the existing baseline tests affected by the dependency change**
- [ ] **Step 6: Commit manifest + lockfile + dependency verification together**
````

Later tasks may rely on this prerequisite only after its verification is green.

## Mandatory Closure Tasks for Product Features

The plan must contain only the closure work justified by the observed impact radius plus the product-learning work required by the MVL:

1. **Prerequisite/dependency verification** — required for every new load-bearing package/service/tool before feature consumers execute.
2. **TDD/local behavior** — always for changed behavior.
3. **Focused or real-component integration** — only when R1/R2/R3 impact requires it; exercise the smallest affected production path with no internal completion-path mocks.
4. **Real-browser UI verification** — mandatory when frontend/UI behavior is affected; prefer the configured Chrome CDP endpoint (commonly `127.0.0.1:9222`).
5. **Vertical/E2E** — when R3 impact or the MVL's smallest real journey crosses architectural boundaries.
6. **Baseline measurement** — run the declared technical and UX evaluation surface on realistic inputs.
7. **Feedback capture verification** — prove the planned telemetry/feedback/correction surface actually records useful evidence.
8. **Improvement cycle** — make at least one evidence-driven change when the iteration requires MVL closure.
9. **Comparable re-test** — rerun the same evaluation surface and record before/after evidence.

A plan that ends after technical verification is implementation-complete, not MVL-complete.

## No Placeholders

Every step must contain the actual content an engineer needs. These are **plan failures** — never write them:
- "TBD", "TODO", "implement later", "fill in details"
- "Install dependencies" without exact package/version/declaration/install/verification details
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — the engineer may be reading tasks out of order)
- Steps that describe what to do without showing how (code blocks required for code steps)
- References to types, functions, or methods not defined in any task

## Self-Review

After writing the complete plan, look at the spec with fresh eyes and check the plan against it. This is a checklist you run yourself — not a subagent dispatch.

**1. Spec coverage:** Skim each section/requirement in the spec. Can you point to a task that implements it? List any gaps.

**2. MVL continuity:** Can you trace the same target user, smallest journey, trial inputs, metrics, feedback surface, improvement lever, and re-test criterion from the plan header into concrete tasks and closure evidence? If not, the feature-development unit fragmented during planning.

**3. Dependency readiness:** For every new package/service/tool, is there an exact declaration/install path, version/pin, compatibility note, and executable smoke/contract verification before consuming feature tasks begin?

**4. Impact-radius evidence:** Did you use `codebase-memory-mcp` when available, index first if needed, and record concrete callers/consumers/boundaries rather than inferring blast radius from diff size?

**5. Integration credibility:** Does required test scope match R0/R1/R2/R3? Are existing focused tests reused before adding overlapping tests? For R1+, do affected internal production components appear real where required?

**6. Placeholder scan:** Search your plan for red flags — any of the patterns from the "No Placeholders" section above. Fix them.

**7. Type consistency:** Do the types, method signatures, and property names you used in later tasks match what you defined in earlier tasks? A function called `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a bug.

If you find issues, fix them inline. No need to re-review — just fix and move on. If you find a spec requirement, dependency prerequisite, or MVL contract item with no task/evidence path, add it.

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `docs/superpowers/plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans, batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use superpowers:subagent-driven-development
- Fresh subagent per task + two-stage review
- The controller owns MVL continuity and prerequisite readiness across task boundaries; individual implementers do not redefine the feature contract or install undeclared dependencies ad hoc.

**If Inline Execution chosen:**
- **REQUIRED SUB-SKILL:** Use superpowers:executing-plans
- Batch execution with checkpoints for review
- Preserve the MVL Contract, Prerequisites and Dependencies, Impact Radius, and Integration Contract unless new codebase evidence or a spec revision requires an explicit update.
