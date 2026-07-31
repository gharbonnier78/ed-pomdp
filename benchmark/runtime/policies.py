"""Observable-only acquisition policies for the Step 2 benchmark matrix.

Every policy receives the same public inputs: observation history and available
channel names. The posterior method exposes the policy's own release-risk belief
for the shared stopping and terminal-decision rule. No policy receives latent
system state, latent evidence quality, or simulator regime.
"""
from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Protocol, Sequence

from .decision import joint_posterior, marginal_system_bad
from .simulator import Observation


class AcquisitionPolicy(Protocol):
    name: str

    def choose(self, history: Sequence[Observation], channels: Sequence[str]) -> str:
        ...

    def posterior_bad(self, history: Sequence[Observation]) -> float:
        ...


def _require_channels(channels: Sequence[str]) -> tuple[str, ...]:
    available = tuple(channels)
    if not available:
        raise ValueError("at least one channel is required")
    return available


def joint_model_posterior_bad(history: Sequence[Observation]) -> float:
    """Shared explicit-E posterior used by non-classical baselines."""
    return marginal_system_bad(joint_posterior(history))


@dataclass(frozen=True)
class FixedPolicy:
    """Cycle through a preregistered plan independently of observations."""

    name: str = "fixed_plan"
    plan: tuple[str, ...] = ("functional", "environment_validation")

    def choose(self, history: Sequence[Observation], channels: Sequence[str]) -> str:
        available = _require_channels(channels)
        if not self.plan:
            raise ValueError("fixed plan must contain at least one channel")
        channel = self.plan[len(history) % len(self.plan)]
        if channel not in available:
            raise ValueError(f"fixed-plan channel is unavailable: {channel}")
        return channel

    def posterior_bad(self, history: Sequence[Observation]) -> float:
        return joint_model_posterior_bad(history)


@dataclass
class RandomPolicy:
    """Seeded uniform acquisition over the common channel set."""

    seed: int
    name: str = "random_acquisition"

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)

    def choose(self, history: Sequence[Observation], channels: Sequence[str]) -> str:
        return self._rng.choice(_require_channels(channels))

    def posterior_bad(self, history: Sequence[Observation]) -> float:
        return joint_model_posterior_bad(history)


@dataclass(frozen=True)
class FailureFocusedPolicy:
    """Rule-based assurance baseline.

    Repeat the most recently failing channel; otherwise follow the fixed plan.
    The rule consumes observable results only and is intentionally not Bayesian
    acquisition planning.
    """

    name: str = "rule_based"
    plan: tuple[str, ...] = ("functional", "environment_validation")

    def choose(self, history: Sequence[Observation], channels: Sequence[str]) -> str:
        available = _require_channels(channels)
        if history and history[-1].failed:
            if history[-1].channel not in available:
                raise ValueError("last failing channel is no longer available")
            return history[-1].channel
        if not self.plan:
            raise ValueError("rule-based plan must contain at least one channel")
        channel = self.plan[len(history) % len(self.plan)]
        if channel not in available:
            raise ValueError(f"rule-based channel is unavailable: {channel}")
        return channel

    def posterior_bad(self, history: Sequence[Observation]) -> float:
        return joint_model_posterior_bad(history)
