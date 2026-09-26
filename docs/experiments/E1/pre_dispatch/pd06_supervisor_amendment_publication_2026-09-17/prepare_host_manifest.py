"""Documentary, non-executable host proposal. Never installs or launches."""
import json,hashlib
from pathlib import Path
OUT=Path(__file__).resolve().parent;F=OUT.parent/'supervisor_succession_2026-09-17'
def load(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def write(n,v):
 with (OUT/n).open('x') as f:json.dump(v,f,sort_keys=True,separators=(',',':'))
q=load(OUT/'CONSUMPTION_QUALIFICATION.json');op=load(OUT/'OPERATIONAL_BINDING.json');app=load(OUT/'PREPARED_STORE.json')['applicability']
frozen=load(F/'PROPOSED_HOST_LAUNCH_SPEC.json');proposal=json.loads(json.dumps(frozen))
proposal['implementation']=q['implementation']['current']
proposal['runtime_binding'].update(app)
proposal['runtime_binding']['authority_store_epoch_sha256']=digest(app)
proposal['applicability_note']='Proposed applicability after the authorized material amendment. Host launch and genuine successor acceptance remain separately unauthorized.'
proposal['missing_before_executable_plan']=['Architect pre-launch authorization of exact finalized bytes and consumption applicability',
 'Jerry explicit attributable host launch authorization and any verified stale socket removal',
 'Fresh host observations, recovery audit hash, then exact final plan and authorization fingerprints']
assert proposal['status']=='PROPOSED_NOT_AUTHORIZED' and proposal['prelaunch_supervisor_audit_sha256'] is None
write('PROPOSED_LAUNCH_SPEC.json',proposal)
auth={'authority':'Architect','decision':None,'authorization_id':None,'qualification_acceptance_id':None,
 'predecessor_id':proposal['predecessor_id'],'runtime_binding':proposal['runtime_binding'],
 'launch_spec_sha256':None,'launcher_sha256':sha(F/'host_launch.py'),
 'host_operator_authorization_id':None,'remove_verified_stale_socket':False,
 'status':'PROPOSED_NOT_AUTHORIZED','successor_instance_id':None,
 'note':'Nulls are deliberate. This amendment publication supplies neither launch consent nor specific succession authorization.'}
write('PROPOSED_HOST_LAUNCH_AUTHORIZATION.json',auth)
write('HOST_AUTHORIZATION_BOUNDARIES.json',{
 'protocol':'Separate pre-launch permission and post-launch exact identity acceptance. A launch permission never selects S2.',
 'Architect_prelaunch_fields':{'authority':'Architect','decision':'AUTHORIZE_HOST_SUPERVISOR_LAUNCH (not yet issued)',
  'authorization_id':'new attributable Architect launch decision identity, not fabricated',
  'qualification_acceptance_id':'explicit acceptance of consumption implementation '+q['implementation_identity'],
  'predecessor_id':proposal['predecessor_id'],'runtime_binding':proposal['runtime_binding'],
  'launch_spec_sha256':'exact final root-observation-completed AUTHORIZED_FOR_HOST_LAUNCH plan; currently unset',
  'launcher_sha256':sha(F/'host_launch.py')},
 'Jerry_host_fields':{'operator':'Jerry','authority':'HOST_OPERATOR','decision':'AUTHORIZE_HOST_SUPERVISOR_LAUNCH',
  'authorization_id':'genuine Jerry consent ID, copied to host_operator_authorization_id in wrapper input',
  'authority_source':'private content ID of Jerry explicit authorization; not Architect attribution',
  'predecessor_id':proposal['predecessor_id'],'runtime_binding':proposal['runtime_binding'],
  'launch_spec_sha256':'exact final plan hash','launcher_sha256':sha(F/'host_launch.py'),
  'command':'sudo /usr/bin/python3.11 /var/lib/kge-forge-supervisor-succession/host_launch.py /var/lib/kge-forge-supervisor-succession/LAUNCH_SPEC.json /var/lib/kge-forge-supervisor-succession/HOST_LAUNCH_AUTHORIZATION.json',
  'scope':['root-owned package installation','root child placement in delegated cgroup before credential drop','runtime UID/GID 1000:1000 groups []','one host launch; no succession/activation authority'],
  'remove_verified_stale_socket':'separate explicit Jerry consent for deletion only after root verifies no listener; defaults false'},
 'postlaunch_Architect_specific_acceptance':{'schema':'SUPERVISOR-SUCCESSION-AUTHORIZATION-1','authority':'Architect',
  'decision':'AUTHORIZE_SUPERVISOR_SUCCESSION','event_body_sha256':'binds exact genuinely observed successor, predecessor evidence, qualification, host receipt, runtime ancestry and event order',
  'reason':'explicitly authorized succession reason','predecessor_instance':proposal['predecessor_id'],
  'host_authorization':'private logical ID of genuine Jerry grant','launch_spec_sha256':'exact launched plan hash','launcher_sha256':sha(F/'host_launch.py'),
  'successor_instance_id':None,'authorization_identity':None},
 'host_wrapper_limitation':'The frozen root wrapper checks nonempty authorization IDs and exact plan/launcher hashes, not cryptographic signatures. Root operator must authenticate both attributable decisions before staging. Controller consumption additionally checks the private Jerry grant and host receipt binding.',
 'all_launch_authorizations_issued':False})
write('PROPOSED_S1_TO_S2_BINDING.json',{'predecessor_instance':proposal['predecessor_id'],'successor_instance':None,
 'release_authority':load(OUT/'PD06_AMENDMENT_DECISION.json')['resulting_release_authority'],
 'dispatch_amendment':load(OUT/'ARCHITECT_DISPATCH_AMENDMENT.json')['id'],
 'runtime_binding':proposal['runtime_binding'],'specific_Architect_succession_authorization':None,
 'host_authorization':None,'host_launch':None,'successor_qualification':None,'succession_event':None,'current_holder_selected':False})
entries=[]
for src,dst,role in [(F/'host_launch.py','host_launch.py','frozen qualified executable; installation only after host consent'),
 (OUT/'PROPOSED_LAUNCH_SPEC.json','LAUNCH_SPEC.json','proposal only; final approved hash requires fresh observations and consent'),
 (OUT/'PROPOSED_HOST_LAUNCH_AUTHORIZATION.json','HOST_LAUNCH_AUTHORIZATION.json','unapproved template; never install as authority')]:
 entries.append({'source':str(src),'source_sha256':sha(src),'destination':'/var/lib/kge-forge-supervisor-succession/'+dst,
                 'owner':'root','group':'root','mode':'0600','role':role,
                 'authorized_install_sha256':sha(src) if dst=='host_launch.py' else None})
write('HOST_INSTALLATION_MANIFEST.json',{'schema':'PROPOSED-HOST-INSTALLATION-MANIFEST-1','status':'NOT_INSTALLED_NOT_AUTHORIZED',
 'target_directory_exists':Path('/var/lib/kge-forge-supervisor-succession').exists(),
 'frozen_package':{'launcher_sha256':sha(F/'host_launch.py'),'frozen_launch_proposal_sha256':sha(F/'PROPOSED_HOST_LAUNCH_SPEC.json'),
 'accepted_succession_implementation':q['accepted_succession_implementation'],'qualified_consumption_implementation':q['implementation_identity']},
 'entries':entries,'directories':[{'path':'/var/lib/kge-forge-supervisor-succession','owner':'root:root','mode':'0700'},
 {'path':'/var/cache/kge-forge-supervisor-succession/S2','owner':'root:root','mode':'0755','must_be_empty':True}],
 'final_plan_and_authorization_hashes':'Intentionally unset until actual separate authorizations and fresh host observations exist.'})
print('Documentary host proposal and installation manifest prepared; nothing installed or launched.')
