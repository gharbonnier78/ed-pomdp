# Data Readiness Gate

Industrial calibration and retrospective replay are conditional on this gate.

## Decision

`G_data ∈ {READY, PARTIALLY_READY, NOT_READY}`

## Criteria

Assess at minimum:

- release history and trustworthy timestamps;
- links among requirements, risks, tests, environments and incidents;
- test-result retention and execution metadata;
- environment representativity and configuration history;
- observability signals and trace completeness;
- ability to connect incidents to releases;
- privacy, confidentiality and intellectual-property constraints;
- lawful processing and internal governance approval;
- publication rights for aggregate results.

## Outcomes

### READY

Proceed to governed industrial calibration and retrospective replay.

### PARTIALLY_READY

Use a hybrid design: industrial marginals and structures where allowed, synthetic completion where data are missing, and explicit uncertainty labels.

### NOT_READY

Proceed with the complete synthetic contribution. Industrial claims remain blocked, but the research programme does not stall.

## Gate rule

No document may imply industrial validation unless this gate is recorded as READY for the relevant dataset and use case.