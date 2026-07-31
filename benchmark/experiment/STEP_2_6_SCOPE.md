# Step 2.6 — Reproducible Experiment Harness and Analysis Freeze

## Purpose

Step 2.6 turns the reviewed Step 2.5 policy mechanisms into a preregistered, paired and hash-guarded experimental system. It does not execute the headline experiment and does not promote either empirical claim.

## Executable headline matrix

The canonical candidate configuration is `benchmark/config/headline_matrix.json`:

- 4 executable regimes: identifiable, evidence degraded, likelihood misspecified and non-identifiable;
- 4 exact-cost budgets: 2, 4, 8 and 12 acquisitions;
- 30 common episode seeds: 0–29;
- 7 reviewed policies;
- 3,360 raw episode rows;
- 5 confirmatory baselines and 1 descriptive rule-based baseline;
- 3 confirmatory endpoints;
- 1 mandatory non-inferential safety endpoint;
- 240 confirmatory hypotheses.

The former YAML file is retained only as a pointer from the original research-family scaffold to the exact executable JSON matrix.

## Paired scenario construction

A mutable environment object cannot literally be reused across policies because policies select different channels and mutate observation history. Step 2.6 therefore uses fresh environment instances backed by the same deterministic counterfactual scenario tape.

For a common episode seed:

- latent `S` uses a named SHA-256 stream;
- latent `E` uses a separate named SHA-256 stream;
- each acquisition step uses one named observation-noise quantile shared across policy instances;
- the selected channel changes the failure threshold but not the exogenous noise quantile;
- identical seeds therefore reproduce identical latent states and common random numbers without cross-policy state leakage.

This preserves each policy's correct marginal observation distribution and creates a legitimate paired comparison.

## Separate policy randomness

`RandomPolicy` receives a deterministic policy-local seed derived from `(episode seed, policy name)`. It is not the environment seed and cannot advance the environment stream. `build_policy_matrix` creates fresh policy instances for every `(regime, budget, seed)` cell, so mutable RNG state never leaks across experimental units.

## Exact-cost fairness

Headline execution does not call the stopping-capable exploratory runner. It executes exactly `budget` unit-cost acquisitions for every policy.

The harness rejects any row where:

- acquisition count differs from budget;
- evidence cost differs from budget;
- policy order differs from the canonical registry;
- paired policies do not share the same latent scenario.

Early stopping remains available for later exploratory analysis but is excluded from the confirmatory multiplicity family.

## Frozen loss semantics

The following values are explicit in the executable matrix and later repeated in the final manifest:

- `unsafe_go = 10.0`;
- `unnecessary_no_go = 2.0`;
- `conditional_bad = 4.0`;
- `conditional_good = 0.5`;
- `evidence_cost = 0.1`.

The harness constructs `LossWeights` from configuration rather than relying on implicit defaults. Any change invalidates the artifact lock.

## Raw evidence schema

Each episode row preserves:

- `(regime, budget, seed, policy)` key;
- derived policy seed;
- true latent `S` and `E`, recorded only after execution for scoring/audit;
- serialized observable acquisition history;
- policy-specific posterior risk;
- terminal decision;
- realized decision loss and safety flags;
- Brier score, posterior residual risk, evidence cost and acquisition count.

Latent values are never passed to a policy.

The raw runner also writes metadata containing the current Git head plus SHA-256 hashes of the manifest, executable configuration and raw table. Confirmatory analysis permits only the raw table and metadata as uncommitted artifacts, verifies those hashes before reading the table, rejects incomplete or duplicated cells and rechecks that each paired cell has one common latent scenario.

## Confirmatory and safety endpoints

The confirmatory endpoints are:

- decision loss;
- Brier score;
- expected calibration error.

`unsafe_go_rate` remains mandatory safety reporting for every policy, regime and budget, but it receives no paired p-value and is excluded from Holm correction.

