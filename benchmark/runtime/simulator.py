"""Executable synthetic environment for Step 2.1.

This module exposes only observable data to policies. Latent system state and
latent evidence quality remain internal to the environment and are used solely
for scoring after an episode.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import random


class Regime(str, Enum):
    IDENTIFIABLE = "identifiable"
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
        self._evidence_bad = self._rng.random() < 0.5
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
        if self.regime is Regime.NON_IDENTIFIABLE:
            # Deliberate aliasing: bad system/good evidence and good system/bad
            # evidence induce the same marginal observation probability.
            if self._system_bad != self._evidence_bad:
                return 0.80
            return 0.20

        if channel == "functional":
            return 0.80 if self._system_bad else 0.20
        return 0.80 if self._evidence_bad else 0.20
