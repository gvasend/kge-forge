# INPUT-BUDGET — DEC-BUDGET dossier 1

**Unadopted alternatives. No recommendation, decision, mapping or authority issuance.**

Question: Which exact canonical type/representation shall authenticated_inputs.budget_policy use: A authority reference, B entire policy value, or C explicitly typed projection? Choose one or defer/reject; no inferred default.

Scope: Representation and exact projection contract for the recorded StatusBudgetAuthority snapshot only; no budget change, applicability assertion, grant expansion or downstream execution.

Source: `StatusBudgetAuthority-sha256:02cc22de4ad70612c8b1e39e4df6f3bf8733c777d4729fb66d59d519fc6edc99`, recorded scope `LIVE_R4/G4/E1-WP-001/FIRST_PROGRAMMER_EXECUTION`, lineage `R4-final CURRENT UNIQUE`. The 1189-byte authority body identity matches accepted SEM-BUDGET evidence. This verifies recorded bytes only.

## Preserved policy and controls

```json
{
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
  "source_controls": {
    "single_use": true,
    "authority_expansion": "NONE",
    "hard_exhaustion": "close admission; cancellation/recovery; QUIESCENT; no future execution",
    "cancellation": "authoritative cancellation; release ownership; no unconfirmed transmission claim",
    "recovery": "durable counters/policy/identity; no reset; ambiguity blocks",
    "escalation": "FAIL_CLOSED"
  }
}
```

## Concrete alternatives

### Option A — Authority reference

JSON type: string. Exact selector: `"/authority_id"`.

Copy the complete authority ID including StatusBudgetAuthority-sha256 prefix, exactly; field denotes AUTHORITY_IDENTITY, not content identity.

```json
"StatusBudgetAuthority-sha256:02cc22de4ad70612c8b1e39e4df6f3bf8733c777d4729fb66d59d519fc6edc99"
```

Reference resolves to the hash-verified full source body; policy is exactly /policy of that body. All source controls remain authoritative.

Constructor currently stores/hashes the supplied string but does not authenticate or dereference it. A later approved CONTRACT-T1/validator must require exact reference type plus independently supplied verified source; no new resolver availability is claimed.

Small field; mandatory source resolution remains external to value. Field canonical bytes differ from B and C; identity-covered bodies therefore differ.

UTF-8 encoding of json.dumps(value, sort_keys=True, separators=(",",":"), ensure_ascii=True); no whitespace/newline, after strict JSON/type validation. Escape strings by JSON rules; no normalization/coercion.

Illustrative field-only bytes: 95 bytes, SHA-256 `42de4041f9408b344d002017ef982d698ae59beb557d1578e563bb2a5d7f8f67`. This is a dossier example, not a constructed Template-1 input, accepted mapping or authority identity.

### Option B — Complete policy body

JSON type: object. Exact selector: `"/policy (entire object, no omitted members)"`.

Copy the exact complete /policy JSON subtree including schema, seconds, requests, tokens, automatic_retry and usage_unknown. This is a policy value, not an authority ID or full authority record.

```json
{
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
}
```

A separate mandatory provenance/validation input pins the full source authority_id and exact /policy selector. Body equality alone does not confer authority; the full authority controls remain enforced from authenticated source. This dossier supplies the source link, but does not authorize adding another Template-1 key.

Constructor hashes the supplied object but lacks field-specific source/type validation. Later contract/validator must compare it against the entire authenticated /policy; full-record controls cannot be discarded because absent from this subtree.

Self-contained numerical policy in this field; ownership/applicability linkage still requires independent source proof. No changes to the 22-input key set.

UTF-8 encoding of json.dumps(value, sort_keys=True, separators=(",",":"), ensure_ascii=True); no whitespace/newline, after strict JSON/type validation. Escape strings by JSON rules; no normalization/coercion.

Illustrative field-only bytes: 239 bytes, SHA-256 `b25973ad894b287ca758552a9fdfd4e22ddbef671485b280a199c2c9b03dc177`. This is a dossier example, not a constructed Template-1 input, accepted mapping or authority identity.

### Option C — Explicit typed projection with authority link

JSON type: object with exact fixed keys. Exact selector: `{"schema": "literal E1-TEMPLATE1-BUDGET-PROJECTION-1 (PROPOSED, unadopted)", "authority_id": "/authority_id", "scope": "/scope", "lineage": "/lineage", "runtime": "/runtime", "controller_store": "/controller_store", "programmer_profile": "/programmer_profile", "policy": "/policy", "controls": {"single_use": "/single_use", "authority_expansion": "/authority_expansion", "hard_exhaustion": "/hard_exhaustion", "cancellation": "/cancellation", "recovery": "/recovery", "escalation": "/escalation"}}`.

Construct exactly the displayed object; preserve every selected value and complete policy/control subtrees. The literal schema is a proposed discriminator, not an existing adopted contract. No additional or omitted keys.

