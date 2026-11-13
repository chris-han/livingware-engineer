# Detailed Verification Playbook

Load only the section needed to resolve a specific question left open by the compact skill. [Verification Impact Analysis](../../../docs/verification-impact-analysis-v1.md) owns cadence, incremental evidence and tool-output budgets; this reference does not schedule another E2E campaign.

## Evidence validity

Bind a reused result to the relevant implementation, tests, dependencies, configuration, fixtures, environment and acceptance contract at production time, not merely its reporting time. Use runner/CI/Git metadata already available. If the contract changed, distinguish `EXACT_REUSE`, `PARTIAL_REUSE` and `STALE` where useful; new or strengthened requirements need direct support. Uncertain identity is not a passing result. Live external claims need current observations.

Inspect the assertion's meaning: inputs, expected outcome, oracle, real components, forbidden substitutes and any required repeats/thresholds. A test name, metadata validator or green command list alone does not establish coverage. One run can cover many requirements; retain one result and reference the relevant assertions only for unresolved questions. Do not manufacture a parallel evidence package.

## Final acceptance and integration

Use established coverage plus the current delta and gap list. Read the original acceptance source when first establishing coverage or resolving change/ambiguity; do not reread every referenced document at each phase. Confirm no required condition is failed or unverified before declaring the goal achieved. An incomplete checkpoint requires targeted reconstruction, not assumed coverage.

Connected journey evidence must exercise the real components on the required shared state, including restart/reopen when specified. Disconnected passing unit tests cannot substitute for it. UI acceptance starts from the actual UI through CDP or its qualified adapter; backend inspection corroborates effects rather than bypassing user actions. Use the [browser lifecycle contract](../../test-driven-development/remote-cdp-browser-lifecycle.md) for the actual required browser/native target and owned cleanup.

Run the consolidated campaign at the integration-ready candidate. A later merge needs affected revalidation only when relevant state changed; preserve valid results instead of starting a second full campaign. Apply [Plan integration and retirement](../../finishing-a-development-branch/references/plan-integration-and-retirement.md) to target contents/reachability, required local integration, retained evidence and owned-resource cleanup. A narrower preservation/PR handoff exception must come from actual user/repository authority, not agent-authored plan text.

Keep plan disposition separate from the host goal. A predeclared negative/inconclusive disposition may close that run without establishing the requested outcome. Continue authorized repair/recovery; involve the user only when the User Intervention Necessity Test is met. Never mark complete to satisfy a linter. Retract disproved completion claims and restore editable status to incomplete, noting any host status that cannot be reopened.

## Match the claim

| Claim | Necessary support |
|---|---|
| Tests/build/lint pass | Actual successful result for that scope and valid state |
| Bug fixed | Original defect reproducer/negative control passes after the fix |
| Behavior preserved | Adequate before/after characterization, not artificial RED ritual |
| Architecture implemented | Real-component production wiring, not internal mocks |
| UI goal complete | Required real-UI connected journey and effects on the integrated candidate |
| Delegated work complete | Actual scoped diff and applicable results, not an agent assertion |

A focused result is not full-suite success. Preserve the declared MVL's target user/job, trial inputs, technical/UX measures, feedback, justified improvement, comparable retest and stopping criterion when applicable; do not invent an MVL for maintenance. Automated clicks/screenshots cannot establish measured human benefit.

## Required artifacts and records

When the requested deliverable is a human-readable evidence/research artifact, independently inspect its provenance, denominators, limitations, stopping reason and demonstrated versus unproved claims. This does not require an extra report about that inspection. Governance hashes attest to a performed review; recomputing a hash is not reviewing the changed content. Refresh only affected reviewed bindings.

Preserve required product audit, financial/security/replay records and useful failure evidence at their existing owner. Keeping a raw log locally does not require loading it into model context. Default to bounded summaries and inspect deeper only for the current unresolved failure. Stop when the declared claim is sufficiently supported.
