import copy
from pathlib import Path

from benchmark.experiment.harness import (
    derive_policy_seed,
    load_headline_config,
    loss_weights_from_config,
    run_experiment_cell,
    validate_headline_config,
)
from benchmark.runtime.decision import LossWeights
from benchmark.runtime.simulator import Regime, SyntheticReleaseEnvironment


CONFIG_PATH = Path("benchmark/config/headline_matrix.json")


def test_same_seed_replays_same_latents_and_noise_tape() -> None:
    first = SyntheticReleaseEnvironment(Regime.IDENTIFIABLE, seed=19)
    second = SyntheticReleaseEnvironment(Regime.IDENTIFIABLE, seed=19)
    channels = ("functional", "environment_validation", "functional")
    first_observations = tuple(first.acquire(channel) for channel in channels)
    second_observations = tuple(second.acquire(channel) for channel in channels)
    assert first_observations == second_observations
    assert first.finish() == second.finish()


def test_headline_cell_pairs_all_policies_on_same_latent_scenario() -> None:
    records = run_experiment_cell(
        regime=Regime.EVIDENCE_DEGRADED,
        budget=4,
        seed=7,
        weights=LossWeights(),
    )
    assert len(records) == 7
    assert len({(record.true_system_bad, record.true_evidence_bad) for record in records}) == 1
    assert {record.acquisition_count for record in records} == {4}
    assert {record.evidence_cost for record in records} == {4.0}


def test_fresh_policy_instances_make_cell_replay_seed_stable() -> None:
    first = run_experiment_cell(
        regime=Regime.IDENTIFIABLE,
        budget=8,
        seed=11,
        weights=LossWeights(),
    )
    second = run_experiment_cell(
        regime=Regime.IDENTIFIABLE,
        budget=8,
        seed=11,
        weights=LossWeights(),
    )
    assert first == second


def test_policy_rng_is_distinct_and_stably_derived() -> None:
    random_seed = derive_policy_seed(5, "random_acquisition")
    environment_namespace_seed = derive_policy_seed(5, "environment")
    assert random_seed == derive_policy_seed(5, "random_acquisition")
    assert random_seed != environment_namespace_seed


def test_loss_weights_are_explicit_and_loaded_from_frozen_axis() -> None:
    config = load_headline_config(CONFIG_PATH)
    assert loss_weights_from_config(config) == LossWeights(
        unsafe_go=10.0,
        unnecessary_no_go=2.0,
        conditional_bad=4.0,
        conditional_good=0.5,
        evidence_cost=0.1,
    )


def test_headline_config_rejects_early_stopping() -> None:
    config = load_headline_config(CONFIG_PATH)
    invalid = copy.deepcopy(config)
    invalid["matched_budget"]["allow_early_stopping"] = True
    try:
        validate_headline_config(invalid)
    except ValueError as error:
        assert "early stopping" in str(error)
    else:
        raise AssertionError("headline config must reject early stopping")


def test_expected_headline_row_count_is_frozen() -> None:
    config = load_headline_config(CONFIG_PATH)
    assert config["expected_episode_rows"] == 3360
