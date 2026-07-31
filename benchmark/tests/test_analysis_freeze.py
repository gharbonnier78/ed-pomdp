import copy
from dataclasses import asdict
import json
from pathlib import Path
import platform

from benchmark.analysis.analyze_headline import analyze_records
from benchmark.analysis.metrics import (
    calibration_resolution,
    expected_calibration_error,
    holm_step_down,
    metric_summary,
    pair_policy_records,
    paired_contrast,
)
from benchmark.experiment.freeze_guard import sha256_path, verify_analysis_freeze
from benchmark.experiment.harness import iter_headline_records, load_headline_config


def _record(seed: int, policy: str, probability: float, loss: float) -> dict[str, object]:
    outcome = seed % 2 == 1
    return {
        "regime": "identifiable",
        "budget": 2,
        "seed": seed,
        "policy": policy,
        "true_system_bad": outcome,
        "true_evidence_bad": False,
        "posterior_bad": probability,
        "decision_loss": loss,
        "unsafe_go": 0,
        "brier_score": (probability - float(outcome)) ** 2,
    }


def test_ece_uses_frozen_fixed_bins() -> None:
    value = expected_calibration_error(
        [0.1, 0.9], [False, True], [0.0, 0.5, 1.0]
    )
    assert abs(value - 0.1) < 1e-12


def test_ece_resolution_diagnostics_report_sparse_support() -> None:
    resolution = calibration_resolution(
        [0.1, 0.1, 0.9], [0.0, 0.5, 1.0]
    )
    assert resolution == {
        "distinct_prediction_count": 2,
        "populated_bin_count": 2,
        "total_bin_count": 2,
    }


def test_metric_summary_uses_consistent_bootstrap_column_semantics() -> None:
    records = [
        _record(0, "ed_pomdp_voi", 0.1, 0.5),
        _record(1, "ed_pomdp_voi", 0.8, 1.0),
    ]
    loss = metric_summary(
        records,
        endpoint="decision_loss",
        bin_edges=[0.0, 0.5, 1.0],
        confidence_level=0.95,
        bootstrap_resamples=20,
        analysis_seed=17,
        summary_key="loss",
    )
    ece = metric_summary(
        records,
        endpoint="expected_calibration_error",
        bin_edges=[0.0, 0.5, 1.0],
        confidence_level=0.95,
        bootstrap_resamples=20,
        analysis_seed=17,
        summary_key="ece",
    )
    for summary in (loss, ece):
        assert "estimate" in summary
        assert "bootstrap_median" in summary
        assert "bootstrap_standard_deviation" in summary
        assert "median" not in summary
        assert "standard_deviation" not in summary
    assert loss["distinct_prediction_count"] is None
    assert ece["distinct_prediction_count"] == 2


def test_paired_contrast_is_deterministic_for_same_analysis_seed() -> None:
    ed = [
        _record(0, "ed_pomdp_voi", 0.1, 0.5),
        _record(1, "ed_pomdp_voi", 0.8, 1.0),
    ]
    baseline = [
        _record(0, "fixed_plan", 0.3, 1.0),
        _record(1, "fixed_plan", 0.6, 2.0),
    ]
    pairs = pair_policy_records(ed, baseline)
    first = paired_contrast(
        pairs,
        endpoint="decision_loss",
        bin_edges=[0.0, 0.5, 1.0],
        confidence_level=0.95,
        bootstrap_resamples=100,
        permutation_resamples=100,
        analysis_seed=17,
        contrast_key="test",
    )
    second = paired_contrast(
        pairs,
        endpoint="decision_loss",
        bin_edges=[0.0, 0.5, 1.0],
        confidence_level=0.95,
        bootstrap_resamples=100,
        permutation_resamples=100,
        analysis_seed=17,
        contrast_key="test",
    )
    assert first == second
    assert first["difference_ed_minus_baseline"] < 0.0


