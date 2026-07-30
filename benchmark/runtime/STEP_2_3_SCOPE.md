# Step 2.3 Scope — Minimal Decision-Aware VoI Policy

## Milestone status

Step 1 and Step 1.1 are already shipped. Step 2 remains open until the preregistered matched-budget experiment, statistical analysis and synchronized claim-governance review are complete.

## Implemented in this increment

- an observable-history posterior over the four joint hypotheses `(S,E)`;
- fixed identifiable likelihoods that do not adapt to the simulator's true regime;
- one-step look-ahead expected terminal decision loss;
- acquisition-channel selection by minimum expected decision loss plus evidence cost;
- a single Bayes-optimal terminal rule derived from `LossWeights` and shared by the runner and VoI planner;
- tests for posterior semantics, channel selection, terminal-rule consistency and absence of privileged state inputs.

## Decision-rule consistency

The terminal decision executed by the episode runner and the terminal decision assumed inside VoI look-ahead are now the same function. Both minimize the configured expected loss over `GO`, `CONDITIONAL_GO` and `NO_GO`.

The earlier fixed posterior thresholds `0.20/0.80` were not derived from the asymmetric loss weights and are therefore not used by the Step 2.3 decision path. Under the default weights, for example, posterior risk `p=0.5` correctly selects `NO_GO`, because its expected loss is lower than the alternatives.

This alignment is mandatory: otherwise the acquisition policy would optimize an idealized decision-maker while the runner realized a different terminal loss.

## Deliberate limitation

In the current identifiable agent model, the functional channel informs system quality and the environment-validation channel informs evidence-production quality. The terminal loss used by this increment depends on system-release risk only. Consequently, this increment is the first executable decision-aware VoI policy for `CLM-VOI-001`, but it does not yet constitute a fair test of `CLM-EQ-001`.

A later evidence-degradation increment must make evidence quality affect observation reliability, calibration or governed release constraints before an environment-validation acquisition can have decision value. That experiment must not expose the simulator's true `E` or true regime to the policy.

## Claim boundary

No Step 2.3 unit test or smoke run may promote `CLM-VOI-001` or `CLM-EQ-001` from `NONE`. Promotion requires the complete preregistered policy matrix, at least 30 seeds per configuration, confidence intervals, robustness checks, raw results and synchronized registry updates.
