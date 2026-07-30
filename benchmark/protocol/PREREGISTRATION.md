# Step 2 Preregistration

## Claims under test

### CLM-VOI-001
Decision-aware value of information reduces matched-budget decision loss relative to fixed, random, entropy and risk-only acquisition policies.

### CLM-EQ-001
Explicit modelling of evidence-production quality improves calibration and decision loss under evidence degradation and likelihood misspecification.

## Experimental unit

One simulated release-decision episode with sampled latent state, evidence-quality state, observation history, acquisition sequence and terminal decision.

## Matched-budget rule

All policies receive the same episode-level budget. Comparisons are invalid if policies differ in total acquisition cost, permitted channels, stopping horizon or access to ground-truth variables.

## Primary endpoints

1. Mean decision loss
2. Unsafe GO rate
3. Brier score
4. Expected calibration error

## Secondary endpoints

- unnecessary NO-GO rate
- residual risk at decision
- evidence cost consumed
- number of acquisitions
- hard-constraint violations
- decision latency in simulator steps

## Planned contrasts

- ED-POMDP vs fixed policy
- ED-POMDP vs random policy
- ED-POMDP vs entropy policy
- ED-POMDP vs risk-only policy
- ED-POMDP vs classical POMDP without explicit `E`

## Statistical protocol

- at least 30 independent seeds per preregistered configuration;
- report means, medians, standard deviations and 95% confidence intervals;
- report paired effect sizes where common seeds are used;
- correct for multiple primary comparisons;
- retain all failed and null configurations;
- publish configuration files and raw result tables.

## Refutation criteria

`CLM-VOI-001` is not supported if ED-POMDP shows no material reduction in matched-budget decision loss over the strongest baseline, or if gains disappear under confidence intervals and robustness checks.

`CLM-EQ-001` is not supported if explicit evidence-quality modelling fails to improve calibration or decision loss under preregistered degradation regimes, or if improvement depends only on privileged access to the true latent `E`.

## Claim-governance rule

This protocol does not promote either claim beyond `NONE`. Promotion requires completed runs, reproducible artifacts, statistical review and synchronized updates to `docs/CLAIMS.md`, CSV and JSON registries.