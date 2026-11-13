# Verification Impact Analysis v1

Status: Active engineering verification policy

Verification Impact Analysis (VIA) selects the smallest verification surface capable of falsifying the claim implied by a change. It exists to reduce CI time, agent latency, and token cost without weakening evidence.

## Principle

Test scope follows observed production impact radius, not diff size and not habit. Scope does not determine execution frequency: an R3 change needs goal-level E2E evidence, not an E2E run after every task.

```text
changed production surface
  -> relationship-aware impact analysis
  -> affected seams, consumers, trust boundaries, and user paths
  -> smallest sufficient verification
  -> broader verification only when blast radius or uncertainty requires it
```

Prefer a current code graph when it materially improves confidence. `codebase-memory-mcp` can supply `search_graph`, `trace_path`, `query_graph`, `search_code`, and `get_code_snippet`. Whole-repository indexing is not a prerequisite for a bounded change; when graph evidence is unavailable, use targeted static/source evidence and state the lower confidence.

## Radius classes

- `R0` — local behavior only: focused TDD/unit-level behavior evidence.
- `R1` — one production seam: focused integration across the affected seam.
- `R2` — multi-component production path: real-component integration through the affected path.
- `R3` — user journey, UI, cross-process, or multiple architectural boundaries: vertical/E2E evidence; real-browser verification for affected UI behavior.

Broad suites are justified when impact is itself broad or uncertain: shared-core changes, schema migrations, auth/security boundaries, dependency upgrades, release candidates, highly reused abstractions, or unresolved fan-out.

## Stratified verification cadence

- `D0 — deterministic invariants`: cheap mechanical checks on relevant mutations.
- `D1 — local semantic sentinels`: focused behavior, contract and necessary real-component integration checks during implementation.
- `D2 — full semantic audits`: broad or expensive suites at the integrated goal/release candidate, explicit periodic triggers, or demonstrated broad risk. A task completion, commit or phase transition alone is not a trigger.

## Goal-level E2E, task-level focused verification

This section owns the shared scheduling and evidence-economy contract. Planning, execution and completion skills reference it rather than starting separate campaigns.

**E2E is a goal-completion gate, not a per-task completion gate.** Finish all implementation tasks in the current goal's task list with focused checks; assemble the candidate, ready its real services/dependencies and fixtures, then run one consolidated E2E campaign before declaring the goal achieved. Final acceptance and cleanup tasks naturally follow implementation readiness; do not require them to finish before the campaign that proves them.

For a UI goal, start from the actual application UI and drive the connected user journey through CDP or the project's qualified UI automation adapter. Verify relevant backend effects and persistence, not only visible labels. API tests, mocked UI and screenshots alone cannot replace that journey. Use the required native/browser application; a web page cannot substitute for required native Electron acceptance. Non-UI goals use their real entry point; do not introduce a browser just for ceremony.

One campaign may contain several scenarios, application targets and required ordering constraints. A Windows-first constraint orders final acceptance inside the campaign; it does not by itself defer Workspace implementation or require repeated Windows E2E during development. Honor explicit user/repository exceptions. Do not broaden scope to all platforms or all repository tests.

Earlier UI work is limited to a bounded diagnostic smoke when a named unresolved UI/native risk cannot be resolved more cheaply, or when explicitly required. Record only the reason and result in the existing tracker. A diagnostic smoke is not full E2E, is not required at every milestone, and does not unlock an otherwise unmet goal. Keep necessary local security, authorization, transaction and dependency tests early.

On failure, diagnose, repair and rerun the failed scenarios plus paths invalidated by the repair. Do not restart the whole campaign by default, retry until green, weaken assertions or erase failed attempts. Broaden reruns only for demonstrated shared-state/fan-out risk. Integration or merge invalidates evidence only when relevant contents, wiring, configuration, dependencies, fixtures, environment or acceptance contract changed; a new commit hash alone is not a full-rerun requirement. Final claims must cover the actual integrated candidate.

## Incremental evidence and stopping

Start from the current checkpoint, changed surfaces and existing executable assertions/results. Reuse supported coverage; inspect only changed, failed, missing or uncertain coverage. Read the original acceptance source when first establishing coverage, when it changes or when the checkpoint is insufficient—not at every phase. At final closure confirm no required condition remains failed or unverified; incrementality never permits silently dropping a requirement.

One run may prove many acceptance conditions. Reference that result once and use assertion IDs only where needed to resolve gaps. Do not create one evidence file per requirement, copy a requirement-to-evidence matrix at each stage, or generate a second ledger. Keep the minimal recovery checkpoint: relevant candidate/environment identity, result location, remaining gaps and next action. Available runner/CI/Git metadata can supply identities; do not invent a separate hash manifest by default. Reuse classifications such as `EXACT_REUSE`, `PARTIAL_REUSE` and `STALE` belong only where a changed contract or uncertain provenance makes the distinction useful.

When the required current-candidate evidence is sufficient, stop testing and reporting. Preserve product-required audit, financial, security and replay evidence and useful failure diagnostics under their existing retention owner; token economy is not permission to delete them or bypass acceptance.

## Token-bounded UI execution

Batch deterministic actions and assertions in a script; the LLM plans the journey and investigates exceptions rather than reasoning through every click. Reuse a controlled CDP connection within its ownership and identity boundaries; never share authentication/storage across accounts merely to reduce setup cost.

Read targeted DOM/accessible state and selected response fields. Avoid repeated full DOM, accessibility-tree, console or network dumps. Capture screenshots for failures or required visual assertions/key checkpoints, not after every action. Keep raw logs/traces locally with redaction and bounded retention; do not feed them all back into model context.

Before a campaign, choose finite action, timeout, retry and output limits appropriate to the existing runner. Default tool-result budget: a compact summary of at most 20 lines; on failure, the failing assertion and at most 80 relevant diagnostic lines, with a local path for deeper inspection. These are output defaults, not truncation of stored evidence or requested complete reports. Expand only the excerpt needed to resolve the current failure. Do not introduce a telemetry service or a mandatory budget approval step.

Return the scoped verdict, missing/failed conditions, reusable result reference and next action. Record actual token/tool-call metrics when already available; otherwise say `UNKNOWN`. Text size, script automation and source checks do not prove realized token savings or improved agent behavior.

## Required evidence

For material changes, record enough in the existing plan/tracker or runner metadata to identify changed surfaces, relevant consumers/boundaries, uncertainty, R0–R3 radius, selected focused tests, and any required final journey. Do not fill a large template when a short delta and existing test references answer those questions. Broader omitted suites need a reason only when their omission is material to the claim.

## Relationship to MVL evaluation

VIA is not the product evaluation loop and R0–R3 are not MVL levels. VIA chooses implementation verification evidence. MVL evaluation measures whether the feature produced the intended value and learning. A feature can be locally verified yet fail its MVL outcome; an MVL experiment must not weaken real-component evidence. Preserve explicitly required human-benefit measurements; browser success does not establish reduced human cognitive load.

## Relationship to IA-before-UI

`docs/ia-before-ui.md` asks whether a user-facing structure is conceptually correct before production UI coding begins. VIA asks how broadly the resulting code must be verified and when that evidence is needed:

```text
IA-before-UI -> implementation tasks + focused checks
            -> integrated candidate ready
            -> one consolidated real-UI E2E campaign
            -> evidence-backed goal completion and authorized cleanup
```

Neither gate requires human approval by default.
