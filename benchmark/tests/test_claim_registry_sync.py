from __future__ import annotations

import csv
import json
from pathlib import Path


CSV_PATH = Path("docs/CLAIMS.csv")
JSON_PATH = Path("docs/CLAIMS.json")
MARKDOWN_PATH = Path("docs/CLAIMS.md")
LEGACY_CSV_PATH = Path("claims/claim_registry.csv")
LEGACY_JSON_PATH = Path("claims/claim_registry.json")
LEGACY_README_PATH = Path("claims/README.md")
SCALAR_FIELDS = (
    "id",
    "statement",
    "type",
    "maturity",
    "evidence_level",
    "evidence_polarity",
    "disposition",
    "refutation_gate",
    "next_step",
    "last_revision",
)


def _read_csv(path: Path) -> tuple[dict[str, str], ...]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return tuple(csv.DictReader(handle))


def test_claim_registry_csv_json_and_markdown_are_synchronized() -> None:
    csv_rows = _read_csv(CSV_PATH)
    registry = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    json_rows = tuple(registry["claims"])
    markdown = MARKDOWN_PATH.read_text(encoding="utf-8")

    assert registry["authoritative_source"] == "docs/CLAIMS.md"
    assert registry["last_revision"] == "2026-07-31"
    assert len(csv_rows) == len(json_rows) == 7

    csv_by_id = {row["id"]: row for row in csv_rows}
    json_by_id = {row["id"]: row for row in json_rows}
    assert set(csv_by_id) == set(json_by_id)

    for claim_id in sorted(csv_by_id):
        csv_row = csv_by_id[claim_id]
        json_row = json_by_id[claim_id]
        for field in SCALAR_FIELDS:
            assert csv_row[field] == json_row[field], (claim_id, field)
        assert csv_row["supporting_artifacts"].split("|") == json_row[
            "supporting_artifacts"
        ]
        assert f"| {claim_id} |" in markdown
        assert json_row["disposition"] in markdown


def test_legacy_claim_registry_paths_are_controlled_mirrors() -> None:
    canonical_csv = _read_csv(CSV_PATH)
    legacy_csv = _read_csv(LEGACY_CSV_PATH)
    canonical_json = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    legacy_json = json.loads(LEGACY_JSON_PATH.read_text(encoding="utf-8"))
    legacy_readme = LEGACY_README_PATH.read_text(encoding="utf-8")

    assert legacy_csv == canonical_csv
    assert legacy_json == canonical_json
    assert "authoritative epistemic claim registry" in legacy_readme
    assert "docs/CLAIMS.md" in legacy_readme
    assert "must not edit the legacy mirrors independently" in legacy_readme


def test_step2_claim_dispositions_are_bounded_and_unpromoted() -> None:
    registry = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    claims = {claim["id"]: claim for claim in registry["claims"]}

    voi = claims["CLM-VOI-001"]
    assert voi["evidence_level"] == "SYNTHETIC"
    assert voi["evidence_polarity"] == "ADVERSE_MIXED"
    assert voi["disposition"] == "NOT_SUPPORTED_STEP2"
    assert "new preregistration" in voi["next_step"]

    evidence_quality = claims["CLM-EQ-001"]
    assert evidence_quality["evidence_level"] == "SYNTHETIC"
    assert evidence_quality["evidence_polarity"] == "MIXED_NARROW_POSITIVE"
    assert (
        evidence_quality["disposition"]
        == "BROAD_FORM_NOT_SUPPORTED_NARROW_ECE_SIGNAL"
    )
    assert "bounded calibration observation" in evidence_quality["next_step"]
