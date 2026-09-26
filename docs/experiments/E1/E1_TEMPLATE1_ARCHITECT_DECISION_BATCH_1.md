# E1 Template-1 Architect decision batch 1

**Review package only. Three decisions are ready: DEC-BINDING, DEC-IGNORED, DEC-VALIDATOR. DEC-EXEC is excluded as FACT_BLOCKED. No answer is selected, authority issued, or state transition applied.**

## Eligibility audit and planner defect

All four persisted DEC prerequisites are completed. Source/plan hashes and all completed-result/source-evidence hashes were verified. Completion is not sufficient proof of decision readiness.

| Persisted actionable decision | Review classification | Included |
|---|---|---|
| DEC-BINDING | DECISION_READY | YES |
| DEC-EXEC | FACT_BLOCKED | NO |
| DEC-IGNORED | DECISION_READY | YES |
| DEC-VALIDATOR | DECISION_READY | YES |

**BATCH1-ACTIONABILITY-01:** DEC-EXEC is persisted ACTIONABLE_NOW, but the S-EXEC dossier provides a gap and an instruction to designate a source, not an exact source/projector or concrete policy alternative. Passing its preparation criterion did not establish every decision input. This task records the defect and excludes the action; it does not modify the historical execution ledger or repair the planner. A subsequent selection must account for this finding before attempting DEC-EXEC.

DEC-BINDING and DEC-VALIDATOR may be decided conditionally before their future schema/source work completes, as Closure Plan §3 explicitly permits. DEC-IGNORED has concrete alternatives; any remaining exact version selection is part of its policy decision rather than an external fact. No factual prerequisite is silently waived.

## Independence

No included decision depends on another included decision, requires its output identity, or invalidates another dossier. They may receive different answers. DEC-IGNORED changes future canonical schema/identity and therefore later validator checks; it does not change the conditional validator grant’s purpose or the binding-subobject scope. Both defer actual work to CONTRACT-T1. No ordering edge is added and no authority semantics are merged.

## Exact current construction envelope

Scope: LIVE_R4/G4/E1-WP-001/FIRST_PROGRAMMER_REQUEST. Runtime: sha256:b6bcbb437f63c1433167103b1c7e15b723190721518e02ff2e4d2523fd625761. G4: AUTHORITY-STORE-GENERATION-sha256:ab07c7cbd889588fd80976bf5c47b7358722eaf6e2e1b7364e612c03899bf9ff.

Release: ReleaseAuthority-sha256:18184991d9ebdddcae05b1ee138dbc2bbef27be72cd6ad07e1515bf4fb29ff1e. Context: OperationalContext-sha256:ff57a2103cdcbfa578a4ce22d774ecea374a34267cdaf8d53385fca916dbc10c. These source references do not themselves supply missing currentness/mapping proofs.

## DEC-BINDING

**DECISION_ID**: DEC-BINDING

**STATUS**: DECISION_READY

**QUESTION**: Authorize at most one provenance-only canonical binding subobject candidate for the exact recorded current envelope, only after all existing source/schema/mapping gates pass?

**EVIDENCE**: [E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_BINDING_GRANT_1_RESULT.md](E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_BINDING_GRANT_1_RESULT.md), [E1_TEMPLATE1_GRAPH_RESOLUTION_S_BINDING_1_RESULT.md](E1_TEMPLATE1_GRAPH_RESOLUTION_S_BINDING_1_RESULT.md), [E1_TEMPLATE1_PRODUCTION_CONTRACT_CLOSURE_PLAN_1.md](E1_TEMPLATE1_PRODUCTION_CONTRACT_CLOSURE_PLAN_1.md)

**OPTIONS**: 

1. Approve only the prepared conditional one-candidate scope.
2. Decline or defer; no construction authority is established.

**RECOMMENDED_MINIMUM_IF_SUPPORTED**: If granting permission, approve only the prepared conditional one-subobject scope; this is the dossier’s expressly bounded least-authority alternative. No recommendation to waive a gate.

**SCOPE**: LIVE_R4/G4/E1-WP-001/FIRST_PROGRAMMER_REQUEST; exact invocation e89c032eb0b0a006b041e3b0ddf0093d8d8b7a7f30882ac21f9ab05b0eb8bbfa and CurrentDispatch ee06120a0b5d6301ab66de62d4b90747e1ddea164ecd635675e369f770775aa3; exact runtime/G4/release/context references in the accepted S-BINDING inventory.

**AUTHORITY_GRANTED_IF_APPROVED**: Only a separately issued/authenticated grant for one BUILD-BINDING provenance-only candidate: canonical subobject bytes, binding_sha256 and source/derivation evidence, after complete inputs and approved schema.

