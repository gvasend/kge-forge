"""Versioned, non-self-authorizing E1 Run-2 material context.

Candidate inspection and issued authority share content verification. A private
PROSPECTIVE selection cannot activate, reserve ownership or dispatch. Its report
is deliberately not a production activation validation proof.
"""
from .validation_spans import measured
import ast
import json
from pathlib import Path
from types import SimpleNamespace
from .context_projection import canonical,digest,sha,read_exact,model_input
from .controller_authority_store import current,read_authority_ref,authority_bytes
from .run2_amendment import RUN1_AUTH,PRIOR_RELEASE,PRIOR_AMENDMENT,PAYLOAD,SCOPES,require,read,sealed,unseal
from .run_control import E1_POLICY

HEAD={'OperationalContextId':'E1-OPERATIONAL-CONTEXT-sha256:3672ba1076042f90563116c57a0e002beb19f03f164c4dfabc71fe721ac72453',
      'continuation_chain_digest':'2193231e010af1189bd90e5519bfc1232f84e0de8dfc9fd6ed5d377616f83515'}
TERMINATION='E1-AUTHORIZATION-LIFECYCLE-sha256:2dedc9e0b3dca1cd6b481b9f53f78f3aa925508150a4356c99f75e5a000efc2a'
APPROVED_PROFILE='3eb002b0ab1d40fc6821665456bdefff85d1e30a7a0ab64a9cf4592091575b91'


def identities(candidate, historical):
    return {**{k:historical[k] for k in ('ReleaseBasisId','ReleaseDecisionId')},
        'OperationalContextId':'E1-OPERATIONAL-CONTEXT-sha256:'+digest({'predecessor':HEAD['OperationalContextId'],'Run2AmendmentId':candidate['id']}),
        'continuation_chain_digest':digest({'predecessor':HEAD['continuation_chain_digest'],'Run2AmendmentId':candidate['id']})}


def selection(authorization_id, issued=False):
    store=current();require(store is not None,'private Run-2 context required')
    s=json.loads(store.resolve(authorization_id+':run2-context'))
    require(set(s)=={'candidate','release_decision','dispatch_decision','mode'},'unknown Run-2 context selection')
    require(s['mode'] in ('PROSPECTIVE','ISSUED'),'unknown Run-2 decision mode')
    if issued:require(s['mode']=='ISSUED','prospective Run-2 decisions cannot authorize effects')
    return s


