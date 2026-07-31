# Step 2 Benchmark

This directory contains the quantitative validation increment for ED-POMDP.

## Objective

Evaluate whether decision-aware evidence acquisition and explicit evidence-quality modelling improve software-release decisions under strictly matched budgets.

## Scope

The benchmark controls:

- latent system state `S`;
- latent evidence-quality state `E`;
- observation channels and evidence degradation;
- likelihood misspecification and non-identifiability;
- acquisition cost and exact budget;
- terminal loss and posterior calibration;
- random-stream pairing and analysis multiplicity;
- exact analysis-runtime identity.

## Current executable state

The repository now includes:

- a causal evidence-production model in which latent `E` controls functional-channel reliability;
- a shared joint posterior `P(S,E | history)` for explicit-`E` policies;
- a collapsed classical posterior `P(S | history)` that permanently marginalizes `E`;
- identifiable, evidence-degraded, likelihood-misspecified and deliberately non-identifiable regimes;
- the complete seven-policy preregistered matrix;
- a fixed-horizon exact-cost experiment harness;
- common-random-number pairing across all policies for each `(regime, budget, seed)` cell;
- a separate deterministic policy RNG stream and fresh policy instance per experimental unit;
- explicit configured `LossWeights`;
- raw episode-level evidence and metric schema;
- three confirmatory endpoints plus mandatory non-inferential unsafe-GO reporting;
- fixed-bin ECE with posterior-support and bin-occupancy diagnostics;
- paired bootstrap, paired permutation and Holm implementations;
- exact Python `3.12.13` runtime identity and pinned `pytest==9.1.1` test environment;
- a hash/Git guard that prevents unfrozen headline execution;
- a two-phase lock and dated-manifest generator.

The Step 2.6 branch is still a **freeze candidate**. It deliberately contains no final lock, no final analysis-freeze manifest and no headline result. Those artifacts are generated only after review.

See:

- `runtime/STEP_2_4_SCOPE.md` for the causal model and numeric regression;
- `runtime/STEP_2_5_SCOPE.md` for policy definitions and fairness invariants;
- `experiment/STEP_2_6_SCOPE.md` for pairing, exact-cost execution, statistics and freeze mechanics;
- `config/headline_matrix.json` for the executable freeze candidate;
- `protocol/PRE_FREEZE_POWER_REVIEW.md` for the held-out seeds `100–129` estimability review;
- `protocol/STEP_2_REMAINING_PLAN.md` for the remaining Step 2 sequence;
- `protocol/PREREGISTRATION.md` for the confirmatory protocol.

## Headline matrix candidate

- 4 regimes
- 4 budgets: 2, 4, 8, 12
- 30 shared headline seeds: 0–29
- 7 policies
- 3,360 raw episode rows
- 5 confirmatory ED-POMDP-versus-baseline contrasts
- 3 confirmatory endpoints
- 1 mandatory safety endpoint outside inferential testing
- 240 hypotheses in the complete Holm family

The former `config/benchmark_matrix.yaml` is retained as a historical scaffold pointer. The canonical executable matrix is `config/headline_matrix.json`.

## Policies

- ED-POMDP decision-aware VoI
- classical POMDP without explicit evidence-quality state
- entropy-reduction acquisition over the full joint belief
- fixed alternating acquisition plan
- seeded random acquisition
- risk-only marginal system-uncertainty acquisition
- failure-focused rule-based assurance baseline

The executable registry is `runtime/policy_matrix.py`.

## Confirmatory metrics

- decision loss
- Brier score
- fixed ten-bin expected calibration error

`unsafe_go_rate` is mandatory safety reporting for every cell but receives no p-value and does not enter Holm correction. Secondary and audit metrics include unnecessary NO-GO, posterior residual risk, evidence cost and acquisition count.

Every ECE row reports the number of distinct posterior values, populated bins and total frozen bins. Sparse support at small budgets is interpreted as low-resolution rather than hidden by post-hoc bin merging.

## Frozen runtime

Headline generation and analysis require exactly Python `3.12.13`. They use only the Python standard library. CI tests use the same Python version and pin `pytest==9.1.1`; pytest is not a headline runtime dependency.

## Execution boundary

Headline generation is refused until `protocol/ANALYSIS_FREEZE.json` exists as a committed file and every frozen artifact hash, runtime version, dimension, endpoint registry, multiplicity setting and `LossWeights` value matches. Early-stopping runs are exploratory and cannot enter the confirmatory family.

No headline empirical claim is made by the current increment. Claim maturity changes only after Step 2.7 execution, independent statistical review and synchronized registry updates in Step 2.8.
