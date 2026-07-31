from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from benchmark.analysis.analyze_step28_mechanisms import (
    CONDITIONAL_NO_GO_BOUNDARY,
    EXPECTED_PAIR_ROWS,
    GO_CONDITIONAL_BOUNDARY,
    PAIRWISE_FIELDS,
    _direction,
    _nearest_boundary_distance,
    generate,
    sha256_path,
)


RAW_SHA256 = "6695ab664fb67ec1eeb60669273aadf6a355a4fcdb45994f3870f638775dd070"
DIRECTIONALITY_SHA256 = (
    "fdad023ffb2ab82a65ec6b8f2cd962b0e0e3421192e4e30e399bed31c82c1339"
)


def test_frozen_decision_boundaries() -> None:
    assert GO_CONDITIONAL_BOUNDARY == pytest.approx(1.0 / 13.0)
    assert CONDITIONAL_NO_GO_BOUNDARY == pytest.approx(3.0 / 11.0)
    assert _nearest_boundary_distance(GO_CONDITIONAL_BOUNDARY) == pytest.approx(0.0)
    assert _nearest_boundary_distance(CONDITIONAL_NO_GO_BOUNDARY) == pytest.approx(0.0)


def test_direction_uses_lower_is_better() -> None:
    assert _direction(-1.0) == "favorable"
    assert _direction(1.0) == "adverse"
    assert _direction(0.0) == "equal"
    assert _direction(1e-13) == "equal"


def test_step28_generation_is_complete_and_deterministic(tmp_path: Path) -> None:
    raw = Path("benchmark/results/headline_raw.csv")
    directionality = Path("benchmark/results/step27_posthoc_directionality.csv")
    assert sha256_path(raw) == RAW_SHA256
    assert sha256_path(directionality) == DIRECTIONALITY_SHA256

    output_dir = tmp_path / "step28"
    metadata = generate(
        raw_path=raw,
        directionality_path=directionality,
        output_dir=output_dir,
    )

    assert metadata["analysis_role"] == "post_hoc_descriptive"
    assert metadata["inferential_status"] == "descriptive_post_hoc_no_new_tests"
    assert metadata["counts"]["pairwise_rows"] == EXPECTED_PAIR_ROWS
    assert metadata["counts"]["summary_rows"] == 125
    assert metadata["counts"]["threshold_rows"] == 112
    assert metadata["counts"]["transition_rows"] > 0
    assert metadata["counts"]["acquisition_rows"] > 0

    pairwise = output_dir / "step28_pairwise_diagnostics.csv"
    with pairwise.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = tuple(reader)
        assert tuple(reader.fieldnames or ()) == PAIRWISE_FIELDS
    assert len(rows) == EXPECTED_PAIR_ROWS
    assert {row["baseline"] for row in rows} == {
        "fixed_plan",
        "random_acquisition",
        "entropy_acquisition",
        "risk_only",
        "classical_pomdp",
    }

    report = (output_dir / "STEP_2_8_CLAIM_ADJUDICATION.md").read_text(
        encoding="utf-8"
    )
    assert "NOT SUPPORTED IN THE FROZEN STEP 2 BENCHMARK" in report
    assert "mandatory descriptive safety evidence" in report.lower()
    assert "was not tested for superiority" in report.lower()
    assert "zero discrepancies" not in report.lower()  # independent review is recorded elsewhere

    first_hashes = {
        name: details["sha256"]
        for name, details in metadata["outputs"].items()
    }
    metadata_again = generate(
        raw_path=raw,
        directionality_path=directionality,
        output_dir=output_dir,
        overwrite=True,
    )
    second_hashes = {
        name: details["sha256"]
        for name, details in metadata_again["outputs"].items()
    }
    assert first_hashes == second_hashes

    persisted = json.loads(
        (output_dir / "step28_analysis_metadata.json").read_text(encoding="utf-8")
    )
    assert persisted["inputs"][str(raw)] == RAW_SHA256
    assert persisted["inputs"][str(directionality)] == DIRECTIONALITY_SHA256
