# Step 2 Benchmark — Closed Frozen Increment

This directory contains the completed quantitative validation increment for ED-POMDP.

## Objective

Evaluate whether decision-aware evidence acquisition and explicit evidence-quality modelling improve software-release decisions under strictly matched budgets.

## Final status

Step 2 is closed after:

- causal evidence-quality modelling;
- completion of the seven-policy matrix;
- fixed-horizon exact-cost harness construction;
- cryptographic analysis freeze;
- execution of 3,360 immutable headline episodes;
- analysis of 240 Holm-corrected confirmatory contrasts;
- independent hash, row-count and Holm verification;
- audited post-hoc directionality analysis;
- deterministic Step 2.8 mechanism diagnosis;
- synchronized claim adjudication.

The frozen runtime, config, raw results and confirmatory outputs are immutable. Step 2.8 reads them without modification.

## Frozen design

- 4 regimes
- 4 budgets: 2, 4, 8, 12
- 30 shared headline seeds: 0–29
- 7 policies
- 3,360 raw episode rows
- 5 confirmatory ED-POMDP-versus-baseline contrasts per regime and budget
- 3 confirmatory endpoints
- 1 mandatory safety endpoint outside inferential testing
- 240 hypotheses in the complete Holm family

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

`unsafe_go_rate` is mandatory safety reporting for every cell but receives no p-value and does not enter Holm correction.

## Confirmatory result

Exactly one of 240 contrasts survives Holm correction:

- ED-POMDP versus classical POMDP;
- degraded-evidence regime;
- budget 2;
- expected calibration error;
- ED-minus-classical difference approximately `-0.042708`;
- Holm-adjusted p-value approximately `0.004800`.

The paired bootstrap interval crosses zero and posterior support is sparse. No decision-loss contrast survives Holm correction.

Across the four acquisition baselines directly associated with `CLM-VOI-001`, aggregate decision-loss directions are:

- favourable: 10/64;
- adverse: 16/64;
- equal: 38/64.

## Step 2.8 mechanism diagnosis

`analysis/analyze_step28_mechanisms.py` deterministically reads the immutable Step 2.7 outputs and creates:

- `results/step28/step28_pairwise_diagnostics.csv` — 2,400 episode pairs;
- `results/step28/step28_mechanism_summary.csv` — 125 aggregate mechanism rows;
- `results/step28/step28_decision_transitions.csv` — terminal-action transition table;
- `results/step28/step28_threshold_occupancy.csv` — posterior distance to frozen decision boundaries;
- `results/step28/step28_acquisition_summary.csv` — channel use by position;
- `results/step28/STEP_2_8_CLAIM_ADJUDICATION.md` — generated scientific adjudication;
- `results/step28/step28_analysis_metadata.json` — input/output hashes and row counts.

The diagnostic is `post_hoc_descriptive`. It produces no new p-values or confidence intervals.

### Main mechanism finding

ED-POMDP improves Brier score in 1,119 of 2,400 paired episodes. In 1,054 of those cases — 94.19% — the terminal action remains unchanged.

Against `risk_only`, ED-POMDP selects exactly the same terminal action in all 480 paired episodes despite different acquisition traces in 275 episodes and a non-zero mean posterior difference.

The benchmark therefore identifies a calibration-to-action coupling problem: better beliefs are frequently decision-inert under the frozen terminal thresholds and fixed horizons.

## Mandatory safety evidence

Unsafe GO counts for ED-POMDP are `0, 0, 0, 17` across identifiable, degraded, misspecified and non-identifiable regimes. Classical POMDP counts are `2, 2, 2, 18`.

This pattern is retained as favourable descriptive evidence and is not promoted as an inferential superiority result.

## Claim disposition

- `CLM-VOI-001`: `NOT_SUPPORTED_STEP2`;
- `CLM-EQ-001`: `BROAD_FORM_NOT_SUPPORTED_NARROW_ECE_SIGNAL`.

The canonical status is in `../docs/CLAIMS.md`; CSV and JSON mirrors are checked by the test suite.

## Canonical artifacts

- `protocol/PREREGISTRATION.md`
- `config/headline_matrix.json`
- `config/FROZEN_ARTIFACTS.json`
- `protocol/ANALYSIS_FREEZE.json`
- `results/headline_raw.csv`
- `results/headline_run_metadata.json`
- `results/headline_summary.csv`
- `results/headline_contrasts.csv`
- `results/step27_execution_audit.json`
- `results/STEP_2_7_RESULTS_REVIEW.md`
- `results/step27_posthoc_directionality.csv`
- `protocol/STEP_2_8_ANALYSIS_PLAN.md`
- `results/step28/`

## Reproduction

```bash
python -m pytest -q benchmark/tests
python -m benchmark.analysis.analyze_step28_mechanisms --output-dir /tmp/step28
```

The analysis requires exactly Python `3.12.13` for repository parity and uses only the Python standard library. CI pins `pytest==9.1.1`.

## Boundary for future work

A future claim must not tune against headline seeds 0–29. Redesigned terminal rules, adaptive stopping, correlated evidence, non-unit costs or industrial scenarios require a new protocol, new development seeds and new untouched confirmatory seeds.
