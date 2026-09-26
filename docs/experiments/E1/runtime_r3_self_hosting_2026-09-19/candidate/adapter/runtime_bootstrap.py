"""One-shot transition from legacy selection to runtime-head authority.

This is a material bootstrap artifact, not an implementation continuation.
Its exact bytes and selected records require external Architect authorization.
Runtime journal writes are staged until the single bootstrap COMMITTED event.
No future runtime selection is performed by this module.
"""
import json
import os
import fcntl
import subprocess
from pathlib import Path
from contextlib import contextmanager
from . import runtime_adoption as runtime
from .controller_authority_store import encoded,sha

SELECTOR='controller:runtime-bootstrap'


def require(ok,message):
    if not ok:raise ValueError(message)


def verify_records(store):
    selector=json.loads(store.resolve(SELECTOR))
    require(set(selector)=={'record','Architect_authorization'},'bootstrap selector shape')
    record=runtime.read(store,selector['record']);runtime.unseal('RUNTIME-AUTHORITY-BOOTSTRAP',record)
    require(record['schema']=='RUNTIME-AUTHORITY-BOOTSTRAP-1','bootstrap schema')
    p=runtime.policy(store)
    require(record['runtime_head_authority']==p['id'] and record['lineage']==p['bootstrap_lineage'],'wrong runtime-head authority')
    require(record['material_amendment']==p['material_amendment'] and record['release_context']==p['release_context'],'wrong bootstrap amendment/ancestry')
    require(record['binding_kind']==p['binding_kind'],'qualification bootstrap cannot select production')
    require(record['legacy_runtime']==runtime.descriptor(store,p['genesis'])['identity'],'wrong legacy runtime')
    require(record['consumer_files']=={f.name:sha(f.read_bytes()) for f in Path(__file__).parent.glob('*.py')},'bootstrap implementation substitution')
    q=runtime.read(store,record['qualification'])
    require(q['result']=='PASS' and q['scope']=='BOUNDED_BOOTSTRAP' and q['consumer_files']==record['consumer_files'] and
            q['legacy_runtime']==record['legacy_runtime'] and q['first_continuation']==record['first_continuation'],'unqualified bootstrap')
    # Qualification is selected by the exact external grant, never sufficient alone.
    grant=runtime.read(store,selector['Architect_authorization'])
    body={'authority':'Architect','decision':'AUTHORIZE_ONE_TIME_RUNTIME_AUTHORITY_BOOTSTRAP',
          'record':selector['record'],'lineage':record['lineage'],'binding_kind':record['binding_kind']}
    require({k:v for k,v in grant.items() if k!='authority_source'}==body and
            runtime.read(store,grant['authority_source'])==dict(body,channel='user'),'missing/wrong Architect bootstrap authorization')
    runtime.transition(store,p,record['first_continuation'],record['first_adoption_authority'])
    return p,record,selector


@contextmanager
def guard(store,p,write=False):
    path=store.state_path(p['bootstrap_journal'])
    fd=os.open(path,(os.O_RDWR if write else os.O_RDONLY)|os.O_NOFOLLOW)
    try:
        fcntl.flock(fd,fcntl.LOCK_EX if write else fcntl.LOCK_SH)
        require((os.fstat(fd).st_dev,os.fstat(fd).st_ino)==(path.lstat().st_dev,path.lstat().st_ino),'bootstrap journal replaced')
        yield fd
    finally:os.close(fd)


def history(fd,record,selector):
    raw=runtime.data(fd);require(not raw or raw.endswith(b'\n'),'INDETERMINATE: torn bootstrap evidence')
    rows=[];last=None
    for n,line in enumerate(raw.splitlines()):
        row=json.loads(line);b=runtime.unseal('RUNTIME-BOOTSTRAP-EVENT',row)
        require(set(b)=={'schema','sequence','previous','event','record','authorization','lineage'} and
                b['schema']=='RUNTIME-BOOTSTRAP-EVENT-1' and b['sequence']==n and b['previous']==last and
                b['record']==selector['record'] and b['authorization']==selector['Architect_authorization'] and b['lineage']==record['lineage'],'INDETERMINATE: bootstrap evidence mismatch')
        allowed=('BOOTSTRAP_INTENT',) if n==0 else (('BOOTSTRAP_COMMITTED','BOOTSTRAP_ABORTED') if n==1 else ('BOOTSTRAP_RECORDED',))
        require(n<3 and b['event'] in allowed and (n!=2 or rows[1]['event']=='BOOTSTRAP_COMMITTED'),'INDETERMINATE: reordered/replayed bootstrap')
        rows.append(row);last=row['id']
    return rows


def append(fd,rows,event,record,selector):
    row=runtime.seal('RUNTIME-BOOTSTRAP-EVENT',{'schema':'RUNTIME-BOOTSTRAP-EVENT-1','sequence':len(rows),'previous':rows[-1]['id'] if rows else None,
          'event':event,'record':selector['record'],'authorization':selector['Architect_authorization'],'lineage':record['lineage']})
    b=encoded(row)+b'\n';os.lseek(fd,0,os.SEEK_END)
    while b:
        n=os.write(fd,b);require(n>0,'bootstrap write failed');b=b[n:]
    os.fsync(fd)


