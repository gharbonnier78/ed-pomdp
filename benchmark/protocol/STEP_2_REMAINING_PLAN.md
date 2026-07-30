# Step 2 Remaining Plan

## Ordering decision

Step 2.4 precedes policy-matrix completion because the central contrast between a classical POMDP without explicit `E` and ED-POMDP is not meaningful while evidence quality has no causal effect on observation reliability, calibration, governed constraints or terminal loss.

Under the current Step 2.3 model, `environment_validation` changes only the marginal belief over `E`; it does not change the marginal belief over `S` or terminal decision risk. Its decision VoI is therefore zero, and the two central policies can collapse to identical behavior.

## Step 2.4 — Evidence-quality and degradation mechanism

Implement and test a non-privileged mechanism in which latent evidence quality affects observable evidence production. Required properties:

- `E` changes functional-channel reliability, calibration or governed release constraints;
- the policy never observes true `E` or the simulator's true regime;
- environment-validation observations can change expected future decision loss;
- identifiable, degraded and likelihood-misspecified regimes are distinguishable in generated data;
- tests demonstrate non-zero decision value for evidence-quality acquisition in at least one preregistered configuration;
- no claim promotion occurs.

## Step 2.5 — Policy matrix completion

Implement the remaining preregistered policies only after Step 2.4 makes the central contrast operational:

- fixed;
- random;
- risk/failure-focused;
- entropy over the full joint belief `P(S,E | history)`;
- risk-only;
- classical POMDP without explicit `E`;
- ED-POMDP decision-aware VoI.

All policies must share observable inputs, available channels, budget accounting, stopping rules and terminal loss semantics.

## Step 2.6 — Reproducible experiment harness and analysis freeze

Before headline execution:

- freeze the complete regime × budget × policy matrix;
- freeze primary and secondary metric implementations;
- freeze the confirmatory multiplicity family and Holm correction;
- commit the analysis scripts and locked dependency/configuration manifest;
- publish the Git commit SHA and SHA-256 hashes in a dated analysis-freeze manifest;
- reject headline execution when the working tree or hashes do not match the manifest.

## Step 2.7 — Preregistered runs and statistical analysis

- run at least 30 independent seeds per frozen configuration;
- preserve raw episode-level results;
- compute paired contrasts, confidence intervals and corrected primary inferences;
- retain failed, null and adverse configurations;
- label all non-frozen analyses exploratory.

## Step 2.8 — Claim review and Step 2 close-out

- review refutation criteria before promotion;
- synchronize Markdown, CSV and JSON claim registries;
- publish reproducibility artifacts and analysis-freeze identifiers;
- close Step 2 only after independent statistical and epistemic review.
