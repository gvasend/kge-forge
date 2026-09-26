"""Pure documentary construction. Does not publish, select, activate or dispatch."""
import json
from pathlib import Path
from adapter.context_projection import canonical,digest,sha
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.run2_amendment import sealed,RUN1_AUTH,PRIOR_RELEASE,PRIOR_AMENDMENT,PAYLOAD,SCOPES
from adapter.run_control import E1_POLICY
O=Path(__file__).resolve().parent
R=O.parent/'run2_remediation_2026-09-17'
ROOT=O.parents[3]
def write(name,value):
    b=canonical(value).encode();p=O/name
    with p.open('xb') as f:f.write(b)
    return {'authority_id':'sha256:'+sha(b),'sha256':sha(b)}
def ref(p):
    b=Path(p).read_bytes();return {'authority_id':'sha256:'+sha(b),'sha256':sha(b)}
def logical(r):return {'authority_id':'sha256:'+r['sha256'],'sha256':r['sha256']}
accepted=(R/'PROPOSED_RUN2_PROFILE.json').read_bytes()
assert sha(accepted)=='3eb002b0ab1d40fc6821665456bdefff85d1e30a7a0ab64a9cf4592091575b91'
payload=json.loads((R/'PROPOSED_MODEL_PAYLOAD.json').read_bytes());assert payload['ModelPayloadDigest']==PAYLOAD
inventory={str(p):sha(p.read_bytes()) for p in sorted((ROOT/'adapter').glob('*.py'))}
assert inventory
implementation=write('IMPLEMENTATION.json',{'identity':'sha256:'+digest(inventory),'inventory':inventory})
unit=O/'host_package/kge-forge-supervisor-run2.service';launcher=O/'host_package/host_launch.py'
life={'schema':'SUPERVISOR-HOST-LIFETIME-1','mechanism':'ROOT_SYSTEM_SERVICE_NO_RESTART',
      'unit_sha256':sha(unit.read_bytes()),'launcher_sha256':sha(launcher.read_bytes()),
      'terminal_closure_qualification_required':True,'automatic_restart':False,
      'new_host_authorization_required':True,'new_specific_succession_required':True}
profile=json.loads(accepted)
profile['proposed_run2_bindings']['implementation']={'path':str(O/'IMPLEMENTATION.json'),'sha256':implementation['sha256']}
profile['supervisor_durability']=life
pr=write('PROPOSED_RUN2_PROFILE.json',profile)
old=json.loads((R/'PROPOSED_OPERATIONAL_BINDING.json').read_bytes())['body']
pin=Path('/tmp/kge-forge-controller-authority')/RUN1_AUTH/'supervisor-succession-adoption-2026-09-17/SUCCESSION_PUBLICATION.json'
b=pin.read_bytes();assert sha(b)=='95a2454b094f2b6e4af044cbfa8a8efd98a225866e2b19fc286a2d63abdacd4e'
s=ControllerAuthorityStore(**json.loads(b)['selected_store'])
try:
    raw=json.loads(s.resolve(RUN1_AUTH));g=json.loads(raw['operational_binding'])['governance']
finally:s.close()
closure=json.loads((O/'regression_final/QUALIFICATION_CLOSURE.json').read_bytes())
assert closure['result']=='PASS'
log=(O/'DECISION_TESTS.log').read_text();assert 'Ran 10 tests' in log and log.rstrip().endswith('OK')
final_log=(O/'FINAL_BOOTSTRAP_TESTS.log').read_text();assert final_log.rstrip().endswith('OK')
q=write('QUALIFICATION.json',{'result':'BLOCKED','implementation_identity':'sha256:'+digest(inventory),
    'non_live_regression':ref(O/'regression_final/QUALIFICATION_CLOSURE.json'),
    'final_bootstrap_regression':ref(O/'FINAL_BOOTSTRAP_TESTS.log'),
    'bounded_decision_preflight':{'result':'PASS','tests':10,'log':ref(O/'DECISION_TESTS.log')},
    'terminal_primitive':ref(O/'TERMINAL_PROBE.json'),
    'production_bootstrap':ref(O/'ACTUAL_BOOTSTRAP_TIMING.json'),
    'blockers':['Complete Run-2 operational-context/projection integration is not qualified',
      'No successfully validated actual amended Run-2 context or production warm timing',
      'Privileged terminal-independent supervisor package launch/closure qualification pending',
      'No Run-2 release decision, specific dispatch, new host consent or successor acceptance'],
    'live_or_model_operations':False})
accepted_changes={'non_material_candidates':['correlated_timing','read_only_status','immutable_evidence_reuse'],
    'material':list(SCOPES),'decision_scope':'APPROVED_FOR_RELEASE_CONSTRUCTION_ONLY',
    'final_release_decision':None,'new_dispatch_authorization':None,'host_consent':None}
