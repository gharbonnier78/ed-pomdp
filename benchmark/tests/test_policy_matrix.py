from benchmark.runtime.baseline_policies import (
    ClassicalPOMDPPolicy,
    EntropyReductionPolicy,
    RiskOnlyPolicy,
    classical_posterior_system_bad,
    expected_joint_entropy,
    expected_system_uncertainty,
)
from benchmark.runtime.decision_runner import run_decision_episode
from benchmark.runtime.policy_matrix import POLICY_NAMES, build_policy_matrix
from benchmark.runtime.simulator import Observation, Regime


CHANNELS = ("functional", "environment_validation")


def test_policy_registry_is_complete_and_ordered() -> None:
    policies = build_policy_matrix(random_seed=19)
    assert tuple(policy.name for policy in policies) == POLICY_NAMES
    assert len({policy.name for policy in policies}) == 7


def test_every_policy_uses_public_contract_and_available_channels() -> None:
    history = (Observation(channel="functional", failed=False),)
    for policy in build_policy_matrix(random_seed=3):
        assert policy.choose(history, CHANNELS) in CHANNELS
        assert 0.0 <= policy.posterior_bad(history) <= 1.0
        assert "true_system_bad" not in policy.choose.__annotations__
        assert "true_evidence_bad" not in policy.choose.__annotations__
        assert "regime" not in policy.choose.__annotations__


def test_entropy_baseline_targets_full_joint_belief() -> None:
    assert expected_joint_entropy((), "functional") < expected_joint_entropy(
        (), "environment_validation"
    )
    assert EntropyReductionPolicy().choose((), CHANNELS) == "functional"


def test_risk_only_targets_system_uncertainty_without_loss_weights() -> None:
    assert expected_system_uncertainty((), "functional") < expected_system_uncertainty(
        (), "environment_validation"
    )
    assert RiskOnlyPolicy().choose((), CHANNELS) == "functional"


def test_classical_model_cannot_learn_from_environment_validation() -> None:
    base = (Observation(channel="functional", failed=False),)
    environment_pass = base + (
        Observation(channel="environment_validation", failed=False),
    )
    environment_failure = base + (
        Observation(channel="environment_validation", failed=True),
    )
    probability_bad = classical_posterior_system_bad(base)
    assert (
        abs(classical_posterior_system_bad(environment_pass) - probability_bad)
        < 1e-12
    )
    assert (
        abs(classical_posterior_system_bad(environment_failure) - probability_bad)
        < 1e-12
    )


def test_classical_and_explicit_e_beliefs_diverge_after_environment_evidence() -> None:
    history = (
        Observation(channel="functional", failed=False),
        Observation(channel="environment_validation", failed=False),
    )
    classical = ClassicalPOMDPPolicy().posterior_bad(history)
    explicit = build_policy_matrix(random_seed=1)[0].posterior_bad(history)
    assert abs(classical - explicit) > 0.05


def test_decision_runner_uses_policy_specific_posterior() -> None:
    class CertainGoodPolicy:
        name = "certain_good"

        def choose(self, history, channels):
            return channels[0]

        def posterior_bad(self, history):
            return 0.01

    record = run_decision_episode(
        seed=5,
        regime=Regime.IDENTIFIABLE,
        policy=CertainGoodPolicy(),
        budget=4.0,
        minimum_acquisitions=1,
    )
    assert record.posterior_bad == 0.01
    assert record.acquisitions == 1
