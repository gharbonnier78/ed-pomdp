# Post-Step-2 Bet Register

This register complements `docs/CLAIMS.md`. It records the programme-level bets that must be revised before any new confirmatory or industrial milestone.

## Counting boundary

- Raw Step 2 episodes: `4 regimes × 4 budgets × 30 seeds × 7 policies = 3,360`.
- Step 2.8 paired mechanism diagnostics: `4 regimes × 4 budgets × 30 seeds × 5 confirmatory baselines = 2,400`.
- Brier-improving pairs: `1,119`.
- Brier-improving pairs with unchanged terminal action: `1,054`, or `94.19%`.

The 3,360 rows are executed policy episodes. The 2,400 rows are ED-POMDP-versus-baseline paired diagnostics.

## Revised bets

| ID | Bet | Status after Step 2 | Programme decision |
|---|---|---|---|
| P0 | System risk and evidence-production quality should be represented separately. | Not invalidated; no operational-gain proof. | Retain as a modelling hypothesis. |
| P1 | Decision-aware VOI generally improves decisions at equal evidence budget. | Not supported. | Withdraw the broad form. |
| P2 | Explicit evidence-quality modelling generally improves calibration and terminal decisions. | Broad form not supported. | Decompose into narrower conditional claims. |
| P3 | Better calibration naturally converts into better terminal action. | Contradicted by the observed mechanism. | Withdraw as an implicit assumption. |
| P4 | Benefit depends on the joint coupling of belief, thresholds, loss, stopping, compensating control, and action. | New mechanism hypothesis. | Test explicitly after Milestone 2R. |
| P5 | Evidence-quality awareness may reduce dangerous release actions. | Descriptive signal only. | Pre-register a dedicated safety endpoint. |

## Candidate conditional hypotheses

### H3-A — Joint terminal decision

A terminal rule using both `P(S=bad)` and the belief over evidence quality reduces weighted terminal loss under degraded evidence relative to a risk-only terminal rule.

### H3-B — Adaptive stopping

An adaptive acquisition policy reduces mean evidence cost without increasing terminal loss or unsafe-GO rate.

### H3-C — Governed CONDITIONAL GO

A CONDITIONAL GO action linked to explicit, verifiable compensating controls reduces loss relative to an unstructured intermediate decision region.

### H3-D — Conditional value of information

VOI provides benefit only when available evidence is heterogeneous, sufficiently discriminating, non-redundant, and capable of crossing a relevant decision boundary.

#### H3-D falsifiability and operationalisation gate

H3-D is not eligible for confirmatory testing until all four qualifiers are computed under a frozen rule:

- provenance heterogeneity from a preregistered evidence-family taxonomy and dependency graph;
- normalized Jensen-Shannon discrimination `D = JS / ln(2)` in `[0,1]`, with the raw value retained in nats;
- normalized conditional information gain `U = I(S;O_a|O_H) / H(S|O_H)` in `[0,1]`, with the raw value retained in nats and low-residual-entropy cells marked `UNINFORMATIVE_BY_CONSTRUCTION`;
- decision-boundary reachability `B`, the predictive probability that acquisition changes the admissible terminal action or continue/stop decision.

A cell is eligible only when `H_prov=1`, `D>=delta_D`, `U>=delta_U`, and `B>=delta_B`. Thresholds may be calibrated only on new Milestone 3A development seeds and must be frozen before any Milestone 3B confirmatory seed is opened. Retuning or relabelling after confirmatory access is prohibited.

The primary estimand is the eligibility-by-policy interaction, not an eligible-only subgroup effect. The preregistration must freeze numerical minimum counts for **both** eligible and ineligible cells. If either group is undersized, H3-D is `NOT_TESTABLE_IN_BENCHMARK`, not supported or refuted. Full definitions are governed by [`benchmark/protocol/H3D_OPERATIONALISATION_GATE.md`](../benchmark/protocol/H3D_OPERATIONALISATION_GATE.md).

### H3-E — Safety

Evidence-quality-aware terminal rules reduce unsafe-GO rate under controlled evidence degradation at comparable total evidence cost.

These are candidate hypotheses. They are not confirmatory claims until estimands, effect thresholds, multiplicity, failure criteria, protocol, code, and untouched seeds are frozen.

## Epistemic taxonomy

Evidence level records the **source class of adjudicating evidence**, not whether the claim is supported.

- `NONE`: no adjudicating evidence.
- `FORMAL`: definition, derivation, proof, or counterexample.
- `SYNTHETIC`: controlled generated evidence or simulation, including adverse or null evidence.
- `INDUSTRIAL`: governed retrospective or shadow evidence from real releases.
- `OPERATIONAL`: approved prospective operational evidence.

After Step 2, retaining `NONE` would be incorrect because a frozen synthetic benchmark exists. `SYNTHETIC` does not imply positive support. Evidence polarity and claim disposition remain separate fields in `docs/CLAIMS.md`.

## Anti-leakage rules

1. Step 2 headline seeds remain immutable historical evidence and may not become a tuning set.
2. Milestone 3A uses new development seeds only.
3. Milestone 3B uses untouched confirmatory seeds after protocol and analysis freeze.
4. Brier and ECE remain secondary mechanism diagnostics, not substitutes for decision value.
5. A pilot or industrial replay must not be used to rescue an unstable theory.
6. Simple governed baselines remain first-class comparators.
