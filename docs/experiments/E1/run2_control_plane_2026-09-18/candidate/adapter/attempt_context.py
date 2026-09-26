"""Versioned material attempt authority. PREPARED never permits real effects.

The frozen predecessor is verified by its exact original controller in a bounded
read-only process. Current controller code runs privately; S3's code stays intact.
"""
import json,os,subprocess
from pathlib import Path
from .context_projection import canonical,digest,sha,read_exact
from .controller_authority_store import current,ControllerAuthorityStore,read_authority_ref,outside
from .continuation_envelope import seal,BODY_KEYS
from .invocation_attempt import predecessor_no_effects,BOUND

RULES=('same_dispatch','permanently_closed','not_completed','no_ACTIVE','no_ownership',
 'no_active_execution','no_unresolved_persistent_effect','outcome_established',
 'exact_released_bindings','new_identity_unused_audit','specific_Architect_authorization',
 'no_inherited_state_effects_counters_or_namespace','no_automatic_retry')
REASON='PRE_ISSUANCE_ORCHESTRATION_FAILURE_NO_EFFECTS'

def require(value,message):
    if not value:raise ValueError(message)
def read(ref):return json.loads(read_authority_ref(ref))
def ident(kind,body):return kind+'-sha256:'+digest(body)
def unseal(obj,kind):
    body={k:v for k,v in obj.items() if k!='id'}
    require(obj.get('id')==ident(kind,body),'authority record fingerprint mismatch')
    return body

def selected(store=None):
    store=store or current();require(store is not None,'private attempt authority required')
    s=json.loads(store.resolve(store.applicability['authorization_id']+':attempt-context'))
    require(set(s)=={'mode','amendment','continuation','specific_invocation_authorization','qualification'},'attempt selection shape')
    require(s['mode'] in ('PREPARED','ISSUED'),'unknown attempt selection mode')
    return s

def decision(spec):
    store=current();s=selected(store)
    require(s['amendment']==spec['amendment'] and s['continuation']==spec['continuation'],'unselected attempt authority')
    amendment=read(spec['amendment']);a=unseal(amendment,'E1-RUN2-ATTEMPT-AUTHORITY-AMENDMENT')
    require(a['schema']=='E1-RUN2-ATTEMPT-AUTHORITY-1' and a['rules']==list(RULES) and a['reason_code']==REASON,'attempt authority rule mismatch')
    source=read(a['authority_source'])
    require(source=={'authority':'Architect','channel':'user','decision':'AUTHORIZE_RUN2_ATTEMPT_AUTHORITY',
        'predecessor_release_authority':a['predecessor_release_authority'],'parent_dispatch':a['parent_dispatch'],
        'accepted_candidate':a['proposal'],'rules':list(RULES),'reason_code':REASON,'issuance_authorized':False},'material decision attribution mismatch')
    p=read(a['proposal']);require(p['invocation_identity']['authorization_id']==store.applicability['authorization_id'],'arbitrary child invocation forbidden')
    require(a['proposal']['sha256']=='cb68a30719e88496504cd38004750b5b6848e4f31f1836387b87984ae92a8adc','unaccepted r9 proposal')
    d=read(a['parent_dispatch'])
    require(p['dispatch']==a['parent_dispatch'] and p['bindings']=={k:d[k] for k in BOUND},'attempt substituted parent authority')
    require(d['release_authority']==a['predecessor_release_authority'] and d['succession_head']==a['supervisor_succession'] and d['current_supervisor']==a['supervisor_instance'],'release/supervisor ancestry mismatch')
    predecessor_no_effects(p)
    require(p['automatic_retry'] is False and p['initial_state']=='INACTIVE' and p['ownership']=='NONE','inherited attempt state')
    require(a['correction_continuation']==spec['continuation'],'correction ancestry substituted')
    c=read(spec['continuation']);body={k:c[k] for k in BODY_KEYS}
    require(c==seal(body,c['approval']) and c['schema']=='OPERATIONAL-CONTINUATION-1' and c['classification']=='NON_MATERIAL_IMPLEMENTATION_CONTINUATION','correction continuation invalid')
    approval=read(c['approval'])
    require(approval=={'authority':'Architect','decision':'INTEGRATE_QUALIFIED_ISSUANCE_AND_AUDIT_COMPOSITION_CORRECTIONS',
        'authority_source':a['authority_source'],'body_sha256':digest(body),'evidence':body['evidence']},'unapproved correction continuation')
    accepted=read(a['accepted_corrections']);qualification=read(body['evidence'])
    require(qualification['status']=='PASS_SYNTHETIC_NOT_PRODUCTION_ADOPTION' and qualification['implementation']==accepted['identity'],'accepted correction qualification missing')
    require(body['authority']==a['authority_source'] and body['authority_invariants']==p['bindings'] and body['sequence']==1,'correction protected authority changed')
    require({Path(row['path']).name for row in body['artifacts']}=={'activation_transaction.py','authorization_lifecycle.py','run_control.py','invocation_issuance.py'},'unrelated non-material correction')
    for row in body['artifacts']:
        require(accepted['inventory'][row['path']]==row['new_sha256'],'correction differs from accepted qualification')
        require(sha(read_authority_ref(row['new_content']))==row['new_sha256'],'correction artifact substitution')
    runtime=read(a['controller_runtime'])
    require(runtime['identity']=='sha256:'+digest(runtime['files']),'controller runtime identity mismatch')
    root=Path(runtime['root']);outside(root,store.catalog['programmer_roots'])
    actual={p.name:sha(p.read_bytes()) for p in (root/'adapter').glob('*.py')}
    require(actual==runtime['files'] and Path(__file__).resolve().parent==root/'adapter','unexplained controller implementation')
    require(a['ModelPayloadDigest']==p['bindings']['ModelPayloadDigest'],'payload change forbidden')
    return s,amendment,a,c,p,d,runtime

