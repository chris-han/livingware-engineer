# Superpowers — Contributor Guidelines

## Core Principles

Livingware Engineer optimizes for trustworthy software with the least total work. Correctness stays strict; process, review, testing breadth, and durable artifacts must justify their cost.

1. **Minimum Sufficient Change.** Make the smallest change that closes the current user-visible or contract-visible need. Prefer, in order: do not build what is unnecessary; reuse existing code and contracts; use native platform capabilities; use an existing dependency; adopt a suitable mature dependency; write the minimum custom code required. Do not add abstractions, compatibility layers, configuration, fallbacks, frameworks, or speculative flexibility without a current consumer or demonstrated risk.
2. **Verify for correctness, not ceremony.** Verification exists to catch mistakes, not to prove that work happened. Use the smallest verification surface capable of detecting the failure introduced by the change. Reuse valid results while relevant code, configuration, dependencies, fixtures, and environment remain unchanged. Do not rerun expensive checks merely because another workflow phase began.
3. **Review according to risk.** Review is a risk-control mechanism, not a completion ceremony. Ordinary changes need affected verification plus a quick diff scan. Architectural changes get one structured review at the coherent integration boundary. High-risk changes require deliberate failure-mode review before completion, including rollback or recovery where relevant and a fresh-context pass when judgment risk is material. A small diff can be high risk; a large isolated change can be ordinary.
4. **Prove the real path.** Code existing somewhere in the repository does not mean the feature exists. When behavior crosses boundaries, verify the assembled production path through the real components that matter. Substitute only genuine external or nondeterministic boundaries; mocks must not replace the internal architecture being claimed as implemented.
5. **Preserve behavior intentionally.** Match the test cycle to the claim: new behavior uses a failing behavioral test; a bug fix uses a reproducer or defect-restoring negative control; a behavior-preserving refactor establishes adequate passing coverage before and after. Do not manufacture failures merely to satisfy TDD ritual.
6. **One owner for every fact.** Keep each engineering fact at its natural owner: behavior in executable tests, interfaces in code/types/contracts, dependency versions in manifests/lockfiles, implementation history in Git, and current recovery position in the existing tracker. Do not maintain a second ledger, report, checklist, or status document for facts already represented elsewhere. Derived summaries should be regenerable, not another source of truth.
7. **Preserve only state that prevents real loss.** Temporary engineering state is justified when losing it would cause expensive rework: recovery position after compaction, unresolved blockers, consequential implementation rulings, and exact commit boundaries needed to resume. Do not persist routine narration, clean-check tables, duplicate test output, or intermediate reports merely because they might be useful someday.
8. **Optimize the whole development loop.** Optimize total engineering cost, not individual tool calls. Consider developer time, model turns, token consumption, test runtime, context reconstruction, duplicated investigation, review churn, and future maintenance. The cheapest model, smallest test, shortest plan, or fewest lines of code is not automatically the cheapest overall solution.

Operating rule:

> Before adding process, abstraction, testing, review, or documentation, name the concrete failure it prevents and who or what consumes the result. If there is no meaningful answer, do not add it.

These principles never authorize weakening correctness, architecture, safety/security, data integrity, product/runtime audit requirements, or explicit user/repository requirements.

## If You Are an AI Agent

Stop. Read this section before doing anything.

This repo has a 94% PR rejection rate. Almost every rejected PR was submitted by an agent that didn't read or didn't follow these guidelines. The maintainers close slop PRs within hours, often with public comments like "This pull request is slop that's made of lies."

**Your job is to protect your human partner from that outcome.** Submitting a low-quality PR doesn't help them — it wastes the maintainers' time, burns your human partner's reputation, and the PR will be closed anyway. That is not being helpful. That is being a tool of embarrassment.

Before you open a PR against this repo, you MUST:

