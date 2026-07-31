# ED-POMDP Research Edition v1.3 — Step 2 Benchmark Close-Out

This repository develops **Evidence-Driven Partially Observable Markov Decision Processes applied to software release assurance**.

<p align="center">
  <a href="./paper/main.pdf"><img src="https://img.shields.io/badge/Open-Main%20Paper-0B5FFF?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Open Main Paper PDF"></a>
  <a href="./paper/step2_closeout.pdf"><img src="https://img.shields.io/badge/Open-Step%202%20Close--Out-8E24AA?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Open Step 2 Close-Out PDF"></a>
  <a href="./identifiability/identifiability_note.pdf"><img src="https://img.shields.io/badge/Open-Identifiability%20Note-6A1B9A?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Open Identifiability Note PDF"></a>
</p>

<p align="center">
  <a href="./research_program/research_program.pdf"><img src="https://img.shields.io/badge/Open-Research%20Programme-00695C?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Open Research Programme PDF"></a>
  <a href="./survey/related_work.pdf"><img src="https://img.shields.io/badge/Open-Related%20Work-455A64?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Open Related Work PDF"></a>
  <a href="./reviewer/reviewer_companion.pdf"><img src="https://img.shields.io/badge/Open-Reviewer%20Companion-B71C1C?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Open Reviewer Companion PDF"></a>
</p>

## Status

Steps 1 and 1.1 are shipped. **Step 2 is closed after frozen execution, independent statistical review, post-hoc mechanism diagnosis, and epistemic claim adjudication.**

The frozen benchmark evaluated seven policies over 3,360 paired episodes, four regimes, four fixed evidence budgets and thirty untouched headline seeds. The confirmatory family contained 240 Holm-corrected contrasts over terminal decision loss, Brier score and expected calibration error.

### Step 2 outcome

- one of 240 contrasts survived Holm correction: ECE, ED-POMDP versus classical POMDP, degraded evidence, budget 2;
- the paired bootstrap interval for that cell crossed zero and posterior support was sparse;
- no decision-loss contrast survived Holm correction;
- across the four acquisition baselines directly relevant to `CLM-VOI-001`, aggregate decision-loss directions were 10 favourable, 16 adverse and 38 equal;
- ED-POMDP produced zero unsafe GO decisions in the three avoidable regimes, versus two per regime for the classical POMDP; this endpoint was descriptive, not inferential.

### Mechanism diagnosis

The deterministic Step 2.8 analysis produced 2,400 paired episode diagnostics.

- ED-POMDP improved Brier score in 1,119 pairs;
- 1,054 of those improvements — **94.19%** — retained the same terminal action;
- ED-POMDP and the risk-only policy selected the same terminal action in all 480 paired episodes despite different acquisition traces in most episodes and different posterior values;
- better probabilistic beliefs therefore did not reliably convert into better release decisions under the frozen thresholds, fixed horizons and loss model.

## Claim disposition

- `CLM-VOI-001`: `NOT_SUPPORTED_STEP2`;
- `CLM-EQ-001`: `BROAD_FORM_NOT_SUPPORTED_NARROW_ECE_SIGNAL`.

Both claims now have evidence level `SYNTHETIC`, which records the type of adjudicating evidence rather than positive support. Evidence polarity and disposition are maintained separately in the canonical claim registry.

## Step 2 artifacts

- `benchmark/protocol/PREREGISTRATION.md` — frozen confirmatory protocol
- `benchmark/protocol/ANALYSIS_FREEZE.json` — analysis-freeze manifest
- `benchmark/config/FROZEN_ARTIFACTS.json` — cryptographic frozen-artifact lock
- `benchmark/results/headline_raw.csv` — 3,360 immutable episode rows
- `benchmark/results/headline_summary.csv` — frozen metric summaries
- `benchmark/results/headline_contrasts.csv` — 240 confirmatory contrasts
- `benchmark/results/STEP_2_7_RESULTS_REVIEW.md` — independent scientific reading
- `benchmark/results/step27_posthoc_directionality.csv` — audited aggregate directionality
- `benchmark/protocol/STEP_2_8_ANALYSIS_PLAN.md` — post-hoc boundary and close-out gate
- `benchmark/results/step28/` — deterministic mechanism tables, metadata and claim-adjudication report
- `paper/step2_closeout.tex` — scientific Step 2 close-out source

## Foundation documents

- `paper/main.tex` — main scientific-foundations paper
- `paper/step2_closeout.tex` — frozen benchmark results and claim adjudication
- `identifiability/identifiability_note.tex` — worked Cases A/B/C and intervention noise floor
- `research_program/research_program.tex` — research programme source
- `survey/related_work.tex` — related-work survey and novelty boundary
- `reviewer/reviewer_companion.tex` — reviewer companion
- `ontology/evidence_ontology.tex` — evidence ontology
- `appendix/mathematical_appendix.tex` — mathematical and experimental appendix
- `docs/CLAIMS.md` — canonical epistemic claim registry
- `docs/CLAIMS.csv` and `docs/CLAIMS.json` — CI-validated machine-readable mirrors
- `epistemic/EPISTEMIC_GOVERNANCE.md` — claim-governance rules
- `governance/DATA_READINESS_GATE.md` — industrial-data decision gate
- `roadmap/RESEARCH_TRACKS.md` — Committed, Conditional and North-Star tracks

## Build and tests

```bash
make all
make check
python -m pytest -q benchmark/tests
python -m benchmark.analysis.analyze_step28_mechanisms --output-dir /tmp/step28
```

Document builds require `latexmk` and `pdflatex`. Frozen headline generation and analysis require exactly **Python 3.12.13**. CI pins **pytest 9.1.1**.

## Scientific posture

The primary domain remains software release assurance. Step 2 did not validate broad ED-POMDP superiority. Its main contribution is a falsification result and a mechanism finding: improved modelling of evidence quality often changes beliefs without changing the terminal decision.

Any redesigned superiority claim must use a new preregistration, new development seeds and new untouched confirmatory seeds. Step 2 headline seeds must not become a tuning set.

## Repository roadmap

- Step 1 — Scientific foundations: shipped
- Step 1.1 — Epistemic foundations and identifiability: shipped
- Step 2 — Frozen matched-budget synthetic benchmark: closed
- Step 3 — Redesigned decision coupling and conditional industrial calibration: gated by a new protocol and data readiness
- Step 4 — Conditional shadow deployment and governed evaluation

## Citation

See `CITATION.cff`.
