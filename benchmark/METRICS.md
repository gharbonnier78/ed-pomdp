# Step 2 Metric Contract

## Decision loss

For terminal decision `a` and latent state `s`, the benchmark reports the frozen loss `L(a,s)` plus the evidence-cost contribution. The explicit `LossWeights` are stored in `benchmark/config/headline_matrix.json` and repeated in the final analysis-freeze manifest. They cannot be changed after the freeze.

## Unsafe GO rate

Fraction of episodes where the policy selects GO while the latent system state is bad. The current synthetic headline matrix has no additional non-compensatory hard constraint beyond the latent unsafe state.

## Unnecessary NO-GO rate

Fraction of episodes where the policy selects NO-GO while the latent system state is good.

## Brier score

Mean squared error between posterior system-bad probability and the binary latent system outcome:

`(posterior_bad - true_system_bad)^2`.

## Expected calibration error

Weighted absolute difference between mean predicted risk and empirical bad-system frequency over fixed equal-width bins:

`[0.0, 0.1), [0.1, 0.2), ..., [0.9, 1.0]`.

The final bin includes probability `1.0`. Empty bins contribute zero. Bin boundaries are frozen before execution and adaptive binning is prohibited in confirmatory analysis.

## Residual risk

Posterior expected terminal consequence for the policy's final Bayes-optimal action, excluding realized ground truth and excluding evidence acquisition cost. It is computed from the policy-specific posterior without exposing latent state to the policy.

## Evidence cost

Raw sum of acquisition costs consumed during an episode. The confirmatory matrix uses unit action cost and exact fixed horizons, so every policy consumes exactly its assigned budget. Early-stopping utilization is exploratory only.

## Acquisition count

Number of evidence acquisitions. In headline runs this equals the integer budget by construction and is retained as an auditable invariant.

## Common-seed pairing

For each `(regime, budget, seed)` cell, all seven policies face fresh environment instances generated from the same latent and observation-noise tape. Raw results preserve the common seed, latent outcomes and policy-local seed so pairing can be independently verified.

## Uncertainty and inference

- Summary intervals use deterministic percentile bootstrap with `20,000` resamples.
- ED-POMDP-minus-baseline contrasts use seed-paired bootstrap intervals.
- Two-sided p-values use `50,000` within-seed policy-label permutations.
- ECE is recomputed after every paired bootstrap resample or permutation.
- The complete confirmatory family contains `320` hypotheses.
- Holm step-down controls family-wise error at `alpha = 0.05`.
- Analysis RNG streams derive from frozen seed `20260731` plus the summary or contrast identifier.

## Reporting requirements

Every summary table includes regime, budget, policy, endpoint, value, median, standard deviation, seed count and 95% interval. Every confirmatory contrast includes both policy values, ED-minus-baseline difference, paired 95% interval, raw p-value, Holm-adjusted p-value and rejection status. Raw episode-level outputs remain available for audit.
