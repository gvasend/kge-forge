# E1 legacy migration compiler implementation plan 1

Plan a finite, deterministic compatibility boundary: **E1_LEGACY_V1 → PLANNER_SNAPSHOT_V0_1**. Reuse the existing canonical planner and its admission rules. Do not add a second planner or a second snapshot codec.

The first package is **M01 — migration contract and independent oracle closure**. Compiler implementation is not yet eligible: four action semantic domains, three real-source result profiles and the historical-attempt import contract remain incomplete. Migration must expose those gaps, not infer their values. This plan performs no implementation, migration, readiness run, requalification or E1 action.

The [machine-readable plan](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_IMPLEMENTATION_PLAN_1.json) enumerates target classifications, source classes, dependency-ordered packages and current eligibility. The [acceptance matrix](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_ACCEPTANCE_MATRIX_1.md) defines MC01–MC26 independently of compiler output. The [migration-boundary decision](DETERMINISTIC_PLANNER_V0_1_E1_MIGRATION_BOUNDARY_DECISION_1.md) governs this plan; historical correction plans and BR results remain unchanged.

## Target and observed implementation interfaces

`PLANNER_SNAPSHOT_V0_1` is the logical migration target. Its snapshot serialization is the existing `PLANNER-SNAPSHOT-1` schema in [codec.py](../../adapter/planner/codec.py), using `snapshot_bytes`, `snapshot_id`, `decode_snapshot`, `bundle_bytes`, `bundle_id`, `save_bundle` and `restore`. Preserve existing versioned compatibility unless M01 proves a bounded additive field necessary.

Use existing types in [model.py](../../adapter/planner/model.py): Snapshot, Action, KnowledgeRecord, GraphEntity, GraphAssertion, Predicate, RootCondition, ValueSlot, Decision/DecisionDossier, EvidenceRequirement, ExternalGate, ReceiptAdmission/Observation, ControlBoundary, Goal, BudgetProofMatrix, ArtifactPin and PersistenceBundle. Use existing `core.recompute`, `core.resume_eligibility`, `codec.invalidate_sources`, selector policy binding and gate/proof validation.

The current [replay.import_e1](../../adapter/planner/replay.py) loads a reviewed descriptor and defaults to N_P06.json. The new migration entrypoint must select an explicit versioned migration contract; it must not silently use that historical qualification fixture as its full-source normalization. Preserve the old fixture/replay path for regressions. Integrate a thin explicit dispatch into `import_e1` only after the new path is qualified; never maintain two semantic implementations for the same migration version.

### Classified canonical target

| Target fields / category | Classification | Required content or limit |
|---|---|---|
| Snapshot.actions, statuses | REQUIRED | All63 current-plan definitions and current lifecycle/holds, with116 declared prerequisite edges; definitions distinct from attempts |
| roots, slots | REQUIRED |28 tracked root/gate obligations,43 slots, two baseline proof admissions, two separately represented policy-fixed inputs and required deferred obligations |
| knowledge | REQUIRED | Accepted named knowledge and source/type/currentness bindings; non-PASS knowledge remains usable where independently admitted |
| entities, assertions, predicates | REQUIRED | Exact operational graph projection and proof/dependency clauses; no dangling references; provenance-only assertions excluded from operational truth |
| context | REQUIRED | Bound full-run envelope, effects, identity domains and policy context |
| decisions | REQUIRED | Dossiers, readiness, facts, recorded decisions and reevaluation routes; not only saved stages |
| evidence_requirements, external_gates | REQUIRED | Eight active missing-evidence contracts, latent gates separately represented, known producer or explicit unknown competence |
| receipt_admissions, receipt_observations | REQUIRED inventories | Explicit frozen no-receipt state; no invented accepted receipt. A required collection may be independently justified empty. |
| boundaries, goals | REQUIRED | Missing-fact/implementation/dependency frontier, full goal scope, failure/recovery predicates and suspension inputs |
| budget_matrices | REQUIRED contract inventory | Complete obligation definitions, unsatisfied frozen proof state; synthetic positive budget profile is not live evidence |
| PersistenceBundle.initial/current/events | REQUIRED | Canonical migrated baseline, ordered subsequent native events and consistent current state; no forged historical event chain |
| sources, policy, policy_version, scope | REQUIRED | Complete source pins, exact admitted selection-policy binding and full frozen-run scope |
| Historical attempts and current overlays | REQUIRED |24 ledger entries accounted for with immutable history and separately reconciled holds; see history boundary below |
| Expected external absence records | REQUIRED | Eight bound absence/gate/receipt/reentry tuples; never positive proof |
| MigrationManifest and DerivationIndex | REQUIRED | Versioned transformation, exclusive dispositions, field provenance and output identities |
| Snapshot.information; Action.cost/cost_unit | OPTIONAL | Only supported comparable deterministic metrics; absence invokes selector fallback, not default estimates |
| Titles, surrounding narrative, non-governing annotations | PROVENANCE_ONLY | Preserve source references; any actual gate clause is operational and cannot use this disposition |
| Saved global/actionability/resume summaries | PROVENANCE_ONLY / oracle | Compare after independent recomputation; never substitute for predicates |
| Positive external evidence absent at suspension | NOT_REQUIRED_FOR_FROZEN_RESUME | Its absence and governing contract remain REQUIRED |
| Unreferenced archive payloads; whole raw reports embedded in snapshot | NOT_REQUIRED_FOR_FROZEN_RESUME | Only after dependency audit; bytes remain pinned/read-only where referenced, not a general artifact database |

