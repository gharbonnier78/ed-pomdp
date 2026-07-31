# Changelog

## v1.2.6-step2.6-experiment-harness-freeze-candidate — 2026-07-31
- Added the exact executable headline matrix: four regimes, four budgets, thirty common seeds, seven policies and 3,360 episode rows.
- Replaced mutable RNG consumption order in the simulator with named SHA-256 latent streams and a common-random-number observation tape indexed by acquisition step.
- Required fresh environment instances for each policy while preserving the same latent scenario and exogenous noise quantiles within a paired `(regime, budget, seed)` cell.
- Added a separate deterministic policy-local RNG stream and required a fresh policy instance for every experimental unit.
- Froze headline execution to fixed-horizon exact cost and prohibited early stopping from the confirmatory family.
- Added explicit configured `LossWeights` as a hashed experimental axis rather than relying on implicit defaults.
- Added raw episode records with pairing keys, policy-local seed, latent audit outcomes, observable history, posterior risk, terminal decision, realized loss, Brier score, residual risk and exact acquisition cost.
- Added raw-run metadata hashes and analysis-side validation that only the raw table and metadata may be uncommitted, paired cells share one latent scenario and the matrix is complete.
- Added fixed ten-bin ECE, deterministic 20,000-resample bootstrap summaries, seed-paired bootstrap contrasts and 50,000 within-seed label permutations.
- Recorded a held-out pre-freeze estimability review using seeds `100–129`, never the headline seeds `0–29`.
- Removed `unsafe_go_rate` from paired permutation testing after the held-out review showed near-zero cross-policy discordance under common random numbers; retained it as mandatory safety reporting for every cell.
- Reduced the confirmatory Holm family from 320 to 240 estimable hypotheses: five baselines × four regimes × four budgets × decision loss, Brier score and ECE.
- Added code-level rejection preventing the unsafe-GO endpoint from entering `paired_contrast` or Holm correction.
- Added ECE resolution diagnostics for distinct posterior values, populated bins and total bins, with explicit low-resolution interpretation at small budgets.
- Standardized all summary columns as observed `estimate`, `bootstrap_median`, `bootstrap_standard_deviation` and percentile confidence bounds; removed mixed raw/bootstrap dispersion semantics.
- Added a guarded headline runner that rejects missing/untracked manifests, unexpected dirty paths, non-descendant commits, hash drift, dimension drift, `LossWeights` drift, endpoint-registry drift, multiplicity drift, runtime drift and existing output files.
- Froze the analysis runtime to Python `3.12.13`, with no third-party headline dependency, and pinned test-only `pytest==9.1.1` in CI.
- Added a reduced end-to-end regression executing 210 episodes through policy execution, summaries, paired contrasts and Holm correction.
- Added a two-phase lock/manifest generator so the frozen-artifact commit and SHA-256 inventory are committed before any headline raw result can exist.
- Included the metric implementation, normative metric contract, preregistration and held-out pre-freeze power review in the frozen SHA-256 artifact inventory.
- Marked the executable JSON configuration as a freeze candidate pending reviewer approval; no final lock, final manifest or headline result is included yet.
- Kept `CLM-VOI-001` and `CLM-EQ-001` at evidence level `NONE`.

## v1.2.5-step2.5-policy-matrix — 2026-07-31
- Completed the seven preregistered acquisition policies with exact canonical names and deterministic registry ordering.
- Added entropy acquisition over the full joint belief `P(S,E | history)`.
- Added a risk-only baseline minimizing expected marginal system-state uncertainty without terminal loss weights.
- Added a classical POMDP baseline that maintains only `P(S | history)` and permanently marginalizes evidence quality at its prior.
- Preserved the fixed, seeded-random and failure-focused rule-based baselines under the common observable-only policy contract.
- Extended every policy with an observable `posterior_bad(history)` belief used by the shared stopping and terminal-decision runner.
- Ensured the runner applies common budget, stopping, Bayes terminal-action and realized-loss semantics while allowing the preregistered classical-versus-explicit-`E` inference contrast.
- Added regressions for full policy completeness, latent-state isolation, entropy semantics, risk-only semantics, classical non-learning from environment validation and classical/ED posterior divergence.
- Marked the machine-readable matrix as policy-complete but still pending Step 2.6 executable-matrix reconciliation and analysis freeze.
- Kept `CLM-VOI-001` and `CLM-EQ-001` at evidence level `NONE`; no headline experiment or superiority claim is produced.

## v1.2.4-step2.4-evidence-quality-mechanism — 2026-07-30
- Restored and strengthened the preregistered analysis-freeze commitment before any headline experiment.
- Required publication of the analysis Git commit SHA plus SHA-256 digests for the analysis entry point and locked dependency/configuration manifest.
- Required a dated freeze manifest under `benchmark/protocol/` to be committed before headline raw results are generated.
- Froze the entropy baseline as expected Shannon entropy reduction over the full joint belief `P(S,E | history)`.
- Froze the complete confirmatory multiplicity family and Holm family-wise error correction at `alpha = 0.05`.
- Reordered the remaining Step 2 increments so the evidence-quality/degradation mechanism precedes policy-matrix completion.
- Added a causal evidence model in which bad `E` destroys functional-channel discrimination while environment validation informs that reliability.
- Replaced the separate execution posterior with the same joint `P(S,E | history)` used by ED-POMDP look-ahead.
- Added identifiable, evidence-degraded and likelihood-misspecified executable regimes while retaining the deliberate non-identifiable regime.
- Added a regression where environment validation has gross decision VoI approximately `0.1898454746` and is selected over another functional acquisition.
- Added fixed-seed tests for causal relevance, observable regime separation, shared posterior semantics and absence of privileged latent-state access.
- Kept `CLM-VOI-001` and `CLM-EQ-001` at evidence level `NONE`; no headline policy-matrix result is claimed.

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