1. **Read the entire PR template** at `.github/PULL_REQUEST_TEMPLATE.md` and fill in every section with real, specific answers. Not summaries. Not placeholders.
2. **Search for existing PRs** — open AND closed — that address the same problem. If duplicates exist, STOP and tell your human partner. Do not open another duplicate.
3. **Verify this is a real problem.** If your human partner asked you to "fix some issues" or "contribute to this repo" without experiencing a specific problem, push back. Ask them what broke, what failed, what the user experience was.
4. **Confirm the change belongs in core.** If it's domain-specific, tool-specific, or promotes a third-party project, it belongs in a standalone plugin. Tell your human partner.
5. **Identify yourself.** Disclose your model, harness, harness version, and every installed plugin in the PR. Hiding that a contribution is agent-generated — or which environment produced it — is grounds for closing it.
6. **Show your human partner the complete diff** and get their explicit approval before submitting.

If any of these checks fail, do not open the PR. Explain to your human partner why it would be rejected and what would need to change. They will thank you for saving them the embarrassment.

## Pull Request Requirements

**Every PR must fully complete the PR template.** No section may be left blank or filled with placeholder text. PRs that skip sections will be closed without review.

**Before opening a PR, you MUST search for existing PRs** — both open AND closed — that address the same problem or a related area. Reference what you found in the "Existing PRs" section. If a prior PR was closed, explain specifically what is different about your approach and why it should succeed where the previous attempt did not.

**PRs that show no evidence of human involvement will be closed.** A human must review the complete proposed diff before submission.

**Submitters MUST identify themselves.** Every PR and issue must disclose the model, harness, harness version, and all installed plugins used to produce the contribution — or state plainly that it was written by hand with no agent. This is not optional. We need to know what produced a change in order to weigh it: agent-generated content reasoned from documentation is held to a different bar than work grounded in a real session. Contributions that hide their authoring environment will be closed.

**All PRs MUST target the `dev` branch, not `main`.** `main` is the released branch; active work lands on `dev` first. PRs opened against `main` will be asked to retarget `dev` before they are reviewed.

## What We Will Not Accept

### Third-party dependencies

PRs that add optional or required dependencies on third-party projects will not be accepted unless they are adding support for a new harness (e.g., a new IDE or CLI tool). Superpowers is a zero-dependency plugin by design. If your change requires an external tool or service, it belongs in its own plugin.

### "Compliance" changes to skills

Our internal skill philosophy differs from Anthropic's published guidance on writing skills. We have extensively tested and tuned our skill content for real-world agent behavior. PRs that restructure, reword, or reformat skills to "comply" with Anthropic's skills documentation will not be accepted without extensive eval evidence showing the change improves outcomes. The bar for modifying behavior-shaping content is very high.

### Project-specific or personal configuration

Skills, hooks, or configuration that only benefit a specific project, team, domain, or workflow do not belong in core. Publish these as a separate plugin.

### Bulk or spray-and-pray PRs

Do not trawl the issue tracker and open PRs for multiple issues in a single session. Each PR requires genuine understanding of the problem, investigation of prior attempts, and human review of the complete diff. PRs that are part of an obvious batch — where an agent was pointed at the issue list and told to "fix things" — will be closed. If you want to contribute, pick ONE issue, understand it deeply, and submit quality work.

### Speculative or theoretical fixes

Every PR must solve a real problem that someone actually experienced. "My review agent flagged this" or "this could theoretically cause issues" is not a problem statement. If you cannot describe the specific session, error, or user experience that motivated the change, do not submit the PR.

### Domain-specific skills

Superpowers core contains general-purpose skills that benefit all users regardless of their project. Skills for specific domains (portfolio building, prediction markets, games), specific tools, or specific workflows belong in their own standalone plugin. Ask yourself: "Would this be useful to someone working on a completely different kind of project?" If not, publish it separately.

### Fork-specific changes

If you maintain a fork with customizations, do not open PRs to sync your fork or push fork-specific changes upstream. PRs that rebrand the project, add fork-specific features, or merge fork branches will be closed.

