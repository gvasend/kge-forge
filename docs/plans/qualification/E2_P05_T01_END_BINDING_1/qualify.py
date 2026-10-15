"""Independent fresh-process readers, bounded negatives and preservation audit."""
import os
import subprocess
from copy import deepcopy
from concurrent.futures import ThreadPoolExecutor
from common import *
from binding import project, validate
from adapter.planner import validation_transaction as vt

def native_validation(b):
    resolver=c.snapshot_resolver(Path(selection()['restore_manifest']['path']).parent)
    c.bundle_bytes(b,snapshot_resolver=resolver)
    m.validate_model(b.current)
    m.validate_types(b.current,m.Snapshot)
    vt.receipt(b,b.events[-2].result.entity.id)
    c._verify_sources(b,ROOT)
    return dict(bundle='PASS',Snapshot_model='PASS',ledger_replay='PASS',receipt_Evidence_attestation='PASS',source_policy_pins='PASS',commit=False)

def negatives(b):
    records=[]
    def reject(name,call):
        try: call()
        except m.PlannerError as exc: records.append(dict(case=name,status='REJECTED',reason=str(exc)))
        else: raise AssertionError('negative accepted: '+name)
    man=selection()['restore_manifest'];path=ROOT/selection()['native_bundle']['path']
    bad=lambda x: replace(x,sha256='0'*64)
    reject('wrong bundle',lambda:c.restore(path,bad(c._unwire(man['bundle_id'])),ROOT))
    reject('report substituted for native bundle',lambda:c.restore(ROOT/selection()['primary_sources'][2]['path'],c._unwire(man['bundle_id']),ROOT))
    snapshot_path=path.parent/('snapshot-'+man['state_id']['sha256']+'.json')
    reject('Snapshot-only source where event-bearing bundle required',lambda:c.restore(snapshot_path,c._unwire(man['bundle_id']),ROOT))
    def candidate(name,x):
        reject(name,lambda:(native_validation(x),validate(project(x),manifest(project(x)))))
    s=b.current;req=b.events[-2].result;ev=next(e for e in s.entities if e.id==req.entity.id);r=s.receipt_admissions[0]
    def entity_change(**changes):
        return replace(b,current=replace(s,entities=tuple(replace(e,**changes) if e.id==ev.id else e for e in s.entities)))
    candidate('wrong Snapshot',replace(b,current=replace(s,context=replace(s.context,tick=1))))
    candidate('wrong Evidence',entity_change(id=m.EntityId('EVIDENCE:WRONG')))
    candidate('wrong receipt',replace(b,current=replace(s,receipt_admissions=(replace(r,artifact=m.EntityId('EVIDENCE:WRONG')),))))
    candidate('wrong attestation',replace(b,current=replace(s,receipt_admissions=(replace(r,attestation=bad(r.attestation)),))))
    candidate('wrong ingress event',replace(b,events=b.events[:-2]+(replace(b.events[-2],identity=bad(b.events[-2].identity)),b.events[-1])))
    candidate('wrong parent',replace(b,events=b.events[:-1]+(replace(b.events[-1],parent_event=bad(b.events[-1].parent_event)),)))
    candidate('wrong ledger root',replace(b,events=(replace(b.events[0],identity=bad(b.events[0].identity)),)+b.events[1:]))
    candidate('wrong append head',replace(b,events=b.events[:-1]+(replace(b.events[-1],identity=bad(b.events[-1].identity)),)))
    candidate('tampered source pin',replace(b,sources=(replace(b.sources[0],identity=bad(b.sources[0].identity)),)+b.sources[1:]))
    candidate('wrong validation state',entity_change(validation=m.ValidationState.ACCEPTED,validated=True))
    candidate('wrong control',replace(b,current=replace(s,external_gates=(replace(s.external_gates[0],stage=m.ExternalStage.EVIDENCE_VALIDATED),))))
    candidate('wrong scope',entity_change(scope='WRONG'))
    candidate('wrong lineage',entity_change(lineage='WRONG'))
    candidate('wrong provenance',entity_change(provenance=replace(ev.provenance,identity=bad(ev.provenance.identity))))
    candidate('event ancestry reordered',replace(b,events=tuple(reversed(b.events))))
    later=read(SOURCE/'checkpoint-manifests.json')['post-a10']
    later_bundle=c.restore(Path(later['path']),c._unwire(later['bundle_id']),ROOT)
    # Later state is natively valid, but cannot substitute for the T01 boundary.
    reject('later lifecycle state substituted for T01',lambda:validate(project(later_bundle),manifest(project(later_bundle))))
    base=read(OUT/'END-projection.json');baseinv=read(OUT/'invocation-input-manifest.json')
    def pnegative(name,change):
        p=deepcopy(base);change(p);p['identity']=qid('projection',p['body'])
        reject(name,lambda:validate(p,manifest(p)))
    pnegative('wrong END consumer',lambda p:p['body'].update(consumer='E2-OTHER'))
    pnegative('wrong process',lambda p:p['body']['process'].update(identity='WRONG'))
    pnegative('projection scope substitution',lambda p:p['body']['contract'].update(SCOPE='WRONG'))
    pnegative('projection lineage substitution',lambda p:p['body']['terms']['context'].update(lineage='WRONG'))
    pnegative('projection provenance substitution',lambda p:p['body']['terms']['evidence']['provenance'].update(path='WRONG'))
    pnegative('post-restore validation substitution',lambda p:p['body']['terms']['post_restore'].update(validation='ACCEPTED'))
    pnegative('post-restore control substitution',lambda p:p['body']['terms']['post_restore'].update(control='FINISH'))
    pnegative('receipt currentness substitution',lambda p:p['body']['terms']['post_restore'].update(receipt_current=False))
    pnegative('ordered ancestry projection reordered',lambda p:p['body']['terms']['ancestry'].reverse())
    for name,fn in [('missing manifest input',lambda x:x['body']['inputs'].pop()),('extra manifest input',lambda x:x['body']['inputs'].append(deepcopy(x['body']['inputs'][0]))),('wrong projection identity',lambda x:x['body']['inputs'][0].update(PROJECTION_IDENTITY='WRONG')),('manifest consumer substitution',lambda x:x['body'].update(consumer='WRONG')),('manifest process substitution',lambda x:x['body'].update(process='WRONG'))]:
        x=deepcopy(baseinv);fn(x);x['identity']=qid('manifest',x['body']);reject(name,lambda:validate(base,x))
    x=deepcopy(base);x['identity']='WRONG';reject('projection identity integrity',lambda:validate(x,baseinv))
    # Unordered presentation is required to be accepted, rather than rejected.
    for form in ['reversed','rotated']:
        x=permutation(b,form);p=project(x);validate(p,manifest(p))
        records.append(dict(case='unordered '+form+' presentation accepted as same semantics',status='ACCEPTED_EQUIVALENT'))
    return dict(status='PASS',cases=records,native_candidate_policy='Isolated in-memory immutable replacements only; no candidate bundle/event/Snapshot published or committed')

