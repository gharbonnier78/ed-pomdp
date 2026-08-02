from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "paper/milestone2r_theory_claim_reset.tex",
    "reviewer/guide_fr_milestone2r.tex",
    "docs/POST_STEP2_BET_REGISTER.md",
    "roadmap/RESEARCH_TRACKS.md",
    "research_program/research_program.tex",
]

REQUIRED_TEXT = {
    "README.md": [
        "Step 2 is closed",
        "NOT_SUPPORTED_STEP2",
        "Milestone 2R",
        "94.19%",
    ],
    "paper/main.tex": [
        "4\\times4\\times30\\times5=2{,}400",
        "Why Milestone 2R is not post-hoc goal displacement",
        "Epistemic taxonomy: why NONE becomes SYNTHETIC",
    ],
    "paper/milestone2r_theory_claim_reset.tex": [
        "4\\times 4\\times 30\\times 5=2{,}400",
        "Why Milestone 2R is not goal displacement",
        "Epistemic taxonomy: NONE to SYNTHETIC",
    ],
    "reviewer/guide_fr_milestone2r.tex": [
        "4\\times 4\\times 30\\times 5=2\\,400",
        "Pourquoi le passage à SYNTHETIC est correct",
        "Pourquoi ce pivot n'est pas une rationalisation post-hoc",
    ],
}

FORBIDDEN_ACTIVE_TEXT = {
    "README.md": ["Step 2 is the current quantitative-validation increment"],
    "research_program/research_program.tex": ["M2 & Benchmark v1"],
}

errors: list[str] = []

for relative in REQUIRED_FILES:
    if not (ROOT / relative).is_file():
        errors.append(f"Missing required Milestone 2R file: {relative}")

for relative, snippets in REQUIRED_TEXT.items():
    path = ROOT / relative
    if not path.is_file():
        errors.append(f"Missing checked file: {relative}")
        continue
    text = path.read_text(encoding="utf-8")
    for snippet in snippets:
        if snippet not in text:
            errors.append(f"Missing required status text in {relative}: {snippet}")

for relative, snippets in FORBIDDEN_ACTIVE_TEXT.items():
    path = ROOT / relative
    if not path.is_file():
        continue
    text = path.read_text(encoding="utf-8")
    for snippet in snippets:
        if snippet in text:
            errors.append(f"Outdated active wording in {relative}: {snippet}")

if errors:
    print("Current-status check failed:")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("Current-status check OK")
