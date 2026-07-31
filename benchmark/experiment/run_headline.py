"""Guarded entry point for generating Step 2 headline raw results."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess

from benchmark.experiment.freeze_guard import sha256_path, verify_analysis_freeze
from benchmark.experiment.harness import (
    iter_headline_records,
    load_headline_config,
    write_raw_csv,
)


def _git_head(repo_root: Path) -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", default="benchmark/config/headline_matrix.json"
    )
    parser.add_argument(
        "--manifest", default="benchmark/protocol/ANALYSIS_FREEZE.json"
    )
    parser.add_argument(
        "--raw", default="benchmark/results/headline_raw.csv"
    )
    parser.add_argument(
        "--metadata", default="benchmark/results/headline_run_metadata.json"
    )
    arguments = parser.parse_args()

    repo_root = Path(".").resolve()
    raw_path = repo_root / arguments.raw
    metadata_path = repo_root / arguments.metadata
    if raw_path.exists() or metadata_path.exists():
        raise RuntimeError(
            "headline execution refused: output already exists; preserve prior run"
        )

    manifest = verify_analysis_freeze(
        arguments.manifest, repo_root=repo_root, require_git=True
    )
    config = load_headline_config(repo_root / arguments.config)
    if config.get("status") != "frozen":
        raise RuntimeError("headline execution refused: config is not frozen")

    row_count = write_raw_csv(iter_headline_records(config), raw_path)
    expected_rows = int(config["expected_episode_rows"])
    if row_count != expected_rows:
        raw_path.unlink(missing_ok=True)
        raise AssertionError(
            f"headline run produced {row_count} rows; expected {expected_rows}"
        )

    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "schema_version": "0.2.0",
        "git_head": _git_head(repo_root),
        "frozen_artifact_commit": manifest["frozen_artifact_commit"],
        "manifest_path": arguments.manifest,
        "manifest_sha256": sha256_path(repo_root / arguments.manifest),
        "headline_config": arguments.config,
        "headline_config_sha256": sha256_path(repo_root / arguments.config),
        "raw_results": arguments.raw,
        "raw_results_sha256": sha256_path(raw_path),
        "row_count": row_count,
    }
    metadata_path.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(metadata, sort_keys=True))


if __name__ == "__main__":
    main()
