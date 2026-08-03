# E4 v0.2 — Socio-technical framing and adaptive governance

## 1. Purpose

GO-ED-POMDP v0.1 made the goal contract explicit, but still began after most of the difficult governance work had already occurred. It received a goal, system boundary, action catalogue, observation model and constraints, then selected evidence or intervention actions inside that model.

E4 v0.2 adds the missing outer layer:

> The goal, boundary, state representation, admissible actions and observations are provisional modelling products constructed by people situated within the organisation and the governed system.

The resulting architecture contains two nested loops:

1. an outer socio-technical framing and model-construction loop;
2. the inner GO-ED-POMDP belief and decision loop.

The update does not modify the v0.1 simulator or synthetic results.

---

## 2. Theoretical foundation and attribution boundary

Isabel Evans's 2026 doctoral dissertation, *A framework to support test tool design and acquisition*, studies testers and tools in an increasingly complex socio-technical environment and applies an HCI lens to tool design and acquisition. The work proposes the empirically grounded IDEA-T framework following interviews, workshops, surveys, case studies and expert review.

Stable source record:

`https://www.um.edu.mt/library/oar/handle/123456789/144337`

E4 uses that work as a foundation for recognising that testers, tools, technologies, organisational maturity and quality viewpoints belong inside the system being governed rather than outside it as neutral observers.

For this extension, that foundation is combined with:

- **human-computer interaction**, to investigate people, work, goals and quality in use;
- **soft systems thinking**, to preserve multiple viewpoints, contested purposes and system-boundary critique;
- **design thinking**, to generate and prototype candidate interventions rather than assuming a closed action catalogue.

This synthesis is an E4 research proposal. It is not presented as a result validated by Evans, and IDEA-T has not been experimentally validated as an outer loop for GO-ED-POMDP.

---

## 3. Framing contract before goal contract

The outer loop produces a provisional framing contract:

```text
phi_t = <
    stakeholders,
    viewpoints,
    authority_structure,
    system_boundary,
    concerns,
    assumptions,
    time_horizons,
    action_ontology,
    observation_ontology,
    hard_constraints,
    unresolved_conflicts,
    provenance,
    reopening_triggers
>
```

The goal contract is then constructed within that framing:

```text
g_t = GoalContract(phi_t)
```

A compact goal contract remains:

```text
g_t = <
    stakeholders,
    target,
    horizon,
    loss,
    constraints,
    sufficiency,
    update_triggers
>
```

The distinction is essential:

- `phi_t` defines which world and decision problem are currently represented;
- `g_t` defines the provisional target and decision semantics inside that representation;
- `b_t` represents uncertainty about the latent state;
- `pi` selects an admissible action inside those temporary boundaries.

Multiple viewpoints must not be reduced prematurely to an additive expression such as:

```text
0.4 customer + 0.3 investor + 0.2 team + 0.1 regulator
```

A viewpoint may instead be recorded as:

```text
accepted
contested
excluded_with_justification
unresolved
unknown
```

Scalarisation is a modelling choice made after disagreement, authority and exclusions have been made visible. It is not a substitute for understanding them.

---

## 4. Two nested adaptation loops

```text
People, roles, incentives, technologies, history and context
                              |
                              v
     Socio-technical framing and model-construction loop
     HCI + soft systems thinking + design thinking
     ----------------------------------------------------
     * identify affected and decision-authorised stakeholders
     * elicit goals, concerns and quality viewpoints
     * expose disagreements, incentives and assumptions
     * critique the system boundary and time horizon
     * generate candidate interventions and evidence actions
     * establish observations, sufficiency rules and constraints
     * record exclusions and unresolved conflicts
     * produce provisional framing contract phi_t
                              |
                              v
                 Provisional goal contract g_t
                              |
                              v
                       GO-ED-POMDP
     ----------------------------------------------------
     * maintain belief b_t under uncertainty
     * compare evidence, intervention and commitment actions
     * enforce non-compensatory constraints
     * select an accountable action
                              |
                              v
                Observations and consequences
                              |
                +-------------+-------------+
                |                           |
                v                           v
       ordinary belief update       framing challenge
       b_t -> b_t+1                  phi_t -> framing review
```

This produces two forms of adaptation:

1. **belief and policy adaptation**, inside the GO-ED-POMDP decision loop;
2. **framing, boundary and goal adaptation**, through human-centred governance.

### 4.1 Inner-loop update