The companion enumerates every current Snapshot/PersistenceBundle top-level field. M01 must expand this to every required nested operational field and its source selector before the owning implementation package passes. Missing fields must not be silently filled with dataclass defaults. Optionality in the Python type does not waive the full-run contract.

### Expected semantics

Derive, rather than trust labels:

```text
GLOBAL_CONTROL_STATE = MIXED_WAIT
RUNNABLE_INTERNAL_ACTIONS = []
DECISION_READY_ACTIONS = []
NEXT_ACTION = NONE
E1_RESUME_ALLOWED = NO
```

The independent oracle is the frozen manifest, handoff, checkpoint and global-control record, checked for mutual consistency. Supporting expectations include27 unresolved roots,41 unresolved slots,13 completed/50 blocked current action summaries, eight unresolved external boundaries, no received evidence, candidate-only authority VALID_UNCONSUMED, budget external wait, seven other missing-fact frontier points, and dependency-blocked implementation. Preserve the four deferred top-level obligations separately from the28 tracked root/gate inventory. A saved count is never an algorithm input.

## Versioned legacy sources

The existing nine CE-02 source classes are reused. The manifest and its required dependency closure also require explicit external-request, candidate-authority and global-control classes. Source-domain objects need a closed subtype registry; do not admit arbitrary JSON as PINNED_SUBJECT.

| Legacy class | Recognition discriminator / version | Canonical destination |
|---|---|---|
| PLAN | E1-TEMPLATE1-GRAPH-RESOLUTION-PLAN-1 | Actions, dependencies, historical attempts, overlay, policy |
| GRAPH | E1-TEMPLATE1-TYPED-KNOWLEDGE-GRAPH-1 | Operational entities/assertions, proof obligations |
| MANIFEST | E1-RESUME-MANIFEST-1 | Source inventory, subject pins, receipt/reentry/suspension bindings |
| HANDOFF | E1-EXTERNAL-HANDOFF-PACKAGE-1 | Missing propositions, gates and transfer boundaries |
| CHECKPOINT | E1-SUSPENSION-CHECKPOINT-1 | Exact snapshot/suspension binding |
| DECISION_AUTHORITY | E1-ARCHITECT-DECISION-AUTHORITY-1 | Decision/grant/dossier correspondence |
| PROFILE_CANDIDATE | CURRENT-R4-PROFILE-ROOT-CANDIDATE-1 | Typed profile identity and baseline proof |
| INVOCATION_CANDIDATE | record_type INVOCATION-CANDIDATE-1 plus schema_version E1-JOINT-CONSTRUCTION-1 | Typed invocation identity and baseline proof |
| GOVERNED_TEXT | Authenticated document kind and reviewed versioned section selectors | Bounded results, dossiers, governing rule evidence |
| EXTERNAL_REQUEST | E1-EXTERNAL-EVIDENCE-REQUEST-1 | Budget receipt/evidence contract |
| CANDIDATE_AUTHORITY | E1-CANDIDATE-CONSTRUCTION-AUTHORITY-1 | Candidate-only grant and consumption restrictions |
| GLOBAL_CONTROL | E1-GLOBAL-CONTROL-RECOMPUTATION-1 | Source-bound frontier reasoning; output labels oracle-only |
| PINNED_SUBJECT | Exact domain schema/type/version whitelist completed in M01 | Runtime/G4/context/dispatch/release/profile source identities |

