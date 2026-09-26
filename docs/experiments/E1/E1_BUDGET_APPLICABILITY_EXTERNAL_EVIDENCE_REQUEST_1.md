# E1 budget applicability — external evidence request 1

External gate: **EXT-BUDGET-APPLICABILITY-EVIDENCE**. This is an evidence contract, not applicability evidence or authority. **CONTROL_STATE = WAITING_FOR_EXTERNAL_EVIDENCE; ACTIONABLE = []; NEXT_ACTION = NONE.** The request is prepared but has not been sent. No receipt or reentry action is run.

## Exact subject

Every response must identify the exact source and target below. These are recorded identifiers, not new applicability assertions.

```json
{
  "budget_authority": "StatusBudgetAuthority-sha256:02cc22de4ad70612c8b1e39e4df6f3bf8733c777d4729fb66d59d519fc6edc99",
  "target_invocation": "InvocationAttempt-sha256:e89c032eb0b0a006b041e3b0ddf0093d8d8b7a7f30882ac21f9ab05b0eb8bbfa",
  "target_dispatch": "CurrentDispatch-sha256:ee06120a0b5d6301ab66de62d4b90747e1ddea164ecd635675e369f770775aa3",
  "target_context": "OperationalContext-sha256:ff57a2103cdcbfa578a4ce22d774ecea374a34267cdaf8d53385fca916dbc10c",
  "target_release": "ReleaseAuthority-sha256:18184991d9ebdddcae05b1ee138dbc2bbef27be72cd6ad07e1515bf4fb29ff1e",
  "source_scope": "LIVE_R4/G4/E1-WP-001/FIRST_PROGRAMMER_EXECUTION",
  "target_scope": "LIVE_R4/G4/E1-WP-001/FIRST_PROGRAMMER_REQUEST",
  "recorded_lineage": "R4-final CURRENT UNIQUE",
  "runtime": "sha256:b6bcbb437f63c1433167103b1c7e15b723190721518e02ff2e4d2523fd625761",
  "controller_store": "AUTHORITY-STORE-GENERATION-sha256:ab07c7cbd889588fd80976bf5c47b7358722eaf6e2e1b7364e612c03899bf9ff",
  "programmer_profile": "ProgrammerProfile-sha256:0a0718f285a942c13a9f00e4b367cbea2394937fa18c4d7e11ed2c6c2803dd67"
}
```

The prior fact-acquisition attempt ended with EXTERNAL_GATE_REQUIRED and remains BLOCKED in the ledger; it is not a completed proof. Local source authenticity/identity and reference consistency do not settle the eight current obligations.

## Common evidence acceptance contract

- **identity**: Name exact pinned source and target identities, artifact content identities, identity domains and canonicalization rules. No all-SHA256 equivalence.
- **scope**: Bind this exact invocation/dispatch/context and recorded source/target phases; broader E1 scope or copied strings are insufficient.
- **lineage**: Show authenticated lineage binding and current selection, not merely the recorded R4-final CURRENT UNIQUE label.
- **currentness**: Supply owning snapshot/checkpoint/event generation, observation/capture point and governing validity/freshness rule, plus an independently trusted current anchor against which that generation is checked. Timestamp alone is insufficient; no invented TTL. State revocation/supersession/single-use uncertainty explicitly.
- **authentication**: Recompute artifact identities from retrievable exact bytes using the source identity rule; authenticate producer competence through existing trusted authority chain/store/channel and bind evidence to subject/snapshot. A self-hash, arbitrary signature or new exchange wrapper is not authority. Missing trust rule/anchor => evidence unvalidated.
- **rejection**: Reject malformed/duplicate-key/type-confused data, wrong subject/source, unverifiable bytes, unsupported producer authority, incomplete derivations, mismatched scope/generation, stale/incompatible proof or reliance on unsupported inference. Reject evidence as sufficient without pretending absent evidence disproves applicability.

## Eight independently required propositions

### BUDGET-PROOF-AVAILABILITY_PUBLICATION

