"""Terminal decision semantics and preregistered loss endpoints.

The decision policy receives observations only. Ground-truth latent state is used
strictly after termination to score the decision.

The inference model is deliberately fixed to the identifiable functional-channel
likelihoods (0.80/0.20). It is not made regime-aware. Future evaluation against
non-identifiable or likelihood-misspecified environments therefore measures
robustness to model misspecification rather than silently adapting the agent to
the data-generating regime.

Terminal decisions are Bayes-optimal under ``LossWeights``. This same rule is used
by the episode runner and by decision-aware acquisition policies, preventing the
look-ahead model from optimizing against a different terminal decision-maker.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import log

from .simulator import EpisodeOutcome, Observation


class ReleaseDecision(str, Enum):
    GO = "GO"
    NO_GO = "NO_GO"
    CONDITIONAL_GO = "CONDITIONAL_GO"


@dataclass(frozen=True)
class LossWeights:
    unsafe_go: float = 10.0
    unnecessary_no_go: float = 2.0
    conditional_bad: float = 4.0
    conditional_good: float = 0.5
    evidence_cost: float = 0.1


@dataclass(frozen=True)
class DecisionScore:
    decision: ReleaseDecision
    decision_loss: float
    unsafe_go: bool
    unnecessary_no_go: bool
    acquisition_cost: float


def posterior_system_bad(history: tuple[Observation, ...], prior: float = 0.5) -> float:
    """Bayesian posterior under the fixed identifiable functional-channel model."""
    if not 0.0 < prior < 1.0:
        raise ValueError("prior must be between zero and one")
    log_odds = log(prior / (1.0 - prior))
    for obs in history:
        if obs.channel != "functional":
            continue
        p_bad = 0.80 if obs.failed else 0.20
        p_good = 0.20 if obs.failed else 0.80
        log_odds += log(p_bad / p_good)
    odds = pow(2.718281828459045, log_odds)
    return odds / (1.0 + odds)


def expected_terminal_risk(
    probability_bad: float,
    decision: ReleaseDecision,
    *,
    weights: LossWeights = LossWeights(),
) -> float:
    """Expected terminal loss for one decision at posterior risk ``probability_bad``."""
    if not 0.0 <= probability_bad <= 1.0:
        raise ValueError("probability_bad must be in [0, 1]")
    if decision is ReleaseDecision.GO:
        return weights.unsafe_go * probability_bad
    if decision is ReleaseDecision.NO_GO:
        return weights.unnecessary_no_go * (1.0 - probability_bad)
    return (
        weights.conditional_bad * probability_bad
        + weights.conditional_good * (1.0 - probability_bad)
    )


def decide_from_posterior(
    probability_bad: float,
    *,
    weights: LossWeights = LossWeights(),
) -> ReleaseDecision:
    """Return the Bayes-optimal terminal decision under ``weights``.

    Ties are resolved deterministically in the order GO, CONDITIONAL_GO, NO_GO.
    """
    ordered = (
        ReleaseDecision.GO,
        ReleaseDecision.CONDITIONAL_GO,
        ReleaseDecision.NO_GO,
    )
    return min(
        ordered,
        key=lambda decision: expected_terminal_risk(
            probability_bad, decision, weights=weights
        ),
    )


def score_decision(
    outcome: EpisodeOutcome,
    decision: ReleaseDecision,
    *,
    weights: LossWeights = LossWeights(),
) -> DecisionScore:
    unsafe_go = decision is ReleaseDecision.GO and outcome.true_system_bad
    unnecessary_no_go = decision is ReleaseDecision.NO_GO and not outcome.true_system_bad
    if unsafe_go:
        terminal_loss = weights.unsafe_go
    elif unnecessary_no_go:
        terminal_loss = weights.unnecessary_no_go
    elif decision is ReleaseDecision.CONDITIONAL_GO:
        terminal_loss = weights.conditional_bad if outcome.true_system_bad else weights.conditional_good
    else:
        terminal_loss = 0.0
    acquisition_cost = sum(obs.cost for obs in outcome.observations)
    return DecisionScore(
        decision=decision,
        decision_loss=terminal_loss + weights.evidence_cost * acquisition_cost,
        unsafe_go=unsafe_go,
        unnecessary_no_go=unnecessary_no_go,
        acquisition_cost=acquisition_cost,
    )
