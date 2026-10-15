# A15 prospective authority instrument definition — Package 64

`WORK_PACKAGE = E2-P05-D01-A15-PROSPECTIVE-AUTHORITY-INSTRUMENT-64`

`RESULT = PARTIAL`. The typed qualification schema, proposed mandate content, exact technical subject bindings and non-circular identity rules are complete. **The instrument content remains explicitly incomplete:** current issuer identity/role, applicable issuing power, governing adoption/version and mandate-composition/lifecycle authority are unbound. `ISSUANCE_READY = NO`, `EXECUTION_AUTHORIZATION_READY = NO`, and `DECISION_READY = NO`. No approval option, instrument, issuance event or execution grant is issued.

Package 63's 24 sealed files, Package 62's 25 and Package 61's 40 match exactly. The 42-record authority inventory and its four insufficient records are preserved. Both oracle/variant definitions, the nineteen checkpoint ledger files, static harness, protection policy, frozen acceptance, exact authority-subject evidence and historical exclusions are unchanged. All 17,475 original runtime/E1/retained file hashes match. V3, the native authority schema and Planner runtime remain unchanged.

The [typed schema](qualification/E2_P05_D01_A15_PROSPECTIVE_AUTHORITY_INSTRUMENT_64/typed-instrument-schema.json) defines every requested field, exact native-compatible `ArtifactIdentity(kind, namespace, sha256)` structure, nested mandate/boundary/prerequisite shapes and explicit unbound-draft rules. It validates with the installed JSON Schema Draft 7 validator. A complete proposed status requires non-null issuer/role and verified external designation/power evidence; the current incomplete draft cannot pass that condition. No new `AuthorityClass` enum or native `GraphEntity` is constructed. Existing `DECIDE`, `ISSUE`, `USE`, `INSTALL` or `ATTEST` labels are not used as blanket equivalents of the three mandates.

The exact [draft content](qualification/E2_P05_D01_A15_PROSPECTIVE_AUTHORITY_INSTRUMENT_64/proposed-instrument-content.json) uses Package 63's identifier `A15-BOUNDED-PROSPECTIVE-QUALIFICATION-AUTHORITY-INSTRUMENT-PROPOSAL-1`, proposed version **1**, status `PROPOSED_INCOMPLETE_NOT_ISSUED`. Version 1 is a pinned proposed definition, not evidence of an existing governing authority version. The field named `AUTHORIZED_SUBJECT` binds Package 62's technical preparation identity; that field name does not make its subject authorized.

| Definition term | Bound value/status |
|---|---|
| Technical subject | `CONTENT_IDENTITY/qualification-A15-technical-preparation-subject-v1:befe07aacc6b4c4e203488bce731f265a0520cf145174dca33dbfb4e68b43e9b` |
| Starting Snapshot | `CONTENT_IDENTITY/planner-snapshot-v1:ce54ff49907abcad564ec0ddfe8c7a019fab129936172b67f4ce0ff5ed013586` |
| Starting bundle | `CONTENT_IDENTITY/planner-bundle-v1:6dcd63b9cb4b6e6b074bd8112f24bf2c570615e1acab38c7afcb63df606ab0e0` |
| Variants/oracles | Both exact Package 62 variant records and Package 61 full oracle identities/pins, without wildcard selection |
| Harness | Exact `qualification-A15-static-harness-binding-v1` identity and eight component pins; specification only, not activated executable |
| Scope/lineage/generation | `E2-QUALIFICATION-ONLY` / `E2-P03-PROSPECTIVE-QUALIFICATION-1` / `E2-P03-PROSPECTIVE-GENERATION-1` |
| Protection | All 53 direct-protected content identities, protected objects/history/context/policy and both complete frame oracles |
| Publication | Exact two namespaces, save targets, native ledger filenames/byte hashes, handoffs, exit and reader evidence paths from original manifests |
| Operation budget | One supervisor; two writers/initial restores; two caller-level record/save operations; eight cold-reader restores; zero separate pre-apply calls and zero retries |
| Current issuer/role | Explicitly null; historical role precedents retained as evidence only |

Every field has a [value/provenance record](qualification/E2_P05_D01_A15_PROSPECTIVE_AUTHORITY_INSTRUMENT_64/field-value-provenance.json): field name, value, exact retained source/pointer or explicitly proposed definition, authority status, identity effect and validation rule. The mandate values are exact proposed content; they are not evidence that anyone presently has authority to issue them.