def test_unsafe_go_cannot_enter_confirmatory_contrast_function() -> None:
    ed = [
        _record(0, "ed_pomdp_voi", 0.1, 0.5),
        _record(1, "ed_pomdp_voi", 0.8, 1.0),
    ]
    baseline = [
        _record(0, "fixed_plan", 0.3, 1.0),
        _record(1, "fixed_plan", 0.6, 2.0),
    ]
    pairs = pair_policy_records(ed, baseline)
    try:
        paired_contrast(
            pairs,
            endpoint="unsafe_go_rate",
            bin_edges=[0.0, 0.5, 1.0],
            confidence_level=0.95,
            bootstrap_resamples=10,
            permutation_resamples=10,
            analysis_seed=17,
            contrast_key="unsafe",
        )
    except ValueError as error:
        assert "not in the frozen confirmatory family" in str(error)
    else:
        raise AssertionError("unsafe GO must remain descriptive safety reporting")


def test_holm_step_down_controls_complete_family() -> None:
    corrected = holm_step_down([0.001, 0.02, 0.06], alpha=0.05)
    assert corrected[0]["reject_holm"] is True
    assert corrected[1]["reject_holm"] is True
    assert corrected[2]["reject_holm"] is False
    assert corrected[0]["adjusted_p_value"] <= corrected[1]["adjusted_p_value"]


def test_reduced_matrix_runs_end_to_end_through_holm() -> None:
    config = copy.deepcopy(
        load_headline_config("benchmark/config/headline_matrix.json")
    )
    config["regimes"] = ["identifiable"]
    config["budgets"] = [2]
    config["seeds"] = list(range(30))
    config["expected_episode_rows"] = 30 * 7
    config["analysis"]["bootstrap_resamples"] = 25
    config["analysis"]["permutation_resamples"] = 25
    config["analysis"]["multiplicity"]["expected_family_size"] = 5 * 3

    records = [asdict(record) for record in iter_headline_records(config)]
    summaries, contrasts = analyze_records(records, config)

    assert len(records) == 210
    assert len(summaries) == 7 * 4
    assert len(contrasts) == 5 * 3
    assert {row["seed_count"] for row in contrasts} == {30}
    assert {row["endpoint"] for row in contrasts} == {
        "decision_loss",
        "brier_score",
        "expected_calibration_error",
    }
    safety_rows = [row for row in summaries if row["endpoint"] == "unsafe_go_rate"]
    assert len(safety_rows) == 7
    assert {row["inference_role"] for row in safety_rows} == {
        "mandatory_safety_descriptive"
    }
    assert all(0.0 <= row["adjusted_p_value"] <= 1.0 for row in contrasts)


def test_freeze_guard_rejects_missing_manifest(tmp_path: Path) -> None:
    try:
        verify_analysis_freeze(
            "benchmark/protocol/ANALYSIS_FREEZE.json",
            repo_root=tmp_path,
            require_git=False,
        )
    except RuntimeError as error:
        assert "manifest is absent" in str(error)
    else:
        raise AssertionError("headline execution must refuse a missing manifest")


