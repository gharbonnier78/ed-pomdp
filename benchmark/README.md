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
- a shared joint posterior `P(S,E | history)` for explicit-`E` policies;
- a collapsed classical posterior `P(S | history)` that permanently marginalizes `E`;
- identifiable, evidence-degraded, likelihood-misspecified and deliberately non-identifiable regimes;
- a tested observable history in which environment validation has non-zero decision VoI;
- the complete seven-policy preregistered matrix;
- a canonical policy registry with exact names and deterministic ordering;
- a common runner using each policy's observable belief with shared stopping and terminal-loss semantics.

See:

- `runtime/STEP_2_4_SCOPE.md` for the causal model and numeric regression;
- `runtime/STEP_2_5_SCOPE.md` for policy definitions and fairness invariants;
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
- entropy-reduction acquisition over the full joint belief
- fixed alternating acquisition plan
- seeded random acquisition
- risk-only marginal system-uncertainty acquisition
- failure-focused rule-based assurance baseline

The executable registry is `runtime/policy_matrix.py`.

## Primary metrics

- expected decision loss
- unsafe GO rate
- unnecessary NO-GO rate
- Brier score
- expected calibration error
- residual risk
- evidence cost
- hard-constraint violations

No headline empirical claim is made by the current runtime increments. Claim maturity changes only after the Step 2.6 analysis freeze, preregistered experiments, statistical review and synchronized registry updates.
