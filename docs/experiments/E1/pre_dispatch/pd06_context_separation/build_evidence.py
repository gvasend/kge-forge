"""Build the non-activating R6 profile and separated context evidence."""
from pathlib import Path
from dataclasses import replace
import hashlib,json,os,shutil,sys,uuid
ROOT=Path('/home/gvasend/app/kge-forge');sys.path.insert(0,str(ROOT))
from adapter.context_binding import CommittedContext
from adapter.context_projection import specification,derive,sha,digest,canonical
from adapter.runnable_profile import authorization
from adapter.governed_host import GovernedHost
from adapter.orchestrator import ReasoningOrchestrator
from adapter.responses_orchestrator import ResponsesReasoning
PRE=ROOT/'docs/experiments/E1/pre_dispatch';OUT=PRE/'pd06_context_separation';ACCEPTED=PRE/'pd06_final_clearance'
def write(name,value):(OUT/name).write_text(json.dumps(value,indent=2)+'\n')
clearance_path=ACCEPTED/'CONTENT_CLEARANCE_MANIFEST.json';clearance=json.loads(clearance_path.read_text())
assert clearance['counts']=={'TRANSMIT':6,'LOCAL_ONLY':120,'NEVER_TRANSMIT':60}
cap=Path(clearance['candidate']['manifest']);snapshot=json.loads(cap.read_text());assert len(snapshot['inputs'])==186
assert sha(cap.read_bytes())==clearance['candidate']['capture_sha256']
for path,row in snapshot['inputs'].items():assert sha((cap.parent/'blobs'/row['sha256']).read_bytes())==row['sha256']
b=CommittedContext(PRE/'CONTEXT_MANIFEST.json','5871bdce4f5b6539c84f69f4f2b2f94ee31be5cd');assert b.verify()
# The original 186-input capture is historical authority. The explicitly authorized
# adapter changes are bound as a current implementation supplement, never concealed.
material={str(p):sha(p.read_bytes()) for p in sorted((ROOT/'adapter').glob('*.py'))}
material[str(OUT/'ARCHITECT_AUTHORITY.md')]=sha((OUT/'ARCHITECT_AUTHORITY.md').read_bytes())
spec=specification(b,cap,clearance_path,PRE/'E1-WP-001.md',material)
projection=derive(spec,b)
write('CONTEXT_BINDING.json',spec);write('MODEL_CONTEXT_PROJECTION.json',projection['projection'])
write('AUTHORITATIVE_CONTROLLER_CONTEXT.json',projection['controller_context'])
write('CONTEXT_IDENTITIES.json',{k:projection[k] for k in ('AuthoritativeContextId','FullContextDigest','ModelProjectionDigest')})
policy=json.loads((ACCEPTED/'PRODUCTION_PROFILE.json').read_text())['model_transmission']
policy['initial_clearances']=[{'sha256':digest(projection['projection']['payload']),
 'category':'cleared-reasoning-context','authority_source':str(OUT/'ARCHITECT_AUTHORITY.md'),
 'task_sha256':sha(projection['projection']['payload']['task'].encode()),
 'ModelProjectionDigest':projection['ModelProjectionDigest']}]
policy['private_paths']=list(policy['private_paths'])+[str(OUT)]
policy['clearance_manifest_file_sha256']=sha(clearance_path.read_bytes())
profile=json.loads((ACCEPTED/'PRODUCTION_PROFILE.json').read_text())
profile['schema']='E1-PRODUCTION-PROFILE-6';profile['revision']=6
profile['model_transmission']=policy;profile['context_projection']=spec
profile['production_context_sha256']=digest(projection['projection']['payload']['context'])
profile['production_task_sha256']=sha(projection['projection']['payload']['task'].encode())
profile['release_preconditions']=[]
profile['qualification_state']='PASS: accepted PD05 mechanism plus scoped context/projection qualification'
profile['architect_status']['PD-06']='UNRELEASED / reserved Architect decision'
profile['authority_sources']['current_supplement']='pd06_context_separation/ARCHITECT_AUTHORITY.md'
profile['identity']['authorization']='auth-e1-wp-001-r6-<controller UUID4>'
ids={'authorization':'auth-e1-wp-001-r6-'+uuid.uuid4().hex,'session':'session-e1-'+uuid.uuid4().hex,'turn':'turn-e1-'+uuid.uuid4().hex}
profile['identity']['allocated']=ids
profile['field_attribution'].update({
 'context_projection':{'classification':'Architect-authorized deterministic derivation','source':'accepted 186-input clearance + ARCHITECT_AUTHORITY.md'},
 'model_transmission':{'classification':'accepted clearance, narrowed binding','source':'unchanged six-source manifest; deterministic initial payload'},
 'release_preconditions':{'classification':'no unresolved selection; final decision reserved','source':'scoped qualification and independent verification'},
 'production_context_sha256':{'classification':'derived','source':'MODEL_CONTEXT_PROJECTION.json'},
 'production_task_sha256':{'classification':'unchanged captured task','source':'accepted clearance'},
 'identity':{'classification':'controller allocation under accepted UUID rules','source':'accepted launch configuration'}})
