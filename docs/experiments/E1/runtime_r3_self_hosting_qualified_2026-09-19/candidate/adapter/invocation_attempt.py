"""Specific, separately approved replacement attempts; never automatic retry.

Original dispatch stays immutable. A selected Architect approval pins one entire
child proposal. This module grants nothing from pre-effect failure alone.
"""
import json
import os
from pathlib import Path
from .context_projection import canonical,digest,sha
from .run_control import events
from .activation_transaction import _lease,invocation
from .invocation_ownership import InvocationOwnership
from .authorization_lifecycle import _append

BOUND = ('release_authority','material_amendment','current_supervisor','succession_head',
    'work_package_id','released_profile_sha256','ModelPayloadDigest',
    'OperationalContextId','FullContextDigest','ModelProjectionBindingDigest',
    'budget_policy_identity','transmission_retention_identity','implementation_identity')

def read(store,ref):
    if set(ref) != {'authority_id','sha256'}:
        raise ValueError('private logical reference required')
    b=store.resolve(ref['authority_id'])
    if sha(b)!=ref['sha256']:raise ValueError('private object substitution')
    return json.loads(b)

def authenticate(store,ref):
    p=read(store,ref)
    if p['schema']!='INVOCATION-ATTEMPT-BINDING-1':raise ValueError('unknown attempt schema')
    original=read(store,p['dispatch'])
    if p['DispatchAuthorizationId']!='E1-ARCHITECT-DISPATCH-sha256:'+p['dispatch']['sha256'] or \
            original['authority']!='Architect' or original['decision']!='DISPATCH_AUTHORIZED':
        raise ValueError('original dispatch substitution')
    if p['bindings']!={k:original[k] for k in BOUND}:raise ValueError('attempt changed released bindings')
    if p['predecessor']['authorization_id']!=original['invocation_identity']['authorization_id'] or \
            p['predecessor']['audit']!=original['all_authorized_bindings']['audit']:
        raise ValueError('predecessor substitution')
    new=p['invocation_identity'];old=original['invocation_identity']
    if set(new)!=set(old) or type(new['revision']) is not int or new['revision']<=old['revision'] or \
            any(not isinstance(new[k],str) or not new[k] or new[k]==old[k] for k in ('authorization_id','session_id','turn_id')):
        raise ValueError('new unique invocation required')
    if p['automatic_retry'] is not False or p['initial_state']!='INACTIVE' or p['ownership']!='NONE' or not p['reason']:
        raise ValueError('attempt cannot inherit authority state')
    if p['InvocationAttemptId']!='InvocationAttempt-sha256:'+digest({
            'dispatch':p['DispatchAuthorizationId'],'predecessor':p['predecessor'],
            'invocation_identity':new,'audit':p['audit']}):raise ValueError('attempt identity mismatch')
    if str(Path(p['audit']).resolve())!=p['audit'] or p['audit']==p['predecessor']['audit']:
        raise ValueError('closed audit path cannot be reused')
    selected=json.loads(store.resolve(p['DispatchAuthorizationId']+':replacement-approval'))
    expected={'authority':'Architect','decision':'AUTHORIZE_SPECIFIC_REPLACEMENT_INVOCATION',
              'proposal':ref,'DispatchAuthorizationId':p['DispatchAuthorizationId'],
              'InvocationAttemptId':p['InvocationAttemptId'],'automatic_retry':False}
    if {k:selected.get(k) for k in expected}!=expected:
        raise ValueError('specific Architect invocation authorization required')
    source=read(store,selected['authority_source'])
    if source!=dict(expected,channel='user'):raise ValueError('unattributed invocation authorization')
    return p,original,selected

def predecessor_no_effects(p):
    path=Path(p['predecessor']['audit']);b=path.read_bytes()
    if sha(b)!=p['predecessor']['audit_sha256']:raise ValueError('predecessor evidence changed')
    rows=events(path)
    allowed={'invocation_start','span_start','span_end','activity','budget_warning',
             'admission_closed','final_disposition'}
    if not rows or any(r.get('schema')!='E1-RUN-CONTROL-1' or r.get('event') not in allowed or
                      r['identity']['authorization_id']!=p['predecessor']['authorization_id'] for r in rows):
        raise ValueError('effecting, issued or uncertain predecessor is not replaceable here')
    if not any(r['event']=='admission_closed' for r in rows) or rows[-1]['event']!='final_disposition' or \
       rows[-1]['details'].get('disposition')!='BLOCKED_BEFORE_AUTHORIZATION_ISSUANCE' or \
       rows[-1]['details'].get('uncertainty') is not None:
        raise ValueError('predecessor closure not established')
    return sha(b)

