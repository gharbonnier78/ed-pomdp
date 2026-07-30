# Step 2.4 Scope — Causal Evidence-Quality Mechanism

## Implemented mechanism

Latent evidence quality `E` now controls the reliability of the functional observation channel without becoming directly observable to any policy.

Under the fixed identifiable agent model:

- with good evidence quality, `P(functional fail | S=good, E=good) = 0.10`;
- with good evidence quality, `P(functional fail | S=bad, E=good) = 0.95`;
- with bad evidence quality, `P(functional fail | S, E=bad) = 0.60` for either system state;
- `P(environment-validation fail | E=good) = 0.20`;
- `P(environment-validation fail | E=bad) = 0.80`.

Bad evidence quality therefore destroys the functional channel's ability to distinguish good and bad systems and introduces a noisy failure bias. Environment validation informs the probability that existing and future functional observations are trustworthy.

## Planning and execution consistency

The episode runner and ED-POMDP look-ahead now use the same joint posterior `P(S,E | history)` implemented in `benchmark/runtime/decision.py`.

The policy receives only observation history and available channel names. It never receives true `S`, true `E`, the true evidence model or the simulator regime.

## Non-zero evidence-quality value of information

The regression configuration containing two successful functional observations demonstrates the required causal contrast.

Before another acquisition:

- posterior system risk is approximately `0.1434878587`;
- Bayes-optimal terminal risk is approximately `1.0022075055`.

For one environment-validation acquisition:

- expected terminal risk is approximately `0.8123620309`;
- gross decision VoI is approximately `0.1898454746`;
- expected loss including unit evidence cost is approximately `0.9123620309`.

For one additional functional acquisition:

- expected terminal risk is approximately `0.8788079470`;
- expected loss including unit evidence cost is approximately `0.9788079470`.

The ED-POMDP policy therefore selects `environment_validation` in this observable history. This is a unit-level mechanistic result only, not evidence for a headline superiority claim.

## Regimes

- `IDENTIFIABLE` uses the same conditional likelihood model assumed by the policy.
- `EVIDENCE_DEGRADED` increases the latent prevalence of bad evidence quality while preserving the same observation mechanism.
- `LIKELIHOOD_MISSPECIFIED` generates observations from a different fixed model that is not disclosed to the policy.
- `NON_IDENTIFIABLE` retains deliberate latent-state aliasing.

Tests verify that degraded and misspecified regimes produce observably distinct fixed-seed samples.

## Claim boundary

This increment makes the classical-POMDP-versus-ED-POMDP contrast operational for the later policy matrix. It does not execute the preregistered headline matrix and does not promote `CLM-VOI-001` or `CLM-EQ-001`; both remain at evidence level `NONE`.
