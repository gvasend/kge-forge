# CE-02 source-to-profile admission bridge 1

**Result: PARTIAL — CE-02 remains OPEN.** Source recognition, a finite source inventory, lossless source-envelope projection and stage-specific rejection behavior are specified. The complete operational profile projection is **not established**. No source-envelope extraction is counted as Oxx admission, and C06A-3 retry is not allowed.

This does not fulfill the requested complete bridge. In particular, there are no new source-shaped positive cases accepted end-to-end by an existing Oxx predicate. Publishing that limitation is preferable to manufacturing independently trusted profiles or proof objects from candidate data.

## Governing scope and deliverables

The [RETRY_4 report](DETERMINISTIC_PLANNER_V0_1_C06A_3_RETRY_4_RESULT.md), [remaining-contract package](DETERMINISTIC_PLANNER_V0_1_C06A_REMAINING_CONTRACT_1.md), [closure](DETERMINISTIC_PLANNER_V0_1_C06A_3_PREFLIGHT_CLOSURE_1.md), [CE-01 refinement](DETERMINISTIC_PLANNER_V0_1_CE01_CONTRACT_RECONCILIATION_1.md), and [C06A-2 inventory](DETERMINISTIC_PLANNER_V0_1_C06A_2_MAPPING_1.json) remain unchanged. C06A-3 assignments are O01/O02/O03/O06/O08/O09/O10/O16. O08 and O09 exact support identities are taken from their governing contracts; they are not inferred from filenames.

New companions:

- [Source classes and complete bounded source inventory](DETERMINISTIC_PLANNER_V0_1_CE02_SOURCE_PROFILE_BRIDGE_1_SOURCE_CLASSES.json).
- [Projection contracts, selectors and source pins](DETERMINISTIC_PLANNER_V0_1_CE02_SOURCE_PROFILE_BRIDGE_1_PROJECTIONS.json).
- [Source-shaped fixtures and executable structural specification](DETERMINISTIC_PLANNER_V0_1_CE02_SOURCE_PROFILE_BRIDGE_1_FIXTURES.json).
- [Validation results](DETERMINISTIC_PLANNER_V0_1_CE02_SOURCE_PROFILE_BRIDGE_1_VALIDATION.json).
- [Complete preflight, including all unresolved groups](DETERMINISTIC_PLANNER_V0_1_CE02_SOURCE_PROFILE_BRIDGE_1_PREFLIGHT.json).

No runtime implementation, operational registry or existing tests are changed. The embedded program is a specification for the partial recognition/extraction boundary only.

## Inventory unit and completeness

A source instance here is a distinct **owning artifact content identity**, with all required selectors attached. It is not each field, each assertion, or every file in E1. The bounded inventory consists of:

- Five owners P/G/M/H/S from assigned rows of the C06A-2 mapping inventory.
- Nine support owners required by the exact O08 and two O09 contracts.
- Two additional bounded-result owners for O03 S-BINDING and S-CONTEXT; PREP-VALIDATOR is already counted among O08 support owners.

Total: **16 required source artifacts**, **nine classes**. The inventory records all exact raw identities, paths as locators, selectors, governing bindings and consuming roles. All **2,733 assigned field records** were checked against their pinned owner and selected-value hash. This is extraction verification, not operational mapping qualification.

All 16 are uniquely recognizable, but are classified **UNSUPPORTED_REQUIRED_SOURCE** for the *complete operational bridge*. No required source is silently dropped. `NOT_REQUIRED_OPERATIONALLY = 0` is within this deliberately required-owner inventory, not a claim that all 10,911 E1 files should be loaded. The rest of the archive is not implicitly in scope. Historical narrative inside a required owner can remain provenance-only; the artifact may still be required for another operative field.

## Source classes

Every class requires independently authenticated raw CONTENT_IDENTITY, exact selected-value provenance, source schema/kind, and projection version. Frozen identity proves only the pinned historical/replay source; it does not prove live freshness. A trusted validity view must distinguish current, stale and revoked supporting records.

