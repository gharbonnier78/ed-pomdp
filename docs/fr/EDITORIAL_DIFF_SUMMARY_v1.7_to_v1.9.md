# Editorial delta summary — v1.8 to v1.9 / companion v1.0

## Structural delta

| v1.8 source | New location | Editorial status |
|---|---|---|
| Page 1 | Main guide v1.9 page 2 | Imported from v1.8 with only the version label and introductory editorial callout overlaid |
| Pages 2–30 | Main guide v1.9 pages 3–31 | Imported verbatim with `\includepdf`; no retyping or terminology edits |
| Pages 31–37, former Annex G | Advanced companion pages 3–9 | Imported verbatim with `\includepdf`; no scientific-content rewrite |
| None | Main guide v1.9 page 1 | New reading contract and first-reading glossary |
| None | Companion pages 1–2 | New autonomous cover, prerequisites and specialised glossary |

## Intended editorial rule

The correction does **not** require every concept to be defined completely at first occurrence. It follows this rule:

> The reader must be able to continue the engineering argument without mastering the full mathematical mechanism immediately.

Accordingly:

- the role of Brier, ECE, bootstrap, permutation and Holm may appear before their detailed derivation;
- `bin` receives a short explanation in the new first-reading glossary;
- `odds` is introduced there as a probabilistic cote before the formula is developed;
- repository identifiers such as `seed`, `endpoint` or policy names may be retained when needed for traceability;
- advanced estimation and policy-learning families are moved to the companion rather than expanded inside the main guide.

These terminology explanations are confined to newly generated front matter. The inherited scientific pages are not retyped or locally edited.

## Scientific invariants

The publication build preserves the inherited pages as PDF pages. The reviewer should therefore find no change to:

- the 240 confirmatory comparisons;
- the single Holm-surviving ECE contrast;
- the bootstrap interval interpretation;
- the 1,119 Brier-improving pairs and 1,054 unchanged terminal actions;
- the 94.19% mechanism diagnosis;
- unsafe-GO descriptive counts;
- the bounded dispositions of `CLM-VOI-001` and `CLM-EQ-001`;
- the distinction between probabilistic quality and decision quality.

## Reproducible publication source

The editable LaTeX sources are committed under `docs/fr/latex/`:

- `main-guide.tex` imports v1.8 page 1 with a bounded cover overlay and imports pages 2–30 verbatim;
- `companion.tex` generates two new front-matter pages and imports v1.8 pages 31–37 verbatim;
- `common.tex` contains shared formatting;
- `Makefile` documents local compilation;
- `base/ED_POMDP_En_Clair_FR_v1.8.pdf` is the validated inherited publication base.

The CI compiles both documents, verifies page counts, publishes the resulting PDFs and regenerates `SHA256SUMS`.

## Remaining review boundary

Structural and content invariance of inherited pages is established by the explicit `\includepdf` operations. A reviewer may still inspect the rendered PDFs for the visual quality and readability of the three newly generated front-matter pages and the bounded overlay on the inherited cover.