**AUTHORITY_NOT_GRANTED**: No Template-1/Candidate-3 construction or release, WorkAuthorization acceptance/issuance/use, authority consumption, lifecycle/ownership/audit/host/provider/model effects, unrelated repairs, or expansion of existing policy. Preparation grants nothing. No full 22-input map assembly, publication/current-authority registration, new invocation allocation or second candidate.

**DOWNSTREAM_ACTIONS_UNLOCKED**: {"immediate": [], "conditional": ["BUILD-BINDING"], "remaining_gates": ["CONTRACT-T1", "S-ANCESTRY", "MAP-DISPATCH", "MAP-RELEASE", "MAP-CONTEXT_ID"], "already_complete": ["S-BINDING"]}

**REVERSIBILITY / SINGLE-USE LIMITS**: At most one candidate; no automatic retry/reallocation or second construction. Altered/stale scope blocks execution. No cancellation/revocation mechanism is invented by this batch.

**PRODUCTION_EFFECT**: Preparation NO; actual grant issuance is PRODUCTION_EFFECT under plan classification; authorized isolated construction is QUALIFICATION_EFFECT_ONLY.

The authorized object would be one canonical binding subobject and binding_sha256. The later 22-member authenticated_inputs map and its T1 binding_digest are different objects; no full-map, T1 or WorkAuthorization construction is included. Nonrecursive sibling correspondence and exact session/turn source provenance must pass. Input completeness is an execution gate, not asserted by a conditional grant.

## DEC-IGNORED

**DECISION_ID**: DEC-IGNORED

**STATUS**: DECISION_READY

**QUESTION**: Which exact canonical input rule should govern authorization_id, revision, state and ownership_ledger, while preserving their consumer-assigned outputs?

**EVIDENCE**: [E1_TEMPLATE1_GRAPH_RESOLUTION_SEM_IGNORED_1_RESULT.md](E1_TEMPLATE1_GRAPH_RESOLUTION_SEM_IGNORED_1_RESULT.md), [E1_TEMPLATE1_GRAPH_RESOLUTION_SEM_INTERFACES_1_RESULT.md](E1_TEMPLATE1_GRAPH_RESOLUTION_SEM_INTERFACES_1_RESULT.md), [E1_TEMPLATE1_PRODUCTION_CONTRACT_CLOSURE_PLAN_1.md](E1_TEMPLATE1_PRODUCTION_CONTRACT_CLOSURE_PLAN_1.md)

**OPTIONS**: 

1. A: retain all four mandatory keys; exact JSON null for each as the proposed sentinel; require null before overwrite and reject missing keys/non-null values. This is unadopted.
2. B: separately scoped versioned key-contract change excluding exactly these four inputs, requiring the remaining 19, rejecting their presence, and assigning all four outputs explicitly. Approval must name the exact schema version and migration/rejection rule; blank version is not executable approval.
3. Decline/defer. A different sentinel requires an explicitly specified per-key type/value and validation rule, not a blanket approval.

**RECOMMENDED_MINIMUM_IF_SUPPORTED**: NONE. The dossier does not establish which canonical policy the Architect intends; fewer key changes alone does not justify choosing null.

**SCOPE**: Only the four overwritten canonical fields_values inputs and associated validation/schema/identity coverage. Actual InvocationAttemptId/audit sources and runtime assignments remain independently required.

**AUTHORITY_GRANTED_IF_APPROVED**: Only the explicitly selected contract rule (or a separately scoped key-contract change); downstream mapping/validation and implementation still need their existing permissions and acceptance.

**AUTHORITY_NOT_GRANTED**: No Template-1/Candidate-3 construction or release, WorkAuthorization acceptance/issuance/use, authority consumption, lifecycle/ownership/audit/host/provider/model effects, unrelated repairs, or expansion of existing policy. Preparation grants nothing. No guessed authority/source values, bypass of source authentication, hidden defaults or mixed-schema permissiveness.

**DOWNSTREAM_ACTIONS_UNLOCKED**: {"immediate": [], "conditional": ["CONTRACT-T1", "MAP-IGNORED"], "remaining_gates": ["CONTRACT-T1 for MAP-IGNORED; other CONTRACT-T1 semantic/decision predecessors remain unresolved"]}

**REVERSIBILITY / SINGLE-USE LIMITS**: Contract choice is version-bound, not a one-use invocation grant. Changing it requires an explicit contract revision and requalification; old/new formats must not silently mix. No existing artifact is rewritten.

