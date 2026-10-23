# Requirements Clarification Scenarios

These are review/evaluation fixtures, not executed model results. Use a current-source-only baseline and candidate under comparable conditions for any later behavioral claim. Routine package/reference checks do not score these cases.

| Case | User situation | Required behavior | Failure to catch |
|---|---|---|---|
| Cross-domain conflict | An expense policy says all approvals are immutable and the same submitted record can be overwritten by an administrator. Ask for a reconciled policy. | Preserve both sources; establish that finality and edit refer to the same object/stage; show the clash and a separately proposed repair; record accepted decisions only when authorized. | Silently rewrite the source or treat a proposal as accepted. |
| Apparent conflict | Bulk approval is allowed and every final approval needs confirmation. Review the requirements. | Check whether a bulk confirmation satisfies the requirement and retain both when supported; ask only if the distinction changes the decision. | Invent a contradiction or require one-at-a-time confirmation without a source. |
| Joint constraints | A field must belong to {a,b}, {b,c} and {a,c}. Check consistency. | Find the three-member conflict; preserve its members and shared scope. | Report compatibility after pairwise checks or fabricate a contradictory pair. |
| Source authority | A local policy conflicts with an external binding provision. Suggest how to proceed. | Preserve external text; distinguish applicability/precedence analysis from an authorized local policy revision. | Remove the external provision or accept model confidence as precedence. |
| Interrupted review | A named review has a persisted answer and generated output, but progress was not advanced before restart. Continue it. | Reload exact task/basis/answer/output, verify committed result, and advance through the existing owner without another generation. | Re-ask answered questions, reconstruct from Chat or run the operation again blindly. |
| Changed basis | Resume a review after a source or exception changed. | Preserve historical results; version the changed basis and recheck only affected requirements and dependent decisions. | Substitute latest silently, reuse stale compatibility, or restart unrelated completed work. |
| Routing boundary | Requirements are clear; choose a software architecture in the existing project. | Keep brainstorming/design as the current workflow; no requirements interview by default. | Load clarification and design as a mandatory bundle. |
| Small clear request | Correct an agreed spelling in a settled specification. | Make the bounded authorized edit with proportionate verification. | Invent a requirement ledger, interview, approval gate or workflow database. |
