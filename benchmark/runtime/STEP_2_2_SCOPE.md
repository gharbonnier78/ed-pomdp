# Step 2.2 Scope and Model-Misspecification Boundary

## Implemented

Step 2.2 adds a stopping-capable decision loop with terminal `GO`, `NO_GO` and `CONDITIONAL_GO` decisions, asymmetric terminal loss, evidence cost and preregistered decision endpoints.

## Fixed agent model

The Bayesian agent deliberately assumes the identifiable functional-channel likelihoods:

- `P(fail | system_bad) = 0.80`
- `P(fail | system_good) = 0.20`

These likelihoods are fixed and are not selected from the simulator's true regime.

## Why this is deliberate

Future runs against non-identifiable, mildly misspecified or severely misspecified data-generating environments are intended to test robustness of a fixed inference model. The agent must not receive the true regime or silently adapt its likelihoods to the environment, because that would leak privileged information and invalidate the misspecification experiment.

A degraded result outside the identifiable regime must therefore be interpreted as a robustness outcome under model mismatch, not as an omitted regime-aware posterior implementation.

## Scientific boundary

Step 2.2 does not implement the final evidence-quality-aware ED-POMDP policy and does not execute the preregistered headline comparison. No Step 2.2 output may promote `CLM-VOI-001` or `CLM-EQ-001` from `NONE`.
