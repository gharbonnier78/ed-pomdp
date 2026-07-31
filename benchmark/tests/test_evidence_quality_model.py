from benchmark.runtime.evidence_model import (
    EvidenceModel,
    IDENTIFIABLE_AGENT_MODEL,
    MISSPECIFIED_TRUE_MODEL,
)
from benchmark.runtime.simulator import Regime, SyntheticReleaseEnvironment


def test_evidence_model_rejects_invalid_probabilities() -> None:
    try:
        EvidenceModel(degraded_functional_fail=1.1)
    except ValueError as error:
        assert "degraded_functional_fail" in str(error)
    else:
        raise AssertionError("invalid evidence probabilities must be rejected")


def test_bad_evidence_erases_functional_state_separation() -> None:
    good_system = IDENTIFIABLE_AGENT_MODEL.failure_probability(
        "functional", (False, True)
    )
    bad_system = IDENTIFIABLE_AGENT_MODEL.failure_probability(
        "functional", (True, True)
    )
    assert good_system == bad_system == 0.60


def test_good_evidence_makes_functional_channel_discriminative() -> None:
    good_system = IDENTIFIABLE_AGENT_MODEL.failure_probability(
        "functional", (False, False)
    )
    bad_system = IDENTIFIABLE_AGENT_MODEL.failure_probability(
        "functional", (True, False)
    )
    assert good_system == 0.10
    assert bad_system == 0.95
    assert bad_system - good_system == 0.85


def test_misspecified_true_model_is_not_the_agent_model() -> None:
    state = (True, True)
    assert MISSPECIFIED_TRUE_MODEL.failure_probability(
        "functional", state
    ) != IDENTIFIABLE_AGENT_MODEL.failure_probability("functional", state)
    assert MISSPECIFIED_TRUE_MODEL.failure_probability(
        "environment_validation", state
    ) != IDENTIFIABLE_AGENT_MODEL.failure_probability(
        "environment_validation", state
    )


def _observed_failure_rate(regime: Regime, channel: str, seeds: int = 1000) -> float:
    failures = 0
    for seed in range(seeds):
        environment = SyntheticReleaseEnvironment(regime=regime, seed=seed)
        failures += int(environment.acquire(channel).failed)
    return failures / seeds


def test_degraded_and_misspecified_regimes_are_observably_distinct() -> None:
    nominal_environment = _observed_failure_rate(
        Regime.IDENTIFIABLE, "environment_validation"
    )
    degraded_environment = _observed_failure_rate(
        Regime.EVIDENCE_DEGRADED, "environment_validation"
    )
    nominal_functional = _observed_failure_rate(Regime.IDENTIFIABLE, "functional")
    misspecified_functional = _observed_failure_rate(
        Regime.LIKELIHOOD_MISSPECIFIED, "functional"
    )
    assert degraded_environment - nominal_environment > 0.15
    assert misspecified_functional - nominal_functional > 0.02
