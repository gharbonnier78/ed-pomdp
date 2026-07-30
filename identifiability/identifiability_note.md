# Identifiability of System State and Evidence Quality

**Status:** Step 1.1 formal note. This document supports `CLM-IDENT-001` in `docs/CLAIMS.md` and does not assert empirical identifiability.

## Problem

Let `S` denote latent system condition and `E` latent evidence-production quality. Observations follow `P(O | S,E)`. The factorization is useful only if distinct values of `S` and `E` can be distinguished under stated assumptions.

## Case A — Non-identifiability

If two latent pairs induce the same observation law,

`P(O | S=s1,E=e1) = P(O | S=s2,E=e2)`,

then no amount of repeated evidence from that unchanged observation channel can separate the pairs. More observations reduce sampling error but do not repair structural aliasing.

## Case B — Heterogeneous evidence

Separation can become possible when channels have different sensitivity profiles. For example, a functional test may be primarily sensitive to `S`, while an environment validation probe is primarily sensitive to `E`. Joint observations can then distinguish pairs that one channel alone aliases.

A minimal sufficient design requirement is that the joint observation map over the candidate latent states has distinct rows, up to the equivalence class relevant to the decision.

## Case C — Controlled intervention

Changing an evidence-production condition while holding the build nominally fixed can increase information about `E`. In practice, the system is not perfectly invariant between runs. Flakiness, timing, load, hidden state and environmental drift introduce an intervention noise floor `epsilon_drift`.

Therefore the intervention identifies `E` only relative to an explicit stability assumption and only above that noise floor. Repeated paired runs, randomized order, invariant checks and nuisance-variable logging are required before attributing an observation change to `E`.

## Consequence for assurance design

Identifiability comes from experimental structure, not evidence volume alone. This provides a principled reason to include:

- environment smoke tests;
- observability and oracle validation;
- heterogeneous evidence channels;
- paired cross-environment execution;
- controlled interventions with nuisance logging.

## Current conclusion

The S/E factorization is formally meaningful, but empirical identifiability is not established. Step 2 must test identifiable, weakly identifiable and non-identifiable regimes separately.