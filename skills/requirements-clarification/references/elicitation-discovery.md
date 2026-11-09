# Discovering needs in context

Use this reference when the current need or practice is tacit, a requested mechanism lacks a clear outcome, a material boundary/constraint or role/scenario may be missing, or requirement satisfaction may not establish the intended outcome. The [shared requirements workflow](requirements-workflow.md) remains the owner of source, disposition, authority, continuity and stopping rules.

## Build context from the operating situation

Use only the dimensions that can change the named decision; this table is a discovery aid, not a new output schema.

| Dimension | Recover when material |
|---|---|
| Outcome and choice | Whose outcome matters, what decision is next, and which live alternatives the evidence distinguishes |
| Boundary and control | The system of interest, what may actually be changed, external actors/interfaces, resource dependencies and relevant lifecycle conditions |
| Physical and capability limits | Applicable law/model, measured or specified capacity, environment, timing and resource limits; preserve source, units, conditions and uncertainty |
| Institutions and relationships | Applicable policy/contract, decision rights, responsibilities, incentives and dependencies on other people or organizations |
| Culture and tacit practice | Concrete routines, workarounds, informal coordination, expertise and differing interpretations; distinguish an account of practice from a binding rule |
| Uncertainty | What remains unknown or disputed, why it matters to this decision, and the smallest useful evidence action |

Do not classify every contextual fact as a constraint. A practice can explain resistance, delay or successful coordination without being an authorized requirement. A formal rule can remain binding even when people report ignoring it. Preserve both kinds of evidence and the discrepancy.

Tacit knowledge may emerge through examples, artifacts, demonstrations or authorized observation as well as questions. Record what was observed, what a participant explained and what the agent inferred separately. Do not promise that all know-how can be verbalized, infer consensus from silence, or generalize one account into a cultural rule.

## Select an evidence action

Start with the uncertainty that can change the next decision and the evidence already available. Choose the least burdensome action likely to distinguish the live alternatives. Reassess after its result; do not run every technique or generate a numerical information-gain score.

| Current uncertainty | Useful action | Evidence and claim boundary |
|---|---|---|
| A solution is requested without a clear desired change | Ask about the decision or outcome and one concrete recent episode | Keep the proposed mechanism distinct from the underlying need; preserve an already mandated mechanism |
| Familiar work is hard to articulate | Inspect relevant logs, forms or examples, then request a targeted walkthrough or authorized observation if needed | A reported procedure, an observed episode and an inferred need are different kinds of evidence; one episode does not establish prevalence |
| Stakeholders describe incompatible outcomes | Compare a concrete shared scenario and the consequences of alternatives | Preserve disagreement and actual decision authority; do not infer consensus from a coherent proposal |
| Interaction behavior is uncertain | Use a small scenario, sketch or prototype when it can resolve that uncertainty | A proposed prototype is not observed behavior; a liked mockup does not approve every implied requirement |
| A quality target or bottleneck is unknown | Inspect the available baseline or use a bounded measurement/probe | Do not invent target values, subtract incomparable time measures or claim improvement without a comparable basis |
| Success depends on external people or systems | Examine the relevant handoff, operating condition or failure case | Separate system obligations from environmental assumptions and responsibility that has actually been assigned |
| Formal procedure and actual work diverge | Compare the applicable rule with a concrete episode and relevant participants' accounts | Preserve disagreement; observed custom can affect feasibility without conferring authority or proving its cause |

Ask only a question whose alternatives still change the next decision after reusing existing evidence. Apply the shared workflow's [token-economy rules](requirements-workflow.md#token-economy-required); expand only for the requested deliverable or required context. If evidence is sufficient for the named step, return to the owning workflow.

## Detect a consequential omission

When a missing participant or lifecycle condition could change a requirement, examine that specific omission. For an unattended import, for example, an operations team that handles failed runs may supply a material recovery need even though it did not request the feature. Use existing operating evidence before asking for new input.

Choose relevant stages rather than an exhaustive lifecycle inventory. A single-user bounded change does not need additional stakeholders or a workshop by default. Preserve domain interpretation and actual authority at their existing owners.

## Check the outcome with a counterexample

For a material outcome claim, ask: could all requirement checks pass while the intended outcome still fails?