For every class: pin raw CONTENT_IDENTITY of its container; preserve separately tagged declared domain identities; retain schema/version, source selector, accepted binding and dependencies. Historical existence never establishes current validity. Recognition requires the discriminator and required field/type shape; competing matches reject. GOVERNED_TEXT and PINNED_SUBJECT are explicitly incomplete field profiles until M01 closes them, not permissive catchalls. No filenames or directory paths establish semantic class.

M02 walks the exact manifest/contract reference closure using explicit joins. It compares all10,911 preserved files but parses only required classified sources and provenance dependencies. It does not “best match” by repository search. Unknown required source schema stops migration with a coverage diagnostic.

## Minimal MigrationIR and manifest

MigrationIR is a temporary **assembly/coverage envelope**, not a parallel domain model. Its minimum members are recognized source records/pins, reviewed rule references, pending canonical objects using existing types, typed unresolved references, field derivations and dispositions. Use the existing ActionIR specification only at the action boundary; discard source-shape wrappers after their provenance is indexed.

Add only passive migration metadata types in the future bounded `adapter/planner/migration.py` (or the existing model registry if canonical wire persistence requires a registered type): MigrationManifest, SourceDisposition and FieldDerivation. Do not copy Action, Gate, RootCondition, KnowledgeRecord or control-state types. Current admission APIs may need a public shared wrapper; expose the existing enforcing path rather than duplicating it.

Every relevant source instance receives exactly one primary disposition:

- MIGRATED_OPERATIONAL: at least one required operational field; ancillary fields retain field-level dispositions.
- MIGRATED_PROVENANCE_ONLY: dependencies authenticate claims but supply no operational predicate themselves.
- REPRESENTED_AS_EXPECTED_ABSENCE: a **virtual expected-source record** bound to an actual gate contract, not a falsely present file.
- HISTORICAL_ONLY: immutable earlier evidence not admitted as current operational truth.
- NOT_REQUIRED: explicit audited exclusion from the required dependency closure.

Use MIGRATED_OPERATIONAL as the primary disposition for mixed-role artifacts and classify their fields separately. Ambiguous or unsupported required sources are unresolved diagnostics, not an invented sixth successful disposition; a successful manifest has no unresolved required disposition.

Each field derivation records original source identity/domain, raw content identity, embedded identity where relevant, schema/version, selector, operation (copy/typed conversion/authorized join/contract constant), migration-contract identity/version, rule identity, canonical target identity, dependencies and validity. Accepted rule provenance is required in addition to hashes.

MigrationManifest contains SOURCE_FORMAT, TARGET_FORMAT, native codec schema/version, migration-contract identity, source-inventory identity, sorted source pins, canonical snapshot and bundle identities, provenance-index identity, output-artifact inventory identity, external-absence inventory, unresolved disposition diagnostics and qualification status. Prevent a hash cycle: hash snapshot/bundle and derivation index first; output inventory excludes the manifest itself; manifest identity is an external digest of its bytes. Qualification status is NOT_QUALIFIED/QUALIFIED_MIGRATION with a separately pinned test record; it cannot itself authorize admission or v0.1 qualification.

## Action and result semantics

Action path: legacy plan record → versioned semantic binding adapter → shared ActionIR → independent O01 admission → canonical Action. Reuse29 literal bindings, exact scope/recorded-lineage rules and all63 instance IDs. The future native type must explicitly bind operation/stage/effect and result/proof contracts; source-specific text is not interpreted at runtime.

| Remaining category | Classification | Implementation prerequisite |
|---|---|---|
| Result | Historical outcomes are RECOVERABLE_FROM_LEGACY_SCHEMA; bounded existing oracles are DERIVABLE_FROM_EXISTING_CONTRACT; complete prospective type/transition declarations currently GENUINELY_MISSING from the accepted mapping layer | M01 defines source-cited semantic rules; no default PASS or inferred result type |
| Authority | Issued identities/exclusions recoverable; admission rules derivable; complete conditional requirement normalization not yet governed | M01 distinguishes outstanding requirement, existing grant and applicability; no authority inferred |
| Evidence | Source references and external gaps recoverable; freshness/proof checks derivable; reference-role classification still missing | M01 explicitly separates provenance, current proof and required proposition |
| Knowledge | Named claims/source support recoverable; explicit-empty map and non-PASS knowledge validity derivable;56 omission interpretations and unkeyed/type joins missing | M01 binds KnowledgeId/KnowledgeType without fabricating producer completion |

