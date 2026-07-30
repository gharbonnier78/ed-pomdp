# Identifiability of System State and Evidence Quality

**Status:** Step 1.1 formal note. This document supports `CLM-IDENT-001` in `docs/CLAIMS.md` and does not assert empirical identifiability.

## Problem

Let `S` denote latent system condition and `E` latent evidence-production quality. Observations follow `P(O | S,E)`. The factorization is useful only if distinct values of `S` and `E` can be distinguished under stated assumptions.

## Case A — Non-identifiability

If two latent pairs induce the same observation law,

`P(O | S=s1,E=e1) = P(O | S=s2,E=e2)`,

then no amount of repeated evidence from that unchanged observation channel can separate the pairs. More observations reduce sampling error but do not repair structural aliasing.

### Worked binary counterexample

Let the only observed variable be `O ∈ {fail, pass}` and consider two different latent explanations:

- `(S=bad, E=good)`;
- `(S=good, E=bad)`.

Define the unchanged observation channel by:

`P(fail | bad,good) = 0.80`, `P(pass | bad,good) = 0.20`,

`P(fail | good,bad) = 0.80`, `P(pass | good,bad) = 0.20`.

The two rows of the observation model are identical. For any sequence containing `k` failures in `n` independent repetitions, both latent pairs assign exactly the same likelihood:

`0.80^k × 0.20^(n-k)`.

Consequently, posterior odds between the two explanations remain equal to their prior odds, regardless of the number of repetitions. This is a concrete structural non-identifiability counterexample.

## Case B — Heterogeneous evidence

Separation can become possible when channels have different sensitivity profiles. Let `F` be a functional-test channel and `V` an evidence-environment validation channel. Consider:

| Latent pair | `P(F=fail)` | `P(V=fail)` |
|---|---:|---:|
| `(S=bad, E=good)` | 0.80 | 0.20 |
| `(S=good, E=bad)` | 0.20 | 0.80 |

The channel-specific rows are now distinct. Under conditional independence given `(S,E)`, the event `(F=fail, V=pass)` has probability:

- `0.80 × 0.80 = 0.64` under `(bad,good)`;
- `0.20 × 0.20 = 0.04` under `(good,bad)`.

Conversely, `(F=pass, V=fail)` has probability `0.04` under `(bad,good)` and `0.64` under `(good,bad)`. The likelihood ratio for either asymmetric observation is therefore `16:1`, demonstrating separation in this toy model.

This does not establish identifiability for arbitrary industrial data. It establishes only that heterogeneous channels can remove the specific aliasing exhibited in Case A when their sensitivity structure is sufficiently distinct and known or estimable.

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

The worked Case A establishes a formal counterexample to unconditional identifiability. Case B gives a concrete separating construction under stated channel assumptions. Neither establishes empirical identifiability in an industrial setting. Step 2 must test identifiable, weakly identifiable and non-identifiable regimes separately.