def _write_guard_fixture(tmp_path: Path) -> tuple[dict[str, object], Path, Path]:
    artifact = tmp_path / "benchmark/analysis/entry.py"
    artifact.parent.mkdir(parents=True)
    artifact.write_text("print('frozen')\n", encoding="utf-8")

    multiplicity = {
        "method": "holm_step_down",
        "alpha": 0.05,
        "expected_family_size": 3,
    }
    calibration = {"bin_edges": [0.0, 0.5, 1.0]}
    config: dict[str, object] = {
        "status": "frozen",
        "regimes": ["identifiable"],
        "budgets": [2],
        "seeds": list(range(30)),
        "policies": ["ed_pomdp_voi"],
        "confirmatory_metrics": [
            "decision_loss",
            "brier_score",
            "expected_calibration_error",
        ],
        "mandatory_safety_metrics": ["unsafe_go_rate"],
        "calibration": calibration,
        "analysis": {"multiplicity": multiplicity},
        "loss_weights": {
            "unsafe_go": 10.0,
            "unnecessary_no_go": 2.0,
            "conditional_bad": 4.0,
            "conditional_good": 0.5,
            "evidence_cost": 0.1,
        },
    }
    config_path = tmp_path / "benchmark/config/headline_matrix.json"
    config_path.parent.mkdir(parents=True)
    config_path.write_text(json.dumps(config), encoding="utf-8")

    lock = {
        "python": {"exact_version": platform.python_version()},
        "artifacts": {
            "benchmark/analysis/entry.py": sha256_path(artifact),
            "benchmark/config/headline_matrix.json": sha256_path(config_path),
        },
    }
    lock_path = tmp_path / "benchmark/config/FROZEN_ARTIFACTS.json"
    lock_path.write_text(json.dumps(lock), encoding="utf-8")

    manifest = {
        "status": "frozen",
        "lock_file": "benchmark/config/FROZEN_ARTIFACTS.json",
        "lock_sha256": sha256_path(lock_path),
        "python_exact_version": platform.python_version(),
        "headline_config": "benchmark/config/headline_matrix.json",
        "loss_weights": config["loss_weights"],
        "confirmatory_metrics": config["confirmatory_metrics"],
        "mandatory_safety_metrics": config["mandatory_safety_metrics"],
        "calibration": calibration,
        "multiplicity": multiplicity,
        "headline_dimensions": {
            "regimes": config["regimes"],
            "budgets": config["budgets"],
            "seeds": config["seeds"],
            "policies": config["policies"],
        },
        "frozen_artifact_commit": "1234567",
    }
    manifest_path = tmp_path / "benchmark/protocol/ANALYSIS_FREEZE.json"
    manifest_path.parent.mkdir(parents=True)
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return config, config_path, manifest_path


def _rehash_config_and_lock(config_path: Path, manifest_path: Path) -> None:
    lock_path = config_path.parent / "FROZEN_ARTIFACTS.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    lock["artifacts"]["benchmark/config/headline_matrix.json"] = sha256_path(
        config_path
    )
    lock_path.write_text(json.dumps(lock), encoding="utf-8")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["lock_sha256"] = sha256_path(lock_path)
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")


def test_freeze_guard_checks_artifacts_dimensions_and_loss_weights(tmp_path: Path) -> None:
    config, config_path, _ = _write_guard_fixture(tmp_path)
    assert verify_analysis_freeze(
        "benchmark/protocol/ANALYSIS_FREEZE.json",
        repo_root=tmp_path,
        require_git=False,
    )["status"] == "frozen"

    config["loss_weights"]["unsafe_go"] = 9.0
    config_path.write_text(json.dumps(config), encoding="utf-8")
    try:
        verify_analysis_freeze(
            "benchmark/protocol/ANALYSIS_FREEZE.json",
            repo_root=tmp_path,
            require_git=False,
        )
    except RuntimeError as error:
        assert "hash mismatch" in str(error)
    else:
        raise AssertionError("changed LossWeights/config must invalidate the freeze")


def test_freeze_guard_checks_endpoint_registry_even_with_rehashed_config(
    tmp_path: Path,
) -> None:
    config, config_path, manifest_path = _write_guard_fixture(tmp_path)
    config["confirmatory_metrics"] = ["decision_loss", "unsafe_go_rate"]
    config_path.write_text(json.dumps(config), encoding="utf-8")
    _rehash_config_and_lock(config_path, manifest_path)

    try:
        verify_analysis_freeze(
            "benchmark/protocol/ANALYSIS_FREEZE.json",
            repo_root=tmp_path,
            require_git=False,
        )
    except RuntimeError as error:
        assert "confirmatory metrics differ" in str(error)
    else:
        raise AssertionError("manifest must reject endpoint-registry drift")


def test_freeze_guard_checks_calibration_even_with_rehashed_config(
    tmp_path: Path,
) -> None:
    config, config_path, manifest_path = _write_guard_fixture(tmp_path)
    config["calibration"] = {"bin_edges": [0.0, 0.25, 0.5, 0.75, 1.0]}
    config_path.write_text(json.dumps(config), encoding="utf-8")
    _rehash_config_and_lock(config_path, manifest_path)

    try:
        verify_analysis_freeze(
            "benchmark/protocol/ANALYSIS_FREEZE.json",
            repo_root=tmp_path,
            require_git=False,
        )
    except RuntimeError as error:
        assert "calibration semantics differ" in str(error)
    else:
        raise AssertionError("manifest must reject ECE-bin drift")