Absent positive-reentry evidence is NOT_REQUIRED_FOR_FROZEN_STATE, but its typed requirement/absence is required. A mandatory O01 definition field cannot be omitted merely because the action currently waits. GENUINELY_MISSING here identifies an unestablished semantic rule, not a claim that E1 lacked all governing prose. Stop the dependent package until an independently supported rule exists.

For S-BINDING, S-CONTEXT and PREP-VALIDATOR, join the exact report hash to its ledger record and producing action. Canonical result identities are domain-separated hashes of an approved migrated representation; original report and record identities remain provenance. Explicit outcomes, claims and empty resolved-root/slot arrays must agree. Do not infer PASS from existence or current proof from historical PASS.

Existing result predicates pin synthetic source hashes and subjects. M01 must define and independently qualify a real-source profile parameterization under the same acceptance semantics. Keep historical synthetic fixtures unchanged; do not insert real source bytes under their hashes. Admission predicates remain authoritative.

### History representation boundary

`ExecutionEvent` requires parent snapshot, after snapshot, parent event and event identity, and `codec._replay` verifies the chain. Do not fabricate these for legacy records lacking sufficient historical prestate.

M01 must qualify one precise import representation: preserve legacy attempts as typed immutable imported-history records, reusing canonical result/knowledge types where their semantics fit; construct a proved current canonical baseline and start new native events from that baseline. If an additive imported-history field/type is necessary, add only that bounded canonical metadata through model/codec with backward-compatible version rules. Do not maintain an alternative event executor. If historical native transitions can actually be reconstructed and proved, native events are preferable; object counts alone are not such proof.

O02/O06 reconciliation must account for all24 ledger entries and current holds/overrides. The three report routes are a required subset, not the complete ledger. S-BINDING unkeyed inventory cannot be relabeled as accepted typed knowledge without a governed identity/type derivation. Canonical append-only history begins at an authenticated migration baseline; subsequent events use existing replay.

## Graph, proofs and external boundaries

O10 admits the operational projection from graph/source assertions. Preserve relation meaning, typed endpoint identities, source pins, accepted provenance, scope, currentness and dependencies. Exclude non-operational material only by a reviewed disposition; no silent edge dropping. Reject conflicting assertions, dangling predicates and unsupported required relationship kinds. Proposed historical corrections stay proposed.

Restore decision/dossier facts, authority/grant limits and proof predicates. O08 still requires the complete PREP-VALIDATOR → dossier/decision → bounded grant → validator-authority admission chain. O09 still requires the exact two baseline slot-proof predicates. Generic valid proof, accepted knowledge or action PASS cannot replace either. Restore the budget eight-obligation contract with its absent/current evidence state; never import the synthetic positive matrix as real E1 evidence.

For each of eight BR-C1 expected absences restore request identity, missing proposition, expected producer/source class (or explicit unknown), receipt action, named reentry, waiting state, scope/lineage and source provenance. The eight are budget, ancestry, approval, audit, runtime head, supervisor, executable policy and implementation. No accepted receipt exists at the frozen checkpoint. Latent eligibility remains separately represented, not a ninth current transfer point.

Use existing C03 `resume_eligibility`: current accepted evidence, verified pins, accepted reentry lineage and named-action eligibility are all necessary. Receipt alone is insufficient; validation alone is insufficient; a saved Boolean is not a proof. Preserve branch-local waits and independent work in synthetic controls.

A changed legacy source/rule invalidates every dependent canonical object through retained dependencies, then triggers the existing admission/recompute path. Historical facts survive as history; current proofs fail closed. Negative source copies never repair the frozen manifest by rebinding altered bytes. M07 must test this after canonical cold reload.

## Modules, APIs and package sequence

Proposed implementation files are bounded extensions, not work performed here:

