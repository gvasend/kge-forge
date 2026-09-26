# E1 Template-1 Architect decision batch 1 — issuance result

Three separate records were issued from the explicit Architect instruction. These records are append-only artifacts: existing decisions, dossiers and Candidate-3 authority were not modified. SHA-256 authority identities cover sorted-key compact UTF-8 JSON excluding authority_id only; each recomputed successfully. No external signer or live-store publication is claimed.

| Decision | Record | Authority identity |
|---|---|---|
| DEC-BINDING | [E1_TEMPLATE1_ARCHITECT_DEC_BINDING_AUTHORITY_1.json](E1_TEMPLATE1_ARCHITECT_DEC_BINDING_AUTHORITY_1.json) | `E1-ArchitectDecisionAuthority-sha256:fbebb98f3d136b0baab84590628e62db660111dac463b82e49421267b3983ae0` |
| DEC-IGNORED | [E1_TEMPLATE1_ARCHITECT_DEC_IGNORED_AUTHORITY_1.json](E1_TEMPLATE1_ARCHITECT_DEC_IGNORED_AUTHORITY_1.json) | `E1-ArchitectDecisionAuthority-sha256:ddb9fdad668cc94419c973d725373eddae65defcf62aecea360a79a626a96079` |
| DEC-VALIDATOR | [E1_TEMPLATE1_ARCHITECT_DEC_VALIDATOR_AUTHORITY_1.json](E1_TEMPLATE1_ARCHITECT_DEC_VALIDATOR_AUTHORITY_1.json) | `E1-ArchitectDecisionAuthority-sha256:ddd8e36587e2780f640b7babb0e44951b4f5510955822af1db8a00aa74fdd629` |

DEC-BINDING retains the one-candidate conditional subobject scope and all hash-bound dossier gates/exclusions. DEC-IGNORED adopts exact JSON null on all four required input keys, rejecting absence/non-null/mixed-schema inputs; the established consumer assignments follow validation. Actual invocation/audit sources remain independently required; no 19-key schema or migration authorized. DEC-VALIDATOR grants only bounded implementation/test scope, preserving CONTRACT-T1 and every dossier qualification/effect prohibition. A validator PASS grants no operational authority.

Mechanical propagation: DEC-VALIDATOR is the existing required final action for gate:validator_authority, and its preparation plus issued authenticated record now satisfy that gate. Root:binding still requires BUILD-BINDING; root:ignored still requires MAP-IGNORED. No slot is resolved by these grants or policy choice. No implementation is performed, so null validation and pure-validator behavior are not claimed implemented.

DEC-EXEC remains fact-blocked under BATCH1-ACTIONABILITY-01; this previously recorded review classification is persisted without repair. DEC-AUDIT, DEC-RUNTIME_HEAD and DEC-SUPERVISOR retain their exact prior blockers. All other prerequisites/external gates remain unresolved as recorded. Eleven actions completed, 45 blocked, zero actionable; selector receives an empty set and returns NONE. No next action executed.

The typed graph adds three provenance-backed non-ordering authority relationships and satisfies only the validator-authority gate. All slot entities and baseline prerequisite topology are preserved. Plan source hash is refreshed for this explicitly authorized graph update; original policy replay is a historical snapshot. Prior closure-analysis snapshots remain historical. Other incomplete source, schema, mapping and validator gates keep both readiness predicates false. Candidate-3 authority remains unchanged and unconsumed.

PRODUCTION_EFFECT = YES only in the plan’s control-plane sense of authority/contract issuance. No runtime, provider, repository task, lifecycle, ownership, issuance/use of WorkAuthorization, construction or implementation effects occurred.

```text
DEC-BINDING = APPROVED_OPTION_1
DEC-IGNORED = APPROVED_OPTION_A_NULL_SENTINELS
DEC-VALIDATOR = APPROVED_OPTION_1
AUTHORITY_RECORDS = ["docs/experiments/E1/E1_TEMPLATE1_ARCHITECT_DEC_BINDING_AUTHORITY_1.json", "docs/experiments/E1/E1_TEMPLATE1_ARCHITECT_DEC_IGNORED_AUTHORITY_1.json", "docs/experiments/E1/E1_TEMPLATE1_ARCHITECT_DEC_VALIDATOR_AUTHORITY_1.json"]
ROOT_CONDITIONS_RESOLVED = ["gate:validator_authority"]
ROOT_CONDITIONS_REMAINING = 27
SLOTS_RESOLVED = []
SLOTS_REMAINING = 41
NEWLY_ACTIONABLE = []
ACTIONABLE = []
NEXT_ACTION = NONE
TEMPLATE1_CONSTRUCTION_READY = NO
CANDIDATE3_RESUMPTION_READY = NO
PRODUCTION_EFFECT = YES (control-plane authority/contract issuance only; runtime effects NO)
```
