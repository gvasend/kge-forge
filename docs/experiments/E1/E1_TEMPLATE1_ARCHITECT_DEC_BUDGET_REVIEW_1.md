# E1 Template-1 — Architect review: DEC-BUDGET

DECISION_ID = DEC-BUDGET. STATUS = DECISION_READY. **Review only: no choice has been made and no authority is issued.**

## Question and exact governing proposition

Which exact canonical type/representation shall authenticated_inputs.budget_policy use: A authority reference, B entire policy value, or C explicitly typed projection? Choose one or defer/reject; no inferred default.

Adopt exactly one of A, B or C below as the canonical representation and exact source-projection contract for authenticated_inputs.budget_policy, for the recorded StatusBudgetAuthority snapshot. Preserve all existing budget values, scope, lineage and controls. This establishes representation policy only; it does not establish current applicability, qualify source use, implement validation, perform mapping, or authorize execution.

## Authoritative budget source

Source: [Host Prerequisite Authority Issuance 1](E1_HOST_PREREQUISITE_AUTHORITY_ISSUANCE_1.md), second JSON block, `CURRENT_STATUS_BUDGET_AUTHORITY-1`.

- Authority identity: `StatusBudgetAuthority-sha256:02cc22de4ad70612c8b1e39e4df6f3bf8733c777d4729fb66d59d519fc6edc99`.
- Recorded scope: `LIVE_R4/G4/E1-WP-001/FIRST_PROGRAMMER_EXECUTION`.
- Recorded lineage: `R4-final CURRENT UNIQUE`.
- Authority body: 1189 canonical bytes; SHA-256 `02cc22de4ad70612c8b1e39e4df6f3bf8733c777d4729fb66d59d519fc6edc99`, excluding only `authority_id`.

The [accepted result](E1_TEMPLATE1_GRAPH_RESOLUTION_INPUT_BUDGET_1_RESULT.md) and [dossier](E1_TEMPLATE1_GRAPH_RESOLUTION_INPUT_BUDGET_1_DOSSIER.md) establish representation decision readiness. Their exact hashes and current gate were verified. Recorded source authentication does not prove live publication, freshness or applicability. In particular, EXECUTION scope must not be equated with the target REQUEST construction scope.

## Budget value semantics: unchanged

The values and controls below are existing source facts, not alternatives in this decision. Ordered arrays are reproduced exactly; this review neither reinterprets their endpoint semantics nor revisits their bounds.

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

No evidence requires reconsidering these values. Single-use, no expansion, cancellation/recovery, durable counters/no reset and FAIL_CLOSED remain in force for every option.

## Budget representation policy: the choice

A, B and C are mutually exclusive representations for the same existing policy. They do not change its value semantics or confer different operational powers. No recommended choice is supported: **RECOMMENDED_MINIMUM_IF_SUPPORTED = NONE**. A smaller field or inline policy is a tradeoff, not evidence of a preferred governing contract.

Canonical byte rule for all options: UTF-8 of `json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)`, with no newline/whitespace after strict JSON/type validation. The following compact code blocks show exact field bytes for the recorded snapshot. They are review examples, not accepted field mappings or Template-1 artifacts. Field-content digests below are neither authority identities nor complete Template-1/WorkAuthorization identities.

### Option A — Authority reference

Exact canonical representation (string):

```json
"StatusBudgetAuthority-sha256:02cc22de4ad70612c8b1e39e4df6f3bf8733c777d4729fb66d59d519fc6edc99"
```

Canonical field bytes: 95; SHA-256 `42de4041f9408b344d002017ef982d698ae59beb557d1578e563bb2a5d7f8f67`.

**Authoritative source relationship:** Reference resolves to the hash-verified full source body; policy is exactly /policy of that body. All source controls remain authoritative.

**Mapping consequences:** Copy the complete authority ID including StatusBudgetAuthority-sha256 prefix, exactly; field denotes AUTHORITY_IDENTITY, not content identity. Exact selector: `"/authority_id"`.

