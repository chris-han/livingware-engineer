# Livingware Engineering MVL Laws

These laws sit under the Minimum Viable Loop (MVL) principle and define cross-cutting product and architecture invariants. Skills may add domain-specific guidance, but must not weaken them.

## MVL Law 1 — Fast-to-Aha: ambient governance, interruptive only by exception

Preserve governance as an explicit safety and authority boundary, but do not make it the default blocking interaction for exploration, context formation, comparison, preview, reversible local work, or other low-risk paths. Form the useful working context and expose the useful result first. Keep the gate present, recorded, inspectable, and default-pass.

Escalate to an explicit interruption only when a deterministic trigger protects a real boundary: material risk, contradiction, missing mandatory evidence, permission or tenant-boundary failure, consequential external action, authority escalation, irreversible/destructive action, or mutation/admission/activation of higher-authority semantics.

Passing a low-risk gate never grants consequential-action authorization or higher-tier semantic authority.

> Governance should be ambient by default and interruptive only by exception.

Review question: if an approval step delays the first useful result without changing risk, remove or default-pass it.

### Human Judgment Necessity Test

Human judgment is a scarce input, not a generic workflow gate. Treat explicit delegation from the user as continuing authorization for in-scope engineering decisions; do not repeatedly ask the same authority holder to re-approve technical choices, phase transitions, reviews, or gates.

A running plan may stop for human judgment only when all three conditions are true:

1. **A real decision is required now** — the next action cannot proceed without choosing among materially different outcomes.
2. **The decision is not already delegated or mechanically resolvable** — it cannot be resolved from the user's standing delegation, binding spec/policy, observed code/runtime evidence, executable verification, established project conventions, or a safe reversible default within scope.
3. **The consequence of choosing wrong is material and not cheaply reversible** — for example a genuinely subjective product-intent choice, non-delegable legal/compliance determination, disclosure of sensitive data, irreversible/destructive operation, or consequential external/production action with material blast radius.

Before asking, state the exact decision, viable options, material consequence, and why standing delegation plus evidence or a reversible default cannot resolve it. If any element is missing, human judgment is not necessary: make the smallest reversible in-scope ruling and continue.

Human judgment is **not** required merely because a phase ended, a checkpoint or review completed, tests passed or failed, remaining gates exist, a task is incomplete, a browser/service fixture still needs to run, a technical design choice is required, or the agent has ordinary uncertainty that can be reduced by inspection, testing, debugging, rollback, or a reversible implementation choice.
