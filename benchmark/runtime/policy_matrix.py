"""Canonical constructors for the seven preregistered Step 2 policies."""
from __future__ import annotations

from .baseline_policies import (
    ClassicalPOMDPPolicy,
    EntropyReductionPolicy,
    RiskOnlyPolicy,
)
from .decision import LossWeights
from .ed_pomdp_policy import EvidenceDrivenVoIPolicy
from .policies import FailureFocusedPolicy, FixedPolicy, RandomPolicy


POLICY_NAMES = (
    "ed_pomdp_voi",
    "classical_pomdp",
    "entropy_acquisition",
    "fixed_plan",
    "random_acquisition",
    "risk_only",
    "rule_based",
)


def build_policy_matrix(
    *,
    random_seed: int,
    weights: LossWeights = LossWeights(),
):
    """Return fresh policy instances in preregistered order."""
    policies = (
        EvidenceDrivenVoIPolicy(weights=weights),
        ClassicalPOMDPPolicy(weights=weights),
        EntropyReductionPolicy(),
        FixedPolicy(),
        RandomPolicy(seed=random_seed),
        RiskOnlyPolicy(),
        FailureFocusedPolicy(),
    )
    names = tuple(policy.name for policy in policies)
    if names != POLICY_NAMES:
        raise AssertionError(f"policy registry drift: {names!r}")
    return policies