- **Proposition**: Exact referenced authority is available from its competent owning domain and published/registered as required for this target, or governing rule explicitly proves publication not required.
- **Producer**: Existing authority publisher/store owner with competence for this authority.
- **Artifact/record type**: Authenticated catalog membership/resolution receipt or publication record, with governing publication rule; not a local-file existence report.
- **Identity**: Exact budget authority plus owning store/domain, publication record content ID and returned body hash.
- **Scope**: Bind this exact invocation/dispatch/context and recorded source/target phases; broader E1 scope or copied strings are insufficient.
- **Lineage**: Show authenticated lineage binding and current selection, not merely the recorded R4-final CURRENT UNIQUE label.
- **Time/generation/currentness**: Current catalog generation/checkpoint and validity rule applicable at receipt; publication time alone insufficient.
- **Authentication**: Recompute artifact identities from retrievable exact bytes using the source identity rule; authenticate producer competence through existing trusted authority chain/store/channel and bind evidence to subject/snapshot. A self-hash, arbitrary signature or new exchange wrapper is not authority. Missing trust rule/anchor => evidence unvalidated.
- **Rejection criteria**: Local Markdown existence; ISSUED label; stale catalog; missing membership; no-publication claim without governing rule.

### BUDGET-PROOF-SCOPE

- **Proposition**: Source EXECUTION-scoped authority applies to budget reference use for the exact REQUEST construction subject under an existing governing rule.
- **Producer**: Existing governing scope/contract authority and competent current target source.
- **Artifact/record type**: Authenticated scope-binding/contract decision or adopted rule plus exact application proof; decision must already exist, not be created by receipt.
- **Identity**: Name exact pinned source and target identities, artifact content identities, identity domains and canonicalization rules. No all-SHA256 equivalence.
- **Scope**: Bind this exact invocation/dispatch/context and recorded source/target phases; broader E1 scope or copied strings are insufficient.
- **Lineage**: Show authenticated lineage binding and current selection, not merely the recorded R4-final CURRENT UNIQUE label.
- **Time/generation/currentness**: Rule version/effective generation and target checkpoint must be applicable together.
- **Authentication**: Recompute artifact identities from retrievable exact bytes using the source identity rule; authenticate producer competence through existing trusted authority chain/store/channel and bind evidence to subject/snapshot. A self-hash, arbitrary signature or new exchange wrapper is not authority. Missing trust rule/anchor => evidence unvalidated.
- **Rejection criteria**: Prefix similarity; budget equality; unadopted interpretation; DEC-BUDGET representation approval substituted for applicability.

### BUDGET-PROOF-LINEAGE

- **Proposition**: Source and target are governed by the applicable current R4 lineage with no disqualifying supersession.
- **Producer**: Competent release/lineage selection authority.
- **Artifact/record type**: Current lineage/adoption/selection record or authenticated relevant chain and selection proof.
- **Identity**: Name exact pinned source and target identities, artifact content identities, identity domains and canonicalization rules. No all-SHA256 equivalence. Include lineage/head/selection identity. 
- **Scope**: Bind this exact invocation/dispatch/context and recorded source/target phases; broader E1 scope or copied strings are insufficient.
- **Lineage**: Show authenticated lineage binding and current selection, not merely the recorded R4-final CURRENT UNIQUE label.
- **Time/generation/currentness**: Current selection generation, applicable chain position and supersession status under owning rule.
- **Authentication**: Recompute artifact identities from retrievable exact bytes using the source identity rule; authenticate producer competence through existing trusted authority chain/store/channel and bind evidence to subject/snapshot. A self-hash, arbitrary signature or new exchange wrapper is not authority. Missing trust rule/anchor => evidence unvalidated.
- **Rejection criteria**: Copied lineage string; old selection; missing chain link; selection for different target/generation.

### BUDGET-PROOF-RUNTIME

- **Proposition**: Exact source runtime binding is independently authenticated and applicable to current target runtime.
- **Producer**: Competent runtime/content and runtime selection/release owners.
- **Artifact/record type**: Authenticated runtime content/selection binding and governing applicability rule; retrievable bytes or qualified proof under that rule.
- **Identity**: Exact pinned runtime CONTENT_IDENTITY plus owning selection/content evidence IDs; never another SHA-256 domain.
- **Scope**: Bind this exact invocation/dispatch/context and recorded source/target phases; broader E1 scope or copied strings are insufficient.
- **Lineage**: Show authenticated lineage binding and current selection, not merely the recorded R4-final CURRENT UNIQUE label.
- **Time/generation/currentness**: Current applicable runtime selection checkpoint and source-target binding freshness.
- **Authentication**: Recompute artifact identities from retrievable exact bytes using the source identity rule; authenticate producer competence through existing trusted authority chain/store/channel and bind evidence to subject/snapshot. A self-hash, arbitrary signature or new exchange wrapper is not authority. Missing trust rule/anchor => evidence unvalidated.
- **Rejection criteria**: Matching runtime references only; unverifiable content/selection linkage; obsolete/different runtime; unsupported byte-domain conversion.

