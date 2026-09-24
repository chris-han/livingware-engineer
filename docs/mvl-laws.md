# Livingware Engineering MVL Laws

These laws sit under the Minimum Viable Loop (MVL) principle and define cross-cutting product and architecture invariants. Skills may add domain-specific guidance, but must not weaken them.

## MVL Law 1 — Fast-to-Aha: ambient governance, interruptive only by exception

Preserve governance as an explicit safety and authority boundary, but do not make it the default blocking interaction for exploration, context formation, comparison, preview, reversible local work, or other low-risk paths. Form the useful working context and expose the useful result first. Keep the gate present, recorded, inspectable, and default-pass.

Escalate to an explicit interruption only when a deterministic trigger protects a real boundary: material risk, contradiction, missing mandatory evidence, permission or tenant-boundary failure, consequential external action, authority escalation, irreversible/destructive action, or mutation/admission/activation of higher-authority semantics.

Passing a low-risk gate never grants consequential-action authorization or higher-tier semantic authority.

> Governance should be ambient by default and interruptive only by exception.

Review question: if an approval step delays the first useful result without changing risk, remove or default-pass it.

### User Intervention Necessity Test

User intervention is a scarce input, not a generic workflow gate. Apply standing user delegation first. A running plan or workflow may interrupt the user only when all three are true:

1. **The next required action cannot proceed autonomously** — progress genuinely depends on input or action the agent cannot supply itself.
2. **The blocker is not already delegated or recoverable** — it cannot be resolved from standing authorization, binding spec/policy, observed evidence, executable verification, established convention, a safe reversible default, retry/debug/replan within scope, or another already-authorized path.
3. **The missing capability is genuinely user-owned** — for example subjective product intent, non-delegable legal/compliance judgment, authority for a consequential external/production action, access or credentials that only the user can authorize through a supported secure mechanism, sensitive-data disclosure, or an irreversible/destructive operation.

Before asking, state the exact missing input or action, why autonomous recovery is exhausted, the material consequence of guessing, and what would unlock progress. Otherwise make the smallest reversible in-scope ruling or recovery action and continue.

User intervention is **not** required merely because a phase ended, a checkpoint or review completed, tests passed or failed, remaining gates exist, a task is incomplete, a browser/service fixture still needs to run, a technical design choice is required, or ordinary uncertainty can be reduced by inspection, testing, debugging, rollback, or a reversible implementation choice.

Progress reporting is observational, not a synchronization barrier. For long-running work, concise updates may report a meaningful milestone, material finding, or recovery-state change, but execution continues immediately afterward unless this test is satisfied. Do not turn routine updates into “should I continue?” checkpoints.

A predeclared negative or inconclusive terminal disposition is not a blocker. When its terminal predicate is satisfied by evidence, close the plan with that disposition rather than asking whether to continue.
