# E2-P04 dependency-provenance closure 1

**RESULT = BLOCKED.** The exact native mismatch is diagnosed and applicable negative controls pass, but no contract/adapter or issued authority permits the missing ATTEST definitions to enter this lineage. **DEPENDENCY_PROVENANCE_CLOSED = NO; P04_EXECUTION_READY = NO.** No installation or A09–A13 operation occurred. See the [machine companion](DETERMINISTIC_PLANNER_V0_1_E2_P04_DEPENDENCY_PROVENANCE_CLOSURE_1.json) and [native trace](qualification/E2_P04_DEPENDENCY_PROVENANCE_CLOSURE_1/native-trace.json).

## Exact checkpoint and predicate

The exact [post-route-install bundle](DETERMINISTIC_PLANNER_V0_1_E2_P04_POST_ROUTE_INSTALL_BUNDLE_1.json) restores with native trust, physical pins and replay PASS. Its bundle ID is `885b23b6f64503153d2d6c4419b160cc278112b26238eecbab14c8b9ecb92ee4`, State is `99e47ad1e462c30cd33e2258e4c74ff670164fa7378e5a998e0f23b9256e4454`, and head is `a19b52ab601c6d3c7668b78c6e20cc87e54cfc317595e4da641fcbb7d107fb1e`. The existing fresh A09 candidate matches all three exactly; installed route currentness PASS. Pure `evidence.apply(snapshot, candidate, transient_attestation)` reproduces **DEPENDENCY_PROVENANCE** without returning an admitted Snapshot or executing a transaction.

The native call path is preflight → `evidence.apply` → canonical authentication-predicate/owner lookup → expected dependency construction → full-set/cardinality equality. [evidence.py:118–126](../../adapter/planner/evidence.py) computes:

```python
auth_record = canonical predicate with admission.authentication
trust = canonical entity referenced by auth_record, if present
expected = {ingress.provenance, gate.provenance}
expected |= required requirement and current route provenances
if trust is not None:
    expected.add(trust.provenance)
require set(admission.dependencies) == expected
require len(admission.dependencies) == len(expected)
```

Actual set size **4**, expected size **3**, missing records **0**, extra records **1**. Gate and requirement share one complete Provenance record. This is an unordered set, so there is no execution-order “first” dependency: the unique extra record identifies the mismatch unambiguously.

## Failing dependency and complete inventory

The extra dependency is the prepared trust-entity source [authorization-capture.json](qualification/E2_P04_CONTINUATION_INPUT_CLOSURE_1/authorization-capture.json), raw-file content ID **`92dadc3f807b795bc2fcd36583b21ecc0d806c20892aa55c7dec2b466102d74b`**. Its file hash, exact excerpt, native provenance shape and scope are valid. Both prepared ATTEST entities reference it. The candidate ingress names source predicate `E2-ATTESTOR-MAY-ATTEST:80f82bc3c61ea0dd5cb77f715d2af356b5249d01fc37e6a8c1701102713c7539`, which points to `E2-SYNTHETIC-ATTESTOR:80f82bc3c61ea0dd5cb77f715d2af356b5249d01fc37e6a8c1701102713c7539`. Neither predicate nor entity exists in the canonical Snapshot. Native lookup therefore yields no trust entity and does not add its provenance to the expected set.

| Dependency role | Source/definition status | Canonical/current/applicable |
|---|---|---|
| Ingress contract | Exact native body and physical origin provenance valid; offline, prefix pin absent | NO |
| External gate | Authored pre-receipt gate, pinned prospective source | YES |
| Evidence requirement | Pinned source, producer/target/proposition bindings; same Provenance as gate | YES |
| External route | Exact installed native body, current I02 event/authority/source binding | YES |
| ATTEST chain trust source | Valid preparation capture; referenced authority/attestor/predicates remain offline | NO |

