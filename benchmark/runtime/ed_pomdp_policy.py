"""Minimal decision-aware evidence acquisition for Step 2.3.

The policy maintains an observable-history posterior over joint latent hypotheses
(system quality S, evidence-production quality E) under a fixed identifiable
agent model. It never receives the simulator's true S, E or regime.

This is a one-step look-ahead policy: for each available channel it computes the
expected terminal Bayes risk after the next pass/fail observation and selects the
channel with the lowest expected decision loss plus evidence cost.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from .decision import LossWeights, ReleaseDecision
from .simulator import Observation

State = tuple[bool, bool]  # (system_bad, evidence_bad)


def _likelihood(channel: str, failed: bool, state: State) -> float:
    system_bad, evidence_bad = state
    if channel == "functional":
        p_fail = 0.80 if system_bad else 0.20
    elif channel == "environment_validation":
        p_fail = 0.80 if evidence_bad else 0.20
    else:
        raise ValueError(f"unknown channel: {channel}")
    return p_fail if failed else 1.0 - p_fail


def joint_posterior(
    history: Sequence[Observation],
    prior: Mapping[State, float] | None = None,
) -> dict[State, float]:
    """Return P(S,E | observable history) under the fixed agent model."""
    states: tuple[State, ...] = ((False, False), (False, True), (True, False), (True, True))
    weights = {state: 0.25 for state in states} if prior is None else dict(prior)
    if set(weights) != set(states) or any(value < 0.0 for value in weights.values()):
        raise ValueError("prior must define non-negative mass for all four joint states")
    total_prior = sum(weights.values())
    if total_prior <= 0.0:
        raise ValueError("prior mass must be positive")
    weights = {state: value / total_prior for state, value in weights.items()}

    for observation in history:
        for state in states:
            weights[state] *= _likelihood(observation.channel, observation.failed, state)
        normalizer = sum(weights.values())
        if normalizer <= 0.0:
            raise ArithmeticError("observation history has zero probability under agent model")
        weights = {state: value / normalizer for state, value in weights.items()}
    return weights


def marginal_system_bad(belief: Mapping[State, float]) -> float:
    return sum(probability for (system_bad, _), probability in belief.items() if system_bad)


def marginal_evidence_bad(belief: Mapping[State, float]) -> float:
    return sum(probability for (_, evidence_bad), probability in belief.items() if evidence_bad)


def _terminal_bayes_risk(probability_system_bad: float, weights: LossWeights) -> float:
    risks = {
        ReleaseDecision.GO: weights.unsafe_go * probability_system_bad,
        ReleaseDecision.NO_GO: weights.unnecessary_no_go * (1.0 - probability_system_bad),
        ReleaseDecision.CONDITIONAL_GO: (
            weights.conditional_bad * probability_system_bad
            + weights.conditional_good * (1.0 - probability_system_bad)
        ),
    }
    return min(risks.values())


def expected_one_step_loss(
    history: Sequence[Observation],
    channel: str,
    *,
    weights: LossWeights = LossWeights(),
    observation_cost: float = 1.0,
) -> float:
    """Expected terminal Bayes risk after one observation on ``channel``."""
    belief = joint_posterior(history)
    expected_risk = 0.0
    for failed in (False, True):
        predictive = sum(
            probability * _likelihood(channel, failed, state)
            for state, probability in belief.items()
        )
        if predictive <= 0.0:
            continue
        posterior = {
            state: probability * _likelihood(channel, failed, state) / predictive
            for state, probability in belief.items()
        }
        expected_risk += predictive * _terminal_bayes_risk(marginal_system_bad(posterior), weights)
    return expected_risk + weights.evidence_cost * observation_cost


@dataclass(frozen=True)
class EvidenceDrivenVoIPolicy:
    """Choose the observable channel minimizing one-step expected decision loss."""

    weights: LossWeights = LossWeights()
    name: str = "ed_pomdp_one_step_voi"

    def choose(self, history: Sequence[Observation], channels: Sequence[str]) -> str:
        if not channels:
            raise ValueError("at least one channel is required")
        scored = [
            (expected_one_step_loss(history, channel, weights=self.weights), index, channel)
            for index, channel in enumerate(channels)
        ]
        return min(scored)[2]
