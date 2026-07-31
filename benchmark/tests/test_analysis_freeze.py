import json
from pathlib import Path

from benchmark.analysis.metrics import (
    expected_calibration_error,
    holm_step_down,
    pair_policy_records,
    paired_contrast,
)
from benchmark.experiment.freeze_guard import sha256_path, verify_analysis_freeze


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


def test_paired_contrast_is_deterministic_for_same_analysis_seed() -> None:
    ed = [_record(0, "ed_pomdp_voi", 0.1, 0.5), _record(1, "ed_pomdp_voi", 0.8, 1.0)]
    baseline = [_record(0, "fixed_plan", 0.3, 1.0), _record(1, "fixed_plan", 0.6, 2.0)]
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


def test_holm_step_down_controls_complete_family() -> None:
    corrected = holm_step_down([0.001, 0.02, 0.04], alpha=0.05)
    assert corrected[0]["reject_holm"] is True
    assert corrected[1]["reject_holm"] is True
    assert corrected[2]["reject_holm"] is False
    assert corrected[0]["adjusted_p_value"] <= corrected[1]["adjusted_p_value"]


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


def test_freeze_guard_checks_artifacts_dimensions_and_loss_weights(tmp_path: Path) -> None:
    artifact = tmp_path / "benchmark/analysis/entry.py"
    artifact.parent.mkdir(parents=True)
    artifact.write_text("print('frozen')\n", encoding="utf-8")

    config = {
        "status": "frozen",
        "regimes": ["identifiable"],
        "budgets": [2],
        "seeds": list(range(30)),
        "policies": ["ed_pomdp_voi"],
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
        "artifacts": {
            "benchmark/analysis/entry.py": sha256_path(artifact),
            "benchmark/config/headline_matrix.json": sha256_path(config_path),
        }
    }
    lock_path = tmp_path / "benchmark/config/FROZEN_ARTIFACTS.json"
    lock_path.write_text(json.dumps(lock), encoding="utf-8")

    manifest = {
        "status": "frozen",
        "lock_file": "benchmark/config/FROZEN_ARTIFACTS.json",
        "lock_sha256": sha256_path(lock_path),
        "headline_config": "benchmark/config/headline_matrix.json",
        "loss_weights": config["loss_weights"],
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
