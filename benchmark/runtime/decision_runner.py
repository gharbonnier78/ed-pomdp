"""Stopping-capable episode runner with shared loss and policy-specific beliefs."""
from __future__ import annotations

from dataclasses import dataclass

from .decision import (
    DecisionScore,
    LossWeights,
    ReleaseDecision,
    decide_from_posterior,
    score_decision,
)
from .policies import AcquisitionPolicy
from .simulator import Observation, Regime, SyntheticReleaseEnvironment


@dataclass(frozen=True)
class DecisionEpisodeRecord:
    seed: int
    regime: str
    policy: str
    budget: float
    spent: float
    acquisitions: int
    stopped_early: bool
    posterior_bad: float
    score: DecisionScore


def run_decision_episode(
    *,
    seed: int,
    regime: Regime,
    policy: AcquisitionPolicy,
    budget: float,
    minimum_acquisitions: int = 2,
    weights: LossWeights = LossWeights(),
) -> DecisionEpisodeRecord:
    if budget <= 0:
        raise ValueError("budget must be positive")
    if minimum_acquisitions < 0:
        raise ValueError("minimum_acquisitions must be non-negative")

    environment = SyntheticReleaseEnvironment(regime=regime, seed=seed)
    history: list[Observation] = []
    spent = 0.0
    stopped_early = False

    while spent + 1.0 <= budget:
        channel = policy.choose(tuple(history), environment.available_channels)
        observation = environment.acquire(channel)
        history.append(observation)
        spent += observation.cost

        probability_bad = policy.posterior_bad(tuple(history))
        decision = decide_from_posterior(probability_bad, weights=weights)
        if len(history) >= minimum_acquisitions and decision is not ReleaseDecision.CONDITIONAL_GO:
            stopped_early = spent + 1.0 <= budget
            break

    probability_bad = policy.posterior_bad(tuple(history))
    decision = decide_from_posterior(probability_bad, weights=weights)
    outcome = environment.finish()
    score = score_decision(outcome, decision, weights=weights)
    return DecisionEpisodeRecord(
        seed=seed,
        regime=regime.value,
        policy=policy.name,
        budget=budget,
        spent=spent,
        acquisitions=len(history),
        stopped_early=stopped_early,
        posterior_bad=probability_bad,
        score=score,
    )


def validate_budget_ceiling(record: DecisionEpisodeRecord) -> None:
    """Validate feasibility without pretending stopping policies spend equally."""
    if record.spent > record.budget:
        raise AssertionError("policy exceeded the assigned budget ceiling")
    if record.acquisitions < 0:
        raise AssertionError("acquisition count cannot be negative")