profile_hash=digest(profile);write('PRODUCTION_PROFILE.json',profile)
auth=authorization(b,b,ids['authorization'],6,ids['session'],ids['turn'])
auth=replace(auth,model_transmission=canonical(policy),context_projection=canonical(spec));assert auth.state=='INACTIVE'
audit=Path('/tmp/kge-forge-e1-evidence')/ids['authorization']/ids['session']/ids['turn']/'controller.jsonl'
audit.parent.mkdir(parents=True,exist_ok=False)
parent=audit.parent
while parent!=Path('/tmp'):
 assert not parent.is_symlink();parent.chmod(0o700);parent=parent.parent
host=GovernedHost(auth,audit);runner=ResponsesReasoning(ReasoningOrchestrator(host))
actual=runner._verify_context();assert actual==projection['projection']['payload']
runner.transmission.initial(actual['task'],actual['context'])
try:runner.run(actual['task'],actual['context'],1)
except ValueError as e:assert str(e)=='Programmer authorization not released'
else:raise AssertionError('inactive E1 ran')
assert host.scope is None and not host.invocations
raw=dict(auth.__dict__);raw['context_binding']={'capture_commit':b.capture_commit,'context_sha256':b.digest}
oldlaunch=json.loads((ACCEPTED/'PRODUCTION_LAUNCH_RECORD.json').read_text())
launch=dict(oldlaunch);launch.update({'schema':'E1-PRODUCTION-LAUNCH-PROPOSAL-6','authorization':raw,
 'profile_sha256':profile_hash,'audit_destination':str(audit),'identity':profile['identity'],
 'model_transmission':policy,'context_projection':spec,'production_task_sha256':profile['production_task_sha256'],
 'production_context_sha256':profile['production_context_sha256'],
 'launch_compatibility':'PASS for deterministic selected context; E1 remains INACTIVE',
 'QUALIFIED':True,'RELEASED':False,'ELIGIBLE':False,'DISPATCHED':False})
write('PRODUCTION_LAUNCH_RECORD.json',launch)
for src,name in [('/tmp/pd06-separation-qualified-bound-20260916','synthetic'),('/tmp/pd06-separation-live-bound-20260916','live')]:
 shutil.copytree(src,OUT/name)
shutil.copyfile('/tmp/pd06-separation-tests-bound.txt',OUT/'focused_tests.txt')
assert json.loads((OUT/'synthetic/REPORT.json').read_text())['result']=='PASS'
assert json.loads((OUT/'live/LIVE_REPORT.json').read_text())['result']=='PASS'
assert (OUT/'focused_tests.txt').read_text().rstrip().endswith('OK')
source={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in sorted((ROOT/'adapter').rglob('*.py'))}
write('SOURCE_SHA256.json',source)
drift=[]
for path,row in snapshot['inputs'].items():
 now=sha(Path(path).read_bytes())
 if now!=row['sha256']:
  assert path.startswith(str(ROOT/'adapter')) or path=='/tmp/a21m.sock.supervisor-audit.jsonl',path
  drift.append({'path':path,'historical_sha256':row['sha256'],'current_sha256':now,
    'authority':'Current Architect context-separation/qualification instruction; historical capture remains unchanged'})
write('IMPLEMENTATION_SUPPLEMENT.json',{'authorized_differences_from_186_capture':drift,
 'new_runtime_module':'adapter/context_projection.py','new_qualification':'adapter/tests/test_context_projection.py',
 'historical_186_blobs_verified':True,'accepted_clearance_unchanged':True,'current_material_inputs':material})
write('PROFILE_FINGERPRINT.json',{'sha256':profile_hash,'definition':'SHA256 of canonical compact sorted-key JSON'})
print(json.dumps({'profile_sha256':profile_hash,**{k:projection[k] for k in ('AuthoritativeContextId','FullContextDigest','ModelProjectionDigest')}}))
