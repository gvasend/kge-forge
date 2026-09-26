"""Bounded read-only authority assessment plus exclusive proposal materialization.

No production imports, host launch, catalog selection, lifecycle append or grant.
"""
from pathlib import Path
import ast,hashlib,json,os,stat
OUT=Path(__file__).resolve().parent;PRE=OUT.parent;ROOT=PRE.parents[3]
Q=PRE/'supervisor_succession_2026-09-17'
sha=lambda b:hashlib.sha256(b).hexdigest()
canonical=lambda v:json.dumps(v,sort_keys=True,separators=(',',':'))
digest=lambda v:sha(canonical(v).encode())
def load(p):return json.loads(Path(p).read_bytes())
def ref(p):return {'path':str(Path(p).resolve()),'sha256':sha(Path(p).read_bytes())}
def exact(r):
    b=Path(r['path']).read_bytes();assert sha(b)==r['sha256'],r['path'];return b

def write(name,v):
    p=OUT/name
    with p.open('xb') as f:f.write(canonical(v).encode());f.flush();os.fsync(f.fileno())
    p.chmod(0o444)
    return ref(p)

closure=load(Q/'CLOSURE.json')
for v in closure.values():
    if isinstance(v,dict) and set(v)=={'path','sha256'}:exact(v)
manifest=json.loads(exact(closure['qualification']))
for p,r in manifest['inputs'].items():
    exact({'path':p,'sha256':r['sha256']})
    exact({'path':str(Q/'qualification/blobs'/r['sha256']),'sha256':r['sha256']})
before=load(Q/'IMPLEMENTATION_BEFORE.json')
assert before=={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in (ROOT/'adapter').rglob('*.py')}
for r in load(PRE/'controller_authority_store_2026-09-17/qualified/REFERENCE_CLASSIFICATION.json')['references']:exact(r['evidence'])
state=load(Q/'CURRENT_E1_RECONSTRUCTION.json')
assert state['result']=='PASS' and state['state']=='INACTIVE' and state['ownership']=='NO OWNERSHIP'
for p,h in state['preserved_mutable_fingerprints'].items():exact({'path':p,'sha256':h})
pin=Path('/tmp/kge-forge-controller-authority/auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39/adoption-2026-09-17/ADOPTION_RECORD.json')
adoption=json.loads(exact({'path':str(pin),'sha256':'420b41640db490b2fc33500cd02ffc52a55245c8b7c730b307a513502d2efa77'}))
store=Path(adoption['selected_store']['root']);catalog=json.loads(exact({'path':str(store/'catalog.json'),'sha256':adoption['selected_store']['catalog_sha256']}))
def private(identity):
    h=catalog['objects'][identity]['sha256'];return json.loads(exact({'path':str(store/h),'sha256':h}))
op=private(state['identities']['OperationalContextId']);g=op['governance'];profile=private('sha256:'+g['released_profile']['sha256'])
release=private(g['identities']['ReleaseDecisionId']);launch=private('sha256:'+op['released_launch']['sha256'])
assert release['decision']=={'PD06':'RELEASED','E1_B01':'PASS'}
assert digest(profile)==release['released_profile_sha256']
history=load(Q/'HISTORICAL_S1.json');hid=history.pop('id')
assert hid=='SupervisorHistoricalInstance-sha256:'+digest(history)
assert hid=='SupervisorHistoricalInstance-sha256:8ffe7a419d3953ed54fb1a73a9bd1d793cbe2c540c181cee9c0ca4e30987d572'
assert history['released_supervisor']==profile['supervisor_binding'][0]
assert history['released_profile_bytes_sha256']==g['released_profile']['sha256']
material=load(Q/'IMPLEMENTATION_DELTA.json');candidate=Q/'candidate'
for r in material['delta']:
    assert sha(Path(r['candidate_path']).read_bytes())==r['new_sha256']
    if r['old_sha256'] is not None:assert sha(Path(r['path']).read_bytes())==r['old_sha256']
