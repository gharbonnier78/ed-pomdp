"""Causal evidence-production model shared by inference and simulation.

Evidence quality is latent. When evidence quality is good, functional observations
are strongly discriminative of system quality. When evidence quality is bad, the
functional channel becomes non-discriminative and produces noisy failures at a
state-independent rate. Environment-validation observations inform evidence
quality, not system quality directly.
"""
from __future__ import annotations

from dataclasses import dataclass

State = tuple[bool, bool]  # (system_bad, evidence_bad)


@dataclass(frozen=True)
class EvidenceModel:
    functional_good_system_fail: float = 0.10
    functional_bad_system_fail: float = 0.95
    degraded_functional_fail: float = 0.60
    environment_good_evidence_fail: float = 0.20
    environment_bad_evidence_fail: float = 0.80

    def __post_init__(self) -> None:
        for name, value in self.__dict__.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0, 1]")

    def failure_probability(self, channel: str, state: State) -> float:
        system_bad, evidence_bad = state
        if channel == "functional":
            if evidence_bad:
                return self.degraded_functional_fail
            return (
                self.functional_bad_system_fail
                if system_bad
                else self.functional_good_system_fail
            )
        if channel == "environment_validation":
            return (
                self.environment_bad_evidence_fail
                if evidence_bad
                else self.environment_good_evidence_fail
            )
        raise ValueError(f"unknown channel: {channel}")

    def likelihood(self, channel: str, failed: bool, state: State) -> float:
        probability = self.failure_probability(channel, state)
        return probability if failed else 1.0 - probability


IDENTIFIABLE_AGENT_MODEL = EvidenceModel()

# Used only by the simulator's misspecification regime. The policy never receives
# this model or the regime identifier.
MISSPECIFIED_TRUE_MODEL = EvidenceModel(
    functional_good_system_fail=0.15,
    functional_bad_system_fail=0.85,
    degraded_functional_fail=0.70,
    environment_good_evidence_fail=0.30,
    environment_bad_evidence_fail=0.70,
)