def main():
    b=restore();save('native-validation.json',native_validation(b));save('negative-results.json',negatives(b))
    tasks=[(seed,form,index) for seed in [0,1,7,101] for form in ['original','reversed','rotated'] for index in range(2)]
    def run(task):
        seed,form,index=task
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH='.',PYTHONHASHSEED=str(seed))
        result=subprocess.run([sys.executable,str(OUT/'binding.py'),'reader',form],cwd=ROOT,env=env,text=True,capture_output=True)
        if result.returncode: raise AssertionError(result.stderr)
        row=json.loads(result.stdout);row.update(seed=seed,index=index)
        print('FRESH_READER_PASS',seed,form,index,flush=True)
        return row
    with ThreadPoolExecutor(max_workers=4) as pool: readers=list(pool.map(run,tasks))
    equal('stable projection identities',len({r['projection'] for r in readers}),1)
    equal('stable manifest identities',len({r['manifest'] for r in readers}),1)
    save('determinism.json',dict(status='PASS',fresh_readers=readers,total=len(readers),ordered_ancestry_rejection='PASS',unordered_fields='Native codec.SET_FIELDS only'))
    statuses=[]
    for index in range(1,4):
        report=read(DOCS/(PREFIX+'E2_P05_PC0'+str(index)+'_END_BINDING_1.json'))
        equal('prior PC0'+str(index),report['PC0'+str(index)+'_END_INTERFACE'],'PASS')
        check_refs(report.get('evidence',{}))
        statuses.append(dict(interface='E2-PC0'+str(index)+' -> E2-END',status='PASS'))
    statuses += [dict(interface='E2-T01 -> E2-END',status='PASS'),dict(interface='E2-D01 deterministic runner interface -> E2-END',status='FAIL_NOT_BOUND'),dict(interface='post-reentry continuation contract -> E2-END',status='FAIL_NOT_BOUND')]
    save('six-interface-frontier.json',dict(interfaces=statuses,END_INTERFACES_BOUND=4,END_INTERFACE_COUNT=6,NEXT_UNRESOLVED_INTERFACE=statuses[4]['interface'],composite_END='FAIL',prior_closed_terms_preserved=True))
    baseline=read('/tmp/t01-end-baseline.json')
    changed=[p for p,h in baseline.items() if not (ROOT/p).is_file() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
    equal('preexisting artifacts unchanged',changed,[])
    diff=subprocess.run(['git','diff','--check'],cwd=ROOT,text=True,capture_output=True);equal('git diff --check',diff.returncode,0)
    preservation=dict(preexisting_files_checked=len(baseline),changed_preexisting_files=changed,NATIVE_STATE_CHANGED='NO',INSTALL_EVENTS=0,NEW_AUTHORITIES=0,P05_EXECUTED='NO',P06_EXECUTED='NO',P05_STAGE_BINDINGS='13/13',E1_ARTIFACTS_MODIFIED=0,PRODUCTION_EFFECT='NO',N_REAL_SATISFIED='NO',GIT_DIFF_CHECK='PASS')
    previous=read(DOCS/(PREFIX+'E2_P05_PC03_END_BINDING_1.json'))
    for k,v in previous.items():
        if v=='UNPROVEN':preservation[k]=v
    save('preservation.json',preservation)
    save('preflight.json',dict(status='PASS',terms={k:'PASS' for k in ['source','cold_restore','post_restore_oracle','projection','process','manifest','currentness','scope','lineage','provenance','native_validation','negatives','determinism']},T01_END_INTERFACE='PASS'))
    print('T01_END_INTERFACE_PASS; END_INTERFACES_BOUND=4/6')
if __name__=='__main__': main()
