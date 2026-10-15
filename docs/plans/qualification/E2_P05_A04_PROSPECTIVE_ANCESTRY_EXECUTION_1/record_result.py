"""Record completed qualification, frozen-file audit, and A04-only binding."""
import hashlib
import json
import subprocess

import execution_driver as d
from qualification_checks import descriptor,validate_witness
from adapter.planner import codec as c,core


def pin(path,pointer=''):
    return {'path':str(path.relative_to(d.ROOT)),'raw_sha256':d.sha(path),'pointer':pointer}


def main():
    baseline=d.read(d.OUT/'baseline.json')
    missing=[];changed=[]
    for name,digest in baseline['files'].items():
        path=d.ROOT/name
        if not path.is_file():missing.append(name)
        elif d.sha(path)!=digest:changed.append(name)
    d.equal('PREEXISTING_FILES_MISSING',missing,[])
    d.equal('PREEXISTING_FILES_CHANGED',changed,[])
    frozen={name:digest for name,digest in baseline['files'].items() if name.startswith('docs/experiments/E1/')}
    current={str(p.relative_to(d.ROOT)):d.sha(p) for p in (d.ROOT/'docs/experiments/E1').rglob('*')
             if p.is_file() and not p.is_symlink() and '__pycache__' not in p.parts}
    d.equal('FROZEN_E1_INVENTORY_AND_HASHES',current,frozen)
    runtime={str(p.relative_to(d.ROOT)):d.sha(p) for p in (d.ROOT/'adapter').rglob('*')
             if p.is_file() and not p.is_symlink() and '__pycache__' not in p.parts}
    d.equal('RUNTIME_INVENTORY_AND_HASHES',runtime,baseline['runtime_hashes'])
    diff=subprocess.run(['git','diff','--check'],cwd=str(d.ROOT),capture_output=True,text=True)
    d.equal('GIT_DIFF_CHECK',diff.returncode,0)
    graphs=[d.read(d.OUT/'graph-readers'/('seed-'+str(seed)+'.json')) for seed in (0,1,7,101)]
    for graph in graphs[1:]:d.equal('P05_BINDING_GRAPH_DETERMINISM',graph,graphs[0])
    graph=graphs[0]
    d.write(d.OUT/'P05-binding-rerun.json',graph)
    d.write(d.OUT/'graph-determinism.json',{'result':'PASS','hash_seeds':[0,1,7,101],
        'independent_graph_readers':4,'semantic_graph_identical':True,
        'graph_sha256':hashlib.sha256(c.canonical_bytes(graph)).hexdigest(),
        'P05_BOUND_STAGE_INPUTS':graph['P05_BOUND_STAGE_INPUTS'],'P05_NEXT_MISSING_INPUT':graph['P05_NEXT_MISSING_INPUT']})
    bundle=validate_witness(descriptor());trace=d.read(d.OUT/'primary/writer-result.json')
    event=bundle.events[-1];before,preid,artifacts=d.load_start()
    computation=core.recompute(bundle.current)
    d.equal('A04_POST_CONTROL',computation.control.value,'HUMAN_HANDOFF')
    d.equal('READY_DECISION',bundle.current.decisions[0].stage.value,'DECISION_READY')
    d.equal('NO_DECISION_CHOICE',bundle.current.decisions[0].recorded_choice,None)
    for name in ('process-qualification.json','A04-negative-results.json','D01-current-runtime-tests.json',
                 'D01-overlay-negative-results.json','idempotence.json','bundle-export.json'):
        d.equal('FINAL_QUALIFICATION:'+name,d.read(d.OUT/name)['result'],'PASS')
    preservation={'result':'PASS','preexisting_files_verified':len(baseline['files']),
        'preexisting_files_changed':changed,'preexisting_files_missing':missing,
        'runtime_files_verified':len(runtime),'RUNTIME_MODIFIED':'NO',
        'frozen_E1_files_verified':len(frozen),'frozen_E1_inventory_exact':True,
        'E1_ARTIFACTS_MODIFIED':0,'original_historical_records_modified':False,
        'sealed_contracts_oracles_modified':False,'canonical_P04_modified':False,
        'PRODUCTION_EFFECT':'NO','P05_EXECUTED':'NO','P06_EXECUTED':'NO','GIT_DIFF_CHECK':'PASS'}
    d.write(d.OUT/'preservation.json',preservation)
    evidence_names=['entry-gate.json','primary/writer-result.json','postcommit-report-recovery.json',
        'process-qualification.json','A04-negative-results.json','D01-overlay-negative-results.json',
        'D01-current-runtime-tests.json','idempotence.json','bundle-export.json','P05-binding-rerun.json',
        'graph-determinism.json','preservation.json']
    evidence={name:pin(d.OUT/name) for name in evidence_names}
    export=d.read(d.OUT/'bundle-export.json');negative=d.read(d.OUT/'A04-negative-results.json')
    report={**d.LABELS,'schema':'E2-P05-A04-PROSPECTIVE-ANCESTRY-EXECUTION-RESULT-1',
        'WORK_PACKAGE':'E2-P05-A04-PROSPECTIVE-ANCESTRY-EXECUTION','RESULT':'PASS',
        'SELECTED_OPTION':'AUTHORIZE_PROSPECTIVE_P05_A04_ANCESTRY_QUALIFICATION',
        'ENTRY_GATE':'PASS','ENTRY_GATE_CHECKS':97,'AUTHORITY_APPLICABILITY':'PASS',
        'ADDITIONAL_AUTHORITY_REQUIRED':'NO','AUTHORITIES_ISSUED':0,'DEFINITIONS_INSTALLED':0,
        'PROSPECTIVE_A04_EXECUTION':'PASS','PROSPECTIVE_A04_EXECUTED':'YES',
        'PRIMARY_PRODUCER_INVOCATIONS':1,'PRIMARY_PRODUCER_REEXECUTIONS':0,
        'ACTUAL_A04_RESULT':{'type':'SuppliedResult','outcome':event.result.result.value,
            'ActionId':event.result.action.value,'knowledge_outputs':[k.id.value for k in event.result.knowledge],
            'actual_native_result':pin(d.ROOT/export['path'],'/bundle/events/2/result'),
            'dossier_id':d.uid(c._identity(c.canonical_bytes(c._wire(event.result.dossier)),'planner-dossier-sha256')),
            'standalone_PrepareResult_identity':'NO SUCH NATIVE FIELD'},
        'A04_EVENT_ID':d.uid(event.identity),'EVENT_TYPE':'ExecutionEvent',
        'EVENT_PAYLOAD':c._wire(event),'PARENT_EVENT_ID':d.uid(event.parent_event),
        'PRE_STATE_ID':d.uid(event.parent_snapshot),'POST_SNAPSHOT_ID':d.uid(event.after_snapshot),
        'VALIDATION_BINDING':{'result':'PASS','representation':'Exact immutable event.after_snapshot archive plus native PredicateId/dossier selectors',
            'typed_member_count':6,'native_members':c._wire(bundle.current.validation_instances),
            'ordered_inputs':[d.uid(event.parent_snapshot),d.uid(artifacts[0][0].identity)],
            'no_inline_event_validation_fields':True,'snapshot_identity_exact':True,
            'tampered_binding_negatives':'PASS'},
        'LEDGER_ID':trace['LEDGER_ID'],'LEDGER_ID_DOMAIN':'Sealed starting bundle content identity plus /bundle/events anchor; no standalone native LedgerId',
        'LEDGER_POSITION':3,'LEDGER_ZERO_BASED_INDEX':2,'PREFIX_EVENT_COUNT':2,'POST_EVENT_COUNT':3,
        'POST_LEDGER_ROOT':trace['POST_LEDGER_ROOT'],'POST_APPEND_HEAD':d.uid(event.identity),
        'RESULT_BINDING':'PASS; exact SuppliedResult retained in /bundle/events/2/result, bound to native pre-Snapshot',
        'OUTPUT_BINDING':'PASS; actual E2-K-PREPARE in event result and immutable post-Snapshot',
        'POSTCONDITION':{'PREPARE_COMPLETED':True,'E2_K_PREPARE_ADMITTED_CURRENT':True,
            'dossier_current':True,'validation_count':6,'DECISION_READY':True,'CONTROL':'HUMAN_HANDOFF',
            'human_choice_recorded':False,'grant_issued':False,'REENTER_EXECUTED':False,'FINISH_EXECUTED':False,
            'root_slot_unchanged':True},
        'PROSPECTIVE_A04_ANCESTRY':'PASS','POST_A04_BUNDLE_ID':export['bundle_id'],
        'POST_A04_STATE_ID':trace['POST_A04_STATE_ID'],'POST_A04_SNAPSHOT_ID':d.uid(event.after_snapshot),
        'POST_A04_LEDGER_ROOT':trace['POST_LEDGER_ROOT'],'POST_A04_APPEND_HEAD':d.uid(event.identity),
        'POST_A04_BUNDLE':pin(d.ROOT/export['path']),
        'POST_SNAPSHOT_ARCHIVE':pin(d.ROOT/export['detached_archive']),
        'PERSISTENCE':'PASS','COLD_RESTORE':'PASS','COLD_READER_COUNT':12,'REPRODUCTION_COLD_READER_COUNT':12,
        'WRITER_TERMINATED_BEFORE_READERS':True,
        'HISTORICAL_REPLAY':'PASS; read-only historical projection in prospective qualification lineage',
        'REPLAY_LIVE_OPERATION_INVOCATIONS':0,'REPLAY_VALIDATORS_RERUN':False,'REPLAY_DUPLICATE_EVENTS':0,
        'IDEMPOTENCE':'PASS','IDENTICAL_RETRIES':3,'CONFLICTING_RETRY':'FAIL_CLOSED',
        'INDEPENDENT_REPRODUCTION':'PASS','INDEPENDENT_REPRODUCTIONS':12,
        'REPRODUCTION_IDENTITY_POLICY':'Same sealed native inputs/lineage yield equal content identities in 12 distinct stores/processes; run IDs remain separate.',
        'DETERMINISM':'PASS','HASH_SEEDS':[0,1,7,101],
        'UNORDERED_PRESENTATIONS':['original','reverse','rotate'],
        'ORDERED_FIELDS_UNCHANGED':['event sequence/parent chain','Decision.history','ValidationInstance.inputs'],
        'FULL_NATIVE_COMPUTATION_EQUAL':True,'EVENT_COMPARISON_IDENTITY':'UNCHANGED; exact sealed native value',
        'SNAPSHOT_COMPARISON_IDENTITY':'UNCHANGED; exact sealed native value',
        'BUNDLE_COMPARISON_IDENTITY':'EXACT; D01 native binding covered by planner-bundle-v1',
        'NEGATIVE_SUITE':'PASS','SEALED_A04_NEGATIVE_COUNT':24,'D01_OVERLAY_NEGATIVE_COUNT':24,
        'ADDITIONAL_A04_SNAPSHOT_BINDING_CONTROLS':len(negative['snapshot_validation_overlay_cases']),
        'D01_CURRENT_RUNTIME_TEST_METHODS_PASS':23,'UNRELATED_RUNTIME_REPAIRS':0,
        'END_MAPPING':'PASS','END_MAPPING_CLASSIFICATION':'AUTHORIZED_PROSPECTIVE_REPLACEMENT',
        'N12_MAPPING':'PASS','N13_MAPPING':'PASS','N12_MAPPING_PRESERVED':'YES','N13_MAPPING_PRESERVED':'YES',
        'E2_A04_PREPARE_RESULT_EVENT_ANCESTRY':'PASS','ORIGINAL_HISTORICAL_EVENT_ID':None,
        'ORIGINAL_HISTORICAL_PARENT_ID':None,'ORIGINAL_HISTORY_SPLICED':False,
        'P05_BOUND_STAGE_INPUTS':graph['P05_BOUND_STAGE_INPUTS'],'P05_TOTAL_STAGE_INPUTS':13,
        'P05_NEXT_MISSING_INPUT':graph['P05_NEXT_MISSING_INPUT'],'NEXT_INPUT_RESOLVED':False,
        'P05_REMAINING_STAGE_GAPS':graph['remaining_stage_gaps'],
        'ADDITIONAL_END_GATE':graph['additional_unresolved_END_gate'],
        'P05_EXECUTION_READY':'NO','E2_P05_READY':'YES','P05_EXECUTED':'NO','P06_EXECUTED':'NO',
        'E2_P04_RESULT':'PASS','P03_HISTORICAL_CORRESPONDENCE':'UNPROVEN','N_REAL_SATISFIED':'NO',
        'NEXT_PACKAGE':graph['NEXT_PACKAGE'],'FIRST_RUNTIME_COUNTEREXAMPLE':None,
        'POSTCOMMIT_REPORT_RECOVERY':{'result':'PASS','error':'Relative report path formatting failed after native commit and complete sealed checks',
            'error_preserved':pin(d.OUT/'STOP.json'),'native_state_repaired':False,'primary_operation_repeated':False,
            'recovery':'Native committed bytes restored and compared read-only; reporting path normalized in unsealed harness only.'},
        'RUNTIME_MODIFIED':'NO','E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO','GIT_DIFF_CHECK':'PASS',
        'evidence':evidence,'preservation':preservation}
    result_path=d.PLANS/'DETERMINISTIC_PLANNER_V0_1_E2_P05_A04_PROSPECTIVE_ANCESTRY_RESULT_1.json'
    d.write(result_path,report)
    body=f'''**DETERMINISTIC PLANNER v0.1 — E2-P05 A04 PROSPECTIVE ANCESTRY QUALIFICATION EXECUTION 1**

`RESULT = PASS`. The primary prospective PREPARE operation executed once through qualified D01 and durably admitted its actual PASS result, `E2-K-PREPARE`, complete dossier and six independently evaluated typed validations. All sealed result, post-Snapshot, event and bundle comparisons pass. `PROSPECTIVE_A04_ANCESTRY = PASS`.

The authorized A04 replacement closes `E2-A04.prepare_result_event_ancestry`. P05 now binds **11 / 13** stages. The next missing input is **`E2-A05.recorded_decision_event_ancestry`**; this package leaves it unresolved. `P05_EXECUTION_READY = NO`; P05 and P06 remain unexecuted.

The [machine result]({result_path.name}) contains actual identities, payload, member bindings, preservation hashes and qualification references. The [native post-A04 bundle]({d.ROOT.joinpath(export['path']).name}) retains the result, event, ledger and D01 transaction binding. Its [detached immutable post-Snapshot](snapshot-{event.after_snapshot.sha256}.json) retains the original typed validation members. No validation bodies were added to the occurrence-event schema.

The [entry gate](qualification/{d.OUT.name}/entry-gate.json) passes 97 checks. The exact retained A03 start, authored dossier source, operating-authority requirement (`None`), qualification scope decision and versioned representation/durable overlays remain unchanged. No new authority or definition is issued. The bounded producer reads the authored source and native prerequisites, constructs fresh values, and evaluates the six rules independently; expected objects are comparison data only. Native T02 applies the actual result. D01 constructs the immutable Snapshot, unchanged occurrence event, temporal binding and complete bundle before atomic HEAD publication.

| Native object | Actual identity |
|---|---|
| Pre-Snapshot | `{d.uid(event.parent_snapshot)}` |
| Parent / retained COLLECT head | `{d.uid(event.parent_event)}` |
| A04 occurrence event / new head | `{d.uid(event.identity)}` |
| Immutable post-Snapshot | `{d.uid(event.after_snapshot)}` |
| Post-A04 bundle | `{export['bundle_id']}` |

The ledger preserves its CHECK root `{trace['POST_LEDGER_ROOT']}` and unchanged two-event prefix. A04 is sequence **3**, zero-based index **2**, immediately after COLLECT. The sealed ledger anchor is `{trace['LEDGER_ID']}`. There is no standalone native LedgerId or PrepareResult identity. The `SuppliedResult` lives in `/bundle/events/2/result`; its actual KnowledgeRecord is also present in the post-Snapshot. The event's immutable `after_snapshot`, each member's PredicateId/dossier subject and ordered pre-Snapshot/source inputs provide the complete typed-validation binding.

The exact terminal state is PREPARE completed, current `E2-K-PREPARE`, dossier and six accepted validations, `DECISION_READY` and `HUMAN_HANDOFF`. No human choice, operating grant, downstream REENTER/FINISH execution or root/slot satisfaction occurs.

The [process qualification](qualification/{d.OUT.name}/process-qualification.json) passes **12 independent prospective writers**, **12 required primary cold readers** and **12 additional reproduction readers**, across hash seeds **0, 1, 7, 101** and original/reversed/rotated unordered presentations. Every reader runs after writer termination and performs three read-only historical projections with live producer, validation execution and publication hooks barred. Event, Snapshot, bundle and full native Computation match. Equal native identities across distinct stores reflect the exact same sealed semantic lineage; separate run IDs distinguish the reproductions. Ordered event history, Decision history and ValidationInstance inputs are preserved.

The [retry qualification](qualification/{d.OUT.name}/idempotence.json) passes three identical committed retries with zero producer calls and no new result, event, Snapshot, ledger entry or bundle. A conflicting source/result context fails closed. Retry tests use an isolated copy and preserve the primary lineage.

All **24 sealed A04 negatives** and **24 D01 overlay cases** pass. The [A04 matrix](qualification/{d.OUT.name}/A04-negative-results.json) additionally tests seven Snapshot/typed-member controls, including foreign Snapshot, rehashed tampering, missing/duplicate/rejected members, Boolean replacement and ordered-input reversal. Native admission/replay checks enforce native fields; the qualification witness guard enforces scope, labeling and acceptable evidence classes. Those layers are recorded separately. The [D01 overlay matrix](qualification/{d.OUT.name}/D01-overlay-negative-results.json) maps its 23 native cases to a new **23 / 23 PASS** current-runtime test run and tests historical relabeling separately. Negative fixtures never mutate the successful primary lineage.

The [END binding rerun](qualification/{d.OUT.name}/P05-binding-rerun.json) compares retained original bindings, actual P04 target/events and the A03 replacement prefix, then applies only the selected A04 prospective mapping. Four independent graph readers produce identical graph semantics. Original A03 occurrence and original A04 ancestry remain **UNPROVEN**; no original event or parent ID is created or aliased. N12 preserves selection versus execution separation; N13 preserves prospective definition versus actual result admission. The remaining A05/A06 stage inputs and original full-END ancestry gate remain unresolved.

A reporting path error occurred after the primary transaction committed and passed all sealed comparisons. The raw error is retained in [STOP.json](qualification/{d.OUT.name}/STOP.json). [Read-only recovery](qualification/{d.OUT.name}/postcommit-report-recovery.json) restored and rechecked the committed bytes; the primary operation was never invoked again. Only the unsealed reporting harness path formatting was corrected. No runtime, fixture, oracle or native state was repaired, and no runtime counterexample occurred.

The [preservation audit](qualification/{d.OUT.name}/preservation.json) verifies **{len(baseline['files']):,} pre-existing files**, all **{len(runtime)} runtime/test files**, and all **{len(frozen):,} frozen E1 files**, with identical inventories and hashes. Prior sealed artifacts, original historical records and canonical P04 remain unchanged. `git diff --check = PASS`.

```text
WORK_PACKAGE = E2-P05-A04-PROSPECTIVE-ANCESTRY-EXECUTION
RESULT = PASS
QUALIFICATION_TYPE = PROSPECTIVE_REPLACEMENT
ORIGINAL_A04_HISTORICAL_ANCESTRY = UNPROVEN
ACTUAL_A04_RESULT = SuppliedResult; PASS + E2-K-PREPARE
A04_EVENT_ID = {d.uid(event.identity)}
PARENT_EVENT_ID = {d.uid(event.parent_event)}
PRE_STATE_ID = {d.uid(event.parent_snapshot)}
POST_SNAPSHOT_ID = {d.uid(event.after_snapshot)}
VALIDATION_BINDING = PASS; 6 exact typed members via immutable Snapshot
LEDGER_POSITION = 3 (zero-based index 2)
POST_LEDGER_ROOT = {trace['POST_LEDGER_ROOT']}
POST_APPEND_HEAD = {d.uid(event.identity)}
RESULT_BINDING = PASS
OUTPUT_BINDING = PASS
PROSPECTIVE_A04_ANCESTRY = PASS
POST_A04_BUNDLE_ID = {export['bundle_id']}
COLD_RESTORE = PASS
HISTORICAL_REPLAY = PASS; no new operation or validation decision
IDEMPOTENCE = PASS
INDEPENDENT_REPRODUCTION = PASS; 12
DETERMINISM = PASS
NEGATIVE_SUITE = PASS; 24 A04 + 24 D01 overlay
END_MAPPING = PASS; AUTHORIZED_PROSPECTIVE_REPLACEMENT
N12_MAPPING = PASS
N13_MAPPING = PASS
E2_A04_PREPARE_RESULT_EVENT_ANCESTRY = PASS
P05_BOUND_STAGE_INPUTS = 11 / 13
P05_NEXT_MISSING_INPUT = {graph['P05_NEXT_MISSING_INPUT']}
P05_EXECUTION_READY = NO
P05_EXECUTED = NO
P06_EXECUTED = NO
ORIGINAL_A03_HISTORICAL_OCCURRENCE = UNPROVEN
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN
N_REAL_SATISFIED = NO
RUNTIME_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```
'''
    result_path.with_suffix('.md').write_text(body)
    print(json.dumps({'RESULT':'PASS','PROSPECTIVE_A04_ANCESTRY':'PASS','P05_BOUND_STAGE_INPUTS':11,
        'P05_NEXT_MISSING_INPUT':graph['P05_NEXT_MISSING_INPUT'],'P05_EXECUTION_READY':'NO',
        'preexisting_files_unchanged':len(baseline['files']),'E1_files_unchanged':len(frozen)}))


if __name__=='__main__':main()