- `adapter/planner/migration.py`: source-class registry dispatch, coverage envelope, normalization orchestration and migration manifest. Proposed APIs: `inspect_legacy(root, manifest_pin, contract_pin)`, `migrate_legacy(inspection, contract)`, `validate_migration(output, source_root)`. Accept explicit pinned reviewed contracts; never execute imported code.
- Existing `replay.py`: share result/provenance helpers and provide explicit versioned E1 migration dispatch. No fallback to fixed expected snapshot.
- Existing `model.py`/`codec.py`: only justified additive imported-history/provenance types; reuse canonicalization, source verification, invalidation, bundle persistence and replay.
- Existing `gates.py`, `core.py`, `selector.py`, `budget.py`: reuse enforcing APIs. Change only if M01 demonstrates a necessary type/admission integration gap; do not implement new lifecycle/control semantics opportunistically.
- Existing `__main__.py`: thin noninteractive migration entrypoint in M07 with explicit contract and output directory; deterministic JSON and existing error conventions. No network or E1 action execution.
- Proposed `adapter/tests/test_planner_migration.py` and a bounded `adapter/tests/fixtures/planner_v0_1/e1_legacy_v1/` fixture directory: independent source-shaped positives/negatives and cold subprocess tests. Keep authoritative oracle artifacts separate from generated outputs.

| Package | Prerequisites; sources/targets | Implementation and owning files | Oracles/tests; acceptance; unlocks |
|---|---|---|---|
| M01 Contract/oracle closure | Existing decision/contracts; all required source classes → reviewed mappings/types | Specification and fixture contracts only; close four semantic domains, three result profiles, history representation, exact source whitelist and17-element coverage | MC01–06; every required field has independent semantics and positive/negative oracle. Unresolved rules block the relevant implementation. Unlocks M02. |
| M02 Sources/provenance/manifest | M01; all required classes → ArtifactPin/MigrationIR/manifest | migration.py plus minimal model/codec metadata; recognition, pins, explicit joins, inventory closure/dispositions | MC01–02,07–10; unknown/malformed/ambiguous sources fail, coverage/provenance complete. Unlocks M03. |
| M03 Actions | M02; plan/manifest/governing rules → ActionIR/Action/Predicate/Gate | migration.py/replay.py and necessary existing admission integration; one constructor,63 instances | MC03,06,11–12;63/63 independently admitted, no defaults, all assigned negatives/invalidation pass. Unlocks M04. |
| M04 Results/history | M03; plan/reports/decision records → results/knowledge/immutable history/holds | migration.py/replay.py; approved model/codec history support only | MC04–05,13–14; three complete result routes plus all required ledger coverage and O02/O06 consistency. Unlocks M05. |
| M05 Graph/proofs/decisions | M04; graph/authorities/subject objects → existing canonical graph/decision/root/slot/budget types | migration.py with existing gates/budget/model admission paths | MC06,15–18; complete proof chains, cross-envelope negatives and transitive invalidation pass. Unlocks M06. |
| M06 Absence/control/reentry | M05; handoff/manifest/checkpoint/request → gates/boundaries/goals/resume inputs | migration.py/replay.py; existing core control/resume computation | MC19–22; eight unresolved boundaries, correct fact/dependency states, no unauthorized readiness. Unlocks M07. |
| M07 Assembly/qualification | M06; admitted components → Snapshot/PersistenceBundle/manifest | migration.py/codec/replay thin integration and CLI; tests/results | MC01–26, all affected regressions; frozen cold derivation, synthetic reentry, determinism, preservation pass. Unlocks migration closure review, not E1 resume. |

The companion expands every package's source classes, target types, implementation, oracle/test IDs, acceptance and unlocks. Sequence is deliberately dependency ordered; no package uses migration output to author its own expected profile. Tests run incrementally, but every required gate must pass at the same final contract/code/source identities.

The first runnable vertical slice follows M01: M02 pinned source/derivation admission → M03 a contract-complete action through O01 → canonical encode/decode → source invalidation rejection. It does not require external services, positive real evidence or complete experiment reconstruction. Full M03 acceptance still requires63/63.

## Independent qualification and determinism

Reuse BR-C1, CE-01, O01/O02/O06/O08/O09/O10/O16, budget proof and source-invalidation oracles. Add only migration-specific recognition, schema normalization, identity-transformation, disposition/provenance and full snapshot coverage oracles. Freeze their identities before implementation. Expected values must be derived from governing source clauses, not captured from compiler output.

Require same **pinned source bytes and migration contract** to produce the same canonical snapshot identity across filesystem traversal, source enumeration, map/key iteration, hash seeds and independent processes. Parsed object-key order and set-valued inventories may vary; causal history may not. Re-encoding an actual raw-pinned file with different JSON whitespace/keys changes its raw identity: reject the original pin. A separately admitted changed source revision may yield equal operational values but different provenance/snapshot identity. Do not demand identical authenticated identity across genuinely changed raw inputs.