### BUDGET-PROOF-CONTROLLER_STORE_G4

- **Proposition**: Exact G4 generation is applicable to source/target resolution and the authority belongs to the competent current owning domain.
- **Producer**: Competent controller-store generation/catalog owner.
- **Artifact/record type**: Authenticated generation identity and authority resolution/membership proof, with trust/selection chain.
- **Identity**: Exact G4 generation ID; owning catalog/resolution record IDs; exact authority and target IDs.
- **Scope**: Bind this exact invocation/dispatch/context and recorded source/target phases; broader E1 scope or copied strings are insufficient.
- **Lineage**: Show authenticated lineage binding and current selection, not merely the recorded R4-final CURRENT UNIQUE label.
- **Time/generation/currentness**: Current generation selection and catalog checkpoint; coherent with all other evidence.
- **Authentication**: Recompute artifact identities from retrievable exact bytes using the source identity rule; authenticate producer competence through existing trusted authority chain/store/channel and bind evidence to subject/snapshot. A self-hash, arbitrary signature or new exchange wrapper is not authority. Missing trust rule/anchor => evidence unvalidated.
- **Rejection criteria**: Copied G4 reference; guessed directory; membership in different generation; stale or untrusted catalog.

### BUDGET-PROOF-PROGRAMMER_PROFILE

- **Proposition**: The exact pinned ProgrammerProfile is authenticated and governs the target where required; or governing rule explicitly establishes check is not applicable.
- **Producer**: Competent ProgrammerProfile owner and target-binding authority.
- **Artifact/record type**: Owning profile bytes/identity proof plus authoritative target-profile applicability binding.
- **Identity**: Exact ProgrammerProfile identity and owner-record ID; no substitution of released-profile/content/root identities.
- **Scope**: Bind this exact invocation/dispatch/context and recorded source/target phases; broader E1 scope or copied strings are insufficient.
- **Lineage**: Show authenticated lineage binding and current selection, not merely the recorded R4-final CURRENT UNIQUE label.
- **Time/generation/currentness**: Applicable profile version and current target binding checkpoint; explicit supersession status.
- **Authentication**: Recompute artifact identities from retrievable exact bytes using the source identity rule; authenticate producer competence through existing trusted authority chain/store/channel and bind evidence to subject/snapshot. A self-hash, arbitrary signature or new exchange wrapper is not authority. Missing trust rule/anchor => evidence unvalidated.
- **Rejection criteria**: Matching copied references; wrong profile identity domain; absent owning bytes/proof; omission without governing non-applicability rule.

### BUDGET-PROOF-TEMPORAL_CURRENTNESS

- **Proposition**: Source remains valid for this exact target at evaluation: relevant revocation, supersession and single-use state meet existing governing rules.
- **Producer**: Competent owning authority/current-state or usage-ledger producer under existing policy; concrete producer unknown.
- **Artifact/record type**: Authenticated current validity/usage snapshot or events sufficient to reconstruct it, including governing evaluation rule and trusted current anchor.
- **Identity**: Exact budget/source and invocation identity; snapshot/event IDs; governing rule identity.
- **Scope**: Bind this exact invocation/dispatch/context and recorded source/target phases; broader E1 scope or copied strings are insufficient.
- **Lineage**: Show authenticated lineage binding and current selection, not merely the recorded R4-final CURRENT UNIQUE label.
- **Time/generation/currentness**: Supply owning snapshot/checkpoint/event generation, observation/capture point and governing validity/freshness rule, plus an independently trusted current anchor against which that generation is checked. Timestamp alone is insufficient; no invented TTL. State revocation/supersession/single-use uncertainty explicitly.
- **Authentication**: Recompute artifact identities from retrievable exact bytes using the source identity rule; authenticate producer competence through existing trusted authority chain/store/channel and bind evidence to subject/snapshot. A self-hash, arbitrary signature or new exchange wrapper is not authority. Missing trust rule/anchor => evidence unvalidated.
- **Rejection criteria**: FRESH defaults; stable content hash; old NOT_ACTIVATED; issue date alone; absent trusted current anchor; unknown usage/revocation status; contradictory snapshots.

