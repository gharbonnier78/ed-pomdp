# Step 2.3 Scope — Minimal Decision-Aware VoI Policy

## Milestone status

Step 1 and Step 1.1 are already shipped. Step 2 remains open until the preregistered matched-budget experiment, statistical analysis and synchronized claim-governance review are complete.

## Implemented in this increment

- an observable-history posterior over the four joint hypotheses `(S,E)`;
- fixed identifiable likelihoods that do not adapt to the simulator's true regime;
- one-step look-ahead expected terminal decision loss;
- acquisition-channel selection by minimum expected decision loss plus evidence cost;
- tests for posterior semantics, channel selection and absence of privileged state inputs.

## Deliberate limitation

In the current identifiable agent model, the functional channel informs system quality and the environment-validation channel informs evidence-production quality. The terminal loss used by this increment depends on system-release risk only. Consequently, this increment is the first executable decision-aware VoI policy for `CLM-VOI-001`, but it does not yet constitute a fair test of `CLM-EQ-001`.

A later evidence-degradation increment must make evidence quality affect observation reliability, calibration or governed release constraints before an environment-validation acquisition can have decision value. That experiment must not expose the simulator's true `E` or true regime to the policy.

## Claim boundary

No Step 2.3 unit test or smoke run may promote `CLM-VOI-001` or `CLM-EQ-001` from `NONE`. Promotion requires the complete preregistered policy matrix, at least 30 seeds per configuration, confidence intervals, robustness checks, raw results and synchronized registry updates.
