# Step 2 Metric Contract

## Decision loss — confirmatory

For terminal decision `a` and latent state `s`, the benchmark reports the frozen loss `L(a,s)` plus the evidence-cost contribution. The explicit `LossWeights` are stored in `benchmark/config/headline_matrix.json` and repeated in the final analysis-freeze manifest. They cannot be changed after the freeze.

## Unsafe GO rate — mandatory safety reporting, non-inferential

Fraction of episodes where the policy selects GO while the latent system state is bad. The current synthetic headline matrix has no additional non-compensatory hard constraint beyond the latent unsafe state.

Unsafe GO is reported for every policy, regime and budget, including zero, null and adverse cells. It is deliberately excluded from paired permutation testing and Holm correction in this 30-seed common-random-number design because cross-policy discordance can be structurally near zero. No p-value or superiority claim is attached to this endpoint. A future inferential safety comparison requires a separately powered and preregistered design.

## Unnecessary NO-GO rate — secondary

Fraction of episodes where the policy selects NO-GO while the latent system state is good.

## Brier score — confirmatory

Mean squared error between posterior system-bad probability and the binary latent system outcome:

`(posterior_bad - true_system_bad)^2`.

## Expected calibration error — confirmatory with resolution diagnostics

Weighted absolute difference between mean predicted risk and empirical bad-system frequency over fixed equal-width bins:

`[0.0, 0.1), [0.1, 0.2), ..., [0.9, 1.0]`.

The final bin includes probability `1.0`. Empty bins contribute zero. Bin boundaries are frozen before execution and adaptive binning is prohibited in confirmatory analysis.

Because each cell contains 30 seeds and policy posteriors may have sparse discrete support, ECE can be low-resolution at small budgets. Every ECE summary therefore includes:

- `distinct_prediction_count`;
- `populated_bin_count`;
- `total_bin_count`.

The ten bins are retained rather than coarsened. Merging bins would change the estimand and could conceal posterior discreteness; sparse occupancy must instead remain visible and constrain interpretation.

## Residual risk — secondary

Posterior expected terminal consequence for the policy's final Bayes-optimal action, excluding realized ground truth and excluding evidence acquisition cost. It is computed from the policy-specific posterior without exposing latent state to the policy.

## Evidence cost — secondary and fairness invariant

Raw sum of acquisition costs consumed during an episode. The confirmatory matrix uses unit action cost and exact fixed horizons, so every policy consumes exactly its assigned budget. Early-stopping utilization is exploratory only.

## Acquisition count — secondary and fairness invariant

Number of evidence acquisitions. In headline runs this equals the integer budget by construction and is retained as an auditable invariant.

## Common-seed pairing

For each `(regime, budget, seed)` cell, all seven policies face fresh environment instances generated from the same latent and observation-noise tape. Raw results preserve the common seed, latent outcomes and policy-local seed so pairing can be independently verified.

## Uncertainty and inference

- Summary intervals use deterministic percentile bootstrap with `20,000` resamples.
- ED-POMDP-minus-baseline contrasts use seed-paired bootstrap intervals.
- Two-sided p-values use `50,000` within-seed policy-label permutations for confirmatory endpoints only.
- ECE is recomputed after every paired bootstrap resample or permutation.
- The complete confirmatory family contains `240` hypotheses.
- Holm step-down controls family-wise error at `alpha = 0.05`.
- Analysis RNG streams derive from frozen seed `20260731` plus the summary or contrast identifier.

## Reporting requirements

Every summary table includes regime, budget, policy, endpoint, inference role, observed `estimate`, `bootstrap_median`, `bootstrap_standard_deviation`, seed count and 95% percentile interval. ECE rows additionally report the three resolution diagnostics above; those fields are empty for other endpoints.

Every confirmatory contrast includes both policy values, ED-minus-baseline difference, paired 95% interval, raw p-value, Holm-adjusted p-value and rejection status. Confirmatory contrast tables contain only decision loss, Brier score and ECE. Unsafe GO appears in summary/safety reporting only and never receives a p-value. Raw episode-level outputs remain available for audit.