def legacy(store,p,record):
    runtime.descriptor(store,p['genesis'],live=True)
    pin=record['legacy_verifier'];require(set(pin)=={'python','python_sha256','path','sha256','input','expected'},'legacy verifier shape')
    for path,h in ((pin['python'],pin['python_sha256']),(pin['path'],pin['sha256'])):
        require(sha(Path(path).read_bytes())==h,'legacy verifier changed')
    request=runtime.read(store,pin['input'])
    result=subprocess.run([pin['python'],pin['path']],input=encoded(request),stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120,check=True)
    result=json.loads(result.stdout)
    require(result==pin['expected'] and result['runtime']==record['legacy_runtime'] and result['release_context']==record['release_context'],'legacy current authority reconstruction mismatch')
    return result


def fresh_supervisor(store, record):
    proof=record['supervisor']
    if proof is None:
        require(record['binding_kind']=='QUALIFICATION_BINDING','production supervisor evidence absent')
        return
    from .supervisor_observation import observe
    from .supervisor_succession import legacy_tuple
    from .activation_transaction import _host
    instance=runtime.read(store,proof['instance'])
    require(observe(instance)==instance,'supervisor instance changed')
    _host(legacy_tuple(instance),check_scopes=True)
    require(observe(instance)==instance and sha(Path(proof['succession_ledger']['path']).read_bytes())==proof['succession_ledger']['sha256'],'supervisor authority changed')


def establish(store, *, binding_kind='PRODUCTION_ADOPTION'):
    p,record,selector=verify_records(store)
    require(p['binding_kind']==binding_kind,'qualification cannot establish production')
    # Permanent lineage guard; ordinary transitions never acquire it exclusively.
    with guard(store,p,True) as fd:
        rows=history(fd,record,selector);require(not rows,'bootstrap lineage already consumed')
        legacy(store,p,record)
        fresh_supervisor(store,record)
        with runtime.locked(store,p,True) as ledger:
            state=runtime.reconstruct_locked(store,p,ledger)
            require(not state['events'] and state['current_runtime']==record['legacy_runtime'],'bootstrap predecessor already transitioned')
            c,b,a=runtime.transition(store,p,record['first_continuation'],record['first_adoption_authority'])
            require(a['identity']==record['successor_runtime'],'wrong successor implementation')
            append(fd,rows,'BOOTSTRAP_INTENT',record,selector);rows=history(fd,record,selector)
            for event in ('ADOPTION_INTENT','HEAD_COMMITTED','ADOPTION_RECORDED'):
                runtime.append(ledger,state,event,record['first_continuation'],record['first_adoption_authority'],b,a)
                state=runtime.reconstruct_locked(store,p,ledger)
            # Stage is durable but not current until this single authority commit.
            verify_records(store);runtime.descriptor(store,p['genesis'],live=True)
            fresh_supervisor(store,record)
            append(fd,rows,'BOOTSTRAP_COMMITTED',record,selector);rows=history(fd,record,selector)
            append(fd,rows,'BOOTSTRAP_RECORDED',record,selector)
    return reconstruct(store)


def require_established(store,p):
    checked,record,selector=verify_records(store);require(checked==p,'bootstrap policy changed')
    with guard(store,p) as fd:rows=history(fd,record,selector)
    require(len(rows)>=2 and rows[1]['event']=='BOOTSTRAP_COMMITTED','runtime-head authority not established')


def reconstruct(store):
    p,record,selector=verify_records(store)
    with guard(store,p) as fd:
        rows=history(fd,record,selector)
        committed=len(rows)>=2 and rows[1]['event']=='BOOTSTRAP_COMMITTED'
        if not committed:
            runtime.descriptor(store,p['genesis'],live=True)
            return {'state':'PREDECESSOR_CURRENT','runtime':record['legacy_runtime'],'bootstrap_consumed':bool(rows),'runtime_head_established':False}
        with runtime.locked(store,p) as ledger:s=runtime.reconstruct_locked(store,p,ledger)
        require(s['continuations'] and s['continuations'][0]==runtime.read(store,record['first_continuation'])['id'],'INDETERMINATE: committed bootstrap missing initial adoption')
        return {'state':'SUCCESSOR_CURRENT','runtime':s['current_runtime'],'runtime_head_authority':p['id'],'runtime_head_established':True,'head_event':s['head_event'],'runtime_ancestry':s['continuations'],'bootstrap_consumed':True}


def recover(store):
    p,record,selector=verify_records(store)
    with guard(store,p,True) as fd:
        rows=history(fd,record,selector)
        if len(rows)==1:append(fd,rows,'BOOTSTRAP_ABORTED',record,selector)
        elif len(rows)==2 and rows[1]['event']=='BOOTSTRAP_COMMITTED':append(fd,rows,'BOOTSTRAP_RECORDED',record,selector)
    return reconstruct(store)
