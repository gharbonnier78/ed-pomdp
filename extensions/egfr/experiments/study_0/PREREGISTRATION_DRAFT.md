# EGFR Study 0 — preregistration draft

**Version:** 0.1-draft  
**Date:** 2026-08-09  
**Status:** protocol design only; margins and frozen manifests are not yet approved  
**Claims:** EGFR-CLM-RET-001 and EGFR-CLM-BUNDLE-001

## Purpose

Study 0 asks whether a hybrid recommender can recover useful, untried falsification actions on synthetic project families and emit valid proposal bundles. It does not test industrial effectiveness or sequential decision value.

## Data-generating process

The development simulator will generate:

- 200 projects grouped into families;
- 30 candidate actions;
- 6 failure modes;
- observable architecture, traffic, dependency, change, risk and environment features;
- latent project and action factors;
- action costs, durations and feasibility;
- noisy evidence outcomes;
- a complete evaluation-only potential-outcome matrix.

An initial candidate mechanism is:

[
z_jsimmathcal N(0,I_d),quad v_isimmathcal N(0,I_d),
]

[
p_{ji}=sigma(z_j^	op v_i+gamma^	op x_{ji}),quad O_{ji}sim Bernoulli(p_{ji}).
]

Detection probability, information gain and utility remain separate variables.

## Historical masking

The complete matrix is generated before masking. A logging indicator is sampled from a policy influenced by action popularity, project suspicion and simulated team expertise.

Regimes:

1. approximately random masking;
2. popularity-biased masking;
3. suspicion/expertise-biased masking;
4. held-out project-family distribution shift.

Unobserved cells are represented as question marks, never zeros.

## Methods

| ID | Candidate generator | Role |
|---|---|---|
| B0 | Random untried action | sanity baseline |
| B1 | Global popularity | habit baseline |
| B2 | Rule/risk heuristic | expert-system baseline |
| B3 | Observable-feature similarity | content-only baseline |
| M1 | Matrix factorization | collaborative baseline |
| M2 | Hybrid content plus collaborative model | candidate method |
| U0 | Simulator oracle | evaluation-only upper bound |

No method may access latent state or the complete matrix at training or recommendation time.

## Splits and leakage control

- Split by project family.
- Development families may be used for simulator debugging, model selection and margin selection.
- Confirmatory families and seeds remain untouched until the protocol, code and manifest are frozen.
- Near-duplicate releases from one family may not cross split boundaries.
- ED-POMDP Step 2 headline seeds may not be reused as EGFR development or confirmatory seeds.

## Task A — candidate retrieval

For each held-out project, retrieve the top three untried actions.

Primary endpoint:

[
Delta_{retrieval}=NDCG@3(M2)-max_{bin{B1,B2,B3}}NDCG@3(b).
]

Secondary endpoints:

- Recall@3;
- mean hidden utility of retrieved actions;
- coverage of rare failure modes;
- performance by masking regime;
- abstention behavior under family shift.

The strongest baseline is selected only from preregistered eligible baselines and is not changed after confirmatory results are known.

## Task B — falsification bundle validity

For every retrieved action, produce a structured bundle containing:

- claim;
- current and alternative hypotheses;
- falsifying observation;
- cost and constraints;
- uncertainty;
- evidence status;
- provenance;
- limitations;
- abstention reason when applicable;
- mandatory human validation.

Primary semantic invariants:

- unknown is never encoded as zero;
- inferred content is never labeled observed;
- not falsified is never labeled proven;
- no unsupported causal statement;
- no autonomous GO/NO-GO;
- no hidden change to objectives, constraints or framing.

## Statistical unit and intervals

The project is the primary independent unit. Report paired differences. Bootstrap resampling is clustered by project and stratified by held-out family where required. Cells and proposal bundles from one project are not treated as independent observations.

Simulator-seed sensitivity is reported separately from project-sampling uncertainty.

## Gates

### G0 — reproducibility

Pass requires the same frozen manifest to reproduce:

- simulator configuration and seeds;
- split identifiers;
- masked and evaluation-only matrix hashes;
- method configuration;
- predictions;
- metrics;
- gate outcomes.

### G1 — retrieval

Pass requires the paired project-clustered interval for the primary estimand to clear a practical margin selected from development data and frozen before confirmatory execution.

Current margin: **NULL — NOT YET FROZEN**.

If G1 fails, the disposition is BENEFIT_NOT_DEMONSTRATED. The result may not be reframed as preliminary success based only on a favorable mean.

### G2 — bundle validity

Pass requires all mandatory schema fields and semantic invariants to satisfy preregistered tolerances on held-out projects.

Current tolerances: **NULL — NOT YET FROZEN**.

A G2 failure blocks board-facing use even if G1 passes.

## Required run bundle

- frozen experiment manifest;
- code revision and dependency lock;
- simulator configuration and seeds;
- complete oracle matrix in an evaluation-only location;
- masked history with explicit unknowns;
- predictions and candidate bundles;
- project-level endpoint table;
- clustered interval samples;
- failure analysis;
- gate dispositions;
- limitations and revised priors.

## Stop rule

Study 0 stops at G0–G2. G3 sequential decision value, GO-ED-POMDP selection, hybrid replay, shadow deployment and industrial evaluation are out of scope until G1 and G2 have been independently reviewed.

## Non-claims

A pass would demonstrate only bounded performance in the frozen synthetic regimes. It would not demonstrate causal identification from project history, industrial transfer, autonomous decision authority or improvement of the existing ED-POMDP claim dispositions.
