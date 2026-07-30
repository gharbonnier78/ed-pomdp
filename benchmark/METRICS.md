# Step 2 Metric Contract

## Decision loss

For terminal decision `a` and latent state `s`, the benchmark reports the preregistered loss `L(a,s)`. Loss tables are versioned configuration artifacts and cannot be changed after results are inspected.

## Unsafe GO rate

Fraction of episodes where the policy selects GO while the latent state belongs to a preregistered unsafe set or a hard release constraint is unsatisfied.

## Unnecessary NO-GO rate

Fraction of episodes where the policy selects NO-GO while the latent state is releasable under the preregistered decision model.

## Brier score

Mean squared error between predicted release-risk probabilities and binary outcome indicators. Multiclass experiments must use the multiclass Brier score and declare the class mapping.

## Expected calibration error

Weighted absolute difference between confidence and empirical frequency over preregistered bins. Bin boundaries and adaptive/fixed binning must be declared before execution.

## Residual risk

Posterior expected consequence remaining at terminal decision, computed without exposing latent ground truth to the policy.

## Evidence cost

Sum of acquisition costs consumed during an episode. Matched-budget comparisons require equal maximum cost and report actual utilization.

## Hard-constraint violations

Count and rate of terminal actions forbidden by non-compensatory constraints. The expected value is exactly zero for a compliant constrained policy.

## Reporting requirements

Every metric table must include configuration ID, policy, budget, seed count, mean, dispersion and 95% confidence interval. Raw episode-level outputs remain available for audit.