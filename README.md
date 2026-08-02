# ED-POMDP Research Edition v1.4 — Milestone 2R

Evidence-Driven Partially Observable Markov Decision Processes for governed software-release assurance.

<p align="center">
  <a href="./paper/main.pdf"><img src="https://img.shields.io/badge/Open-Main%20Paper-0B5FFF?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Open Main Paper PDF"></a>
  <a href="./paper/step2_closeout.pdf"><img src="https://img.shields.io/badge/Open-Step%202%20Close--Out-8E24AA?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Open Step 2 Close-Out PDF"></a>
  <a href="./identifiability/identifiability_note.pdf"><img src="https://img.shields.io/badge/Open-Identifiability%20Note-6A1B9A?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Open Identifiability Note PDF"></a>
</p>

<p align="center">
  <a href="./research_program/research_program.pdf"><img src="https://img.shields.io/badge/Open-Research%20Programme-00695C?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Open Research Programme PDF"></a>
  <a href="./survey/related_work.pdf"><img src="https://img.shields.io/badge/Open-Related%20Work-455A64?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Open Related Work PDF"></a>
  <a href="./reviewer/reviewer_companion.pdf"><img src="https://img.shields.io/badge/Open-Reviewer%20Companion-B71C1C?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Open Reviewer Companion PDF"></a>
</p>

<p align="center">
  <a href="./docs/fr/ED_POMDP_En_Clair_FR_v1.9.pdf"><img src="https://img.shields.io/badge/FR%20only-Guide%20ED--POMDP%20en%20clair-1565C0?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Open French-only ED-POMDP plain-language guide PDF"></a>
  <a href="./docs/fr/ED_POMDP_Belief_to_Action_Companion_FR_v1.0.pdf"><img src="https://img.shields.io/badge/FR%20only-Companion%20croyance%20vers%20action-6A1B9A?style=for-the-badge&logo=adobeacrobatreader&logoColor=white" alt="Open French-only belief-to-action advanced companion PDF"></a>
</p>
<p align="center"><sub>French-only pedagogical documents passed through the separate editorial review gate in PR #11.</sub></p>

## Scientific status

Steps 1 and 1.1 are shipped. **Step 2 is closed** after frozen execution, independent statistical review, deterministic mechanism diagnosis, and claim adjudication.

The Step 2 benchmark produced **3,360 policy-episode rows**:

`4 regimes × 4 budgets × 30 untouched headline seeds × 7 policies = 3,360`.

Its confirmatory family contained 240 Holm-corrected contrasts over terminal decision loss, Brier score, and expected calibration error.

The broad claims are bounded as follows:

- `CLM-VOI-001`: `NOT_SUPPORTED_STEP2`;
- `CLM-EQ-001`: `BROAD_FORM_NOT_SUPPORTED_NARROW_ECE_SIGNAL`.

No terminal-decision-loss contrast survived Holm correction. Across the four acquisition baselines directly relevant to the VOI claim, aggregate directions were 10 favourable, 16 adverse, and 38 equal. One degraded-evidence, budget-two ECE contrast survived Holm correction, but its bootstrap interval crossed zero and posterior support was sparse.

## Principal mechanism result

The deterministic Step 2.8 diagnosis produced **2,400 ED-POMDP-versus-baseline paired records**:

`4 regimes × 4 budgets × 30 seeds × 5 confirmatory baselines = 2,400`.

ED-POMDP improved Brier score in 1,119 pairs. In 1,054 of those cases — **94.19%** — the terminal action remained unchanged.

> Better evidence selection can improve probabilistic belief without crossing a decision boundary, changing a stopping decision, enabling a different governed action, or reducing realised loss.

The risk-only comparison selected the same terminal action in all 480 paired episodes despite frequently different acquisition traces and posterior values.

A favourable unsafe-GO pattern remains descriptive: ED-POMDP produced zero unsafe GO decisions in the three structurally avoidable regimes, versus two per regime for the classical POMDP. This endpoint was outside the confirmatory p-value family and is not promoted retrospectively.

## Evidence level does not mean support

The move from `NONE` to `SYNTHETIC` records that a frozen synthetic benchmark now exists. It does **not** promote either claim.

The repository keeps three fields separate:

- evidence level: source class of adjudicating evidence;
- evidence polarity: supportive, mixed, adverse, or untested;
- disposition: active, narrowed, unsupported, blocked, or deferred.

For `CLM-VOI-001`, the correct combination is synthetic evidence, adverse/mixed polarity, and `NOT_SUPPORTED_STEP2`.

## Mandatory Milestone 2R

