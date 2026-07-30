"""Matched-budget execution helpers for Step 2.1 smoke experiments."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .policies import AcquisitionPolicy
from .simulator import EpisodeOutcome, Observation, Regime, SyntheticReleaseEnvironment


@dataclass(frozen=True)
class EpisodeRecord:
    seed: int
    regime: str
    policy: str
    budget: float
    spent: float
    acquisitions: int
    outcome: EpisodeOutcome


def run_episode(
    *,
    seed: int,
    regime: Regime,
    policy: AcquisitionPolicy,
    budget: float,
) -> EpisodeRecord:
    if budget <= 0:
        raise ValueError("budget must be positive")

    environment = SyntheticReleaseEnvironment(regime=regime, seed=seed)
    history: list[Observation] = []
    spent = 0.0

    while spent + 1.0 <= budget:
        channel = policy.choose(tuple(history), environment.available_channels)
        observation = environment.acquire(channel)
        history.append(observation)
        spent += observation.cost

    return EpisodeRecord(
        seed=seed,
        regime=regime.value,
        policy=policy.name,
        budget=budget,
        spent=spent,
        acquisitions=len(history),
        outcome=environment.finish(),
    )


def validate_matched_records(records: Iterable[EpisodeRecord]) -> None:
    records = tuple(records)
    if not records:
        raise ValueError("at least one record is required")
    budgets = {record.budget for record in records}
    spent = {record.spent for record in records}
    acquisitions = {record.acquisitions for record in records}
    if len(budgets) != 1 or len(spent) != 1 or len(acquisitions) != 1:
        raise AssertionError("policies were not evaluated under a matched budget")