**PRODUCTION_EFFECT**: Preparation NO; an actual governing contract decision is PRODUCTION_EFFECT under the plan; no runtime effect is implied.

| Mandatory current input | Assigned output |
|---|---|
| authorization_id | result[InvocationAttemptId] |
| revision | integer 1 |
| state | string INACTIVE |
| ownership_ledger | result[audit] |

A preserves the 23-key set but needs explicit null validation before overwrite and canonical/runtime type distinction. B changes the canonical set to 19 inputs, requires versioned discrimination and consumer changes to insert the four outputs. Neither fits by merely exploiting the existing overwrite. Both require approved T1 body identity coverage and reject mixed or malformed representations. Actual audit/invocation source proofs remain mandatory; input policy does not resolve them. No sentinel or version is adopted by this batch.

## DEC-VALIDATOR

**DECISION_ID**: DEC-VALIDATOR

**STATUS**: DECISION_READY

**QUESTION**: Issue the narrowly scoped WP-14 shared pure-validator implementation/test grant in the prepared dossier, with implementation gated on CONTRACT-T1?

**EVIDENCE**: [E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_VALIDATOR_1_RESULT.md](E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_VALIDATOR_1_RESULT.md), [E1_TEMPLATE1_GRAPH_RESOLUTION_SEM_INTERFACES_1_RESULT.md](E1_TEMPLATE1_GRAPH_RESOLUTION_SEM_INTERFACES_1_RESULT.md), [E1_TEMPLATE1_PRODUCTION_CONTRACT_CLOSURE_PLAN_1.md](E1_TEMPLATE1_PRODUCTION_CONTRACT_CLOSURE_PLAN_1.md)

**OPTIONS**: 

1. Approve only the bounded active-consumer validation seam and isolated qualification scope, with CONTRACT-T1 prerequisite retained.
2. Decline/defer; validator implementation authority remains absent.

**RECOMMENDED_MINIMUM_IF_SUPPORTED**: If granting permission, approve only the prepared shared-validator seam and §4 tests. The dossier supports no general adapter permission.

**SCOPE**: adapter/workauth_lifecycle.py::consume_and_issue pre-effect stage; adapter/workauth_issuance.py::validate; adapter/invocation_constructor.py canonical checks; directly associated isolated adapter/tests qualification and only helpers necessary for this seam.

**AUTHORITY_GRANTED_IF_APPROVED**: Separately issued/authenticated implementation/test permission for validate_for_issuance(candidate,current_state) and a private shared validation path, subject to accepted CONTRACT-T1.

**AUTHORITY_NOT_GRANTED**: No Template-1/Candidate-3 construction or release, WorkAuthorization acceptance/issuance/use, authority consumption, lifecycle/ownership/audit/host/provider/model effects, unrelated repairs, or expansion of existing policy. Preparation grants nothing. A validator PASS does not authorize acceptance or issuance of WorkAuthorization. No context/governance/transmission repair, budget/identity decision or ignored-key policy is implicitly approved.

**DOWNSTREAM_ACTIONS_UNLOCKED**: {"immediate": [], "conditional": ["IMPL-VALIDATOR"], "remaining_gates": ["CONTRACT-T1"], "implementation_package": "IP-SHARED-VALIDATOR"}

**REVERSIBILITY / SINGLE-USE LIMITS**: Bounded implementation/qualification scope, not a reusable operational authority; exact implementation identity and evidence must be recorded. No production publication permission or automatic runtime migration.

**PRODUCTION_EFFECT**: Preparation NO; actual implementation-grant issuance is PRODUCTION_EFFECT; isolated authorized implementation/tests are QUALIFICATION_EFFECT_ONLY.

Share the entire existing pre-effect decision: byte/parse checks; exact authorization schema/key set and WorkAuthorizationId; canonical binding digest and invocation/dispatch/release/context correspondence; T1 schema/content identity, binding_digest, INACTIVE/NONE and field types; independent source scope/lineage/freshness/mappings; reconstruction/equality; current-state and issuance-authority checks.

Verify the approved T1 body identity before comparing with issuance authority. Do not substitute WorkAuthorizationId or binding_digest for T1 identity. CONTRACT-T1 must supply the currently missing exact body/version rule. One private helper must serve pure validate_for_issuance and consume_and_issue pre-effect stage, with atomic mutable-state freshness recheck before effect; no caller-provided PASS bypass.

Mandatory qualification: differential valid/invalid decisions; malformed bytes/schema/types/keys/digests/stale identities/changed projections; zero-effect PASS and FAIL; unissued/unconsumed/inactive/unowned pure PASS; exactly one shared-helper call before the effect boundary; mutable-generation race rejection; active-consumer imports and exact qualified implementation identity. During validation prohibit audit/issuance, lifecycle, ownership, repository, host and provider/model effects. Isolated implementation edits/tests require a later grant; neither permission to implement nor a validator PASS grants permission to accept/issue WorkAuthorization.

