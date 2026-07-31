# Step 2.5 — Policy Matrix Completion

## Purpose

Complete the seven preregistered acquisition policies after Step 2.4 made latent evidence quality causally relevant to functional evidence.

This increment completes executable policy definitions. It does **not** freeze or execute the headline experiment matrix and does not promote any empirical claim.

## Canonical policy registry

`benchmark/runtime/policy_matrix.py` constructs fresh policy instances in the following frozen order:

1. `ed_pomdp_voi`
2. `classical_pomdp`
3. `entropy_acquisition`
4. `fixed_plan`
5. `random_acquisition`
6. `risk_only`
7. `rule_based`

The registry asserts exact name and ordering equality so later experiment code cannot silently drift from the preregistration.

## Shared public contract

Every policy receives only:

- observable `Observation` history;
- the common ordered set of available channel names.

Every policy exposes:

- `choose(history, channels)` for acquisition;
- `posterior_bad(history)` for its observable belief about system risk.

No policy receives true system state `S`, true evidence-quality state `E`, simulator regime, true likelihood model or future observations.

The decision runner applies the same:

- budget ceiling;
- minimum-acquisition rule;
- Bayes-optimal terminal action derived from `LossWeights`;
- realized terminal-loss and evidence-cost scoring.

The only intentional inference difference is the preregistered classical-POMDP contrast described below.

## Policy semantics

### ED-POMDP decision-aware VoI

Maintains the full joint posterior `P(S,E | history)` and selects the channel minimizing expected one-step terminal decision risk plus acquisition cost.

### Classical POMDP without explicit `E`

Maintains only `P(S | history)`. Evidence quality is permanently marginalized at prior probability `0.5` for every observation.

Consequences:

- environment-validation evidence is non-discriminative for `S` in the collapsed model;
- the model cannot learn that functional evidence has become more or less reliable;
- its acquisition still minimizes the same one-step expected terminal loss and uses the same `LossWeights`.

This creates the intended explicit-`E` versus collapsed-`E` contrast without granting either policy privileged simulator information.

### Entropy acquisition

Minimizes expected Shannon entropy of the complete joint belief `P(S,E | history)` after the next observation. It is uncertainty-seeking and does not use terminal loss asymmetry.

### Risk-only acquisition

Minimizes expected Bernoulli variance `p(S=bad)(1-p(S=bad))` after the next observation. It targets marginal uncertainty about `S` only and does not use terminal loss weights.

### Fixed plan

Cycles through the preregistered sequence:

`functional → environment_validation → ...`

It ignores observation values for acquisition.

### Random acquisition

Uses a seeded uniform draw over the common available channels. A fresh seeded policy instance is built for each experimental unit.

### Rule-based assurance

`FailureFocusedPolicy` implements the preregistered `rule_based` baseline:

- repeat the most recently failing channel;
- otherwise follow the fixed alternating plan.

It uses observable results only and performs no acquisition look-ahead.

## Regression coverage

Step 2.5 tests verify:

- exact seven-policy completeness and ordering;
- channel-access and latent-information boundaries;
- full-joint entropy semantics;
- risk-only marginal uncertainty semantics;
- inability of the classical model to learn from environment validation;
- divergence between classical and explicit-`E` posteriors after reliability evidence;
- use of each policy's own observable posterior by the common decision runner.

## Scientific boundary

This increment provides executable mechanisms and unit-level regression evidence only.

It does not provide:

- matched-budget headline results;
- superiority estimates;
- calibration estimates;
- confidence intervals;
- robustness conclusions;
- claim promotion.

`CLM-VOI-001` and `CLM-EQ-001` remain at evidence level `NONE` until Steps 2.6–2.8 are completed.