@measured('decision_consumption')
def content(spec):
    store=current();require(store is not None,'private Run-2 context required')
    sel=selection(store.applicability['authorization_id'])
    require(sel['candidate']==spec['candidate'],'unselected Run-2 context')
    candidate=read(sel['candidate']);c=unseal(candidate,'E1-RUN2-RELEASE-AMENDMENT')
    require(c['schema']=='E1-RUN2-MATERIAL-CONTEXT-2' and c['prior_release_authority']==PRIOR_RELEASE and
            c['prior_supervisor_amendment']==PRIOR_AMENDMENT and c['material_scopes']==list(SCOPES),'Run-2 material scope mismatch')
    require(c['predecessor_operational_context']==HEAD and c['ModelPayloadDigest']==PAYLOAD and
            c['budget_policy']==E1_POLICY,'Run-2 ancestry/payload/budget substitution')
    prior=read(c['predecessor_authorization']);op=json.loads(prior['operational_binding'])
    require(prior['authorization_id']==RUN1_AUTH and {k:op['governance']['identities'][k] for k in HEAD}==HEAD,
            'Run-2 historical authorization substitution')
    inventory=read(c['implementation'])
    require(inventory['identity']=='sha256:'+digest(inventory['inventory']),'Run-2 implementation identity mismatch')
    actual={str(p.resolve()):sha(p.read_bytes()) for p in Path(__file__).resolve().parent.glob('*.py')}
    require(actual==inventory['inventory'],'Run-2 implementation changed')
    approved=read(c['approved_profile']);profile=read(c['profile'])
    require(c['approved_profile']['sha256']==APPROVED_PROFILE,'unapproved Run-2 authority ancestor')
    # Only storage/implementation bookkeeping and the explicitly required host
    # lifetime prerequisite may differ from the accepted profile content.
    expected=json.loads(canonical(approved))
    expected['proposed_run2_bindings']['implementation']=profile['proposed_run2_bindings']['implementation']
    expected['supervisor_durability']=profile['supervisor_durability']
    require(profile==expected,'Run-2 profile changes authority outside approved decisions')
    require(profile['proposed_run2_bindings']['implementation']['sha256']==c['implementation']['sha256'] and
            profile['supervisor_durability']==c['supervisor_durability'],'unbound Run-2 implementation/lifetime')
    require(c['supervisor_durability']['automatic_restart'] is False and
            c['supervisor_durability']['terminal_closure_qualification_required'] is True and
            c['supervisor_durability']['new_specific_succession_required'] is True,'supervisor durability weakened')
    policy=read(c['policy']);require(policy==profile['model_transmission'] and policy['run_control']==E1_POLICY,
                                   'Run-2 transmission/retention/budget changed')
    expected_authorization=dict(prior)
    expected_authorization.pop('operational_binding',None)
    require(c['invocation_identity']==approved['identity']['proposed_allocation'],'Run-2 invocation substitution')
    expected_authorization.update(c['invocation_identity'])
    expected_authorization.update(state='INACTIVE',model_transmission=canonical(policy))
    require(read(c['authorization_template'])==expected_authorization,'Run-2 authorization expanded or substituted')
    package=c['host_package']
    require(set(package)=={'launcher','unit'} and package['launcher']['sha256']==c['supervisor_durability']['launcher_sha256'] and
        package['unit']['sha256']==c['supervisor_durability']['unit_sha256'] and
        c['supervisor_durability']['mechanism']=='ROOT_SYSTEM_SERVICE_NO_RESTART','Run-2 host package substitution')
    read_authority_ref(package['launcher']);read_authority_ref(package['unit'])
    payload=read(c['payload'])
    require(payload['tools']==profile['tool_registry'] and
            digest({'input':model_input(payload['payload']),'tools':payload['tools']})==PAYLOAD,
            'Run-2 model payload substitution')
    # The task and cleared context are the original, separately cleared bytes.
    old_projection=json.loads(read_authority_ref(op['governance']['predecessor']['anchor']['projection']))
    require(payload['payload']==old_projection['payload'],'Run-2 task or cleared context changed')
    approval=read(c['construction_approval'])
    require(approval=={'authority':'Architect','decision':'AUTHORIZE_RUN2_NONHOST_RELEASE_CONSTRUCTION',
        'approved_profile_sha256':APPROVED_PROFILE,'ModelPayloadDigest':PAYLOAD,
        'material_scopes':list(SCOPES),'budget_policy':E1_POLICY,'host_launch_authorized':False},
        'Run-2 construction authority mismatch')
    termination=read(c['run1_termination'])
    require(termination['event_id']==TERMINATION and termination['resulting_state']=='CANCELLED',
            'Run-1 termination changed')
    body={k:v for k,v in termination.items() if k not in ('event_id','event_sha256')}
    require(termination['event_sha256']==digest(body) and TERMINATION.endswith(digest(body)),'Run-1 terminal fingerprint mismatch')
    require(c['run1_audit']['sha256']=='23d46d0fe282d322b731b309f7d48beebd676894ca0701e75c5468ed4fde427f',
            'Run-1 audit substitution')
    audit=read_authority_ref(c['run1_audit'])
    require(termination in [json.loads(x) for x in audit.splitlines()],'Run-1 terminal not in genuine audit')
    q=read(c['qualification'])
    require(q['result']=='PASS' and q['implementation_identity']==inventory['identity'],'Run-2 implementation qualification absent')
    return sel,candidate,c,prior,inventory