## DEC-EXEC — excluded, informational only

S-EXEC independently established that the three named profile/repository sources do not expose exec_bins and that the contract prohibits deriving permissions from argv. It did not establish global absence of alternatives. Its available branches are: (a) authenticate an existing independent source/projector, if supplied; (b) present an exact separately scoped independent policy proposal for decision; or (c) retain the unresolved state. Neither (a) nor (b) is concretely supplied. These are paths to decision readiness, not approval options in this batch.

Do not invent a permission set, choose empty bins as a default, derive basenames from argv, or turn a generic instruction to designate a source into an authority grant. Existing least-authority bounds are exact current R4/G4/E1 scope, independent source/representation/projection, no allowlist expansion, no weaker comparison and no runtime effect. Eventual accepted DEC-EXEC output would be one prerequisite of MAP-EXEC_BINS and CONTRACT-T1; neither would become ready now because other gates remain. No executable construction is unlocked here.

## Consequences of each possible answer

Approval below means a later exact decision actually issued/authenticated and accepted, not a response to this review package alone. Independent simulation of each approval yields no newly actionable implementation or construction action in the current snapshot.

- **DEC-BINDING approval:** reevaluate root:binding (grant conjunct only). Newly actionable: []. Conditional packages/constructions: ["BUILD-BINDING"]. Outstanding gates: CONTRACT-T1, S-ANCESTRY, MAP-DISPATCH, MAP-RELEASE, MAP-CONTEXT_ID. No condition/slot automatically satisfied.

- **DEC-IGNORED approval:** reevaluate root:ignored (contract-rule conjunct only). Newly actionable: []. Conditional packages/constructions: []. Outstanding gates: CONTRACT-T1 for MAP-IGNORED; other CONTRACT-T1 semantic/decision predecessors remain unresolved. No condition/slot automatically satisfied.

- **DEC-VALIDATOR approval:** reevaluate gate:validator_authority (requires issued/authenticated grant evidence). Newly actionable: []. Conditional packages/constructions: ["IP-SHARED-VALIDATOR"]. Outstanding gates: CONTRACT-T1. No condition/slot automatically satisfied.

For DEC-IGNORED, both A and fully specified B remove only that decision prerequisite; MAP-IGNORED/CONTRACT-T1 still require remaining inputs. B additionally requires explicit version and bounded consumer-contract change scope. Any incomplete alternative is returned for clarification, not counted as accepted. Decline/defer for any item grants nothing and unlocks nothing; it does not prevent independent answers to the other items. Even all three approvals leave CONTRACT-T1 blocked on other semantic decisions and DEC-EXEC/DEC-INTERFACES, so no immediate construction/implementation is unlocked.

## Fact-blocked Architect actions — not presented for decision

- **DEC-EXEC**: Exact independently supported executable-policy source/field and projector, or a concrete proposed independent policy with exact permission/type/scope consequences; existing dossier explicitly includes no permission list. Evidence: [E1_TEMPLATE1_GRAPH_RESOLUTION_S_EXEC_1_RESULT.md](E1_TEMPLATE1_GRAPH_RESOLUTION_S_EXEC_1_RESULT.md).
- **DEC-AUDIT**: Concrete namespace/store selector and evidence of external-to-agent-root placement for current scope. Evidence: [E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_AUDIT_1_RESULT.md](E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_AUDIT_1_RESULT.md).
- **DEC-RUNTIME_HEAD**: Concrete current R4/G4 head selector and exact applicable authority-domain publication target with supporting lineage facts. Evidence: [E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_RUNTIME_HEAD_1_RESULT.md](E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_RUNTIME_HEAD_1_RESULT.md).
- **DEC-SUPERVISOR**: Concrete supervisor selector with authoritative current release/context applicability facts. Evidence: [E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_SUPERVISOR_1_RESULT.md](E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_SUPERVISOR_1_RESULT.md).

DEC-INTERFACES is also excluded (SEMANTICALLY_INCOMPLETE): its SEM-BUDGET and SEM-IMPLEMENTATION prerequisites remain AUTHORITY_REQUIRED. This is carried forward without reopening those tasks. DEC-AUDIT, DEC-RUNTIME_HEAD and DEC-SUPERVISOR remain fact-blocked exactly as their incomplete dossiers record.

## Provenance and preservation

