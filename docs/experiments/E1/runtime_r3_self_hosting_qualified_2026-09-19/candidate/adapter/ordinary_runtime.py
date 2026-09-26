"""Authenticated ordinary evolution extending an immutable consumed-bootstrap head.

The externally selected integration decision, enrollment and adoption remain
separate authorities. Historical bootstrap verification is read-only. No bootstrap
operation can be invoked through this module. Actual execution is content-bound.
"""
import json
import os
import sys
import importlib.util
from pathlib import Path
from adapter import runtime_adoption as r
from adapter.controller_authority_store import encoded, sha
from . import continuation_enrollment as en

SELECTOR = 'controller:ordinary-enrolled-adoption'
_anchor_cache = {}


def anchor(store,p):
    """Verify the immutable R1 prefix with its original exact consumer.

    Reuse only when *all* captured immutable inputs remain byte-identical.
    Extension journal/head, current runtime, eligibility and adoption are never
    cached. The archive is execution provenance, not a new runtime selection.
    """
    spec=p['anchor_verifier']
    for path,digest in spec['dependencies'].items():
        r.require(sha(Path(path).read_bytes())==digest,'historical anchor dependency changed')
    root=Path(spec['root']);inventory={f.name:sha(f.read_bytes()) for f in (root/'adapter').glob('*.py')}
    r.require(inventory==spec['files'],'historical verifier implementation changed')
    key=sha(encoded(spec))
    if key not in _anchor_cache:
        name='_forge_frozen_runtime_'+key
        package_spec=importlib.util.spec_from_file_location(name,root/'adapter/__init__.py',submodule_search_locations=[str(root/'adapter')])
        package=importlib.util.module_from_spec(package_spec);sys.modules[name]=package;package_spec.loader.exec_module(package)
        from importlib import import_module
        old=import_module(name+'.runtime_adoption');stores=import_module(name+'.controller_authority_store')
        base=stores.ControllerAuthorityStore(**spec['store'])
        try:
            state=old.reconstruct(base)
            r.require(state['current_runtime']==p['anchor_runtime'] and state['head_event']==p['anchor_head'] and state['pending'] is None,'wrong R1 anchor')
            # Dependency closure includes every immutable object, catalog, both
            # typed journals and all live historical runtime inventory bytes.
            required={str(base.root/'catalog.json')}
            required.update(str(base.root/x['sha256']) for x in base.catalog['objects'].values())
            oldp=old.policy(base)
            predecessor=dict(oldp['release_context']);release=predecessor.pop('release_authority')
            runtime_binding={'runtime_head_authority':oldp['id'],'runtime':state['current_runtime'],'head_event':state['head_event']}
            released,context=old.production_identities(base,release,predecessor,runtime_binding)
            state['runtime_authority_context']=dict(context,release_authority=released)
            required.update(str(base.state_path(oldp[k])) for k in ('journal','bootstrap_journal'))
            descriptors=[old.descriptor(base,oldp['genesis'])]
            for pair in oldp['adoptions']:
                c=old.read(base,pair['continuation'])
                descriptors += [old.descriptor(base,c['predecessor']),old.descriptor(base,c['successor'])]
            required.update(str(Path(d['root'])/'adapter'/n) for d in descriptors for n in d['files'])
            r.require(required<=set(spec['dependencies']),'incomplete anchor witness')
            _anchor_cache[key]=encoded(state)
        finally:base.close()
    state=json.loads(_anchor_cache[key])
    r.require(state['current_runtime']==p['anchor_runtime'] and state['head_event']==p['anchor_head'],'anchor substitution')
    return state


