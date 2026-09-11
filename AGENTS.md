# Superpowers — Contributor Guidelines

## Core Principles

Livingware Engineer optimizes for trustworthy software with the least total work. Correctness stays strict; process, review, testing breadth, and durable artifacts must justify their cost.

1. **Minimum Sufficient Change.** Make the smallest change that closes the current user-visible or contract-visible need. Prefer, in order: do not build what is unnecessary; reuse existing code and contracts; use native platform capabilities; use an existing dependency; adopt a suitable mature dependency; write the minimum custom code required. Do not add abstractions, compatibility layers, configuration, fallbacks, frameworks, or speculative flexibility without a current consumer or demonstrated risk.
2. **Verify for correctness, not ceremony.** Verification exists to catch mistakes, not to prove that work happened. Use the smallest verification surface capable of detecting the failure introduced by the change. Reuse valid results while relevant code, configuration, dependencies, fixtures, and environment remain unchanged. Do not rerun expensive checks merely because another workflow phase began.
3. **Review according to risk.** Review is a risk-control mechanism, not a completion ceremony. Ordinary changes need affected verification plus a quick diff scan. Architectural changes get one structured review at the coherent integration boundary. High-risk changes require deliberate failure-mode review before completion, including rollback or recovery where relevant and a fresh-context pass when judgment risk is material. A small diff can be high risk; a large isolated change can be ordinary.
4. **Prove the real path.** Code existing somewhere in the repository does not mean the feature exists. When behavior crosses boundaries, verify the assembled production path through the real components that matter. Substitute only genuine external or nondeterministic boundaries; mocks must not replace the internal architecture being claimed as implemented.
5. **Preserve behavior intentionally.** Match the test cycle to the claim: new behavior uses a failing behavioral test; a bug fix uses a reproducer or defect-restoring negative control; a behavior-preserving refactor establishes adequate passing coverage before and after. Do not manufacture failures merely to satisfy TDD ritual.
6. **One authoritative owner for every fact.** Keep each engineering fact at its natural owner: behavior in executable tests, interfaces in code/types/contracts, dependency versions in manifests/lockfiles, implementation history in Git, current recovery position in the existing tracker, and product intent in the nearest authoritative requirement source. Other representations must be derived from or linked to that owner, never independently authoritative. Do not maintain a second ledger, report, checklist, status document, or intent artifact when the same fact is already preserved clearly elsewhere.
7. **Preserve only state that prevents real loss.** Temporary engineering state is justified when losing it would cause expensive rework: recovery position after compaction, unresolved blockers, consequential implementation rulings, and exact commit boundaries needed to resume. Do not persist routine narration, clean-check tables, duplicate test output, or intermediate reports merely because they might be useful someday.
8. **Optimize the whole development loop.** Optimize total engineering cost, not individual tool calls. Consider developer time, model turns, token consumption, test runtime, context reconstruction, duplicated investigation, review churn, and future maintenance. The cheapest model, smallest test, shortest plan, or fewest lines of code is not automatically the cheapest overall solution.
9. **Budget framework learning.** Behavioral evals and workflow-learning runs are maintenance work, not default execution steps or CI gates. Never start them autonomously. Suggest a targeted learning run only when repeated materially independent evidence plausibly points to a shared workflow rule and one concrete policy decision can be tested, except for a clearly framework-level high-impact event. Execution requires explicit human initiation and smallest-relevant-scope first.
10. **Route incidents to the smallest durable owner.** After root-cause analysis, keep an implementation defect in its reproducer/regression test and fix; update an existing contract only when that contract is wrong or ambiguous; reopen intent/MVL/spec only when evidence shows the requirement, architecture, or value hypothesis itself must change. Do not create incident reports or new planning artifacts by default.

Operating rule:

> Before adding process, abstraction, testing, review, or documentation, name the concrete failure it prevents and who or what consumes the result. If there is no meaningful answer, do not add it.

> Before stopping for human judgment, first apply any standing user delegation. Then name the exact decision that still cannot be delegated or resolved from binding authority/evidence, why a reversible default is insufficient, and the material consequence of choosing wrong. If all three cannot be named, choose the smallest reversible in-scope path and continue.

These principles never authorize weakening correctness, architecture, safety/security, data integrity, product/runtime audit requirements, or explicit user/repository requirements.

## Repository Boundaries and Workflow Routing

- Preserve user-owned changes and required safety, architecture, integrity, and permission boundaries.
- This repository is a zero-dependency plugin; dependency exceptions and contribution eligibility are defined in [CONTRIBUTING.md](CONTRIBUTING.md).
- Before preparing a pull request or harness contribution, read [CONTRIBUTING.md](CONTRIBUTING.md) and the PR template. Existing human-review and target-branch requirements remain binding.
- For browser work, read [the browser selection and lifecycle contract](skills/test-driven-development/remote-cdp-browser-lifecycle.md). It owns evidence lanes, startup, process ownership, and cleanup.
- Use the task-sensitive skill router. Honor explicit user/repository requirements over generic workflow defaults.
