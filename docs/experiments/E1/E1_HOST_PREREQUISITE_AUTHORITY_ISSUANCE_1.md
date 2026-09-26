# E1 Host Prerequisite Authority Issuance 1

Issued exactly the two bounded authorities approved by the Architect.

## Repository authority

```json
{
  "schema_version": "E1-AUTHORITY-1",
  "status": "ISSUED",
  "scope": "LIVE_R4/G4/E1-WP-001/FIRST_PROGRAMMER_EXECUTION",
  "runtime": "sha256:b6bcbb437f63c1433167103b1c7e15b723190721518e02ff2e4d2523fd625761",
  "controller_store": "AUTHORITY-STORE-GENERATION-sha256:ab07c7cbd889588fd80976bf5c47b7358722eaf6e2e1b7364e612c03899bf9ff",
  "lineage": "R4-final CURRENT UNIQUE",
  "programmer_profile": "ProgrammerProfile-sha256:0a0718f285a942c13a9f00e4b367cbea2394937fa18c4d7e11ed2c6c2803dd67",
  "architect_decision": "APPROVE REAUTHORIZE_QUALIFIED_VALUES",
  "decision_date": "2026-09-21",
  "single_use": true,
  "authority_expansion": "NONE",
  "record_type": "CURRENT_REPOSITORY_AUTHORITY-1",
  "read_roots": [
    "/home/gvasend/app/kge-forge",
    "/home/gvasend/app/kge-forge-demo"
  ],
  "write_roots": [
    "/home/gvasend/app/kge-forge/src/kge_forge/__init__.py",
    "/home/gvasend/app/kge-forge/src/kge_forge/context",
    "/home/gvasend/app/kge-forge/tests/context",
    "/home/gvasend/app/kge-forge/docs/implementation/E1-WP-001.md"
  ],
  "promotion": "NONE",
  "dynamic_expansion": "DENY",
  "restart": "same identity append-only audit/ownership; no reset",
  "denied": "protected and unrelated paths, secrets, credentials",
  "authority_id": "RepositoryAuthority-sha256:79b5d23d69e623306279d4966c31443a45ceea2adc03549b08cf1d2967e515fb"
}
```

Identity: `RepositoryAuthority-sha256:79b5d23d69e623306279d4966c31443a45ceea2adc03549b08cf1d2967e515fb`.

## Status/budget authority

```json
{
  "schema_version": "E1-AUTHORITY-1",
  "status": "ISSUED",
  "scope": "LIVE_R4/G4/E1-WP-001/FIRST_PROGRAMMER_EXECUTION",
  "runtime": "sha256:b6bcbb437f63c1433167103b1c7e15b723190721518e02ff2e4d2523fd625761",
  "controller_store": "AUTHORITY-STORE-GENERATION-sha256:ab07c7cbd889588fd80976bf5c47b7358722eaf6e2e1b7364e612c03899bf9ff",
  "lineage": "R4-final CURRENT UNIQUE",
  "programmer_profile": "ProgrammerProfile-sha256:0a0718f285a942c13a9f00e4b367cbea2394937fa18c4d7e11ed2c6c2803dd67",
  "architect_decision": "APPROVE REAUTHORIZE_QUALIFIED_VALUES",
  "decision_date": "2026-09-21",
  "single_use": true,
  "authority_expansion": "NONE",
  "record_type": "CURRENT_STATUS_BUDGET_AUTHORITY-1",
  "policy": {
    "schema": "E1-RUN-CONTROL-1",
    "seconds": {
      "cycle": [
        120,
        300
      ],
      "no_progress": [
        180,
        300
      ],
      "invocation": [
        1200,
        1800
      ],
      "phase": [
        30,
        120
      ]
    },
    "requests": [
      8,
      12
    ],
    "tokens": [
      100000,
      150000
    ],
    "automatic_retry": false,
    "usage_unknown": "TIME_AND_REQUEST_LIMITS_ONLY"
  },
  "hard_exhaustion": "close admission; cancellation/recovery; QUIESCENT; no future execution",
  "cancellation": "authoritative cancellation; release ownership; no unconfirmed transmission claim",
  "recovery": "durable counters/policy/identity; no reset; ambiguity blocks",
  "escalation": "FAIL_CLOSED",
  "authority_id": "StatusBudgetAuthority-sha256:02cc22de4ad70612c8b1e39e4df6f3bf8733c777d4729fb66d59d519fc6edc99"
}
```

Identity: `StatusBudgetAuthority-sha256:02cc22de4ad70612c8b1e39e4df6f3bf8733c777d4729fb66d59d519fc6edc99`.

## Dependency transitions

- `REPOSITORY_AUTHORITY`: `BLOCKED → SATISFIED`
- `STATUS_BUDGET`: `BLOCKED → SATISFIED`

Deterministic propagation exposes existing graph dependents. Current actionable frontier: `DISPATCHER_ELIGIBILITY`, `ACCEPTANCE_EVIDENCE`, `FIRST_REPO_OPERATION`. `HOST_CONSTRUCTION` remains blocked by dispatcher eligibility and other existing prerequisites. `MODEL_REQUEST_READY` remains blocked.

No new dependencies or topology changes were introduced. No host, lifecycle, ownership, transmission, model request, or E1 effect occurred.
