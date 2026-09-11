# AI-Native SDLC Minimal Absorptions Refactor Plan

## Goal

Absorb four useful ideas from Anthropic's AI-native SDLC into Livingware Engineer without importing its artifact-heavy stage model, adding automatic behavioral evals, or increasing routine token/output cost.

## Governing constraint: no slop output

No absorption may create a new default artifact, report, ledger, checklist, summary, telemetry stream, eval run, or approval stage. Existing authoritative sources, executable tests, Git history, and current trackers remain the preferred owners. A new durable artifact is allowed only when losing that information would create material rework, mistranslation, or authority ambiguity.

## Four absorptions

### A1 — Optional intent authority, not mandatory `intent.md`

Preserve one authoritative statement of what is wanted, why, material constraints, and success conditions. Reuse the nearest user request, issue, spec, ADR, or product document when sufficient. Create a dedicated intent artifact only when intent would otherwise be lost, repeatedly mistranslated, reused across sessions/agents/systems, or needs independent durable authority.

Acceptance: no new mandatory SDLC stage and no duplicate intent document.

### A2 — Budgeted behavioral learning

Behavioral evals and workflow-learning runs are framework maintenance, not ordinary completion work or CI gates. The agent may suggest a targeted run only after repeated/systemic evidence accumulates and it can name the evidence, suspected pattern, and concrete framework decision the run could improve. The user must explicitly initiate execution. Start with the smallest relevant scenario subset; expand only when evidence or release risk justifies the token/review cost.

Acceptance: no automatic corpus runner, no automatic policy mutation, no periodic eval merely because time has passed.

### A3 — Incident evidence routes to the smallest owner

Do not turn every incident into a new incident artifact or a new intent document. After root-cause analysis, route the finding to the smallest durable owner:

- implementation defect with unchanged intent -> reproducer/regression test + fix;
- violated existing contract/requirement -> update the existing authoritative contract only if it was ambiguous or wrong, otherwise just fix the defect;
- evidence that the requirement, architecture, or value hypothesis itself is wrong -> reopen the existing authoritative intent/MVL/spec and revise it there.

Acceptance: incidents create new planning artifacts only when they reveal a genuine change in intent or hypothesis that cannot be represented safely in the existing owner.

### A4 — One authoritative source; other representations derive or link

Extend `One owner for every fact` into an explicit authority rule: each fact has one authoritative owner; copies, summaries, generated views, plans, and integration surfaces must derive from or link to that owner rather than becoming independently authoritative.

Acceptance: no synchronization burden between duplicate sources of truth.

## Implementation

1. Keep the concise authority and budget-learning invariants in `AGENTS.md`; do not turn it into a runbook.
2. Keep detailed behavioral-learning guidance behind progressive disclosure under `skills/skill-review/references/`.
3. Express optional intent and incident routing as ownership rules, not new artifact templates or workflow stages.
4. Do not add a behavioral corpus file, runner, CI hook, cron job, telemetry store, evidence ledger, intent template requirement, or incident-report requirement.
5. Bump repository plugin manifests consistently to `6.5.27`.

## Non-goals

- Reproducing Anthropic's `intent.md -> spec.md -> plan.md` chain.
- Mandatory human gates between stages.
- Uniform review passes for every change.
- Autonomous self-improvement loops.
- Automatic token-budget estimators.
- New documentation produced merely to prove that a workflow step occurred.

## Completion criteria

The repository should express all four ideas as decision rules while ordinary development produces exactly the same default artifact set as before. Behavioral learning remains human-initiated; intent artifacts remain conditional; incidents normally terminate in tests/code or the existing authority source; duplicate sources remain non-authoritative; all release manifests report `6.5.27`.
