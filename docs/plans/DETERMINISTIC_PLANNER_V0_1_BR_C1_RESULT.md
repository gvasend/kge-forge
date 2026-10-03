# BR-C1 shared binding contract qualification

**WORK_PACKAGE = BR-C1. RESULT = PASS for the assigned contract/qualification-specification scope.** No planner implementation or runtime restoration element is qualified by this result. The shared binding prerequisites for BR-C2 are satisfied; BR-C2 is not executed.

The authoritative [dependency analysis](DETERMINISTIC_PLANNER_V0_1_CE02_REMAINING_BRIDGE_DEPENDENCIES_1.md) and [package record](DETERMINISTIC_PLANNER_V0_1_CE02_REMAINING_BRIDGE_DEPENDENCIES_1.json) define BR-C1 as common role/identity/context/provenance/dependency projection and an independently accepted expected-profile process. They explicitly defer action/results, history, graph and full composition to BR-C2–BR-C5. The user's “implement or qualify” instruction is satisfied here through an executable specification and qualification of that common contract, not changes to `adapter/planner`.

## Artifacts and scope

- [Binding contract and reference specification](DETERMINISTIC_PLANNER_V0_1_BR_C1_CONTRACT.json): independently pinned input sources, binding targets, joins, provenance, context, absence routes, trust boundary and pure reference program.
- [Qualification fixtures](DETERMINISTIC_PLANNER_V0_1_BR_C1_FIXTURES.json): explicit source locators/pins and a qualification-only frozen-snapshot validity view.
- [Validation evidence and reproducible runner](DETERMINISTIC_PLANNER_V0_1_BR_C1_VALIDATION.json): every negative case and rejecting clause, canonical identities, reload checks, process/hash-seed comparison and preservation evidence. The embedded runner reads only explicit fixture inputs and performs no writes or planner operations.

The fixtures use pinned historical source bytes and synthetic qualification state. They do not create real E1 evidence. The expected target identities come from the independently supplied source registry, manifest, checkpoint and governing records, not from projection output. `admit()` checks those expected targets without calling `project()`.

Existing O01/O02/O06/O08/O09/O10/O16 predicates and BR-04 history are unchanged. BR-04's documentary specification checks were rerun, preserving its three positive chains, 30 negatives, nine invalidations and four partial composition cases.

## Verified package contract

**Shared blockers:** D1 typed context/role identity, D2 provenance/dependency/snapshot validity, D3 independent expected-profile governance boundary. **Affected gaps:** BR-01, BR-02, BR-03, BR-05.

All nine source classes occur in the 16 original owners. Explicit support joins additionally include the 19 named result artifacts outside that owner set, the checkpoint-bound selection-policy document and the manifest-bound budget external contract. Deduplication by independently pinned artifact identity gives **37 source payloads**. No filename-based discovery or archive scan supplies a missing semantic source.

The common values covered are dependency-analysis V03/V04/V05/V07/V12/V13/V14/V17. V09's per-knowledge support assignment remains BR-C3 work. The full expected action/history/graph parameter tables remain BR-C2/C3/C4 work; BR-C1 defines their acceptance boundary rather than fabricating them.

Acceptance was checked against each package condition:

| Package condition | Evidence |
|---|---|
| Common inputs explicitly mapped or unavailable | 37 pinned payloads; 54 typed present bindings; eight explicit no-receipt routes |
| Same digest cannot cross identity domains | Wrong-domain mutation for every present binding rejected |
| Embedded policy and policy document remain distinct | Separate targets, raw versus extracted canonicalization, explicit policy-substitution negative |
| Candidate is not its own oracle | Fixture pins the contract independently; candidate contract-pin substitution rejected; admission compares fixed expected targets rather than projection output |
| Missing/stale and cross-envelope negatives | Missing support, every source invalidation, wrong scope/lineage/runtime/ledger/policy and wrong request/proposition/receipt/reentry cases rejected |

## Shared bindings

Each present descriptor records source role, source identity, exact selector, transformation, typed target, any join, dependencies and provenance. All candidates additionally carry the context, snapshot validity and `positive_subject_applicability=false`.