old=(ROOT/'adapter/activation_transaction.py').read_text();new=(candidate/'adapter/activation_transaction.py').read_text()
replacement="    from .supervisor_succession import readiness as supervisor_readiness\n    host=supervisor_readiness(auth,store,req['supervisor'],idle_host,_host)"
assert new.replace(replacement,"    host=_host(req['supervisor'],check_scopes=idle_host)")==old
for name in ('ActivationTransaction','_host','invocation','execution_guard','_lease'):
    def item(text):return ast.dump(next(n for n in ast.parse(text).body if getattr(n,'name',None)==name))
    assert item(old)==item(new)
controller={str(ROOT/p.relative_to(candidate)):sha(p.read_bytes()) for p in (candidate/'adapter').glob('*.py')}
plan=load(Q/'PROPOSED_HOST_LAUNCH_SPEC.json');assert controller==plan['implementation']
impl={'controller':controller,'host_launcher':material['delta'][-1]['new_sha256']}
impl_id='sha256:'+digest(impl)
implementation_ref=write('QUALIFIED_IMPLEMENTATION_IDENTITY.json',{'identity':impl_id,'definition':'SHA256(canonical full controller inventory and host launcher hash)','inventory':impl,'delta':material['delta'],'qualified_capture':closure['qualification'],'exact_match':'PASS','deployed':False})

host=[]
for name in ('host_launch.py','LAUNCH_SPEC.json','HOST_LAUNCH_AUTHORIZATION.json'):
    p=Path('/var/lib/kge-forge-supervisor-succession')/name
    try:
        st=p.lstat();row={'path':str(p),'result':'PRESENT','mode':oct(stat.S_IMODE(st.st_mode)),'uid':st.st_uid,'gid':st.st_gid}
        if stat.S_ISREG(st.st_mode) and not p.is_symlink():row['sha256']=sha(p.read_bytes())
        else:row['result']='WRONG_TYPE'
    except FileNotFoundError:row={'path':str(p),'result':'ABSENT'}
    except PermissionError:row={'path':str(p),'result':'NOT_READABLE_NOT_VERIFIED'}
    host.append(row)
fields={
 'authority':{'issuer':'ARCHITECT','required':'Architect; backed by genuine decision provenance, never sufficient as a label'},
 'decision':{'issuer':'ARCHITECT','required':'AUTHORIZE_HOST_SUPERVISOR_LAUNCH; separate from amendment adoption, succession selection and dispatch'},
 'authorization_id':{'issuer':'ARCHITECT','required':'Genuine Architect launch-decision identity'},
 'qualification_acceptance_id':{'issuer':'ARCHITECT','required':'Genuine accepted qualification/applicability decision for the final exact implementation and plan'},
 'predecessor_id':{'issuer':'ARCHITECT; HOST acknowledges same target','required':hid},
 'runtime_binding':{'issuer':'ARCHITECT; HOST acknowledges exact binding','required':'Final approved release-amendment applicability, authorization/context/chain/profile/execution/store epoch; current old-context proposal is not final applicability'},
 'launch_spec_sha256':{'issuer':'ARCHITECT AND HUMAN_HOST','required':'Both consent to the exact final spec bytes, including source inventory, paths, runtime identity, cgroup-before-drop, environment and fresh audit hash'},
 'launcher_sha256':{'issuer':'ARCHITECT AND HUMAN_HOST','required':impl['host_launcher']},
 'host_operator_authorization_id':{'issuer':'HUMAN_HOST ONLY','required':'Independent host decision identifying operator/host, exact spec and launcher, purpose and permitted privileged actions. Architect must not invent it'},
 'remove_verified_stale_socket':{'issuer':'ARCHITECT scope AND HUMAN_HOST action consent','required':'Conditional true only with explicit permission from both and fresh proof the exact socket is stale; default deny. Observation alone grants no unlink authority'}
}
host_ref=write('HOST_PACKAGE_ASSESSMENT.json',{'installed_paths':host,'installed_package_result':'NOT_INSTALLED_OR_NOT_VERIFIED_NO_LAUNCH_AUTHORITY','source_wrapper':closure['host_launcher'],
 'source_exact_hash_verification':'PASS','source_syntax':'PASS','source_live_execution':'NOT_PERFORMED',
 'proposal_spec':closure['proposed_host_spec'],'proposal_status':plan['status'],'fresh_prelaunch_audit_sha256':plan['prelaunch_supervisor_audit_sha256'],
 'authorization_fields':fields,'field_exhaustiveness':'All ten authorization keys accessed by the qualified wrapper are listed, including the conditional stale-socket key.',
 'host_evidence_required_beyond_fields':['Authenticated independent host authorization source and exact linkage to host_operator_authorization_id','Host/operator identity and scope/validity of permitted privileged actions','Fresh absence/listener/scope/recovery observations and exact approved audit digest','Root-controlled staging after authenticating BOTH approvals','Post-launch root parent/placement-before-drop/credential/executable/source/config/socket/birth receipts'],
 'enforcement_limit':'The wrapper verifies root-controlled files and checks host_operator_authorization_id is nonempty. It does not resolve or authenticate a separate host-decision object. Root ownership and a supplied ID are not independent consent. A genuine independently authenticated host decision must be demonstrated before staging/launch; an automated verifier change would require new exact qualification.',
 'command':'sudo /usr/bin/python3.11 /var/lib/kge-forge-supervisor-succession/host_launch.py /var/lib/kge-forge-supervisor-succession/LAUNCH_SPEC.json /var/lib/kge-forge-supervisor-succession/HOST_LAUNCH_AUTHORIZATION.json',
 'command_executed':False,'files_installed':False,'authorizations_issued':False})

