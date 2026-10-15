"""Read-only contract discrimination. Does not implement an END binding."""
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
DOCS=ROOT/'docs/plans'
P='DETERMINISTIC_PLANNER_V0_1_'

def read(p):return json.loads(Path(p).read_bytes())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def ref(p):return dict(path=str(Path(p).relative_to(ROOT)),pointer='',raw_sha256=sha(p))
def save(n,x):(OUT/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
def require(v,msg):
    if not v:raise ValueError(msg)
def verify(p):
    require(sha(ROOT/p['path'])==p['raw_sha256'],'PIN:'+p['path'])
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()

def source_audit():
    closure=read(DOCS/(P+'E2_P05_END_INTERFACE_CLOSURE_1.json'))
    inventory=read(DOCS/'qualification/E2_P05_END_INTERFACE_CLOSURE_1/six-interface-inventory.json')
    c=inventory['interfaces'][4]
    require(c['INTERFACE_ID']=='E2-END#/dependencies/4' and c['ORDINAL']==5,'INTERFACE')
    for p in c['PROVENANCE']+[c['CONSUMER_DECLARATION']]:verify(p)
    definition=read(ROOT/c['PROVENANCE'][0]['path'])
    require(definition['case_id']=='E2-D01','RUNNER_DEFINITION')
    capability=read(DOCS/(P+'DURABLE_ADMISSION_D01_RESULT.json'))
    require(capability['WORK_PACKAGE']=='DURABLE-ADMISSION-D01','DURABLE_QUALIFICATION')
    require(capability['RESULT']==capability['DURABLE_ADMISSION_CAPABILITY']=='PASS','CAPABILITY_PASS')
    gates=['result_application','post_snapshot','validation_binding','event_construction','ledger_append','bundle_construction','atomicity','idempotence','cold_restore','historical_replay','identity_ordering','negatives','failure_injection','determinism']
    require(set(capability['CAPABILITY_GATES'])==set(gates),'EXACT_CAPABILITY_GATES')
    for g in gates:require(capability['CAPABILITY_GATES'][g]=='PASS','CAPABILITY_TERM:'+g)
    for p in capability['evidence'].values():verify(p)
    runtime=[]
    for p in capability['PRESERVATION']['runtime_files']:
        runtime.append(dict(p,actual_raw_sha256=sha(ROOT/p['path']),classification='UNCHANGED' if sha(ROOT/p['path'])==p['raw_sha256'] else 'STALE'))
        require(runtime[-1]['classification']=='UNCHANGED','RUNTIME_STALE')
        ast.parse((ROOT/p['path']).read_text())
    a04=read(DOCS/(P+'E2_P05_A04_PROSPECTIVE_ANCESTRY_RESULT_1.json'))
    for p in a04['evidence'].values():verify(p)
    verify(a04['POST_A04_BUNDLE'])
    driver=DOCS/'qualification/E2_P05_A04_PROSPECTIVE_ANCESTRY_EXECUTION_1/execution_driver.py'
    require('dt.execute(before,bid,operation' in driver.read_text(),'A04_D01_USE_CALL')
    bundle=read(ROOT/a04['POST_A04_BUNDLE']['path'])['bundle']
    events=bundle['events'];e=events[-1]
    require(e['identity']['namespace']+':'+e['identity']['sha256']==a04['A04_EVENT_ID'],'A04_EVENT')
    require(e['after_snapshot']['namespace']+':'+e['after_snapshot']['sha256']==a04['POST_A04_SNAPSHOT_ID'],'A04_SNAPSHOT_BINDING')
    require(e['parent_event']==events[-2]['identity'],'A04_PARENT')
    bindings=bundle['dossier_materializations']
    require(any(b['event_identity']==e['identity'] for b in bindings),'A04_NATIVE_D01_BINDING')
    pins=[ref(DOCS/(P+n)) for n in ['E2_P05_END_INTERFACE_CLOSURE_1.md','E2_P05_END_INTERFACE_CLOSURE_1.json','E2_PC04_D01.json','DURABLE_ADMISSION_D01_RESULT.md','DURABLE_ADMISSION_D01_RESULT.json','E2_P05_A04_PROSPECTIVE_ANCESTRY_RESULT_1.json','CANONICAL_QUALIFICATION_EXPERIMENT_1.md','CANONICAL_QUALIFICATION_EXPERIMENT_1.json','CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md','E2_P05_READINESS.json']]
    return dict(recovered_contract=c,deterministic_runner_definition=definition,
        durable_capability=dict(identity=ref(DOCS/(P+'DURABLE_ADMISSION_D01_RESULT.json')),WORK_PACKAGE=capability['WORK_PACKAGE'],status='PASS',gates=capability['CAPABILITY_GATES'],runtime=runtime,qualified_evidence_pins=capability['evidence'],validation_binding=capability['VALIDATION_BINDING_MODEL'],atomicity_limit=capability['ATOMICITY_LIMIT'],atomic_commit=capability['ATOMIC_COMMIT_BOUNDARY'],identity_ordering='ValidationInstance.inputs ordered; Snapshot.validation_instances unordered; causal event chronology ordered',replay= dict(operation_invocations=capability['REPLAY_OPERATION_INVOCATIONS'],new_occurrences=capability['REPLAY_NEW_OCCURRENCES'],validators_rerun=capability['REPLAY_VALIDATORS_RERUN']),failure_hooks=capability['FAILURE_HOOKS']),
        A04_support_only=dict(identity=ref(DOCS/(P+'E2_P05_A04_PROSPECTIVE_ANCESTRY_RESULT_1.json')),driver=ref(driver),native_bundle=a04['POST_A04_BUNDLE'],actual_execution=a04['PROSPECTIVE_A04_EXECUTION'],bundle=a04['POST_A04_BUNDLE_ID'],Snapshot=a04['POST_A04_SNAPSHOT_ID'],event=a04['A04_EVENT_ID'],ordered_ancestry=[v['identity'] for v in events],native_dossier_bindings=bindings,persistence=a04['PERSISTENCE'],cold_restore=a04['COLD_RESTORE'],historical_replay=a04['HISTORICAL_REPLAY'],live_operation_replay_calls=a04['REPLAY_LIVE_OPERATION_INVOCATIONS'],validated_in_this_package='Artifact hash, embedded event/parent/after-Snapshot and native binding inspected; fresh restore not run because no END exercised-use requirement was established'),
        authoritative_pins=pins,
        distinction=dict(sealed_case='E2-D01',sealed_role='Ordering/hash/process determinism',supplied_capability='DURABLE-ADMISSION-D01',supplied_role='Durable dossier-result admission transaction',alias_mapping_in_recovered_contract=False,complete_END_runner_matrix_selected=False))

def reader(form):
    x=source_audit()
    # Documentary map/key order may vary; ordered event arrays never permuted.
    if form=='reversed':x=dict(reversed(list(x.items())))
    elif form=='rotated':
        items=list(x.items());x=dict(items[1:]+items[:1])
    return dict(pid=os.getpid(),seed=os.environ.get('PYTHONHASHSEED'),presentation=form,
        diagnostic_identity='qualification-D01-contract-discrimination-v1:'+hashlib.sha256(canonical(x)).hexdigest(),END_projection_materialized=False)

def main():
    x=source_audit();save('contract-and-source-audit.json',x)
    negatives=[]
    def reject(n,value):
        try:require(value,'SOURCE_ROLE_MISMATCH')
        except ValueError as e:negatives.append(dict(case=n,status='REJECTED',reason=str(e)))
        else:raise AssertionError('BAD_DIAGNOSTIC_NEGATIVE')
    reject('Durable admission qualification substituted for E2-D01 runner',x['durable_capability']['WORK_PACKAGE']==x['deterministic_runner_definition']['case_id'])
    reject('A04 local exercised use substituted for complete END runner matrix',x['distinction']['complete_END_runner_matrix_selected'])
    reject('Local capability PASS promoted to sealed END interface PASS',x['distinction']['alias_mapping_in_recovered_contract'])
    save('diagnostic-negatives.json',dict(status='PASS_DIAGNOSTIC_ONLY',cases=negatives,complete_binding_negative_suite='NOT_RUN_NO_BINDING'))
    rows=[]
    for seed in [0,1,7,101]:
        for form in ['original','reversed','rotated']:
            result=subprocess.run([sys.executable,str(OUT/'audit.py'),'reader',form],cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH='.',PYTHONHASHSEED=str(seed)),text=True,capture_output=True)
            require(result.returncode==0,result.stderr);rows.append(json.loads(result.stdout))
    require(len({r['diagnostic_identity'] for r in rows})==1,'DIAGNOSTIC_DETERMINISM')
    save('diagnostic-determinism.json',dict(status='PASS_DIAGNOSTIC_ONLY',readers=rows,complete_END_projection_manifest_determinism='NOT_RUN_NO_BINDING'))
    prior=[]
    for n,key in [('PC01','PC01_END_INTERFACE'),('PC02','PC02_END_INTERFACE'),('PC03','PC03_END_INTERFACE'),('T01','T01_END_INTERFACE')]:
        p=DOCS/(P+'E2_P05_'+n+'_END_BINDING_1.json');report=read(p);require(report[key]=='PASS','PRIOR_INTERFACE:'+n)
        for pin in report['evidence'].values():verify(pin)
        prior.append(dict(interface=n,status='PASS',report=ref(p)))
    prior += [dict(interface='E2-D01 deterministic runner interface',status='FAIL_NOT_BOUND'),dict(interface='post-reentry continuation contract',status='FAIL_NOT_BOUND')]
    save('six-interface-frontier.json',dict(interfaces=prior,END_INTERFACES_BOUND=4,END_INTERFACE_COUNT=6,next_unresolved='E2-D01 deterministic runner interface -> E2-END',final_sole_unresolved_interface=None,remaining_interfaces=2,continuation_classification='SAME_PROJECTION_PATTERN'))
    baseline=read(OUT/'preservation-baseline.json')
    changed=[p for p,h in baseline.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h];require(not changed,'PRESERVATION')
    result=subprocess.run(['git','diff','--check'],cwd=ROOT,text=True,capture_output=True);require(result.returncode==0,result.stdout+result.stderr)
    save('preservation.json',dict(preexisting_files_checked=len(baseline),changed_preexisting_files=changed,E1_files_checked=sum(p.startswith('docs/experiments/E1/') for p in baseline),NATIVE_STATE_CHANGED='NO',E1_ARTIFACTS_MODIFIED=0,INSTALL_EVENTS=0,NEW_AUTHORITIES=0,P05_EXECUTED='NO',P06_EXECUTED='NO',PRODUCTION_EFFECT='NO',N_REAL_SATISFIED='NO',GIT_DIFF_CHECK='PASS'))
    print('CONTRACT_SOURCE_MISMATCH_CONFIRMED; FRONTIER_UNCHANGED=4/6')
if __name__=='__main__':
    if len(sys.argv)>1:print(json.dumps(reader(sys.argv[2]),sort_keys=True))
    else:main()