**Identity/canonicalization consequences:** Small field; mandatory source resolution remains external to value. Field canonical bytes differ from B and C; identity-covered bodies therefore differ. A future alternative change changes identity-covered input bytes and requires revalidation; no permissive mixed schema is authorized.

**Consumer consequences:** Constructor currently stores/hashes the supplied string but does not authenticate or dereference it. A later approved CONTRACT-T1/validator must require exact reference type plus independently supplied verified source; no new resolver availability is claimed.

**Freshness/currentness consequences:** Authenticated source and exact current applicability/freshness must be established independently before mapping/use. Neither reference nor copied policy nor embedded scope proves currentness. Changed source bytes stale dependent evidence.

**Supported advantages:** Smallest displayed field (95 canonical bytes), with an explicit authority identity linking the complete source record.

**Supported disadvantages:** Policy is not inline. A verified owning source must remain independently available; existing constructor neither resolves nor authenticates the reference.

**Downstream actions potentially unlocked:** REEVAL-BUDGET only after an explicit authenticated decision record; subsequent actions retain all gates. After accepted reevaluation, DEC-INTERFACES / CONTRACT-T1 / MAP-BUDGET can be reconsidered subject to remaining prerequisites.

**Authority granted if approved:** Only the exact selected representation/source-projection policy; no operational authority.

**Authority not granted:** budget expansion or counter reset; new authority/source creation; implementation or validator changes; map or candidate construction; WorkAuthorization acceptance/issuance/use; Template-1 or Candidate-3 construction; runtime/lifecycle/ownership/repository/transmission effects.

### Option B — Complete policy body

Exact canonical representation (object):

```json
{"automatic_retry":false,"requests":[8,12],"schema":"E1-RUN-CONTROL-1","seconds":{"cycle":[120,300],"invocation":[1200,1800],"no_progress":[180,300],"phase":[30,120]},"tokens":[100000,150000],"usage_unknown":"TIME_AND_REQUEST_LIMITS_ONLY"}
```

Canonical field bytes: 239; SHA-256 `b25973ad894b287ca758552a9fdfd4e22ddbef671485b280a199c2c9b03dc177`.

**Authoritative source relationship:** A separate mandatory provenance/validation input pins the full source authority_id and exact /policy selector. Body equality alone does not confer authority; the full authority controls remain enforced from authenticated source. This dossier supplies the source link, but does not authorize adding another Template-1 key.

**Mapping consequences:** Copy the exact complete /policy JSON subtree including schema, seconds, requests, tokens, automatic_retry and usage_unknown. This is a policy value, not an authority ID or full authority record. Exact selector: `"/policy (entire object, no omitted members)"`.

**Identity/canonicalization consequences:** Self-contained numerical policy in this field; ownership/applicability linkage still requires independent source proof. No changes to the 22-input key set. A future alternative change changes identity-covered input bytes and requires revalidation; no permissive mixed schema is authorized.

**Consumer consequences:** Constructor hashes the supplied object but lacks field-specific source/type validation. Later contract/validator must compare it against the entire authenticated /policy; full-record controls cannot be discarded because absent from this subtree.

**Freshness/currentness consequences:** Authenticated source and exact current applicability/freshness must be established independently before mapping/use. Neither reference nor copied policy nor embedded scope proves currentness. Changed source bytes stale dependent evidence.

**Supported advantages:** Carries the complete numerical policy directly in the field, with no new projection discriminator.

**Supported disadvantages:** The field alone lacks owning authority/scope/control linkage. Mandatory external provenance and full-source validation remain necessary; policy equality is not authority.

**Downstream actions potentially unlocked:** REEVAL-BUDGET only after an explicit authenticated decision record; subsequent actions retain all gates. After accepted reevaluation, DEC-INTERFACES / CONTRACT-T1 / MAP-BUDGET can be reconsidered subject to remaining prerequisites.