This separation follows a pre-freeze estimability review using held-out seeds `100–129`, never the headline seeds `0–29`. The common-random-number coupling made unsafe-GO events highly concordant across policies, leaving almost no discordant pairs. With zero discordant pairs, paired randomization is structurally uninformative; including 80 such tests would only tighten Holm thresholds for endpoints capable of distinguishing policies. The complete rationale is preserved in `benchmark/protocol/PRE_FREEZE_POWER_REVIEW.md`.

Absolute unsafe-GO counts and rates remain publication requirements. A future inferential safety comparison requires a separately powered and preregistered study.

## Frozen analysis

The analysis entry point computes:

- summaries for all policies, regimes, budgets, three confirmatory endpoints and the mandatory safety endpoint;
- fixed ten-bin ECE;
- ECE resolution diagnostics: distinct posterior count, populated bins and total bins;
- seed-paired ED-minus-baseline effects for confirmatory endpoints only;
- 20,000-resample percentile bootstrap intervals;
- 50,000 within-pair label permutations;
- deterministic analysis streams derived from seed `20260731`;
- Holm step-down correction over the complete 240-hypothesis family.

ECE is recomputed after every paired resample or label permutation rather than replaced by a per-row surrogate. Small-budget ECE is explicitly labelled low-resolution when posterior support is sparse; the ten frozen bins are not coarsened after inspection.

All summary rows use one schema:

- `estimate` is the statistic evaluated on the observed 30-seed cell;
- `bootstrap_median` is the median of its deterministic bootstrap distribution;
- `bootstrap_standard_deviation` is the standard deviation of that bootstrap distribution;
- percentile confidence bounds use the same bootstrap distribution.

The previous mixed raw-sample versus bootstrap meaning of `median` and `standard_deviation` is eliminated before freeze.

A reduced integration regression executes all seven policies over 30 seeds for one regime/budget cell, then traverses summaries, paired contrasts and Holm correction. It validates the complete assembly without using the frozen headline matrix or producing headline evidence.

## Frozen runtime

The lock and final manifest identify exactly Python `3.12.13`. The headline runner and analysis use only the Python standard library. CI uses the same Python version and pins test-only dependency `pytest==9.1.1`. A runtime-version mismatch blocks both generation and analysis.

## Freeze mechanism

`scripts/freeze_headline_analysis.py` enforces a two-commit sequence:

1. generate and commit `benchmark/config/FROZEN_ARTIFACTS.json` after all accepted code/configuration is committed;
2. generate and commit `benchmark/protocol/ANALYSIS_FREEZE.json` referencing the commit containing that lock.

The lock hashes every model, policy, runtime, runner, metric implementation, metric contract, analysis, configuration and protocol artifact capable of changing results, including the held-out pre-freeze power review. The final manifest repeats:

- frozen artifact commit;
- lock hash;
- exact Python runtime;
- runner and analysis entry-point hashes;
- complete regimes, budgets, seeds and policies;
- explicit `LossWeights`;
- confirmatory metric and mandatory safety registries;
- fixed ECE calibration bins;
- RNG design;
- multiplicity method, alpha and expected family size.

`run_headline.py` refuses execution unless the manifest is tracked, the Git tree has no unexpected dirty paths, the frozen commit is an ancestor, all hashes match, the exact runtime matches, configuration dimensions match, `LossWeights` match, endpoint registries match, ECE calibration matches, multiplicity semantics match and no previous output exists.

## Current branch state

This PR is intentionally a freeze candidate:

- configuration status is `freeze_candidate_not_executable`;
- no frozen-artifact lock exists;
- no final analysis-freeze manifest exists;
- no headline result exists.

The lock and final manifest must be generated only after reviewer approval of this implementation.

## Claim boundary

`CLM-VOI-001` and `CLM-EQ-001` remain at evidence level `NONE`. Step 2.6 establishes experimental integrity; only Step 2.7 can produce empirical evidence, and only Step 2.8 can review claim promotion.
