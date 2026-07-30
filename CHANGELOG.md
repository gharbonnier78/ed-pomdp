# Changelog

## v1.2.3-step2.3-voi-policy — 2026-07-30
- Added an observable-history posterior over joint system and evidence-quality hypotheses.
- Added a fixed-model one-step look-ahead acquisition policy minimizing expected terminal decision loss plus evidence cost.
- Added tests for joint-posterior semantics, decision-relevant channel selection and absence of privileged latent-state inputs.
- Explicitly limited this increment to the first executable decision-aware VoI policy; evidence quality does not yet alter terminal loss or functional-channel reliability.
- Kept `CLM-VOI-001` and `CLM-EQ-001` at evidence level `NONE`; no matched-budget headline result or calibration claim is produced.

## v1.2.2-step2.2-decision-loop — 2026-07-30
- Added terminal `GO`, `NO_GO` and `CONDITIONAL_GO` decisions.
- Added an observable-only Bayesian posterior baseline over system risk.
- Added threshold-based stopping that may leave budget unspent.
- Added asymmetric terminal loss, evidence cost, unsafe-GO and unnecessary-NO-GO endpoints.
- Replaced equal-spend validation with budget-ceiling validation for stopping policies.
- Deliberately fixed the inference model to the identifiable functional-channel likelihoods so non-identifiable and misspecified environments can be evaluated as robustness tests rather than silently changing the agent model.
- Kept `CLM-VOI-001` and `CLM-EQ-001` at evidence level `NONE`; the final ED-POMDP policy and headline matched-budget experiment are not yet implemented.

## v1.2.1-step2.1-execution-core — 2026-07-30
- Added a deterministic synthetic release simulator with explicit latent system and evidence-quality states.
- Implemented identifiable and deliberately non-identifiable observation regimes aligned with the identifiability note.
- Added observable-only fixed, random and failure-focused acquisition policies.
- Added a matched-budget episode runner and invariant validation.
- Added tests for seed stability, budget equality and absence of privileged latent-state inputs.
- Explicitly limited this increment to acquisition-runtime validation: no stopping decision, terminal GO/NO-GO action or decision-loss endpoint is implemented yet.
- Kept `CLM-VOI-001` and `CLM-EQ-001` at evidence level `NONE`; this increment does not exercise or validate decision-aware Value of Information.

## v1.2.0-step2-scaffold — 2026-07-30
- Opened Step 2 as a separate matched-budget quantitative-validation increment.
- Added benchmark families for identifiable, weakly identifiable and non-identifiable regimes.
- Added evidence degradation, channel dependence and likelihood misspecification regimes.
- Added ED-POMDP and six baseline policy definitions.
- Added a preregistration for `CLM-VOI-001` and `CLM-EQ-001` with explicit refutation criteria.
- Added machine-readable benchmark configuration and an auditable metric contract.
- Added policy and matched-budget software interfaces.
- Kept both empirical claims at evidence level `NONE`; no result is claimed by this scaffold.

## v1.1.0-step1.1 — 2026-07-30
- Added a formal S/E identifiability note with non-identifiability, heterogeneous-evidence and controlled-intervention cases.
- Added worked numeric non-identifiability and heterogeneous-channel separation cases so `CLM-IDENT-001` legitimately satisfies the `FORMAL` evidence label.
- Added an explicit intervention noise floor for imperfectly controlled reruns.
- Promoted `docs/CLAIMS.md` to the canonical epistemic registry.
- Added machine-readable claim registries in CSV and JSON.
- Added epistemic governance and anti-drift rules.
- Added the mandatory Data Readiness Gate with READY, PARTIALLY_READY and NOT_READY paths.
- Re-scoped the programme into Committed Core, Conditional Industrial and North-Star tracks.
- Added a claim traceability matrix.
- Standardized milestone numbering as Step 1, Step 1.1, Step 2, Step 3 and Step 4.
- Added README PDF shortcut buttons consistent with the author's other research repositories.
- No empirical superiority or industrial-validation claim added.

## v1.0.0-step1 — 2026-07-30
- Repositioned software release as the primary validation domain.
- Added explicit non-claims and identifiability research question.
- Added matched-budget hypotheses with refutation criteria.
- Added hard-constraint semantics and evidence-quality latent state.
- Added research programme, survey, reviewer companion, ontology, and appendix.
