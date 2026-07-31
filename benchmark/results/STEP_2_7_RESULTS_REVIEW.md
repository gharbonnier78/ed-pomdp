# Step 2.7 Frozen Headline Results — Scientific Review Note

## Status and provenance

This note interprets the immutable Step 2.7 outputs produced by the frozen Step 2.6 protocol. It does not modify the preregistration, analysis implementation, endpoint family, or claim registry.

- execution workflow run: `30619187371`;
- execution Git head: `58eeeacd4a887ed86b040364e050d177ca28cd1d`;
- frozen-artifact commit: `8e86d655bd4d9873c87b60c1a541c7712df389ce`;
- analysis-freeze manifest SHA-256: `a131b7e4e86dc8a77f7eedfcff47c46f12b915924ead1706d122fd209f7bb5cf`;
- raw rows: `3,360`;
- summary rows: `448`;
- confirmatory contrasts: `240`;
- frozen tests: `50/50` passed.

Immutable result hashes:

- `headline_raw.csv`: `6695ab664fb67ec1eeb60669273aadf6a355a4fcdb45994f3870f638775dd070`;
- `headline_summary.csv`: `8a2e6f4191862015b39b97c99d9358bb603859f7aaaead86c418b20bd7c34f5b`;
- `headline_contrasts.csv`: `89bc40f8bc2b7f4be00bfadfc3cb3397b23c34ccd9b96b8e004c1151fad82478`.

## Independent verification

The reviewer independently verified that `FROZEN_ARTIFACTS.json`, `ANALYSIS_FREEZE.json`, `headline_raw.csv`, and `headline_matrix.json` retained their exact frozen hashes. The reviewer also:

- confirmed the exact counts of 3,360 raw rows, 448 summary rows, and 240 contrasts;
- reimplemented Holm step-down from the raw `p_value` column with zero discrepancies across all 240 adjusted values;
- independently recomputed every row of `step27_posthoc_directionality.csv`, including all budget and regime subgroups, with zero discrepancies;
- independently confirmed the unsafe-GO counts by regime for ED-POMDP and the classical POMDP.

The post-hoc material is additive and explicitly labelled exploratory; it does not alter any frozen scientific artifact.

## Confirmatory family result

Exactly **one of the 240 preregistered contrasts rejects after Holm correction**.

| Regime | Budget | Contrast | Endpoint | ED value | Baseline value | ED − baseline | Raw p | Holm-adjusted p |
|---|---:|---|---|---:|---:|---:|---:|---:|
| `evidence_degraded` | 2 | ED-POMDP vs classical POMDP | ECE | 0.183672 | 0.226380 | -0.042708 | 0.0000199996 | 0.00479990 |

The raw p-value is the minimum attainable Monte Carlo value with `50,000` frozen permutations: `1 / 50,001`.

This result requires cautious interpretation for two preregistered reasons:

1. the paired bootstrap interval for the ECE difference is `[-0.046647, 0.003407]`, which crosses zero even though the paired randomization test rejects;
2. this is a low-resolution calibration cell: ED-POMDP has only `3` distinct posterior values occupying `3/10` bins, while the classical POMDP has `4` distinct values occupying `3/10` bins.

The result is therefore a genuine confirmatory rejection under the frozen test, but it is **narrow, discrete-support-sensitive evidence**, not broad proof of superiority.

## Directionality audit relevant to Step 2.8

Across all five confirmatory baselines, four regimes, and four budgets:

- decision loss: ED better in `17/80` cells, worse in `17/80`, equal in `46/80`;
- Brier score: ED better in `63/80` cells, worse in `13/80`, equal in `4/80`;
- ECE: ED better in `53/80` cells, worse in `23/80`, equal in `4/80`.

For the four acquisition baselines named directly by `CLM-VOI-001`:

- decision loss: ED better in `10/64` cells, worse in `16/64`, equal in `38/64`;
- mean ED-minus-baseline decision-loss difference: `+0.020833` — positive is worse for ED;
- among non-tied cells, adverse directions outnumber favourable directions `16` to `10`;
- no favourable decision-loss cells occur under `evidence_degraded` (`0/16`) or at budget `8` (`0/16`).

This is not a confirmatory sign test and must not be reported as one. It is a post-hoc descriptive diagnosis. Nevertheless, it shows that the broad VOI claim is not merely unsupported through lack of power: on its claim-relevant acquisition baselines, the observed decision-loss direction is more often adverse than favourable when the policies differ.

The risk-only policy has exactly the same decision loss as ED-POMDP in all `16` regime-budget cells, despite posterior and calibration differences. This is an important mechanistic result: under the current observation model, horizon, and terminal loss rule, the extra decision-aware acquisition objective often does not alter the terminal action enough to change realised decision loss.