The machine inventory records every full Provenance, logical role, content ID, canonical membership, currentness/applicability, authority and scope/lineage/generation independently. Native Evidence bytes, the semantic/native/content binding and transient Evidence-bound attestation are additional admission inputs, distinct from this support set. They are not canonically received Evidence yet.

**PROVENANCE_STATUS = COMPLETE_BUT_UNINSTALLED** applies to the physical definition/origin record. It does not mean complete canonical installation provenance or admitted operating authority. The preparation capture explicitly permits “Prepare scoped candidate ATTEST/fixture definitions and independent preflight; no admission, lifecycle execution, checkpoint alteration or runtime repair”. It remains bound to the earlier `9f00d563…` parent. This is valid historical preparation evidence, not a current installation grant. The [prepared definition wrapper](qualification/E2_P04_CONTINUATION_INPUT_CLOSURE_1/attest-definitions.json) contains typed candidates and an external T04 helper contract; it is not a sealed native installable ATTEST body/descriptor.

## What provenance does and does not establish

The failing predicate protects the exact dependency closure, complete-record identity and duplicate exclusion. It does **not** independently prove who authorized a definition, how it entered canonical state, an installation event, source-file availability or generation/lineage currentness. In particular, it includes the parsed offline ingress provenance even though that pin is absent from the canonical prefix. These concerns have separate native checks: ingress body/content/schema/context; canonical source-level ATTEST predicate/entity applicability; E02 evidence-bound attestation; codec source/field/prefix/policy/event verification; and I01/I02 installed-definition authority/event/currentness witnesses.

Definition origin/source provenance, installation authorization/event provenance, runtime-instance payload provenance and support/evidence provenance must remain separate. A prepared file hash or `validation=ACCEPTED` on an offline candidate cannot substitute for admitted authority or canonical installation. Dropping the extra trust source in an isolated negative candidate is also insufficient: the next observed native rejection is **`REFERENCE_CONTRACT: unknown predicate ID`**. The published fresh candidate was not edited.

## Installation and authority classification

**INSTALLATION_CLASSIFICATION = INSTALL_CONTRACT_INCOMPLETE.** I02 supports only the `EXTERNAL_RESOLUTION_CONTRACT` adapter; an independently hashed ATTEST type probe rejects with **DEFINITION_TYPE_NOT_ENABLED**. There is no ATTEST-chain native body/descriptor/currentness/frame/persistence adapter contract here. T04 constructs an offline definition-bearing Snapshot; adopting it would bypass the ordinary event lineage.

The future operation is **INSTALL**, because all prepared authority/attestor/predicate IDs are absent. The route's earlier REPLACE does not establish replacement ownership for these new roles. A legitimately installed chain must bind already-issued/admitted operating ATTEST authority, exact definition/body/source identity, a separate bounded INSTALL grant and accepted receipt, ordinary pre-State/parent/policy, scope/lineage/generation, installation event/registry witness and the A09 source-level consumer. INSTALL must not issue operating ATTEST rights.

No issued INSTALL authority applies. I02's single-use grant is exact route REPLACE only and has one canonical use. USE/DECIDE, PC02 fixture authority and preparation-only T04 candidate rights cannot be broadened into installation authority. Contract and adapter specification is the first blocker; bounded authority is an additional independent blocker. This request does not select a new authorization option.

The machine companion defines a bounded **draft** decision dossier with unselected options `AUTHORIZE_P04_ATTEST_DEFINITION_INSTALLATION` and `DECLINE_P04_ATTEST_DEFINITION_INSTALLATION`. The human qualification role must authorize exact sealed terms; Architect semantic design is separate. The dossier fixes the preserved current bundle/State/head, E2 scope/lineage/generation, source pin, gate, requirement and consumer, excludes lifecycle/P03/N-REAL/release effects, and enumerates missing body/adapter/authority seals. **Decision readiness = NO** until those terms exist; no partially specified grant is issued. New T04 authorization materialization may change ATTEST/predicate identities, so future ingress and A09 inputs must be resealed/rematerialized rather than reusing old native bindings automatically.

## Remaining DAG and later stages

