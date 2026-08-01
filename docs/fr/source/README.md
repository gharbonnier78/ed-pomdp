# ED-POMDP French editorial split - reproducible publication source

This directory is the authoritative source for the French editorial split.

It does **not** claim that a monolithic LaTeX source exists for the inherited guide. The inherited publication source is the frozen PDF:

- `base/ED_POMDP_En_Clair_FR_v1.8.pdf`
- expected SHA-256: `7af6e07623b66412362c1a1c4c816b7e950d948fe36db11e4729715761162899`

The editable source is `build.py`. It generates the new front matter and performs the page-level composition transparently.

## Exact editorial operation

### Main guide v1.9

1. Generate one unnumbered first-reading/glossary page.
2. Reuse inherited v1.8 page 1 and patch only:
   - the version label;
   - the introductory callout explaining that Annex G is now separate.
3. Reuse inherited v1.8 pages 2-30 without modification.
4. Exclude inherited pages 31-37 from the main guide.

### Advanced companion v1.0

1. Generate two autonomous front-matter pages.
2. Reuse inherited v1.8 pages 31-37 without modification.

No frozen Step 2 result, formula, claim disposition, table, figure or statistical explanation is rewritten by the split.

## Build

Requirements:

- Python 3.11+
- `pypdf`
- `reportlab`
- Debian/Ubuntu package `fonts-dejavu-core`

```bash
python -m pip install -r requirements.txt
python build.py
python verify.py
```

Outputs:

- `output/ED_POMDP_En_Clair_FR_v1.9.pdf`
- `output/ED_POMDP_Belief_to_Action_Companion_FR_v1.0.pdf`

## Verification

The verification performed for this package established:

- 29/29 inherited main-guide pages after the cover are text-identical and visually identical to v1.8 pages 2-30;
- 7/7 exported Annex G pages are text-identical and visually identical to v1.8 pages 31-37;
- the main guide has 31 A4 pages;
- the companion has 9 A4 pages.

See `VERIFICATION_REPORT.md`.
