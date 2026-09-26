"""Non-effecting proposal/evidence construction. Never imports candidate code."""
from pathlib import Path
import ast,difflib,hashlib,json,os
ROOT=Path(__file__).resolve().parents[5]
OUT=Path(__file__).resolve().parent
PRE=OUT.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
canonical=lambda v:json.dumps(v,sort_keys=True,separators=(',',':'))
def load(p):return json.loads(Path(p).read_bytes())
def ref(p):return {'path':str(p),'sha256':sha(Path(p).read_bytes())}
def write(name,value):(OUT/name).write_text(canonical(value)+'\n')
def sealed(kind,v):return {**v,'id':kind+'-sha256:'+sha(canonical(v).encode())}
pin=Path('/tmp/kge-forge-controller-authority/auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39/adoption-2026-09-17/ADOPTION_RECORD.json')
assert sha(pin.read_bytes())=='420b41640db490b2fc33500cd02ffc52a55245c8b7c730b307a513502d2efa77'
adopted=load(pin);store=Path(adopted['selected_store']['root']);catalog=load(store/'catalog.json')
assert sha((store/'catalog.json').read_bytes())==adopted['selected_store']['catalog_sha256']
def private(identity):
    h=catalog['objects'][identity]['sha256'];b=(store/h).read_bytes();assert sha(b)==h
    return json.loads(b)
op=private(adopted['identities']['OperationalContextId']);g=op['governance'];profile=private('sha256:'+g['released_profile']['sha256'])
basis=private(g['identities']['ReleaseBasisId']);inputs=basis['current_inputs']
sources=[]
for rel in ('pd05_final_evidence/HOST_RECEIPT.json','pd06_release_evidence/execution/HOST_RECEIPT.json'):
    p=PRE/rel;h=inputs[str(p)]['sha256'];receipt=private('sha256:'+h)
    assert receipt['supervisor']==profile['supervisor_binding'];sources.append({'evidence_path':str(p),'sha256':h,'private_identity':'sha256:'+h})
p=PRE/'A2_LIVE_RECOVERY_AND_READINESS_2026-09-15.md';h=inputs[str(p)]['sha256']
assert sha((store/h).read_bytes())==h
sources.append({'evidence_path':str(p),'sha256':h,'private_identity':'sha256:'+h})
history=sealed('SupervisorHistoricalInstance',{'schema':'SUPERVISOR-HISTORICAL-INSTANCE-1',
    'released_supervisor':profile['supervisor_binding'][0],
    'released_profile_bytes_sha256':g['released_profile']['sha256'],
    'released_profile_canonical_fingerprint':sha(canonical(profile).encode()),
    'release_identities':{k:g['identities'][k] for k in ('ReleaseBasisId','ReleaseDecisionId')},
    'evidence':sources,'known_additional_facts':{'gid':1000,'socket_path':'/tmp/a21m.sock','socket_uid':1000,'socket_gid':1000,'socket_mode':0o600},
    'missing_instance_observations':['boot_id','process_start_ticks','parent_start_ticks','PID_namespace_inode','socket_filesystem_inode','socket_listener_inode','root_launch_command_receipt'],
    'identity_kind':'IMMUTABLE_HISTORICAL_EVIDENCE_ANCHOR_NOT_COMPLETE_PROCESS_BIRTH_IDENTITY',
    'availability_authority':'Architect current instruction: Released supervisor S1 unavailable',
    'live_reinterpretation_forbidden':True})
write('HISTORICAL_S1.json',history)
before=load(OUT/'IMPLEMENTATION_BEFORE.json')
assert before=={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in (ROOT/'adapter').rglob('*.py')}
candidate={str(p.relative_to(OUT/'candidate')):sha(p.read_bytes()) for p in (OUT/'candidate/adapter').rglob('*.py')}
delta=[];patch=[]
for rel in sorted(set(before)|set(candidate)):
    if before.get(rel)==candidate.get(rel):continue
    p=OUT/'candidate'/rel;old=(ROOT/rel).read_text() if (ROOT/rel).exists() else ''
    new=p.read_text() if p.exists() else ''
    delta.append({'path':str(ROOT/rel),'candidate_path':str(p),'old_sha256':before.get(rel),'new_sha256':candidate.get(rel),
                  'category':'QUALIFICATION_TEST' if '/tests/' in rel else 'PRODUCTION'})
    patch.extend(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='a/'+rel,tofile='b/'+rel))
(OUT/'EXACT_CANDIDATE_DELTA.patch').write_text(''.join(patch))
delta.append({'path':'/var/lib/kge-forge-supervisor-succession/host_launch.py','candidate_path':str(OUT/'host_launch.py'),'old_sha256':None,'new_sha256':sha((OUT/'host_launch.py').read_bytes()),'category':'HOST_LAUNCH_PROCEDURE'})
ast.parse((OUT/'host_launch.py').read_bytes())
write('IMPLEMENTATION_DELTA.json',{'classification':'MATERIAL_RELEASE_CHANGE','applied':False,'delta':delta,
    'reason':'Replaces exact released S1-only readiness with authority to select a different process through a new succession trust root. Preserving profile bytes does not preserve the old execution-authority selection semantics.',
    'OPERATIONAL_CONTINUATION_1':None,'non_material_record_not_constructed':'Only non-material continuation types exist in the current canonical mechanism. A material transition must not be mislabeled to pass it.',
    'current_production_inventory_unchanged':True})