**Authority granted if approved:** Only the exact selected representation/source-projection policy; no operational authority.

**Authority not granted:** budget expansion or counter reset; new authority/source creation; implementation or validator changes; map or candidate construction; WorkAuthorization acceptance/issuance/use; Template-1 or Candidate-3 construction; runtime/lifecycle/ownership/repository/transmission effects.

### Option C — Explicit typed projection with authority link

Exact canonical representation (object with exact fixed keys):

```json
{"authority_id":"StatusBudgetAuthority-sha256:02cc22de4ad70612c8b1e39e4df6f3bf8733c777d4729fb66d59d519fc6edc99","controller_store":"AUTHORITY-STORE-GENERATION-sha256:ab07c7cbd889588fd80976bf5c47b7358722eaf6e2e1b7364e612c03899bf9ff","controls":{"authority_expansion":"NONE","cancellation":"authoritative cancellation; release ownership; no unconfirmed transmission claim","escalation":"FAIL_CLOSED","hard_exhaustion":"close admission; cancellation/recovery; QUIESCENT; no future execution","recovery":"durable counters/policy/identity; no reset; ambiguity blocks","single_use":true},"lineage":"R4-final CURRENT UNIQUE","policy":{"automatic_retry":false,"requests":[8,12],"schema":"E1-RUN-CONTROL-1","seconds":{"cycle":[120,300],"invocation":[1200,1800],"no_progress":[180,300],"phase":[30,120]},"tokens":[100000,150000],"usage_unknown":"TIME_AND_REQUEST_LIMITS_ONLY"},"programmer_profile":"ProgrammerProfile-sha256:0a0718f285a942c13a9f00e4b367cbea2394937fa18c4d7e11ed2c6c2803dd67","runtime":"sha256:b6bcbb437f63c1433167103b1c7e15b723190721518e02ff2e4d2523fd625761","schema":"E1-TEMPLATE1-BUDGET-PROJECTION-1","scope":"LIVE_R4/G4/E1-WP-001/FIRST_PROGRAMMER_EXECUTION"}
```

Canonical field bytes: 1166; SHA-256 `4e226f1e89617fba3243c01575505f459dc5a3a9d01542098cacbb19fa38da81`.

**Authoritative source relationship:** authority_id authenticates the full owning record; all included identity/scope/policy/control members must equal their named source paths. The envelope is a canonical value with authority provenance, never new authority.

**Mapping consequences:** Construct exactly the displayed object; preserve every selected value and complete policy/control subtrees. The literal schema is a proposed discriminator, not an existing adopted contract. No additional or omitted keys. Exact selector: `{"authority_id": "/authority_id", "controller_store": "/controller_store", "controls": {"authority_expansion": "/authority_expansion", "cancellation": "/cancellation", "escalation": "/escalation", "hard_exhaustion": "/hard_exhaustion", "recovery": "/recovery", "single_use": "/single_use"}, "lineage": "/lineage", "policy": "/policy", "programmer_profile": "/programmer_profile", "runtime": "/runtime", "schema": "literal E1-TEMPLATE1-BUDGET-PROJECTION-1 (PROPOSED, unadopted)", "scope": "/scope"}`.

**Identity/canonicalization consequences:** More redundant data; exact equality checks prevent drift between embedded policy/scope/controls and owning source. No extra top-level Template-1 input key or migration is implied. A future alternative change changes identity-covered input bytes and requires revalidation; no permissive mixed schema is authorized.

**Consumer consequences:** Current generic constructor can include JSON objects in hashing; it does not validate this proposed schema. Adopting it would require explicit CONTRACT-T1 treatment and separately authorized validation; no implementation grant or working consumer support is claimed.

**Freshness/currentness consequences:** Authenticated source and exact current applicability/freshness must be established independently before mapping/use. Neither reference nor copied policy nor embedded scope proves currentness. Changed source bytes stale dependent evidence.

