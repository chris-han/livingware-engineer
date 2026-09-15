# IA-Before-UI Engineering Gate

Use this gate before production UI implementation when a change introduces or materially changes a screen, route, workbench, navigation model, semantic control, panel, drawer, state surface, or ordinary user task flow.

This is an engineering-process gate, not a product-runtime governance gate and not a blanket human-approval requirement. A developer or agent may satisfy it mechanically by recording the review and clearing the stop conditions.

## Required review

Record:

- user task / job-to-be-done;
- primary domain objects and user-facing concepts;
- canonical semantic owner for every major state/action;
- proposed region hierarchy and placement rationale;
- ordinary Fast-to-Aha path to the first useful result;
- loading, empty, partial, stale, forbidden, error, retry/recovery, disabled/submitting and relevant lifecycle states;
- separation of navigation/selection from mutation, admission, activation, execution, or other authority-changing actions;
- shared primitives/patterns to reuse;
- compact-width, short-height, keyboard, localization, long-identifier and reduced-motion constraints where relevant;
- deterministic/browser evidence that will prove the implemented IA is structurally correct.

## Stop conditions

Disposition is `REVISE_IA` and production UI coding stops when any of these is unresolved:

- the user task or primary domain object cannot be stated clearly;
- implementation vocabulary is exposed where a domain concept should be used;
- two surfaces compete as semantic owner for the same object/state/action/lifecycle;
- a new shell, rail, drawer, uploader, viewer, selector, or control system duplicates an existing canonical owner without an explicit replacement decision;
- semantic controls are placed for renderer/layout convenience rather than point-of-use meaning;
- navigation/selection is conflated with semantic mutation or authority-changing action;
- required state/recovery behavior has no clear owner;
- responsive behavior would hide or ambiguously relocate a required semantic control;
- approval/configuration ceremony delays the first useful result without changing risk, authority, reversibility, or consequence;
- no verification method can distinguish structurally correct IA from a merely plausible screenshot.

When all applicable checks pass, disposition is `GO_FOR_UI` and implementation proceeds directly.

Pure visual-token corrections, implementation-only refactors, renderer-performance work, and accessibility fixes that do not alter information architecture may record `NOT_APPLICABLE` with one sentence of rationale.

## Combined development sequence

IA and verification impact analysis solve different problems and should be composed rather than substituted for one another:

```text
requirement / problem
  -> architecture + semantic-owner impact
  -> IA-before-UI review (when user-facing IA changes)
  -> implementation plan
  -> implementation / focused TDD
  -> Verification Impact Analysis from observed production impact radius
  -> smallest sufficient integration/browser/E2E evidence
  -> completion claim
```

IA-before-UI asks whether we are implementing the right user-facing structure. Verification Impact Analysis asks how much evidence the resulting code change needs. Neither implies running a broad suite or requesting human approval by default.
