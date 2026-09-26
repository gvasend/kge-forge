"""Isolated qualification of ordinary enrollment/adoption composition.

This candidate is deliberately restricted to QUALIFICATION_BINDING. It does not
replace production's selected consumer. An externally selected synthetic material
integration decision is required, separately from enrollment and adoption.
The sidecar records an authenticated extension of the unchanged base runtime head.
"""
import json
import os
from pathlib import Path
from adapter import runtime_adoption as r
from adapter.controller_authority_store import encoded, sha
import continuation_enrollment as en

SELECTOR = 'controller:ordinary-enrolled-adoption'


def policy(store, base):
    p = json.loads(store.resolve(SELECTOR)); r.unseal('ORDINARY-ADOPTION-INTEGRATION', p)
    r.require(p['schema'] == 'ORDINARY-ADOPTION-INTEGRATION-1' and
              p['binding_kind'] == 'QUALIFICATION_BINDING', 'qualification-only integration')
    r.require(store.applicability.get('ordinary_integration') == p['id'], 'unselected integration')
    d = en.delegation(store)
    r.require(d['binding_kind'] == p['binding_kind'] and d['id'] == p['delegation'] and
              d['lineage'] == p['lineage'], 'integration delegation mismatch')
    r.require(p['implementation_sha256'] == sha(Path(__file__).read_bytes()), 'integration implementation changed')
    grant = en.trusted(store, 'integration-decision', p['authority'])
    r.require(grant == {'authority':'Architect','decision':'QUALIFY_ORDINARY_ENROLLED_ADOPTION',
                        'lineage':p['lineage'],'delegation':p['delegation'],
                        'implementation_sha256':p['implementation_sha256'],
                        'binding_kind':'QUALIFICATION_BINDING'}, 'integration authority mismatch')
    b = r.policy(base); s = r.reconstruct(base)
    r.require(b['id'] == p['lineage'] and s['pending'] is None and
              s['current_runtime'] == p['anchor_runtime'] and s['head_event'] == p['anchor_head'],
              'base ancestry changed')
    return p, d, s


def transition(store, d, candidate, enrollment, adoption):
    with en.lock(store, d, False) as fd:
        rows = en.history(store, d, fd)
    matches = [row for row in rows if row['id'] == enrollment and row['candidate'] == candidate]
    r.require(len(matches) == 1, 'missing exact enrollment')
    row = matches[0]
    c,b,a,_ = en.validate(store,d,row['candidate'],row['qualification'],row['decision'])
    g = en.trusted(store,'runtime-adoption-decision',adoption)
    r.unseal('ENROLLED-RUNTIME-ADOPTION-DECISION',g)
    r.require(g == r.seal('ENROLLED-RUNTIME-ADOPTION-DECISION', {
        'schema':'ENROLLED-RUNTIME-ADOPTION-DECISION-1','authority':'Architect',
        'decision':'ADOPT_EXACT_ENROLLED_CONTINUATION','binding_kind':'QUALIFICATION_BINDING',
        'lineage':d['lineage'],'delegation':d['id'],'candidate':candidate,'enrollment':enrollment,
        'qualification':row['qualification'],'predecessor':b['identity'],'successor':a['identity'],
        'head_event':row['head_event']}), 'wrong adoption authority or bindings')
    return c,b,a,row


def reconstruct_locked(store,p,d,anchor,fd):
    raw=r.data(fd);r.require(not raw or raw.endswith(b'\n'),'INDETERMINATE torn adoption')
    state={'runtime':anchor['current_runtime'],'descriptor':anchor['current_descriptor'],
           'head':anchor['head_event'],'pending':None,'events':[],'used':[], 'ancestry':list(anchor['continuations'])}
    for line in raw.splitlines():
        row=json.loads(line);r.unseal('ENROLLED-RUNTIME-EVENT',row)
        r.require(set(row)=={'id','schema','sequence','previous','integration','event','candidate','enrollment','adoption'},'adoption event shape')
        r.require(row['schema']=='ENROLLED-RUNTIME-EVENT-1' and row['sequence']==len(state['events']) and
                  row['previous']==state['head'] and row['integration']==p['id'],'adoption event ancestry')
        c,b,a,enrollment=transition(store,d,row['candidate'],row['enrollment'],row['adoption'])
        subject={k:row[k] for k in ('candidate','enrollment','adoption')}
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
    # R1 descriptors live in the unchanged anchor store; successors in extension.
    if state['events'] and state['runtime'] != anchor['current_runtime']:
        r.descriptor(store,state['descriptor'],live=True)
    return state


def append(fd,p,s,event,subject):
    row=r.seal('ENROLLED-RUNTIME-EVENT',dict(schema='ENROLLED-RUNTIME-EVENT-1',
        sequence=len(s['events']),previous=s['head'],integration=p['id'],event=event,**subject))
    blob=encoded(row)+b'\n';os.lseek(fd,0,os.SEEK_END)
    while blob:
        n=os.write(fd,blob);r.require(n>0,'adoption write failed');blob=blob[n:]
    os.fsync(fd)


def reconstruct(store,base):
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
    d=r.descriptor(store if s['events'] and s['runtime'] != r.reconstruct(base)['current_runtime'] else base,
                   s['descriptor'],live=True)
    r.require(Path(root).resolve()==Path(d['root']).resolve(),'unaccounted runtime')
    return s
