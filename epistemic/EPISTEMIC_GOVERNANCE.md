# Epistemic Governance

`docs/CLAIMS.md` is the canonical epistemic registry for this repository.

## Rule

Papers, notes, programmes, experiments and reviewer responses reference claim IDs. They must not independently redefine a claim's maturity or evidence level.

## Claim lifecycle

1. Conceptual
2. Formal proposal
3. Falsifiable hypothesis
4. Synthetic evidence
5. Industrial evidence
6. Operational evidence
7. Accepted, revised, rejected or retired

Progression is not automatic. Every transition requires an identified artifact and a recorded decision.

## Required fields

Each governed claim records:

- stable ID;
- exact statement;
- type and maturity;
- current evidence level;
- assumptions and dependencies;
- refutation criterion;
- supporting artifacts;
- next experiment or gate;
- affected reviewer comments;
- last revision.

## Evidence levels

- `FORMAL`: definition, derivation, proof or counterexample.
- `SYNTHETIC`: controlled generated data or simulation.
- `INDUSTRIAL`: retrospective or shadow evidence from governed real data.
- `OPERATIONAL`: prospective evidence in an approved operational process.

## Reviewer traceability

A reviewer comment must link to the claim, assumption, gate or document it affects. Closure requires a concrete repository change or an explicit accepted limitation.

## Anti-drift rule

When two documents disagree, `docs/CLAIMS.md` governs epistemic status. The inconsistency is treated as a defect and corrected before release.