### BUDGET-PROOF-EXECUTION_REQUEST_PHASE

- **Proposition**: Existing phase semantics permit this EXECUTION authority as the budget reference in REQUEST preconstruction without authorizing execution or consuming authority.
- **Producer**: Competent governing phase/contract authority; current target producer supplies facts only.
- **Artifact/record type**: Existing adopted phase rule or scoped applicability decision plus exact source/target application and exclusions.
- **Identity**: Exact rule/decision identity and pinned source/target identities.
- **Scope**: Bind this exact invocation/dispatch/context and recorded source/target phases; broader E1 scope or copied strings are insufficient.
- **Lineage**: Show authenticated lineage binding and current selection, not merely the recorded R4-final CURRENT UNIQUE label.
- **Time/generation/currentness**: Rule effective generation and coherent current target phase snapshot.
- **Authentication**: Recompute artifact identities from retrievable exact bytes using the source identity rule; authenticate producer competence through existing trusted authority chain/store/channel and bind evidence to subject/snapshot. A self-hash, arbitrary signature or new exchange wrapper is not authority. Missing trust rule/anchor => evidence unvalidated.
- **Rejection criteria**: Assumed EXECUTION=>REQUEST implication; unadopted proposal; technical compatibility treated as permission; expansion to runtime/issuance/use.

A record may report incompatibility, revocation or stale state. Such authenticated negative facts must be preserved as DISPROVED where they actually refute a proposition; lack of evidence is not disproof. Stale evidence cannot prove current applicability, even when its past content is authentic.

## Minimum evidence set

Request **one logical current-applicability bundle**, containing two irreducible proof components:

1. **CURRENT_SUBJECT_SNAPSHOT**: current availability/publication, lineage, runtime, G4, required profile and validity/usage evidence, with governing rules and independently trusted current checkpoint.
2. **GOVERNING_APPLICABILITY_RULE_AND_APPLICATION**: existing adopted scope/phase rule or issued decision and its explicit application to the pinned source and target, without runtime authority expansion.

One existing authoritative record may contain both components and prove all eight propositions if its authenticated producer is competent for each claim and the proofs, anchors and governing rules are explicit. Otherwise include supporting source records from their competent owners. The bundle’s hash cannot confer authority on its contents. No requirement for eight files is imposed. No global minimum physical artifact count is claimed: actual source formats, trust chains and producer availability are unknown. Full bytes or explicitly admitted retrievable evidence for every necessary reference must be supplied; unsupported cross-references do not close obligations.

## Producer identification and access

| Expected owner | Evidence | Forge access / external production | Authority boundary |
|---|---|---|---|
| Authority publisher / controller-store catalog or generation owner | Current availability, publication, owning-domain resolution, G4 checkpoint | May read explicitly supplied/admitted exact bytes; no endpoint or request transport established. Cannot send a request autonomously. If not already available, external owner must provide it. | Reading existing records may be non-effecting; publication/current-state attestation generation requires producer existing scope or separately obtained authority, never granted here. |
| Release/lineage/runtime and ProgrammerProfile owning authorities | Applicable lineage/runtime/profile and target bindings | Same bounded supplied-evidence rule; no recursively followed references. Owner must supply authentic records if absent. | Existing source export only under its existing permissions; new selection/release/authority is separate. |
| Current validity / revocation / usage evidence owner | Fresh authoritative state and trusted current anchor under governing rule | Read supplied qualified evidence only. Owner may be controller, ledger service or another source only if governing contract establishes competence. | Must not consume single-use authority or modify lifecycle to produce evidence; any required effect needs separate authority. |
| Existing governing scope/phase contract authority | Applicable adopted rule or already issued bounded decision | Read provided existing authority record; cannot manufacture applicability. If no rule exists, later fact-complete dossier/readiness/Architect decision is separate; this request is not that decision. | Any new Architect grant is explicitly outside receipt/request authority. |

