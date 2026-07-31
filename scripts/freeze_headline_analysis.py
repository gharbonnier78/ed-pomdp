"""Create the Step 2 frozen-artifact lock and final analysis manifest.

Scientific sequence:
1. Commit all candidate code/configuration.
2. Run ``lock`` and commit ``benchmark/config/FROZEN_ARTIFACTS.json``.
3. Run ``manifest`` and commit ``benchmark/protocol/ANALYSIS_FREEZE.json``.
4. Only then may ``benchmark.experiment.run_headline`` generate raw results.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import platform
import subprocess
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from benchmark.experiment.freeze_guard import sha256_path
from benchmark.experiment.harness import load_headline_config


LOCK_PATH = Path("benchmark/config/FROZEN_ARTIFACTS.json")
MANIFEST_PATH = Path("benchmark/protocol/ANALYSIS_FREEZE.json")
RAW_RESULTS_PATH = Path("benchmark/results/headline_raw.csv")
EXPECTED_PYTHON_VERSION = "3.12.13"

FROZEN_ARTIFACTS = (
    "benchmark/config/headline_matrix.json",
    "benchmark/METRICS.md",
    "benchmark/protocol/PREREGISTRATION.md",
    "benchmark/runtime/evidence_model.py",
    "benchmark/runtime/simulator.py",
    "benchmark/runtime/decision.py",
    "benchmark/runtime/policies.py",
    "benchmark/runtime/baseline_policies.py",
    "benchmark/runtime/ed_pomdp_policy.py",
    "benchmark/runtime/policy_matrix.py",
    "benchmark/experiment/harness.py",
    "benchmark/experiment/freeze_guard.py",
    "benchmark/experiment/run_headline.py",
    "benchmark/analysis/metrics.py",
    "benchmark/analysis/analyze_headline.py",
    "scripts/freeze_headline_analysis.py",
)


def _git(*arguments: str) -> str:
    return subprocess.run(
        ("git", *arguments),
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _require_clean_tree() -> None:
    if _git("status", "--porcelain"):
        raise RuntimeError("freeze generation requires a clean working tree")


def _require_no_headline_results() -> None:
    if (REPO_ROOT / RAW_RESULTS_PATH).exists():
        raise RuntimeError("headline raw results already exist; freeze must precede execution")


def _require_frozen_python() -> None:
    actual = platform.python_version()
    if actual != EXPECTED_PYTHON_VERSION:
        raise RuntimeError(
            f"freeze generation requires Python {EXPECTED_PYTHON_VERSION}; found {actual}"
        )


def create_lock() -> None:
    _require_clean_tree()
    _require_no_headline_results()
    _require_frozen_python()
    lock_path = REPO_ROOT / LOCK_PATH
    manifest_path = REPO_ROOT / MANIFEST_PATH
    if lock_path.exists() or manifest_path.exists():
        raise RuntimeError("remove stale freeze artifacts before creating a new lock")
    config = load_headline_config(REPO_ROOT / "benchmark/config/headline_matrix.json")
    if config.get("status") != "frozen":
        raise RuntimeError("headline config must be marked frozen before lock generation")
    missing = [path for path in FROZEN_ARTIFACTS if not (REPO_ROOT / path).is_file()]
    if missing:
        raise RuntimeError(f"frozen artifact inventory is incomplete: {missing!r}")
    source_commit = _git("rev-parse", "HEAD")
    lock = {
        "schema_version": "0.2.0",
        "status": "frozen_artifact_lock",
        "source_commit": source_commit,
        "python": {
            "exact_version": EXPECTED_PYTHON_VERSION,
            "analysis_runtime_dependencies": [],
            "test_only_dependencies": ["pytest==9.1.1"],
        },
        "artifacts": {
            path: sha256_path(REPO_ROOT / path) for path in sorted(FROZEN_ARTIFACTS)
        },
    }
    lock_path.write_text(
        json.dumps(lock, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"wrote {LOCK_PATH}; commit it before creating the manifest")


def create_manifest() -> None:
    _require_clean_tree()
    _require_no_headline_results()
    _require_frozen_python()
    lock_path = REPO_ROOT / LOCK_PATH
    manifest_path = REPO_ROOT / MANIFEST_PATH
    if not lock_path.is_file():
        raise RuntimeError("frozen-artifact lock is absent")
    if manifest_path.exists():
        raise RuntimeError("analysis-freeze manifest already exists")
    _git("ls-files", "--error-unmatch", str(LOCK_PATH))

    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    artifacts = lock.get("artifacts")
    if not isinstance(artifacts, dict) or not artifacts:
        raise RuntimeError("invalid frozen-artifact lock")
    if lock.get("python", {}).get("exact_version") != EXPECTED_PYTHON_VERSION:
        raise RuntimeError("frozen-artifact lock has the wrong Python version")
    for path, expected_hash in artifacts.items():
        if sha256_path(REPO_ROOT / path) != expected_hash:
            raise RuntimeError(f"artifact changed after lock creation: {path}")

    config_path = Path("benchmark/config/headline_matrix.json")
    config = load_headline_config(REPO_ROOT / config_path)
    if config.get("status") != "frozen":
        raise RuntimeError("headline config is not frozen")
    frozen_artifact_commit = _git("rev-parse", "HEAD")
    manifest = {
        "schema_version": "0.2.0",
        "status": "frozen",
        "created_date": "2026-07-31",
        "frozen_artifact_commit": frozen_artifact_commit,
        "lock_file": str(LOCK_PATH),
        "lock_sha256": sha256_path(lock_path),
        "python_exact_version": EXPECTED_PYTHON_VERSION,
        "runner_entrypoint": {
            "path": "benchmark/experiment/run_headline.py",
            "sha256": sha256_path(REPO_ROOT / "benchmark/experiment/run_headline.py"),
        },
        "analysis_entrypoint": {
            "path": "benchmark/analysis/analyze_headline.py",
            "sha256": sha256_path(REPO_ROOT / "benchmark/analysis/analyze_headline.py"),
        },
        "headline_config": str(config_path),
        "headline_config_sha256": sha256_path(REPO_ROOT / config_path),
        "headline_dimensions": {
            "regimes": config["regimes"],
            "budgets": config["budgets"],
            "seeds": config["seeds"],
            "policies": config["policies"],
        },
        "loss_weights": config["loss_weights"],
        "randomness": config["randomness"],
        "multiplicity": config["analysis"]["multiplicity"],
        "raw_results_absent_at_freeze": True,
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"wrote {MANIFEST_PATH}; commit it before headline execution")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("lock", "manifest"))
    arguments = parser.parse_args()
    if arguments.mode == "lock":
        create_lock()
    else:
        create_manifest()


if __name__ == "__main__":
    main()