| Class | Recognition, schema/version | Expected operational profile / consumers |
|---|---|---|
| PLAN | `schema=E1-TEMPLATE1-GRAPH-RESOLUTION-PLAN-1`, required action/history/state fields | ActionDefinition, PrerequisiteContract, BoundedResultContract, HistoricalAttemptAndOverlay; O01/O02/O03/O06/O08/O09/O16 |
| GRAPH | `schema=E1-TEMPLATE1-TYPED-KNOWLEDGE-GRAPH-1`, entity/assertion/relationship/synchronization fields | TypedRelationAndEntity, slot proof context, coverage; O09/O10/O16 |
| MANIFEST | `schema=E1-RESUME-MANIFEST-1`, exact graph/plan/ledger/pin members | Source-bound historical overlay/coverage references; O06/O16 |
| HANDOFF | `schema=E1-EXTERNAL-HANDOFF-PACKAGE-1`, source snapshots and request inventory | Coverage dependencies; O16 only here; O12 semantics remain later work |
| CHECKPOINT | `schema=E1-SUSPENSION-CHECKPOINT-1`, bindings/state/identity | Coverage dependencies; O16; no automatic resume |
| DECISION_AUTHORITY | `schema=E1-ARCHITECT-DECISION-AUTHORITY-1`, decision/scope/source/authority fields | O08 bounded validator grant chain; semantic authority identity retained separately from raw content identity |
| INVOCATION_CANDIDATE | Exact `schema_version` and `record_type` pair recorded in registry, required canonical identity/body members | O09 InvocationAttemptId source; candidate existence is not slot proof |
| PROFILE_CANDIDATE | `schema=CURRENT-R4-PROFILE-ROOT-CANDIDATE-1`, identity/canonicalization/authority members | O09 released-profile-content source; not ProgrammerProfile/authority identity substitution |
| GOVERNED_TEXT | Independently authenticated artifact-kind descriptor, raw identity and explicit selectors | O03 accepted reports and O08/O09 preparation/dossier/acceptance/release evidence; no general semantic extraction |

GOVERNED_TEXT is not “any Markdown file.” Recognition requires an authenticated kind binding from the governing input set. A candidate-supplied type label alone is insufficient. Its operational subrole is explicitly assigned by the governing support relationship. Filename and extension never select a class.

Schema recognition does not imply complete schema validity. Known discriminator plus missing/wrong typed required field fails source validation. A non-object JSON source or missing discriminator is malformed; an unknown version is unsupported. More than one recognized discriminator is ambiguous and rejects before projection. The ambiguity fixture combines the plan and invocation discriminator signatures without relying on path names.

## Deterministic projection defined in this artifact

`PROJECT_SOURCE_ENVELOPE(source_bytes, authenticated_descriptor, registry)` is pure. Its output is **not** yet the operational profile supplied to Oxx. The nine `PROJECT-<class>-1` entries describe the same lossless mechanism over class-specific selectors.

| Target member | Selector / transformation / type |
|---|---|
| source class | Unique schema/kind recognition, enum from this registry |
| raw source identity | Independently supplied CONTENT_IDENTITY; SHA256 of exact bytes must match |
| source schema/version | Exact source discriminator; no default when missing |
| selected values | Explicit JSON Pointer from the pinned inventory; exact scalar/container types preserved, with selected-value SHA256 |
| text value | Exact authenticated bytes; the executable partial fixture only supports `/raw`; section/semantic extraction is not invented |
| dependencies | Explicit supplied typed source identities and selectors; never a repository search |
| provenance | Raw identity, authenticated kind, exact selectors, source schema/version, projection version and validity context |
| projected envelope identity | Derived CONTENT_IDENTITY in `ce02-source-envelope-v1`; SHA256 of canonical body excluding the derived identity |

Canonicalization is UTF-8, sorted object keys and compact separators. Causal arrays remain ordered. Source raw identity is not recomputed from normalized bytes. Changing whitespace changes the raw source pin; changing inventory order does not change a set-valued selector projection. Equal digest bytes under another identity domain are not accepted.

Every assigned selector is present in the projection companion with owner identity and expected selected-value hash. The target of this lossless step retains the selected record; it does not compile prose into permissions, predicates, result acceptance rules or proof objects.

The required next operation, `PROJECT_ENVELOPE_TO_OPERATIONAL_PROFILE`, is unresolved for the full assigned scope. Its missing target fields are listed below. Therefore the executable partial specification returns `UNSUPPORTED_REQUIRED_SOURCE` at `OPERATIONAL_PROFILE_PROJECTION`, even for successful recognition/extraction. It never returns Oxx ACCEPT by default.

