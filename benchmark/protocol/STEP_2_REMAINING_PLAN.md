# Step 2 Remaining Plan

## Ordering decision

Step 2.4 preceded policy-matrix completion because the central contrast between a classical POMDP without explicit `E` and ED-POMDP was not meaningful while evidence quality had no causal effect on observation reliability, calibration, governed constraints or terminal loss.

Under the former Step 2.3 model, `environment_validation` changed only the marginal belief over `E`; it did not change the marginal belief over `S` or terminal decision risk. Its decision VoI was therefore zero, and the two central policies could collapse to identical behavior.

## Step 2.4 — Evidence-quality and degradation mechanism

Implemented and merged:

- `E` controls functional-channel discrimination without being exposed to the policy;
- the runner and look-ahead share one joint posterior `P(S,E | history)`;
- environment-validation observations can recalibrate system risk after functional evidence;
- identifiable, evidence-degraded, likelihood-misspecified and non-identifiable regimes are executable;
- fixed-seed tests show the degraded and misspecified regimes are observably distinct;
- a regression configuration with two successful functional observations gives environment validation gross decision VoI of approximately `0.1898454746`;
- in that configuration the ED-POMDP policy selects environment validation over another functional acquisition;
- no claim promotion occurs.

The model, numeric regression and claim boundary are documented in `benchmark/runtime/STEP_2_4_SCOPE.md`.

## Step 2.5 — Policy matrix completion

Implemented on the Step 2.5 branch:

- fixed alternating plan;
- seeded random acquisition;
- failure-focused rule-based assurance;
- entropy acquisition over the full joint belief `P(S,E | history)`;
- risk-only acquisition minimizing expected marginal system uncertainty;
- classical POMDP with evidence quality permanently marginalized at its prior;
- ED-POMDP decision-aware VoI over the explicit joint belief;
- canonical seven-policy registry with exact preregistered names and ordering;
- common observable input, channel access, stopping rule and terminal loss semantics;
- policy-specific observable posterior support in the shared decision runner;
- regressions proving that the classical model cannot recalibrate from environment validation while ED-POMDP can.

The definitions, invariants and claim boundary are documented in `benchmark/runtime/STEP_2_5_SCOPE.md`.

## Step 2.6 — Reproducible experiment harness and analysis freeze

Next increment, before headline execution:

- freeze the complete executable regime × budget × policy matrix;
- reconcile scaffold regime labels with the four implemented simulator regimes;
- freeze primary and secondary metric implementations;
- define the matched-budget headline runner, including explicit treatment of early stopping and equal total acquisition cost;
- freeze the confirmatory multiplicity family and Holm correction;
- commit the analysis scripts and locked dependency/configuration manifest;
- publish the Git commit SHA and SHA-256 hashes in a dated analysis-freeze manifest;
- reject headline execution when the working tree or hashes do not match the manifest.

## Step 2.7 — Preregistered runs and statistical analysis

- run at least 30 independent seeds per frozen configuration;
- preserve raw episode-level results;
- compute paired contrasts, confidence intervals and corrected primary inferences;
- retain failed, null and adverse configurations;
- label all non-frozen analyses exploratory.

## Step 2.8 — Claim review and Step 2 close-out

- review refutation criteria before promotion;
- synchronize Markdown, CSV and JSON claim registries;
- publish reproducibility artifacts and analysis-freeze identifiers;
- close Step 2 only after independent statistical and epistemic review.
