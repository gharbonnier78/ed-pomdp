# Step 2.8 Claim Adjudication and Mechanism Diagnosis

## Epistemic status

This report combines the frozen Step 2.7 confirmatory outcome with deterministic post-hoc mechanism diagnostics. The diagnostics add no p-values, confidence intervals or retrospective confirmatory hypotheses.

## Frozen confirmatory outcome

- Decision loss across all five baselines: favourable `17/80`, adverse `17/80`, equal `46/80`.
- Brier score: favourable `63/80`, adverse `13/80`, equal `4/80`.
- ECE: favourable `53/80`, adverse `23/80`, equal `4/80`.
- Claim-relevant VOI baselines, decision loss: favourable `10/64`, adverse `16/64`, equal `38/64`.
- Exactly one of 240 frozen contrasts survived Holm correction: ECE, ED-POMDP versus classical POMDP, degraded evidence, budget 2. Its paired bootstrap interval crossed zero and posterior support was sparse.

## Post-hoc mechanism findings

The episode-level diagnostic contains `2400` paired ED-POMDP-versus-baseline rows.

### Calibration-to-action bridge

- Better ED-POMDP Brier score with the same terminal action: `1054/2400` pairs.
- Better ED-POMDP Brier score with a changed terminal action: `65/2400` pairs.
- Across all `106` changed-action pairs, realised loss was better for ED-POMDP in `65`, worse in `41`, and equal in `0`.

This directly tests the proposed mechanism: improved probabilistic accuracy often remains decision-inert because the posterior does not cross a frozen GO / CONDITIONAL GO / NO-GO boundary. When a boundary is crossed, the realised decision is not consistently improved.

### Classical POMDP comparison

- Action agreement: `459/480` (`0.956250000000`).
- Acquisition-trace agreement: `206/480` (`0.429166666667`).
- Mean absolute posterior difference: `0.127341504401`.
- Changed-action outcomes: ED better `10`, worse `11`, equal `0`.

### Risk-only comparison

- Action agreement: `480/480` (`1.000000000000`).
- Acquisition-trace agreement: `205/480` (`0.427083333333`).
- Mean absolute posterior difference: `0.045387919413`.
- Changed-action outcomes: ED better `0`, worse `0`, equal `0`.

### Mandatory descriptive safety evidence

- ED-POMDP unsafe GO: identifiable `0`, degraded evidence `0`, likelihood misspecified `0`, non-identifiable `17`.
- Classical POMDP unsafe GO: identifiable `2`, degraded evidence `2`, likelihood misspecified `2`, non-identifiable `18`.

The safety pattern is favourable to ED-POMDP in the three avoidable regimes, but `unsafe_go_rate` was a mandatory descriptive endpoint and was not tested for superiority.

## Claim adjudication

### `CLM-VOI-001`

**Disposition: NOT SUPPORTED IN THE FROZEN STEP 2 BENCHMARK.** No decision-loss contrast survived Holm correction. At the aggregate-cell level, the four claim-relevant acquisition baselines yielded 10 favourable, 16 adverse and 38 equal directions. The post-hoc mechanism analysis shows that probabilistic changes frequently fail to change the action and that changed actions are not consistently beneficial.

This disposition is benchmark-bounded; it is not a proof that decision-aware value of information can never help under another terminal rule, horizon, loss model or evidence structure.

### `CLM-EQ-001`

**Disposition: BROAD FORM NOT SUPPORTED; ONE NARROW CALIBRATION SIGNAL RETAINED.** Explicit evidence-quality modelling produced one Holm-significant ECE contrast in the degraded-evidence, budget-2 cell. The evidence is too narrow and resolution-sensitive to support general calibration or decision superiority across degradation and misspecification.

## Step 2 scientific conclusion

Step 2 does not validate general ED-POMDP superiority. It establishes a more precise engineering result: a better probabilistic representation of evidence quality is not sufficient unless the terminal decision architecture can convert that improvement into a different and better action.

## Future preregistration boundary

A future experiment must use new development and confirmatory seeds and must not tune on Step 2 headline seeds. Candidate changes include adaptive stopping, explicit GO / CONDITIONAL GO / NO-GO governance, asymmetric safety and business costs, correlated evidence, non-unit acquisition costs, and terminal rules conditioned jointly on system risk and evidence quality.