## Admission stages and errors

```text
raw source + independent authenticated descriptor
 -> recognition [unsupported / ambiguous / malformed]
 -> source validation [identity/domain/substitution/currentness/type/provenance]
 -> lossless source-envelope projection [selector unavailable / unsupported text selector]
 -> operational-profile projection [currently UNSUPPORTED_REQUIRED_SOURCE]
 -> profile validation [not reached for this partial bridge]
 -> existing Oxx predicate [not reached]
 -> operational admission [not reached; no authority or E1 resumption]
```

Existing predicates remain authoritative. CE-01 still requires mandatory supporting payloads locally. This document neither weakens O16 nor supplies a new permissive profile-level path.

A complete bridge must derive the independently reviewed profile/candidate distinction correctly. Generating a candidate's own expected allowlist from that same unadmitted candidate would erase the trust boundary. Merely copying BASE/RENAMED expected values would instead special-case the fixture. Neither is authorized here.

## Multi-source relationships and missing projection rules

All joins must use explicit role arguments and typed identities. Locations are locators after identity selection, never fallback discovery keys. No sibling artifact may fill an absent field unless the governing mapping names it.

| Profile family | Required set and correspondence | Missing/stale behavior |
|---|---|---|
| O01/O03 action/result | Plan action record plus explicitly named accepted result/rule source; join by ActionId and result identity, exact scope and source selector | Missing rule does not become generic PASS; stale support cannot authorize current output |
| O02/O06 history/holds | Plan history/current overlay, exact ledger binding and accepted result/knowledge/override sources; explicit event/action/result/hold identities | Missing supporting payload rejects current admission per CE-01; stale accepted bytes may remain history without current eligibility |
| O10 graph | Owning graph, relationship semantics, referenced typed entities and accepted support sources | Dangling support or unaccepted provenance cannot become an operative edge; preserve descriptive relationships separately |
| O08 gate | Exact preparation, dossier, authority and propagation records already identified by O08; gate/decision/option/scope/lineage must correspond | Documents do not automatically manufacture the admitted proof object; missing/stale chain prevents gate support |
| O09 slots | Invocation candidate + acceptance, or profile candidate + acceptance + release; exact slot/predicate/value-domain and source envelope | Candidate/value existence does not establish a slot-completion proof |
| O16 instance | All required component admissions, source coverage, graph/plan/ledger/policy/envelope bindings | A missing join or incomplete source set must not be repaired by inference; local admission alone is insufficient |

These are the governing source-set constraints, not claims that all joins have now been compiled into executable operational projections. In particular, the frozen history contains a selection-only `SELECTION_BLOCKED` entry with `action_result=null` and an explicit statement that no action executed. A source projector must not manufacture an ActionId/result for that event. The synthetic HISTORY fixture's action/result sequence is not a sufficient universal projection rule for it.

## Complete remaining gap set

No gap below is dismissed because the original specification cases pass.

- **BR-01 — O01/O03 operational definitions:** source-specific scope/actionability restrictions and bounded output rules need exact target-field expressions and source bindings. Lossless field copying is known; the complete independently trusted operational definition table is not supplied by that copying operation.
- **BR-02 — O02/O06 event/hold normalization:** complete typed classification of historical selection, action, override and knowledge records and their current-overlay relationship is required. No source event may be silently interpreted as completed action proof.
- **BR-03 — O10 graph normalization:** source entity/assertion/provenance states need a complete projection into the predicate's entity/predicate/assertion tables. `SOURCE_LOCATED` and proposed semantics must not silently become accepted operational truth.
- **BR-04 — O08/O09 source-to-proof construction:** documentary support must be projected into proof/profile candidates with explicit provenance, prerequisite and validity inputs. The existing admission rules validate these objects; their existence does not itself define a documentary proof constructor. Expected qualification proof objects are not source evidence.
- **BR-05 — O16 trust/composition bridge:** generated profiles require an explicit independently governed trust binding and complete source-to-component correspondence. Exact fixture pins cannot be repinned by an importer to admit arbitrary candidate state.

