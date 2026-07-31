# ED-POMDP Research Edition v1.2 — Step 2: Matched-Budget Benchmark

This repository develops **Evidence-Driven Partially Observable Markov Decision Processes applied to software release assurance**.

<p align="center">
  <a href="./paper/main.pdf"><img src="https://img.shields.io/badge/Open-Main%20Paper-0B5FFF?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Open Main Paper PDF"></a>
  <a href="./identifiability/identifiability_note.pdf"><img src="https://img.shields.io/badge/Open-Identifiability%20Note-6A1B9A?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Open Identifiability Note PDF"></a>
  <a href="./research_program/research_program.pdf"><img src="https://img.shields.io/badge/Open-Research%20Programme-00695C?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Open Research Programme PDF"></a>
</p>

<p align="center">
  <a href="./survey/related_work.pdf"><img src="https://img.shields.io/badge/Open-Related%20Work-455A64?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Open Related Work PDF"></a>
  <a href="./reviewer/reviewer_companion.pdf"><img src="https://img.shields.io/badge/Open-Reviewer%20Companion-B71C1C?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Open Reviewer Companion PDF"></a>
  <a href="./appendix/mathematical_appendix.pdf"><img src="https://img.shields.io/badge/Open-Mathematical%20Appendix-E65100?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Open Mathematical Appendix PDF"></a>
</p>

## Status

Step 1 and Step 1.1 are shipped. Step 2 is the current quantitative-validation increment.

Steps 2.4 and 2.5 established a causally relevant evidence-quality model and the complete seven-policy matrix. Step 2.6 now provides the paired fixed-horizon harness, metric/statistical implementation and cryptographic freeze guard.

The current Step 2.6 branch is a **freeze candidate**. No frozen-artifact lock, final analysis-freeze manifest or headline result has yet been produced. Both `CLM-VOI-001` and `CLM-EQ-001` remain at evidence level `NONE`.

## Step 2 benchmark

- `benchmark/README.md` — executable benchmark status and policy matrix
- `benchmark/protocol/PREREGISTRATION.md` — hypotheses, pairing, endpoints and refutation criteria
- `benchmark/config/headline_matrix.json` — canonical executable freeze candidate
- `benchmark/config/benchmark_matrix.yaml` — historical scaffold pointer
- `benchmark/METRICS.md` — frozen metric and inference definitions
- `benchmark/experiment/STEP_2_6_SCOPE.md` — common seeds, exact cost and freeze mechanics
- `benchmark/experiment/run_headline.py` — guarded raw-result entry point
- `benchmark/analysis/analyze_headline.py` — frozen analysis entry point

The candidate headline matrix contains four regimes, four budgets, thirty common seeds and seven policies: 3,360 episode rows and 320 confirmatory hypotheses.

## Foundation documents

- `paper/main.tex` — main scientific paper source
- `identifiability/identifiability_note.tex` — worked Cases A/B/C and intervention noise floor
- `research_program/research_program.tex` — research programme source
- `survey/related_work.tex` — related-work survey and novelty boundary
- `reviewer/reviewer_companion.tex` — reviewer companion
- `ontology/evidence_ontology.tex` — evidence ontology
- `appendix/mathematical_appendix.tex` — mathematical and experimental appendix
- `docs/CLAIMS.md` — canonical epistemic claim registry
- `epistemic/EPISTEMIC_GOVERNANCE.md` — claim-governance rules
- `governance/DATA_READINESS_GATE.md` — industrial-data decision gate
- `roadmap/RESEARCH_TRACKS.md` — Committed, Conditional and North-Star tracks

Compiled PDFs are generated from the LaTeX sources. The relative PDF buttons become active when compiled PDFs are present in the repository or release package.

## Build and tests

```bash
make all
make check
python -m pytest -q benchmark/tests
```

Document builds require `latexmk` and `pdflatex`. The Step 2.6 frozen headline runner and analysis require exactly **Python 3.12.13** and use only the Python standard library. The CI test environment additionally pins **pytest 9.1.1**.

## Scientific posture

The primary domain is software release assurance. Biometrics and UAV active perception remain North-Star external-validity studies. Step 2 tests whether decision-aware evidence acquisition and explicit evidence-quality modelling improve decisions under controlled, paired and exactly matched-budget conditions.

## Repository roadmap

- Step 1 — Scientific Foundations: shipped
- Step 1.1 — Epistemic Foundations and Identifiability: shipped
- Step 2 — Matched-budget benchmark and software-release demonstrator: current increment
- Step 3 — Conditional industrial calibration and retrospective replay
- Step 4 — Conditional shadow deployment and governed evaluation

## Citation

See `CITATION.cff`.