for p in (OUT/'candidate/adapter').rglob('*.py'):ast.parse(p.read_bytes())
# Verify transaction and all non-selection host checks are byte/AST unchanged.
old=ast.parse((ROOT/'adapter/activation_transaction.py').read_bytes());new=ast.parse((OUT/'candidate/adapter/activation_transaction.py').read_bytes())
def item(tree,name):return ast.dump(next(n for n in tree.body if getattr(n,'name',None)==name))
for name in ('_host','ActivationTransaction','invocation','execution_guard','_lease'):assert item(old,name)==item(new,name)
write('INVARIANT_PRESERVATION.json',{'result':'PASS','unchanged_AST':['ActivationTransaction','_host','invocation','execution_guard','_lease'],
    'unchanged_source_modules':[x for x,h in before.items() if '/tests/' not in x and candidate.get(x)==h],
    'historical_adoption_pin':ref(pin),'real_E1_reconstruction':ref(OUT/'CURRENT_E1_RECONSTRUCTION.json')})
app=adopted['selected_store']['applicability']
binding={**app,'released_profile_content_sha256':sha(canonical(profile).encode()),
    'execution_profile_sha256':sha(private(app['authorization_id'])['execution_profile'].encode()),
    'authority_store_epoch_sha256':sha(canonical(app).encode())}
implementation={str(ROOT/rel):h for rel,h in candidate.items() if '/tests/' not in rel}
env={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','PYTHONDONTWRITEBYTECODE':'1','PYTHONPYCACHEPREFIX':'/var/cache/kge-forge-supervisor-succession/S2'}
config={'protocol_version':1,'socket_path':'/tmp/a21m.sock','cgroup_path':'/sys/fs/cgroup/unified/kge-forge/executor',
    'environment':env,'qualified_constants':{'termination_seconds':5,'grace_seconds':0.5,'poll_seconds':0.05,'supervisor_first_receipt_wait_seconds':10,'first_receipt_max_bytes':65536},
    'contract':'Existing owner-bound A2.1 supervisor wire protocol, governed admission barrier and authoritative QUIESCENT; no protocol implementation changes.'}
plan={'schema':'SUPERVISOR-HOST-LAUNCH-SPEC-1','status':'PROPOSED_NOT_AUTHORIZED','predecessor_id':history['id'],
    'runtime_binding':binding,'applicability_note':'Current accepted context is the proposal ancestor. Material applicability must be resolved and this exact plan requalified/pinned if the effective context changes before launch.',
    'uid':1000,'gid':1000,'supplementary_groups':[],'workspace':str(ROOT),
    'cgroup':'/sys/fs/cgroup/unified/kge-forge/executor','socket':'/tmp/a21m.sock',
    'interpreter':profile['supervisor_binding'][0]['exe'],'interpreter_sha256':profile['supervisor_binding'][0]['exe_sha256'],
    'argv':['/usr/bin/python','-m','adapter.supervisor_server','/tmp/a21m.sock'],
    'environment':env,'implementation':implementation,'protocol_configuration':config,
    'prelaunch_supervisor_audit_sha256':None,'host_launcher':ref(OUT/'host_launch.py'),
    'missing_before_executable_plan':['Genuine Architect and host launch authorization','Approved material implementation applicability','Fresh root-observed predecessor/socket/cgroup/recovery-audit evidence and audit hash']}
write('PROPOSED_HOST_LAUNCH_SPEC.json',plan)
proposal={'schema':'SUPERVISOR-SUCCESSION-PROPOSAL-1','status':'NOT_AUTHORIZED_NOT_AN_EVENT',
    'predecessor_instance':history['id'],'predecessor_status':'UNAVAILABLE','predecessor_identity_kind':history['identity_kind'],
    'reason':'Historical released S1 is unavailable. Propose separately authorized qualified successor; never reinterpret S2 as S1.',
    'sequence':1,'predecessor_event':None,'successor_instance':None,'architect_authorization':None,'host_launch':None,'qualification':None,'predecessor_evidence':None,
    'current_OperationalContextId':app['OperationalContextId'],'continuation_chain_digest':app['continuation_chain_digest'],
    'runtime_binding':binding,'predecessor_private_catalog_sha256':adopted['selected_store']['catalog_sha256'],
    'proposed_policy_role':app['authorization_id']+':supervisor-succession',
    'proposed_ledger_role':app['authorization_id']+':supervisor-succession-events',
    'proposed_private_ledger_location':str(store.parent/'supervisor-succession.jsonl'),
    'event_id':None,'required_authorization':'Architect must explicitly accept the material readiness change and historical-evidence anchor rule, then authorize host launch; exact observed S2 and event require authenticated authorization before catalog selection.',
    'post_launch_order':['Capture root launch and fresh independent instance observations','Canonicalize exact immutable S2 instance and qualification objects','Obtain Architect authorization binding exact event body and S2 identity','Import exact authorized objects into a newly pinned private catalog','Append authorized event under ledger lock','Select approved head pin; restart reconstruction before readiness','No E1 activation implied by any succession step'],
    'guards':['No real ledger created during qualification','No host launch performed','No S2 PID or birth identity invented','No Architect succession authorization invented']}
write('PROPOSED_S1_TO_S2.json',proposal)
print(canonical({'historical_S1_evidence_id':history['id'],'production_delta_count':sum(r['category']=='PRODUCTION' for r in delta),'classification':'MATERIAL_RELEASE_CHANGE','real_E1_unchanged':True}))
