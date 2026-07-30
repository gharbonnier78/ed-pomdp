# ED-POMDP Research Edition v1.1 — Step 1.1: Epistemic Foundations

This repository is the reviewer-oriented scientific foundation for **Evidence-Driven Partially Observable Markov Decision Processes applied to software release assurance**.

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

Step 1 is shipped. Step 1.1 is the current de-risking increment and must not be confused with completion of Step 1. It adds identifiability analysis, epistemic governance, a canonical claim registry, programme re-scoping and a mandatory data-readiness gate.

No operational superiority, real-data calibration or cross-domain validation is claimed.

## Documents

- `paper/main.tex` — main scientific paper source
- `identifiability/identifiability_note.tex` — S/E identifiability note and intervention noise floor
- `research_program/research_program.tex` — research programme source
- `survey/related_work.tex` — related-work survey and novelty boundary
- `reviewer/reviewer_companion.tex` — reviewer companion
- `ontology/evidence_ontology.tex` — evidence ontology
- `appendix/mathematical_appendix.tex` — mathematical and experimental appendix
- `docs/CLAIMS.md` — canonical epistemic claim registry
- `epistemic/EPISTEMIC_GOVERNANCE.md` — claim-governance rules
- `governance/DATA_READINESS_GATE.md` — industrial-data decision gate
- `roadmap/RESEARCH_TRACKS.md` — Committed, Conditional and North-Star tracks

Compiled PDFs are generated from the LaTeX sources. The relative PDF buttons above become active when the compiled PDFs are present in the repository or release package.

## Build

```bash
make all
make check
```

Requirements: `latexmk`, `pdflatex`, and Python 3. Bibliography is embedded for portable builds.

## Scientific posture

The primary domain is software release assurance. Biometrics and UAV active perception remain North-Star external-validity studies. The central open question is whether evidence quality and system state can be identified and calibrated robustly from governed assurance data.

## Repository roadmap

- Step 1 — Scientific Foundations: shipped
- Step 1.1 — Epistemic Foundations and Identifiability: current increment
- Step 2 — Matched-budget benchmark and software-release demonstrator
- Step 3 — Conditional industrial calibration and retrospective replay
- Step 4 — Conditional shadow deployment and governed evaluation

## Citation

See `CITATION.cff`.