def peer(a,operation):
    conf=a['predecessor_verifier'];read_exact(conf['path'],conf['sha256']);read_exact(conf['python'],conf['python_sha256'])
    # A fixed read-only program; no input originates in a model/tool request.
    env={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':conf['repository']}
    bootstrap="import sys,runpy; root=sys.argv.pop(1); sys.path.insert(0,root); sys.argv=sys.argv[1:]; runpy.run_path(sys.argv[0],run_name='__main__')"
    result=subprocess.run([conf['python'],'-B','-I','-c',bootstrap,conf['repository'],conf['path'],canonical(a['predecessor_publication']),operation],
        cwd=conf['repository'],env=env,capture_output=True,timeout=30)
    require(result.returncode==0,'frozen predecessor verification failed: '+result.stderr.decode()[-800:])
    require(len(result.stdout)<20_000_000,'predecessor proof oversized')
    return json.loads(result.stdout)

def predecessor(store,a):
    pin=a['predecessor_publication'];b=read_exact(pin['path'],pin['sha256']);publication=json.loads(b)
    old=ControllerAuthorityStore(**publication['selected_store'])
    try:
        key=digest({'publication':pin,'verifier':a['predecessor_verifier']})
        cached=getattr(store,'_attempt_predecessor',{}).get(key)
        if cached is None:
            proof=peer(a,'context');packed=canonical(proof)
            store._attempt_predecessor={key:(packed,sha(packed.encode()))}
        else:
            packed,h=cached;require(sha(packed.encode())==h,'predecessor cache substituted');proof=json.loads(packed)
        old.verify_immutable_witness(proof['immutable_witness'])
        for path,h in proof['mutable'].items():read_exact(path,h)
        return proof
    finally:old.close()

def identities(amendment,continuation,prior):
    release=ident('E1-RELEASE-AUTHORITY',{'predecessor':prior['release_authority'],'attempt_amendment':amendment['id']})
    ids={k:prior[k] for k in ('ReleaseBasisId','ReleaseDecisionId')}
    ids.update(OperationalContextId=ident('E1-OPERATIONAL-CONTEXT',{'predecessor':prior['OperationalContextId'],
        'amendment':amendment['id'],'continuation':continuation['continuation_id']}),
        continuation_chain_digest=digest({'predecessor':prior['continuation_chain_digest'],'amendment':amendment['id'],'continuation':continuation['continuation_id']}))
    return release,ids

def verify(owner):
    store=current();spec=owner.spec
    require(set(spec)=={'schema','amendment','continuation','identities','release_basis','release_decision','released_profile','clearance'} and digest(spec)==owner._issued_digest and spec['schema']==5,'attempt context changed')
    s,amendment,a,c,p,d,runtime=decision(spec)
    proof=predecessor(store,a);old=proof['governance'];op=json.loads(proof['authorization']['operational_binding'])
    for key in ('release_basis','release_decision','released_profile','clearance'):
        require(spec[key]==op['governance'][key],'released authority selection replaced')
    require(c['predecessor_OperationalContextId']==old['identities']['OperationalContextId'] and c['predecessor_chain_digest']==old['identities']['continuation_chain_digest'],'stale correction predecessor')
    require(proof['dispatch']==d and old['run2']['release_authority']==a['predecessor_release_authority'],'predecessor dispatch/release unauthenticated')
    release,ids=identities(amendment,c,dict(old['identities'],release_authority=a['predecessor_release_authority']))
    require(spec['identities']==ids and store.applicability==dict(ids,authorization_id=p['invocation_identity']['authorization_id']),'attempt context ancestry substitution')
    for name in ('changes','authority_invariants','anchor_projection','anchor_op','ancestor_ops'):
        setattr(owner,name,old[name])
    owner.identities=ids;owner.supplement=json.loads(canonical(old['supplement']))
    owner.supplement['controller_runtime']={'identity':runtime['identity'],'authority':spec['amendment'],'corrections':spec['continuation']}
    owner.ancestry=old['ancestry']+[{'material_attempt_amendment':amendment['id'],'release_authority':release,
        'implementation_continuation':c['continuation_id'],**ids}]
    owner.run5={'release_authority':release,'proposal':p,'amendment':a,'selection':s,'predecessor':proof,'continuation':c}
    return ids

def verify_authorization(auth):
    g=auth.context_binding.governance;g.verify();op=json.loads(auth.operational_binding)
    require(set(op)-{'dispatch_authorization'}=={'governance','released_launch','invocation_identity','context_identities'} and op['governance']==g.spec,'attempt authorization context substituted')
    expected=json.loads(canonical(g.run5['predecessor']['authorization']));expected.update(g.run5['proposal']['invocation_identity'])
    expected.pop('operational_binding')
    actual=dict(auth.__dict__);actual.pop('operational_binding')
    actual['context_binding']={'path':str(auth.context_binding.path),'capture_commit':auth.context_binding.capture_commit}
    if actual['state']=='ACTIVE':require_issued(auth);expected['state']='ACTIVE'
    require(json.loads(canonical(actual))==expected,'attempt authorization broadened or substituted')
    oldop=json.loads(g.run5['predecessor']['authorization']['operational_binding'])
    require(op['released_launch']==oldop['released_launch'] and op['invocation_identity']==g.run5['proposal']['invocation_identity'],'attempt invocation/launch substitution')
    return op

def require_issued(auth):
    s=selected();require(s['mode']=='ISSUED' and s['specific_invocation_authorization'] is not None,'specific Architect r9 issuance authorization absent')
    g=auth.context_binding.governance
    from .invocation_attempt import authenticate,require_claim
    p,_,approval=authenticate(current(),g.run5['amendment']['proposal'])
    require(read(s['specific_invocation_authorization'])==approval,'unselected specific approval')
    q=read(s['qualification'])
    require(q['result']=='PASS' and q['amendment']==g.spec['amendment'] and
        q['controller_runtime']==g.run5['amendment']['controller_runtime'] and
        q['accepted_proposal']==g.run5['amendment']['proposal'],'unqualified production attempt context')
    return approval


def verify_dispatch(auth,decision):
    g=auth.context_binding.governance;g.verify();s=selected()
    if s['mode']=='ISSUED':
        require_issued(auth)
        from .invocation_attempt import require_claim
        require_claim(current(),g.run5['amendment']['proposal'])
    expected=derive_dispatch(auth)
    require(decision==expected,'attempt dispatch derivation substituted')
    return 'PROSPECTIVE' if s['mode']=='PREPARED' else 'ISSUED'

def derive_dispatch(auth):
    g=auth.context_binding.governance;op=json.loads(auth.operational_binding);p=g.run5['proposal']
    d=dict(g.run5['predecessor']['dispatch'])
    d.update(g.identities);d.update(op['context_identities']);d.update(invocation_identity=p['invocation_identity'],
        decision='PROPOSED_DISPATCH' if selected()['mode']=='PREPARED' else 'DISPATCH_AUTHORIZED',
        parent_dispatch=p['dispatch'],attempt_authority=g.spec['amendment'],accepted_attempt_binding=g.run5['amendment']['proposal'],
        authority_source=g.run5['amendment']['authority_source'],release_authority=g.run5['release_authority'])
    original=dict(op);original.pop('dispatch_authorization',None)
    d['all_authorized_bindings']=dict(d['all_authorized_bindings'],audit=p['audit'],operational_binding_sha256=digest(original))
    return d

def readiness(auth,store,historical,check_scopes,legacy_check):
    g=auth.context_binding.governance;g.verify()
    result=peer(g.run5['amendment'],'readiness')
    result.pop('immutable_witness',None)
    require(result['SupervisorInstanceId']==g.run5['proposal']['bindings']['current_supervisor'] and
        result['SupervisorSuccessionHead']==g.run5['proposal']['bindings']['succession_head'],'current supervisor changed')
    return result
