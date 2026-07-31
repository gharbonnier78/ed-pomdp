# Epistemic Governance

`docs/CLAIMS.md` is the canonical epistemic registry for this repository.

`benchmark/protocol/PREREGISTRATION.md` is the canonical Step 2 experimental preregistration.

## Rule

Papers, notes, programmes, experiments and reviewer responses reference claim IDs. They must not independently redefine a claim's maturity, evidence level, evidence polarity or disposition.

Experimental documents, scripts and reports must not independently redefine preregistered hypotheses, matched-budget rules, seeds, endpoints, exclusion rules, robustness checks or refutation criteria.

## Claim lifecycle

1. Conceptual
2. Formal proposal
3. Falsifiable hypothesis
4. Synthetic evidence
5. Industrial evidence
6. Operational evidence
7. Accepted, revised, not supported, rejected or retired

Progression is not automatic. Every transition requires an identified artifact and a recorded decision.

## Evidence type is not evidence direction

Evidence level records provenance and maturity:

- `NONE`;
- `FORMAL`;
- `SYNTHETIC`;
- `INDUSTRIAL`;
- `OPERATIONAL`.

It does not imply that evidence supports a claim. Null, adverse and mixed results still constitute evidence at the appropriate level.

Each empirically adjudicated claim therefore also records:

- `evidence_polarity`;
- `disposition`.

This prevents a failed or mixed synthetic experiment from being represented as positive claim promotion merely because its evidence level changed from `NONE` to `SYNTHETIC`.

## Required fields

Each governed claim records:

- stable ID;
- exact statement;
- type and maturity;
- current evidence level;
- evidence polarity;
- disposition;
- assumptions and dependencies;
- refutation criterion or gate;
- supporting artifacts;
- next experiment or gate;
- affected reviewer comments;
- last revision.

## Evidence levels

- `FORMAL`: definition, derivation, proof or counterexample.
- `SYNTHETIC`: controlled generated data or simulation, including null and adverse results.
- `INDUSTRIAL`: retrospective or shadow evidence from governed real data.
- `OPERATIONAL`: prospective evidence in an approved operational process.

## Machine-readable mirrors

`docs/CLAIMS.csv` and `docs/CLAIMS.json` are machine-readable mirrors of `docs/CLAIMS.md`.

The mirrors are validated in CI. They do not replace the Markdown registry and may not define a different statement, evidence level, polarity, disposition, artifact or next step.

## Confirmatory and post-hoc boundary

Frozen confirmatory outcomes govern claim promotion or non-promotion.

Post-hoc analyses may diagnose mechanisms, retain safety evidence and guide future protocols, but they may not retrospectively enlarge the confirmatory family or create an unregistered superiority claim.

The Step 2.8 mechanism analysis is therefore labelled `post_hoc_descriptive`, produces no new p-values or confidence intervals, and remains separate from the frozen Step 2.7 Holm family.

## Reviewer traceability

A reviewer comment must link to the claim, assumption, gate or document it affects. Closure requires a concrete repository change or an explicit accepted limitation.

## Anti-drift rule

When documents disagree about epistemic status, `docs/CLAIMS.md` governs.

When documents disagree about the Step 2 experimental protocol, `benchmark/protocol/PREREGISTRATION.md` governs.

`docs/PREREGISTRATION.md` is a non-normative compatibility pointer only and must not contain a duplicate protocol.

Any inconsistency is treated as a repository defect and corrected before release, execution of headline experiments or claim adjudication.
