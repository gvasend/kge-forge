"""Prepare documentary, non-authorizing Run-2 candidates. No runtime mutation."""
import ast,json,os
from pathlib import Path
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.context_projection import canonical,digest,sha,model_input,model_payload_digest
from adapter.responses_orchestrator import tool_definitions,TOOL_NAMES
from adapter.run_control import E1_POLICY

O=Path(__file__).resolve().parent
Q=O/'qualification_final_seal'
A='auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39'
P=Path('/tmp/kge-forge-controller-authority')/A
pin=P/'supervisor-succession-adoption-2026-09-17/SUCCESSION_PUBLICATION.json'
data=pin.read_bytes();assert sha(data)=='95a2454b094f2b6e4af044cbfa8a8efd98a225866e2b19fc286a2d63abdacd4e'
store=ControllerAuthorityStore(**json.loads(data)['selected_store'])
def write(name,value):
    data=canonical(value).encode();path=O/name
    with path.open('xb') as f:f.write(data)
    return {'path':str(path),'sha256':sha(data)}
try:
    raw=json.loads(store.resolve(A));oldop=json.loads(raw['operational_binding'])
    original_profile=json.loads(store.resolve('sha256:'+oldop['governance']['released_profile']['sha256']))
    spec=json.loads(raw['context_projection'])
    clearance=json.loads(store.resolve('sha256:'+spec['clearance_sha256']))
    payload={'task':None,'context':{'schema':'E1-CLEARED-CONTEXT-1','sources':[]}}
    for row in clearance['inputs']:
        if row['classification']!='TRANSMIT':continue
        content=store.resolve('sha256:'+row['captured_sha256'])
        selections=[]
        for span in row['spans']:
            part=content[span['start_byte']:span['end_byte_exclusive']]
            assert sha(part)==span['sha256']
            selections.append({'label':span['label'],'content':part.decode()})
        if row['canonical_path']==spec['task_path']:payload['task']=content.decode()
        else:payload['context']['sources'].append({'source':row['canonical_path'],'selections':selections})
    assert payload['task'] is not None
    # Recompute the historical digest using exact frozen Run-1 tool functions.
    baseline=json.loads((O/'BASELINE_IMPLEMENTATION.json').read_bytes())
    source=(O/'baseline'/baseline['adapter/responses_orchestrator.py']).read_text()
    tree=ast.parse(source);functions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('_string','tool_definitions')]
    ns={'TOOL_NAMES':TOOL_NAMES};exec(compile(ast.Module(body=functions,type_ignores=[]),'frozen_run1_tools','exec'),ns)
    old_digest=digest({'input':model_input(payload),'tools':ns['tool_definitions']()})
    assert old_digest=='8e9b1fa28d57a4c4e21e28dbe9be7d70e028438ce425862b43b3728d9c22b577'
    new_digest=model_payload_digest(payload)
    assert new_digest!=old_digest
    # Only separately cleared initial content is copied into this documentary file.
    payload_ref=write('PROPOSED_MODEL_PAYLOAD.json',{'payload':payload,'tools':tool_definitions(),
        'ModelPayloadDigest':new_digest,'historical_ModelPayloadDigest':old_digest,
        'initial_context_content_unchanged':True})
    transmission=json.loads(raw['model_transmission'])
    historical_transmission_source=transmission['authority_source']
    transmission['authority_source']='PROPOSED Run-2 material clearance; Architect decision required; not issued'
    transmission['permitted_result_category']='Previously cleared exact file bytes, constant redaction, or explicitly cleared fixed READ_LIMIT_OUT_OF_RANGE diagnostic only'
    transmission.update({'run_control':E1_POLICY,
        'safe_diagnostics':{'schema':'E1-SAFE-DIAGNOSTICS-1','codes':['READ_LIMIT_OUT_OF_RANGE']},
        'action_evidence':'GRANTED_RESOURCE_AND_SCALARS_V1'})
    policy_ref=write('PROPOSED_TRANSMISSION_AND_RUN_POLICY.json',transmission)
    inventory={str(p.resolve()):sha(p.read_bytes()) for p in sorted(Path('adapter').glob('*.py'))}
    inventory_ref=write('PROPOSED_IMPLEMENTATION.json',{'identity':'sha256:'+digest(inventory),'inventory':inventory})
    seed=digest({'predecessor':A,'ModelPayloadDigest':new_digest,'policy':digest(transmission)})
    identity={'authorization_id':'auth-e1-wp-001-r8-'+seed[:32],'revision':8,
        'session_id':'session-e1-run2-'+seed[32:48],'turn_id':'turn-e1-run2-'+seed[48:]}
    profile=json.loads(canonical(original_profile))
    profile.update({'state':'INACTIVE','revision':8,'release_authorized':False,
        'eligible':False,'dispatch_issued':False,'architect_status':'PENDING_ARCHITECT_REVIEW',
        'qualification_state':'SYNTHETIC_ONLY_NOT_RELEASED','model_transmission':transmission})
    profile['identity']=dict(profile['identity'],production_ids_allocated=False,
        allocated=None,proposed_allocation=identity)
    profile['tool_registry']=tool_definitions()
    profile['operational_limits'].update({'run_control':E1_POLICY,'INCOMPLETE':'CANCEL_AFTER_RECONCILIATION',
        'uncertain_outcome':'INDETERMINATE_OWNERSHIP_HELD_NO_RETRY'})
    profile['model_information_categories']['TRANSMIT']+='; proposed separately cleared READ_LIMIT_OUT_OF_RANGE + fixed 1..65536 range only'
    profile['proposed_run2_bindings']={'ModelPayloadDigest':new_digest,'payload':payload_ref,
        'implementation':inventory_ref,'controller_entry':'adapter.controlled_dispatch.dispatch',
        'policy':policy_ref,'historical_profile':oldop['governance']['released_profile'],
        'Architect_release_decision':None,'Architect_dispatch_authorization':None,
        'approval_state':'PROPOSED_ONLY'}
    profile['audit'].update({'proposed_path':profile['audit']['path_rule'].format(**identity),
        'created':False,'mechanism':'Existing audit append + E1-RUN-CONTROL-1'})
    profile_ref=write('PROPOSED_RUN2_PROFILE.json',profile)
    qualified=json.loads((Q/'REGRESSION_RESULTS.json').read_bytes())
    assert qualified['verdict']=='PASS'
    closure=json.loads((Q/'QUALIFICATION_CLOSURE.json').read_bytes())
    assert closure['result']=='PASS' and closure['source_unchanged_during_qualification']
    for p,h in json.loads((Q/'QUALIFIED_SOURCE_INVENTORY.json').read_bytes()).items():assert sha(Path(p).read_bytes())==h
    timing=json.loads((Q/'TIMING_RESULTS.json').read_bytes())
    proposal={'schema':'E1-RUN2-RELEASE-PROPOSAL-1','state':'PROPOSED_NOT_AUTHORIZED',
        'predecessor_operational_context':oldop['governance']['identities'],
        'historical_release_authority':'E1-RELEASE-AUTHORITY-sha256:c0d6aed0894c9d07945b017423b3bb2fedb7207780b5e3d4e6c928aacb82bae3',
        'Run1_terminal_event':'E1-AUTHORIZATION-LIFECYCLE-sha256:2dedc9e0b3dca1cd6b481b9f53f78f3aa925508150a4356c99f75e5a000efc2a',
        'profile':profile_ref,'payload':payload_ref,'implementation':inventory_ref,'policy':policy_ref,
        'historical_transmission_authority_source':historical_transmission_source,
        'proposed_invocation_identity':identity,'issued_authorization':None,'dispatch_authorization':None,
        'activation':None,'ownership_reservation':None,'supervisor_succession_unchanged':
        'SupervisorSuccession-sha256:e547147d27f88c38fe8dbfafdd6e45330621cf2e59ae156af60b885fa6f83db5',
        'qualification':{'regression_sha256':sha((Q/'REGRESSION_RESULTS.json').read_bytes()),
            'timing_sha256':sha((Q/'TIMING_RESULTS.json').read_bytes()),
            'closure_sha256':sha((Q/'QUALIFICATION_CLOSURE.json').read_bytes()),'tests':qualified['tests']},
        'unchanged':{'task_sha256':sha(payload['task'].encode()),'work_id':'E1-WP-001',
            'initial_context_sha256':digest(payload),'execution_profile_sha256':sha(raw['execution_profile'].encode()),
            'model_transport_sha256':sha(raw['model_transport'].encode()),
            'read_roots':raw['read_roots'],'read_deny_roots':raw['read_deny_roots'],
            'write_roots':raw['write_roots'],'write_deny_roots':raw['write_deny_roots']},
        'release_applicability':{'telemetry_storage':'NON_MATERIAL_CANDIDATE_SUBJECT_TO_RETENTION_REVIEW',
            'budget_stopping':'MATERIAL_RELEASE_CHANGE','validation_performance':'NON_MATERIAL_IMPLEMENTATION_CANDIDATE',
            'tool_schema_payload':'MATERIAL_RELEASE_CHANGE','denial_transmission':'MATERIAL_RELEASE_CHANGE',
            'argument_retention':'MATERIAL_POLICY_CHANGE','INCOMPLETE_lifecycle':'MATERIAL_RELEASE_CHANGE'},
        'blocking_decisions':['Architect approval of new payload/profile/transmission and stopping semantics',
            'Qualified material-release decision-consumption binding for this amendment scope (existing material verifier is supervisor-only)',
            'Full amended-production ancestry timing and current supervisor readiness before activation',
            'Separate Run-2 dispatch/activation authorization; no inheritance of cancelled Run-1 invocation'],
        'warm_synthetic_target_pass':timing['warm_below_soft_threshold']}
    identity='E1-RUN2-RELEASE-PROPOSAL-sha256:'+digest(proposal)
    final=write('PROPOSED_OPERATIONAL_BINDING.json',{'proposal_identity':identity,'body':proposal})
    write('PROPOSAL_SUMMARY.json',{'proposal_identity':identity,'proposal_file':final,
        'proposed_profile_sha256':profile_ref['sha256'],'ModelPayloadDigest':new_digest,
        'implementation_identity':'sha256:'+digest(inventory),'published':False,'Run2_started':False})
    print(canonical({'proposal_identity':identity,'ModelPayloadDigest':new_digest,'profile_sha256':profile_ref['sha256']}))
finally:store.close()
