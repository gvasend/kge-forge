"""Publish reconciliation evidence; no qualification operations."""
import hashlib,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;D=R/'docs/plans';P='DETERMINISTIC_PLANNER_V0_1_'
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p):return {'path':str(p.relative_to(R)),'raw_sha256':sha(p)}
def save(p,x):p.write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
base=read(O/'preservation-baseline.json');changed=[p for p,h in base.items() if not (R/p).is_file() or sha(R/p)!=h];assert not changed,changed
check=subprocess.run(['git','diff','--check'],cwd=str(R),capture_output=True,text=True);assert check.returncode==0,check.stdout+check.stderr
preservation={'PRE_EXISTING_ADAPTER_DOCS_FILE_COUNT':len(base),'PRE_EXISTING_FILES_CHANGED':changed,'P05_STAGE_BINDINGS':'13/13','END_INTERFACES_BOUND':'4/6','PC01_END':'PASS','PC02_END':'PASS','PC03_END':'PASS','T01_END':'PASS','E2_D01_END':'BLOCKED','CONTINUATION_INTERFACE':'UNRESOLVED_UNCHANGED','QUALIFICATION_CASES_EXECUTED':0,'MUTATIONS_APPLIED':0,'INVALIDATIONS_APPLIED':0,'FULL_OUTPUT_ORACLES':'0/128','P05_EXECUTED':'NO','P06_EXECUTED':'NO','NATIVE_STATE_CHANGED':'NO','E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO','INSTALL_EVENTS':0,'NEW_AUTHORITIES':0,'N_REAL_SATISFIED':'NO','HISTORICAL_UNPROVEN_LABELS':'PRESERVED','ORIGINAL_D01_COMPLETE_INPUT_MATRIX':'UNRECOVERED','GIT_DIFF_CHECK':'PASS'}
save(O/'preservation.json',preservation)
classes=read(O/'72-reference-classification.json');front=read(O/'remaining-frontier.json');bindings=read(O/'resolved-bindings.json');verification=read(O/'fresh-process-verification.json');neg=read(O/'negative-suite.json')
assert len(classes['ROWS'])==72 and len(front['ROWS'])==59 and bindings['TOTAL_RESOLVED']==52
assert sum(classes['PRIMARY_CAUSE_COUNTS'].values())==72
assert len({r['all_resolved']['semantic_identity'] for r in verification['records']})==1
assert all(r['all_resolved']['semantic_identity']==bindings['SEMANTIC_IDENTITY'] for r in verification['records'])
report={'WORK_PACKAGE':'E2-P05-D01-OPERAND-RECONCILIATION-4','RESULT':'PARTIAL','INITIAL_TOTAL_REFERENCES':111,'PREVIOUSLY_RESOLVED':39,'INITIAL_UNRESOLVED':72,'RESOLVED_39_PRESERVATION':'PASS_EXACT_ROWS_AND_SOURCE_PINS; all five descriptor derivations independently revalidated','UNRESOLVED_CLASSIFICATION':classes['PRIMARY_CAUSE_COUNTS'],'A03_BOUNDARY':'RECONCILED_PRE_COLLECT_AFTER_CHECK; original D01 acquisition semantics, not entire P05 A03 two-action package','A14_BOUNDARY':'GOVERNED_UNKNOWN_SEMANTIC_PHASES_RECOVERED; V2 bundle/source closure and cold-process transfer remain unresolved','A03_A14_RECONCILIATION':'NO_SHARED_PRODUCER_CONSUMER_EDGE; A03 rebind sealed; A14/N02/A16 concrete process operands incomplete','SOURCE_BINDINGS_RESOLVED':13,'SOURCE_BINDING_BREAKDOWN':{'A03_RETAINED_SUPPLIED_RESULT_REFERENCES':2,'TRUSTED_PRETAMPER_BUNDLE_IDENTITY_REFERENCES':11},'MUTATION_BINDINGS_RESOLVED':0,'MUTATION_DESCRIPTORS_SEALED':0,'PARENT_HEAD_RESOLVED':{'supporting_A03_row_tuples':2,'additional_initial_111_references':0,'rule':'Explicit retained input Snapshot and ordered prefix head; no future output'},'CONTEXT_PHASE_RESOLVED':{'A03_row_contexts':2,'A14':'Semantic phase ownership recovered; concrete source-root/store/persisted handoff not complete'},'RESOLVED_THIS_PACKAGE':13,'TOTAL_RESOLVED':52,'TOTAL_UNRESOLVED':59,'INDEPENDENT_RECONSTRUCTION':'PASS_ALL_52_RESOLVED_BINDINGS_FRESH_SEEDS_0_1_7_101; not complete invocation qualification','RESOLVED_SEMANTIC_IDENTITY':bindings['SEMANTIC_IDENTITY'],'NEGATIVE_SUITE':neg['STATUS'],'NEGATIVE_SUITE_LIMITS':neg['LIMITS'],'CROSS_OPERAND_CONSISTENCY':'PASS_NEW_BOUND_INPUT_PINS_AND_BOUNDARY_RELATIONS; complete rows not qualified','INVOCATION_STATIC_PREFLIGHT':'NOT_RUN','NEXT_UNRESOLVED_CLASS':'A14_BOUNDARY','REMAINING_CLASS_COUNTS':front['PRIMARY_CAUSE_COUNTS'],'D01_INVOCATION_OPERANDS_COMPLETE':'NO','ORACLE_HANDOFF_CREATED':False,'FULL_OUTPUT_ORACLES':'0/128','PROSPECTIVE_D01_MATRIX_CONSTRUCTION_READY':'NO','PROSPECTIVE_D01_SCOPE_DECISION_READY':'NO','PROSPECTIVE_D01_EXECUTION_READY':'NO','END_INTERFACES_BOUND':'4/6','P05_EXECUTION_READY':'NO','E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO','PRESERVATION':preservation,'AUTHORITATIVE_CONTRACT_PINS':[pin(D/(P+'CANONICAL_QUALIFICATION_EXPERIMENT_1.json')),pin(D/(P+'CANONICAL_QUALIFICATION_EXPERIMENT_1.md')),pin(D/(P+'CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md'))],'ARTIFACTS':{p.name:pin(p) for p in sorted(O.iterdir()) if p.is_file() and p.name!='preservation-baseline.json'}}
save(D/(P+'E2_P05_D01_OPERAND_RECONCILIATION_4.json'),report)
lines=['# E2-P05 D01 operand boundary and source/mutation reconciliation 4','',
'`WORK_PACKAGE = E2-P05-D01-OPERAND-RECONCILIATION-4`','',
'**RESULT = PARTIAL.** Thirteen more references are resolved: two A03 acquisition inputs and eleven trusted pre-tamper bundle identities. The original 39 bindings remain unchanged. **52 resolved + 59 unresolved = 111.** No qualification case, mutation, invalidation, output-oracle construction, scope issuance, or END binding occurred.','',
'| Report field | Result |','| --- | --- |',
'| INITIAL_TOTAL_REFERENCES | 111 |','| PREVIOUSLY_RESOLVED | 39 |','| INITIAL_UNRESOLVED | 72 |',
'| SOURCE_BINDINGS_RESOLVED | 13: A03 inputs 2; trusted bundle identities 11 |',
'| MUTATION_BINDINGS_RESOLVED | 0 |',
'| PARENT_HEAD_RESOLVED | Two supporting A03 row tuples; no extra references counted |',
'| CONTEXT_PHASE_RESOLVED | A03 contexts pinned; A14 semantic phase ownership recovered |',
'| RESOLVED_THIS_PACKAGE | 13 |','| TOTAL_RESOLVED | 52 |','| TOTAL_UNRESOLVED | 59 |',
'| INDEPENDENT_RECONSTRUCTION | PASS for all 52 resolved bindings, seeds 0/1/7/101 |',
'| NEGATIVE_SUITE | 20/20 fail-closed static metadata guards |',
'| INVOCATION_STATIC_PREFLIGHT | NOT_RUN: 59 references remain |',
'| NEXT_UNRESOLVED_CLASS | A14_BOUNDARY |','| D01_INVOCATION_OPERANDS_COMPLETE | NO |',
'| FULL_OUTPUT_ORACLES | 0/128 |',
'| PROSPECTIVE_D01_MATRIX_CONSTRUCTION_READY | NO |',
'| PROSPECTIVE_D01_SCOPE_DECISION_READY | NO |',
'| PROSPECTIVE_D01_EXECUTION_READY | NO |',
'| END_INTERFACES_BOUND | 4/6 |','| P05_EXECUTION_READY | NO |',
'| E1_ARTIFACTS_MODIFIED | 0 |','| PRODUCTION_EFFECT | NO |','',
'## Exact primary classification of the 72 initial gaps','',
'Every original unresolved occurrence is classified once by obligation, variant, dispatch step and operand. Secondary effects are described without counting a reference twice. Zero A03/A14 cross-boundary assignments reflects the absence of a producer/consumer edge between those two cases.','',
'| Primary cause | Initial count | Remaining count |','| --- | ---: | ---: |']
for k,v in classes['PRIMARY_CAUSE_COUNTS'].items():lines.append(f"| {k} | {v} | {front['PRIMARY_CAUSE_COUNTS'].get(k,0)} |")
lines+=['','## A03 boundary reconciliation','',
'The original experiment and acceptance matrix define D01 A03 as a **selected acquisition action with a bounded supplied result**. P05 A03’s retained package covers CHECK followed by COLLECT. CHECK is DETERMINISTIC_VALIDATION; COLLECT is SOURCE_ACQUISITION. The sealed D01 capsule was before CHECK, while the retained COLLECT command names the post-CHECK Snapshot. They cannot be paired.','',
'The authoritative publication after CHECK locates the retained native prefix. Its bytes, native current Snapshot identity, ordered ledger prefix/head, source/policy pins, COLLECT operation class, and accepted inventory are checked read-only. The COLLECT command’s expected_snapshot equals that exact prefix state. Both A03 rows now bind this existing SuppliedResult and require explicit snapshot/bundle/policy/version source overlays. The old capsule files and V2 operation sequence are preserved.','',
'The producer’s prior CHECK occurrence is retained input history. The prospective A03 operation owns future application/append and post-state; neither is supplied as pre-state. No CHECK or COLLECT operation was rerun. Native IDs remain distinct from qualification binding digests.','',
'## A14 boundary and dependent conflicts','',
'A14 independently requires an external checkpoint copy with rule_known=false and a valid ExternalResolutionContract, followed by native recompute, persistence, writer termination, and cold restore. Computation is an observation, not a PersistenceBundle or a positive Evidence receipt. Recompute does not authorize a rule-known flag patch or receipt continuation. A16’s acquisition-contract invalidation belongs after A14 restore.','',
'The prospective backend remains sealed V2 save_bundle/restore. The Snapshot-only capsule has no bundle, exact policy/source-root/archive construction, or durable native save-return handoff. Native save supplies a Path and planner-bundle-v1 identity for restore; their ownership is mechanically identified, but an in-memory prior_result cannot alone cross writer termination into a cold reader. These references stay unresolved until the concrete producer and transfer are pinned. The retained E06 Snapshot analogue is not substituted for an event-bearing V2 bundle.','',
'The original N02 case explicitly starts from an A14 copy. Its current capsules instead have rule_known=true and a different lineage/generation. Binding a mutated A09 command would test that later receipt-admission boundary, not establish the required unknown-rule route variant. Those eight references are A14 boundary gaps. A14 itself contributes six and A16 two. Generic controls are not assigned to A14 merely because their labels resemble N02.','',
'## Sources and mutation contracts','',
'Eleven expected_bundle_identity references are now native CONTENT_IDENTITY/planner-bundle-v1 values derived from the exact retained capsule-owned pre-tamper bytes. Each source matches the capsule bundle, canonical structural encoding, and every declared source/policy pin. These are externally trusted inputs to restore. Attacker-rehashed bytes or future post-mutation outputs never replace them. The corresponding mutated path remains unresolved.','',
'Candidate inventories retain original source classifications, exact pointers/identities, owning scopes/lineages, and currentness checks. Broad composite END qualification does not automatically authorize a candidate for a runner row. Source/report/specification candidates are not promoted to native inputs by presentation order, name, recency, or convenience.','',
'No remaining mutation has a uniquely pinned complete base/target/operator/parameter combination. The inventory separates those requirements and intended changed/unchanged dimensions; it is not an executable descriptor set. No arbitrary wrong request, authority class, producer, source index, or Snapshot field is chosen. SourceInvalidation remains a separate native descriptor type. The five Closure-3 descriptors are preserved and independently re-derived from their original receipt/route identities without application.','',
'## Reconstruction, negatives and limits','',
'Fresh independent processes under hash seeds 0, 1, 7 and 101 reconstruct the 39 preserved bindings, five invalidation derivations, raw-payload mapping, and 13 new source bindings. They produce one identity:','',
'`'+bindings['SEMANTIC_IDENTITY']+'`','',
'Twenty static guards reject A03/A14 pre/post swaps and cross-consumption, future-result substitution, post-mutation base substitution, unsealed mutation targets/operators, applied descriptors, invalidation/mutation confusion, wrong receipt/route/source, stale source pins, wrong identity domains, parent/head, phase/context, and cross-row leakage. Target/operator guards reject unsealed descriptors; they do not claim a complete accepted mutation oracle or native negative execution.','',
'Current native source pins match Closure 3, and runner/helper/dispatch bytes match the sealed V2 contract. New operand scope/lineage/generation come from their exact input states. A03 source overlays and parent/head relations are explicit. Native structural loading and pin checks are not full semantic bundle replay or case execution. All 128 invocation records remain documentary drafts. Complete preflight and the oracle handoff are withheld.','',
'## Remaining frontier','',
'First pin A14’s concrete bundle/source root/policy/archive closure and durable save-return transfer across writer termination. Then reconcile its N02/A16 consumer boundaries. Remaining mutation families need exact source/target/operator/parameters; source invalidations need one uniquely eligible dependency-bearing boundary or a sealed all-source realization. SOURCE_BYTES still requires every current/prefix source, while V2 exposes one unselected LOAD_PIN argument; a singular arbitrary pin cannot satisfy that collection obligation.','',
'## Machine-readable evidence','',
'All supporting files are in `qualification/E2_P05_D01_OPERAND_RECONCILIATION_4/`:','',
'- `frozen-39-bindings.json` and `72-reference-classification.json`.',
'- `a03-boundary-oracle.json`, `a14-boundary-oracle.json`, `boundary-conflicts.json`, `affected-row-boundary-map.json`.',
'- `new-source-bindings.json`, `a03-invocation-source-overrides.json`, `resolved-bindings.json`.',
'- `source-candidate-inventory.json`, `mutation-contract-inventory.json`, `mutation-descriptors.json`.',
'- `cross-operand-checks.json`, `runtime-currentness.json`, `reconciled-invocation-drafts.json`.',
'- `fresh-process-verification.json`, `negative-suite.json`, `remaining-frontier.json`.',
'- `reconcile.py`, `verify.py`, `negatives.py`, `invocation_overlay.py`, `report.py`.',
'- `preservation-baseline.json` and `preservation.json`.','',
'## Preservation','',
'Every pre-existing adapter/docs file in the baseline is unchanged, including Closure 3 bindings, V2 metadata, all 117 capsules, and E1. P05 stage bindings remain 13/13; PC01/PC02/PC03/T01 remain PASS; END remains 4/6; E2-D01 stays BLOCKED; the continuation interface is unchanged. All historical UNPROVEN labels and original D01 input-matrix UNRECOVERED status remain.','',
'`QUALIFICATION_CASES_EXECUTED = 0`; `MUTATIONS_APPLIED = 0`; `INVALIDATIONS_APPLIED = 0`; `P05_EXECUTED = NO`; `P06_EXECUTED = NO`; `NATIVE_STATE_CHANGED = NO`; `INSTALL_EVENTS = 0`; `NEW_AUTHORITIES = 0`; `N_REAL_SATISFIED = NO`; `E1_ARTIFACTS_MODIFIED = 0`; `PRODUCTION_EFFECT = NO`; `git diff --check = PASS`.','']
(D/(P+'E2_P05_D01_OPERAND_RECONCILIATION_4.md')).write_text('\n'.join(line.rstrip() for line in lines))
print('REPORT=PARTIAL; 39 preserved + 13 new = 52 resolved; 59 unresolved; all pre-existing files unchanged')
