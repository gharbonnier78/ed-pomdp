# Step 2.1 Runtime Boundary

This increment validates only the deterministic acquisition runtime and its fairness invariants.

## Implemented

- synthetic latent system and evidence-quality states;
- identifiable and non-identifiable observation regimes;
- observable-only channel-selection policies;
- deterministic seeded execution;
- equal acquisition-cost accounting;
- matched-budget validation;
- tests preventing privileged latent-state inputs.

## Deliberately not implemented

- policy-controlled stopping;
- terminal `GO`, `NO_GO`, or `CONDITIONAL_GO` decisions;
- evidence-cost versus decision-loss trade-offs;
- unsafe-GO or unnecessary-NO-GO metrics;
- the final ED-POMDP decision-aware Value-of-Information policy.

Because all Step 2.1 acquisition actions have unit cost and episodes exhaust the assigned budget, budget equality is currently an infrastructure invariant rather than evidence of fair comparison among stopping strategies.

These capabilities belong to Step 2.2. Until then, no Step 2.1 output may be used to promote `CLM-VOI-001` or `CLM-EQ-001` above evidence level `NONE`.