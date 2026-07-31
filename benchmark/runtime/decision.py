"""Posterior, terminal decision semantics and preregistered loss endpoints.

The runner and acquisition planner share the same joint posterior over system
quality and latent evidence-production quality. Functional evidence is reliable
only conditionally on evidence quality, while environment validation informs that
reliability without exposing the true latent state or simulator regime.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Sequence

from .evidence_model import IDENTIFIABLE_AGENT_MODEL, State
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


def observation_likelihood(channel: str, failed: bool, state: State) -> float:
    """Likelihood under the fixed, non-regime-aware agent evidence model."""
    return IDENTIFIABLE_AGENT_MODEL.likelihood(channel, failed, state)


def joint_posterior(
    history: Sequence[Observation],
    prior: Mapping[State, float] | None = None,
) -> dict[State, float]:
    """Return ``P(S,E | history)`` from observable evidence only."""
    states: tuple[State, ...] = (
        (False, False),
        (False, True),
        (True, False),
        (True, True),
    )
    belief = {state: 0.25 for state in states} if prior is None else dict(prior)
    if set(belief) != set(states) or any(value < 0.0 for value in belief.values()):
        raise ValueError("prior must define non-negative mass for all four joint states")
    total_prior = sum(belief.values())
    if total_prior <= 0.0:
        raise ValueError("prior mass must be positive")
    belief = {state: value / total_prior for state, value in belief.items()}

    for observation in history:
        belief = {
            state: probability
            * observation_likelihood(observation.channel, observation.failed, state)
            for state, probability in belief.items()
        }
        normalizer = sum(belief.values())
        if normalizer <= 0.0:
            raise ArithmeticError("observation history has zero probability under agent model")
        belief = {state: value / normalizer for state, value in belief.items()}
    return belief


def marginal_system_bad(belief: Mapping[State, float]) -> float:
    return sum(probability for (system_bad, _), probability in belief.items() if system_bad)


def marginal_evidence_bad(belief: Mapping[State, float]) -> float:
    return sum(probability for (_, evidence_bad), probability in belief.items() if evidence_bad)


def posterior_system_bad(history: tuple[Observation, ...], prior: float = 0.5) -> float:
    """Marginal system-risk posterior from the shared joint belief model."""
    if not 0.0 < prior < 1.0:
        raise ValueError("prior must be between zero and one")
    joint_prior = {
        (False, False): (1.0 - prior) * 0.5,
        (False, True): (1.0 - prior) * 0.5,
        (True, False): prior * 0.5,
        (True, True): prior * 0.5,
    }
    return marginal_system_bad(joint_posterior(history, prior=joint_prior))


def expected_terminal_risk(
    probability_bad: float,
    decision: ReleaseDecision,
    *,
    weights: LossWeights = LossWeights(),
) -> float:
    """Expected terminal loss for one decision at posterior risk."""
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
    """Return the Bayes-optimal terminal decision under ``weights``."""
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
        terminal_loss = (
            weights.conditional_bad
            if outcome.true_system_bad
            else weights.conditional_good
        )
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