The normative section binds Package 59's fixed accepted ROOT/SLOT admission-provenance boundary, exact owner/source relationships, requiredness distinction, two singleton content identities, nonempty protection policy and prospective assurance limits. It adopts no historical general source universe, changes no frozen acceptance, rewrites no proof declaration and suppresses no usable alternative. Native `ALL`/`ANY` remains authoritative.

The execution section binds only the two sealed variants from independent copies of the original checkpoint. It permits no additional source, variant, unrelated operation or source/event/parent repinning. Required proof/state/control/resume comparisons are the exact independent Package 61 outputs. A prospective permission is still absent: proposed text cannot execute or install itself.

The capture section binds `record_result → save_bundle → restore`, distinct immutable outputs, supervisor-observed successful writer exit, persisted handoffs, four fresh cold readers per variant under seeds `0,1,7,101`, complete bytes/replay/output comparisons, no HEAD/E1/production mutation and no A14 authority transfer. The original file-fsync-before-hard-link assurance is preserved; directory/general crash durability is not added. The selected V3 prior-bundle dispatch remains unchanged; unsealed supervisor/worker/invocation activation is excluded.

The [mandate separation analysis](qualification/E2_P05_D01_A15_PROSPECTIVE_AUTHORITY_INSTRUMENT_64/mandate-separation-analysis.json) distinguishes **one draft instrument containing three separately identified mandate sections** from legal permission to issue combined authority. `COMBINED_INSTRUMENT_PERMITTED = UNDETERMINED`; a requirement for three separate instruments is likewise not established. The issuer must independently possess power for adoption, execution and capture. Pending actual composition evidence, the proposed fail-closed sequence remains qualification of issuer/instrument power, explicit normative adoption, then explicit execution and capture approval. Neither adoption nor execution permission implies another mandate or that an execution occurred.

The [issuer matrix](qualification/E2_P05_D01_A15_PROSPECTIVE_AUTHORITY_INSTRUMENT_64/issuer-delegation-qualification-matrix.json) qualifies no current A15 issuer. Historical I04/F03 `AUTHENTICATED_HUMAN_USER` / `QUALIFICATION_AUTHORITY` records remain `UNDETERMINED` for new A15 power. The exact E2-DECIDE role and E1 Architect continuation delegation are `UNQUALIFIED` for this A15 subject. A specifically delegated engineering issuer remains `UNDETERMINED`, with null role/delegation evidence; an engineering title does not supply issuing power. Any other role requires an actual authoritative definition. A direct qualified owner need not fabricate an intermediate delegation, but delegated authority must evidence the full chain and limits.

The digest `CONTENT_IDENTITY/qualification-A15-incomplete-instrument-content-v1:d67e58aded1b058143ad422fa784cdf81d206fc7dd0e8e9a3a10e87b1cacac78` identifies the exact **incomplete draft**, including its explicit null issuer fields. It is not a completed normative knowledge-contract ID or authority identity. Filling those fields changes content and requires resealing. Its hash covers only the content object; the identity wrapper and future approvals/receipts are excluded.

[Identity separation](qualification/E2_P05_D01_A15_PROSPECTIVE_AUTHORITY_INSTRUMENT_64/instrument-identity-separation.json) leaves `ISSUED_INSTRUMENT_IDENTITY`, `ISSUANCE_EVENT_IDENTITY` and `AUTHORIZED_EXECUTION_GRANT_IDENTITY` null. The future dependency order is external issuer-power evidence, verified issuing role, exact final content/version and scope approval, distinct execution/capture approvals, issued document, separately evidenced issuance occurrence, then exact execution grant. The issued document's own identity and later event/grant identities are excluded from its hash. No native Planner authority-issuance event is fabricated, and the two expected A15 event identities are unchanged. The dependency graph is acyclic; a grant-to-issuer back edge fails verification. These are proposed identity/qualification rules, not an already adopted governance mechanism.

The [issuance prerequisites](qualification/E2_P05_D01_A15_PROSPECTIVE_AUTHORITY_INSTRUMENT_64/issuance-prerequisite-inventory.json) distinguish exact subject/protection/exclusions/content verification from unverified issuer, direct-or-delegated power, governing version/adoption, per-mandate power, composition and effective/lifecycle rules. Proposed version 1 being sealed does not pass governing version adoption. Structural qualification is not independent qualification of issuing power. No mandatory unresolved prerequisite may become issued.