unchanged_fields={
 'E1-WP-001':['work_id','production_task_sha256'],
 'Programmer tool registry':['tool_registry'],
 'read authority':['effective_scope'],
 'write/patch authority':['effective_scope','captured_write_protections'],
 'execution-scope semantics':['runtime','operational_limits'],
 'QUIESCENT semantics':['operational_limits'],
 'sequential execution':['operational_limits','model_execution_settings'],
 'ownership semantics':['ownership'],
 'model-transmission authority':['model_transmission','content_clearance_sha256','model_information_categories'],
 'external destination policy':['model_transport','external_policy'],
 'released ModelPayloadDigest':[],
 'filesystem/snapshot isolation':['snapshot','runtime','effective_scope'],
 'audit/evidence isolation':['audit'],
 'authority-expansion semantics':['tool_registry','effective_scope'],
 'Architect dispatch requirement':[],
 'human/host authority boundary':['supervisor_binding']}
modules={
 'E1-WP-001':['context_binding.py'], 'Programmer tool registry':['responses_orchestrator.py'],
 'read authority':['governed_host.py','authority_profile.py'], 'write/patch authority':['governed_host.py','authority_profile.py'],
 'execution-scope semantics':['host_supervisor.py','exec_barrier.py','launch_broker.py'],
 'QUIESCENT semantics':['host_supervisor.py','termination.py','recovery_ledger.py'],
 'sequential execution':['orchestrator.py','invocation_ownership.py'], 'ownership semantics':['invocation_ownership.py'],
 'model-transmission authority':['model_transmission.py','context_projection.py'], 'external destination policy':['model_transport.py'],
 'released ModelPayloadDigest':['context_projection.py'], 'filesystem/snapshot isolation':['execution_snapshot.py','exec_barrier.py'],
 'audit/evidence isolation':['controller_authority_store.py','governed_host.py'], 'authority-expansion semantics':['orchestrator.py','governed_host.py'],
 'Architect dispatch requirement':['authorization_lifecycle.py','continuation_envelope.py'], 'human/host authority boundary':['supervisor_server.py','host_supervisor.py']}
matrix=[]
for name,keys in unchanged_fields.items():
    source=[]
    for mod in modules[name]:
        p=ROOT/'adapter'/mod;cp=candidate/'adapter'/mod;assert p.read_bytes()==cp.read_bytes();source.append(ref(p))
    row={'authority':name,'result':'UNCHANGED_IN_PROPOSED_AUTHORITY_BOUNDARY','original_profile_fields':{k:{'json_pointer':'/'+k,'canonical_sha256':digest(profile[k])} for k in keys},'unchanged_enforcement_sources':source}
    if name=='released ModelPayloadDigest':row['value']=state['identities']['ModelPayloadDigest']
    if name=='Architect dispatch requirement':row['qualification']='Explicit dispatch still mandatory. Existing dispatch does NOT automatically inherit the new material rule.'
    if name=='human/host authority boundary':row['qualification']='No Programmer host privilege or generic access is granted. Separate genuine host consent remains mandatory; wrapper provenance alone does not establish that consent. Host procedure is static-reviewed, not live-qualified.'
    matrix.append(row)
