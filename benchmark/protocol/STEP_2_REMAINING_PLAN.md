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

Implemented, reviewed and merged:

- fixed alternating plan;
- seeded random acquisition;
- failure-focused rule-based assurance;
- entropy acquisition over the full joint belief `P(S,E | history)`;
- risk-only acquisition minimizing expected marginal system uncertainty;
- classical POMDP with evidence quality permanently marginalized at its prior;
- ED-POMDP decision-aware VoI over the explicit joint belief;
- canonical seven-policy registry with exact preregistered names and ordering;
- common observable input, channel access and terminal loss semantics;
- policy-specific observable posterior support in the shared decision runner;
- regressions proving that the classical model cannot recalibrate from environment validation while ED-POMDP can.

The definitions, invariants and claim boundary are documented in `benchmark/runtime/STEP_2_5_SCOPE.md`.

## Step 2.6 — Reproducible experiment harness and analysis freeze

Implemented on the Step 2.6 branch as a freeze candidate:

- exact executable matrix of four regimes × four budgets × thirty common seeds × seven policies (`3,360` episode rows);
- common-random-number scenario tape keyed by episode seed, with fresh environment instances for each policy;
- separate deterministic policy-local RNG stream and fresh policy instance per experimental unit;
- fixed-horizon exact-cost headline execution with early stopping prohibited;
- explicit frozen `LossWeights` axis;
- raw episode schema containing policy prediction, decision, realized loss, pairing keys, latent outcomes and acquisition trace;
- fixed implementations for decision loss, unsafe GO, Brier score and ten-bin ECE;
- deterministic paired bootstrap intervals, within-seed randomization p-values and complete-family Holm correction;
- guarded runner that rejects missing/untracked manifests, dirty trees, non-descendant commits, hash drift, dimension drift and `LossWeights` drift;
- two-phase lock/manifest generator that guarantees the final manifest is committed before raw headline results exist.

Deliberately not completed before review:

- `benchmark/config/headline_matrix.json` remains `freeze_candidate_not_executable`;
- `benchmark/config/FROZEN_ARTIFACTS.json` has not yet been generated;
- `benchmark/protocol/ANALYSIS_FREEZE.json` has not yet been generated;
- no headline raw result exists.

After reviewer approval, finalization is mechanical:

1. mark the executable config `frozen` and commit all accepted code/configuration;
2. generate and commit the frozen-artifact lock;
3. generate and commit the dated analysis-freeze manifest referencing the lock commit;
4. verify CI and merge Step 2.6;
5. execute Step 2.7 only from a clean descendant of the frozen commit.

## Step 2.7 — Preregistered runs and statistical analysis

- execute exactly the `3,360` frozen episode rows;
- preserve raw episode-level results and run metadata hashes;
- generate policy summaries and `320` corrected confirmatory contrasts;
- retain failed, null and adverse configurations;
- label all non-frozen analyses exploratory.

## Step 2.8 — Claim review and Step 2 close-out

- review refutation criteria before promotion;
- synchronize Markdown, CSV and JSON claim registries;
- publish reproducibility artifacts and analysis-freeze identifiers;
- close Step 2 only after independent statistical and epistemic review.
