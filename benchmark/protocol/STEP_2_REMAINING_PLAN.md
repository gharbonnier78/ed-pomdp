# Step 2 Execution and Close-Out Record

## Ordering decision

Step 2.4 preceded policy-matrix completion because the central contrast between a classical POMDP without explicit `E` and ED-POMDP was not meaningful while evidence quality had no causal effect on observation reliability, calibration, governed constraints or terminal loss.

Under the former Step 2.3 model, `environment_validation` changed only the marginal belief over `E`; it did not change the marginal belief over `S` or terminal decision risk. Its decision VoI was therefore zero, and the two central policies could collapse to identical behaviour.

## Step 2.4 — Evidence-quality and degradation mechanism

Completed and merged:

- `E` controls functional-channel discrimination without being exposed to the policy;
- the runner and look-ahead share one joint posterior `P(S,E | history)`;
- environment-validation observations can recalibrate system risk after functional evidence;
- identifiable, evidence-degraded, likelihood-misspecified and non-identifiable regimes are executable;
- fixed-seed tests show the degraded and misspecified regimes are observably distinct;
- a regression configuration gives non-zero decision VoI for environment validation;
- no claim promotion occurred.

## Step 2.5 — Policy matrix completion

Completed and merged:

- fixed alternating plan;
- seeded random acquisition;
- failure-focused rule-based assurance;
- entropy acquisition over the full joint belief;
- risk-only marginal system-uncertainty acquisition;
- classical POMDP with evidence quality permanently marginalized;
- ED-POMDP decision-aware VoI;
- canonical seven-policy registry and fairness invariants.

## Step 2.6 — Reproducible experiment harness and analysis freeze

Completed, reviewed and merged:

- four regimes × four budgets × thirty common seeds × seven policies;
- 3,360 expected episode rows;
- fixed-horizon exact-cost execution;
- common-random-number pairing and separate policy RNG streams;
- explicit frozen loss weights;
- three confirmatory endpoints;
- mandatory descriptive unsafe-GO endpoint;
- fixed ten-bin ECE and resolution diagnostics;
- deterministic paired bootstrap, randomization tests and Holm correction;
- exact Python 3.12.13 runtime identity;
- frozen-artifact lock and committed analysis-freeze manifest.

Frozen-artifact lock SHA-256:

`7acac871ae85343b71b3bbd0cbc399b74075dd45aa4a7f8cdb8acb7f3bf23dd8`

Analysis-freeze manifest SHA-256:

`a131b7e4e86dc8a77f7eedfcff47c46f12b915924ead1706d122fd209f7bb5cf`

## Step 2.7 — Preregistered execution and statistical analysis

Completed, independently reviewed and merged in PR #9:

- exactly 3,360 frozen episode rows executed;
- 448 summary rows generated;
- 240 Holm-corrected confirmatory contrasts generated;
- raw results and run metadata hashes preserved;
- null, adverse and safety configurations retained;
- independent reviewer reproduced all hashes and row counts;
- independent Holm step-down reconstruction produced zero discrepancies;
- post-hoc aggregate directionality was independently recomputed with zero discrepancies.

Confirmatory outcome:

- one ECE contrast survived Holm correction;
- no terminal-decision-loss contrast survived;
- broad claims remained unpromoted pending Step 2.8.

## Step 2.8 — Claim review and Step 2 close-out

Implemented on branch `step-2.8-claim-adjudication`:

- explicit post-hoc analysis boundary;
- deterministic episode-level mechanism diagnosis from immutable Step 2.7 inputs;
- 2,400 ED-POMDP-versus-baseline diagnostic rows;
- 125 mechanism summary rows;
- terminal-action transitions, threshold occupancy and acquisition-position summaries;
- generated artifact hashes and deterministic regeneration tests;
- Markdown, CSV and JSON claim-registry synchronization;
- scientific close-out paper;
- repository and benchmark status correction.

### Mechanism result

ED-POMDP improves Brier score in 1,119 episode pairs. In 1,054 of these pairs, the terminal action is unchanged. The calibration-to-action conversion rate is therefore low under the frozen decision boundaries.

ED-POMDP and `risk_only` select the same action in all 480 paired episodes despite different acquisition traces in most episodes and different posterior values.

### Claim disposition

- `CLM-VOI-001`: `NOT_SUPPORTED_STEP2`;
- `CLM-EQ-001`: `BROAD_FORM_NOT_SUPPORTED_NARROW_ECE_SIGNAL`.

The evidence level is `SYNTHETIC`; evidence polarity and disposition are recorded separately to prevent null or adverse evidence from appearing as positive claim promotion.

## Step 2 close-out gate

Step 2 is considered closed only after:

1. all Step 2.8 diagnostics regenerate deterministically from immutable Step 2.7 inputs;
2. all repository tests pass;
3. all LaTeX documents compile and package checks pass;
4. `docs/CLAIMS.md`, `docs/CLAIMS.csv` and `docs/CLAIMS.json` agree;
5. the one-shot Step 2.8 workflow is removed after result commitment;
6. an independent reviewer verifies the mechanism outputs, claim dispositions and frozen-hash invariance;
7. the Step 2.8 PR is merged.

## Boundary for Step 3

Step 3 is not an automatic continuation of the rejected broad VOI claim. Any redesigned experiment requires:

- a new preregistration;
- new development seeds;
- new untouched confirmatory seeds;
- an explicit calibration-to-action hypothesis;
- adaptive stopping or a justified fixed horizon;
- terminal rules that expose the operational role of evidence quality;
- sensitivity analysis over asymmetric safety and business losses;
- data-readiness approval before any industrial calibration claim.