boundary_ref=write('MATERIAL_BOUNDARY_ASSESSMENT.json',{'verdict':'NARROW_MATERIAL_RULE_CHANGE_VERIFIED_AT_PROPOSAL_LEVEL','matrix':matrix,
 'material_change':'Only eligibility and authenticated succession of the Execution Supervisor authority holder. No action privilege, tool, resource grant, payload, destination or work-package change.',
 'original_profile_exact_bytes':g['released_profile'],'original_profile_canonical_sha256':digest(profile),
 'all_non_supervisor_profile_fields_sha256':digest({k:v for k,v in profile.items() if k!='supervisor_binding'}),
 'production_callsite_change':'Only the supervisor-selection call in validate_production changes; all other original module text matches after normalizing that callsite.',
 'unchanged_AST':['ActivationTransaction','_host','invocation','execution_guard','_lease'],
 'qualification_scope':'Accepted synthetic mechanism evidence; no release-amendment consumer/deployment, host readiness, or new dispatch authority is implied.'})

dispatch=private(state['dispatch_id']);assert 'no repair, replacement binding' in dispatch['authorization_scope']
source=exact(dispatch['authority_source']).decode();assert 'no MATERIAL governance continuation has occurred' in source
impact_ref=write('DISPATCH_IMPACT_ASSESSMENT.json',{'original_dispatch_identity':state['dispatch_id'],'original_dispatch_sha256':state['dispatch_id'].split(':')[-1],
 'original_authority_source':dispatch['authority_source'],'original_authorization_scope':dispatch['authorization_scope'],
 'automatic_inheritance_through_material_amendment':'DENIED',
 'current_unamended_inheritance':'PASS; unchanged original and adopted non-material ancestry only',
 'reason':'Original authorization explicitly requires no MATERIAL governance continuation, exact profile/release/context and forbids replacement binding. Qualified mechanism and equal model payload cannot override those conditions.',
 'smallest_semantically_correct_treatment':'EXPLICIT_ARCHITECT_DISPATCH_AMENDMENT_AUTHORIZATION',
 'required_future_binding':['Exact original dispatch ID/hash and authority source','Issued PD-06 supervisor amendment decision and resulting release-authority ID','Final material implementation/applicability and OperationalContextId/chain/FullContextDigest/ModelProjectionBindingDigest','Same E1-WP-001/task/payload/authorization/session/turn/revision/audit/ownership/clearance/destinations','Explicit exception only for this named supervisor-holder rule, with specific succession authorization and complete live readiness remaining mandatory','All other original dispatch conditions preserved; no uncertain-effect retry, new task or authority expansion'],
 'mechanism_limit':'Current dispatch_ancestor/OPERATIONAL-CONTINUATION-1 authenticates non-material immutable-release ancestry only. A typed material-amendment plus dispatch-amendment consumer must be qualified before operational use. If that representation is unavailable, a new full explicit Architect dispatch decision is required; neither is issued here.',
 'new_dispatch_or_dispatch_amendment_created':False})

