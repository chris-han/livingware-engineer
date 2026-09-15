---
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment.
---

# Writing Skills

Writing skills is TDD applied to agent workflow guidance. This is Livingware Engineer's repository-owned skill-creator workflow; revise skills here rather than adding a competing creator/router skill.

The canonical layer architecture lives in `../../docs/skill-runtime-architecture.md`. Read it before materially changing a core/high-frequency skill.

## What is a skill?

A **skill is a discoverable entry package for a reusable, context-conditioned workflow**. It is not the owner of every rule, tool mechanic, or piece of reference knowledge used during that workflow.

Use the ownership gate before creating or expanding a skill:

```text
Is the behavior deterministic/reusable/mechanically testable?
  -> TOOL / SCRIPT / TEST

Is it a stable cross-cutting repository or architecture constraint?
  -> POLICY / INVARIANT OWNER

Is it knowledge only, without routing/execution authority?
  -> REFERENCE

Is it reusable transition/recovery structure?
  -> WORKFLOW

Is it context-conditioned selection among current options?
  -> ROUTING

Does a discoverable workflow entry need to exist?
  -> SKILL
```

Do not create a new skill for one-off solutions, project-specific conventions, ordinary well-documented practice, or mechanical constraints that a deterministic tool/test can enforce more reliably.

## Root SKILL.md contract

A frequently selected root skill should normally contain only:

- `name` and a discriminating `description`;
- entry/exit lifecycle when stateful;
- hard local invariants whose violation has concrete consequence;
- the smallest workflow contract needed after activation;
- explicit progressive-disclosure pointers;
- tool-economy guidance only where broad discovery is an observed risk.

Move conditional examples, long checklists, platform mechanics, browser procedures, model compensation, and workflow depth into references. Keep executable mechanics in scripts/tools/tests.

## Discovery / routing design

Descriptions answer **when should this skill be loaded now?**, not how the workflow works.

- Start with a concrete current-state trigger such as `Use when ...`.
- Do not summarize the process in the description; agents may shortcut the body.
- Keep neighboring workflow states mutually distinguishable where practical.
- For every high-frequency skill with a non-obvious boundary, identify at least one nearest competing state/skill and state what must *not* activate for the same bounded task.
- Do not use a mandatory meta-router where the host already performs native skill matching.

Examples:

```yaml
# bad: describes workflow and overlaps adjacent states
description: Use for bugs - debug, fix with TDD, then verify

# better: identifies the current unresolved state
description: Use while an observed failure is still unexplained and requires root-cause investigation
```

Routing is recurrent. A skill should exit when its state is resolved and let the next current-state skill match; it should not preload future-state skills merely because the task may eventually reach them.

## Workflow authoring

Express workflows as state transitions with evidence-based entry/exit conditions, not universal itineraries.

Prefer:

```text
state + evidence
  -> choose next distinguishing action
  -> observe
  -> route again
  -> exit / recover
```

over a fixed long sequence that every task must follow.

Keep compact handoffs between states: current state, intended/preserved behavior, affected surface, valid evidence, unresolved material risk, and next-state entry reason.

## Tool promotion

Promote behavior into a tool/operator when all are substantially true:

- the mechanic is deterministic or mechanically testable;
- it is reusable across more than one execution;
- repeated natural-language interpretation adds error/cost;
- the executable owner can have a focused regression test;
- tool schema/output cost does not exceed the prompt/tool-loop savings.

A workflow decides **when** to call the operator; it does not duplicate how it works.

Do not manufacture scripts purely to make the architecture look symmetric.

## Skill TDD

Match evaluation to the behavior being changed.

```text
changed routing      -> positive + negative + collision scenarios
changed workflow     -> transition/recovery/convergence behavioral scenario
changed operator     -> deterministic contract/regression test
changed policy       -> cross-workflow invariant/bypass evaluation
behavior-preserving  -> preservation evidence, no artificial RED ceremony
```

For a new behavioral steering rule:

1. create the smallest scenario that exposes the missing/incorrect behavior;
2. observe the baseline when practical;
3. make the smallest owning-layer change;
4. rerun the matched scenario;
5. do not claim generalized learning from the matched case alone.

Use `../skill-review/references/budgeted-behavioral-learning.md` when the change is claimed as shared behavioral learning rather than ordinary refactor/dedup/fix.

## Counterfactual evaluation

Counterfactual evaluation is optional maintenance support, not a skill-authoring requirement.

Use `../../docs/skill-runtime-architecture.md` and `../skill-review/references/layered-evaluation.md` when a replay/simulation can cheaply narrow a routing/workflow candidate before paying for real re-execution.

Preserve provenance:

```text
OBSERVED
REPLAYED
SIMULATED
INFERRED
ASSUMED
```

Simulation may rank or falsify candidates. It cannot substitute for materially independent observed evidence, and Monte Carlo what-if output must not be described as an identified causal effect.

## Token economics

Optimize architecture before wording:

1. do not load unnecessary context;
2. load only the current workflow state;
3. prevent activation collisions;
4. keep root skills compact and progressively disclose depth;
5. do not reimplement host matching/routing capability;
6. bound tool discovery and output;
7. reuse valid unchanged evidence;
8. reduce serial turns;
9. keep stable prefixes where useful for caching;
10. only then shorten prose.

Read `../../docs/skill-token-economics.md` for the full review model and the 6.8.x empirical lessons.

For high-frequency or token-sensitive changes, measure selection/collision behavior first, then latency and cached/uncached input/output using repeated comparable runs when practical. Do not infer a prompt regression from one noisy run.

## File structure

Use a flat discoverable skill namespace unless the host requires otherwise:

```text
skills/<skill-name>/
  SKILL.md
  references/        # conditional knowledge/workflow depth
  scripts/           # executable operators owned by this skill when appropriate
  agents/            # platform-specific agent definitions when required
```

Do not move existing files merely to fit this shape if ownership is already clear and no consumer benefits.

Frontmatter requirements remain compatible with the Agent Skills specification:

- `name`: letters, numbers, hyphens only;
- `description`: third-person/current-state trigger, preferably under 500 characters;
- frontmatter should remain compact and portable.

For platform-specific install paths or tool mapping, use the runtime references under `../using-superpowers/references/` rather than embedding platform mechanics in every skill.

## Verification checklist

Before deployment, verify:

- activation description identifies the current state and avoids known neighboring collisions;
- root body contains only normally-needed guidance;
- deterministic mechanics have executable owners/tests where justified;
- policy has one authoritative owner;
- dynamic choices remain routing decisions rather than universal sequences;
- references are loaded conditionally;
- model/platform compensation is isolated when possible;
- evidence/learning claims preserve provenance and authority boundaries;
- relevant routing, behavioral, operator, packaging, and token-economics tests pass.

For systematic review use `../skill-review/SKILL.md` and its audit rubric.

## Supporting references

- `anthropic-best-practices.md` — external skill-authoring guidance.
- `testing-skills-with-subagents.md` — pressure/evaluation techniques when subagents are the appropriate test harness.
- `examples/CLAUDE_MD_TESTING.md` — historical examples; treat as reference, not current architecture authority.
- `graphviz-conventions.dot` / `render-graphs.js` — optional diagram tooling.
