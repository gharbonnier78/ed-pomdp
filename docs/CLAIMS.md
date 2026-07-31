# Canonical claim registry

This file is the single source of truth for epistemic status. All papers, notes, experiments and reviewer responses reference these stable IDs.

Evidence level records the **kind of evidence available**, not whether that evidence supports the claim. `Evidence polarity` and `Disposition` record the scientific outcome.

| ID | Statement | Type | Maturity | Evidence level | Evidence polarity | Disposition | Refutation / gate | Supporting artifacts | Next step | Last revision |
|---|---|---|---|---|---|---|---|---|---|---|
| CLM-PO-001 | Software release assurance is structurally partially observable. | Conceptual claim | Formalized | FORMAL | SUPPORTIVE | ACTIVE | Produce a complete observable-state formulation with no hidden decision-relevant variable. | `paper/main.tex` | Formal counterexample comparison | 2026-07-31 |
| CLM-VOI-001 | Decision-aware value of information reduces matched-budget decision loss relative to fixed and entropy policies. | Falsifiable hypothesis | Step 2 adjudicated | SYNTHETIC | ADVERSE_MIXED | NOT_SUPPORTED_STEP2 | Reject if no material improvement under preregistered matched budgets and confidence intervals. No decision-loss contrast survived Holm correction; claim-relevant aggregate directions were 10 favourable, 16 adverse and 38 equal. | `benchmark/results/headline_contrasts.csv`; `benchmark/results/step27_posthoc_directionality.csv`; `benchmark/results/step28/STEP_2_8_CLAIM_ADJUDICATION.md` | Do not promote. Any redesigned VOI claim requires a new preregistration, new development seeds and new untouched confirmatory seeds. | 2026-07-31 |
| CLM-EQ-001 | Modelling evidence-production quality improves calibration under evidence degradation. | Falsifiable hypothesis | Step 2 adjudicated and narrowed | SYNTHETIC | MIXED_NARROW_POSITIVE | BROAD_FORM_NOT_SUPPORTED_NARROW_ECE_SIGNAL | Reject broad form if calibration and decision loss do not improve across degradation and misspecification. One degraded-evidence, budget-2 ECE contrast survived Holm, but its bootstrap interval crossed zero and posterior support was sparse. | `benchmark/results/headline_contrasts.csv`; `benchmark/results/STEP_2_7_RESULTS_REVIEW.md`; `benchmark/results/step28/STEP_2_8_CLAIM_ADJUDICATION.md` | Retain only the bounded calibration observation. Any general claim requires a new preregistered study. | 2026-07-31 |
| CLM-CON-001 | Hard non-compensatory assurance constraints can be integrated into the decision process. | Formal proposal | Formalized | FORMAL | SUPPORTIVE | ACTIVE | Reject implementation if any forbidden action is selected in exhaustive constrained test cases. | `appendix/mathematical_appendix.tex` | Executable zero-violation tests | 2026-07-31 |
| CLM-IDENT-001 | System state S and evidence quality E are not identifiable from arbitrary repeated observations; separation requires structural assumptions such as heterogeneous channels or controlled interventions. | Formal claim | Worked counterexample and separating construction established; empirical status open | FORMAL | SUPPORTIVE | ACTIVE_EMPIRICAL_GATE_OPEN | Refute the non-identifiability case by distinguishing the numerically aliased latent pairs from the unchanged channel alone. | `identifiability/identifiability_note.tex` | Synthetic identifiable / weak / non-identifiable regimes and later industrial calibration | 2026-07-31 |
| CLM-IND-001 | Industrial likelihood and evidence-quality models can be calibrated from governed release data. | Open question | Blocked by data gate | NONE | UNTESTED | BLOCKED | Requires `G_data=READY` and successful calibration with held-out evaluation. | `governance/DATA_READINESS_GATE.md` | Data readiness assessment | 2026-07-31 |
| CLM-XDOM-001 | The framework generalises to biometrics and UAV active perception. | Future hypothesis | North-Star only | NONE | UNTESTED | DEFERRED | Requires separate domain protocols and independent evaluation. | `research_program/research_program.tex` | External-validity studies, not on the critical path | 2026-07-31 |

## Evidence levels

- `NONE`: no empirical or formal evidence has yet been adjudicated.
- `FORMAL`: definition, derivation, proof or counterexample.
- `SYNTHETIC`: controlled generated evidence or simulation, including null or adverse evidence.
- `INDUSTRIAL`: governed retrospective or shadow evidence from real releases.
- `OPERATIONAL`: approved prospective operational evidence.

## Disposition vocabulary

- `ACTIVE`: retained without a closed empirical adjudication.
- `NOT_SUPPORTED_STEP2`: the broad claim did not satisfy its Step 2 promotion criterion.
- `BROAD_FORM_NOT_SUPPORTED_NARROW_ECE_SIGNAL`: the general claim is not promoted; one bounded calibration observation is retained with its limitations.
- `ACTIVE_EMPIRICAL_GATE_OPEN`: formal result retained; empirical validation remains open.
- `BLOCKED`: progression is prohibited until a named governance gate is passed.
- `DEFERRED`: outside the current critical path.

## Step 2 adjudication boundary

`CLM-VOI-001` is not labelled universally false. Step 2 establishes that the broad superiority claim is not supported under the frozen simulator, fixed horizons, loss weights, evidence structure and terminal decision rule.

`CLM-EQ-001` is not promoted on the basis of a single low-budget ECE rejection. The result is preserved as a narrow synthetic observation, not generalized to decision superiority or likelihood misspecification.

Mandatory unsafe-GO evidence remains descriptive. The favourable ED-POMDP safety pattern is reported in the Step 2.7 and Step 2.8 artifacts without inferential promotion.

## Machine-readable mirrors

- `docs/CLAIMS.csv`
- `docs/CLAIMS.json`

The mirrors must contain the same stable IDs, statements, evidence levels, polarities, dispositions, supporting artifacts, next steps and revision dates. This Markdown file remains authoritative.

## Governance rule

When another document differs from this register, this file governs the epistemic status and the discrepancy is treated as a repository defect.
