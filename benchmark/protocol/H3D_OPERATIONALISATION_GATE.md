# H3-D Operationalisation and Confirmatory Entry Gate

## Status and scope

H3-D remains a **candidate conditional hypothesis**, not a confirmatory claim. Milestone 2R may close because the falsifiability framework is now explicit. Milestone 3B may not start until the numerical thresholds, minimum group sizes, estimand, code and confirmatory seed boundary described below are frozen.

The claim under study is that decision-aware value of information provides benefit only when available evidence is heterogeneous, sufficiently discriminating, non-redundant and capable of changing a relevant decision or stopping boundary.

## Predeclared objects

Before Milestone 3A analysis, the protocol must freeze:

- the latent risk-state space and terminal action set;
- the evidence-family taxonomy;
- the provenance graph schema and dependency keys;
- the baseline family and primary loss definition;
- the development-seed set used for threshold calibration;
- the untouched confirmatory-seed set reserved for Milestone 3B.

## Measurable eligibility conditions

For an acquisition action `a`, current belief `b`, and previously observed evidence history `H`:

### 1. Provenance heterogeneity

Let `H_prov(a,H)` equal one only when all of the following preregistered graph conditions hold:

1. the candidate evidence set contains at least two distinct evidence families;
2. it contains at least two distinct generator-root nodes;
3. the corresponding dependency signatures are not identical over the frozen keys `generator`, `dataset`, `environment`, `oracle`, and `instrumentation`;
4. the graph contains no edge tagged `shared_generator=true` joining the selected roots.

The evidence-family list, graph schema, root-selection rule and dependency tags must be frozen before confirmatory data are accessed.

### 2. Discriminative power

Using natural logarithms, define the raw Jensen-Shannon divergence

`D_raw(a) = JS(P(O_a | S=good), P(O_a | S=bad))`.

`D_raw` is measured in **nats** and lies in `[0, ln 2]` for the binary risk state. The eligibility calculation uses the normalized quantity

`D(a) = D_raw(a) / ln 2`,

which lies in `[0,1]`. The condition is `D(a) >= delta_D`.

### 3. Conditional non-redundancy

Define

`U_raw(a | H) = I(S ; O_a | O_H)`

using natural logarithms, so the raw value is measured in **nats**. In the binary-state benchmark it is bounded above by the residual state entropy `H(S | O_H) <= ln 2`. To make the scale comparable across cells and future state spaces, use

`U(a | H) = U_raw(a | H) / H(S | O_H)`

when `H(S | O_H) > epsilon_H`. This normalized value lies in `[0,1]`. If the denominator is at or below `epsilon_H`, the cell is labelled `UNINFORMATIVE_BY_CONSTRUCTION` and is not eligible for H3-D. The condition is `U(a | H) >= delta_U`.

### 4. Decision-boundary reachability

Define

`B(a,b) = P_o[d*(tau(b,a,o)) != d*(b) or s*(tau(b,a,o)) != s*(b)]`,

where `d*` is the admissible terminal action, `s*` is the continue/stop decision, and `tau` is the frozen belief-update operator. `B` lies in `[0,1]`. The condition is `B(a,b) >= delta_B`.

## Frozen eligibility rule

A cell is eligible only if

`E(a,b,H) = 1[H_prov=1 and D>=delta_D and U>=delta_U and B>=delta_B]`.

The numerical values of `delta_D`, `delta_U`, `delta_B`, and `epsilon_H` may be calibrated only on new Milestone 3A development seeds. They must be justified and frozen before any Milestone 3B confirmatory seed is opened. Confirmatory retuning, relabelling or threshold relaxation is prohibited.

## Symmetric minimum-support rule

The interaction analysis is testable only when both groups meet preregistered support requirements:

- `n_eligible >= n_eligible_min`;
- `n_ineligible >= n_ineligible_min`.

Both minima must be numerical, symmetric in status, frozen before confirmation, and checked for every confirmatory comparison stratum used by the primary analysis. A highly imbalanced split, including a benchmark with almost all cells in one group, cannot be rescued by reporting only the populated subgroup.

## Confirmatory estimand

Let

`Delta_L(g) = E[L_ED-POMDP - L_baseline | E=g]`, for `g in {0,1}`.

The primary H3-D estimand is the interaction

`Delta_interaction = Delta_L(1) - Delta_L(0)`.

With lower loss preferred, H3-D requires a favourable eligible-cell effect and a negative interaction showing that the advantage is greater in eligible than in ineligible cells. The preregistration must also freeze:

- the baseline comparison family and multiplicity correction;
- total-evidence-cost comparability bounds;
- the unsafe-GO non-inferiority margin;
- effect-size thresholds and confidence or posterior criteria;
- handling of missing, structurally undefined and `UNINFORMATIVE_BY_CONSTRUCTION` cells.

## Permitted dispositions

- `SUPPORTED_STEP3B`: all preregistered confirmatory criteria pass.
- `NOT_SUPPORTED_STEP3B`: the benchmark is testable but one or more confirmatory criteria fail.
- `NOT_TESTABLE_IN_BENCHMARK`: either group fails its minimum-support rule, the eligibility variables cannot be computed under the frozen protocol, or the planned interaction is otherwise unidentified.

`NOT_TESTABLE_IN_BENCHMARK` must not be reported as evidence for or against H3-D, and it must not trigger post-hoc eligibility changes.

## Stage-gate consequence

- **Milestone 2R exit:** this operationalisation framework, its units, normalization rules, symmetric support rule, interaction estimand and non-testable disposition are documented and reviewable.
- **Milestone 3B entry:** all numerical thresholds, group minima, effect criteria, code, multiplicity rules and seed partitions are frozen after Milestone 3A development work and before confirmatory access.
