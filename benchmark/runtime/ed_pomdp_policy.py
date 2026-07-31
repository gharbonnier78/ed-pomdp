"""Decision-aware acquisition with causal evidence-quality relevance.

The policy maintains the same observable-history joint posterior used by the
runner. Because evidence quality controls functional-channel reliability,
environment validation can change system-risk calibration after functional
evidence without exposing true ``E`` or the simulator regime.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from .decision import (
    LossWeights,
    decide_from_posterior,
    expected_terminal_risk,
    joint_posterior,
    marginal_evidence_bad,
    marginal_system_bad,
    observation_likelihood,
)
from .simulator import Observation


def terminal_policy_risk(probability_system_bad: float, weights: LossWeights) -> float:
    """Risk of the exact Bayes-optimal terminal rule executed by the runner."""
    decision = decide_from_posterior(probability_system_bad, weights=weights)
    return expected_terminal_risk(probability_system_bad, decision, weights=weights)


def expected_one_step_terminal_risk(
    history: Sequence[Observation],
    channel: str,
    *,
    weights: LossWeights = LossWeights(),
) -> float:
    """Expected terminal risk after one observable acquisition, excluding cost."""
    belief = joint_posterior(history)
    expected_risk = 0.0
    for failed in (False, True):
        predictive = sum(
            probability * observation_likelihood(channel, failed, state)
            for state, probability in belief.items()
        )
        if predictive <= 0.0:
            continue
        posterior = {
            state: probability
            * observation_likelihood(channel, failed, state)
            / predictive
            for state, probability in belief.items()
        }
        expected_risk += predictive * terminal_policy_risk(
            marginal_system_bad(posterior), weights
        )
    return expected_risk


def decision_value_of_information(
    history: Sequence[Observation],
    channel: str,
    *,
    weights: LossWeights = LossWeights(),
) -> float:
    """Gross expected terminal-risk reduction from one acquisition."""
    current_belief = joint_posterior(history)
    current_risk = terminal_policy_risk(marginal_system_bad(current_belief), weights)
    return current_risk - expected_one_step_terminal_risk(
        history, channel, weights=weights
    )


def expected_one_step_loss(
    history: Sequence[Observation],
    channel: str,
    *,
    weights: LossWeights = LossWeights(),
    observation_cost: float = 1.0,
) -> float:
    """Expected terminal risk plus preregistered evidence cost."""
    return expected_one_step_terminal_risk(
        history, channel, weights=weights
    ) + weights.evidence_cost * observation_cost


@dataclass(frozen=True)
class EvidenceDrivenVoIPolicy:
    """Choose the channel minimizing expected realized decision loss."""

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