Remain inside the current framing when an observation:

- changes the estimated technical or operational state;
- changes belief about evidence quality;
- changes expected action value;
- reveals a known failure mode;
- remains explainable by the current state and observation models.

### 4.2 Outer-loop reopening

Reopen `phi_t` when evidence indicates that:

- a materially affected stakeholder was omitted;
- declared and effective organisational incentives conflict;
- a consequential effect lies outside the selected boundary or horizon;
- no admissible action addresses the observed problem;
- an intervention creates a new class of complexity or exposure;
- the observation model systematically misses consequential behaviour;
- stakeholders attach incompatible meanings to the same quality measure;
- repeated policy infeasibility suggests that the represented decision problem is not actionable;
- the provenance or authority of the goal contract is no longer valid.

A conceptual transition is:

```text
if frame_challenge(y_t, history_t, phi_t) == false:
    b_t+1 = BayesianUpdate(b_t, y_t, phi_t)
    phi_t+1 = phi_t
else:
    suspend or constrain policy execution
    initiate governed reframing
    phi_t+1 = Reframe(phi_t, y_t, stakeholders)
```

Reframing remains human-governed. The model may signal that the framing should be reviewed, but it must not silently decide whose values have authority or redefine acceptable risk.

---

## 5. Formal adaptive-governance statement

The operative model is conditional on the framing contract:

```text
M_GO(phi_t) = <
    X_phi,
    G_phi,
    A_phi,
    O_phi,
    T_phi,
    Z_phi,
    L_g,
    gamma,
    K_phi,g,
    Pi_phi
>
```

The policy becomes:

```text
pi(a_t | b_t, phi_t, g_t, h_t, K_phi,g)
```

For a fixed framing, goal, belief and horizon, the optimal policy is:

```text
pi*_(phi,g) = argmin_pi E_pi[
    terminal_loss_g
  + evidence_cost
  + delay_cost
  + intervention_cost
  + operational_exposure
  | b_t, phi_t, g_t
]
```

subject to:

```text
pi in Pi_admissible(phi_t, g_t)
```

and hard constraints:

```text
K_phi,g(b_t, history_t, provenance_t) <= 0
```

Hard constraints are not converted into arbitrarily large scalar penalties. They define the admissible policy set.

### 5.1 What is mathematically guaranteed

Under a fixed and auditable framing, finite action set, stated solver assumptions and correctly specified transition, observation and loss models:

> The selected policy is admissible and minimises expected cumulative goal-conditioned loss, exactly or approximately according to the solver.

When the goal, horizon, constraints, belief or admissible actions change, the optimal policy may change. This conditional dependence is the mathematical core of adaptive governance.

### 5.2 What is not guaranteed

The formalism does not guarantee that:

- the real world matches the transition or observation model;
- every failure mode was identified;
- the stakeholder goal is legitimate;
- the system boundary is complete;
- the action catalogue contains the required intervention;
- observations are calibrated and decision-sufficient;
- zero loss is physically achievable;
- an extreme-scale production system will never fail.

The guarantee is therefore model-relative, not an unconditional guarantee over the real socio-technical system.

---

## 6. Demonstration: contract-winning demo versus extreme-scale production

The same proposed solution can rationally require different governance policies because the goal contract and framing are different.

### 6.1 Regime A — strong presales demonstration

A possible goal contract is:

```text
g_demo = <
    buyer confidence,
    probability of contract award,
    short decision horizon,
    bounded demonstration cost,
    credibility and non-misrepresentation constraints
>
```

Relevant actions may include:

- focused prototype;
- benchmark of the critical path;
- simulation of future load;
- representative end-to-end flow;
- observability and recovery demonstration;
- customer workshop or user pilot;
- independent technical review.

A narrow and convincing demonstration can be rational because its principal expected value is:

```text
contract confidence
- demonstration cost
- risk of misleading claims
```

Mandatory constraints include:

- no fabricated evidence;
- no unsupported extrapolation;
- explicit separation between demonstrated and projected capacity;
- traceability of assumptions;
- no representation of a prototype as production qualification.

### 6.2 Regime B — production at illustrative scale `10^11` requests per hour

The operative goal is fundamentally different:

```text
g_prod = <
    continuous service,
    bounded financial and operational loss,
    long horizon,
    resilience and recoverability,
    legal, safety, security and data-integrity constraints
>
```

The latent state may need to include:

- capacity margin;
- queue saturation;
- correlated failure risk;
- data-loss probability;
- fraud and security exposure;
- dependency health;
- geographic degradation;
- recovery capability;
- observability completeness;
- traffic and workload drift.

Relevant actions may include:

- shadow deployment;
- progressive traffic increase;
- canary release;
- regional isolation;
- capacity expansion;
- back-pressure or load shedding;
- rollback;
- disaster-recovery activation;
- resilience experiment;
- release freeze;
- human escalation.

A simplified loss decomposition is:

```text
L_prod =
    C_outage
  + C_data_loss
  + C_fraud
  + C_SLA_breach
  + C_reputation
  + C_operation
```

Some conditions are non-compensatory:

```text
P(catastrophic_loss | b_t, a_t) <= epsilon
P(irrecoverable_data_loss | b_t, a_t) <= delta
throughput(a_t) >= R_min
recovery_time(a_t) <= RTO_max
```

Among admissible actions:

```text
a*_t = argmin_(a in K_production) E[L_prod | b_t, a]
```

The production objective is not literally “no loss.” It is to keep loss and catastrophic-risk probabilities below explicitly governed tolerances while sustaining required service.

### 6.3 Adaptive-governance conclusion

> Winning a contract through a strong but honest demonstrator and operating a massive production system with near-zero tolerated loss are different goal contracts, state models, evidence requirements, admissible actions, loss structures and governance policies.

The same action may be:

- valuable in one context;
- wasteful in another;
- inadmissible in a third.

A user pilot may be decisive for desirability or buyer confidence but insufficient for extreme-scale resilience. A multi-region disaster-recovery exercise may be essential before production and economically unjustified for an early commercial demonstration.

Adaptive governance is therefore not a universally heavier process. It is governance whose evidence burden, intervention set, constraints and decision policy are conditioned on the situated goal and risk.

---

## 7. New research questions

### RQ-E4-F1 — Framing construction

Can a human-centred socio-technical process produce an auditable framing contract containing stakeholders, boundaries, assumptions, actions, observations, constraints and unresolved conflicts?

### RQ-E4-F2 — Reframing triggers

Can observable and reviewable criteria distinguish ordinary belief updates from evidence that the decision framing itself is inadequate?

### RQ-E4-F3 — Boundary and goal sensitivity

How sensitive are selected policies and estimated decision values to plausible alternative system boundaries, stakeholder viewpoints, horizons and authority structures?

These questions are `NOT_TESTED` in the current package.

---

## 8. New conditional claim

| Claim ID | Claim | Gate | Status |
|---|---|---|---|
| `E4-CLM-AG-001` | Under a fixed valid framing and model, the selected policy is admissible and minimises expected goal-conditioned loss; changing the goal contract can change the policy. | Formal proof or solver verification under stated assumptions, plus a goal-regime counterexample. | `FORMAL_CONDITIONAL_CLAIM; EMPIRICAL_SCOPE_NOT_TESTED` |

This claim does not promote the synthetic result and does not establish industrial effectiveness.

---

## 9. Evidence boundary

The v0.1 synthetic experiment used:

- externally specified synthetic goals;
- a fixed system boundary;
- a fixed action ontology;
- a fixed observation model;
- three simplified goal profiles;
- budgets of one and two actions.

It evaluated only the inner loop.

The correct interpretation remains:

> Given externally specified synthetic goal profiles, a fixed boundary and a fixed action ontology, explicit goal conditioning changed the first evidence action in a narrow budget-one case, but did not demonstrate broad decision-loss superiority.

The outer framing loop, reframing criteria and presales-versus-production demonstration are theoretically grounded extensions to be tested separately. They are not retroactive explanations or validation of the held-out synthetic results.

---

## 10. Additional non-claims

E4 v0.2 does not establish that:

- the correct stakeholders or system boundary can be discovered automatically;
- stakeholder disagreements can always be scalarised;
- IDEA-T, HCI, soft systems thinking or design thinking have been validated as an outer loop for GO-ED-POMDP;
- the current synthetic goals were produced through the proposed framing process;
- an algorithm may legitimately resolve normative or political disagreement;
- a framing challenge can be detected reliably from observations alone;
- conditional optimality inside the model guarantees real-world success;
- `10^11` requests per hour has been simulated, benchmarked or qualified;
- near-zero tolerated loss implies a physically achievable zero-loss production system.

GO-ED-POMDP remains a human-governed decision-support research framework.
