# EGFR as a governed MDP/POMDP research proposition

**Version:** 0.1  
**Status:** scientific positioning and falsifiable research proposition  
**Evidence status:** no EGFR experiment has yet been executed; all EGFR claims remain NONE / UNTESTED  
**Date:** 2026-08-15

## Purpose and boundary

This note records why sequential evidence-guided falsification can legitimately be studied through Markov decision process (MDP), partially observable Markov decision process (POMDP), and reinforcement-learning formalisms. It also separates that scientific basis from the stronger, currently unvalidated claim that EGFR will improve real engineering decisions.

The MDP/POMDP framing is not inferred from the name of this repository and is not evidence that EGFR works. It is a candidate mathematical representation whose adequacy must itself be tested.

## From an RL transition to an MDP

A reinforcement-learning experience is commonly represented as:

\[
(s_t,a_t,r_t,s_{t+1}),
\]

where \(s_t\) is the current state, \(a_t\) the selected action, \(r_t\) the reward, and \(s_{t+1}\) the next state.

A finite discounted MDP is commonly written:

\[
\mathcal{M}=(\mathcal{S},\mathcal{A},P,R,\gamma),
\]

with:

- \(\mathcal{S}\): state space;
- \(\mathcal{A}\): action space;
- \(P(s' \mid s,a)\): transition dynamics;
- \(R\): reward model;
- \(\gamma\): temporal discount factor.

Notation varies: an initial-state distribution, horizon, terminal set, or observation model may be stated separately. An MDP defines a sequential decision problem. Reinforcement learning is one family of methods for learning a policy when relevant parts of the model are unknown or must be learned through interaction. When the model is known, planning or dynamic programming may be more appropriate than RL.

## Why evidence-guided engineering is partially observable

The true condition of a system is not directly observed. Tests, traces, metrics, incidents, expert judgements, and contract checks provide incomplete and noisy observations.

Let the latent engineering state be:

\[
x_t=(\text{defects},\text{failure mechanisms},\text{detection capability},\text{residual risks}),
\]

and let the available observation be:

\[
o_t=(\text{test outcomes},\text{telemetry},\text{alerts},\text{reviews},\text{incidents}).
\]

In general:

\[
o_t \neq x_t
\quad\text{and}\quad
P(x_t\mid o_{1:t},a_{1:t-1})
\]

remains uncertain. This motivates a POMDP rather than a fully observed MDP.

A POMDP may be written:

\[
\mathcal{P}=(\mathcal{S},\mathcal{A},P,R,\Omega,O,\gamma),
\]

where \(\Omega\) is the observation space and \(O(o\mid s,a)\) is the observation model. The decision state can then be a belief distribution:

\[
b_t(s)=P(s_t=s\mid o_{1:t},a_{1:t-1}).
\]

This belief-state formulation is scientifically relevant to assurance: a PASS is evidence, not direct observation that no important defect exists.

## Candidate EGFR mapping

| Decision-process element | Candidate EGFR meaning |
|---|---|
| Latent state \(s_t\) | Actual failure mechanisms, system condition, detection capability, and material residual risk |
| Observation \(o_t\) | Test results, mutations, OTEL traces, monitoring signals, expert reviews, and incidents |
| Belief \(b_t\) | Auditable uncertainty over claims, failure hypotheses, and decision-relevant risk |
| Action \(a_t\) | Select, parameterize, or recommend a falsification experiment |
| Transition | System/testbed evolution plus belief update after new evidence |
| Reward or utility | Decision-relevant risk or uncertainty reduction minus evidence cost, delay, and induced risk |
| Terminal condition | Decision threshold reached, budget exhausted, mandatory evidence missing, or required human escalation |
| Policy | Governed strategy for selecting the next evidence-producing action |

The action is not the release decision itself. EGFR remains advisory and cannot issue an autonomous GO/NO-GO decision or accept residual risk.

## Scientific lineage and adjacent evidence

### MDP and RL foundations

Bellman's Markovian decision-process and dynamic-programming work establishes the multistage stochastic decision foundation. Sutton and Barto provide the standard modern connection between finite MDPs and reinforcement-learning methods.

This foundation supports the representation, not the effectiveness of the proposed EGFR system.

### POMDP foundations

Kaelbling, Littman, and Cassandra formalize planning and acting under partial observability, including belief-state reasoning and the dual role of actions: changing the world and gathering information.

This is directly relevant when evidence-producing actions both test a system and change what is believed about it.

### Adaptive Stress Testing

Adaptive Stress Testing (AST) formulates black-box search for likely failure trajectories as an MDP and uses reinforcement learning or related search methods to optimize that search. Lee et al. provide both fully observed and partially observed formulations.

AST is close to EGFR because both select sequential perturbations or scenarios to expose failures. It is not identical:

- AST primarily seeks likely trajectories to a specified failure event;
- EGFR seeks the next falsification action whose evidence is most useful to a governed engineering decision;
- EGFR must represent claims, provenance, contested objectives, abstention, evidence cost, and decision authority.

### NASA airborne collision-avoidance stress testing

NASA-linked research applied adaptive stress testing to airborne collision-avoidance systems, searching for likely scenarios leading to near mid-air collision events. This is important applied evidence that RL/MDP-based stress testing can target a real safety-critical decision system through simulation.

It does not establish safe online RL control, production deployment of EGFR, or transfer to software-release governance. Its evidential relevance is as an adjacent high-fidelity falsification method.

### RETECS

RETECS applies reinforcement learning to automatic test-case prioritization and selection in continuous integration. It uses test duration, recency, and failure history to reduce feedback time and was evaluated on three industrial case studies.

RETECS is relevant evidence that adaptive test selection can be formulated and evaluated using RL. It is narrower than EGFR:

- it ranks existing tests rather than generating provenance-complete falsification bundles;
- its target is rapid failure feedback rather than decision-changing evidence at equal total cost;
- historical failure detection is not equivalent to causal or information value;
- industrial case-study evaluation is not evidence of general production effectiveness.

## Research gap

The adjacent literature does not yet establish the full EGFR proposition:

> Given partially observed project history, explicit claims, risk hypotheses, evidence contracts, costs, constraints, and contested objectives, can a governed recommender retrieve or construct falsification actions and select actions that reduce project-level decision regret at equal total evidence budget, while preserving provenance, unknowns, abstention, and human decision authority?

The proposed contribution is the integration and evaluation of:

1. candidate generation from structured precedents;
2. explicit unknown semantics rather than missing-as-zero;
3. belief-aware and cost-aware sequential selection;
4. falsification bundles tied to claims and discriminating observations;
5. project-level evaluation against strong simple baselines;
6. governance invariants, abstention, dissent, and non-autonomous authority;
7. decision-changing evidence as the primary target rather than raw FAIL count.

## Falsifiable propositions

The canonical claims and gates remain in [claims.yaml](claims.yaml). This note adds no positive result.

The central propositions are:

- retrieval: hybrid retrieval exceeds the strongest eligible simple baseline on held-out synthetic project families;
- bundle integrity: generated proposals preserve mandatory semantics, explicit unknowns, and provenance;
- decision value: after G1 and G2, sequential selection reduces project-level decision regret at equal total evidence budget;
- robustness: performance and calibrated abstention remain within preregistered bounds under logging bias and project-family shift.

Failure to clear the preregistered margins leaves the relevant claim unsupported. Better retrieval alone does not imply better engineering decisions.

## Minimum comparative programme

Any sequential EGFR study should compare, at minimum:

1. random eligible action;
2. global popularity or historical-frequency selection;
3. transparent rule/risk heuristic;
4. observable-feature similarity;
5. non-sequential cost-aware information heuristic;
6. collaborative or hybrid retrieval;
7. sequential belief-aware selector;
8. simulator oracle as an evaluation-only upper bound.

Primary analysis must use projects, not project-action cells, as independent units. Development and confirmatory seeds must remain separated. Historical policies must be modelled explicitly because executed tests are not a randomized sample.

## Threats to validity and stop conditions

- Markov-state inadequacy: the state or belief omits material history.
- Reward misspecification: raw failure discovery is optimized instead of decision value.
- Simulator misspecification: synthetic mechanisms do not represent industrial causal structure.
- Logging-policy bias: historical expert choices are mistaken for action utility.
- Offline-RL extrapolation: unsupported actions receive optimistic value estimates.
- Non-stationarity: projects, tests, architectures, and objectives change.
- Unsafe exploration: learning actions create unacceptable operational risk.
- Authority leakage: a recommendation is treated as approval.
- Metric substitution: belief calibration or retrieval quality improves without changing decisions or loss.

A failure of state adequacy, provenance integrity, authority boundaries, or preregistered gates stops progression to autonomous or online selection.

## Maturity ladder

1. Synthetic, fully known simulator and simple baselines.
2. Replay on historical projects with explicit logging-bias analysis.
3. Shadow recommendations with no influence on execution.
4. Human-reviewed prospective pilot with bounded actions.
5. Only if prior gates pass: constrained sequential experimentation in a safe testbed.

No current claim authorizes level 4 or 5.

## References

1. Bellman, R. E. (1957). [A Markovian Decision Process](https://www.rand.org/pubs/papers/P1066.html). RAND P-1066.
2. Sutton, R. S., & Barto, A. G. (2018). [Reinforcement Learning: An Introduction, 2nd ed.](https://incompleteideas.net/book/the-book-2nd.html). MIT Press.
3. Kaelbling, L. P., Littman, M. L., & Cassandra, A. R. (1998). [Planning and Acting in Partially Observable Stochastic Domains](https://doi.org/10.1016/S0004-3702(98)00023-X). Artificial Intelligence, 101(1–2), 99–134.
4. Lee, R., Mengshoel, O. J., Saksena, A., Gardner, R. W., Genin, D., Brush, J., & Kochenderfer, M. J. (2020). [Adaptive Stress Testing: Finding Likely Failure Events with Reinforcement Learning](https://www.jair.org/index.php/jair/article/view/12190). Journal of Artificial Intelligence Research, 69, 1165–1201.
5. Lee, R., Kochenderfer, M. J., Mengshoel, O. J., Brat, G. P., & Owen, M. P. (2015). [Adaptive Stress Testing of Airborne Collision Avoidance Systems](https://ntrs.nasa.gov/citations/20160005033). NASA NTRS record 20160005033.
6. Koren, M., Alsaif, S., Lee, R., & Kochenderfer, M. J. (2018). [Adaptive Stress Testing for Autonomous Vehicles](https://doi.org/10.1109/IVS.2018.8500400). IEEE Intelligent Vehicles Symposium.
7. Spieker, H., Gotlieb, A., Marijan, D., & Mossige, M. (2017). [Reinforcement Learning for Automatic Test Case Prioritization and Selection in Continuous Integration](https://doi.org/10.1145/3092703.3092709). ISSTA 2017.

## Traceability

- Concept and architecture: [README.md](README.md)
- Canonical bounded claims: [claims.yaml](claims.yaml)
- Study 0 preregistration: [experiments/study_0/PREREGISTRATION_DRAFT.md](experiments/study_0/PREREGISTRATION_DRAFT.md)
- Advisory persona boundary: [personas/integration_strategy_challenger/role_contract.yaml](personas/integration_strategy_challenger/role_contract.yaml)
