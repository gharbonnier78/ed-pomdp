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

## Entropy baseline definition

The preregistered entropy baseline maximizes expected reduction in Shannon entropy of the full joint belief `P(S,E | history)`, not the marginal belief over `S` alone.

This deliberately represents uncertainty-seeking rather than decision-aware acquisition. It may spend evidence budget reducing uncertainty about `E` even when that information has little or no terminal decision value. That behavior is part of the intended contrast with ED-POMDP and must not be changed after headline runs begin.

## Statistical protocol

- at least 30 independent seeds per preregistered configuration;
- report means, medians, standard deviations and 95% confidence intervals;
- report paired effect sizes where common seeds are used;
- retain all failed and null configurations;
- publish configuration files and raw result tables.

### Confirmatory multiplicity family

The confirmatory family contains every preregistered ED-POMDP-versus-baseline contrast for all four primary endpoints, across every preregistered regime and budget included in the frozen headline matrix.

Family-wise error is controlled at `alpha = 0.05` using the Holm step-down correction over that complete family. Secondary endpoints and any analysis outside the frozen family are descriptive or exploratory and must be labelled accordingly.

Neither the family definition, the included configurations nor the correction method may be changed after the analysis freeze without recording a protocol deviation and treating the affected results as exploratory.

## Analysis freeze and script hash

Before any headline experiment is executed:

1. the final analysis scripts, metric implementation and frozen experiment matrix must be committed;
2. the repository must publish the Git commit SHA and SHA-256 digest of the analysis entry-point script and its locked dependency/configuration manifest;
3. those identifiers must be recorded in a dated analysis-freeze manifest under `benchmark/protocol/`;
4. headline raw results must be generated only after that manifest is committed.

Any later script or configuration change requires a new hash, an explicit protocol-deviation record and reclassification of affected analyses as exploratory unless the full headline experiment is rerun from the new frozen version.

## Refutation criteria

`CLM-VOI-001` is not supported if ED-POMDP shows no material reduction in matched-budget decision loss over the strongest baseline, or if gains disappear under confidence intervals and robustness checks.

`CLM-EQ-001` is not supported if explicit evidence-quality modelling fails to improve calibration or decision loss under preregistered degradation regimes, or if improvement depends only on privileged access to the true latent `E`.

## Claim-governance rule

This protocol does not promote either claim beyond `NONE`. Promotion requires completed runs, reproducible artifacts, statistical review and synchronized updates to `docs/CLAIMS.md`, CSV and JSON registries.
