# Progressive Skill Loading Contract

Load only the workflow skill governing the agent's current decision state. Future-state skills remain unloaded until their entry condition is satisfied.

## Debugging

**Entry:** unresolved bug, failed test, unexpected behavior, regression, performance anomaly, or unexplained failure.

**Exit:** root cause and affected behavior are sufficiently established, or the request ends with diagnosis only.

**Replace with:**
- TDD when an authorized behavior change or bug fix is ready to implement.
- verification when no code change is needed but a correctness/completion claim must be made.
- nothing when diagnosis-only work is complete.

**Handoff:** root cause, expected behavior, affected surface, relevant evidence, unresolved material risk.

## TDD

**Entry:** an authorized production behavior change, bug fix, or behavior-preserving refactor has a sufficiently defined behavior/preservation contract.

**Exit:** focused behavior evidence is green and the implementation is ready for broader completion/integration claims.

**Replace with:**
- debugging when new evidence materially invalidates the diagnosis or reveals an unexplained failure.
- verification when a correctness/completion/integration claim is imminent.

**Handoff:** intended behavior, changed surface, relevant focused test results, remaining integration/completion claims.

## Verification

**Entry:** an agent is about to claim fixed, correct, complete, integrated, ready to merge, or ready to release, or a consequential action depends on that claim.

**Exit:** the claim is supported, falsified, or narrowed to what the evidence establishes.

**Replace with:**
- debugging for an unexplained failure.
- TDD for a known implementation gap with the diagnosis still valid.
- nothing after a supported final claim unless an authorized integration/release workflow follows.

## Replacement rules

1. Debugging, TDD, and verification are sequential states, not a default bundle.
2. Do not preload all three.
3. At most one should govern current reasoning except for a brief handoff.
4. Once a skill exits, stop consulting or restating its detailed body. If the runtime can replace context, unload it; otherwise treat it as inactive.
5. Pass compact state across transitions, not the preceding skill text or a narrative transcript.
6. Re-enter an earlier skill only when new evidence satisfies its entry condition.
7. Cross-cutting invariants belong in the router or the skill that owns them, not duplicated across workflow bodies.
