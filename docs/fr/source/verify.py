#!/usr/bin/env python3
"""Mechanical verification of the conservative editorial split."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
BASE = ROOT / "base" / "ED_POMDP_En_Clair_FR_v1.8.pdf"
MAIN = ROOT / "output" / "ED_POMDP_En_Clair_FR_v1.9.pdf"
COMP = ROOT / "output" / "ED_POMDP_Belief_to_Action_Companion_FR_v1.0.pdf"
EXPECTED_BASE = "7af6e07623b66412362c1a1c4c816b7e950d948fe36db11e4729715761162899"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalized_text(page) -> str:
    text = page.extract_text() or ""
    text = text.replace("\u00ad", "").replace("\xa0", " ")
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or re.fullmatch(r"\d+", stripped):
            continue
        lines.append(stripped)
    return re.sub(r"\s+", " ", " ".join(lines)).strip()


def main() -> None:
    assert sha256(BASE) == EXPECTED_BASE, "base v1.8 hash mismatch"
    base = PdfReader(str(BASE))
    main_doc = PdfReader(str(MAIN))
    comp = PdfReader(str(COMP))

    assert len(base.pages) == 37
    assert len(main_doc.pages) == 31
    assert len(comp.pages) == 9

    for base_idx in range(1, 30):
        main_idx = base_idx + 1
        assert normalized_text(base.pages[base_idx]) == normalized_text(main_doc.pages[main_idx]), (
            f"main inherited page mismatch: base {base_idx + 1}, main {main_idx + 1}"
        )

    for base_idx in range(30, 37):
        comp_idx = base_idx - 28
        assert normalized_text(base.pages[base_idx]) == normalized_text(comp.pages[comp_idx]), (
            f"companion inherited page mismatch: base {base_idx + 1}, companion {comp_idx + 1}"
        )

    print("PASS: page counts")
    print("PASS: 29/29 inherited main pages text-identical")
    print("PASS: 7/7 former Annex G pages text-identical")
    print(f"main_sha256={sha256(MAIN)}")
    print(f"companion_sha256={sha256(COMP)}")


if __name__ == "__main__":
    main()
