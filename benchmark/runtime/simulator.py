"""Executable synthetic environment with latent evidence-quality degradation.

Policies receive observations and channel names only. Latent system state, latent
evidence quality and the true simulator regime remain internal and are used for
observation generation and terminal scoring only.

Step 2.6 uses common random numbers for paired policy comparisons. Fresh
environment instances created with the same episode seed receive the same latent
uniform draws and the same observation-noise quantile at each acquisition step.
Policies may choose different channels, but they face the same exogenous scenario.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib

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


def deterministic_uniform(seed: int, stream: str) -> float:
    """Return a stable U[0,1) variate for one named deterministic stream.

    Python's process-randomized ``hash`` and mutable RNG consumption order are
    deliberately avoided. The mapping is stable across processes and platforms.
    """
    payload = f"ed-pomdp-step2|{seed}|{stream}".encode("utf-8")
    digest = hashlib.sha256(payload).digest()
    return int.from_bytes(digest[:8], "big") / float(1 << 64)


class SyntheticReleaseEnvironment:
    """Two-latent-state release model with a seed-addressable noise tape."""

    CHANNELS = ("functional", "environment_validation")

    def __init__(self, regime: Regime, seed: int) -> None:
        self.regime = regime
        self.seed = seed
        self._system_bad = deterministic_uniform(seed, "latent-system") < 0.5
        evidence_bad_prior = 0.80 if regime is Regime.EVIDENCE_DEGRADED else 0.50
        self._evidence_bad = (
            deterministic_uniform(seed, "latent-evidence") < evidence_bad_prior
        )
        self._observations: list[Observation] = []

    @property
    def available_channels(self) -> tuple[str, ...]:
        return self.CHANNELS

    def acquire(self, channel: str) -> Observation:
        if channel not in self.CHANNELS:
            raise ValueError(f"Unknown channel: {channel}")
        p_fail = self._failure_probability(channel)
        step = len(self._observations)
        # The noise quantile is indexed by acquisition step, not policy or
        # channel. This is a common-random-number coupling across policies.
        noise = deterministic_uniform(self.seed, f"observation-step-{step}")
        observation = Observation(channel=channel, failed=noise < p_fail)
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
