# ED-POMDP Research Edition v1.4 — Milestone 2R

Evidence-Driven Partially Observable Markov Decision Processes for governed software-release assurance.

## Scientific status

Steps 1 and 1.1 are shipped. **Step 2 is closed** after frozen execution, independent statistical review, deterministic mechanism diagnosis, and claim adjudication.

The Step 2 benchmark evaluated seven policies over 3,360 paired episodes, four regimes, four fixed evidence budgets, and thirty untouched headline seeds. Its confirmatory family contained 240 Holm-corrected contrasts over terminal decision loss, Brier score, and expected calibration error.

The broad claims are now bounded as follows:

- `CLM-VOI-001`: `NOT_SUPPORTED_STEP2`;
- `CLM-EQ-001`: `BROAD_FORM_NOT_SUPPORTED_NARROW_ECE_SIGNAL`.

No terminal-decision-loss contrast survived Holm correction. Across the four acquisition baselines directly relevant to the VOI claim, aggregate directions were 10 favourable, 16 adverse, and 38 equal. One degraded-evidence, budget-two ECE contrast survived Holm correction, but its bootstrap interval crossed zero and posterior support was sparse.

## Principal mechanism result

ED-POMDP improved Brier score in 1,119 paired episodes. In 1,054 of those cases — **94.19%** — the terminal action remained unchanged.

> Better evidence selection can improve probabilistic belief without crossing a decision boundary, changing a stopping decision, enabling a different governed action, or reducing realised loss.

The risk-only comparison selected the same terminal action in all 480 paired episodes despite frequently different acquisition traces and posterior values.

A favourable unsafe-GO pattern remains descriptive: ED-POMDP produced zero unsafe GO decisions in the three structurally avoidable regimes, versus two per regime for the classical POMDP. This endpoint was outside the confirmatory p-value family and is not promoted retrospectively.

## Mandatory Milestone 2R

The programme does not continue as if the initial architecture had been validated. **Milestone 2R — Theory and Claim Reset** is mandatory before any new confirmatory or industrial milestone.

It:

1. reconstructs the causal chain `acquisition → observation → belief → boundary → action → loss`;
2. audits thresholds, loss ratios, fixed horizons, equal budgets, unit costs, boundary reachability, policy indistinguishability, evidence dependence, and CONDITIONAL GO semantics;
3. retires broad superiority claims and defines conditional hypotheses H3-A to H3-E;
4. freezes progression gates and seed-separation rules.

The revised central question is:

> Under which conditions does additional or better-qualified evidence change a governed engineering decision, and does that changed decision reduce a materially important loss at comparable total cost?

## Documents

### Current closure package

- [`paper/step2_closeout.pdf`](paper/step2_closeout.pdf) — frozen Step 2 results, mechanism diagnosis, and claim adjudication.
- [`paper/milestone2r_theory_claim_reset.tex`](paper/milestone2r_theory_claim_reset.tex) — English research-level Milestone 2R paper.
- [`reviewer/guide_fr_milestone2r.tex`](reviewer/guide_fr_milestone2r.tex) — complete French explanatory companion.
- [`paper/main.tex`](paper/main.tex) — current scientific overview after Step 2.
- [`research_program/research_program.tex`](research_program/research_program.tex) — revised 2026–2030 programme.
- [`docs/POST_STEP2_BET_REGISTER.md`](docs/POST_STEP2_BET_REGISTER.md) — revised bets P0–P5 and candidate hypotheses H3-A–H3-E.
- [`roadmap/RESEARCH_TRACKS.md`](roadmap/RESEARCH_TRACKS.md) — gated post-Step-2 roadmap.
- [`docs/CLAIMS.md`](docs/CLAIMS.md) — canonical epistemic claim registry.

The GitHub Actions workflow compiles the English paper, French guide, current overview, revised programme, and foundation documents, then publishes them in the **`ed-pomdp-v1.4-documents` workflow artifact**. Generated PDFs that would otherwise become stale are not treated as authoritative unless reproduced by CI. The committed deterministic `step2_closeout.pdf` remains governed by its SHA-256 manifest.

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
