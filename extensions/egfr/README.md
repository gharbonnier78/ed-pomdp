# Evidence-Guided Falsification Recommender (EGFR)

**Research concept v0.1**  
**Status:** research hypothesis; no EGFR experiment has yet been executed  
**Date:** 2026-08-09

## Definition

An Evidence-Guided Falsification Recommender generates traceable, falsifiable proposals from prior cases, exposes assumptions and objective trade-offs, estimates consequences through simulation or replay, and learns from the evidence actually produced.

It does not claim to identify the true or optimal next test. It proposes candidate directions that can be challenged.

## Research question

> Given an incompletely observed history of projects, risks, tests, evidence and decisions, can EGFR retrieve useful untried falsification actions and support selection under explicit costs, risks and objective uncertainty better than simple baselines?

This separates candidate generation from decision support. Similarity, collaborative filtering and structured retrieval can support candidate generation. Selection additionally requires beliefs, expected information, costs, constraints and possibly GO-ED-POMDP.

## Scientific positioning

The MDP/POMDP basis, its limits, the research gap, and the falsifiable comparative programme are documented in [EGFR as a governed MDP/POMDP research proposition](RESEARCH_PROPOSAL_MDP_POMDP.md). The note relates EGFR to Adaptive Stress Testing, NASA airborne collision-avoidance stress testing, autonomous-vehicle AST, and RETECS while distinguishing adjacent applied evidence from evidence for EGFR itself.

## Architectural boundary

| Component | Responsibility | Explicit non-responsibility |
|---|---|---|
| ESC/BOS/DMN | Claims, observable properties, evidence contracts and rules | Learn the next experiment |
| OTEL/test runners | Execution observations and evidence | Infer causal utility alone |
| EGFR | Falsifiable candidate bundles from precedents and explicit unknowns | Authoritative GO/NO-GO |
| STRAT-Q | Goals, weights, trade-offs and rationale | Invent missing evidence |
| GO-ED-POMDP | Sequential evidence selection under beliefs and constraints | Replace contracts or accountability |
| Research-assurance harness | Preserve claims, gates, failures and revisions | Reframe a failed gate as success |

EGFR is an optional upstream candidate generator. It does not rescue or reinterpret ED-POMDP Step 2. In particular, CLM-VOI-001 remains NOT_SUPPORTED_STEP2.

## Recommendation unit

A recommendation is a falsification proposal bundle:

\[
p=(a,c,H,A,o^{-},d,C,q,\pi),
\]

where \(a\) is the action, \(c\) the challenged claim, \(H\) the current hypothesis, \(A\) an alternative, \(o^{-}\) a falsifying observation, \(d\) the expected discriminative value, \(C\) the cost and constraints, \(q\) the uncertainty, and \(\pi\) the provenance.

“Not falsified in tested conditions” must never be rewritten as “proven true.”

## Explicit unknowns

For project \(j\) and action \(i\):

\[
Y_{ji}\in\{?,\text{not relevant},\text{inconclusive}\}\cup\mathbb{R}^k.
\]

Crucially, \(?\neq 0\). A question mark means untried, missing or insufficiently observed. Zero means an evaluated component was observed to be zero. Treating missing cells as negative evidence encodes organizational blind spots as truth.

Each field must carry provenance: automatically observed, human declared, model inferred, or human reviewed.

## Conditional utility

For action \(a\), belief \(b\) and visible objective weights \(w\):

\[
U(a\mid b,w)=w_R\Delta R(a)+w_I IG(a\mid b)+w_C\Delta Coverage(a)+w_D\Delta DecisionConfidence(a)-w_E Cost(a)-w_T Delay(a).
\]

Weights are contestable. When objectives conflict, EGFR should expose named scenarios or a Pareto set rather than conceal the conflict in one score.

## Historical-bias threat

Historical execution is not randomized:

\[
P(A=a\mid S=s)\neq P(A=a).
\]

Experts may select difficult tests only when they already suspect a problem. Popular tests may be over-recorded; negative and inconclusive outcomes may be under-recorded. EGFR can therefore learn habit and selection bias rather than utility.

Study 0 first creates a complete synthetic potential-outcome matrix, then masks it with a biased historical policy. The hidden complete matrix is evaluation-only and unavailable to recommenders.

## Study 0 summary

Generate synthetic projects, failure hypotheses, actions, costs and noisy observations. Compare:

| ID | Method |
|---|---|
| B0 | Random untried action |
| B1 | Global popularity |
| B2 | Rule/risk heuristic |
| B3 | Observable-feature similarity |
| M1 | Collaborative filtering |
| M2 | Hybrid content plus collaborative model |
| U0 | Simulator oracle, evaluation-only upper bound |

Hold out complete project families. Evaluate top-\(k\) retrieval with Recall@\(k\), NDCG@\(k\), action utility, rare-failure coverage and calibrated abstention under shift.

The project is the primary independent unit. Intervals must be paired and clustered by project; cells within one project are not independent.

## Gates

| Gate | Purpose | Current state |
|---|---|---|
| G0 | Reproducible run from a frozen manifest | NOT_RUN |
| G1 | Retrieval value beyond strong simple baselines | NOT_RUN |
| G2 | Schema-valid, consistent falsification bundles | NOT_RUN |
| G3 | Lower decision regret at equal budget | DEFERRED |
| G4 | Robustness to selection bias and distribution shift | DEFERRED |

The first implementation stops at G0–G2. Practical margins must be selected from a development pilot and frozen before confirmatory execution.

## Persona boundary

EGFR is a reasoning engine, not a persona. Its board-facing interface is the **AI Integration Strategy Challenger**. This actor generates and compares falsifiable integration directions, exposes incompatible objectives and asks for discriminating evidence.

It is advisory only. It may propose, compare, simulate, challenge, abstain and preserve dissent. It may not accept residual risk, qualify high-impact evidence alone, erase disagreement, or issue an autonomous GO/NO-GO.

See the role contract in personas/integration_strategy_challenger/role_contract.yaml.

## Repository decision

EGFR is incubated here as a bounded v0.x extension. A separate repository requires an independently evaluated claim, a stable interface usable without GO-ED-POMDP, a second consumer or domain, materially divergent dependencies or cadence, and evidence that extraction improves reproducibility.

The reserved future name evidence-guided-falsification is not the current project status.

## Immediate slice

1. Generate 200 synthetic projects, 30 actions and 6 failure modes.
2. Create the complete evaluation-only potential-outcome matrix.
3. Mask it with random and biased historical policies.
4. Compare B0, B1, B3, M1 and M2 on held-out project families.
5. Emit top-3 falsification bundles with provenance.
6. Evaluate project-clustered Recall@3, NDCG@3 and schema consistency.
7. Publish G0–G2 outcomes, including failures, before any sequential POMDP layer.

## Explicit non-claims

Version 0.1 does not claim that historical similarity identifies causal utility; a recommended action is correct or optimal; synthetic performance transfers to industry; AI-generated RETEX is valid without review; one score resolves disagreement; collaborative filtering selects the scientifically best next experiment; or EGFR improves the adjudicated ED-POMDP Step 2 results.
