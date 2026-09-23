---
name: evaluating-skill-runtime
description: Use when evaluating how a Livingware skill actually activates and behaves across trigger, routing, workflow, action, evidence, and exit boundaries; do not use merely to review SKILL.md wording or instruction architecture.
---

# Evaluating Skill Runtime

Evaluate observed or reproducible skill behavior, not just its instruction text.

Use `skill-review` when the task is to audit `SKILL.md`, `AGENTS.md`, activation wording, layer placement, progressive disclosure, or token/tool-loop architecture.

Read `../../docs/livingware-evaluation-architecture.md` for the Eval IR and `../../docs/skill-runtime-architecture.md` for routing/workflow/tool/policy ownership.

## Runtime contract

Evaluate the skill lifecycle across:

```yaml
trigger:
  should_activate:
  should_not_activate:

preconditions:
  required_context:

routing:
  expected:
  prohibited:

workflow:
  required_transitions:
  prohibited_transitions:
  recovery:

actions:
  required:
  optional:
  forbidden:

evidence:
  required:

exit:
  success:
  stop:
  defer:
  handoff:
```

Not every skill requires every field. Keep the contract proportional to the skill.

## Evaluation procedure

1. Define representative positive, negative, neighboring-state, and boundary cases.
2. Run the real harness or the repository's accepted deterministic fixture for the claim.
3. Capture enough trace evidence to identify activation, route, actions, observations, and exit.
4. Evaluate individual claims with deterministic checks where possible.
5. Use interpreted evaluators only for genuinely semantic claims.
6. Classify failures before proposing changes:
   - activation/branch/stop -> ROUTING;
   - transition/recovery/topology -> WORKFLOW;
   - mechanical capability -> CAPABILITY / TOOL;
   - invariant violation -> POLICY;
   - product code or fixture problems -> IMPLEMENTATION / ENVIRONMENT.
7. Add durable regression witnesses for qualified failures.

## Required case classes

For important skills, include:

- should-activate cases;
- should-not-activate cases;
- neighboring-skill collision cases;
- mid-conversation reclassification cases where applicable;
- completion/exit cases;
- at least one hard negative around the most important boundary.

Counterfactual evaluation may compare alternate routes or workflows, but must preserve the accepted intervention and provenance contract.

## Native Codex empirical lane

When the claim is about actual Codex skill activation rather than only a repository contract, use the existing live progressive-routing probe through the Eval IR wrapper:

```bash
CODEX_PROBE_RETRIES=1 \
CODEX_PROBE_TIMEOUT=180 \
bash tests/eval-skills/live-skill-runtime-eval.sh
```

The wrapper executes `tests/codex/live-progressive-skill-probe.sh` and compiles its observed summary through `scripts/compile-live-skill-eval.py`.

The result is written under:

```text
.artifacts/livingware-eval-skill-runtime/<run>/eval-run.json
```

The artifact binds the observed episode to its production run id, repository commit, Livingware version, and Codex CLI version so later reporting or contract changes cannot silently rewrite the evidence basis.

Interpret routing evidence conservatively:

- required skill explicitly observed and no forbidden skill observed -> `PASS`;
- forbidden skill observed -> `FAIL`;
- required skill not explicitly observed -> `UNKNOWN`, even if output behavior looks correct;
- for the no-workflow baseline, observed absence of all forbidden workflow skills is the expected routing evidence and may be `PASS`.

Do not convert historical live runs into current-version evidence. They may serve as regression references only.

## Invariants

- A failed skill-runtime eval does not automatically authorize editing the skill.
- Change the smallest owner identified by failure attribution.
- Do not replace real harness claims with a fake matcher.
- Do not use this skill to duplicate `skill-review`.

## Output

Produce case-level results, failure attribution, regression-witness candidates, and a bounded recommendation for the owning layer. Use `designing-evaluators` or `qualifying-evaluators` when semantic claims need reusable evaluators.
