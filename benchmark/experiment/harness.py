"""Reproducible fixed-horizon harness for the Step 2 headline matrix.

The confirmatory benchmark uses exact-cost fixed horizons. Early stopping remains
available in the runtime for exploratory studies, but is prohibited here because
it would violate equal-total-cost and equal-horizon matching.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import csv
import hashlib
import json
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Sequence

from benchmark.runtime.decision import (
    LossWeights,
    decide_from_posterior,
    expected_terminal_risk,
    score_decision,
)
from benchmark.runtime.policy_matrix import POLICY_NAMES, build_policy_matrix
from benchmark.runtime.simulator import Observation, Regime, SyntheticReleaseEnvironment


CONFIRMATORY_METRICS = (
    "decision_loss",
    "brier_score",
    "expected_calibration_error",
)
MANDATORY_SAFETY_METRICS = ("unsafe_go_rate",)


@dataclass(frozen=True)
class HeadlineEpisodeRecord:
    config_id: str
    regime: str
    budget: int
    seed: int
    policy: str
    policy_seed: int
    true_system_bad: bool
    true_evidence_bad: bool
    posterior_bad: float
    decision: str
    decision_loss: float
    unsafe_go: int
    unnecessary_no_go: int
    brier_score: float
    residual_risk: float
    evidence_cost: float
    acquisition_count: int
    observations: str


def load_headline_config(path: str | Path) -> dict[str, object]:
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_headline_config(config)
    return config


def validate_headline_config(config: Mapping[str, object]) -> None:
    if tuple(config.get("policies", ())) != POLICY_NAMES:
        raise ValueError("headline policy order must match the canonical registry")

    regimes = tuple(config.get("regimes", ()))
    valid_regimes = {regime.value for regime in Regime}
    if not regimes or any(regime not in valid_regimes for regime in regimes):
        raise ValueError("headline regimes must be executable runtime regimes")

    budgets = tuple(config.get("budgets", ()))
    if not budgets or any(not isinstance(budget, int) or budget <= 0 for budget in budgets):
        raise ValueError("headline budgets must be positive integer horizons")

    seeds = tuple(config.get("seeds", ()))
    if len(seeds) < 30 or len(set(seeds)) != len(seeds):
        raise ValueError("headline config requires at least 30 unique seeds")

    matched = config.get("matched_budget")
    if not isinstance(matched, Mapping):
        raise ValueError("matched_budget section is required")
    if matched.get("mode") != "fixed_horizon_exact_cost":
        raise ValueError("headline mode must be fixed_horizon_exact_cost")
    if matched.get("allow_early_stopping") is not False:
        raise ValueError("headline execution must prohibit early stopping")
    if matched.get("unit_action_cost") != 1.0:
        raise ValueError("current headline harness requires unit action cost 1.0")
    for invariant in (
        "enforce_equal_total_cost",
        "enforce_equal_channel_access",
        "enforce_equal_horizon",
        "prohibit_ground_truth_access",
    ):
        if matched.get(invariant) is not True:
            raise ValueError(f"matched-budget invariant not enabled: {invariant}")

    loss_weights = config.get("loss_weights")
    expected_loss_keys = {
        "unsafe_go",
        "unnecessary_no_go",
        "conditional_bad",
        "conditional_good",
        "evidence_cost",
    }
    if not isinstance(loss_weights, Mapping) or set(loss_weights) != expected_loss_keys:
        raise ValueError("all LossWeights values must be explicit in headline config")
    if any(float(value) < 0.0 for value in loss_weights.values()):
        raise ValueError("LossWeights values must be non-negative")

    if tuple(config.get("confirmatory_metrics", ())) != CONFIRMATORY_METRICS:
        raise ValueError("headline confirmatory metrics must match the frozen registry")
    if tuple(config.get("mandatory_safety_metrics", ())) != MANDATORY_SAFETY_METRICS:
        raise ValueError("headline safety metrics must match the frozen registry")
    if set(CONFIRMATORY_METRICS) & set(MANDATORY_SAFETY_METRICS):
        raise AssertionError("safety reporting must remain outside confirmatory inference")

    calibration = config.get("calibration")
    if not isinstance(calibration, Mapping):
        raise ValueError("calibration section is required")
    bin_edges = tuple(float(value) for value in calibration.get("bin_edges", ()))
    expected_bin_edges = tuple(index / 10.0 for index in range(11))
    if bin_edges != expected_bin_edges:
        raise ValueError("headline ECE must use the frozen ten equal-width bins")
    if calibration.get("report_resolution_diagnostics") is not True:
        raise ValueError("ECE resolution diagnostics must be enabled")

    analysis = config.get("analysis")
    if not isinstance(analysis, Mapping):
        raise ValueError("analysis section is required")
    multiplicity = analysis.get("multiplicity")
    if not isinstance(multiplicity, Mapping):
        raise ValueError("multiplicity section is required")
    expected_family_size = (
        len(regimes)
        * len(budgets)
        * len(tuple(config.get("confirmatory_baselines", ())))
        * len(CONFIRMATORY_METRICS)
    )
    if multiplicity.get("expected_family_size") != expected_family_size:
        raise ValueError("configured Holm family size does not match headline dimensions")

    randomness = config.get("randomness")
    if not isinstance(randomness, Mapping):
        raise ValueError("randomness section is required")
    required_randomness = (
        "policy_stream_is_distinct_from_environment",
        "fresh_policy_instance_per_experimental_unit",
        "fresh_environment_instance_per_policy",
        "shared_counterfactual_environment_tape_per_cell",
    )
    if any(randomness.get(key) is not True for key in required_randomness):
        raise ValueError("headline random-stream separation is not fully enabled")

    expected_rows = len(regimes) * len(budgets) * len(seeds) * len(POLICY_NAMES)
    if config.get("expected_episode_rows") != expected_rows:
        raise ValueError("expected_episode_rows does not match the frozen matrix")


def loss_weights_from_config(config: Mapping[str, object]) -> LossWeights:
    values = config["loss_weights"]
    assert isinstance(values, Mapping)
    return LossWeights(**{key: float(value) for key, value in values.items()})


def derive_policy_seed(environment_seed: int, policy_name: str) -> int:
    """Derive a policy-local seed independent of the environment noise tape."""
    payload = f"ed-pomdp-policy|{environment_seed}|{policy_name}".encode("utf-8")
    digest = hashlib.sha256(payload).digest()
    return int.from_bytes(digest[:8], "big")


def _serialize_observations(observations: Sequence[Observation]) -> str:
    return ";".join(
        f"{observation.channel}:{int(observation.failed)}"
        for observation in observations
    )


def run_experiment_cell(
    *,
    regime: Regime,
    budget: int,
    seed: int,
    weights: LossWeights,
) -> tuple[HeadlineEpisodeRecord, ...]:
    """Run all seven fresh policies on one paired counterfactual scenario."""
    random_policy_seed = derive_policy_seed(seed, "random_acquisition")
    policies = build_policy_matrix(random_seed=random_policy_seed, weights=weights)
    records: list[HeadlineEpisodeRecord] = []

    for policy in policies:
        # Fresh mutable objects prevent state leakage. The shared seed addresses
        # the same latent state and common-random-number tape for every policy.
        environment = SyntheticReleaseEnvironment(regime=regime, seed=seed)
        history: list[Observation] = []

        for _ in range(budget):
            channel = policy.choose(tuple(history), environment.available_channels)
            history.append(environment.acquire(channel))

        outcome = environment.finish()
        posterior_bad = policy.posterior_bad(tuple(history))
        decision = decide_from_posterior(posterior_bad, weights=weights)
        score = score_decision(outcome, decision, weights=weights)
        residual_risk = expected_terminal_risk(
            posterior_bad, decision, weights=weights
        )
        record = HeadlineEpisodeRecord(
            config_id=f"{regime.value}|budget={budget}|seed={seed}",
            regime=regime.value,
            budget=budget,
            seed=seed,
            policy=policy.name,
            policy_seed=derive_policy_seed(seed, policy.name),
            true_system_bad=outcome.true_system_bad,
            true_evidence_bad=outcome.true_evidence_bad,
            posterior_bad=posterior_bad,
            decision=decision.value,
            decision_loss=score.decision_loss,
            unsafe_go=int(score.unsafe_go),
            unnecessary_no_go=int(score.unnecessary_no_go),
            brier_score=(posterior_bad - float(outcome.true_system_bad)) ** 2,
            residual_risk=residual_risk,
            evidence_cost=score.acquisition_cost,
            acquisition_count=len(history),
            observations=_serialize_observations(history),
        )
        if record.acquisition_count != budget or record.evidence_cost != float(budget):
            raise AssertionError("headline policy violated exact-cost fixed horizon")
        records.append(record)

    if tuple(record.policy for record in records) != POLICY_NAMES:
        raise AssertionError("policy execution order drifted from frozen registry")
    latent_pairs = {
        (record.true_system_bad, record.true_evidence_bad) for record in records
    }
    if len(latent_pairs) != 1:
        raise AssertionError("paired policies did not receive the same latent scenario")
    return tuple(records)


def iter_headline_records(
    config: Mapping[str, object],
) -> Iterator[HeadlineEpisodeRecord]:
    validate_headline_config(config)
    weights = loss_weights_from_config(config)
    regimes = tuple(Regime(value) for value in config["regimes"])
    budgets = tuple(int(value) for value in config["budgets"])
    seeds = tuple(int(value) for value in config["seeds"])
    for regime in regimes:
        for budget in budgets:
            for seed in seeds:
                yield from run_experiment_cell(
                    regime=regime,
                    budget=budget,
                    seed=seed,
                    weights=weights,
                )


def write_raw_csv(
    records: Iterable[HeadlineEpisodeRecord], path: str | Path
) -> int:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    rows = tuple(records)
    if not rows:
        raise ValueError("at least one headline record is required")
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(asdict(rows[0]).keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))
    return len(rows)
