from benchmark.runtime.decision import (
    LossWeights,
    ReleaseDecision,
    decide_from_posterior,
    expected_terminal_risk,
    posterior_system_bad,
    score_decision,
)
from benchmark.runtime.decision_runner import run_decision_episode, validate_budget_ceiling
from benchmark.runtime.policies import FixedPolicy
from benchmark.runtime.simulator import EpisodeOutcome, Observation, Regime


def test_posterior_uses_observable_evidence_only() -> None:
    history = (
        Observation(channel="functional", failed=False),
        Observation(channel="environment_validation", failed=False),
    )
    assert abs(posterior_system_bad(history) - 0.13043478260869568) < 1e-12


def test_loss_derived_rule_produces_three_terminal_decisions() -> None:
    assert decide_from_posterior(0.05) is ReleaseDecision.GO
    assert decide_from_posterior(0.10) is ReleaseDecision.CONDITIONAL_GO
    assert decide_from_posterior(0.50) is ReleaseDecision.NO_GO


def test_terminal_rule_minimizes_configured_expected_loss() -> None:
    weights = LossWeights()
    for probability_bad in (0.0, 0.05, 0.10, 0.25, 0.50, 0.90, 1.0):
        selected = decide_from_posterior(probability_bad, weights=weights)
        selected_risk = expected_terminal_risk(
            probability_bad, selected, weights=weights
        )
        all_risks = [
            expected_terminal_risk(probability_bad, decision, weights=weights)
            for decision in ReleaseDecision
        ]
        assert selected_risk == min(all_risks)


def test_unsafe_go_has_larger_loss_than_unnecessary_no_go() -> None:
    unsafe = score_decision(
        EpisodeOutcome(observations=(), true_system_bad=True, true_evidence_bad=False),
        ReleaseDecision.GO,
    )
    conservative = score_decision(
        EpisodeOutcome(observations=(), true_system_bad=False, true_evidence_bad=False),
        ReleaseDecision.NO_GO,
    )
    assert unsafe.unsafe_go
    assert conservative.unnecessary_no_go
    assert unsafe.decision_loss > conservative.decision_loss


def test_decision_episode_respects_budget_ceiling_and_is_seed_stable() -> None:
    policy = FixedPolicy("functional")
    first = run_decision_episode(
        seed=17,
        regime=Regime.IDENTIFIABLE,
        policy=policy,
        budget=8.0,
    )
    second = run_decision_episode(
        seed=17,
        regime=Regime.IDENTIFIABLE,
        policy=policy,
        budget=8.0,
    )
    validate_budget_ceiling(first)
    assert first == second


def test_stopping_can_leave_budget_unspent() -> None:
    record = run_decision_episode(
        seed=1,
        regime=Regime.IDENTIFIABLE,
        policy=FixedPolicy("functional"),
        budget=20.0,
        minimum_acquisitions=2,
    )
    assert record.spent <= record.budget
    if record.stopped_early:
        assert record.spent < record.budget