def policy(store, base=None):
    p = json.loads(store.resolve(SELECTOR)); r.unseal('ORDINARY-ADOPTION-INTEGRATION', p)
    r.require(p['schema'] == 'ORDINARY-ADOPTION-INTEGRATION-1' and
              p['binding_kind'] in ('QUALIFICATION_BINDING','PRODUCTION_ENROLLMENT'), 'ordinary integration binding kind')
    r.require(store.applicability.get('ordinary_integration') == p['id'], 'unselected integration')
    d = en.delegation(store)
    r.require(d['binding_kind'] == p['binding_kind'] and d['id'] == p['delegation'] and
              d['lineage'] == p['lineage'], 'integration delegation mismatch')
    r.require(p['implementation_sha256'] == sha(Path(__file__).read_bytes()), 'integration implementation changed')
    grant = en.trusted(store, 'integration-decision', p['authority'])
    decision='QUALIFY_ORDINARY_ENROLLED_ADOPTION' if p['binding_kind']=='QUALIFICATION_BINDING' else 'ADOPT_ORDINARY_ENROLLED_ADOPTION_CONSUMER'
    r.require(grant == {'authority':'Architect','decision':decision,
                        'lineage':p['lineage'],'delegation':p['delegation'],
                        'implementation_sha256':p['implementation_sha256'],
                        'binding_kind':p['binding_kind']}, 'integration authority mismatch')
    s = anchor(store,p); b = {'id':p['lineage']}
    r.require(b['id'] == p['lineage'] and s['pending'] is None and
              s['current_runtime'] == p['anchor_runtime'] and s['head_event'] == p['anchor_head'],
              'base ancestry changed')
    r.require(d['context']==s['runtime_authority_context'],'current runtime authority context mismatch')
    return p, d, s


def transition(store, d, candidate, enrollment, adoption):
    with en.lock(store, d, False) as fd:
        rows = en.history(store, d, fd)
    return _transition_from_verified_rows(store,d,candidate,enrollment,adoption,rows)


def _transition_from_verified_rows(store,d,candidate,enrollment,adoption,rows):
    matches = [row for row in rows if row['id'] == enrollment and row['candidate'] == candidate]
    r.require(len(matches) == 1, 'missing exact enrollment')
    row = matches[0]
    c,b,a,_ = en.validate(store,d,row['candidate'],row['qualification'],row['decision'])
    g = en.trusted(store,'runtime-adoption-decision',adoption)
    r.unseal('ENROLLED-RUNTIME-ADOPTION-DECISION',g)
    r.require(g == r.seal('ENROLLED-RUNTIME-ADOPTION-DECISION', {
        'schema':'ENROLLED-RUNTIME-ADOPTION-DECISION-1','authority':'Architect',
        'decision':'ADOPT_EXACT_ENROLLED_CONTINUATION','binding_kind':d['binding_kind'],
        'lineage':d['lineage'],'delegation':d['id'],'candidate':candidate,'enrollment':enrollment,
        'qualification':row['qualification'],'predecessor':b['identity'],'successor':a['identity'],
        'head_event':row['head_event']}), 'wrong adoption authority or bindings')
    return c,b,a,row


def reconstruct_locked(store,p,d,anchor,fd):
    raw=r.data(fd);r.require(not raw or raw.endswith(b'\n'),'INDETERMINATE torn adoption')
    state={'runtime':anchor['current_runtime'],'descriptor':anchor['current_descriptor'],
           'head':anchor['head_event'],'pending':None,'events':[],'used':[], 'ancestry':list(anchor['continuations'])}
    with en.lock(store,d,False) as enrollment_fd:
        verified_rows=en.history(store,d,enrollment_fd)
    verified_subjects={}
    for line in raw.splitlines():
        row=json.loads(line);r.unseal('ENROLLED-RUNTIME-EVENT',row)
        r.require(set(row)=={'id','schema','sequence','previous','integration','event','candidate','enrollment','adoption'},'adoption event shape')
        r.require(row['schema']=='ENROLLED-RUNTIME-EVENT-1' and row['sequence']==len(state['events']) and
                  row['previous']==state['head'] and row['integration']==p['id'],'adoption event ancestry')
        subject={k:row[k] for k in ('candidate','enrollment','adoption')}
        subject_key=encoded(subject)
        if subject_key not in verified_subjects:
            verified_subjects[subject_key]=_transition_from_verified_rows(store,d,row['candidate'],row['enrollment'],row['adoption'],verified_rows)
        c,b,a,enrollment=verified_subjects[subject_key]
        event=row['event']
        if event=='INTENT':
            r.require(state['pending'] is None and state['runtime']==b['identity'] and
                      enrollment['head_event']==state['head'] and c['id'] not in state['used'],
                      'stale, competing or replayed adoption')
            state['pending']=subject;state['used'].append(c['id'])
        elif event=='COMMITTED':
            r.require(state['pending']==subject and state['runtime']==b['identity'],'commit without exact intent')
            state['runtime']=a['identity'];state['descriptor']=c['successor'];state['ancestry'].append(c['id'])
        elif event=='RECORDED':
            r.require(state['pending']==subject and state['runtime']==a['identity'],'uncommitted terminal record')
            state['pending']=None
        elif event=='ABORTED':
            r.require(state['pending']==subject and state['runtime']==b['identity'],'cannot abort committed runtime')
            state['pending']=None
        else:raise ValueError('unknown adoption event')
        state['events'].append(row);state['head']=row['id']
    r.descriptor(store,state['descriptor'],live=True)
    return state