```json
{
  "schema": "E1-TEMPLATE1-BUDGET-PROJECTION-1",
  "authority_id": "StatusBudgetAuthority-sha256:02cc22de4ad70612c8b1e39e4df6f3bf8733c777d4729fb66d59d519fc6edc99",
  "scope": "LIVE_R4/G4/E1-WP-001/FIRST_PROGRAMMER_EXECUTION",
  "lineage": "R4-final CURRENT UNIQUE",
  "runtime": "sha256:b6bcbb437f63c1433167103b1c7e15b723190721518e02ff2e4d2523fd625761",
  "controller_store": "AUTHORITY-STORE-GENERATION-sha256:ab07c7cbd889588fd80976bf5c47b7358722eaf6e2e1b7364e612c03899bf9ff",
  "programmer_profile": "ProgrammerProfile-sha256:0a0718f285a942c13a9f00e4b367cbea2394937fa18c4d7e11ed2c6c2803dd67",
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
  "controls": {
    "single_use": true,
    "authority_expansion": "NONE",
    "hard_exhaustion": "close admission; cancellation/recovery; QUIESCENT; no future execution",
    "cancellation": "authoritative cancellation; release ownership; no unconfirmed transmission claim",
    "recovery": "durable counters/policy/identity; no reset; ambiguity blocks",
    "escalation": "FAIL_CLOSED"
  }
}
```

authority_id authenticates the full owning record; all included identity/scope/policy/control members must equal their named source paths. The envelope is a canonical value with authority provenance, never new authority.

Current generic constructor can include JSON objects in hashing; it does not validate this proposed schema. Adopting it would require explicit CONTRACT-T1 treatment and separately authorized validation; no implementation grant or working consumer support is claimed.

More redundant data; exact equality checks prevent drift between embedded policy/scope/controls and owning source. No extra top-level Template-1 input key or migration is implied.

UTF-8 encoding of json.dumps(value, sort_keys=True, separators=(",",":"), ensure_ascii=True); no whitespace/newline, after strict JSON/type validation. Escape strings by JSON rules; no normalization/coercion.

Illustrative field-only bytes: 1166 bytes, SHA-256 `4e226f1e89617fba3243c01575505f459dc5a3a9d01542098cacbb19fa38da81`. This is a dossier example, not a constructed Template-1 input, accepted mapping or authority identity.

## Validation and decision boundary

- Parse strict JSON: reject duplicate keys, NaN/infinities, wrong types or extra/missing members; no implicit coercion.
- Authenticate owning authority by SHA-256 of its exact sorted-key compact JSON body excluding authority_id; reject wrong identity/prefix/type.
- Preserve source scope, lineage, runtime, controller store, programmer profile, single-use, no expansion, hard exhaustion, cancellation, recovery/no-reset and FAIL_CLOSED independently of field representation.
- Before actual mapping/use, separately establish current applicability and source availability; a dossier snapshot is not publication/freshness proof.
- Array order and endpoints are exact; integers are not booleans/floats; false remains JSON false. Never broaden bounds or treat policy bytes as new authority.
- Reject cross-alternative types/shapes after any future choice. No permissive union, auto-dereference fallback, omission or silent normalization.

Option B means the complete policy subtree, not the full authority envelope. Its source link is mandatory provenance/validation evidence; no extra Template-1 input key is authorized. Option C’s discriminator and member contract are explicitly proposed choices, not observed existing consumer behavior. All options preserve the same full source restrictions.

The actual constructor presently preserves/hashes budget_policy but does not choose or validate its semantic type. Different alternatives produce different identity-covered canonical bytes; no mixed schema or implicit coercion is proposed. Future contract/validator work remains separate.

## Decision inputs and deferred facts

The source identity, complete policy, scope and restrictions are established for this snapshot. Comparing representation choices needs no newly invented runtime fact. Current applicability to construction—including EXECUTION versus REQUEST scope—remains explicitly unproved and excluded from the proposition being decided. Any later decision purporting to approve use/applicability would exceed this dossier and require new evidence.

Choose exactly A, B or C, or reject/defer. There is no evidence-supported default. Approval governs representation only; it does not grant implementation, authority issuance/use or construction. It schedules REEVAL-BUDGET; no root/slot closes automatically.

## Provenance

- `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_SEM_BUDGET_1_RESULT.md` — `sha256:b8ba709b79227bd765c26f262f2a9ce784a7aa02ac85defe29de2eabae4d7320` — Accepted K1-K3; policy; exact governing decision requirement.
- `docs/experiments/E1/E1_HOST_PREREQUISITE_AUTHORITY_ISSUANCE_1.md` — `sha256:5cf24bf05643e69543a9db154af7e2a6edc1943fe32280ea7d7762b06a43132f` — Second JSON block: StatusBudgetAuthority, /authority_id, /policy, /scope, /lineage and control members.
- `adapter/invocation_constructor.py` — `sha256:5908b257fdc7325d94d7524fbacbe3a7ec26d18d98507d6232c9ba1d41e8f9f7` — _body; artifact; construct_work_authorization.
- `adapter/context_projection.py` — `sha256:54ed15c7764ed1a4c3b4b44c78fadb2a698de0f7e71ec951b2fb618fabf49998` — canonical; digest.
- `docs/experiments/E1/E1_WORKAUTHORIZATION_TEMPLATE1_PRODUCTION_CONTRACT_1.md` — `sha256:1af1f3aac2acc34aefb8c0b2a9a6fb775de152f2f8db6eaf6dd0673458ea6b6a` — budget_policy row.
- `docs/experiments/E1/E1_WORKAUTHORIZATION_PRODUCTION_CONTRACT_DECISION_1.md` — `sha256:b916edc33d1534b516a187118146364c88aa360f0c8ff4f2dcc91a205aca1ad6` — budget_policy expected type/mapping.
- `docs/experiments/E1/E1_DECISION_INPUT_REENTRY_SEMANTICS_1.md` — `sha256:52827b823847a66266322c86818ae62826f761e30954f179e8282f96d79a5367` — Budget route and dossier/readiness predicates.

Exact selectors, proposed values, field-byte checks and future qualification obligations are in the companion JSON. Source byte changes stale this dossier and readiness until revalidated.
