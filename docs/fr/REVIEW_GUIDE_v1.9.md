# Independent editorial review guide — French pedagogical companions

## Review status

This change set is submitted as a **draft editorial review package**. No reviewer is requested and no merge is requested before the two authoritative PDF binaries are present and independently checked.

The review concerns two French-only pedagogical documents derived from the frozen Step 2 close-out:

1. `ED_POMDP_En_Clair_FR_v1.9.pdf` — main guide, 31 pages;
2. `ED_POMDP_Belief_to_Action_Companion_FR_v1.0.pdf` — advanced companion, 9 pages.

The root README contains two quick-link buttons explicitly labelled **FR only**. During draft preparation those links target the final repository paths below. Reviewer hand-off starts only after the binaries at those paths match `SHA256SUMS`.

The PDF files are the authoritative review artifacts. Plain-text extractions may be added later to support line-level comments, but they are not publication sources.

## Editorial objective

Preserve the guide's decision-centred narrative without turning it into a universal mathematics course.

The intended pedagogy is spiral:

1. a notion is first encountered through its role in the reasoning;
2. its effect is observed in the Step 2 results;
3. its mechanism is explained later in the annexes;
4. a second reading should produce a more precise understanding.

A term therefore does not need a complete definition at its first occurrence. A short local translation is required only when the term itself would block the argument.

## Changes submitted for review

### Main guide v1.9

- keeps the main narrative and Annexes A–F;
- adds a one-page reading contract and first-reading glossary;
- introduces short local translations for selected statistical and repository terms;
- explains scalarisation locally without adding a preliminary optimisation course;
- removes the former Annex G from the main guide.

### Advanced companion v1.0

- carries the former Annex G as a separate advanced document;
- adds an autonomous cover, prerequisites and a specialised French glossary;
- preserves the scientific content and the technical names used by the repository or literature.

## Page mapping against v1.7

The main guide contains one new preliminary page followed by the former pages 1–30, with local editorial revisions on a limited set of pages.

- v1.9 page 1: new reading contract and glossary;
- v1.9 pages 2–31: correspond to v1.7 pages 1–30;
- former v1.7 pages 31–37 move to companion pages 3–9;
- companion pages 1–2 are new cover and terminology pages.

## Review questions

Please verify independently:

1. **Narrative preservation** — do mathematical and statistical tools remain subordinate to the engineering decision problem?
2. **Local accessibility** — are terms translated only where their unexplained use would interrupt the reasoning?
3. **No over-teaching** — does the new front matter avoid becoming a prerequisite course?
4. **Scientific invariance** — has the split changed no Step 2 result, claim disposition, number, formula or epistemic boundary?
5. **Companion boundary** — is the former Annex G genuinely separable because it opens the estimation-to-policy research direction?
6. **Cross-document continuity** — is it clear when and why a reader should move from the main guide to the advanced companion?
7. **Terminology** — are French expressions preferred without obscuring canonical English terms from statistics, software engineering or the repository?
8. **Visual integrity** — are page breaks, formulas, tables, headings and cross-references readable and coherent?

## Explicit non-scope

This PR does not:

- alter the frozen Step 2 benchmark, raw data, statistical analysis or hashes;
- reopen `CLM-VOI-001` or `CLM-EQ-001`;
- introduce log-loss or any new evaluation metric;
- claim that the guide is a universal probability, statistics, operations-research or reinforcement-learning course;
- request publication or merge before review closure.

## Merge gate

The PR must remain draft until all of the following are satisfied:

- both authoritative PDF binaries are committed at the README quick-link paths;
- `sha256sum -c docs/fr/SHA256SUMS` passes;
- independent editorial review is completed;
- blocking comments are resolved or explicitly adjudicated;
- editable publication sources are committed, or their absence is explicitly accepted as a bounded artifact-only release decision;
- final rendered pages are inspected;
- all repository checks are green.

Auto-merge must remain disabled.
