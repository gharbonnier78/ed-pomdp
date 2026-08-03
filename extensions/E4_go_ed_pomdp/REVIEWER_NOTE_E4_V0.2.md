# Reviewer note — E4 v0.2 adaptive-governance extension

## Review purpose

This revision addresses one conceptual gap in GO-ED-POMDP v0.1:

> A goal-conditioned POMDP cannot constitute a complete governance theory if the goal, system boundary, action catalogue, observation model and hard constraints are treated as naturally given.

E4 v0.2 therefore adds a human-governed socio-technical framing and model-construction loop outside the existing belief and policy loop.

## Principal architecture change

The extension now separates:

- `phi_t`: provisional framing contract;
- `g_t`: goal contract constructed inside that framing;
- `b_t`: belief over latent system state;
- `pi`: policy operating inside the accepted boundary and constraints.

The outer loop draws on HCI, soft systems thinking and design thinking to identify stakeholders, expose conflicting viewpoints, critique boundaries, generate candidate interventions and record unresolved conflict. The inner GO-ED-POMDP loop then selects evidence, intervention, deployment or commitment actions under uncertainty.

## Adaptive-governance claim

The revision deliberately does **not** claim a mathematical guarantee of real-world success or zero loss.

The defensible claim is conditional:

> For a fixed valid framing, belief, goal, admissible action set and correctly specified model, the policy selects an admissible action that minimises expected goal-conditioned cumulative loss, exactly or approximately according to the solver.

Changing the goal, horizon, belief, constraints or action set can change the selected policy. That conditional dependence is the proposed mathematical core of adaptive governance.

## Reviewer demonstration

The document contrasts two regimes for the same proposed solution:

1. **Presales demonstration** — produce strong, honest and traceable evidence sufficient to increase buyer confidence and contract probability under a short horizon.
2. **Extreme-scale production** — sustain an illustrative `10^11` requests per hour while keeping catastrophic, data-loss, security, SLA, resilience and financial risks below governed tolerances over a long horizon.

These are represented as different framing and goal contracts, state models, action ontologies and hard constraints. They are not merely different weight vectors in one universal reward function.

The `10^11` figure is an illustrative stress scale only. No benchmark, simulation or qualification at that scale is claimed.

## Evidence boundary

No v0.1 synthetic result was rerun, tuned or reinterpreted.

The current evidence still supports only:

- narrow first-action sensitivity under budget 1;
- a narrow goal–horizon interaction;
- a narrow harm signal under deliberately wrong-goal conditioning.

It still does not support broad decision-loss superiority. The outer framing loop, reframing triggers, conditional guarantee assumptions and presales/production architecture are `NOT_TESTED` empirically.

## Requested reviewer checks

1. Is `phi_t` sufficiently separated from `g_t`, `b_t` and `pi`?
2. Is the conditional guarantee stated without implying real-world certainty, production qualification or literal zero loss?
3. Are hard production constraints correctly kept outside ordinary scalar trade-offs?
4. Are the triggers for belief update versus framing review operational enough to become falsifiable?
5. Is the use of Isabel Evans's IDEA-T work accurately attributed as a theoretical foundation rather than validation of GO-ED-POMDP?
6. Does the presales-versus-production example demonstrate goal-dependent governance without implying that the extreme throughput has been tested?
7. Are the v0.1 null and adverse findings visibly preserved?
8. Does the architecture maintain human authority over contested values, system boundaries and reframing?

## Proposed disposition

If accepted, this PR establishes a **conceptual and formal research extension only**:

- `E4-CLM-AG-001`: `FORMAL_CONDITIONAL_CLAIM; EMPIRICAL_SCOPE_NOT_TESTED`;
- `RQ-E4-F1`, `RQ-E4-F2`, `RQ-E4-F3`: `NOT_TESTED`;
- broad goal-conditioned decision-loss superiority: remains `NOT_SUPPORTED_C1`.

Approval should not authorise autonomous release decisions, industrial qualification or claims of real-world performance.