def append(fd,p,s,event,subject):
    row=r.seal('ENROLLED-RUNTIME-EVENT',dict(schema='ENROLLED-RUNTIME-EVENT-1',
        sequence=len(s['events']),previous=s['head'],integration=p['id'],event=event,**subject))
    blob=encoded(row)+b'\n';os.lseek(fd,0,os.SEEK_END)
    while blob:
        n=os.write(fd,blob);r.require(n>0,'adoption write failed');blob=blob[n:]
    os.fsync(fd)


def reconstruct(store,base=None):
    p,d,anchor=policy(store,base)
    with en.lock(store,p,False) as fd:return reconstruct_locked(store,p,d,anchor,fd)


def adopt(store,base,candidate,enrollment,adoption):
    p,d,anchor=policy(store,base)
    # Extension-head then enrollment lock ordering. No call to en.require_eligible
    # while owning a runtime lock: reconstruct the typed evidence in this txn.
    with en.lock(store,p,True) as fd:
        s=reconstruct_locked(store,p,d,anchor,fd)
        c,b,a,row=transition(store,d,candidate,enrollment,adoption)
        r.require(s['pending'] is None and s['runtime']==b['identity'] and
                  s['head']==row['head_event'] and c['id'] not in s['used'],'stale, competing or replayed adoption')
        subject={'candidate':candidate,'enrollment':enrollment,'adoption':adoption}
        for event in ('INTENT','COMMITTED','RECORDED'):
            policy(store,base);transition(store,d,candidate,enrollment,adoption)
            append(fd,p,s,event,subject);s=reconstruct_locked(store,p,d,anchor,fd)
        return s


def recover(store,base):
    p,d,anchor=policy(store,base)
    with en.lock(store,p,True) as fd:
        s=reconstruct_locked(store,p,d,anchor,fd)
        if s['pending']:
            x=s['pending'];c,b,a,row=transition(store,d,x['candidate'],x['enrollment'],x['adoption'])
            append(fd,p,s,'RECORDED' if s['runtime']==a['identity'] else 'ABORTED',x)
            s=reconstruct_locked(store,p,d,anchor,fd)
        return s


def verify_selected_bytes(store,base,root):
    s=reconstruct(store,base);r.require(s['pending'] is None,'unresolved adoption')
    d=r.descriptor(store,
                   s['descriptor'],live=True)
    r.require(Path(root).resolve()==Path(d['root']).resolve(),'unaccounted runtime')
    return s


def binding(store):
    p,d,anchor_state=policy(store)
    with en.lock(store,p,False) as fd:s=reconstruct_locked(store,p,d,anchor_state,fd)
    return {'runtime_head_authority':p['lineage'],'ordinary_integration':p['id'],
            'runtime':s['runtime'],'head_event':s['head']}


