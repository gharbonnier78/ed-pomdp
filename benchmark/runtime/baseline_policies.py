"""Principled baselines completing the preregistered Step 2 policy matrix."""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Mapping, Sequence

from .decision import (
    LossWeights,
    decide_from_posterior,
    expected_terminal_risk,
    joint_posterior,
    marginal_system_bad,
    observation_likelihood,
)
from .evidence_model import IDENTIFIABLE_AGENT_MODEL, State
from .policies import _require_channels, joint_model_posterior_bad
from .simulator import Observation


def shannon_entropy(distribution: Mapping[object, float]) -> float:
    """Shannon entropy in bits, ignoring zero-mass states."""
    return -sum(
        probability * math.log2(probability)
        for probability in distribution.values()
        if probability > 0.0
    )


def _joint_predictive_posterior(
    belief: Mapping[State, float],
    channel: str,
    failed: bool,
) -> tuple[float, dict[State, float]]:
    predictive = sum(
        probability * observation_likelihood(channel, failed, state)
        for state, probability in belief.items()
    )
    if predictive <= 0.0:
        return 0.0, dict(belief)
    posterior = {
        state: probability * observation_likelihood(channel, failed, state) / predictive
        for state, probability in belief.items()
    }
    return predictive, posterior


def expected_joint_entropy(history: Sequence[Observation], channel: str) -> float:
    """Expected entropy of full ``P(S,E | history, next observation)``."""
    belief = joint_posterior(history)
    expected = 0.0
    for failed in (False, True):
        predictive, posterior = _joint_predictive_posterior(belief, channel, failed)
        if predictive > 0.0:
            expected += predictive * shannon_entropy(posterior)
    return expected


def expected_system_uncertainty(history: Sequence[Observation], channel: str) -> float:
    """Expected Bernoulli variance of system risk after one observation.

    This baseline targets uncertainty about ``S`` only. It does not use terminal
    loss asymmetry and does not reward learning about ``E`` except insofar as that
    changes marginal uncertainty about ``S``.
    """
    belief = joint_posterior(history)
    expected = 0.0
    for failed in (False, True):
        predictive, posterior = _joint_predictive_posterior(belief, channel, failed)
        if predictive <= 0.0:
            continue
        probability_bad = marginal_system_bad(posterior)
        expected += predictive * probability_bad * (1.0 - probability_bad)
    return expected


@dataclass(frozen=True)
class EntropyReductionPolicy:
    name: str = "entropy_acquisition"

    def choose(self, history: Sequence[Observation], channels: Sequence[str]) -> str:
        available = _require_channels(channels)
        scored = [
            (expected_joint_entropy(history, channel), index, channel)
            for index, channel in enumerate(available)
        ]
        return min(scored)[2]

    def posterior_bad(self, history: Sequence[Observation]) -> float:
        return joint_model_posterior_bad(history)


@dataclass(frozen=True)
class RiskOnlyPolicy:
    name: str = "risk_only"

    def choose(self, history: Sequence[Observation], channels: Sequence[str]) -> str:
        available = _require_channels(channels)
        scored = [
            (expected_system_uncertainty(history, channel), index, channel)
            for index, channel in enumerate(available)
        ]
        return min(scored)[2]

    def posterior_bad(self, history: Sequence[Observation]) -> float:
        return joint_model_posterior_bad(history)


def classical_observation_likelihood(
    channel: str,
    failed: bool,
    system_bad: bool,
    *,
    evidence_bad_prior: float = 0.5,
) -> float:
    """Collapsed-S likelihood for a classical POMDP without latent ``E``.

    Evidence quality is permanently marginalized at its prior for every
    observation. The model therefore cannot learn that functional evidence has
    become more or less reliable after environment validation.
    """
    if not 0.0 <= evidence_bad_prior <= 1.0:
        raise ValueError("evidence_bad_prior must be in [0, 1]")
    p_fail = (
        (1.0 - evidence_bad_prior)
        * IDENTIFIABLE_AGENT_MODEL.failure_probability(channel, (system_bad, False))
        + evidence_bad_prior
        * IDENTIFIABLE_AGENT_MODEL.failure_probability(channel, (system_bad, True))
    )
    return p_fail if failed else 1.0 - p_fail


def classical_posterior_system_bad(
    history: Sequence[Observation],
    *,
    prior: float = 0.5,
    evidence_bad_prior: float = 0.5,
) -> float:
    if not 0.0 < prior < 1.0:
        raise ValueError("prior must be between zero and one")
    probability_bad = prior
    for observation in history:
        bad_likelihood = classical_observation_likelihood(
            observation.channel,
            observation.failed,
            True,
            evidence_bad_prior=evidence_bad_prior,
        )
        good_likelihood = classical_observation_likelihood(
            observation.channel,
            observation.failed,
            False,
            evidence_bad_prior=evidence_bad_prior,
        )
        predictive = (
            probability_bad * bad_likelihood
            + (1.0 - probability_bad) * good_likelihood
        )
        if predictive <= 0.0:
            raise ArithmeticError(
                "observation history has zero probability under classical model"
            )
        probability_bad = probability_bad * bad_likelihood / predictive
    return probability_bad


def _terminal_policy_risk(probability_bad: float, weights: LossWeights) -> float:
    decision = decide_from_posterior(probability_bad, weights=weights)
    return expected_terminal_risk(probability_bad, decision, weights=weights)


def expected_classical_one_step_loss(
    history: Sequence[Observation],
    channel: str,
    *,
    weights: LossWeights = LossWeights(),
    evidence_bad_prior: float = 0.5,
    observation_cost: float = 1.0,
) -> float:
    probability_bad = classical_posterior_system_bad(
        history, evidence_bad_prior=evidence_bad_prior
    )
    expected_risk = 0.0
    for failed in (False, True):
        bad_likelihood = classical_observation_likelihood(
            channel, failed, True, evidence_bad_prior=evidence_bad_prior
        )
        good_likelihood = classical_observation_likelihood(
            channel, failed, False, evidence_bad_prior=evidence_bad_prior
        )
        predictive = (
            probability_bad * bad_likelihood
            + (1.0 - probability_bad) * good_likelihood
        )
        if predictive <= 0.0:
            continue
        posterior_bad = probability_bad * bad_likelihood / predictive
        expected_risk += predictive * _terminal_policy_risk(posterior_bad, weights)
    return expected_risk + weights.evidence_cost * observation_cost


@dataclass(frozen=True)
class ClassicalPOMDPPolicy:
    weights: LossWeights = LossWeights()
    evidence_bad_prior: float = 0.5
    name: str = "classical_pomdp"

    def choose(self, history: Sequence[Observation], channels: Sequence[str]) -> str:
        available = _require_channels(channels)
        scored = [
            (
                expected_classical_one_step_loss(
                    history,
                    channel,
                    weights=self.weights,
                    evidence_bad_prior=self.evidence_bad_prior,
                ),
                index,
                channel,
            )
            for index, channel in enumerate(available)
        ]
        return min(scored)[2]

    def posterior_bad(self, history: Sequence[Observation]) -> float:
        return classical_posterior_system_bad(
            history, evidence_bad_prior=self.evidence_bad_prior
        )