construction=write('ARCHITECT_CONSTRUCTION_DECISIONS.json',accepted_changes)
c={'schema':'E1-RUN2-RELEASE-AMENDMENT-1','status':'PROPOSED_BLOCKED_NOT_RELEASED',
    'prior_release_authority':PRIOR_RELEASE,'prior_supervisor_amendment':PRIOR_AMENDMENT,
    'material_scopes':list(SCOPES),'ModelPayloadDigest':PAYLOAD,'budget_policy':E1_POLICY,
    'work_package':'E1-WP-001','new_invocation_required':True,
    'successor_instance':None,'host_launch_authorization':None,
    'original_release_decision':logical(g['release_decision']),
    'original_release_basis':logical(g['release_basis']),
    'prior_supervisor_decision':g['material_release']['release_decision'],
    'profile':pr,'payload':ref(R/'PROPOSED_MODEL_PAYLOAD.json'),
    'policy':ref(R/'PROPOSED_TRANSMISSION_AND_RUN_POLICY.json'),
    'implementation':implementation,'qualification':q,'construction_decisions':construction,
    'predecessor_operational_context':{k:g['identities'][k] for k in ('OperationalContextId','continuation_chain_digest')},
    'applicable_continuations':[],
    'accepted_non_material_changes':accepted_changes['non_material_candidates'],
    'non_material_disposition':'Included in proposed material implementation; no separate continuation applied',
    'unchanged_authorities':old['unchanged'],'run1_terminal_event':old['Run1_terminal_event'],
    'run1_preservation':ref(R/'RUN1_PRESERVATION.json'),
    'findings':['OBS-E1-001','EFF-E1-002','SUP-E1-003'],
    'accepted_profile_ancestor_sha256':sha(accepted),'supervisor_durability':life,
    'Architect_amendment_decision':None}
candidate=sealed('E1-RUN2-RELEASE-AMENDMENT',c);cr=write('PROPOSED_AMENDMENT.json',candidate)
rid='E1-RELEASE-AUTHORITY-sha256:'+digest({'predecessor':PRIOR_RELEASE,'Run2AmendmentId':candidate['id']})
head={'OperationalContextId':'E1-OPERATIONAL-CONTEXT-sha256:'+digest({'predecessor':g['identities']['OperationalContextId'],'Run2AmendmentId':candidate['id']}),
      'continuation_chain_digest':digest({'predecessor':g['identities']['continuation_chain_digest'],'Run2AmendmentId':candidate['id']})}
plan=json.loads((ROOT/'docs/experiments/E1/pre_dispatch/pd06_supervisor_amendment_publication_2026-09-17_final/PROPOSED_LAUNCH_SPEC.json').read_bytes())
plan['predecessor_id']='SupervisorInstance-sha256:1aaa0c96caadb97c3e0678e8c0039f32cb2ac7f7ff3c607cf84998190b8e0a41'
plan['status']='PROPOSED_NOT_AUTHORIZED';plan['implementation']=inventory
plan['host_launcher']={'path':str(launcher),'sha256':sha(launcher.read_bytes())}
plan['host_lifetime']=life
plan['runtime_binding']={'proposed_release_authority':rid,'proposed_operational_context':head,
    'issued_runtime_binding':None,'controller_store_selection':None}
plan['prelaunch_supervisor_audit_sha256']=None
plan['environment']['PYTHONPYCACHEPREFIX']='/var/cache/kge-forge-supervisor-run2/S3'
plan['protocol_configuration']['environment']=plan['environment']
plan['missing_before_executable_plan']=['Completed material implementation/production-context qualification',
    'Architect exact release and specific candidate-attempt authorization','Jerry exact new host consent',
    'Fresh recovery audit and host observations','Issued runtime and private-store binding']
plan['applicability_note']='S2 remains historical; S3 is unset. This template cannot launch.'
write('host_package/PROPOSED_LAUNCH_SPEC.json',plan)
manifest=write('HOST_PACKAGE_MANIFEST.json',{'status':'PROPOSED_NOT_INSTALLED_NOT_AUTHORIZED',
    'files':{str(p.relative_to(O)):sha(p.read_bytes()) for p in sorted((O/'host_package').iterdir()) if p.is_file()},
    'missing_authorization_file':'HOST_LAUNCH_AUTHORIZATION.json','procedure':ref(O/'HOST_PROCEDURE.md')})
summary={'verdict':'BLOCKED_NOT_RELEASABLE','profile_sha256':pr['sha256'],'ModelPayloadDigest':PAYLOAD,
    'proposed_amendment_identity':candidate['id'],'candidate_file_sha256':cr['sha256'],
    'proposed_resulting_release_authority':rid,'proposed_operational_context':head,
    'current_operational_context_unchanged':g['identities'],'host_package_manifest':manifest,
    'implementation_identity':'sha256:'+digest(inventory),'qualification':q,
    'Run2_started':False,'Run2_activation_created':False,'Run2_ownership_created':False,
    'Run2_model_requests':0,'successor_launched':False,'published':False}
write('RESULT.json',summary)
print(canonical(summary))
