from benchmark.runtime.policies import FixedPolicy, RandomPolicy
from benchmark.runtime.runner import run_episode, validate_matched_records
from benchmark.runtime.simulator import Regime


def test_episode_is_seed_stable() -> None:
    first = run_episode(seed=7, regime=Regime.IDENTIFIABLE, policy=FixedPolicy(), budget=4)
    second = run_episode(seed=7, regime=Regime.IDENTIFIABLE, policy=FixedPolicy(), budget=4)
    assert first == second


def test_matched_budget_invariant() -> None:
    records = [
        run_episode(seed=11, regime=Regime.IDENTIFIABLE, policy=FixedPolicy(), budget=6),
        run_episode(seed=11, regime=Regime.IDENTIFIABLE, policy=RandomPolicy(seed=99), budget=6),
    ]
    validate_matched_records(records)
    assert {record.spent for record in records} == {6.0}
    assert {record.acquisitions for record in records} == {6}


def test_public_policy_inputs_do_not_include_latent_state() -> None:
    policy = FixedPolicy()
    assert policy.choose((), ("functional", "environment_validation")) == "functional"
    # The public choice contract contains history and channels only; no latent S/E.
    assert "true_system_bad" not in policy.choose.__annotations__
    assert "true_evidence_bad" not in policy.choose.__annotations__
