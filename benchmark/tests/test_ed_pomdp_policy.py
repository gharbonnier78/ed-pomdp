from benchmark.runtime.decision import LossWeights
from benchmark.runtime.ed_pomdp_policy import (
    EvidenceDrivenVoIPolicy,
    expected_one_step_loss,
    joint_posterior,
    marginal_evidence_bad,
    marginal_system_bad,
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


def test_functional_failure_updates_system_not_evidence_quality() -> None:
    belief = joint_posterior((Observation(channel="functional", failed=True),))
    assert abs(marginal_system_bad(belief) - 0.8) < 1e-12
    assert abs(marginal_evidence_bad(belief) - 0.5) < 1e-12


def test_environment_failure_updates_evidence_quality_not_system() -> None:
    belief = joint_posterior((Observation(channel="environment_validation", failed=True),))
    assert abs(marginal_system_bad(belief) - 0.5) < 1e-12
    assert abs(marginal_evidence_bad(belief) - 0.8) < 1e-12


def test_voi_prefers_channel_that_can_reduce_current_decision_risk() -> None:
    history = ()
    functional = expected_one_step_loss(history, "functional")
    environment = expected_one_step_loss(history, "environment_validation")
    assert functional < environment
    assert EvidenceDrivenVoIPolicy().choose(
        history, ("functional", "environment_validation")
    ) == "functional"


def test_policy_interface_contains_no_true_latent_state_or_regime() -> None:
    policy = EvidenceDrivenVoIPolicy(weights=LossWeights())
    assert policy.choose((), ("functional", "environment_validation")) in {
        "functional",
        "environment_validation",
    }