def child_dispatch(store,ref):
    p,d,approval=authenticate(store,ref)
    child=dict(d)
    child.update(invocation_identity=p['invocation_identity'],authority_source=approval['authority_source'],
                 invocation_attempt=ref,parent_dispatch=p['dispatch'])
    child['all_authorized_bindings']=dict(d['all_authorized_bindings'],audit=p['audit'],
        operational_binding_sha256=p['replacement_operational_binding_sha256'])
    return child

def require_claim(store,ref):
    p,_,_=authenticate(store,ref)
    predecessor_no_effects(p)
    data=store.state_path(p['DispatchAuthorizationId']+':attempt-ledger').read_bytes()
    if data and not data.endswith(b'\n'):raise ValueError('uncertain attempt ledger')
    matched=[];prefix=b''
    for line in data.splitlines(keepends=True):
        row=json.loads(line);body={k:v for k,v in row.items() if k!='id'}
        if row['id']!='INVOCATION-ATTEMPT-ALLOCATION-sha256:'+digest(body) or row['ledger_prefix_sha256']!=sha(prefix):
            raise ValueError('attempt allocation history mismatch')
        prefix+=line
        if row['predecessor']==p['predecessor']:
            matched.append(row)
    if len(matched)!=1 or matched[0]['proposal']!=ref or matched[0]['InvocationAttemptId']!=p['InvocationAttemptId']:
        raise ValueError('unique selected attempt allocation required')
    return matched[0]

def claim(store,ref,ledger_id):
    """One durable child allocation per failed predecessor under controller fence.

    Does not issue, activate, acquire invocation ownership, or authorize a model.
    A crash after allocation requires reconciliation, never automatic replay.
    """
    p,d,_=authenticate(store,ref);ownership=Path(d['all_authorized_bindings']['ownership_ledger'])
    # Both locations are selected private state, never a caller filesystem grant.
    if store.state_path(p['DispatchAuthorizationId']+':attempt-ledger')!=store.state_path(ledger_id):
        raise ValueError('unselected attempt ledger')
    gate=_lease(ownership);fd=of=None
    try:
        owner=InvocationOwnership(ownership);of=owner._locked()
        if invocation(of) is not None or owner._history(of) is not None:raise ValueError('ownership conflict')
        predecessor_no_effects(p)
        if os.path.lexists(p['audit']):raise ValueError('new attempt audit already exists')
        path=store.state_path(ledger_id)
        fd=os.open(path,os.O_RDWR|os.O_APPEND|os.O_NOFOLLOW)
        data=path.read_bytes()
        if data and not data.endswith(b'\n'):raise ValueError('uncertain attempt ledger')
        prefix=b''
        for line in data.splitlines(keepends=True):
            row=json.loads(line);body={k:v for k,v in row.items() if k!='id'}
            if row['id']!='INVOCATION-ATTEMPT-ALLOCATION-sha256:'+digest(body) or row['ledger_prefix_sha256']!=sha(prefix):raise ValueError('attempt ledger corrupt')
            prefix+=line
            if row['predecessor']==p['predecessor'] or row['InvocationAttemptId']==p['InvocationAttemptId'] or \
                    row['authorization_id']==p['invocation_identity']['authorization_id']:
                raise ValueError('replay or competing successor attempt')
        row={'schema':'INVOCATION-ATTEMPT-ALLOCATION-1','proposal':ref,'DispatchAuthorizationId':p['DispatchAuthorizationId'],
             'InvocationAttemptId':p['InvocationAttemptId'],'authorization_id':p['invocation_identity']['authorization_id'],
             'predecessor':p['predecessor'],'ledger_prefix_sha256':sha(data),'state':'ALLOCATED_NOT_ISSUED'}
        row['id']='INVOCATION-ATTEMPT-ALLOCATION-sha256:'+digest(row);_append(fd,row)
        return row
    finally:
        if fd is not None:os.close(fd)
        if of is not None:os.close(of)
        os.close(gate)
