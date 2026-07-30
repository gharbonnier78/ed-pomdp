# Canonical claim registry

This file is the single source of truth for epistemic status. All papers, notes, experiments and reviewer responses reference these stable IDs.

| ID | Statement | Type | Maturity | Evidence level | Refutation / gate | Supporting artifact | Next step |
|---|---|---|---|---|---|---|---|
| CLM-PO-001 | Software release assurance is structurally partially observable. | Conceptual claim | Formalized | FORMAL | Produce a complete observable-state formulation with no hidden decision-relevant variable. | `paper/main.tex` | Formal counterexample comparison |
| CLM-VOI-001 | Decision-aware value of information reduces matched-budget decision loss relative to fixed and entropy policies. | Hypothesis | Falsifiable | NONE | Reject if no material improvement under preregistered matched budgets and confidence intervals. | `paper/main.tex` | Step 2 benchmark |
| CLM-EQ-001 | Modelling evidence-production quality improves calibration under evidence degradation. | Hypothesis | Falsifiable | NONE | Reject if calibration and decision loss do not improve under misspecification tests. | `paper/main.tex` | Step 2 degradation experiments |
| CLM-CON-001 | Hard non-compensatory assurance constraints can be integrated into the decision process. | Formal proposal | Formalized | FORMAL | Reject implementation if any forbidden action is selected in exhaustive constrained test cases. | `appendix/mathematical_appendix.tex` | Executable zero-violation tests |
| CLM-IDENT-001 | System state S and evidence quality E are not identifiable from arbitrary repeated observations; separation requires structural assumptions such as heterogeneous channels or controlled interventions. | Formal claim | Worked counterexample and separating construction established; empirical status open | FORMAL | Refute the non-identifiability case by distinguishing the numerically aliased latent pairs from the unchanged channel alone. | `identifiability/identifiability_note.tex` (worked Cases A/B/C) | Synthetic identifiable / weak / non-identifiable regimes |
| CLM-IND-001 | Industrial likelihood and evidence-quality models can be calibrated from governed release data. | Open question | Blocked by data gate | NONE | Requires `G_data=READY` and successful calibration with held-out evaluation. | `governance/DATA_READINESS_GATE.md` | Data readiness assessment |
| CLM-XDOM-001 | The framework generalises to biometrics and UAV active perception. | Future hypothesis | North-Star only | NONE | Requires separate domain protocols and independent evaluation. | `research_program/research_program.tex` | External-validity studies, not on critical path |

## Evidence levels

- `NONE`: no supporting result yet.
- `FORMAL`: definition, derivation, proof or counterexample.
- `SYNTHETIC`: controlled generated evidence.
- `INDUSTRIAL`: governed retrospective or shadow evidence.
- `OPERATIONAL`: approved prospective operational evidence.

## Governance rule

When another document differs from this register, this file governs the epistemic status and the discrepancy is treated as a repository defect.