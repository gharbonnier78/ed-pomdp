from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[1]

required = [
    "paper/main.tex",
    "paper/main.pdf",
    "paper/step2_closeout.tex",
    "paper/step2_closeout.pdf",
    "paper/step2_closeout.sha256",
    "paper/milestone2r_theory_claim_reset.tex",
    "paper/milestone2r_theory_claim_reset.pdf",
    "research_program/research_program.tex",
    "research_program/research_program.pdf",
    "reviewer/reviewer_companion.tex",
    "reviewer/reviewer_companion.pdf",
    "reviewer/guide_fr_milestone2r.tex",
    "reviewer/guide_fr_milestone2r.pdf",
    "survey/related_work.pdf",
    "ontology/evidence_ontology.pdf",
    "appendix/mathematical_appendix.pdf",
    "ontology/evidence_item.schema.json",
    "docs/CLAIMS.md",
    "docs/CLAIMS.csv",
    "docs/CLAIMS.json",
    "docs/POST_STEP2_BET_REGISTER.md",
    "roadmap/RESEARCH_TRACKS.md",
    "claims/README.md",
    "claims/claim_registry.csv",
    "claims/claim_registry.json",
    "benchmark/results/step28/STEP_2_8_CLAIM_ADJUDICATION.md",
    "benchmark/results/step28/step28_analysis_metadata.json",
    "scripts/check_current_status.py",
    "README.md",
    "CITATION.cff",
]

missing = [path for path in required if not (root / path).exists()]
if missing:
    print("Missing:", missing)
    sys.exit(1)

json.loads((root / "ontology/evidence_item.schema.json").read_text())
json.loads((root / "docs/CLAIMS.json").read_text())
json.loads((root / "claims/claim_registry.json").read_text())
json.loads(
    (root / "benchmark/results/step28/step28_analysis_metadata.json").read_text()
)

for path in [root / item for item in required if item.endswith(".pdf")]:
    if path.stat().st_size < 5000:
        print("Suspiciously small PDF", path)
        sys.exit(1)

manifest_line = (root / "paper/step2_closeout.sha256").read_text(
    encoding="utf-8"
).strip()
try:
    expected_sha256, relative_path = manifest_line.split(maxsplit=1)
except ValueError as error:
    raise SystemExit("Malformed paper/step2_closeout.sha256") from error
if relative_path != "paper/step2_closeout.pdf":
    raise SystemExit(f"Unexpected close-out manifest path: {relative_path}")
actual_sha256 = hashlib.sha256((root / relative_path).read_bytes()).hexdigest()
if actual_sha256 != expected_sha256:
    raise SystemExit(
        "Close-out PDF hash mismatch: "
        f"expected {expected_sha256}, got {actual_sha256}"
    )

print("Package check OK:", len(required), "required artifacts")
print("Step 2 close-out PDF SHA-256:", actual_sha256)