No concrete qualified producer, endpoint, supervisor or external controller is invented. The expected roles above must prove their competence. Forge can read an explicitly admitted submission; network requests, messages, new source creation or publication are not authorized by this artifact. New Architect applicability authority, if eventually needed, is separate from evidence production and receipt.

## RECEIVE-BUDGET-APPLICABILITY-EVIDENCE

Defined here as a deterministic, bounded receipt action; not executed and not made actionable without a submission. Its prerequisites are:
- Concrete evidence submission exists with gate/target identifiers, exact bounded file/byte manifest and claimed coverage.
- User/authorized delivery admits receipt of exact bytes; external fetches require explicit bounded source/transport authorization.
- Existing trust anchors and governing identity/validation rules are available; missing anchors block, not self-authenticate.

Required submission metadata:
- request_id
- external_gate
- exact subject pins
- artifact manifest: locator or inline bytes, raw content hash, declared identity and identity rule
- producer identity/domain and existing competence proof references
- per-obligation claim with evidence IDs, precise source pointers and explicit governing derivation
- snapshot/generation and governing freshness rule with trusted current anchor
- contradictions, unknowns and negative findings

The exchange wrapper is not a new authority schema. Preserve original source bytes and identity algorithms. Missing mandatory fields are not filled by the receiver.

Validation sequence:
1. Freeze exact receipt bytes and source identities; reject ambiguous parsing/duplicate keys or identity/type confusion.
2. Authenticate every necessary producer/competence chain under existing trusted rules, independently recompute identities and reject digest substitutions.
3. Check exact subject, source/target phase, lineage, runtime/store/profile bindings and coherent snapshot/current anchor.
4. Evaluate each of eight propositions separately using explicit governing derivations only; record PROVED, DISPROVED, EVIDENCE_NOT_FOUND, AUTHORITY_DECISION_REQUIRED or EXTERNAL_EVIDENCE_REQUIRED.
5. Persist supported observations and provenance; no authority inference, evidence repair or silent fill-in. Negative evidence is retained without authorizing use.
6. Emit content-addressed validation receipt and proof matrix; only accepted full current positive coverage enables the bounded FACT revalidation attempt.

Receipt outcomes:
- **ACCEPTED_COMPLETE**: All required positive proofs accepted; schedule FACT-BUDGET-APPLICABILITY revalidation, do not execute it automatically.
- **ACCEPTED_PARTIAL**: Retain only proved observations; keep remaining external gate, no full reentry.
- **NEGATIVE_EVIDENCE**: Preserve authenticated incompatibility/staleness against named proposition; gate not satisfied, REEVAL remains blocked.
- **REJECTED**: Malformed/untrusted/inapplicable/stale-as-positive or contradictory input cannot establish applicability. Preserve rejection provenance; do not repair.
- **AUTHORITY_BRANCH**: Technical evidence complete but no governing applicability rule: record separate decision-input requirement, not permission or a ready decision.

Every assertion retains exact artifact identity/path, field location, authoritative owner/rule, subject/generation, extraction method and validation result. Request or receipt existence is not proof. Any changed source, target, rule or relevant current generation stales dependent positive assertions pending revalidation.

## Deterministic reentry

EXT-BUDGET-APPLICABILITY-EVIDENCE -> RECEIVE-BUDGET-APPLICABILITY-EVIDENCE -> FACT-BUDGET-APPLICABILITY revalidation -> REEVAL-BUDGET.

Only independently accepted evidence may close a proof obligation. Complete positive receipt permits a new bounded FACT attempt, not an automatic PASS; its accepted full proof permits a new REEVAL attempt. Partial receipt preserves partial facts and waiting gates. Authenticated incompatibility/staleness preserves the exact negative finding and keeps REEVAL blocked. Original historical attempts remain immutable. If facts become complete but a normative applicability grant is missing, stop at the separate decision-input/readiness route; receipt cannot create the grant. MAP-BUDGET, Template-1, Candidate 3 and all runtime effects remain outside scope.

## Generic external-gate lifecycle

The plan has the external hold and revalidation route but not a complete delivery/receipt lifecycle. The missing generic concept is specified here, without implementing other gates or modifying planner state.