The relevant preparation order is:

```text
current policy/context/head + gate/requirement + installed route
    → specify/qualify ATTEST configuration adapter and authority admission
    → separately issue/admit exact operating ATTEST and INSTALL authority
    → INSTALL canonical ATTEST chain/source predicate
    → seal/install ingress definition referencing that canonical predicate
    → rematerialize transient attestation and A09 against final head
    → complete non-mutating A09 preflight
```

Ingress installation has its own adapter/authority contract, unless a reviewed exact contract explicitly requires atomic composition. Neither is installed here. Every configuration event advances State/bundle/head and makes the previously fresh A09 command stale; reconstruct its command key, expected identities, installed-source dependencies, field bindings, ingress and Evidence-bound attestation after each event.

Before A09, contracts and current source-level trust must exist. Received Evidence/ReceiptAdmission belongs to A09, ValidationResult/accepted observation to A10, evidence proof/reentry to A11, actual REENTER output to A12, and actual SLOT/ROOT proof instances and finishing result to A13. These future lifecycle instances must not be installed as definitions or required as present admission inputs.

The same prospective configuration gap affects A10 validation input composition (CONTRACT_BLOCKED), A11 evidence-proof contract/event composition (CONTRACT_BLOCKED), A12 REENTER accepted-result definitions (AUTHORITY_REQUIRED plus non-route adapter absent) and A13 root/slot proof-contract definitions (AUTHORITY_REQUIRED plus non-route adapter absent). E04/E05/E06 capability qualification does not install those instances into this lineage. Their actual support/result/proof objects must still arise only at their native lifecycle boundaries. No later definition was installed speculatively.

**NEXT_PACKAGE = P04 ATTEST-chain/ingress configuration contract and adapter specification; then exact bounded operating/INSTALL authority decision and implementation qualification.**

## Negative controls and preservation

Thirteen applicable read-only controls reject absent/substituted provenance, source and scope substitutions, candidate scope/lineage/generation mismatch, offline trust pretending to be canonical, wrong native install-event identity, wrong authority class, foreign bundle/parent prefix and Evidence instance substituted for a definition. Each result specifies its validation domain. Foreign bundle/parent controls are exact-prefix oracles; `evidence.apply` itself checks Snapshot but not those two fields. No nonexistent ATTEST installer or prospective security suite is claimed qualified.

Only the unchanged existing I02 bundle was cold-restored/replayed; no post-install checkpoint or attestor replay is claimed. All 12,202 pre-existing runtime/plan/E1 files checked remain byte-identical. Runtime was not modified, original candidate is unchanged, and `git diff --check = PASS`. Existing broad-suite/frozen-E1 failures are separate inherited evidence and were not rerun or repaired by this read-only diagnosis.

```text
WORK_PACKAGE = E2-P04-DEPENDENCY-PROVENANCE-CLOSURE
RESULT = BLOCKED
INITIAL_FAILURE = DEPENDENCY_PROVENANCE
DEPENDENCY_TYPE = ATTEST trust-entity definition source provenance
PROVENANCE_STATUS = COMPLETE_BUT_UNINSTALLED
INSTALLATION_CLASSIFICATION = INSTALL_CONTRACT_INCOMPLETE
INSTALL_OPERATION = INSTALL
INSTALL_AUTHORITY = NO_APPLICABLE_ISSUED_AUTHORITY
DEPENDENCY_INSTALLED = NO
INSTALL_EVENT_ID = NONE
A09_CANDIDATE_REMATERIALIZED = NO
A09_PREFLIGHT = FAIL_CLOSED
NEXT_FAILURE = DEPENDENCY_PROVENANCE
DEPENDENCY_PROVENANCE_CLOSED = NO
P04_EXECUTION_READY = NO
E2_P04_READY = NO
A09_A13_EXECUTED = NO
E2_FINISH_EXECUTED = NO
P03_RESULT = PASS
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN
N_REAL_SATISFIED = NO
RUNTIME_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
