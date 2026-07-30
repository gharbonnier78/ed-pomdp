"""Reference acquisition policies for the executable benchmark core.

Policies receive observation history and channel names only. They never receive
latent system state, latent evidence quality, or simulator internals.
"""

from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Protocol, Sequence

from .simulator import Observation


class AcquisitionPolicy(Protocol):
    name: str

    def choose(self, history: Sequence[Observation], channels: Sequence[str]) -> str:
        ...


@dataclass
class FixedPolicy:
    name: str = "fixed"

    def choose(self, history: Sequence[Observation], channels: Sequence[str]) -> str:
        return channels[len(history) % len(channels)]


@dataclass
class RandomPolicy:
    seed: int
    name: str = "random"

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)

    def choose(self, history: Sequence[Observation], channels: Sequence[str]) -> str:
        return self._rng.choice(tuple(channels))


@dataclass
class FailureFocusedPolicy:
    """Observable-only proxy for risk-focused acquisition.

    After a failure, repeat the same channel once; otherwise alternate channels.
    This is intentionally simple and is not yet the final ED-POMDP policy.
    """

    name: str = "failure_focused_proxy"

    def choose(self, history: Sequence[Observation], channels: Sequence[str]) -> str:
        if history and history[-1].failed:
            return history[-1].channel
        return channels[len(history) % len(channels)]
