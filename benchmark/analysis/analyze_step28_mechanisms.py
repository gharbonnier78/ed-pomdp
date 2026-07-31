"""Deterministic Step 2.8 mechanism diagnosis from immutable Step 2.7 results.

This module performs descriptive post-hoc analysis only. It does not rerun the
simulator, add hypothesis tests, compute new confidence intervals, or modify any
frozen Step 2.6/2.7 artifact.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Iterable, Mapping, Sequence


ANALYSIS_ROLE = "post_hoc_descriptive"
ED_POLICY = "ed_pomdp_voi"
BASELINES = (
    "fixed_plan",
    "random_acquisition",
    "entropy_acquisition",
    "risk_only",
    "classical_pomdp",
)
VOI_BASELINES = BASELINES[:-1]
POLICIES = (ED_POLICY, *BASELINES, "rule_based")
GO_CONDITIONAL_BOUNDARY = 1.0 / 13.0
CONDITIONAL_NO_GO_BOUNDARY = 3.0 / 11.0
DECISION_BOUNDARIES = (GO_CONDITIONAL_BOUNDARY, CONDITIONAL_NO_GO_BOUNDARY)
THRESHOLD_WINDOWS = (0.01, 0.025, 0.05)
EPSILON = 1e-12
EXPECTED_RAW_ROWS = 3360
EXPECTED_CONFIGS = 480
EXPECTED_PAIR_ROWS = EXPECTED_CONFIGS * len(BASELINES)


PAIRWISE_FIELDS = (
    "analysis_role",
    "config_id",
    "regime",
    "budget",
    "seed",
    "baseline",
    "true_system_bad",
    "true_evidence_bad",
    "ed_posterior_bad",
    "baseline_posterior_bad",
    "posterior_delta_ed_minus_baseline",
    "absolute_posterior_delta",
    "ed_brier_score",
    "baseline_brier_score",
    "brier_delta_ed_minus_baseline",
    "brier_direction",
    "ed_decision",
    "baseline_decision",
    "action_agreement",
    "decision_transition",
    "ed_decision_loss",
    "baseline_decision_loss",
    "decision_loss_delta_ed_minus_baseline",
    "decision_loss_direction",
    "ed_unsafe_go",
    "baseline_unsafe_go",
    "ed_unnecessary_no_go",
    "baseline_unnecessary_no_go",
    "ed_observations",
    "baseline_observations",
    "acquisition_trace_agreement",
    "ed_distance_to_nearest_boundary",
    "baseline_distance_to_nearest_boundary",
    "ed_within_0_01_boundary",
    "ed_within_0_025_boundary",
    "ed_within_0_05_boundary",
    "baseline_within_0_01_boundary",
    "baseline_within_0_025_boundary",
    "baseline_within_0_05_boundary",
    "calibration_better_action_same",
    "calibration_better_action_changed",
    "action_changed_outcome",
)


@dataclass(frozen=True)
class Episode:
    config_id: str
    regime: str
    budget: int
    seed: int
    policy: str
    true_system_bad: bool
    true_evidence_bad: bool
    posterior_bad: float
    decision: str
    decision_loss: float
    unsafe_go: int
    unnecessary_no_go: int
    brier_score: float
    observations: str


@dataclass(frozen=True)
class PairDiagnostic:
    config_id: str
    regime: str
    budget: int
    seed: int
    baseline: str
    true_system_bad: bool
    true_evidence_bad: bool
    ed_posterior_bad: float
    baseline_posterior_bad: float
    posterior_delta: float
    absolute_posterior_delta: float
    ed_brier_score: float
    baseline_brier_score: float
    brier_delta: float
    brier_direction: str
    ed_decision: str
    baseline_decision: str
    action_agreement: bool
    decision_transition: str
    ed_decision_loss: float
    baseline_decision_loss: float
    decision_loss_delta: float
    decision_loss_direction: str
    ed_unsafe_go: int
    baseline_unsafe_go: int
    ed_unnecessary_no_go: int
    baseline_unnecessary_no_go: int
    ed_observations: str
    baseline_observations: str
    acquisition_trace_agreement: bool
    ed_distance_to_boundary: float
    baseline_distance_to_boundary: float
    ed_within_windows: tuple[bool, ...]
    baseline_within_windows: tuple[bool, ...]
    calibration_better_action_same: bool
    calibration_better_action_changed: bool
    action_changed_outcome: str


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _as_bool(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"true", "1"}:
        return True
    if normalized in {"false", "0"}:
        return False
    raise ValueError(f"invalid boolean value: {value!r}")


def _direction(delta: float) -> str:
    if delta < -EPSILON:
        return "favorable"
    if delta > EPSILON:
        return "adverse"
    return "equal"


def _nearest_boundary_distance(probability: float) -> float:
    return min(abs(probability - boundary) for boundary in DECISION_BOUNDARIES)


def _format_float(value: float) -> str:
    return f"{value:.12f}"


def _format_rate(numerator: int, denominator: int) -> str:
    return _format_float(numerator / denominator if denominator else 0.0)


def read_episodes(path: Path) -> tuple[Episode, ...]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = tuple(csv.DictReader(handle))
    if len(rows) != EXPECTED_RAW_ROWS:
        raise ValueError(f"expected {EXPECTED_RAW_ROWS} raw rows, found {len(rows)}")

    episodes = tuple(
        Episode(
            config_id=row["config_id"],
            regime=row["regime"],
            budget=int(row["budget"]),
            seed=int(row["seed"]),
            policy=row["policy"],
            true_system_bad=_as_bool(row["true_system_bad"]),
            true_evidence_bad=_as_bool(row["true_evidence_bad"]),
            posterior_bad=float(row["posterior_bad"]),
            decision=row["decision"],
            decision_loss=float(row["decision_loss"]),
            unsafe_go=int(row["unsafe_go"]),
            unnecessary_no_go=int(row["unnecessary_no_go"]),
            brier_score=float(row["brier_score"]),
            observations=row["observations"],
        )
        for row in rows
    )
    if set(episode.policy for episode in episodes) != set(POLICIES):
        raise ValueError("raw policy registry does not match Step 2.8 expectations")
    return episodes


def group_episodes(episodes: Sequence[Episode]) -> dict[str, dict[str, Episode]]:
    grouped: dict[str, dict[str, Episode]] = defaultdict(dict)
    for episode in episodes:
        if episode.policy in grouped[episode.config_id]:
            raise ValueError(f"duplicate policy in config {episode.config_id}")
        grouped[episode.config_id][episode.policy] = episode

    if len(grouped) != EXPECTED_CONFIGS:
        raise ValueError(f"expected {EXPECTED_CONFIGS} configs, found {len(grouped)}")
    expected_policies = set(POLICIES)
    for config_id, policies in grouped.items():
        if set(policies) != expected_policies:
            raise ValueError(f"incomplete policy matrix for {config_id}")
        latent = {
            (episode.true_system_bad, episode.true_evidence_bad)
            for episode in policies.values()
        }
        if len(latent) != 1:
            raise ValueError(f"paired latent state drift in {config_id}")
    return dict(grouped)


def build_pair_diagnostics(
    grouped: Mapping[str, Mapping[str, Episode]],
) -> tuple[PairDiagnostic, ...]:
    diagnostics: list[PairDiagnostic] = []
    for config_id in sorted(grouped):
        policies = grouped[config_id]
        ed = policies[ED_POLICY]
        for baseline_name in BASELINES:
            baseline = policies[baseline_name]
            brier_delta = ed.brier_score - baseline.brier_score
            loss_delta = ed.decision_loss - baseline.decision_loss
            brier_direction = _direction(brier_delta)
            loss_direction = _direction(loss_delta)
            action_agreement = ed.decision == baseline.decision
            if action_agreement:
                changed_outcome = "not_changed"
            elif loss_direction == "favorable":
                changed_outcome = "ed_better"
            elif loss_direction == "adverse":
                changed_outcome = "ed_worse"
            else:
                changed_outcome = "equal_loss"

            ed_distance = _nearest_boundary_distance(ed.posterior_bad)
            baseline_distance = _nearest_boundary_distance(baseline.posterior_bad)
            diagnostics.append(
                PairDiagnostic(
                    config_id=config_id,
                    regime=ed.regime,
                    budget=ed.budget,
                    seed=ed.seed,
                    baseline=baseline_name,
                    true_system_bad=ed.true_system_bad,
                    true_evidence_bad=ed.true_evidence_bad,
                    ed_posterior_bad=ed.posterior_bad,
                    baseline_posterior_bad=baseline.posterior_bad,
                    posterior_delta=ed.posterior_bad - baseline.posterior_bad,
                    absolute_posterior_delta=abs(
                        ed.posterior_bad - baseline.posterior_bad
                    ),
                    ed_brier_score=ed.brier_score,
                    baseline_brier_score=baseline.brier_score,
                    brier_delta=brier_delta,
                    brier_direction=brier_direction,
                    ed_decision=ed.decision,
                    baseline_decision=baseline.decision,
                    action_agreement=action_agreement,
                    decision_transition=f"{baseline.decision}->{ed.decision}",
                    ed_decision_loss=ed.decision_loss,
                    baseline_decision_loss=baseline.decision_loss,
                    decision_loss_delta=loss_delta,
                    decision_loss_direction=loss_direction,
                    ed_unsafe_go=ed.unsafe_go,
                    baseline_unsafe_go=baseline.unsafe_go,
                    ed_unnecessary_no_go=ed.unnecessary_no_go,
                    baseline_unnecessary_no_go=baseline.unnecessary_no_go,
                    ed_observations=ed.observations,
                    baseline_observations=baseline.observations,
                    acquisition_trace_agreement=(
                        ed.observations == baseline.observations
                    ),
                    ed_distance_to_boundary=ed_distance,
                    baseline_distance_to_boundary=baseline_distance,
                    ed_within_windows=tuple(
                        ed_distance <= window + EPSILON
                        for window in THRESHOLD_WINDOWS
                    ),
                    baseline_within_windows=tuple(
                        baseline_distance <= window + EPSILON
                        for window in THRESHOLD_WINDOWS
                    ),
                    calibration_better_action_same=(
                        brier_direction == "favorable" and action_agreement
                    ),
                    calibration_better_action_changed=(
                        brier_direction == "favorable" and not action_agreement
                    ),
                    action_changed_outcome=changed_outcome,
                )
            )
    if len(diagnostics) != EXPECTED_PAIR_ROWS:
        raise AssertionError(
            f"expected {EXPECTED_PAIR_ROWS} pair rows, found {len(diagnostics)}"
        )
    return tuple(diagnostics)


def pair_to_row(pair: PairDiagnostic) -> dict[str, object]:
    values = {
        "analysis_role": ANALYSIS_ROLE,
        "config_id": pair.config_id,
        "regime": pair.regime,
        "budget": pair.budget,
        "seed": pair.seed,
        "baseline": pair.baseline,
        "true_system_bad": int(pair.true_system_bad),
        "true_evidence_bad": int(pair.true_evidence_bad),
        "ed_posterior_bad": _format_float(pair.ed_posterior_bad),
        "baseline_posterior_bad": _format_float(pair.baseline_posterior_bad),
        "posterior_delta_ed_minus_baseline": _format_float(pair.posterior_delta),
        "absolute_posterior_delta": _format_float(pair.absolute_posterior_delta),
        "ed_brier_score": _format_float(pair.ed_brier_score),
        "baseline_brier_score": _format_float(pair.baseline_brier_score),
        "brier_delta_ed_minus_baseline": _format_float(pair.brier_delta),
        "brier_direction": pair.brier_direction,
        "ed_decision": pair.ed_decision,
        "baseline_decision": pair.baseline_decision,
        "action_agreement": int(pair.action_agreement),
        "decision_transition": pair.decision_transition,
        "ed_decision_loss": _format_float(pair.ed_decision_loss),
        "baseline_decision_loss": _format_float(pair.baseline_decision_loss),
        "decision_loss_delta_ed_minus_baseline": _format_float(
            pair.decision_loss_delta
        ),
        "decision_loss_direction": pair.decision_loss_direction,
        "ed_unsafe_go": pair.ed_unsafe_go,
        "baseline_unsafe_go": pair.baseline_unsafe_go,
        "ed_unnecessary_no_go": pair.ed_unnecessary_no_go,
        "baseline_unnecessary_no_go": pair.baseline_unnecessary_no_go,
        "ed_observations": pair.ed_observations,
        "baseline_observations": pair.baseline_observations,
        "acquisition_trace_agreement": int(pair.acquisition_trace_agreement),
        "ed_distance_to_nearest_boundary": _format_float(
            pair.ed_distance_to_boundary
        ),
        "baseline_distance_to_nearest_boundary": _format_float(
            pair.baseline_distance_to_boundary
        ),
        "calibration_better_action_same": int(
            pair.calibration_better_action_same
        ),
        "calibration_better_action_changed": int(
            pair.calibration_better_action_changed
        ),
        "action_changed_outcome": pair.action_changed_outcome,
    }
    for index, label in enumerate(("0_01", "0_025", "0_05")):
        values[f"ed_within_{label}_boundary"] = int(pair.ed_within_windows[index])
        values[f"baseline_within_{label}_boundary"] = int(
            pair.baseline_within_windows[index]
        )
    return values


def write_csv(path: Path, fieldnames: Sequence[str], rows: Iterable[Mapping[str, object]]) -> int:
    materialized = tuple(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(materialized)
    return len(materialized)


def _summary_row(
    pairs: Sequence[PairDiagnostic],
    *,
    baseline: str,
    regime: str,
    budget: str,
) -> dict[str, object]:
    n = len(pairs)
    if n == 0:
        raise ValueError("summary groups must not be empty")
    decision_counts = Counter(pair.decision_loss_direction for pair in pairs)
    brier_counts = Counter(pair.brier_direction for pair in pairs)
    action_agreement = sum(pair.action_agreement for pair in pairs)
    trace_agreement = sum(pair.acquisition_trace_agreement for pair in pairs)
    action_changed = n - action_agreement
    changed_outcomes = Counter(pair.action_changed_outcome for pair in pairs)
    calibration_same = sum(pair.calibration_better_action_same for pair in pairs)
    calibration_changed = sum(
        pair.calibration_better_action_changed for pair in pairs
    )
    return {
        "analysis_role": ANALYSIS_ROLE,
        "baseline": baseline,
        "regime": regime,
        "budget": budget,
        "pair_count": n,
        "decision_favorable_count": decision_counts["favorable"],
        "decision_adverse_count": decision_counts["adverse"],
        "decision_equal_count": decision_counts["equal"],
        "brier_favorable_count": brier_counts["favorable"],
        "brier_adverse_count": brier_counts["adverse"],
        "brier_equal_count": brier_counts["equal"],
        "action_agreement_count": action_agreement,
        "action_agreement_rate": _format_rate(action_agreement, n),
        "acquisition_trace_agreement_count": trace_agreement,
        "acquisition_trace_agreement_rate": _format_rate(trace_agreement, n),
        "mean_absolute_posterior_delta": _format_float(
            mean(pair.absolute_posterior_delta for pair in pairs)
        ),
        "mean_decision_loss_delta": _format_float(
            mean(pair.decision_loss_delta for pair in pairs)
        ),
        "mean_brier_delta": _format_float(mean(pair.brier_delta for pair in pairs)),
        "calibration_better_action_same_count": calibration_same,
        "calibration_better_action_same_rate": _format_rate(calibration_same, n),
        "calibration_better_action_changed_count": calibration_changed,
        "action_changed_count": action_changed,
        "action_changed_ed_better_count": changed_outcomes["ed_better"],
        "action_changed_ed_worse_count": changed_outcomes["ed_worse"],
        "action_changed_equal_loss_count": changed_outcomes["equal_loss"],
        "ed_unsafe_go_count": sum(pair.ed_unsafe_go for pair in pairs),
        "baseline_unsafe_go_count": sum(pair.baseline_unsafe_go for pair in pairs),
        "ed_unnecessary_no_go_count": sum(
            pair.ed_unnecessary_no_go for pair in pairs
        ),
        "baseline_unnecessary_no_go_count": sum(
            pair.baseline_unnecessary_no_go for pair in pairs
        ),
    }


def build_mechanism_summaries(
    pairs: Sequence[PairDiagnostic],
) -> tuple[dict[str, object], ...]:
    regimes = sorted({pair.regime for pair in pairs})
    budgets = sorted({pair.budget for pair in pairs})
    rows: list[dict[str, object]] = []
    for baseline in BASELINES:
        baseline_pairs = tuple(pair for pair in pairs if pair.baseline == baseline)
        rows.append(
            _summary_row(
                baseline_pairs, baseline=baseline, regime="ALL", budget="ALL"
            )
        )
        for regime in regimes:
            selected = tuple(pair for pair in baseline_pairs if pair.regime == regime)
            rows.append(
                _summary_row(
                    selected, baseline=baseline, regime=regime, budget="ALL"
                )
            )
        for budget in budgets:
            selected = tuple(pair for pair in baseline_pairs if pair.budget == budget)
            rows.append(
                _summary_row(
                    selected,
                    baseline=baseline,
                    regime="ALL",
                    budget=str(budget),
                )
            )
        for regime in regimes:
            for budget in budgets:
                selected = tuple(
                    pair
                    for pair in baseline_pairs
                    if pair.regime == regime and pair.budget == budget
                )
                rows.append(
                    _summary_row(
                        selected,
                        baseline=baseline,
                        regime=regime,
                        budget=str(budget),
                    )
                )
    return tuple(rows)


def build_transition_rows(
    pairs: Sequence[PairDiagnostic],
) -> tuple[dict[str, object], ...]:
    rows: list[dict[str, object]] = []
    regimes = ["ALL", *sorted({pair.regime for pair in pairs})]
    for baseline in BASELINES:
        baseline_pairs = tuple(pair for pair in pairs if pair.baseline == baseline)
        for regime in regimes:
            selected = (
                baseline_pairs
                if regime == "ALL"
                else tuple(pair for pair in baseline_pairs if pair.regime == regime)
            )
            grouped: dict[tuple[str, str], list[PairDiagnostic]] = defaultdict(list)
            for pair in selected:
                grouped[(pair.baseline_decision, pair.ed_decision)].append(pair)
            for (baseline_decision, ed_decision), items in sorted(grouped.items()):
                directions = Counter(item.decision_loss_direction for item in items)
                rows.append(
                    {
                        "analysis_role": ANALYSIS_ROLE,
                        "baseline": baseline,
                        "regime": regime,
                        "baseline_decision": baseline_decision,
                        "ed_decision": ed_decision,
                        "transition_count": len(items),
                        "mean_decision_loss_delta": _format_float(
                            mean(item.decision_loss_delta for item in items)
                        ),
                        "mean_absolute_posterior_delta": _format_float(
                            mean(item.absolute_posterior_delta for item in items)
                        ),
                        "ed_better_count": directions["favorable"],
                        "ed_worse_count": directions["adverse"],
                        "equal_loss_count": directions["equal"],
                    }
                )
    return tuple(rows)


def build_threshold_rows(episodes: Sequence[Episode]) -> tuple[dict[str, object], ...]:
    grouped: dict[tuple[str, str, int], list[Episode]] = defaultdict(list)
    for episode in episodes:
        grouped[(episode.policy, episode.regime, episode.budget)].append(episode)
    rows: list[dict[str, object]] = []
    for (policy, regime, budget), items in sorted(grouped.items()):
        distances = [_nearest_boundary_distance(item.posterior_bad) for item in items]
        decisions = Counter(item.decision for item in items)
        row: dict[str, object] = {
            "analysis_role": ANALYSIS_ROLE,
            "policy": policy,
            "regime": regime,
            "budget": budget,
            "episode_count": len(items),
            "mean_posterior_bad": _format_float(
                mean(item.posterior_bad for item in items)
            ),
            "mean_distance_to_nearest_boundary": _format_float(mean(distances)),
            "minimum_distance_to_nearest_boundary": _format_float(min(distances)),
            "go_count": decisions["GO"],
            "conditional_go_count": decisions["CONDITIONAL_GO"],
            "no_go_count": decisions["NO_GO"],
        }
        for window, label in zip(THRESHOLD_WINDOWS, ("0_01", "0_025", "0_05")):
            count = sum(distance <= window + EPSILON for distance in distances)
            row[f"within_{label}_count"] = count
            row[f"within_{label}_rate"] = _format_rate(count, len(items))
        rows.append(row)
    return tuple(rows)


def _parse_trace(serialized: str) -> tuple[tuple[str, int], ...]:
    if not serialized:
        return ()
    parsed: list[tuple[str, int]] = []
    for item in serialized.split(";"):
        channel, failed = item.rsplit(":", 1)
        parsed.append((channel, int(failed)))
    return tuple(parsed)


def build_acquisition_rows(episodes: Sequence[Episode]) -> tuple[dict[str, object], ...]:
    grouped: dict[tuple[str, str, int, int, str], list[int]] = defaultdict(list)
    for episode in episodes:
        trace = _parse_trace(episode.observations)
        if len(trace) != episode.budget:
            raise ValueError(f"trace length drift in {episode.config_id} / {episode.policy}")
        for position, (channel, failed) in enumerate(trace, start=1):
            grouped[
                (episode.policy, episode.regime, episode.budget, position, channel)
            ].append(failed)
    rows: list[dict[str, object]] = []
    for (policy, regime, budget, position, channel), failures in sorted(
        grouped.items()
    ):
        selection_denominator = sum(
            len(values)
            for (p, r, b, pos, _), values in grouped.items()
            if (p, r, b, pos) == (policy, regime, budget, position)
        )
        failure_count = sum(failures)
        rows.append(
            {
                "analysis_role": ANALYSIS_ROLE,
                "policy": policy,
                "regime": regime,
                "budget": budget,
                "acquisition_position": position,
                "channel": channel,
                "selection_count": len(failures),
                "selection_rate": _format_rate(
                    len(failures), selection_denominator
                ),
                "failure_count": failure_count,
                "failure_rate": _format_rate(failure_count, len(failures)),
            }
        )
    return tuple(rows)


def read_step27_directionality(path: Path) -> dict[tuple[str, str, str, str], dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = tuple(csv.DictReader(handle))
    indexed = {
        (row["scope"], row["endpoint"], row["grouping"], row["group_value"]): row
        for row in rows
    }
    required = (
        ("all_confirmatory_baselines", "decision_loss", "overall", "all"),
        ("all_confirmatory_baselines", "brier_score", "overall", "all"),
        (
            "all_confirmatory_baselines",
            "expected_calibration_error",
            "overall",
            "all",
        ),
        (
            "clm_voi_named_acquisition_baselines",
            "decision_loss",
            "overall",
            "all",
        ),
    )
    missing = [key for key in required if key not in indexed]
    if missing:
        raise ValueError(f"Step 2.7 directionality rows missing: {missing}")
    return indexed


def _overall_summary(
    summaries: Sequence[Mapping[str, object]], baseline: str
) -> Mapping[str, object]:
    for row in summaries:
        if (
            row["baseline"] == baseline
            and row["regime"] == "ALL"
            and row["budget"] == "ALL"
        ):
            return row
    raise KeyError(baseline)


def build_report(
    *,
    pairs: Sequence[PairDiagnostic],
    summaries: Sequence[Mapping[str, object]],
    directionality: Mapping[tuple[str, str, str, str], Mapping[str, str]],
    episodes: Sequence[Episode],
) -> str:
    all_decision = directionality[
        ("all_confirmatory_baselines", "decision_loss", "overall", "all")
    ]
    all_brier = directionality[
        ("all_confirmatory_baselines", "brier_score", "overall", "all")
    ]
    all_ece = directionality[
        (
            "all_confirmatory_baselines",
            "expected_calibration_error",
            "overall",
            "all",
        )
    ]
    voi_decision = directionality[
        (
            "clm_voi_named_acquisition_baselines",
            "decision_loss",
            "overall",
            "all",
        )
    ]

    classical = _overall_summary(summaries, "classical_pomdp")
    risk_only = _overall_summary(summaries, "risk_only")

    overall_calibration_same = sum(
        pair.calibration_better_action_same for pair in pairs
    )
    overall_calibration_changed = sum(
        pair.calibration_better_action_changed for pair in pairs
    )
    changed_pairs = [pair for pair in pairs if not pair.action_agreement]
    changed_directions = Counter(pair.decision_loss_direction for pair in changed_pairs)

    safety: dict[tuple[str, str], int] = defaultdict(int)
    for episode in episodes:
        if episode.policy in {ED_POLICY, "classical_pomdp"}:
            safety[(episode.policy, episode.regime)] += episode.unsafe_go

    lines = [
        "# Step 2.8 Claim Adjudication and Mechanism Diagnosis",
        "",
        "## Epistemic status",
        "",
        "This report combines the frozen Step 2.7 confirmatory outcome with deterministic post-hoc mechanism diagnostics. The diagnostics add no p-values, confidence intervals or retrospective confirmatory hypotheses.",
        "",
        "## Frozen confirmatory outcome",
        "",
        f"- Decision loss across all five baselines: favourable `{all_decision['favorable_count']}/80`, adverse `{all_decision['adverse_count']}/80`, equal `{all_decision['equal_count']}/80`.",
        f"- Brier score: favourable `{all_brier['favorable_count']}/80`, adverse `{all_brier['adverse_count']}/80`, equal `{all_brier['equal_count']}/80`.",
        f"- ECE: favourable `{all_ece['favorable_count']}/80`, adverse `{all_ece['adverse_count']}/80`, equal `{all_ece['equal_count']}/80`.",
        f"- Claim-relevant VOI baselines, decision loss: favourable `{voi_decision['favorable_count']}/64`, adverse `{voi_decision['adverse_count']}/64`, equal `{voi_decision['equal_count']}/64`.",
        "- Exactly one of 240 frozen contrasts survived Holm correction: ECE, ED-POMDP versus classical POMDP, degraded evidence, budget 2. Its paired bootstrap interval crossed zero and posterior support was sparse.",
        "",
        "## Post-hoc mechanism findings",
        "",
        f"The episode-level diagnostic contains `{len(pairs)}` paired ED-POMDP-versus-baseline rows.",
        "",
        "### Calibration-to-action bridge",
        "",
        f"- Better ED-POMDP Brier score with the same terminal action: `{overall_calibration_same}/{len(pairs)}` pairs.",
        f"- Better ED-POMDP Brier score with a changed terminal action: `{overall_calibration_changed}/{len(pairs)}` pairs.",
        f"- Across all `{len(changed_pairs)}` changed-action pairs, realised loss was better for ED-POMDP in `{changed_directions['favorable']}`, worse in `{changed_directions['adverse']}`, and equal in `{changed_directions['equal']}`.",
        "",
        "This directly tests the proposed mechanism: improved probabilistic accuracy often remains decision-inert because the posterior does not cross a frozen GO / CONDITIONAL GO / NO-GO boundary. When a boundary is crossed, the realised decision is not consistently improved.",
        "",
        "### Classical POMDP comparison",
        "",
        f"- Action agreement: `{classical['action_agreement_count']}/{classical['pair_count']}` (`{classical['action_agreement_rate']}`).",
        f"- Acquisition-trace agreement: `{classical['acquisition_trace_agreement_count']}/{classical['pair_count']}` (`{classical['acquisition_trace_agreement_rate']}`).",
        f"- Mean absolute posterior difference: `{classical['mean_absolute_posterior_delta']}`.",
        f"- Changed-action outcomes: ED better `{classical['action_changed_ed_better_count']}`, worse `{classical['action_changed_ed_worse_count']}`, equal `{classical['action_changed_equal_loss_count']}`.",
        "",
        "### Risk-only comparison",
        "",
        f"- Action agreement: `{risk_only['action_agreement_count']}/{risk_only['pair_count']}` (`{risk_only['action_agreement_rate']}`).",
        f"- Acquisition-trace agreement: `{risk_only['acquisition_trace_agreement_count']}/{risk_only['pair_count']}` (`{risk_only['acquisition_trace_agreement_rate']}`).",
        f"- Mean absolute posterior difference: `{risk_only['mean_absolute_posterior_delta']}`.",
        f"- Changed-action outcomes: ED better `{risk_only['action_changed_ed_better_count']}`, worse `{risk_only['action_changed_ed_worse_count']}`, equal `{risk_only['action_changed_equal_loss_count']}`.",
        "",
        "### Mandatory descriptive safety evidence",
        "",
        f"- ED-POMDP unsafe GO: identifiable `{safety[(ED_POLICY, 'identifiable')]}`, degraded evidence `{safety[(ED_POLICY, 'evidence_degraded')]}`, likelihood misspecified `{safety[(ED_POLICY, 'likelihood_misspecified')]}`, non-identifiable `{safety[(ED_POLICY, 'non_identifiable')]}`.",
        f"- Classical POMDP unsafe GO: identifiable `{safety[('classical_pomdp', 'identifiable')]}`, degraded evidence `{safety[('classical_pomdp', 'evidence_degraded')]}`, likelihood misspecified `{safety[('classical_pomdp', 'likelihood_misspecified')]}`, non-identifiable `{safety[('classical_pomdp', 'non_identifiable')]}`.",
        "",
        "The safety pattern is favourable to ED-POMDP in the three avoidable regimes, but `unsafe_go_rate` was a mandatory descriptive endpoint and was not tested for superiority.",
        "",
        "## Claim adjudication",
        "",
        "### `CLM-VOI-001`",
        "",
        "**Disposition: NOT SUPPORTED IN THE FROZEN STEP 2 BENCHMARK.** No decision-loss contrast survived Holm correction. At the aggregate-cell level, the four claim-relevant acquisition baselines yielded 10 favourable, 16 adverse and 38 equal directions. The post-hoc mechanism analysis shows that probabilistic changes frequently fail to change the action and that changed actions are not consistently beneficial.",
        "",
        "This disposition is benchmark-bounded; it is not a proof that decision-aware value of information can never help under another terminal rule, horizon, loss model or evidence structure.",
        "",
        "### `CLM-EQ-001`",
        "",
        "**Disposition: BROAD FORM NOT SUPPORTED; ONE NARROW CALIBRATION SIGNAL RETAINED.** Explicit evidence-quality modelling produced one Holm-significant ECE contrast in the degraded-evidence, budget-2 cell. The evidence is too narrow and resolution-sensitive to support general calibration or decision superiority across degradation and misspecification.",
        "",
        "## Step 2 scientific conclusion",
        "",
        "Step 2 does not validate general ED-POMDP superiority. It establishes a more precise engineering result: a better probabilistic representation of evidence quality is not sufficient unless the terminal decision architecture can convert that improvement into a different and better action.",
        "",
        "## Future preregistration boundary",
        "",
        "A future experiment must use new development and confirmatory seeds and must not tune on Step 2 headline seeds. Candidate changes include adaptive stopping, explicit GO / CONDITIONAL GO / NO-GO governance, asymmetric safety and business costs, correlated evidence, non-unit acquisition costs, and terminal rules conditioned jointly on system risk and evidence quality.",
        "",
    ]
    return "\n".join(lines)


def generate(
    *,
    raw_path: Path,
    directionality_path: Path,
    output_dir: Path,
    overwrite: bool = False,
) -> dict[str, object]:
    output_paths = {
        "pairwise": output_dir / "step28_pairwise_diagnostics.csv",
        "summary": output_dir / "step28_mechanism_summary.csv",
        "transitions": output_dir / "step28_decision_transitions.csv",
        "thresholds": output_dir / "step28_threshold_occupancy.csv",
        "acquisition": output_dir / "step28_acquisition_summary.csv",
        "report": output_dir / "STEP_2_8_CLAIM_ADJUDICATION.md",
        "metadata": output_dir / "step28_analysis_metadata.json",
    }
    existing = [path for path in output_paths.values() if path.exists()]
    if existing and not overwrite:
        raise FileExistsError(f"Step 2.8 outputs already exist: {existing}")

    episodes = read_episodes(raw_path)
    grouped = group_episodes(episodes)
    pairs = build_pair_diagnostics(grouped)
    summaries = build_mechanism_summaries(pairs)
    transitions = build_transition_rows(pairs)
    thresholds = build_threshold_rows(episodes)
    acquisition = build_acquisition_rows(episodes)
    directionality = read_step27_directionality(directionality_path)

    output_dir.mkdir(parents=True, exist_ok=True)
    counts = {
        "pairwise_rows": write_csv(
            output_paths["pairwise"],
            PAIRWISE_FIELDS,
            (pair_to_row(pair) for pair in pairs),
        ),
        "summary_rows": write_csv(
            output_paths["summary"],
            tuple(summaries[0].keys()),
            summaries,
        ),
        "transition_rows": write_csv(
            output_paths["transitions"],
            tuple(transitions[0].keys()),
            transitions,
        ),
        "threshold_rows": write_csv(
            output_paths["thresholds"],
            tuple(thresholds[0].keys()),
            thresholds,
        ),
        "acquisition_rows": write_csv(
            output_paths["acquisition"],
            tuple(acquisition[0].keys()),
            acquisition,
        ),
    }
    report = build_report(
        pairs=pairs,
        summaries=summaries,
        directionality=directionality,
        episodes=episodes,
    )
    output_paths["report"].write_text(report, encoding="utf-8")

    metadata = {
        "schema_version": "0.3.0",
        "analysis_role": ANALYSIS_ROLE,
        "generator": "benchmark/analysis/analyze_step28_mechanisms.py",
        "generator_sha256": sha256_path(Path(__file__)),
        "inputs": {
            str(raw_path): sha256_path(raw_path),
            str(directionality_path): sha256_path(directionality_path),
        },
        "decision_boundaries": {
            "go_conditional": GO_CONDITIONAL_BOUNDARY,
            "conditional_no_go": CONDITIONAL_NO_GO_BOUNDARY,
        },
        "threshold_windows": list(THRESHOLD_WINDOWS),
        "counts": counts,
        "outputs": {
            key: {
                "path": str(path),
                "sha256": sha256_path(path),
            }
            for key, path in output_paths.items()
            if key != "metadata"
        },
        "inferential_status": "descriptive_post_hoc_no_new_tests",
    }
    output_paths["metadata"].write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return metadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw", default="benchmark/results/headline_raw.csv"
    )
    parser.add_argument(
        "--directionality",
        default="benchmark/results/step27_posthoc_directionality.csv",
    )
    parser.add_argument(
        "--output-dir", default="benchmark/results/step28_generated"
    )
    parser.add_argument("--overwrite", action="store_true")
    arguments = parser.parse_args()
    metadata = generate(
        raw_path=Path(arguments.raw),
        directionality_path=Path(arguments.directionality),
        output_dir=Path(arguments.output_dir),
        overwrite=arguments.overwrite,
    )
    print(json.dumps(metadata, sort_keys=True))


if __name__ == "__main__":
    main()
