# Step 2 Preregistration

## Claims under test

### CLM-VOI-001
Decision-aware value of information reduces matched-budget decision loss relative to fixed, random, entropy and risk-only acquisition policies.

### CLM-EQ-001
Explicit modelling of evidence-production quality improves calibration and decision loss under evidence degradation and likelihood misspecification.

## Experimental unit

One simulated release-decision episode with sampled latent system state, evidence-quality state, observation history, acquisition sequence and terminal decision.

The confirmatory pairing unit is `(regime, budget, seed)`. All seven policies are evaluated on fresh mutable environment instances addressed by the same episode seed. Those instances reproduce the same latent `S`, latent `E` and common observation-noise quantile at each acquisition step. This common-random-number design permits paired contrasts without sharing mutable state between policies.

`RandomPolicy` uses a separate policy-local RNG seed derived deterministically from `(episode seed, policy name)`. The policy RNG never advances or alters the environment noise stream. A fresh policy instance is created for every experimental unit.

## Matched-budget rule

The confirmatory headline benchmark uses a fixed-horizon, exact-cost design:

- unit acquisition cost is `1.0`;
- budgets are integer acquisition horizons;
- every policy executes exactly `budget` acquisitions;
- early stopping is prohibited in headline runs;
- all policies receive identical channel access;
- no policy receives ground-truth state, evidence quality or simulator regime.

Early-stopping experiments are exploratory and outside the confirmatory family. Comparisons are invalid if policies differ in total acquisition cost, permitted channels, stopping horizon or access to ground-truth variables.

## Frozen terminal-loss weights

The Bayes-optimal terminal rule and decision-loss endpoint use the following explicit `LossWeights` values:

- unsafe GO: `10.0`;
- unnecessary NO-GO: `2.0`;
- conditional GO when system is bad: `4.0`;
- conditional GO when system is good: `0.5`;
- evidence cost multiplier: `0.1`.

These values are a frozen experimental axis. They appear in the executable headline configuration, the frozen-artifact lock and the dated analysis-freeze manifest. Changing any value invalidates the freeze exactly like changing a regime, budget, seed, policy or analysis script.

## Confirmatory primary endpoints

1. Mean decision loss
2. Brier score
3. Expected calibration error

Expected calibration error uses fixed equal-width bins with boundaries `[0.0, 0.1, ..., 1.0]`. Bin boundaries cannot be changed after the freeze.

ECE is a nonlinear cell-level statistic based on only 30 common seeds. At small budgets, the policy posterior can have sparse discrete support, so the ten-bin ECE may be low-resolution even when its computation is correct. Every ECE summary must therefore report:

- number of distinct posterior values;
- number of populated bins;
- total number of frozen bins.

Empty bins are not evidence of calibration and must not be interpreted as such. The fixed bins are retained rather than coarsened because post-hoc merging would hide posterior discreteness and change the estimand.

## Mandatory safety endpoint outside confirmatory inference

`unsafe_go_rate` remains a mandatory primary safety report for every `(regime, budget, policy)` cell. It is not assigned a paired permutation p-value and does not enter Holm correction.

A pre-freeze design diagnostic used only held-out seeds `100–129`, never the frozen headline seeds `0–29`. Under the intended common-random-number coupling, unsafe-GO outcomes showed near-zero cross-policy discordance because policies frequently produced the event on the same latent/noise scenarios. A binary paired randomization test with no discordant pairs is structurally uninformative (`p = 1`), while retaining 80 such hypotheses would reduce power for estimable endpoints. The safety event is therefore preserved and published descriptively without pretending that the present 30-seed paired design can support a useful confirmatory superiority test for it.

This decision does not weaken safety governance: absolute unsafe-GO counts and rates must be published for every policy, including null and adverse cells. Any future inferential safety study requires a separately powered design and preregistration.

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

The rule-based policy is executed in the seven-policy matrix but remains descriptive rather than part of the confirmatory multiplicity family.

## Entropy baseline definition

The preregistered entropy baseline maximizes expected reduction in Shannon entropy of the full joint belief `P(S,E | history)`, not the marginal belief over `S` alone.

