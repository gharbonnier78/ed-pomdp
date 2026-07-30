"""Core contracts for the Step 2 ED-POMDP benchmark.

This module intentionally defines interfaces and validation only. It does not
claim that any policy has been implemented or evaluated.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Protocol, Sequence


class Decision(str, Enum):
    GO = "GO"
    CONDITIONAL_GO = "CONDITIONAL_GO"
    NO_GO = "NO_GO"


@dataclass(frozen=True)
class EvidenceAction:
    name: str
    cost: float
    channel: str

    def __post_init__(self) -> None:
        if self.cost < 0:
            raise ValueError("Evidence-action cost must be non-negative")
        if not self.name or not self.channel:
            raise ValueError("Evidence action requires name and channel")


@dataclass(frozen=True)
class Observation:
    channel: str
    value: str
    provenance_id: str


@dataclass(frozen=True)
class EpisodeContext:
    budget: float
    available_actions: Sequence[EvidenceAction]
    hard_constraints: Mapping[str, bool]

    def __post_init__(self) -> None:
        if self.budget < 0:
            raise ValueError("Episode budget must be non-negative")


class AcquisitionPolicy(Protocol):
    """Policy interface shared by ED-POMDP and all matched-budget baselines."""

    name: str

    def select_action(
        self,
        context: EpisodeContext,
        history: Sequence[Observation],
        remaining_budget: float,
    ) -> EvidenceAction | None:
        """Select the next affordable action, or stop acquisition."""

    def decide(
        self,
        context: EpisodeContext,
        history: Sequence[Observation],
    ) -> Decision:
        """Return the terminal release decision."""


def validate_matched_budget(
    contexts: Mapping[str, EpisodeContext],
) -> None:
    """Reject comparisons that give policies unequal benchmark privileges."""

    if not contexts:
        raise ValueError("At least one policy context is required")

    budgets = {context.budget for context in contexts.values()}
    if len(budgets) != 1:
        raise ValueError(f"Policies have unequal budgets: {sorted(budgets)}")

    channel_sets = {
        tuple(sorted(action.channel for action in context.available_actions))
        for context in contexts.values()
    }
    if len(channel_sets) != 1:
        raise ValueError("Policies do not have equal channel access")