For a hypothetical dispatch-delay problem, all software checks may pass while loading capacity, a carrier's schedule, delegated decision rights or an informal handover practice still prevents the desired outcome. These are possible explanations, not findings about a real site. Identify the premise that matters, inspect the smallest relevant evidence, and retain uncertainty where it remains.

Carry a discovered obstacle, environmental assumption or proposed mitigation into the existing requirement basis and affected acceptance criteria. Do not silently add implementation scope or convert an inferred need into an accepted requirement. Preserve readiness for a reversible learning step when that is sufficient.

## Research basis and adoption limits

The method-selection table and operating checks are engineering synthesis. They are not a validated ranking of techniques, a standards-compliance checklist or evidence of improved Livingware agent behavior. Book scope was checked against publisher descriptions; the research findings below remain bounded by their study settings.

- **Ian F. Alexander and Ljerka Beus-Dukic (2009), _Discovering Requirements: How to Specify Products and Services_. Wiley, ISBN 9780470712405.** Supports complementary stakeholder, goal, context, scenario, risk and rationale techniques. Adopt contextual discovery rather than a fixed interview script. [Publisher](https://www.wiley.com/en-us/discovering-requirements-how-to-specify-products-and-services-p-9780470712405)
- **Louis S. Wheatcraft, Michael J. Ryan and Tami Edner Katz (2024 publication listing), _INCOSE Needs and Requirements Manual: Needs, Requirements, Verification, Validation Across the Lifecycle_. Wiley, ISBN 9781394152742.** Supports linking needs and requirements to lifecycle concepts, stakeholders, verification and validation. Adopt only checks material to the current decision; professional guidance is not an experimental performance result. [Publisher](https://www.wiley.com/en-us/incose-needs-and-requirements-manual-needs-requirements-verification-validation-across-the-lifecycle-p-9781394152742)
- **Axel van Lamsweerde (2001), _Goal-Oriented Requirements Engineering: A Guided Tour_. RE 2001.** Supports goals, environmental assumptions, refinement, conflict and obstacle reasoning. Adopt the outcome-adequacy question; the methodological cases do not establish a universal improvement percentage. [Author's paper](https://webperso.info.ucl.ac.be/~avl/files/RE01.pdf)
- **Dante Carrizo, Oscar Dieste and Natalia Juristo (2017), _Contextual attributes impacting the effectiveness of requirements elicitation techniques: Mapping theoretical and empirical research_. Information and Software Technology 92, 194-221. DOI: 10.1016/j.infsof.2017.08.003.** Supports context-sensitive selection while documenting limited empirical support for detailed selection rules. Do not treat this reference's table as an empirically proven matching algorithm. [Primary article](https://doi.org/10.1016/j.infsof.2017.08.003)
- **Alessio Ferrari, Paola Spoletini and Sourav Debnath (2022), _How do requirements evolve during elicitation? An empirical study combining interviews and app store analysis_. Requirements Engineering 27, 489-519. DOI: 10.1007/s00766-022-00383-7.** Supports the interpretation that interaction can develop requirements. The exploratory student-analyst, fictional-customer and software/app setting does not establish a general industrial rate or authorize accepting analyst suggestions. [Primary article](https://doi.org/10.1007/s00766-022-00383-7)

- **NASA, _Systems Engineering Handbook_, sections 4.1 and 4.2.** Supports eliciting external interfaces, assumptions and constraints, establishing the design boundary, and considering physical/functional interfaces and operating conditions. The constraint distinctions above are engineering synthesis, not NASA's prescribed schema or evidence of agent improvement. [Stakeholder expectations](https://www.nasa.gov/reference/4-1-stakeholder-expectations-definition/) · [Technical requirements](https://www.nasa.gov/reference/4-2-technical-requirements-definition/)
- **Peter Checkland and John Poulter (2010), _Soft Systems Methodology_.** Supports learning about problematic real-world situations through multiple purposeful perspectives and discussion toward improvement. Use this to examine social interpretations and feasible action; it does not turn custom or influence into legitimate authority. [Authors' chapter](https://doi.org/10.1007/978-1-84882-809-4_5)
- **Michael Polanyi, _The Tacit Dimension_ (University of Chicago Press edition, 2009).** Supports the limits of verbal accounts of practical knowledge. Choosing episodes, artifacts or observation is our engineering application, not a validated elicitation protocol attributed to the book. [Publisher](https://press.uchicago.edu/ucp/books/book/chicago/T/bo6035368.html)
