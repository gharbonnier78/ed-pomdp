# Step 2 Benchmark

This directory contains the quantitative validation increment for ED-POMDP.

## Objective

Evaluate whether decision-aware evidence acquisition and explicit evidence-quality modelling improve software-release decisions under strictly matched budgets.

## Scope

The benchmark controls:

- latent system state `S`;
- latent evidence-quality state `E`;
- observation channels and dependence structure;
- evidence degradation and likelihood misspecification;
- acquisition cost and total budget;
- decision loss and hard constraints.

## Current executable state

The runtime now includes:

- a causal evidence-production model in which latent `E` controls functional-channel reliability;
- a shared joint posterior `P(S,E | history)` for the runner and ED-POMDP look-ahead;
- identifiable, evidence-degraded, likelihood-misspecified and deliberately non-identifiable regimes;
- a tested observable history in which environment validation has non-zero decision VoI.

See:

- `runtime/STEP_2_4_SCOPE.md` for the causal model and numeric regression;
- `protocol/STEP_2_REMAINING_PLAN.md` for the remaining Step 2 sequence;
- `protocol/PREREGISTRATION.md` for the frozen confirmatory protocol.

## Benchmark families

1. Identifiable regimes
2. Weakly identifiable regimes
3. Structurally non-identifiable regimes
4. Evidence degradation regimes
5. Correlated-channel regimes
6. Hard-constraint regimes

## Policies

- ED-POMDP decision-aware VoI
- classical POMDP without explicit evidence-quality state
- entropy-reduction acquisition
- fixed acquisition plan
- random acquisition
- risk-only heuristic
- rule-based assurance baseline

## Primary metrics

- expected decision loss
- unsafe GO rate
- unnecessary NO-GO rate
- Brier score
- expected calibration error
- residual risk
- evidence cost
- hard-constraint violations

No headline empirical claim is made by the current runtime increments. Claim maturity changes only after preregistered experiments, statistical review and synchronized registry updates.