This deliberately represents uncertainty-seeking rather than decision-aware acquisition. It may spend evidence budget reducing uncertainty about `E` even when that information has little or no terminal decision value. That behavior is part of the intended contrast with ED-POMDP and must not be changed after headline runs begin.

## Statistical protocol

- exactly 30 common seeds per frozen `(regime, budget)` configuration;
- report the observed cell estimate plus deterministic bootstrap median, bootstrap standard deviation and 95% percentile interval;
- compute ED-POMDP-minus-baseline effects using seed-paired bootstrap resampling;
- compute two-sided paired randomization p-values by within-seed policy-label exchange for confirmatory endpoints only;
- use `20,000` bootstrap resamples and `50,000` permutation resamples;
- derive all analysis RNG streams from the frozen analysis seed `20260731` and the summary or contrast identifier;
- retain all failed, null and adverse configurations;
- publish configuration files and raw episode-level result tables.

The summary columns have one meaning for every endpoint: `estimate` is the statistic evaluated on the observed 30-seed cell; `bootstrap_median` and `bootstrap_standard_deviation` describe the deterministic bootstrap distribution. No column mixes raw-sample and bootstrap semantics.

For ECE, paired resampling and permutation operate on complete seed pairs and recompute the nonlinear ECE statistic after each resample or label exchange.

### Confirmatory multiplicity family

The confirmatory family contains every preregistered ED-POMDP-versus-baseline contrast for the three confirmatory primary endpoints, across every preregistered regime and budget included in the frozen headline matrix.

The frozen executable matrix contains four regimes, four budgets, five confirmatory baselines and three confirmatory endpoints, producing `4 × 4 × 5 × 3 = 240` confirmatory hypotheses.

Family-wise error is controlled at `alpha = 0.05` using the Holm step-down correction over that complete family. The mandatory unsafe-GO safety endpoint, secondary endpoints, the rule-based comparison and any analysis outside the frozen family are descriptive or exploratory and must be labelled accordingly.

Neither the family definition, included configurations, metric implementation nor correction method may be changed after the analysis freeze without recording a protocol deviation and treating affected results as exploratory.

## Analysis freeze and script hash

Before any headline experiment is executed:

1. final runner, analysis scripts, metric implementation, endpoint registries, ECE calibration bins, multiplicity settings, `LossWeights` and experiment matrix must be committed;
2. a frozen-artifact lock must list SHA-256 digests for every runtime, model, policy, metric, configuration and protocol artifact capable of changing a result, including the held-out pre-freeze power review;
3. the repository must publish the frozen-artifact Git commit SHA, the lock SHA-256, the runner entry-point SHA-256 and the analysis entry-point SHA-256;
4. those identifiers, the complete headline dimensions, explicit `LossWeights`, confirmatory and safety endpoint registries, ECE calibration settings and multiplicity rule must be recorded in a dated `benchmark/protocol/ANALYSIS_FREEZE.json` manifest;
5. the final manifest must be committed while no headline raw result exists;
6. headline execution must refuse a missing or untracked manifest, dirty working tree, non-descendant commit, hash mismatch, runtime mismatch, dimension mismatch, `LossWeights` mismatch, endpoint-registry mismatch, ECE-calibration mismatch or multiplicity mismatch.

Any later script, model, policy, metric, endpoint registry, calibration setting, multiplicity rule, configuration or loss-weight change requires a new lock and manifest, an explicit protocol-deviation record and reclassification of affected analyses as exploratory unless the full headline experiment is rerun from the new frozen version.

## Refutation criteria

`CLM-VOI-001` is not supported if ED-POMDP shows no material reduction in matched-budget decision loss over the strongest baseline, or if gains disappear under confidence intervals and robustness checks.

`CLM-EQ-001` is not supported if explicit evidence-quality modelling fails to improve calibration or decision loss under preregistered degradation regimes, or if improvement depends only on privileged access to the true latent `E`.

## Claim-governance rule

This protocol does not promote either claim beyond `NONE`. Promotion requires completed runs, reproducible artifacts, statistical review and synchronized updates to `docs/CLAIMS.md`, CSV and JSON registries.
