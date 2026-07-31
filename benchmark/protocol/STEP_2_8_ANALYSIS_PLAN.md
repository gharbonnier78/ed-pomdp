# Step 2.8 Analysis Plan — Claim Adjudication and Mechanism Diagnosis

## Status

This document governs the Step 2.8 close-out work performed after the frozen Step 2.7 confirmatory analysis and independent review.

Step 2.8 is **not a new confirmatory experiment**. It does not alter the Step 2.6 freeze, rerun headline seeds, change the Holm family, add retrospective hypotheses to the preregistration, or promote claims on the basis of post-hoc significance testing.

## Immutable inputs

The following Step 2.7 artifacts remain immutable:

- `benchmark/config/FROZEN_ARTIFACTS.json`;
- `benchmark/protocol/ANALYSIS_FREEZE.json`;
- `benchmark/config/headline_matrix.json`;
- `benchmark/results/headline_raw.csv`;
- `benchmark/results/headline_summary.csv`;
- `benchmark/results/headline_contrasts.csv`;
- `benchmark/results/headline_run_metadata.json`;
- `benchmark/results/step27_execution_audit.json`.

The Step 2.8 analysis reads these files but never modifies them.

## Purpose

The confirmatory result showed a recurring separation between probabilistic quality and terminal decision quality. Step 2.8 therefore asks a narrower diagnostic question:

> Why do frequent improvements in Brier score and ECE fail to produce broad improvements in realised terminal decision loss?

The analysis is descriptive and mechanistic. It supports claim adjudication and future protocol design, not retrospective confirmatory inference.

## Fixed comparison set

Each ED-POMDP episode is paired by `config_id` with the five frozen confirmatory baselines:

- `fixed_plan`;
- `random_acquisition`;
- `entropy_acquisition`;
- `risk_only`;
- `classical_pomdp`.

The analysis preserves the frozen common-random-number pairing over regime, budget and seed.

## Deterministic decision boundaries

The frozen loss weights imply the Bayes-optimal terminal boundaries:

- GO / CONDITIONAL GO boundary: `1 / 13`;
- CONDITIONAL GO / NO-GO boundary: `3 / 11`.

These values are derived directly from `benchmark/runtime/decision.py`; they are not tuned to the observed results.

Threshold-proximity diagnostics use three declared absolute windows:

- `0.01`;
- `0.025`;
- `0.05`.

## Diagnostic outputs

### 1. Pairwise episode diagnostics

For every ED-POMDP-versus-baseline pair, record:

- posterior difference and absolute posterior difference;
- Brier-score difference;
- terminal-decision agreement;
- realised decision-loss difference;
- unsafe-GO and unnecessary-NO-GO differences;
- acquisition-trace agreement;
- distance of each posterior to the nearest terminal boundary;
- whether ED-POMDP improves calibration while leaving the action unchanged;
- whether a changed action improves, worsens or preserves realised loss.

Expected row count: `2,400`.

### 2. Mechanism summaries

Aggregate the pairwise diagnostics by baseline, regime and budget, including:

- favourable / adverse / equal decision-loss counts;
- favourable / adverse / equal Brier counts;
- action-agreement and acquisition-trace-agreement rates;
- mean absolute posterior difference;
- frequency of calibration improvement without action change;
- realised outcome when actions differ;
- unsafe-GO totals.

### 3. Decision-transition table

For every baseline-to-ED terminal-action transition, report count, mean loss difference and favourable / adverse / equal outcomes.

### 4. Threshold-occupancy table

For every policy, regime and budget, report the proportion of posterior values within each declared window of either frozen decision boundary.

### 5. Acquisition summary

Report channel use by policy, regime, budget and acquisition position, preserving the exact serialized traces from the frozen raw file.

### 6. Claim-adjudication report

Produce an English Markdown report that clearly separates:

- frozen confirmatory findings;
- mandatory descriptive safety evidence;
- Step 2.8 post-hoc mechanism findings;
- claim disposition;
- implications for a future preregistration.

## Statistical boundary

Step 2.8 performs no new hypothesis tests, no new confidence intervals and no multiplicity correction. Counts, rates and means are descriptive only.

No Step 2.8 diagnostic may be used to claim that ED-POMDP is statistically superior or inferior beyond the frozen Step 2.7 family.

## Claim adjudication rules

### `CLM-VOI-001`

The broad claim is adjudicated as **not supported in the frozen Step 2 benchmark** because no decision-loss contrast survived Holm correction and the claim-relevant descriptive direction was not favourable overall.

This is not labelled a formal proof of universal inferiority.

### `CLM-EQ-001`

The broad claim is adjudicated as **not supported in its broad form**. One narrow degraded-evidence, budget-2 ECE contrast survived Holm correction, but the bootstrap interval crossed zero, posterior support was sparse and the result did not generalise across decision loss or likelihood misspecification.

### Safety evidence

Unsafe-GO evidence remains mandatory and descriptive. The favourable ED-POMDP pattern is retained without inferential promotion.

## Registry synchronization

Step 2.8 creates synchronized representations:

- `docs/CLAIMS.md` — canonical human-readable registry;
- `docs/CLAIMS.csv` — machine-readable tabular mirror;
- `docs/CLAIMS.json` — machine-readable structured mirror.

The Markdown registry remains authoritative. CSV and JSON files must carry the same stable IDs, statements, evidence levels, dispositions, artifacts and revision date.

## Close-out gate

Step 2 closes only when:

1. all Step 2.8 outputs are reproducible from immutable Step 2.7 inputs;
2. claim registries agree exactly;
3. the paper and repository status no longer describe Step 2.6 as a freeze candidate;
4. null, adverse, equal, calibration and safety findings are retained;
5. CI and package checks pass;
6. an independent reviewer confirms the claim disposition and mechanism report.