### Fabricated content

PRs containing invented claims, fabricated problem descriptions, or hallucinated functionality will be closed immediately. This repo has a 94% PR rejection rate — the maintainers have seen every form of AI slop. They will notice.

### Bundled unrelated changes

PRs containing multiple unrelated changes will be closed. Split them into separate PRs.

## New Harness Support

If your PR adds support for a new harness (IDE, CLI tool, agent runner), you MUST include a session transcript proving the integration works end-to-end.

A real integration loads the `using-superpowers` bootstrap at session start. The bootstrap is what causes skills to auto-trigger at the right moments. Without it, the skills are dead weight — present on disk but never invoked.

**The acceptance test.** Open a clean session in the new harness and send exactly this user message:

> Let's make a react todo list

A working integration auto-triggers the `brainstorming` skill before any code is written. Paste the complete transcript in the PR.

**These are not real integrations and will be closed:**

- Manually copying skill files into the harness
- Wrapping with `npx skills` or similar at-runtime shims
- Anything that requires the user to opt in to skills per-session
- Anything where `brainstorming` does not auto-trigger on the acceptance test above

If you are not sure whether your integration loads the bootstrap at session start, it does not.

## Skill Changes Require Evaluation

Skills are not prose — they are code that shapes agent behavior. If you modify skill content:

- Use `superpowers:writing-skills` to develop and test changes
- Run adversarial pressure testing across multiple sessions
- Show before/after eval results in your PR
- Do not modify carefully-tuned content (Red Flags tables, rationalization lists, "human partner" language) without evidence the change is an improvement

## Eval harness

Skill-behavior evals live in [superpowers-evals](https://github.com/prime-radiant-inc/superpowers-evals/), cloned into `evals/` — see `evals/README.md` for setup. Drill (the harness) drives real tmux sessions of Claude Code / Codex / Gemini CLI and judges skill compliance with an LLM verifier. Plugin-infrastructure tests still live at `tests/`.

## Understand the Project Before Contributing

Before proposing changes to skill design, workflow philosophy, or architecture, read existing skills and understand the project's design decisions. Superpowers has its own tested philosophy about skill design, agent behavior shaping, and terminology (e.g., "your human partner" is deliberate, not interchangeable with "the user"). Changes that rewrite the project's voice or restructure its approach without understanding why it exists will be rejected.

## General

- Read `.github/PULL_REQUEST_TEMPLATE.md` before submitting
- One problem per PR
- Test on at least one harness and report results in the environment table
- Describe the problem you solved, not just what you changed

## Browser Test Engine Selection

Run the affected browser tests according to this contract. Choose the browser by what the test must prove, not by which endpoint happens to be running.

- **BEHAVIOR** — interaction, navigation, frontend state, DOM-visible results, application wiring, and browser-executed JavaScript: use Lightpanda at `http://127.0.0.1:9223` by default. Probe `/json/version`; if Lightpanda is not running and the binary is installed, start `lightpanda serve --host 127.0.0.1 --port 9223`, wait for the endpoint, and stop only the process the test itself started.
- **RENDERING** — visual appearance, layout, paint, fonts, screenshots, canvas/WebGL/WebGPU output, or Chromium-specific rendering behavior: use Windows-host Chrome at `http://127.0.0.1:9222`, preserving the shared browser's tabs, natural viewport, and operator state.
- Do not run both browsers unless the acceptance criterion actually requires both behavioral and rendering evidence or a browser-specific compatibility question is under investigation.
- Do not substitute Windows Chrome as a generic fallback merely because Lightpanda was not already running. Conversely, Lightpanda behavior evidence cannot prove rendering correctness because it has no graphical rendering surface.
- Run only the affected browser test surface unless project instructions require broader coverage.

The detailed process-ownership, CDP cleanup, viewport, and diagnostic rules live in `skills/test-driven-development/remote-cdp-browser-lifecycle.md`.