@measured('context_reconstruction')
def verify(owner):
    s=owner.spec
    require(set(s)=={'schema','candidate','identities','release_basis','release_decision','clearance','released_profile'} and s.get('schema')==4 and digest(s)==owner._issued_digest,'Run-2 operational spec changed')
    sel,candidate,c,prior,inventory=content(s)
    oldop=json.loads(prior['operational_binding']);oldg=oldop['governance']
    for key in ('release_basis','release_decision','clearance'):
        require(s[key]==oldg[key],'Run-2 original release/clearance replaced')
    require(s['released_profile']==c['profile'],'Run-2 selected profile mismatch')
    from .supervisor_amendment import verify_governance,read as oldread
    iq=oldread(oldg['material_release']['implementation_qualification'])
    sourcehash=iq['implementation']['current'][str(Path(__file__).resolve().parent/'responses_orchestrator.py')]
    source=authority_bytes('sha256:'+sourcehash).decode()
    tree=ast.parse(source)
    functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('_string','tool_definitions')]
    from .responses_orchestrator import TOOL_NAMES
    ns={'TOOL_NAMES':TOOL_NAMES};exec(compile(ast.Module(body=functions,type_ignores=[]),'released_tool_contract','exec'),ns)
    historical_tools=ns['tool_definitions']()
    store=current();key=digest({'historical':oldg,'tools':historical_tools,'implementation':inventory['identity']})
    cached=getattr(store,'_run2_verified_history',{}).get(key)
    if cached is None:
        old=SimpleNamespace(spec=oldg,_issued_digest=digest(oldg))
        with store.witness() as witness:
            verify_governance(old,successor_implementation=inventory['inventory'],historical_tools=historical_tools,
                              historical_authorization_id=RUN1_AUTH)
        packed=canonical(old.__dict__)
        store._run2_verified_history={key:(packed,sha(packed.encode()),dict(witness))}
    else:
        packed,h,witness=cached
        require(sha(packed.encode())==h,'historical reconstruction cache changed')
        store.verify_immutable_witness(witness)
        old=SimpleNamespace(**json.loads(packed))
        # These are live governing repository inputs, not immutable authority
        # objects. Revalidate them on every reuse; never cache mutable facts.
        for path,row in old.changes.items():read_exact(path,row['new_sha256'])
    require(old.identities==oldg['identities'],'Run-2 historical ancestry reconstruction mismatch')
    prefix=supervisor_prefix(store)
    require(prefix['applicability']==dict(old.identities,authorization_id=RUN1_AUTH),'historical supervisor epoch changed')
    from .supervisor_succession import reconstruct as reconstruct_supervisor
    restored=reconstruct_supervisor(store,prefix['policy'],prefix['data'],historical_applicability=prefix['applicability'])
    require(restored['instance']['id']==prefix['instance'] and restored['head']==prefix['head'],'historical S2 reconstruction failed')
    # Authenticate historical dispatch and its supervisor-only amendment; neither
    # one grants the new invocation permission to dispatch.
    historic_dispatch=oldread(old.material_decisions[1]['original_dispatch'])
    require(historic_dispatch['invocation_identity']['authorization_id']==RUN1_AUTH,'historical dispatch changed')
    ids=identities(candidate,old.identities)
    require(s['identities']==ids and current().applicability==dict(ids,authorization_id=c['invocation_identity']['authorization_id']),
            'Run-2 selected operational head stale')
    release=read(sel['release_decision']);r=unseal(release,'E1-RUN2-RELEASE-DECISION')
    authority='E1-RELEASE-AUTHORITY-sha256:'+digest({'predecessor':PRIOR_RELEASE,'Run2AmendmentId':candidate['id']})
    expected={'authority':'Architect','decision':('AUTHORIZE_E1_RUN2_RELEASE' if sel['mode']=='ISSUED' else 'PROPOSE_E1_RUN2_RELEASE'),
        'candidate':sel['candidate'],'resulting_release_authority':authority,'predecessor':PRIOR_RELEASE}
    require({k:r.get(k) for k in expected}==expected,'Run-2 release decision mismatch')
    source=read(r['authority_source'])
    require(source==dict(expected,channel='user' if sel['mode']=='ISSUED' else 'NON_EFFECTING_QUALIFICATION'),
            'Run-2 material decision attribution mismatch')
    owner.identities=ids;owner.changes=old.changes
    basis=json.loads(read_authority_ref(s['release_basis']));inputs=basis.get('current_inputs',basis.get('inputs'))
    owner.supplement={'inputs':{p:{'previous_sha256':inputs.get(p,{}).get('sha256'),'sha256':h}
        for p,h in inventory['inventory'].items()},'authority_source':c['construction_approval'],'material_release_authority':authority}
    owner.authority_invariants=dict(old.authority_invariants,ModelPayloadDigest=PAYLOAD)
    owner.anchor_projection=old.anchor_projection;owner.anchor_op=old.anchor_op;owner.ancestor_ops=old.ancestor_ops
    owner.ancestry=old.ancestry+[{'material_amendment':candidate['id'],'release_authority':authority,**ids}]
    owner.run2={'candidate':c,'selection':sel,'release_authority':authority,'release_decision':release['id']}
    return ids


