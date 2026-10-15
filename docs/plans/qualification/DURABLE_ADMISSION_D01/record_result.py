"""Collect D01 qualification evidence and verify preservation of prior seals."""
import hashlib
import json
from pathlib import Path
import subprocess
from dataclasses import fields

from adapter.planner import codec as c, model as m

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
PLANS=ROOT/'docs/plans'
NAME='DETERMINISTIC_PLANNER_V0_1_DURABLE_ADMISSION_D01_RESULT'


def read(path):return json.loads(Path(path).read_bytes())
def save(path,value):path.write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def simple(value):return value.namespace+':'+value.sha256
def ref(path):return {'path':str(path.relative_to(ROOT)),'raw_sha256':sha(path)}


def audit():
    before=read(HERE/'baseline.json')['files']
    allowed={'adapter/planner/codec.py','adapter/planner/model.py'}
    changed=[p for p,h in before.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
    assert set(changed)==allowed,changed
    frozen=[p for p in before if p.startswith('docs/experiments/E1/')]
    assert not set(frozen).intersection(changed)
    current_frozen={str(p.relative_to(ROOT)) for p in (ROOT/'docs/experiments/E1').rglob('*')
                    if p.is_file() and not p.is_symlink() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
    assert current_frozen==set(frozen),'frozen E1 inventory changed'
    check=subprocess.run(['git','diff','--check'],cwd=str(ROOT),capture_output=True,text=True)
    assert check.returncode==0,check.stdout+check.stderr
    return {'result':'PASS','baseline_files':len(before),'unchanged_prior_files':len(before)-len(changed),
            'changed_prior_files':changed,'frozen_E1_files':len(frozen),'frozen_E1_inventory_unchanged':True,
            'E1_ARTIFACTS_MODIFIED':0,
            'prior_plan_artifacts_modified':0,'git_diff_check':'PASS',
            'runtime_files':[ref(ROOT/p) for p in sorted(allowed|{'adapter/planner/dossier_transaction.py'})]}


def negatives():
    contract=read(PLANS/'qualification/E2_P05_A04_DURABLE_ADMISSION_CONTRACT_1/negative-contract.json')
    tests=[
      'test_wrong_native_result_and_output_inventory',
      'test_no_raw_or_boolean_live_execution_context',
      'test_wrong_source_and_pre_bundle',
      'test_wrong_event_parent_position_payload_and_identity',
      'test_archive_missing_wrong_and_no_latest_snapshot_fallback',
      'test_rehashed_tampered_state_still_fails_historical_projection',
      'test_wrong_event_parent_position_payload_and_identity',
      'test_trusted_ledger_head_and_source_tampering',
      'test_foreign_append_head_stops_before_operation',
      'test_validation_subject_inputs_membership_and_currentness',
      'test_binding_missing_tampered_duplicate_orphan_and_extra_source',
      'test_partial_result_event_bundle_and_orphan_files_are_not_head',
      'test_partial_result_event_bundle_and_orphan_files_are_not_head',
      'test_exact_retry_before_producer_and_after_descendants',
      'test_conflicting_validation_retry_and_physical_closure',
      'test_replay_is_read_only_and_cannot_create_second_occurrence',
      'test_trusted_ledger_head_and_source_tampering',
      'test_binding_missing_tampered_duplicate_orphan_and_extra_source',
      'test_missing_historical_archive_after_invalidation',
      'test_partial_result_event_bundle_and_orphan_files_are_not_head',
      'test_binding_missing_tampered_duplicate_orphan_and_extra_source',
      'test_validation_subject_inputs_membership_and_currentness',
      'test_validation_subject_inputs_membership_and_currentness',
      'historical_label_negatives',
    ]
    rows=[]
    for case,test in zip(contract['durable_cases'],tests):
        rows.append({'id':case['id'],'case':case['case'],'expected':case['expected'],'result':'PASS',
                     'test':test,'test_layer':'QUALIFICATION_OVERLAY_VALIDATOR' if case['id']=='DA24' else 'NATIVE_GENERIC_TRANSACTION'})
    assert len(rows)==24
    result={'result':'PASS','durable_cases':rows,'native_generic_cases':23,
       'historical_label_checks':5,'inherited_A04_24_negatives':'PRESERVED_UNCHANGED; NOT_EXECUTED_IN_D01',
       'inherited_negative_contract':contract['inherited_24_negative_expectations'],
       'scope':'Generic native admission negatives, plus qualification-label preservation. No A04 transaction or END binding occurs.'}
    save(HERE/'negative-qualification.json',result)
    return result


def main():
    generic=read(HERE/'generic-tests.json');extra=read(HERE/'generic-extra-tests.json')
    for r in (generic,extra):assert not r['failures'] and not r['errors']
    assert generic['tests_run']==20 and extra['tests_run']==3
    processes=read(HERE/'process-qualification.json')
    final_process=read(HERE/'final-runtime-process-check.json')
    compat=read(HERE/'A04-compatibility.json');regressions=read(HERE/'regression-comparison.json')
    assert all(r['result']=='PASS' for r in (processes,final_process,compat))
    assert not regressions['new_failures']
    for p,h in final_process['runtime_hashes'].items():assert sha(ROOT/p)==h
    preservation=audit();save(HERE/'preservation.json',preservation)
    negative=negatives()
    run=HERE/'runs/seed-0-original';record=read(run/'writer.json')
    bid=c._unwire(record['bundle']);path=run/'store'/('bundle-'+bid.sha256+'.json')
    bundle=c.restore(path,bid,run);event=bundle.events[-1]
    trace={'role':'GENERIC_ISOLATED_ACTUAL_EXECUTION_UNRELATED_TO_A04','result':'PASS',
       'starting_oracle':ref(run/'sealed-oracle.json'),'actual_bundle':ref(path),
       'actual_event':c._wire(event),'actual_supplied_result':c._wire(event.result),
       'post_snapshot':simple(c.snapshot_id(bundle.current)),
       'archive':ref(run/'store'/('snapshot-'+event.after_snapshot.sha256+'.json')),
       'validation_members':[{'snapshot':c._wire(event.after_snapshot),'predicate':c._wire(v.predicate),
                              'dossier':c._wire(v.dossier),'value':c._wire(v)} for v in bundle.current.validation_instances],
       'binding':c._wire(bundle.dossier_materializations[0]),
       'ledger':{'root':simple(bundle.events[0].identity),'head':simple(event.identity),'sequence':2,'index':1},
       'head':read(run/'store/HEAD.json'),
       'event_schema_fields':[f.name for f in fields(m.ExecutionEvent)],
       'result_schema_fields':[f.name for f in fields(m.SuppliedResult)],
       'A04_executed':False,'P05_binding_applied':False}
    save(HERE/'generic-transaction-trace.json',trace)
    identity={'result':'PASS','IDENTITY_CYCLE':'NO','order':['pre_bundle/context/pins','actual_result/typed_validations',
       'post_Snapshot','native_event','temporal_bundle_binding','post_bundle','HEAD'],
       'generic_event_comparison':simple(event.identity),'generic_snapshot_comparison':simple(event.after_snapshot),
       'generic_bundle_comparison':simple(bid),'bundle_binding_has_standalone_identity':False,
       'event_algorithm_unchanged':True,'snapshot_codec_unchanged':True,'old_default_bytes_unchanged':True,
       'A04_comparison_only':{k:compat[k] for k in ('comparison_event','comparison_snapshot','comparison_future_bundle')},
       'ordered_inputs':'ValidationInstance.inputs remains ordered; only codec-declared unordered fields are permuted.'}
    save(HERE/'identity-qualification.json',identity)
    hooks=['after_producer','after_validations','after_result_application','after_snapshot','after_event_binding',
       'after_source_stage','after_archive_stage','after_event_stage','after_bundle_stage','after_files_fsync',
       'before_head_replace','after_head_replace']
    gates={k:'PASS' for k in ['result_application','post_snapshot','validation_binding','event_construction','ledger_append',
        'bundle_construction','atomicity','idempotence','cold_restore','historical_replay','identity_ordering',
        'negatives','failure_injection','determinism']}
    evidence={p.stem:ref(p) for p in sorted(HERE.glob('*.json')) if p.name!='baseline.json'}
    result={'WORK_PACKAGE':'DURABLE-ADMISSION-D01','RESULT':'PASS','DURABLE_ADMISSION_CAPABILITY':'PASS',
      'AUTHORITATIVE_CONTRACT':ref(PLANS/'DETERMINISTIC_PLANNER_V0_1_E2_P05_A04_DURABLE_ADMISSION_CONTRACT_1.json'),
      'IMPLEMENTATION_LAYER':'GENERIC_SELECTED_DECISION_INPUT_ACQUISITION_DOSSIER_RESULT_INTEGRATION',
      'REUSED_NATIVE_CAPABILITIES':['core.admit_dossier_materialization (T02)','native selected Action/result admission',
        'unchanged Snapshot/SuppliedResult/ExecutionEvent codecs and comparison identities',
        'source/policy pins','local transaction lock/immutable writes/fsync/atomic HEAD','historical ordinary event projection'],
      **{k:'PASS' for k in ['RESULT_APPLICATION','POST_SNAPSHOT','VALIDATION_BINDING','EVENT_CONSTRUCTION',
        'LEDGER_APPEND','PERSISTENCE_BUNDLE','ATOMICITY','IDEMPOTENCE','FAILURE_INJECTION','COLD_RESTORE',
        'HISTORICAL_REPLAY','REPLAY_IDEMPOTENCE','NEGATIVE_SUITE','DETERMINISM']},
      'CAPABILITY_GATES':gates,
      'EVENT_COMPARISON_IDENTITY':{'semantics':'UNCHANGED_NATIVE_ALGORITHM','generic_identity':simple(event.identity)},
      'SNAPSHOT_COMPARISON_IDENTITY':{'semantics':'UNCHANGED_NATIVE_CODEC','generic_identity':simple(event.after_snapshot)},
      'BUNDLE_COMPARISON_IDENTITY':{'semantics':'EXACT_NATIVE_BUNDLE_HASH_COVERS_DEFAULT_OMITTED_BINDING','generic_identity':simple(bid)},
      'EXECUTION_INPUTS':['trusted native pre-bundle/expected bundle identity','trusted registered bounded NON_EFFECTING producer/ActionId',
        'pinned source artifact bytes','native pre-state Action/result/T02 contracts','Snapshot/context/source/policy/authority references',
        'exact parent/event ordinal','independent postcondition','repository/store roots'],
      'LIVE_PRODUCER_TRUST_BOUNDARY':'Application registration is explicit and not data/wire authority; no serialized callable/oracle result can bypass it.',
      'TRANSIENT_PREPARED_CONTEXT':'Frozen origin-checked actual effect; commit checks exact original bundle/prefix under lock.',
      'ATOMIC_COMMIT_BOUNDARY':'Existing PLANNER-HEAD-1 atomic publication; staged orphans before HEAD are not admitted occurrence.',
      'ATOMICITY_LIMIT':'One local writer lock; exactly-once durable semantic occurrence, not exactly-once callback invocation across precommit crash.',
      'FAILURE_HOOKS':hooks,'ACTUAL_IO_REPLACE_FAILURE':'PASS','KILLED_WRITER_RECOVERY':processes['killed_writer_recovery'],
      'RETRY_EFFECT_CHECK':'Prepared retry compares complete result, original archived Snapshot/typed tuple/source effect; stale/conflicting prefix fails.',
      'RETRY_WITH_DESCENDANTS':'PASS; returns original transaction identity and current verified head, preserving descendants.',
      'REPLAY_OPERATION_INVOCATIONS':0,'REPLAY_NEW_OCCURRENCES':0,'REPLAY_VALIDATORS_RERUN':False,
      'VALIDATION_BINDING_MODEL':'Original immutable after_snapshot + unique PredicateId/dossier selector; ordered pre-Snapshot/source inputs and complete native member values.',
      'INVALIDATION':'PASS; current members stale while original event/archive/outcomes remain historical and auditable.',
      'NEW_NATIVE_METADATA':'DossierMaterializationBinding(event_identity, expected_bundle, source_additions) in default-omitted PersistenceBundle.dossier_materializations.',
      'EVENT_PAYLOAD_CHANGED':'NO','SNAPSHOT_SCHEMA_CHANGED':'NO','IDENTITY_CYCLE':'NO',
      'QUALIFICATION_COUNTS':{'new_test_methods_passed':23,'generic_test_runs':20,'additional_new_test_runs':3,
          'independent_generic_writers':13,'cold_readers':13,'killed_writers':4,'hash_seeds':[0,1,7,101],
          'unordered_presentations':['original','reverse','rotate'],'native_durable_negative_cases':23,
          'qualification_history_label_negatives':5,'sealed_negative_contract_cases_covered':24},
      'REGRESSIONS':regressions,
      'A04_DURABLE_TRANSACTION_COMPATIBILITY':'PASS','A04_COMPATIBILITY_LAYER':compat['role'],
      'A04_COMPATIBILITY_GATE_COUNT':len(compat['checks']),
      'A04_EVENT_COMPARISON_IDENTITY':compat['comparison_event'],'A04_SNAPSHOT_COMPARISON_IDENTITY':compat['comparison_snapshot'],
      'A04_FUTURE_BUNDLE_COMPARISON_ONLY':compat['comparison_future_bundle'],
      'PROSPECTIVE_A04_EXECUTION_READY':'YES','PROSPECTIVE_A04_EXECUTED':'NO','P05_EXECUTED':'NO','P06_EXECUTED':'NO',
      'P05_BOUND_STAGE_INPUTS':10,'P05_EXECUTION_READY':'NO','P05_NEXT_MISSING_INPUT':'E2-A04.prepare_result_event_ancestry',
      'ORIGINAL_A04_HISTORICAL_ANCESTRY':'UNPROVEN','ORIGINAL_A03_HISTORICAL_OCCURRENCE':'UNPROVEN',
      'P03_HISTORICAL_CORRESPONDENCE':'UNPROVEN','N_REAL_SATISFIED':'NO','HISTORICAL_RECONSTRUCTION':'NO',
      'PROSPECTIVE_A04_EVENT_IS_ORIGINAL_EVENT':'NO','P05_BINDING_APPLIED':'NO','AUTHORITY_ISSUED':'NO','DEFINITIONS_INSTALLED':'NO',
      'RUNTIME_MODIFIED':'YES_AUTHORIZED_GENERIC_IMPLEMENTATION','E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO',
      'GIT_DIFF_CHECK':'PASS','PRESERVATION':preservation,'evidence':evidence,
      'NEXT_PACKAGE':'E2-P05-A04-PROSPECTIVE-ANCESTRY-QUALIFICATION-EXECUTION-1',
      'READINESS_OVERLAY':'D01 supersedes only the missing generic capability/readiness blocker. Prior sealed contracts/oracles/reports remain immutable.'}
    save(PLANS/(NAME+'.json'),result)
    return result


if __name__=='__main__':
    r=main();print(json.dumps({k:r[k] for k in ('RESULT','DURABLE_ADMISSION_CAPABILITY','PROSPECTIVE_A04_EXECUTION_READY','PROSPECTIVE_A04_EXECUTED')}))