**Supported advantages:** Carries an explicit typed discriminator, authority link, applicability references, full policy and selected controls together; exact source-equality checks can detect drift.

**Supported disadvantages:** Largest displayed field (1166 canonical bytes), duplicated source members and a proposed schema requiring explicit contract treatment and strict consistency validation. Generic object hashing does not establish consumer support.

**Downstream actions potentially unlocked:** REEVAL-BUDGET only after an explicit authenticated decision record; subsequent actions retain all gates. After accepted reevaluation, DEC-INTERFACES / CONTRACT-T1 / MAP-BUDGET can be reconsidered subject to remaining prerequisites.

**Authority granted if approved:** Only the exact selected representation/source-projection policy; no operational authority.

**Authority not granted:** budget expansion or counter reset; new authority/source creation; implementation or validator changes; map or candidate construction; WorkAuthorization acceptance/issuance/use; Template-1 or Candidate-3 construction; runtime/lifecycle/ownership/repository/transmission effects.

## Common acceptance and exclusions

- Parse strict JSON: reject duplicate keys, NaN/infinities, wrong types or extra/missing members; no implicit coercion.
- Authenticate owning authority by SHA-256 of its exact sorted-key compact JSON body excluding authority_id; reject wrong identity/prefix/type.
- Preserve source scope, lineage, runtime, controller store, programmer profile, single-use, no expansion, hard exhaustion, cancellation, recovery/no-reset and FAIL_CLOSED independently of field representation.
- Before actual mapping/use, separately establish current applicability and source availability; a dossier snapshot is not publication/freshness proof.
- Array order and endpoints are exact; integers are not booleans/floats; false remains JSON false. Never broaden bounds or treat policy bytes as new authority.
- Reject cross-alternative types/shapes after any future choice. No permissive union, auto-dereference fallback, omission or silent normalization.

Option B is the entire `/policy` subtree, not the full authority record; its separate provenance link adds no Template-1 key. Option C’s schema discriminator is proposed, not already adopted. All three preserve the same authenticated full-source restrictions. The existing constructor’s ability to hash a JSON value is not qualified consumer validation.

## Consequences of each answer

| Answer | Root / slot eligible for reevaluation | Potential next action after accepted decision record | CONTRACT-T1 ready? | Template-1 ready? | Candidate-3 ready? |
|---|---|---|---|---|---|
| APPROVE_A | root:budget / authenticated_inputs.budget_policy; neither satisfied | REEVAL-BUDGET | NO | NO | NO |
| APPROVE_B | root:budget / authenticated_inputs.budget_policy; neither satisfied | REEVAL-BUDGET | NO | NO | NO |
| APPROVE_C | root:budget / authenticated_inputs.budget_policy; neither satisfied | REEVAL-BUDGET | NO | NO | NO |
| REJECT | No new reevaluation enabled | None | NO | NO | NO |
| DEFER | No new reevaluation enabled | None | NO | NO | NO |

Every approval first requires its own authenticated, explicit DEC-BUDGET record tied to the exact reviewed dossier and option. That record is not created here. REEVAL-BUDGET must still prove the full original semantic/source criterion; it may stop at missing current applicability/source evidence. MAP-BUDGET independently requires an accepted mapping and CONTRACT-T1. `root:budget` closes only on its existing accepted final mapping proof; the value slot is not resolved by approval.

Current remaining gates:
- REEVAL-BUDGET: DEC-BUDGET.
- DEC-INTERFACES: REEVAL-IMPLEMENTATION, REEVAL-BUDGET.
- CONTRACT-T1: REEVAL-IMPLEMENTATION, REEVAL-BUDGET, DEC-EXEC, DEC-INTERFACES.
- MAP-BUDGET: CONTRACT-T1, REEVAL-BUDGET.