The bounded follow-up is the target-field expression and trust/admission definition for these five groups, with independently expected source-shaped outputs. This is not a request for new real E1 evidence, a new planner architecture, or a general-purpose document database. Exact identity constants already required by O08/O09 may be retained; new filename-dependent rules are not permissible.

## Invalidation and cold restoration requirements

Source-envelope identities retain raw-source identities, selected-value hashes, selectors and projection version. A full bridge must persist every additional dependency and the accepted validity view; it cannot reconstruct validity from matching identity strings. Source change/invalidation marks every derived profile stale and invalidates its required proof/operational conclusions through existing transitive invalidation.

Historical records remain referenceable where the governing predicate permits; their current usability is recomputed separately. A BLOCKED producer is not an invalid-proof flag. Cold reload must preserve the dependency graph and re-run the same bridge/predicate stages. No conversation state is a permitted input.

The partial specification verifies source-envelope identity and provenance round trips for all nine classes and reverses registry enumeration order. Raw source bytes remain pinned. It does not claim operational cold-resume or source-to-Oxx persistence qualification.

## Fixtures and validation limits

**78 structural specification cases PASS:** nine source-shaped recognition/extraction fixtures and 69 negatives, including schema/type omissions, unknown versions, wrong identity domain, stale source, substituted bytes, wrong provenance class and ambiguous recognition. Nine source-envelope canonical reload/registry-order checks PASS.

**Source-shaped positives accepted by existing Oxx predicates: 0.** The nine positive extraction fixtures intentionally stop at the unsupported operational-profile stage. They are synthetic qualification-only bytes, not copies of expected profile values, and not E1 evidence.

Invalid cross-source joins, incomplete multi-source sets and projection-to-invalid-operational-profile cases are specified as mandatory rejection obligations but are **not qualified end-to-end** here. No “PASS” is assigned to those unavailable paths. Existing 313-case and CE-01 qualification results do not substitute for this missing bridge coverage. Complete C06A-3 preflight is therefore incomplete even though no additional contradiction within the unchanged existing predicates was demonstrated.

## Preservation and report

No existing oracle, implementation, registry, test, historical result or E1 artifact is edited. Artifact paths appear only in the finite identity inventory and provenance. The recognition program contains no E1 filename or directory-based dispatch and does not select expected profile values by fixture name.

```text
CE_02_CLASSIFICATION = SOURCE_NORMALIZATION_AND_PROFILE_TRUST_CONTRACT_GAP
SOURCE_CLASSES = [PLAN, GRAPH, MANIFEST, HANDOFF, CHECKPOINT, DECISION_AUTHORITY, PROFILE_CANDIDATE, INVOCATION_CANDIDATE, GOVERNED_TEXT]
SOURCE_CLASS_COUNT = 9
REQUIRED_SOURCE_INSTANCES = 16 artifact identities; 2733 assigned field records
SUPPORTED_BY_BRIDGE = 0 (complete source-to-Oxx admission)
NOT_REQUIRED_OPERATIONALLY = 0 (within required-owner inventory only)
UNSUPPORTED_REQUIRED_SOURCE = all 16 identities listed in SOURCE_CLASSES companion
AMBIGUOUS_SOURCE = [] (actual required inventory)
PROJECTION_CONTRACTS = nine PROJECT-<class>-1 lossless envelope contracts; operational projection incomplete
MULTI_SOURCE_PROFILES = [action/result, history/hold, graph/support, O08 chain, both O09 chains, O16 composition]
SOURCE_INVALIDATION = specified; full operational path unqualified
SOURCE_SHAPED_POSITIVE_CASES = 0 end-to-end; 9 extraction-only
SOURCE_SHAPED_NEGATIVE_CASES = 69 structural
DETERMINISM_CASES = 9 extraction-only
CE_02_CLOSED = NO
C06A_3_CONTRACT_MISMATCH_SET = [BR-01, BR-02, BR-03, BR-04, BR-05]
C06A_3_CONTRACT_CONFLICT_SET = []
C06A_3_CONTRACT_EXCEPTION_SET = [CE-02]
C06A_3_RETRY_ALLOWED = NO
RESTORED_AND_QUALIFIED = 2/17
C06A_4_READY = NO
C07_RETRY_ALLOWED = NO
F03_STATUS = CLOSED
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
