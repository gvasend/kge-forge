"""Record the actual Architect attempt grant; prepare reviewable host inputs.
No host consent, installation, launch, retry, succession or E1 transition.
"""
from pathlib import Path
import json,os,hashlib
from adapter.controller_authority_store import _directory,_put,outside,encoded
OUT=Path(__file__).resolve().parent;Q=OUT.parent/'pd06_supervisor_amendment_publication_2026-09-17_final'
load=lambda p:json.loads(p.read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
def ref(p):return {'path':str(p),'sha256':sha(p.read_bytes())}
def write(name,value):
 data=encoded(value)
 with (OUT/name).open('xb') as f:f.write(data)
 return data
plan=load(Q/'PROPOSED_LAUNCH_SPEC.json');verified=load(OUT/'PACKAGE_VERIFICATION.json')
assert verified['frozen_package_hashes']=='PASS'
audit=Path('/tmp/a21m.sock.supervisor-audit.jsonl');assert not audit.is_symlink()
audit_bytes=audit.read_bytes();assert sha(audit_bytes)==verified['observations']['supervisor_audit_sha256']
for line in audit_bytes.splitlines():json.loads(line)
final=dict(plan);final['status']='AUTHORIZED_FOR_HOST_LAUNCH';final['prelaunch_supervisor_audit_sha256']=sha(audit_bytes)
assert {k for k in final if final[k]!=plan[k]}=={'status','prelaunch_supervisor_audit_sha256'}
plan_bytes=write('LAUNCH_SPEC.json',final)
body={'schema':'SUPERVISOR-SUCCESSION-ATTEMPT-AUTHORIZATION-1','authority':'Architect',
 'decision':'AUTHORIZE_ONE_CANDIDATE_SUPERVISOR_LAUNCH_ATTEMPT',
 'attribution':{'channel':'user','title':'ARCHITECT SUPERVISOR SUCCESSION-ATTEMPT AUTHORIZATION',
  'quote':'Architect decision: one candidate-S2 succession launch attempt AUTHORIZED, contingent on separate attributable human/host authorization.'},
 'predecessor_id':plan['predecessor_id'],
 'material_amendment':'PD06-SUPERVISOR-AUTHORITY-AMENDMENT-sha256:979201e9e2d4269a483ce904ae4e7f9329ab0378836e7ada59070b3e4636d3b6',
 'release_authority':'E1-RELEASE-AUTHORITY-sha256:c0d6aed0894c9d07945b017423b3bb2fedb7207780b5e3d4e6c928aacb82bae3',
 'dispatch_amendment':'ARCHITECT-DISPATCH-AMENDMENT-sha256:3f29a0c359e626b5fe532af6c9fd06218d33bb9644a4906a2214dbf655d67a31',
 'runtime_binding':plan['runtime_binding'],
 'qualified_package':[ref(Q/n) for n in ('HOST_INSTALLATION_MANIFEST.json','HOST_INSTALLATION_PROCEDURE.md','PROPOSED_LAUNCH_SPEC.json','HOST_AUTHORIZATION_BOUNDARIES.json')],
 'qualified_consumption_implementation':load(Q/'CONSUMPTION_QUALIFICATION.json')['implementation_identity'],
 'launcher_sha256':plan['host_launcher']['sha256'],'finalized_launch_spec_sha256':sha(plan_bytes),
 'finalization':{'changed_fields':['status','prelaunch_supervisor_audit_sha256'],
  'basis':'Only the finalization explicitly prescribed by the approved HOST_INSTALLATION_PROCEDURE; every other proposed field is unchanged.',
  'audit_observation':'Exact bytes read without privilege; host operator must independently confirm this hash and all host prerequisites before launch. A mismatch invalidates this plan for launch.'},
 'maximum_launch_attempts':1,'automatic_retry_permitted':False,'substitute_plan_permitted':False,
 'human_host_authorization_required':True,'human_host_authorization':None,
 'candidate_only':True,'successor_instance_id':None,'specific_succession_authorization':None,
 'prohibited':['E1 activation','E1 ownership','E1 model request','E1-WP-001 execution or dispatch','arbitrary privileged host operations','second attempt','SupervisorSuccession commit','released supervisor rule modification'],
 'failure_action':'Preserve evidence, do not retry or broaden authority, leave readiness unresolved, return to Architect.'}
identity='SupervisorSuccessionAttemptAuthorization-sha256:'+sha(encoded(body))
authority=write('ARCHITECT_ATTEMPT_AUTHORIZATION.json',{**body,'authorization_id':identity})
pending={'authority':'Architect','decision':'AUTHORIZE_HOST_SUPERVISOR_LAUNCH','authorization_id':identity,
 'qualification_acceptance_id':identity,'predecessor_id':plan['predecessor_id'],
 'runtime_binding':plan['runtime_binding'],'launch_spec_sha256':sha(plan_bytes),'launcher_sha256':plan['host_launcher']['sha256'],
 'host_operator_authorization_id':None,'remove_verified_stale_socket':False}
write('HOST_LAUNCH_AUTHORIZATION.PENDING.json',pending)
manifest={'schema':'CANDIDATE-S2-ATTEMPT-INSTALLATION-MANIFEST-1','status':'WAITING_FOR_JERRY_HOST_AUTHORIZATION',
 'Architect_attempt_authorization':identity,'launch_spec_sha256':sha(plan_bytes),
 'launcher_sha256':plan['host_launcher']['sha256'],
 'entries':[{'source':plan['host_launcher']['path'],'sha256':plan['host_launcher']['sha256'],
  'destination':'/var/lib/kge-forge-supervisor-succession/host_launch.py','owner':'root:root','mode':'0600'},
 {'source':str(OUT/'LAUNCH_SPEC.json'),'sha256':sha(plan_bytes),'destination':'/var/lib/kge-forge-supervisor-succession/LAUNCH_SPEC.json','owner':'root:root','mode':'0600'},
 {'source':None,'sha256':None,'pending_template':ref(OUT/'HOST_LAUNCH_AUTHORIZATION.PENDING.json'),
  'destination':'/var/lib/kge-forge-supervisor-succession/HOST_LAUNCH_AUTHORIZATION.json','owner':'root:root','mode':'0600',
  'completion':'Only after genuine Jerry consent, insert its attributable authorization identity and explicitly authorized stale-socket choice. Record completed exact bytes/hash; do not install the pending template.'}],
 'command':'sudo /usr/bin/python3.11 /var/lib/kge-forge-supervisor-succession/host_launch.py /var/lib/kge-forge-supervisor-succession/LAUNCH_SPEC.json /var/lib/kge-forge-supervisor-succession/HOST_LAUNCH_AUTHORIZATION.json',
 'qualified_procedure':ref(Q/'HOST_INSTALLATION_PROCEDURE.md'),'attempts_consumed':0}
write('INSTALLATION_MANIFEST.json',manifest)
# Controller-private recording, separate from the selected operational catalog.
# This grants neither host consent nor a current supervisor role.
selection=load(Q/'PREPARED_STORE.json');catalog=load(Path(selection['root'])/'catalog.json')
assert sha(encoded(catalog))==selection['catalog_sha256']
private=Path(selection['root']).parent/'candidate-s2-attempt-2026-09-17'
outside(private,catalog['programmer_roots']);private.mkdir(mode=0o700);fd=_directory(private)
try:
 for name,data in [('ARCHITECT_ATTEMPT_AUTHORIZATION.json',authority),('LAUNCH_SPEC.json',plan_bytes),('OBSERVED_SUPERVISOR_AUDIT.jsonl',audit_bytes)]:_put(fd,name,data)
 os.fsync(fd)
finally:os.close(fd)
fd=_directory(private.parent)
try:os.fsync(fd)
finally:os.close(fd)
write('PRIVATE_ATTEMPT_RECEIPT.json',{'path':str(private/'ARCHITECT_ATTEMPT_AUTHORIZATION.json'),
 'sha256':sha(authority),'authorization_id':identity,'status':'ARCHITECT_AUTHORIZED_HOST_CONSENT_PENDING',
 'operational_catalog_changed':False,'launch_attempts_consumed':0})
print(json.dumps({'authorization_id':identity,'launch_spec_sha256':sha(plan_bytes),'private_record':str(private),'host_consent':None,'attempts_consumed':0}))