def validate_executing_runtime(store,expected):
    """No caller-supplied execution identity or root can establish self-hosting."""
    p,d,anchor_state=policy(store)
    with en.lock(store,p,False) as fd:
        state=reconstruct_locked(store,p,d,anchor_state,fd)
        actual={'runtime_head_authority':p['lineage'],'ordinary_integration':p['id'],
                'runtime':state['runtime'],'head_event':state['head']}
        r.require(actual==expected,'invocation runtime is not current adopted head')
        descriptor=r.read(store,state['descriptor'])
        r.require(Path(descriptor['root']).resolve()==Path(__file__).resolve().parent.parent,'unaccounted runtime')
        # reconstruct_locked freshly verified the complete selected live inventory
        # under this same head lock. No caller can supply this validated state.
        r.require(state['pending'] is None,'unresolved current runtime')
    return dict(actual,executing_root=str(Path(__file__).resolve().parent.parent))


def enroll(store,candidate,qualification,decision):
    p,d,anchor_state=policy(store)
    # Serialized current extension head precedes enrollment lock, avoiding nested
    # legacy sessions and holding predecessor freshness through fsync.
    with en.lock(store,p,False) as head_fd:
        s=reconstruct_locked(store,p,d,anchor_state,head_fd)
        r.require(s['pending'] is None,'pending adoption')
        with en.lock(store,d,True) as fd:
            return _enroll_locked(store,d,s,fd,candidate,qualification,decision)


def _enroll_locked(store,d,s,fd,candidate,qualification,decision):
        rows=en.history(store,d,fd);c,b,a,g=en.validate(store,d,candidate,qualification,decision)
        r.require(s['runtime']==b['identity'] and s['head']==g['head_event'],'stale enrollment')
        r.require(all(x['candidate']!=candidate and x['decision']!=decision for x in rows),'enrollment replay')
        row=r.seal('CONTINUATION-ENROLLMENT',{'schema':'CONTINUATION-ENROLLMENT-1',
            'sequence':len(rows),'previous':rows[-1]['id'] if rows else None,'delegation':d['id'],
            'candidate':candidate,'qualification':qualification,'decision':decision,
            'predecessor':b['identity'],'head_event':s['head']})
        blob=encoded(row)+b'\n';os.lseek(fd,0,os.SEEK_END)
        while blob:
            n=os.write(fd,blob);r.require(n>0,'enrollment append failure');blob=blob[n:]
        os.fsync(fd)
        return row


def eligible(store,candidate,enrollment):
    p,d,anchor_state=policy(store)
    with en.lock(store,p,False) as head_fd:
        s=reconstruct_locked(store,p,d,anchor_state,head_fd)
        with en.lock(store,d,False) as fd:rows=en.history(store,d,fd)
        matches=[x for x in rows if x['candidate']==candidate and x['id']==enrollment]
        r.require(len(matches)==1 and s['pending'] is None,'missing eligibility')
        row=matches[0]
        r.require(s['runtime']==row['predecessor'] and s['head']==row['head_event'],'stale eligibility')
        return row


def validate_production_binding(store,expected,historical_runtime):
    p,d,prefix=policy(store)
    r.require(p['binding_kind']=='PRODUCTION_ENROLLMENT','qualification cannot select production runtime')
    ids={prefix['current_runtime']}
    for event in prefix['events']:ids.update((event['predecessor'],event['successor']))
    r.require(historical_runtime in ids,'runtime selection does not extend released history')
    return validate_executing_runtime(store,expected)


def production_identities(store,release,ids,expected):
    p,d,_=policy(store)
    r.require(p['binding_kind']=='PRODUCTION_ENROLLMENT','qualification cannot bind production context')
    validate_executing_runtime(store,expected)
    r.require(p['legacy_release_context']==dict(ids,release_authority=release),'ordinary runtime context ancestry differs')
    new_release=r.identity('E1-RELEASE-AUTHORITY',{'predecessor':d['context']['release_authority'],'ordinary_runtime_integration':p['id']})
    out={k:v for k,v in d['context'].items() if k!='release_authority'}
    out['OperationalContextId']=r.identity('E1-OPERATIONAL-CONTEXT',{'predecessor':d['context']['OperationalContextId'],'ordinary_runtime':expected})
    out['continuation_chain_digest']=sha(encoded({'predecessor':d['context']['continuation_chain_digest'],'ordinary_runtime':expected}))
    return new_release,out
