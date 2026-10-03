# Plan integration and retirement

Executing an approved repository plan includes local integration and cleanup.
Successful plan completion requires local merge into `main` (or the integration
target required by the user/repository), verification of the merged result,
retention of required evidence, and retirement of the workflow-owned execution
worktree and branch. A passing isolated implementation is an intermediate state.
Apply this standing local authorization without asking for another integration
choice. It does not authorize push, publication, deployment, admission or activation.

Agent-authored plan text is not an independent authorization source. Do not invent
"merge requires separate approval", "stop after qualification", or "preserve the
worktree" exceptions and then use those clauses to justify stopping. A narrower
handoff, PR-only path, required review, alternate target or preservation exception
must bind the exception's actual user instruction or repository policy. Repository
qualification/authority requirements still govern which changes are eligible for
integration; local Git integration does not grant runtime or semantic authority.

For a proved negative/inconclusive outcome, preserve and integrate the authorized
archive/evidence without promoting unqualified production changes. Retain rejected
candidate history through durable Git references when needed before retiring its
workspace; a negative disposition does not justify stranded evidence. Do not
merge failing implementation solely to satisfy cleanup. Recoverable failures keep
execution in progress through diagnosis/repair/retest.

Before claiming completion, prove the admitted implementation/evidence is present
on the intended target and required workspace cleanup actually occurred. An
exception remains visible with its originating instruction/policy and the exact
handoff achieved; never substitute it for the user's broader goal. Missing access,
mandatory review or unsafe cleanup follows the User Intervention Necessity Test.
Do not discard user-owned changes, unique evidence or externally managed worktrees.