conditions=[
 'Complete modern SupervisorInstanceId captured from genuine host observations; PID/configuration equality is insufficient.',
 'Instance created through the exact approved host-authorized launch mechanism with independent Architect and human/host consent.',
 'Executable, complete implementation inventory and configuration match this amendment-bound qualified requirements and separately approved final applicability.',
 'Runtime UID=1000, GID=1000, supplementary groups=[]; complete real/effective/saved credentials satisfy the qualified identity.',
 'Host-authorized root placement in /sys/fs/cgroup/unified/kge-forge/executor with 0::/kge-forge/executor verified before dropping runtime credentials.',
 'Workspace is /home/gvasend/app/kge-forge with genuine, pinned directory identity.',
 'Socket is /tmp/a21m.sock, UID/GID=1000:1000, mode=0600, genuine filesystem and kernel listener identity bound to this process birth.',
 'Protocol/configuration/environment match the qualified requirements; source identity and fresh observations verify them.',
 'Complete immutable host-launch provenance binds genuine host consent, root parent/start identity, command/spec hashes and placement-before-drop observations.',
 'Predecessor is unavailable with fresh authenticated host evidence and all old work accounted for; another eligibility mode requires its own explicit qualified authority, not mere configuration equivalence.',
 'Exactly one current authority holder; no conflicting process authority, outstanding invocation or execution ownership, competing successor, stale head or branch.',
 'Architect explicitly authorizes this specific predecessor-to-successor event, exact successor ID and qualification, reason and current operational ancestry.',
 'The private append-only SupervisorSuccession event and pinned chain/head validate; replay is non-effecting, missing/reordered/substituted evidence fails closed.',
 'Independent recovery from private authority and journal reconstructs the successor as the unique current holder; fresh readiness and unchanged QUIESCENT checks also pass.'
]
rule={'role':'Execution Supervisor','expression':'CurrentAuthorityHolder = historically released S1, or exactly one explicitly Architect-authorized and qualified successor selected by authenticated SupervisorSuccession; no current ready holder is inferred when evidence is absent.',
 'successor_conditions_all_required':[{'number':i+1,'requirement':v} for i,v in enumerate(conditions)],
 'historical_S1_interpretation':'S1 predates the modern instance schema. It remains the immutable original release anchor. Missing boot/start observations are never manufactured; historical authority does not establish present readiness. S1 is unavailable in the accepted current state. PID reuse, matching configuration or process restart cannot restore S1.',
 'initial_eligible_predecessor_status':'UNAVAILABLE',
 'FENCED_branch':'Candidate contains an explicit-fencing branch; this amendment proposal does not activate an unqualified live-predecessor fencing procedure. Such use needs separately demonstrated qualified fencing and explicit authorization.',
 'configuration_equivalence_confers_authority':False,'host_launch_confers_succession_authority':False,'amendment_confers_specific_S2_or_dispatch_authority':False}
body={'schema':'PD06-SUPERVISOR-AUTHORITY-AMENDMENT-PROPOSAL-1','status':'PROPOSED_NOT_DECIDED_NOT_APPLIED','classification':'MATERIAL_RELEASE_CHANGE',
 'parent_release':{'ReleaseBasisId':g['identities']['ReleaseBasisId'],'ReleaseDecisionId':g['identities']['ReleaseDecisionId'],'release_basis':g['release_basis'],'release_decision':g['release_decision'],'released_profile':g['released_profile'],'released_launch':op['released_launch']},
 'append_only_relationship':'PD-06 Release -> PD-06 Supervisor Authority Amendment; original records unchanged',
 'original_supervisor_rule':'current authority holder = historical S1 process instance','exact_original_supervisor_binding':profile['supervisor_binding'],
 'historical_S1_evidence_identity':hid,'historical_S1_evidence':ref(Q/'HISTORICAL_S1.json'),
 'accepted_succession_qualification':{'closure':ref(Q/'CLOSURE.json'),'capture':closure['qualification'],'schemas':ref(Q/'SCHEMAS.md'),'probes':ref(Q/'PROBE_RESULTS.json'),'tests':{name:ref(Q/name) for name in ('SUCCESSION_FINAL_TESTS.log','KERNEL_OBSERVATION_TEST.log','REGRESSION_TESTS.log')}},
 'required_implementation_identity':impl_id,'required_implementation':implementation_ref,
 'amended_supervisor_authority_rule':rule,'qualified_successor_requirements':{'host_launch_spec_proposal':closure['proposed_host_spec'],'static_requirements':{k:plan[k] for k in ('uid','gid','supplementary_groups','workspace','cgroup','socket','interpreter','interpreter_sha256','argv','environment','protocol_configuration')},'dynamic_identity_values':'Only genuine post-launch observations may fill PID/birth/parent/socket and inode values; exact resulting requirements require approved private selection.'},
 'unchanged_released_authorities':boundary_ref,'released_ModelPayloadDigest':state['identities']['ModelPayloadDigest'],
 'dispatch_assessment':impact_ref,'host_package_assessment':host_ref,
 'current_operational_ancestor':g['identities'],'current_private_catalog_sha256':adoption['selected_store']['catalog_sha256'],
 'architect_amendment_decision':{'status':'PENDING','decision_identity':None,'decision':None,'authority_source':None},
 'publication_gates':['Explicit Architect amendment decision bound to this exact candidate and implementation','Qualified material-release applicability/consumer and private authority selection; never a mislabeled non-material continuation','Explicit dispatch-authority amendment or replacement decision, separately issued','Independent genuine host authorization and final approved launch spec','Observed qualified S2 and specific Architect succession authorization/event','Independent recovery and complete live readiness before any later E1 activation'],
 'no_effects':{'original_PD06_rewritten':False,'amendment_applied':False,'S2_authorized':False,'S2_launched':False,'succession_event_applied':False,'E1_activation':False,'E1_ownership':False,'E1_model_requests':0,'E1_dispatch':False}}
