"""Hash and Git-state guard for preregistered headline execution."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
from typing import Mapping, Sequence


def sha256_path(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _run_git(repo_root: Path, *arguments: str) -> str:
    completed = subprocess.run(
        ("git", *arguments),
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


def _dirty_paths(status: str) -> set[str]:
    paths: set[str] = set()
    for line in status.splitlines():
        if len(line) < 4:
            continue
        path = line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        paths.add(path.strip('"'))
    return paths


def verify_analysis_freeze(
    manifest_path: str | Path,
    *,
    repo_root: str | Path = ".",
    require_git: bool = True,
    allowed_dirty_paths: Sequence[str | Path] = (),
) -> dict[str, object]:
    """Verify manifest, lock inventory, loss weights and controlled Git state.

    Headline generation supplies no allowed dirty paths. Analysis may allow only
    the raw table and its metadata, whose hashes are checked independently by
    the analysis entry point.
    """
    root = Path(repo_root).resolve()
    manifest_file = (root / manifest_path).resolve()
    if not manifest_file.is_file():
        raise RuntimeError(
            "headline execution refused: committed analysis-freeze manifest is absent"
        )
    manifest = _load_json(manifest_file)
    if manifest.get("status") != "frozen":
        raise RuntimeError("headline execution refused: manifest status is not frozen")

    lock_relative = manifest.get("lock_file")
    if not isinstance(lock_relative, str):
        raise RuntimeError("analysis-freeze manifest does not identify a lock file")
    lock_file = root / lock_relative
    if not lock_file.is_file():
        raise RuntimeError("analysis-freeze lock file is absent")
    if sha256_path(lock_file) != manifest.get("lock_sha256"):
        raise RuntimeError("analysis-freeze lock hash mismatch")
    lock = _load_json(lock_file)

    artifacts = lock.get("artifacts")
    if not isinstance(artifacts, Mapping) or not artifacts:
        raise RuntimeError("analysis-freeze lock contains no artifact inventory")
    for relative_path, expected_hash in artifacts.items():
        if not isinstance(relative_path, str) or not isinstance(expected_hash, str):
            raise RuntimeError("invalid artifact inventory entry")
        artifact = root / relative_path
        if not artifact.is_file():
            raise RuntimeError(f"frozen artifact is absent: {relative_path}")
        actual_hash = sha256_path(artifact)
        if actual_hash != expected_hash:
            raise RuntimeError(f"frozen artifact hash mismatch: {relative_path}")

    config_relative = manifest.get("headline_config")
    if not isinstance(config_relative, str):
        raise RuntimeError("manifest does not identify the headline config")
    config = _load_json(root / config_relative)
    if config.get("status") != "frozen":
        raise RuntimeError("headline config status is not frozen")
    if config.get("loss_weights") != manifest.get("loss_weights"):
        raise RuntimeError("LossWeights differ between config and freeze manifest")

    dimensions = manifest.get("headline_dimensions")
    if not isinstance(dimensions, Mapping):
        raise RuntimeError("manifest does not freeze headline dimensions")
    expected_dimensions = {
        "regimes": config.get("regimes"),
        "budgets": config.get("budgets"),
        "seeds": config.get("seeds"),
        "policies": config.get("policies"),
    }
    if dict(dimensions) != expected_dimensions:
        raise RuntimeError("headline dimensions differ from freeze manifest")

    if require_git:
        try:
            tracked = _run_git(
                root,
                "ls-files",
                "--error-unmatch",
                str(manifest_file.relative_to(root)),
            )
        except (subprocess.CalledProcessError, FileNotFoundError) as error:
            raise RuntimeError("analysis-freeze manifest is not committed") from error
        if not tracked:
            raise RuntimeError("analysis-freeze manifest is not tracked")

        status = _run_git(root, "status", "--porcelain", "--untracked-files=all")
        actual_dirty = _dirty_paths(status)
        allowed = {Path(path).as_posix() for path in allowed_dirty_paths}
        unexpected = actual_dirty - allowed
        if unexpected:
            raise RuntimeError(
                "headline execution refused: unexpected dirty paths: "
                + ", ".join(sorted(unexpected))
            )

        frozen_commit = manifest.get("frozen_artifact_commit")
        if not isinstance(frozen_commit, str) or len(frozen_commit) < 7:
            raise RuntimeError("manifest does not publish a frozen artifact commit")
        try:
            _run_git(root, "merge-base", "--is-ancestor", frozen_commit, "HEAD")
        except subprocess.CalledProcessError as error:
            raise RuntimeError(
                "current HEAD does not descend from the frozen artifact commit"
            ) from error

    return manifest
