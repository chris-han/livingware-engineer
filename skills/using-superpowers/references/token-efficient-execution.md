# Token-Efficient Execution Policy

**Purpose:** reduce avoidable generation and repeated context without reducing implementation correctness, user transparency about material risk, security, verification, or repository/host requirements. Applies to long-running plan execution and subagent orchestration; low-risk short tasks should not acquire a new process gate.

## 1. User-visible communication: silent by default

- **Do not narrate routine tool calls.** No obligatory pre-tool or post-tool sentence, status per test, tiny commit, subagent dispatch, poll, task change, successful checkpoint, or ordinary recovery.
- User-visible intermediate updates are **exceptional**: a material blocker requiring user action; consequential change in scope/authority; meaningful new failure or risk that changes the expected outcome; or a substantial independently useful milestone when a long-running host/user workflow needs one. When required, give **one compact sentence or paragraph**, not a chronological task log. Continue autonomously unless the User Intervention Necessity Test applies.
- Subagent waiting: continue local work and internally reconcile children on bounded waits. **Do not emit one user-visible update per wait/poll.** Report only a genuine stalled dependency or material finding, respecting any higher-priority host progress requirement.
- Preserve a concise final handoff with actual outcome, scope, verified evidence, unresolved limitations, commit/path references and any user action. Do not mistake silence for permission to omit material failures. Higher-priority host requirements and explicit user progress preferences override this default.

## 2. Keep tool output bounded and falsifiable

- Prefer targeted paths, symbols, line ranges, diffs and short status commands over whole-repository listings, full-file rereads and repeated searches for settled owner maps. Reuse source/commit hashes and re-read when code changed or evidence is stale.
- For passing tests, report `command, source SHA, suite, pass/skip counts, duration, consequential warnings`. Keep full machine logs in the existing evidence location when needed.
- For a failing test, expose the first **actionable** failing assertion/stack excerpt, the affected scope and log reference; expand the output only if the diagnosis needs it. Never silently discard distinct failures, suppress errors, misreport coverage or truncate the sole proof of a critical boundary.
- For diffs, inspect impacted hunks and interfaces first; fetch surrounding context only on ambiguity. Avoid pasting full files or repeated complete tool outputs into coordinator/subagent prompts.

## 3. Load skills and hand off context progressively

- Honor [Progressive Skill Loading](progressive-skill-loading.md): load only skills whose entry conditions hold. Do not preload debugging, TDD, browser verification, branch finishing, or unrelated skills during initial plan activation merely because the plan mentions them.
- Carry a compact SHA-bound checkpoint (plan/goal, changed owners, completed evidence, open risks, next action). Link to prior source/evidence rather than reprinting skill bodies, full test logs or chronological narration.
- Delegate at the plan's review-unit boundary and supply exact plan/spec anchors, owned paths, snapshot SHA, task contract and expected verification. Request brief result + commit range + tests + blockers; read full subagent output only when a failure or consequential decision requires it. Avoid duplicate reviewers and separate fixers for every minor finding.

## 4. Verification and model effort remain risk-based

- Use the existing Verification Impact Analysis R0–R3: focused checks after local edits, real-component/native counterexamples early for high-risk lifecycle seams, a broad run when the assembled candidate requires it, and scoped post-fix reruns with exact unchanged-evidence justification.
- A saving obtained by skipping required verification, missing a blocking failure, or narrowing the user's goal is **not** efficiency improvement.
- If the harness actually supports choosing reasoning effort/model, prefer proportionate effort: routine mechanical edits need less; architecture, concurrency, unexplained faults and consequential review need more. Do not invent unsupported settings, silently change user-selected models, or sacrifice correctness to lower tokens.

## 5. Measure, don't presume savings

Use [Execution Economics](../../executing-plans/references/execution-economics.md) when measurement is requested/available. Distinguish generated output, uncached input, cache read/write, tool runtime and wall time. Compare next verified completion against the archived historical baseline only with scope and token-accounting comparability disclosed. No fabricated per-phase attribution or claimed percentage from an aggregate-only previous run.

## Behavioral checks

1. Ten routine successful tool calls: **zero obligatory user-visible narrated updates**; actual results stay in evidence.
2. Multi-minute subagent wait: internal reconciliation without repeated status posts; a real blocker still reaches the user.
3. Failing broad test: concise actionable error **plus retained complete log**, followed by scoped diagnosis/retest.
4. New lifecycle bug in an otherwise green task: record/recover and tell the user when it materially changes outcome, not after every fix attempt.
5. Final completion: concise, evidence-grounded, with no hidden failure and no unsupported speedup claim.
