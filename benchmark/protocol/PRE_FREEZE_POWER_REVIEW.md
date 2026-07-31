# Step 2.6 Pre-Freeze Power and Estimability Review

## Status

This document records a design review performed before the analysis freeze. It is not a Step 2.7 result and must not be used to support `CLM-VOI-001` or `CLM-EQ-001`.

The diagnostic used held-out seeds `100–129`. It did not inspect or execute the frozen headline seeds `0–29`.

## Unsafe-GO estimability under common random numbers

The common-random-number design deliberately aligns latent system state, latent evidence-quality state and step-indexed exogenous noise across policies. This improves paired precision for continuous and calibration endpoints, but it can make rare binary safety events concordant across policies.

Observed discordant-pair counts for ED-POMDP versus the five confirmatory baselines were almost always zero in the held-out diagnostic. Representative cells included:

```text
identifiable      budget=4   fixed=0 entropy=0 classical=0 risk_only=0 random=0
identifiable      budget=12  fixed=0 entropy=0 classical=0 risk_only=0 random=0
evidence_degraded budget=4   fixed=0 entropy=0 classical=0 risk_only=0 random=0
evidence_degraded budget=12  fixed=0 entropy=0 classical=1 risk_only=0 random=0
```

Unsafe-GO events themselves were present, but policies usually produced them on the same paired seeds. With no discordant pair, every within-pair label exchange reproduces the observed difference and the paired randomization p-value is exactly `1.0`.

For a binary paired endpoint with `d` discordant pairs all in the same direction, the smallest exact two-sided sign-flip probability is approximately `2^(1-d)`. Under Holm correction across the original 320-hypothesis family, reaching the first-step threshold would require at least 14 discordant pairs all aligned in one direction among 30 seeds. The held-out diagnostic showed that this condition is not credible for the current coupled design.

## Design decision before freeze

`unsafe_go_rate` remains mandatory safety evidence and is reported for every policy, regime and budget. It is removed from the confirmatory permutation/Holm family because the present design cannot estimate a meaningful paired superiority contrast for it.

The resulting confirmatory family contains:

- 4 regimes;
- 4 budgets;
- 5 baselines;
- 3 confirmatory endpoints: decision loss, Brier score and ECE;
- `4 × 4 × 5 × 3 = 240` hypotheses.

A future inferential unsafe-GO study would require a separately powered protocol, potentially more seeds, enriched unsafe scenarios or a safety-specific sampling design. Such work is outside the current frozen headline matrix.

## ECE resolution review

The held-out diagnostic also showed sparse posterior support at small budgets. Representative counts across 30 seeds were:

```text
budget=2  -> 3 distinct posterior values, 3/10 populated bins
budget=4  -> 7 distinct posterior values, 5/10 populated bins
budget=8  -> 18 distinct posterior values, 7/10 populated bins
budget=12 -> 25 distinct posterior values, 5/10 populated bins
```

The fixed ten-bin ECE is retained because coarsening bins would change the estimand and could hide discreteness. Every ECE summary must instead report distinct posterior count, populated-bin count and total-bin count. Low-budget ECE must be interpreted as low-resolution.

## Summary-table semantics

Before freeze, the summary schema was also revised so that all endpoints use the same columns:

- `estimate`: statistic on the observed 30-seed cell;
- `bootstrap_median`: median of the deterministic bootstrap distribution;
- `bootstrap_standard_deviation`: standard deviation of that bootstrap distribution;
- percentile confidence bounds.

The previous mixed use of raw-sample dispersion for decomposable metrics and bootstrap dispersion for ECE is prohibited.