| Binding family | Count | Source → target and semantics |
|---|---:|---|
| Raw source content | 37 | Exact supplied UTF-8 bytes → pinned CONTENT_IDENTITY. Does not convert a file digest into a semantic authority identity. |
| Extracted ledger/state/policy | 3 | P JSON Pointer → canonical selected JSON body digest under EXTRACTED_JSON_VALUE; independently compared with M's declared digest. Raw plan identity remains separate. |
| Recorded subject references | 11 | M `/subject_pins/*` → role-specific tagged references, retaining exact source scope, target scope and lineage. A named authority/runtime/profile is not an applicability proof. |
| Recorded hold inputs | 3 | Exact plan selectors for DEC-EXEC `blocking_result`, INPUT-IMPLEMENTATION `decision_readiness`, and BUILD-BINDING `unresolved_prerequisites`; retained as source-bound current-overlay inputs, not replayed transitions. |

The subject and hold tags are specification value domains, not new runtime identity enums or a parallel planner model. Later packages must map their semantics to existing typed planner representations. Raw/semantic/instance identities cannot substitute merely because their printable values resemble each other.

**Scope and lineage:** context explicitly separates the source EXECUTION scope, target REQUEST scope and recorded lineage. Every candidate must match the independently bound context. No blanket scope replacement is performed.

**Operational envelope:** graph, plan, manifest, checkpoint, runtime/G4 and all subject references are retained; ledger, embedded policy and policy-document identities are distinct. These are references into the recorded envelope. Unknown applicability or missing constructed objects stay unknown; common binding acceptance does not establish a valid OperationalBinding, ProgrammerProfile applicability or WorkAuthorization permission.

**Canonical representation:** sorted object keys, compact UTF-8 JSON, no NaN serialization; raw source hashes cover exact bytes. Ordered source history is not reordered. The binding output uses canonical binding/request ID order. Provenance retains source identity, selector, governing source references, projection version and context identity inputs. Complete source inputs and the independently pinned contract are sufficient to rerun the specification in a fresh process.

## Absence and external-gate bindings

The contract keeps these meanings distinct:

- **KNOWN_PRESENT / PRESENT_BINDING:** the exact recorded object/reference exists in the pinned snapshot. This does not establish positive subject applicability.
- **KNOWN_ABSENT / EXPECTED_EXTERNAL_ABSENCE:** M records `evidence_received=false` and `WAITING_FOR_EXTERNAL_INPUT`, joined to the exact H request, handoff item, receipt contract and reentry route. The normalized gate is `WAITING_FOR_EXTERNAL_EVIDENCE` and the evidence payload is null.
- **MALFORMED_MISSING_SOURCE:** a required present support record is missing; bundle admission rejects. It cannot be relabelled as an external absence.
- **UNSUPPORTED_SOURCE:** no accepted projection exists; it cannot stand in for an expected absence.
- **FACT_BLOCKED:** exact recorded DEC-EXEC and INPUT-IMPLEMENTATION facts are retained with source bindings. Their presence does not make either decision ready.
- **DEPENDENCY_BLOCKED:** BUILD-BINDING's recorded unresolved ACTION prerequisite list is preserved. Computing its complete current actionability remains BR-C3/planner work, not a new boolean asserted by this specification.

For each of the eight requests, the contract retains request identity, handoff/frontier identity, exact missing proposition, acceptable source/expected owner, source-specific scope/lineage/currentness requirements, receipt ID, reentry list and provenance. The budget item retains its incorporated external proof contract; that named contract is also a pinned input. No missing budget fact is produced.

The eight qualified absence bindings are budget, ancestry, approval, audit, runtime-head, supervisor, execution policy, and implementation source/selector. A qualified absence is positive evidence that the **restored suspension representation is faithful**, not evidence satisfying the missing proposition. Neither a known producer role nor a named request establishes that a competent producer is available.

All joined request IDs must resolve uniquely. Manifest/handoff IDs, receipt actions and reentry lists must match exactly. Missing gate, wrong proposition, invented producer, wrong receipt/reentry, fabricated evidence, RUNNABLE state, positive-reentry flag and unsupported-source substitution each reject.

## Validity, invalidation and trust

`CURRENT_AT_PINNED_SNAPSHOT` is an explicit qualification premise supplied separately from the source bytes. It does not assert live freshness. Source identity stability alone cannot create that premise or satisfy an external applicability rule.

Every binding persists its source dependencies and context pins. The complete BR-C1 bundle requires all declared supports: invalidating any one of the 37 sources after canonical reload rejects the bundle. This is conservative qualification of the common prerequisite bundle, not a claim that all unrelated runtime branches must be suspended together. Branch-local transitive invalidation is consumed and refined by the later action/history/graph projections. No automatic revalidation transition or producer-completion requirement is introduced.

