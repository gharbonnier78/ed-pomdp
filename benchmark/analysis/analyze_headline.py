"""Frozen analysis entry point for the Step 2 confirmatory headline matrix."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Mapping, Sequence

from benchmark.analysis.metrics import (
    PRIMARY_ENDPOINTS,
    group_records,
    holm_step_down,
    metric_summary,
    pair_policy_records,
    paired_contrast,
    read_raw_csv,
)
from benchmark.experiment.freeze_guard import verify_analysis_freeze
from benchmark.experiment.harness import load_headline_config


def validate_raw_matrix(
    records: Sequence[Mapping[str, object]], config: Mapping[str, object]
) -> None:
    regimes = tuple(str(value) for value in config["regimes"])
    budgets = tuple(int(value) for value in config["budgets"])
    seeds = tuple(int(value) for value in config["seeds"])
    policies = tuple(str(value) for value in config["policies"])
    expected_rows = int(config["expected_episode_rows"])
    if len(records) != expected_rows:
        raise ValueError(f"raw matrix has {len(records)} rows; expected {expected_rows}")

    seen: set[tuple[str, int, int, str]] = set()
    for record in records:
        key = (
            str(record["regime"]),
            int(record["budget"]),
            int(record["seed"]),
            str(record["policy"]),
        )
        if key in seen:
            raise ValueError(f"duplicate raw experimental unit: {key!r}")
        seen.add(key)
        if key[0] not in regimes or key[1] not in budgets or key[2] not in seeds or key[3] not in policies:
            raise ValueError(f"raw row outside frozen matrix: {key!r}")
        if int(record["acquisition_count"]) != key[1]:
            raise ValueError("raw row violates fixed horizon")
        if float(record["evidence_cost"]) != float(key[1]):
            raise ValueError("raw row violates exact matched cost")

    expected = {
        (regime, budget, seed, policy)
        for regime in regimes
        for budget in budgets
        for seed in seeds
        for policy in policies
    }
    if seen != expected:
        raise ValueError("raw matrix is incomplete or contains unexpected cells")


def _write_csv(path: str | Path, rows: Sequence[Mapping[str, object]]) -> None:
    if not rows:
        raise ValueError("cannot write empty analysis table")
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def analyze_records(
    records: Sequence[Mapping[str, object]], config: Mapping[str, object]
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    validate_raw_matrix(records, config)
    groups = group_records(records)
    calibration = config["calibration"]
    analysis = config["analysis"]
    assert isinstance(calibration, Mapping)
    assert isinstance(analysis, Mapping)
    bin_edges = tuple(float(value) for value in calibration["bin_edges"])
    confidence_level = float(analysis["confidence_level"])
    bootstrap_resamples = int(analysis["bootstrap_resamples"])
    permutation_resamples = int(analysis["permutation_resamples"])
    analysis_seed = int(analysis["analysis_seed"])

    summary_rows: list[dict[str, object]] = []
    for regime in config["regimes"]:
        for budget in config["budgets"]:
            for policy in config["policies"]:
                group = groups[(str(regime), int(budget), str(policy))]
                for endpoint in PRIMARY_ENDPOINTS:
                    key = f"summary|{regime}|{budget}|{policy}|{endpoint}"
                    summary_rows.append(
                        {
                            "regime": regime,
                            "budget": budget,
                            "policy": policy,
                            "endpoint": endpoint,
                            **metric_summary(
                                group,
                                endpoint=endpoint,
                                bin_edges=bin_edges,
                                confidence_level=confidence_level,
                                bootstrap_resamples=bootstrap_resamples,
                                analysis_seed=analysis_seed,
                                summary_key=key,
                            ),
                        }
                    )

    contrast_rows: list[dict[str, object]] = []
    for regime in config["regimes"]:
        for budget in config["budgets"]:
            ed_group = groups[(str(regime), int(budget), "ed_pomdp_voi")]
            for baseline in config["confirmatory_baselines"]:
                baseline_group = groups[(str(regime), int(budget), str(baseline))]
                pairs = pair_policy_records(ed_group, baseline_group)
                for endpoint in PRIMARY_ENDPOINTS:
                    key = f"contrast|{regime}|{budget}|{baseline}|{endpoint}"
                    contrast_rows.append(
                        {
                            "regime": regime,
                            "budget": budget,
                            "ed_policy": "ed_pomdp_voi",
                            "baseline": baseline,
                            "endpoint": endpoint,
                            "seed_count": len(pairs),
                            **paired_contrast(
                                pairs,
                                endpoint=endpoint,
                                bin_edges=bin_edges,
                                confidence_level=confidence_level,
                                bootstrap_resamples=bootstrap_resamples,
                                permutation_resamples=permutation_resamples,
                                analysis_seed=analysis_seed,
                                contrast_key=key,
                            ),
                        }
                    )

    multiplicity = analysis["multiplicity"]
    assert isinstance(multiplicity, Mapping)
    if multiplicity.get("method") != "holm_step_down":
        raise ValueError("only frozen Holm step-down correction is permitted")
    holm = holm_step_down(
        [float(row["p_value"]) for row in contrast_rows],
        alpha=float(multiplicity["alpha"]),
    )
    for row, correction in zip(contrast_rows, holm):
        row.update(correction)

    expected_contrasts = (
        len(config["regimes"])
        * len(config["budgets"])
        * len(config["confirmatory_baselines"])
        * len(PRIMARY_ENDPOINTS)
    )
    if len(contrast_rows) != expected_contrasts:
        raise AssertionError("confirmatory family size drifted from frozen matrix")
    return summary_rows, contrast_rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", required=True)
    parser.add_argument(
        "--config", default="benchmark/config/headline_matrix.json"
    )
    parser.add_argument(
        "--manifest", default="benchmark/protocol/ANALYSIS_FREEZE.json"
    )
    parser.add_argument(
        "--summary", default="benchmark/results/headline_summary.csv"
    )
    parser.add_argument(
        "--contrasts", default="benchmark/results/headline_contrasts.csv"
    )
    arguments = parser.parse_args()

    verify_analysis_freeze(arguments.manifest)
    config = load_headline_config(arguments.config)
    records = read_raw_csv(arguments.raw)
    summary_rows, contrast_rows = analyze_records(records, config)
    _write_csv(arguments.summary, summary_rows)
    _write_csv(arguments.contrasts, contrast_rows)
    print(
        json.dumps(
            {
                "summary_rows": len(summary_rows),
                "confirmatory_contrasts": len(contrast_rows),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