The programme does not continue as if the initial architecture had been validated. **Milestone 2R — Theory and Claim Reset** is mandatory before any new confirmatory or industrial milestone.

It:

1. reconstructs `acquisition → observation → belief → boundary/stopping → action → loss`;
2. audits thresholds, loss ratios, fixed horizons, equal budgets, unit costs, boundary reachability, policy indistinguishability, evidence dependence, and CONDITIONAL GO semantics;
3. retires broad superiority claims and defines conditional hypotheses H3-A to H3-E;
4. freezes progression gates and seed-separation rules.

This is not a post-hoc replacement of a failed claim with a positive narrative. The original claims remain visible and unsupported; the new hypotheses are narrower and require a new preregistration, new development seeds, and untouched confirmatory seeds.

The revised central question is:

> Under which conditions does additional or better-qualified evidence change a governed engineering decision, and does that changed decision reduce a materially important loss at comparable total cost?

## Documents in this PR

- [`paper/milestone2r_theory_claim_reset.tex`](paper/milestone2r_theory_claim_reset.tex) — English research-level Milestone 2R paper.
- [`reviewer/guide_fr_milestone2r.tex`](reviewer/guide_fr_milestone2r.tex) — complete French explanatory companion.
- [`paper/main.tex`](paper/main.tex) — current scientific overview after Step 2.
- [`research_program/research_program.tex`](research_program/research_program.tex) — revised 2026–2030 programme.
- [`reviewer/reviewer_companion.tex`](reviewer/reviewer_companion.tex) — post-Step-2 reviewer response and approval boundary.
- [`docs/POST_STEP2_BET_REGISTER.md`](docs/POST_STEP2_BET_REGISTER.md) — revised bets P0–P5 and candidate hypotheses H3-A–H3-E.
- [`benchmark/protocol/H3D_OPERATIONALISATION_GATE.md`](benchmark/protocol/H3D_OPERATIONALISATION_GATE.md) — measurable H3-D eligibility, normalization, symmetric support, interaction estimand, and 3B entry gate.
- [`roadmap/RESEARCH_TRACKS.md`](roadmap/RESEARCH_TRACKS.md) — gated post-Step-2 roadmap.
- [`scripts/check_current_status.py`](scripts/check_current_status.py) — anti-drift status guard.
- [`paper/step2_closeout.pdf`](paper/step2_closeout.pdf) — committed frozen Step 2 close-out, governed by SHA-256.

The two new PDFs are generated by GitHub Actions from the LaTeX sources and published in the **`ed-pomdp-v1.4-documents` workflow artifact**:

- `paper/milestone2r_theory_claim_reset.pdf`;
- `reviewer/guide_fr_milestone2r.pdf`.

Generated PDFs are not described as committed repository files unless they are actually committed. The deterministic `step2_closeout.pdf` remains the only PDF governed by its committed SHA-256 manifest.

The French editorial documents merged in PR #11 remain published separately under `docs/fr/` and are not modified by Milestone 2R.

`benchmark/results/STEP_2_7_EXECUTIVE_STATUS_NOTE.tex` is retained as a historical Step 2.7 snapshot. Final claim status is governed by the Step 2 close-out and canonical registry.

## Revised roadmap

- **Milestone 2R** — theory and claim reset;
- **Milestone 3A** — exploratory mechanism benchmark using new development seeds only, with no confirmatory claim;
- **Milestone 3B** — new preregistered benchmark centred on weighted terminal loss, unsafe GO, and total evidence cost;
- **Milestone 4** — realistic STRAT-Q scenarios with heterogeneous costs, correlated evidence, OTEL, compensating controls, governed provenance, and project-specific loss;
- **Milestone 5** — retrospective and shadow industrial evaluation, gated by data readiness and prior bounded validation.

## Anti-leakage rules

- Step 2 headline seeds remain immutable historical evidence and may not become a tuning set.
- Exploratory redesign uses new development seeds.
- New confirmatory seeds remain untouched until protocol and analysis code are frozen.
- Brier and ECE remain secondary mechanism diagnostics, not substitutes for decision value.
- The industrial pilot must not be used to rescue an unstable theory.

## Build and verification

```bash
make all
make check
python -m pytest -q benchmark/tests
python -m benchmark.analysis.analyze_step28_mechanisms --output-dir /tmp/step28
```

CI pins Python `3.12.13` and `pytest 9.1.1`, verifies the deterministic Step 2 close-out PDF, compiles the active LaTeX corpus, checks current-status wording, and publishes the document bundle.

## Citation

See [`CITATION.cff`](CITATION.cff).
