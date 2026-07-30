"""Terminal decision semantics and preregistered loss endpoints for Step 2.2.

The decision policy receives observations only. Ground-truth latent state is used
strictly after termination to score the decision.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import log

from .simulator import EpisodeOutcome, Observation


class ReleaseDecision(str, Enum):
    GO = "GO"
    NO_GO = "NO_GO"
    CONDITIONAL_GO = "CONDITIONAL_GO"


@dataclass(frozen=True)
class LossWeights:
    unsafe_go: float = 10.0
    unnecessary_no_go: float = 2.0
    conditional_bad: float = 4.0
    conditional_good: float = 0.5
    evidence_cost: float = 0.1


@dataclass(frozen=True)
class DecisionScore:
    decision: ReleaseDecision
    decision_loss: float
    unsafe_go: bool
    unnecessary_no_go: bool
    acquisition_cost: float


def posterior_system_bad(history: tuple[Observation, ...], prior: float = 0.5) -> float:
    """Bayesian posterior under the identifiable functional-channel model.

    Environment-validation observations are intentionally excluded from the
    system-state likelihood; they inform evidence quality in later increments.
    """
    if not 0.0 < prior < 1.0:
        raise ValueError("prior must be between zero and one")
    log_odds = log(prior / (1.0 - prior))
    for obs in history:
        if obs.channel != "functional":
            continue
        p_bad = 0.80 if obs.failed else 0.20
        p_good = 0.20 if obs.failed else 0.80
        log_odds += log(p_bad / p_good)
    odds = pow(2.718281828459045, log_odds)
    return odds / (1.0 + odds)


def decide_from_posterior(
    probability_bad: float,
    *,
    go_threshold: float = 0.20,
    no_go_threshold: float = 0.80,
) -> ReleaseDecision:
    if not 0.0 <= probability_bad <= 1.0:
        raise ValueError("probability_bad must be in [0, 1]")
    if not 0.0 <= go_threshold < no_go_threshold <= 1.0:
        raise ValueError("thresholds must satisfy 0 <= go < no_go <= 1")
    if probability_bad <= go_threshold:
        return ReleaseDecision.GO
    if probability_bad >= no_go_threshold:
        return ReleaseDecision.NO_GO
    return ReleaseDecision.CONDITIONAL_GO


def score_decision(
    outcome: EpisodeOutcome,
    decision: ReleaseDecision,
    *,
    weights: LossWeights = LossWeights(),
) -> DecisionScore:
    unsafe_go = decision is ReleaseDecision.GO and outcome.true_system_bad
    unnecessary_no_go = decision is ReleaseDecision.NO_GO and not outcome.true_system_bad
    if unsafe_go:
        terminal_loss = weights.unsafe_go
    elif unnecessary_no_go:
        terminal_loss = weights.unnecessary_no_go
    elif decision is ReleaseDecision.CONDITIONAL_GO:
        terminal_loss = weights.conditional_bad if outcome.true_system_bad else weights.conditional_good
    else:
        terminal_loss = 0.0
    acquisition_cost = sum(obs.cost for obs in outcome.observations)
    return DecisionScore(
        decision=decision,
        decision_loss=terminal_loss + weights.evidence_cost * acquisition_cost,
        unsafe_go=unsafe_go,
        unnecessary_no_go=unnecessary_no_go,
        acquisition_cost=acquisition_cost,
    )