def verify_authorization(auth):
    op=json.loads(auth.operational_binding);g=auth.context_binding.governance
    require(set(op)-{'dispatch_authorization'}=={'governance','released_launch','invocation_identity','context_identities'} and op['governance']==g.spec,'Run-2 operational specification mismatch')
    if 'dispatch_authorization' in op:
        require(op['dispatch_authorization']==selection(auth.authorization_id)['dispatch_decision'],'Run-2 dispatch selection changed')
    auth.context_binding.verify()
    c=g.run2['candidate'];expected=read(c['authorization_template'])
    actual=dict(auth.__dict__)
    actual['context_binding']={'path':str(auth.context_binding.path),'capture_commit':auth.context_binding.capture_commit}
    actual.pop('operational_binding');expected.pop('operational_binding',None)
    if actual['state']=='ACTIVE':
        selection(auth.authorization_id,issued=True);expected['state']='ACTIVE'
    require(json.loads(canonical(actual))==expected,'Run-2 authorization differs from exact release template')
    require(op['released_launch']==c['launch'] and op['invocation_identity']==c['invocation_identity'],
            'Run-2 launch/invocation changed')
    launch=read(c['launch'])
    require(launch['profile_sha256']==digest(read(c['profile'])) and launch['authorization']==dict(expected,state='INACTIVE'),
            'Run-2 launch/profile mismatch')
    return op


def verify_dispatch(auth,decision):
    g=auth.context_binding.governance;g.verify();sel=g.run2['selection'];c=g.run2['candidate']
    require(read(sel['dispatch_decision'])==decision,'unselected Run-2 dispatch')
    expected={'authority':'Architect','decision':'DISPATCH_AUTHORIZED' if sel['mode']=='ISSUED' else 'PROPOSED_DISPATCH',
        'release_authority':g.run2['release_authority'],'release_decision':g.run2['release_decision'],
        'ModelPayloadDigest':PAYLOAD,'invocation_identity':c['invocation_identity']}
    require({k:decision.get(k) for k in expected}==expected,'Run-2 dispatch cannot inherit from historical dispatch')
    src=read(decision['authority_source'])
    require(src==dict(expected,channel='user' if sel['mode']=='ISSUED' else 'NON_EFFECTING_QUALIFICATION',
        binding_sha256=digest(decision['all_authorized_bindings'])),'Run-2 dispatch attribution mismatch')
    return sel['mode']


def supervisor_prefix(store):
    """Immutable prior epoch. It supplies a predecessor, never current readiness."""
    chosen=selection(store.applicability['authorization_id'])
    candidate=read(chosen['candidate']);c=unseal(candidate,'E1-RUN2-RELEASE-AMENDMENT')
    ref=c['supervisor_historical_prefix'];value=read(ref)
    require(value['head']=='SupervisorSuccession-sha256:e547147d27f88c38fe8dbfafdd6e45330621cf2e59ae156af60b885fa6f83db5' and
        value['instance']=='SupervisorInstance-sha256:1aaa0c96caadb97c3e0678e8c0039f32cb2ac7f7ff3c607cf84998190b8e0a41',
        'historical S2 succession changed')
    policy=read(value['policy']);data=read_authority_ref(value['ledger'])
    require(policy['pinned_head']==value['head'] and policy['release_authority']==PRIOR_RELEASE,
        'historical supervisor release/head changed')
    from .supervisor_amendment import host_event
    from .supervisor_succession import events
    for row in events(data):host_event(store,row)
    return dict(value,reference=ref,policy=policy,data=data)