cid='PD06-SUPERVISOR-AUTHORITY-AMENDMENT-sha256:'+digest(body)
proposed_id='E1-RELEASE-AUTHORITY-sha256:'+digest({'ReleaseBasisId':g['identities']['ReleaseBasisId'],'ReleaseDecisionId':g['identities']['ReleaseDecisionId'],'SupervisorAuthorityAmendmentId':cid})
envelope={'body':body,'amendment_candidate_identity':cid,'proposed_release_authority_identity':proposed_id,
 'identity_semantics':'Candidate identity hashes canonical body. Proposed composite hashes original release IDs plus candidate ID. Neither is an issued decision or effective release. A future issued authority must additionally authenticate the separate Architect amendment decision; no effective operational ID is assigned here.'}
candidate_ref=write('PD06_AMENDMENT_CANDIDATE.json',envelope)
write('CANDIDATE_IDENTITY.json',{'amendment_candidate_identity':cid,'candidate_file':candidate_ref,'proposed_release_authority_identity':proposed_id,'implementation_identity':impl_id,'issued_amendment_decision':None,'effective_new_release_authority':None})
write('PROPOSED_S1_TO_S2_BINDING.json',{'schema':'SUPERVISOR-SUCCESSION-PROPOSAL-1','status':'PROPOSAL_ONLY_NOT_AN_EVENT','proposed_amendment':candidate_ref,'proposed_release_authority_identity':proposed_id,
 'predecessor_instance':hid,'predecessor_status':'UNAVAILABLE','sequence':1,'predecessor_event':None,
 'current_ancestor':g['identities'],'current_authorization_id':state['authorization_id'],'released_ModelPayloadDigest':state['identities']['ModelPayloadDigest'],
 'required_implementation_identity':impl_id,'successor_instance':None,'successor_PID':None,'successor_birth':None,'successor_qualification':None,'host_launch':None,'architect_succession_authorization':None,'host_operator_authorization':None,'event_identity':None,
 'effective_amended_operational_context':None,'effective_amended_chain_digest':None,
 'publication_rule':'Fill only from genuine approvals, final qualified material applicability and host observations. Proposal may not be ingested as an event or selection.'})
write('VERIFICATION.json',{'verdict':'NARROW_AMENDMENT_PROPOSAL_READY_FOR_ARCHITECT_REVIEW_APPLICATION_BLOCKED',
 'qualification_inputs_and_blobs_verified':len(manifest['inputs']),'qualified_implementation_exact':'PASS','current_deployed_inventory_unchanged':'PASS','original_profile_and_release_private_content_verified':'PASS',
 'historical_S1_anchor_exact':'PASS','historical_reference_fingerprints_unchanged':716,'original_dispatch_unchanged':state['dispatch_id'],
 'current_state_evidence':ref(Q/'CURRENT_E1_RECONSTRUCTION.json'),'current_state_evidence_use':'Prior independent reconstruction remains applicable: exact adopted code/pin/private release inputs, audit and ledger fingerprints verified unchanged; no new live host observation claimed.',
 'preserved_audit_and_ledger_fingerprints':state['preserved_mutable_fingerprints'],'E1':'INACTIVE','ownership':'NONE','E1_WP_001':'INELIGIBLE_AND_UNDISPATCHED',
 'actual_amendment':None,'actual_S2':None,'actual_succession':None,'new_dispatch_authority':None,'host_command_executed':False,'E1_model_requests':0,'E1_implementation_effects':0})
print(canonical({'candidate':cid,'candidate_sha256':candidate_ref['sha256'],'proposed_release_authority':proposed_id,'implementation_identity':impl_id,'host_files':host}))