The expected-profile process is:

1. Pin governing source records and the accepted projection version independently of the imported candidate.
2. Define source selectors, typed expected targets and independent admission requirements from those governing records.
3. Review the complete per-family tables in BR-C2/C3/C4, preserving unresolved or absent subjects explicitly.
4. Pin the accepted expected profile before admitting any candidate.
5. Compare candidate values and provenance to that profile; never generate its allowlist from the candidate itself.

This defines D3's shared process and qualifies the contract-pin boundary. It does not pre-approve the later full action/history/graph profile tables or grant authority.

## Qualification results and limits

**54 present-binding positives and eight suspended-state binding positives pass** within one complete common-bundle fixture. Every expected target is checked independently by admission; counts alone are not the oracle.

**283 negative cases pass:**

- 162 target/domain/provenance mutations across all 54 present bindings;
- 72 absence/gate/route mutations across all eight requests;
- 37 source invalidations after canonical reload;
- five source-inventory/identity/substitution/ambiguity cases;
- seven scope/lineage/runtime/ledger/policy/profile-pin/resume cases.

Each negative records its rejecting stage and clause in the validation artifact. These do not constitute A–N runtime tests or full O16 qualification.

Canonical reload, reversed object keys, reversed source order, reversed inventory order and repeated reload all produce identical restored binding state. Independent processes with hash seeds 1 and 97 produce byte-identical semantic validation output, including the canonical state identity. Both present and expected-absence records survive those checks without cached planner state or conversation input.

The specification admits only a frozen-suspension binding result: `resume_allowed=false`, `newly_runnable=[]`, eight absence records with `positive_reentry=false`. Negative attempts to change these fields fail. This verifies the BR-C1 boundary; it does **not** purport to recompute E1's global planner state. No actual E1 importer/resume/action was executed.

## Coverage and next package

Newly qualified **BR-C1 specification contracts** are shared typed identity/context correspondence, source/provenance/dependency bindings, explicit expected external absence, independent profile-pin acceptance, and their persistence/determinism behavior.

No O01–O17 runtime element transitions to RESTORED_AND_QUALIFIED. D1/D2/D3 are satisfied only at the shared prerequisite scope assigned to BR-C1; family-specific field mappings and full composition remain open. BR-04 remains closed within its accepted scope; BR-01/02/03/05 remain open.

**BR_C2_READY = YES:** the preserved BR-04 inputs, pinned shared contract, executable positive/negative binding specification, identity separation and expected-profile process are present. BR-C4 also has its shared prerequisite, but the reported sequence remains BR-C2 next. No later package is executed.

```text
WORK_PACKAGE = BR-C1
RESULT = PASS (contract/qualification-specification scope only)
SHARED_BLOCKERS_ADDRESSED = [D1 shared bindings, D2 shared provenance/dependency/validity bindings, D3 independent expected-profile process]
BR_GAPS_AFFECTED = [BR-01, BR-02, BR-03, BR-05]
PRESENT_BINDINGS_QUALIFIED = 54, enumerated in contract companion
EXPECTED_EXTERNAL_ABSENCES_QUALIFIED = 8, enumerated by request identity
NEGATIVE_BINDING_CASES = 283 PASS
PERSISTENCE_RELOAD = PASS (binding specification)
DETERMINISM = PASS (binding specification)
CONTRACT_ELEMENTS_NEWLY_QUALIFIED = [shared identity/context, provenance/dependencies, expected absence/gate correspondence, profile-pin boundary, binding persistence]
RESTORED_AND_QUALIFIED = 2/17
REMAINING_COVERAGE = 15
BR_C2_READY = YES
NEXT_PACKAGE = BR-C2
EXTERNAL_EVIDENCE_GAPS_REMAINING = 8
E1_RESUME_ALLOWED = NO
CE_02_CLOSED = NO
C06A_3_RETRY_ALLOWED = NO
C07_RETRY_ALLOWED = NO
F03_STATUS = CLOSED
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
REAL_E1_EVIDENCE_CREATED = NO
E1_ARTIFACTS_MODIFIED = 0
IMPLEMENTATION_MODIFIED = NO
DEFERRED_SCOPE_VIOLATIONS = 0
PRODUCTION_EFFECT = NO
```