def supervisor_policy(auth,store):
    g=auth.context_binding.governance;g.verify();selection(auth.authorization_id,issued=True)
    p=json.loads(store.resolve(auth.authorization_id+':supervisor-succession'))
    prefix=supervisor_prefix(store);c=g.run2['candidate']
    require(p['schema']=='SUPERVISOR-SUCCESSION-POLICY-2' and p['historical_prefix']==prefix['reference'] and
        p['anchor_id']==prefix['instance'] and p['release_authority']==g.run2['release_authority'] and
        p['dispatch_amendment']==g.run2['selection']['dispatch_decision']['authority_id'] and
        p['requirements']['implementation']==read(c['implementation'])['inventory'],
        'Run-2 supervisor policy is not bound to amended authority')
    from .supervisor_succession import runtime_binding,equivalent
    old_instance=json.loads(store.resolve(prefix['instance']))
    baseline=equivalent(old_instance);req=p['requirements']
    require(all(req[k]==baseline[k] for k in ('uid','gid','groups','executable','workspace','socket')),
        'Run-2 supervisor runtime identity/workspace/socket changed')
    require(all(req['cgroup'][k]==baseline['cgroup'][k] for k in ('path','unified','device','inode')),
        'Run-2 delegated cgroup changed')
    config=json.loads(canonical(baseline['protocol_configuration']))
    config['environment']['PYTHONPYCACHEPREFIX']='/var/cache/kge-forge-supervisor-run2/S3'
    require(req['protocol_configuration']==config,'Run-2 supervisor protocol/configuration changed')
    require(p['runtime_binding']==runtime_binding(auth,store,read(c['profile'])),'Run-2 supervisor epoch stale')
    for aid in p['authorized_succession_ids']:
        approval=json.loads(store.resolve(aid));grant=json.loads(store.resolve(approval['host_authorization']))
        source=json.loads(store.resolve(grant['authority_source']))
        require(grant['authority']=='HOST_OPERATOR' and grant['operator']=='Jerry' and
            grant['decision']=='AUTHORIZE_HOST_SUPERVISOR_LAUNCH' and
            source['operator']=='Jerry' and source['channel']=='user' and
            source['authorization_id']==grant['authorization_id'] and
            grant['runtime_binding']==p['runtime_binding'] and
            grant['predecessor_id']==approval['predecessor_instance'] and
            grant['launch_spec_sha256']==approval['launch_spec_sha256'] and
            grant['launcher_sha256']==approval['launcher_sha256']==c['supervisor_durability']['launcher_sha256'],
            'Run-2 requires separate attributable host authorization')
    return p


def supervisor_readiness(auth,store,historical,check_scopes,legacy_check):
    from .supervisor_succession import reconstruct,legacy_tuple,events
    from .supervisor_observation import observe
    from .supervisor_amendment import host_event
    p=supervisor_policy(auth,store)
    data=store.state_path(p['ledger_id']).read_bytes()
    selected=reconstruct(store,p,data);candidate=selected['instance']
    require(candidate['runtime_binding']==p['runtime_binding'],'no qualified current supervisor in Run-2 epoch')
    for row in events(data):host_event(store,row)
    q=json.loads(store.resolve(p['terminal_closure_qualification']))
    require(q['schema']=='SUPERVISOR-TERMINAL-CLOSURE-1' and q['result']=='PASS' and
        q['instance_id']==candidate['id'] and q['before']==q['after']==candidate['process'] and
        q['operator_terminal_closed'] is True and q['independent_observer'] and q['authority']=='HOST_OPERATOR',
        'genuine terminal-closure qualification missing')
    host=json.loads(store.resolve(candidate['host_launch']))
    life=host['host_lifetime'];required=auth.context_binding.governance.run2['candidate']['supervisor_durability']
    require(life['unit_sha256']==required['unit_sha256'] and life['terminal_independent'] is True and
        life['properties']['Restart']=='no' and life['properties']['DropInPaths']=='' and
        life['service_invocation_id']==life['properties']['InvocationID'], 'unqualified supervisor host lifetime')
    require(observe(candidate)==candidate,'current supervisor birth/configuration changed')
    result=legacy_check(legacy_tuple(candidate),check_scopes=check_scopes)
    require(observe(candidate)==candidate and store.state_path(p['ledger_id']).read_bytes()==data,
        'supervisor identity/authority changed during readiness')
    return dict(result,SupervisorInstanceId=candidate['id'],SupervisorSuccessionHead=selected['head'])
