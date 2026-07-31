"""Frozen metric and paired-inference implementation for Step 2 headline runs."""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path
import random
from statistics import fmean, median, stdev
from typing import Iterable, Mapping, Sequence


CONFIRMATORY_ENDPOINTS = (
    "decision_loss",
    "brier_score",
    "expected_calibration_error",
)
MANDATORY_SAFETY_ENDPOINTS = ("unsafe_go_rate",)
SUMMARY_ENDPOINTS = CONFIRMATORY_ENDPOINTS + MANDATORY_SAFETY_ENDPOINTS


def read_raw_csv(path: str | Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        for raw in csv.DictReader(handle):
            records.append(
                {
                    **raw,
                    "budget": int(raw["budget"]),
                    "seed": int(raw["seed"]),
                    "true_system_bad": raw["true_system_bad"] == "True",
                    "true_evidence_bad": raw["true_evidence_bad"] == "True",
                    "posterior_bad": float(raw["posterior_bad"]),
                    "decision_loss": float(raw["decision_loss"]),
                    "unsafe_go": int(raw["unsafe_go"]),
                    "unnecessary_no_go": int(raw["unnecessary_no_go"]),
                    "brier_score": float(raw["brier_score"]),
                    "residual_risk": float(raw["residual_risk"]),
                    "evidence_cost": float(raw["evidence_cost"]),
                    "acquisition_count": int(raw["acquisition_count"]),
                }
            )
    if not records:
        raise ValueError("raw result table is empty")
    return records


def _validate_bin_edges(bin_edges: Sequence[float]) -> None:
    if len(bin_edges) < 2 or bin_edges[0] != 0.0 or bin_edges[-1] != 1.0:
        raise ValueError("ECE bin edges must span [0, 1]")
    if any(left >= right for left, right in zip(bin_edges, bin_edges[1:])):
        raise ValueError("ECE bin edges must be strictly increasing")


def _bin_index(probability: float, bin_edges: Sequence[float]) -> int:
    for index, (lower, upper) in enumerate(zip(bin_edges, bin_edges[1:])):
        if lower <= probability < upper:
            return index
        if index == len(bin_edges) - 2 and probability == upper:
            return index
    raise ValueError("probability is outside frozen calibration bins")


def calibration_resolution(
    probabilities: Sequence[float], bin_edges: Sequence[float]
) -> dict[str, int]:
    if not probabilities:
        raise ValueError("calibration resolution requires predictions")
    _validate_bin_edges(bin_edges)
    populated = {_bin_index(float(probability), bin_edges) for probability in probabilities}
    return {
        "distinct_prediction_count": len(set(float(value) for value in probabilities)),
        "populated_bin_count": len(populated),
        "total_bin_count": len(bin_edges) - 1,
    }


def expected_calibration_error(
    probabilities: Sequence[float],
    outcomes: Sequence[bool],
    bin_edges: Sequence[float],
) -> float:
    if len(probabilities) != len(outcomes) or not probabilities:
        raise ValueError("ECE requires equally sized non-empty predictions and outcomes")
    _validate_bin_edges(bin_edges)

    total = len(probabilities)
    ece = 0.0
    for index in range(len(bin_edges) - 1):
        members = [
            item
            for item, probability in enumerate(probabilities)
            if _bin_index(float(probability), bin_edges) == index
        ]
        if not members:
            continue
        confidence = fmean(float(probabilities[item]) for item in members)
        frequency = fmean(float(outcomes[item]) for item in members)
        ece += len(members) / total * abs(confidence - frequency)
    return ece


def endpoint_value(
    records: Sequence[Mapping[str, object]],
    endpoint: str,
    bin_edges: Sequence[float],
) -> float:
    if not records:
        raise ValueError("endpoint computation requires records")
    if endpoint == "decision_loss":
        return fmean(float(record["decision_loss"]) for record in records)
    if endpoint == "unsafe_go_rate":
        return fmean(float(record["unsafe_go"]) for record in records)
    if endpoint == "brier_score":
        return fmean(float(record["brier_score"]) for record in records)
    if endpoint == "expected_calibration_error":
        return expected_calibration_error(
            [float(record["posterior_bad"]) for record in records],
            [bool(record["true_system_bad"]) for record in records],
            bin_edges,
        )
    raise ValueError(f"unknown headline endpoint: {endpoint}")


def _stable_seed(base_seed: int, key: str) -> int:
    digest = hashlib.sha256(f"{base_seed}|{key}".encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


def metric_summary(
    records: Sequence[Mapping[str, object]],
    *,
    endpoint: str,
    bin_edges: Sequence[float],
    confidence_level: float,
    bootstrap_resamples: int,
    analysis_seed: int,
    summary_key: str,
) -> dict[str, float | int | None]:
    """Return one consistently labelled bootstrap summary.

    ``estimate`` is the statistic on the observed 30-seed cell. The median,
    standard deviation and interval are always properties of the deterministic
    bootstrap distribution, including for nonlinear ECE. Calibration-resolution
    diagnostics are populated only for ECE rows.
    """
    if not records:
        raise ValueError("metric summary requires records")
    if bootstrap_resamples <= 0:
        raise ValueError("bootstrap_resamples must be positive")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must be in (0, 1)")

    observed = endpoint_value(records, endpoint, bin_edges)
    rng = random.Random(_stable_seed(analysis_seed, summary_key))
    sample_count = len(records)
    bootstrap: list[float] = []
    for _ in range(bootstrap_resamples):
        sample = [records[rng.randrange(sample_count)] for _ in range(sample_count)]
        bootstrap.append(endpoint_value(sample, endpoint, bin_edges))
    bootstrap.sort()
    tail = (1.0 - confidence_level) / 2.0
    lower_index = min(int(tail * bootstrap_resamples), bootstrap_resamples - 1)
    upper_index = min(
        int((1.0 - tail) * bootstrap_resamples), bootstrap_resamples - 1
    )

    resolution: dict[str, int | None] = {
        "distinct_prediction_count": None,
        "populated_bin_count": None,
        "total_bin_count": None,
    }
    if endpoint == "expected_calibration_error":
        resolution.update(
            calibration_resolution(
                [float(record["posterior_bad"]) for record in records], bin_edges
            )
        )

    return {
        "estimate": observed,
        "bootstrap_median": median(bootstrap),
        "bootstrap_standard_deviation": stdev(bootstrap) if len(bootstrap) > 1 else 0.0,
        "ci_lower": bootstrap[lower_index],
        "ci_upper": bootstrap[upper_index],
        "seed_count": sample_count,
        **resolution,
    }


def pair_policy_records(
    ed_records: Sequence[Mapping[str, object]],
    baseline_records: Sequence[Mapping[str, object]],
) -> tuple[tuple[Mapping[str, object], Mapping[str, object]], ...]:
    ed_by_seed = {int(record["seed"]): record for record in ed_records}
    baseline_by_seed = {int(record["seed"]): record for record in baseline_records}
    if set(ed_by_seed) != set(baseline_by_seed):
        raise ValueError("paired policies must contain identical seed sets")
    pairs = tuple(
        (ed_by_seed[seed], baseline_by_seed[seed]) for seed in sorted(ed_by_seed)
    )
    for ed_record, baseline_record in pairs:
        if (
            ed_record["regime"] != baseline_record["regime"]
            or ed_record["budget"] != baseline_record["budget"]
            or ed_record["true_system_bad"] != baseline_record["true_system_bad"]
            or ed_record["true_evidence_bad"] != baseline_record["true_evidence_bad"]
        ):
            raise ValueError("paired records do not share the same experimental unit")
    return pairs


def paired_contrast(
    pairs: Sequence[tuple[Mapping[str, object], Mapping[str, object]]],
    *,
    endpoint: str,
    bin_edges: Sequence[float],
    confidence_level: float,
    bootstrap_resamples: int,
    permutation_resamples: int,
    analysis_seed: int,
    contrast_key: str,
) -> dict[str, float]:
    if endpoint not in CONFIRMATORY_ENDPOINTS:
        raise ValueError(f"endpoint is not in the frozen confirmatory family: {endpoint}")
    if not pairs:
        raise ValueError("paired contrast requires at least one pair")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must be in (0, 1)")
    if bootstrap_resamples <= 0 or permutation_resamples <= 0:
        raise ValueError("resample counts must be positive")

    ed_records = [pair[0] for pair in pairs]
    baseline_records = [pair[1] for pair in pairs]
    ed_value = endpoint_value(ed_records, endpoint, bin_edges)
    baseline_value = endpoint_value(baseline_records, endpoint, bin_edges)
    observed = ed_value - baseline_value

    rng = random.Random(_stable_seed(analysis_seed, contrast_key))
    bootstrap: list[float] = []
    pair_count = len(pairs)
    for _ in range(bootstrap_resamples):
        indices = [rng.randrange(pair_count) for _ in range(pair_count)]
        resampled_ed = [pairs[index][0] for index in indices]
        resampled_baseline = [pairs[index][1] for index in indices]
        bootstrap.append(
            endpoint_value(resampled_ed, endpoint, bin_edges)
            - endpoint_value(resampled_baseline, endpoint, bin_edges)
        )
    bootstrap.sort()
    tail = (1.0 - confidence_level) / 2.0
    lower_index = min(int(tail * bootstrap_resamples), bootstrap_resamples - 1)
    upper_index = min(
        int((1.0 - tail) * bootstrap_resamples), bootstrap_resamples - 1
    )

    extreme = 0
    for _ in range(permutation_resamples):
        permuted_ed: list[Mapping[str, object]] = []
        permuted_baseline: list[Mapping[str, object]] = []
        for ed_record, baseline_record in pairs:
            if rng.random() < 0.5:
                permuted_ed.append(ed_record)
                permuted_baseline.append(baseline_record)
            else:
                permuted_ed.append(baseline_record)
                permuted_baseline.append(ed_record)
        permuted = endpoint_value(permuted_ed, endpoint, bin_edges) - endpoint_value(
            permuted_baseline, endpoint, bin_edges
        )
        extreme += int(abs(permuted) >= abs(observed) - 1e-15)
    p_value = (extreme + 1.0) / (permutation_resamples + 1.0)

    return {
        "ed_value": ed_value,
        "baseline_value": baseline_value,
        "difference_ed_minus_baseline": observed,
        "ci_lower": bootstrap[lower_index],
        "ci_upper": bootstrap[upper_index],
        "p_value": p_value,
    }


def holm_step_down(p_values: Sequence[float], alpha: float) -> list[dict[str, object]]:
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be in (0, 1)")
    if any(not 0.0 <= value <= 1.0 for value in p_values):
        raise ValueError("p-values must be in [0, 1]")
    count = len(p_values)
    order = sorted(range(count), key=lambda index: p_values[index])
    adjusted = [0.0] * count
    running = 0.0
    reject_open = True
    rejected = [False] * count
    for rank, index in enumerate(order):
        multiplier = count - rank
        running = max(running, min(1.0, multiplier * p_values[index]))
        adjusted[index] = running
        threshold = alpha / multiplier
        rejected[index] = reject_open and p_values[index] <= threshold
        if not rejected[index]:
            reject_open = False
    return [
        {"adjusted_p_value": adjusted[index], "reject_holm": rejected[index]}
        for index in range(count)
    ]


def group_records(
    records: Iterable[Mapping[str, object]],
) -> dict[tuple[str, int, str], list[Mapping[str, object]]]:
    groups: dict[tuple[str, int, str], list[Mapping[str, object]]] = {}
    for record in records:
        key = (str(record["regime"]), int(record["budget"]), str(record["policy"]))
        groups.setdefault(key, []).append(record)
    for group in groups.values():
        group.sort(key=lambda record: int(record["seed"]))
    return groups