M07 real frozen test: verify the10,911-file inventory; compile only required closure into an isolated output directory; validate every canonical admission and field disposition; terminate compiler process; cold-load using native codec and recompute using existing planner; compare independent frozen semantics, gates, proofs, frontier and resume reasons; recheck preservation. No request sending, receipt injection, authority consumption, selection execution or E1 mutation occurs.

Separately, derive an explicitly synthetic clone with its own correctly typed source/subject identities. Use one independently complete synthetic budget evidence bundle satisfying all eight budget obligations, receive/validate it through canonical receipt/reentry transitions and recompute. The corresponding named fact-acquisition reentry action may become eligible only if all its other gates hold; no authority/effect is automatically executed. Other seven absent branches stay blocked/waiting. Real E1 remains unchanged and its eight gaps unresolved. If the governing contract requires another prerequisite, include its independently admitted synthetic proof rather than manually clearing the gate.

## Prior work disposition and completion

| Prior work | Disposition |
|---|---|
| BR-C1 binding/absence contracts and qualification | REUSED_DIRECTLY plus REUSED_AS_ORACLE in M02/M06; not a blanket admission of all migrated state |
| BR-C2 common Action model,29 literals, typed scope/lineage rules | REUSED_DIRECTLY; direct source-specific projection implementation approach SUPERSEDED_BY_MIGRATION; four missing domains and result routes STILL_REQUIRED in M01/M03/M04 |
| BR-C3 history obligations | STILL_REQUIRED; source support/reconciliation oracles REUSED_AS_ORACLE in M04; not implemented here |
| BR-C4 graph projection | STILL_REQUIRED in M05 using O10; no transfer into BR-C2 |
| BR-C5 composition/coverage | STILL_REQUIRED in M07 using O16; existing observations/probes REUSED_AS_ORACLE |
| CE-02 recognition, source inventory, joins, gap history | REUSED_DIRECTLY/REUSED_AS_ORACLE; direct-bridge-only packaging SUPERSEDED_BY_MIGRATION; semantic coverage obligations STILL_REQUIRED |
| Historical synthetic profiles and blocked results | REUSED_AS_ORACLE/HISTORICAL_EVIDENCE; never overwritten or declared real-source positives |
| General ingestion/GraphRAG, databases, external retrieval | DEFERRED; not migration prerequisites |

No prior artifact is deleted. Supersession concerns future work ownership, not historical claims or tests. New migration results must cross-reference original BR/CE requirement IDs and the17-element matrix.

Migration qualification requires all required dispositions, canonical admissions, provenance, independent controls, deterministic cold migration, invalidation, frozen acceptance, synthetic reentry, regressions and preservation to pass. Any unsupported required semantic value or unexplained field prevents qualification. All eight real external evidence gaps remain unresolved. No conversation state is needed.

Even a QUALIFIED_MIGRATION result does not restore Planner v0.1 QUALIFIED. Submit the new migration coverage/result to the existing C06A/CE-02 closure predicates; preserve C06A-3/C07 retry=NO until their complete gates independently pass. Full correction requalification and fresh adversarial review remain separately required.

```text
SOURCE_FORMAT = E1_LEGACY_V1
TARGET_FORMAT = PLANNER_SNAPSHOT_V0_1 (existing PLANNER-SNAPSHOT-1 codec)
MIGRATION_TARGET_ELEMENTS = companion.target_fields
LEGACY_SOURCE_CLASSES = 13 families; exact GOVERNED_TEXT/PINNED_SUBJECT field profiles are M01 prerequisites
MIGRATION_WORK_PACKAGES = [M01, M02, M03, M04, M05, M06, M07]
FIRST_PACKAGE = M01 (specification/oracle closure; no compiler implementation yet)
EXPECTED_FROZEN_CONTROL_STATE = MIXED_WAIT
EXPECTED_RUNNABLE_ACTIONS = []
EXPECTED_DECISION_READY_ACTIONS = []
EXPECTED_RESUME_ALLOWED = NO
EXPECTED_EXTERNAL_GATES = 8
BR_WORK_DISPOSITION = reused contracts/oracles; direct projection packaging superseded; obligations preserved
CE_02_DISPOSITION = OPEN_MIGRATION_WORKSTREAM
BR_C2_STATUS = SUSPENDED
C06A_3_RETRY_ALLOWED = NO
C07_RETRY_ALLOWED = NO
V0_1_CURRENT_STATUS = CORRECTION_REQUIRED
IMPLEMENTATION_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
```
