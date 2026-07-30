from benchmark.runtime.decision import (
    LossWeights,
    decide_from_posterior,
    expected_terminal_risk,
    posterior_system_bad,
)
from benchmark.runtime.ed_pomdp_policy import (
    EvidenceDrivenVoIPolicy,
    decision_value_of_information,
    expected_one_step_loss,
    joint_posterior,
    marginal_evidence_bad,
    marginal_system_bad,
    terminal_policy_risk,
)
from benchmark.runtime.simulator import Observation


def test_joint_prior_is_uniform_without_observations() -> None:
    belief = joint_posterior(())
    assert belief == {
        (False, False): 0.25,
        (False, True): 0.25,
        (True, False): 0.25,
        (True, True): 0.25,
    }
    assert marginal_system_bad(belief) == 0.5
    assert marginal_evidence_bad(belief) == 0.5


def test_functional_observation_updates_joint_belief() -> None:
    belief = joint_posterior((Observation(channel="functional", failed=False),))
    assert abs(marginal_system_bad(belief) - 0.2571428571428572) < 1e-12
    assert abs(marginal_evidence_bad(belief) - 0.4571428571428572) < 1e-12


def test_environment_only_updates_evidence_quality() -> None:
    belief = joint_posterior(
        (Observation(channel="environment_validation", failed=True),)
    )
    assert abs(marginal_system_bad(belief) - 0.5) < 1e-12
    assert abs(marginal_evidence_bad(belief) - 0.8) < 1e-12


def test_environment_recalibrates_system_after_functional_evidence() -> None:
    base = (Observation(channel="functional", failed=False),)
    environment_pass = base + (
        Observation(channel="environment_validation", failed=False),
    )
    environment_failure = base + (
        Observation(channel="environment_validation", failed=True),
    )
    assert (
        posterior_system_bad(environment_pass)
        < posterior_system_bad(base)
        < posterior_system_bad(environment_failure)
    )


def test_environment_validation_has_positive_decision_voi() -> None:
    history = (
        Observation(channel="functional", failed=False),
        Observation(channel="functional", failed=False),
    )
    assert decision_value_of_information(
        history, "environment_validation"
    ) > 0.18


def test_policy_selects_environment_when_reliability_information_is_more_valuable() -> None:
    history = (
        Observation(channel="functional", failed=False),
        Observation(channel="functional", failed=False),
    )
    environment_loss = expected_one_step_loss(history, "environment_validation")
    functional_loss = expected_one_step_loss(history, "functional")
    assert environment_loss < functional_loss
    assert EvidenceDrivenVoIPolicy().choose(
        history, ("functional", "environment_validation")
    ) == "environment_validation"


def test_voi_prefers_functional_channel_initially() -> None:
    functional = expected_one_step_loss((), "functional")
    environment = expected_one_step_loss((), "environment_validation")
    assert functional < environment
    assert EvidenceDrivenVoIPolicy().choose(
        (), ("functional", "environment_validation")
    ) == "functional"


def test_voi_terminal_risk_matches_executed_terminal_rule() -> None:
    weights = LossWeights()
    for probability_bad in (0.05, 0.10, 0.50, 0.90):
        decision = decide_from_posterior(probability_bad, weights=weights)
        expected = expected_terminal_risk(
            probability_bad, decision, weights=weights
        )
        assert terminal_policy_risk(probability_bad, weights) == expected


def test_policy_interface_contains_no_true_latent_state_or_regime() -> None:
    policy = EvidenceDrivenVoIPolicy(weights=LossWeights())
    assert policy.choose((), ("functional", "environment_validation")) in {
        "functional",
        "environment_validation",
    }
    assert "true_system_bad" not in policy.choose.__annotations__
    assert "true_evidence_bad" not in policy.choose.__annotations__
    assert "regime" not in policy.choose.__annotations__