The proposed lifecycle rule denies activation if issuer power or actual effective/revocation/expiration/supersession status is absent, ambiguous or unverifiable; pins, subject, context or budgets change; or the fixed successful-use boundary is exceeded. Its governing authority is null. No date, TTL or expiration event is invented. This rule proposes fail-closed behavior without purporting to revoke an existing grant. Zero retries remain the initial limit; any future retry needs separately evidenced exact permission and starts only from the original immutable checkpoint.

The exact external gap is [A64-EXTERNAL-A15-ISSUER-POWER-AND-INSTRUMENT-ADOPTION](qualification/E2_P05_D01_A15_PROSPECTIVE_AUTHORITY_INSTRUMENT_64/issuer-delegation-gap-dossier.json). It requires actual current subject-bound issuer/role designation and direct/delegated power; the governing accepted instrument/version; independent normative/execution/capture mandates; and composition/effective/revocation/expiration evidence. The proposed instrument cannot supply its own credential or delegation. A future issued grant is not demanded before preparing a proposal, but the actual governing mechanism must be evidenced before approval options or issuance readiness can be claimed.

Independent verification reloads retained inputs, validates the typed schema and exact field/source equalities, checks effective/output/protection/budget bindings, recomputes the incomplete draft digest with a separate encoder, verifies identity acyclicity, and rejects inferred issuer/composition power. All **19/19 static negative controls pass**, including wrong issuer/version/subject, missing mandate/delegation, scope expansion, A14 substitution, proof/event mutation, new variant, wrong checkpoint/oracle, missing protection, retry/E1/production expansion and self-authorizing/circular identity claims. Four fresh static verifier processes agree. These are not native cold readers or runtime fault injection.

LL-01 through LL-10 retain their identities and prior event prefix. Ten evidence reviews were appended, with no duplicate/new lesson, quantified efficiency gain or validated causal attribution.

```text
WORK_PACKAGE = E2-P05-D01-A15-PROSPECTIVE-AUTHORITY-INSTRUMENT-64
RESULT = PARTIAL
PACKAGE_63_AUTHENTICATED = YES
INSTRUMENT_SCHEMA_COMPLETE = YES
PROPOSED_INSTRUMENT_COMPLETE = NO
ISSUER_IDENTITY = UNBOUND
ISSUER_ROLE = UNBOUND
ISSUER_AUTHORITY_VERIFIED = NO
AUTHORITY_VERSION = 1 PROPOSED_ONLY; GOVERNING_ACCEPTED_VERSION_UNBOUND
NORMATIVE_MANDATE_COMPLETE = YES PROPOSED_CONTENT_ONLY
EXECUTION_MANDATE_COMPLETE = YES PROPOSED_CONTENT_ONLY
CAPTURE_MANDATE_COMPLETE = YES PROPOSED_CONTENT_ONLY
COMBINED_INSTRUMENT_PERMITTED = UNDETERMINED
AUTHORITY_SUBJECT_VERIFIED = YES
ISSUANCE_READY = NO
DECISION_READY = NO
MISSING_AUTHORITY_EVIDENCE = [A64-EXTERNAL-A15-ISSUER-POWER-AND-INSTRUMENT-ADOPTION]
NEGATIVE_SUITE = 19/19 PASS STATIC
FOUR_SEED_DETERMINISM = PASS
LESSONS_REVIEWED = 10
NEW_LESSONS = 0
TOTAL_REFERENCES = 161
TOTAL_RESOLVED = 109
TOTAL_UNRESOLVED = 52
NEXT_CRITICAL_BLOCKER = EXTERNAL_CURRENT_ISSUER_POWER_AND_GOVERNING_INSTRUMENT_ADOPTION
A15_EXECUTED = NO
A16_EXECUTED = NO
A14_PERSISTENCE_RERUN = NO
NORMATIVE_AUTHORITY_ISSUED = NO
EXECUTION_AUTHORITY_ISSUED = NO
BASELINE_AMENDED = NO
END_INTERFACES_BOUND = 4/6
P05_EXECUTION_READY = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```