## CLM-VOI-001 review

The claim under test was that decision-aware value of information reduces matched-budget decision loss relative to fixed, random, entropy, and risk-only acquisition policies.

**Conclusion:** the current confirmatory experiment does not support the broad form of `CLM-VOI-001`. The claim must remain unpromoted. Step 2.8 should either reject it for this benchmark or narrow it to a more specific mechanism or regime before any new experiment.

## CLM-EQ-001 review

The claim under test was that explicit modelling of evidence quality improves calibration and decision loss under evidence degradation and likelihood misspecification relative to the classical model without explicit `E`.

For ED-POMDP versus classical POMDP in the two target regimes across four budgets:

- decision loss: ED better in `4/8` cells and equal in `4/8`; no Holm rejection;
- Brier score: ED better in `7/8` cells and worse in `1/8`; no Holm rejection;
- ECE: ED better in `5/8` cells and worse in `3/8`; one Holm rejection, at `evidence_degraded`, budget `2`.

Under evidence degradation, the descriptive pattern strengthens at larger budgets: ED decision loss equals classical at budgets `2` and `4`, then is lower by `0.366667` at budget `8` and `0.266667` at budget `12`. These differences do not reject under the frozen family.

Under likelihood misspecification, calibration is mixed: ED ECE is worse at budgets `2`, `4`, and `8`, and better at budget `12`. This prevents a general calibration-superiority interpretation across the misspecification regime.

**Conclusion:** the experiment provides narrow confirmatory evidence that explicit evidence-quality modelling can improve calibration in one degraded-evidence, low-budget cell. It does not support the full broad form of `CLM-EQ-001` across degradation and misspecification or across both calibration and decision loss. The broad claim must remain unpromoted pending Step 2.8 claim decomposition.

## Mandatory descriptive safety endpoint

`unsafe_go_rate` was preregistered as mandatory descriptive safety evidence and was not tested inferentially. Unsafe GO carries weight `10.0` in the frozen loss function, compared with `2.0` for an unnecessary NO-GO.

Across `480` episodes per policy:

| Policy | Unsafe GO count | Rate |
|---|---:|---:|
| fixed plan | 15 | 3.125% |
| ED-POMDP | 17 | 3.542% |
| entropy acquisition | 17 | 3.542% |
| risk-only | 17 | 3.542% |
| rule-based | 17 | 3.542% |
| random acquisition | 17 | 3.542% |
| classical POMDP | 24 | 5.000% |

The regime-level comparison between ED-POMDP and the classical POMDP is:

| Regime | ED-POMDP unsafe GO | Classical POMDP unsafe GO |
|---|---:|---:|
| `identifiable` | 0 | 2 |
| `evidence_degraded` | 0 | 2 |
| `likelihood_misspecified` | 0 | 2 |
| `non_identifiable` | 17 | 18 |

ED-POMDP therefore produces zero unsafe GO decisions in the three regimes where such errors are mathematically avoidable, while the classical POMDP produces two in each. This is a favourable safety signal and is especially relevant to Test Authority readers. It remains descriptive evidence: the frozen protocol did not define an inferential superiority test for `unsafe_go_rate`.

## Calibration-resolution audit

The frozen ten-bin ECE diagnostics confirm the preregistered low-resolution concern:

| Budget | Distinct posterior values, range | Median distinct values | Populated bins, range | Median populated bins |
|---:|---:|---:|---:|---:|
| 2 | 3–9 | 4 | 3–6 | 4 |
| 4 | 7–21 | 9 | 4–10 | 7 |
| 8 | 11–27 | 17 | 5–9 | 7 |
| 12 | 14–30 | 21.5 | 4–7 | 5 |

Higher acquisition budgets increase the number of distinct posterior values, but do not monotonically increase occupied fixed bins. This is consistent with posterior concentration rather than a simple resolution failure.

## Claim-governance recommendation for Step 2.8

1. Keep `CLM-VOI-001` and `CLM-EQ-001` at their current unpromoted status.
2. Do not summarise Step 2.7 as “ED-POMDP wins.” The confirmatory family supports one narrow ECE contrast and rejects no decision-loss contrast.
3. State explicitly that the claim-relevant decision-loss direction is more often adverse than favourable among non-tied cells.
4. Preserve the favourable regime-level unsafe-GO signal as mandatory descriptive safety evidence.
5. Treat the decision equivalence between ED-POMDP and risk-only as a primary mechanistic finding requiring explanation.
6. Consider decomposing `CLM-EQ-001` into a narrow degraded-evidence calibration claim and separate unsupported misspecification and decision-loss claims.
7. Preserve all null, adverse, equal, calibration, and safety results in the publication package.
