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

## CLM-VOI-001 review

The claim under test was that decision-aware value of information reduces matched-budget decision loss relative to fixed, random, entropy, and risk-only acquisition policies.

Across the four named acquisition baselines, four regimes, and four budgets:

- decision loss: ED better in `10/64` cells, worse in `16/64`, equal in `38/64`;
- mean ED-minus-baseline decision-loss difference: `+0.020833` — positive is worse for ED;
- no decision-loss contrast rejects after Holm correction;
- only one decision-loss contrast has unadjusted `p < 0.05`, and it does not survive multiplicity correction.

Descriptively, ED has lower Brier score in `49/64` cells and lower ECE in `43/64` cells, but none of these comparisons survives Holm correction.

The risk-only policy has exactly the same decision loss as ED-POMDP in all `16` regime-budget cells, despite posterior and calibration differences. This is an important mechanistic result: under the current observation model, horizon, and terminal loss rule, the extra decision-aware acquisition objective often does not alter the terminal action enough to change realized decision loss.

**Conclusion:** the current confirmatory experiment does not support the broad form of `CLM-VOI-001`. The claim must remain unpromoted. Step 2.8 should either refute it for this benchmark or narrow it to a more specific mechanism or regime before any new experiment.

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

`unsafe_go_rate` was preregistered as mandatory descriptive safety evidence and was not tested inferentially.

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

For ED-POMDP, all `17` unsafe-GO events occur in the `non_identifiable` regime; the count is zero in `identifiable`, `evidence_degraded`, and `likelihood_misspecified`. The classical POMDP additionally produces two unsafe-GO events in each of those three regimes.

These figures are safety observations, not superiority tests. The fixed plan has the lowest absolute count in this matrix, while the classical POMDP has the highest.

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

1. Keep `CLM-VOI-001` and `CLM-EQ-001` at their current unpromoted status while the reviewer independently reproduces the result tables and hashes.
2. Do not summarize Step 2.7 as “ED-POMDP wins.” The confirmatory family supports one narrow ECE contrast and rejects no decision-loss contrast.
3. Treat the decision equivalence between ED-POMDP and risk-only as a primary mechanistic finding requiring explanation.
4. Consider decomposing `CLM-EQ-001` into a narrow degraded-evidence calibration claim and separate unsupported misspecification and decision-loss claims.
5. Preserve all null, adverse, and safety results in the publication package.
