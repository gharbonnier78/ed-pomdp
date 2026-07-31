"""Executable synthetic environment with latent evidence-quality degradation.

Policies receive observations and channel names only. Latent system state, latent
evidence quality and the true simulator regime remain internal and are used for
observation generation and terminal scoring only.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import random

from .evidence_model import IDENTIFIABLE_AGENT_MODEL, MISSPECIFIED_TRUE_MODEL


class Regime(str, Enum):
    IDENTIFIABLE = "identifiable"
    EVIDENCE_DEGRADED = "evidence_degraded"
    LIKELIHOOD_MISSPECIFIED = "likelihood_misspecified"
    NON_IDENTIFIABLE = "non_identifiable"


@dataclass(frozen=True)
class Observation:
    channel: str
    failed: bool
    cost: float = 1.0


@dataclass(frozen=True)
class EpisodeOutcome:
    observations: tuple[Observation, ...]
    true_system_bad: bool
    true_evidence_bad: bool


class SyntheticReleaseEnvironment:
    """Two-latent-state release model with seed-stable observations."""

    CHANNELS = ("functional", "environment_validation")

    def __init__(self, regime: Regime, seed: int) -> None:
        self.regime = regime
        self._rng = random.Random(seed)
        self._system_bad = self._rng.random() < 0.5
        evidence_bad_prior = 0.80 if regime is Regime.EVIDENCE_DEGRADED else 0.50
        self._evidence_bad = self._rng.random() < evidence_bad_prior
        self._observations: list[Observation] = []

    @property
    def available_channels(self) -> tuple[str, ...]:
        return self.CHANNELS

    def acquire(self, channel: str) -> Observation:
        if channel not in self.CHANNELS:
            raise ValueError(f"Unknown channel: {channel}")
        p_fail = self._failure_probability(channel)
        observation = Observation(channel=channel, failed=self._rng.random() < p_fail)
        self._observations.append(observation)
        return observation

    def finish(self) -> EpisodeOutcome:
        return EpisodeOutcome(
            observations=tuple(self._observations),
            true_system_bad=self._system_bad,
            true_evidence_bad=self._evidence_bad,
        )

    def _failure_probability(self, channel: str) -> float:
        state = (self._system_bad, self._evidence_bad)
        if self.regime is Regime.NON_IDENTIFIABLE:
            # Deliberate aliasing: latent causes cannot be separated from the
            # observable distribution in this regime.
            if self._system_bad != self._evidence_bad:
                return 0.80
            return 0.20
        if self.regime is Regime.LIKELIHOOD_MISSPECIFIED:
            return MISSPECIFIED_TRUE_MODEL.failure_probability(channel, state)
        return IDENTIFIABLE_AGENT_MODEL.failure_probability(channel, state)