| State | Entry/exit evidence |
|---|---|
| EXTERNAL_EVIDENCE_REQUIRED | Accepted bounded action lacks proof; exact gate and obligations recorded. |
| EVIDENCE_REQUEST_READY | This complete request specifies evidence, trust/currentness requirements, receipt and reentry; still no evidence. |
| WAITING_FOR_EXTERNAL_EVIDENCE | Request prepared, no admitted evidence, no eligible internal action. Sending is a separate explicit operation; waiting does not assert delivery. |
| EVIDENCE_RECEIVED | Exact submitted bytes and source manifest recorded; no acceptance implied. |
| EVIDENCE_VALIDATED | Per-obligation authentication/validation completed; positive, partial or negative result distinct. |
| DEPENDENT_ACTION_REENTRY | Only accepted full positive matrix enables FACT revalidation; only its accepted proof enables REEVAL new attempt; no historical outcome rewritten. |

Partial/failed validation returns to the explicit waiting or rejection state without marking the gate satisfied. Waiting is event-driven: only an admitted evidence submission or explicit new control input can advance it. Elapsed time, repeated LLM reasoning or the request’s existence cannot create actionability.

## Current control disposition

EVIDENCE_REQUEST_READY is established by this artifact; the task now formally hands control to WAITING_FOR_EXTERNAL_EVIDENCE. This is not a claim that a request was delivered. No submission is present, so the receipt action is not internally executable and the persisted empty actionable set remains correct. No additional LLM reasoning is requested. Stop here.

## Provenance and state preservation

- `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_PLAN_1.json` — SHA-256 `b3c4733bff12052978b39c1d08295137d0825b449adc08fba5ea08002be9b760` — execution_state and budget_applicability_reentry_semantics.
- `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_FACT_BUDGET_APPLICABILITY_1_RESULT.md` — SHA-256 `6b3f486f72b1beeca3ae3a2beb6b1a3e5156f4d85ee35068bf5f6cb1f0d46b2d` — bounded result and external gate.
- `docs/experiments/E1/E1_TEMPLATE1_GRAPH_RESOLUTION_FACT_BUDGET_APPLICABILITY_1_RESULT.json` — SHA-256 `bb566f2e7b42157ea0b783a39e5b06de970ad367e33c738275416afa88284232` — proof_matrix and source_manifest.
- `docs/experiments/E1/E1_BUDGET_APPLICABILITY_REENTRY_1.md` — SHA-256 `00d935e5ed63b9ce86192a7de9d142640280cf798d63bd4ae40e2cdc900dd1e3` — proof obligations and existing reentry rule.
- `docs/experiments/E1/E1_TEMPLATE1_ARCHITECT_DEC_BUDGET_AUTHORITY_1.json` — SHA-256 `2439eeb699057196323ed5373dc72082c4a7210d745713995a9c3e2fd494e1f4` — approved representation and exclusions.
- `docs/experiments/E1/E1_TEMPLATE1_TYPED_KNOWLEDGE_GRAPH_1.json` — SHA-256 `7964c9eea0b00e0198f9f698b6efbd1b2d88d7a48e5266731e67c2408835e399` — current typed-state baseline.

Only this request and its JSON companion are created. Existing planner, graph, DEC-BUDGET, root/slot, implementation, lifecycle and production artifacts remain unchanged.

```text
EXTERNAL_GATE = EXT-BUDGET-APPLICABILITY-EVIDENCE
PROOF_OBLIGATIONS = 8
MINIMUM_EVIDENCE_SET = ["EVIDENCE-BUDGET-CURRENT-APPLICABILITY-BUNDLE"]
EXPECTED_PRODUCERS = ["Authority publisher / controller-store catalog or generation owner", "Release/lineage/runtime and ProgrammerProfile owning authorities", "Current validity / revocation / usage evidence owner", "Existing governing scope/phase contract authority"]
RECEIPT_ACTION = RECEIVE-BUDGET-APPLICABILITY-EVIDENCE
REENTRY_ACTION = FACT-BUDGET-APPLICABILITY
GENERIC_EXTERNAL_GATE_RULE_REQUIRED = YES
ACTIONABLE = []
CONTROL_STATE = WAITING_FOR_EXTERNAL_EVIDENCE
NEXT_ACTION = NONE
ROOT_CONDITIONS_REMAINING = 27
SLOTS_REMAINING = 41
TEMPLATE1_CONSTRUCTION_READY = NO
CANDIDATE3_RESUMPTION_READY = NO
PRODUCTION_EFFECT = NO
```