After a passing REEVAL-BUDGET, CONTRACT-T1 would still wait for REEVAL-IMPLEMENTATION, DEC-EXEC and DEC-INTERFACES. DEC-INTERFACES still needs accepted implementation-domain reevaluation and its own decision. Other sources, mappings, binding construction and qualified validator remain outstanding. No A/B/C answer alone makes construction or resumption ready. Rejection or deferral creates no representation default and unlocks no action. A modified fourth proposal is outside this reviewed option set and requires bounded preparation and a new readiness check.

## Fact-blocked decisions — informational only

These are not submitted for decision in this review:

- DEC-IMPLEMENTATION: Distinct implementation-domain owning record, identity contract and exact canonical selector; partial dossier is FACT_BLOCKED.
- DEC-EXEC: Concrete independent executable-policy source/projector or exact independently grounded permission proposal; no argv-derived permission.
- DEC-AUDIT: Concrete namespace/store identity, owning provenance and independently evidenced outside-agent-root placement.
- DEC-RUNTIME_HEAD: Concrete current R4/G4 head selector/authority body, publication target and scoped lineage evidence.
- DEC-SUPERVISOR: Concrete supervisor selector and owning current-release/context selection and freshness/lineage evidence.

DEC-INTERFACES is also blocked by its reevaluation prerequisites; no interface decision is requested here. Current ACTIONABLE remains [DEC-BUDGET], with the existing human decision handoff unchanged.

## Provenance and validation

Source identities below preserve the exact evidence reviewed. A changed source or dossier requires readiness revalidation; no claim of live qualification is made.

- `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_INPUT_BUDGET_1_RESULT.md` — SHA-256 `d23e956938b2d29380157032bfd5e76748f887994a24fe44d175ec742947ba84` — Accepted action result and readiness audit.

- `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_INPUT_BUDGET_1_DOSSIER.md` — SHA-256 `5ebf7b266d3dc6129257114a184c31396b1322306eb1ce705e3507870cb05e0b` — All three prepared alternatives.

- `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_INPUT_BUDGET_1_DOSSIER.json` — SHA-256 `50ba6151aaa86c5e62f5f26e8960e4bad902009e82b8d5aa2e16d6583d356957` — Exact proposed values/selectors and source provenance.

- `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json` — SHA-256 `b5bd277f17c65ff534e1cd407ef0252905cd1ababd0c8945774cebedec37715f` — Current execution state, readiness gate and action prerequisites.

- `docs/experiments/E1/E1_TEMPLATE1_TYPED_KNOWLEDGE_GRAPH_1.json` — SHA-256 `5f95d8b0cb3b4ba3a8d659f1028a6626afff020553b27b8690b60e0b89d2af39` — Root/slot state baseline.

- `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_INPUT_IMPLEMENTATION_1_RESULT.md` — SHA-256 `a1000808e24e1a5193a79023d9f23384c03e343cb4be308273401ca4ccd97205` — Fact-blocked outcome.

All dossier source hashes and the accepted result identity match. Exact canonical sample byte lengths/hashes were checked. Only this review and its JSON companion are created; no existing E1 state or artifact is changed.

```text
DECISION_ID = DEC-BUDGET
STATUS = DECISION_READY
OPTIONS = ["A: authority reference", "B: complete policy body", "C: explicit typed projection"]
RECOMMENDED_MINIMUM_IF_SUPPORTED = NONE
FACT_BLOCKED_DECISIONS = ["DEC-IMPLEMENTATION", "DEC-EXEC", "DEC-AUDIT", "DEC-RUNTIME_HEAD", "DEC-SUPERVISOR"]
ARCHITECT_DECISION_REQUIRED = YES
ROOT_CONDITIONS_RESOLVED = 0
SLOTS_RESOLVED = 0
TEMPLATE1_CONSTRUCTION_READY = NO
CANDIDATE3_RESUMPTION_READY = NO
PRODUCTION_EFFECT = NO
```
