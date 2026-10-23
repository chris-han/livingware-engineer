---
name: requirements-clarification
description: Use when requirements, stakeholder requests, policies, rules, or specifications contain material missing information, ambiguity, conflicting constraints, or unresolved changes. Do not use for simple copyediting, an already settled implementation request, or software architecture choices whose requirements are clear.
---

# Requirements Clarification

Turn source-backed requests into a sufficiently explicit, consistent requirement basis for the next decision. Apply this across domains; a PRD, policy, contract, rule list, source-to-model task, or operational request can all contain interacting requirements.

## Entry and ownership

Read [the shared requirements workflow contract](references/requirements-workflow.md). Locate the current requirement source and its owner before eliciting more information. Domain skills keep domain interpretation, legal authority, execution, and admission/activation ownership.

Enter at the actual unresolved state: elicit missing intent, clarify meaning, test compatibility, reconcile a change, or recover an interrupted review. Do not restart the whole interview for each state.

## Workflow

1. Preserve the original requests and their source/version references; separate explicit requirements, interpretations, assumptions, and proposals.
2. Make material actors, outcomes, scope, conditions, exceptions, time and acceptance observations explicit enough to compare requirements.
3. Check relevant requirements together before polishing their wording. Distinguish a verified contradiction, a suspected conflict, ambiguity, incomplete coverage and a supported exception or precedence resolution.
4. Resolve from existing authority/evidence and standing delegation first. Ask the smallest decision-changing question only when user-owned input is still necessary; continue independent safe work.
5. Record the disposition and rationale at the existing owner. Treat a proposed repair separately from an accepted change, preserve unresolved items, and recheck affected requirements after a material answer or edit.
6. For work that spans interruption, sessions, waiting or consequential effects, recover from the authoritative task/artifact basis under the shared continuity contract. Reuse committed results and exact versions.

## Exit and handoff

Exit when the next bounded decision has a sufficient requirement basis, or when a specific unresolved item genuinely prevents it. Preserve effective requirement refs, accepted changes, remaining assumptions/questions, affected actions, acceptance criteria and the next decision in the existing owner. Do not create a second ledger.

Return to the calling domain workflow. Software design decisions belong to `brainstorming`; implementation planning belongs to `writing-plans` after their own entry conditions are met. Do not load them as a default bundle.

A finding is not a disposition, a disposition is not execution authority, and resuming work does not grant new authority.