All source snapshots below are raw-file SHA-256. Assertion extraction is read-only compilation; no authority identity is minted. Source identity changes stale derived readiness/consequence findings and require review. The companion JSON retains per-decision evidence, classifications, conditional consequences and the planner defect.

| Source | SHA-256 |
|---|---|
| [E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json](E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json) | `466b98d08f4f3082281d00ffaee9d208967a23738de35a96aeb00f7a38cfbe5d` |
| [E1_TEMPLATE1_TYPED_KNOWLEDGE_GRAPH_1.json](E1_TEMPLATE1_TYPED_KNOWLEDGE_GRAPH_1.json) | `019762515216eccf4b24329cfc1174d240980e55c3b50c3974eb3ce30d25f246` |
| [E1_TEMPLATE1_PRODUCTION_CONTRACT_CLOSURE_PLAN_1.md](E1_TEMPLATE1_PRODUCTION_CONTRACT_CLOSURE_PLAN_1.md) | `bf88220168766599236a22d34f88686fb943bd55682ef4458046d84c36e6eaaf` |
| [E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_BINDING_GRANT_1_RESULT.md](E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_BINDING_GRANT_1_RESULT.md) | `a8659a5bd82d4c4188b882dbd0378c153a1d2ada1c3d55577854fd19ce3f24a3` |
| [E1_TEMPLATE1_GRAPH_RESOLUTION_S_EXEC_1_RESULT.md](E1_TEMPLATE1_GRAPH_RESOLUTION_S_EXEC_1_RESULT.md) | `464f653148b2266151f71bdf6228a154541afe12d0310b1eca7a3cf8a275f9f1` |
| [E1_TEMPLATE1_GRAPH_RESOLUTION_SEM_IGNORED_1_RESULT.md](E1_TEMPLATE1_GRAPH_RESOLUTION_SEM_IGNORED_1_RESULT.md) | `8e071f5f6f7f305bc35e07b2bcb7f77175f54ce03528048522d6db2e0ef7f816` |
| [E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_VALIDATOR_1_RESULT.md](E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_VALIDATOR_1_RESULT.md) | `bf0662e3aeba6128ab4c1b268a626e872c89cdc0eb77edc7c98d262cc4742337` |
| [E1_TEMPLATE1_GRAPH_RESOLUTION_SEM_INTERFACES_1_RESULT.md](E1_TEMPLATE1_GRAPH_RESOLUTION_SEM_INTERFACES_1_RESULT.md) | `2b7bb889f71a4eebabbc2109f4c6c88369c0a8ae7a8b8e5cfd54c7dd2108976f` |
| [E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_AUDIT_1_RESULT.md](E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_AUDIT_1_RESULT.md) | `48bd8c492aa1cbf7cd8b3b7ee31b75e85488dca7ddbf0082965aa1fc44b3dfb1` |
| [E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_RUNTIME_HEAD_1_RESULT.md](E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_RUNTIME_HEAD_1_RESULT.md) | `6ebfe3a8f57ba309cc810fdb27610ad14ee6b048f2a5f989a05e61338b094897` |
| [E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_SUPERVISOR_1_RESULT.md](E1_TEMPLATE1_GRAPH_RESOLUTION_PREP_SUPERVISOR_1_RESULT.md) | `1c1d280b85a3a92e36780776af96c9287a9212780c3fa9a7eff7f4c2e48a7a7e` |
| [E1_TEMPLATE1_GRAPH_RESOLUTION_S_BINDING_1_RESULT.md](E1_TEMPLATE1_GRAPH_RESOLUTION_S_BINDING_1_RESULT.md) | `829ecbd2bba6cbf4cb0c45c8886f80097c754db11d607a296840714569f465b7` |

Only this Markdown package and its JSON companion are created. Plan, graph, authorities, lifecycle, implementation and all prior results remain unchanged. 28 cut conditions and 41 value slots remain unresolved; Candidate-3 construction authority remains valid and unconsumed as recorded.

```text
DECISION_READY = ["DEC-BINDING", "DEC-IGNORED", "DEC-VALIDATOR"]
FACT_BLOCKED = ["DEC-EXEC", "DEC-AUDIT", "DEC-RUNTIME_HEAD", "DEC-SUPERVISOR"]
DECISION_DEPENDENCIES = []
BATCH_SIZE = 3
ARCHITECT_DECISION_REQUIRED = YES
ROOT_CONDITIONS_RESOLVED = 0
SLOTS_RESOLVED = 0
TEMPLATE1_CONSTRUCTION_READY = NO
CANDIDATE3_RESUMPTION_READY = NO
PRODUCTION_EFFECT = NO
```
