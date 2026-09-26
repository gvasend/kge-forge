"""Independent PD06 verifier and non-activating content-addressed capture writer."""
from pathlib import Path
from dataclasses import replace
import hashlib,json,os,subprocess,sys
ROOT=Path('/home/gvasend/app/kge-forge');sys.path.insert(0,str(ROOT))
from adapter.context_binding import CommittedContext
from adapter.context_projection import canonical,sha,digest
from adapter.runnable_profile import validate,ARGV,INPUTS
from adapter.model_transport import validate as validate_transport
from adapter.directory_provisioning import open_directory,SOURCE
from adapter.launch_profile import provisioning,LEDGER
from adapter.invocation_ownership import InvocationOwnership
from adapter.recovery_ledger import _observe,CGROUP_BASE,SUPERVISOR_AUDIT
from adapter.governed_host import WorkAuthorization,GovernedHost
from adapter.orchestrator import ReasoningOrchestrator
from adapter.responses_orchestrator import ResponsesReasoning
PRE=ROOT/'docs/experiments/E1/pre_dispatch';OUT=PRE/'pd06_context_separation';ACCEPTED=PRE/'pd06_final_clearance'
def read(name):return json.loads((OUT/name).read_text())
def write(name,value):(OUT/name).write_text(json.dumps(value,indent=2)+'\n')
spec=read('CONTEXT_BINDING.json');projection=read('MODEL_CONTEXT_PROJECTION.json')
full=read('AUTHORITATIVE_CONTROLLER_CONTEXT.json');ids=read('CONTEXT_IDENTITIES.json')
clearance_bytes=(ACCEPTED/'CONTENT_CLEARANCE_MANIFEST.json').read_bytes();clearance=json.loads(clearance_bytes)
assert sha(clearance_bytes)==spec['clearance_sha256']
prior=Path(clearance['candidate']['manifest']);capture=json.loads(prior.read_text());blobs=prior.parent/'blobs'
assert sha(prior.read_bytes())==spec['capture_sha256']==clearance['candidate']['capture_sha256']
assert len(capture['inputs'])==186 and len(clearance['inputs'])==186
assert {r['canonical_path'] for r in clearance['inputs']}==set(capture['inputs'])
assert clearance['counts']=={'TRANSMIT':6,'LOCAL_ONLY':120,'NEVER_TRANSMIT':60}
assert all(r['classification'] in ('TRANSMIT','LOCAL_ONLY','NEVER_TRANSMIT') for r in clearance['inputs'])
for path,row in capture['inputs'].items():assert sha((blobs/row['sha256']).read_bytes())==row['sha256']
b=CommittedContext(PRE/'CONTEXT_MANIFEST.json','5871bdce4f5b6539c84f69f4f2b2f94ee31be5cd');assert b.verify()
assert full['controller_context']==b.model_context() and full['committed_context_sha256']==b.digest
assert full['committed_capture']==b.capture_commit and full['capture_sha256']==spec['capture_sha256']
assert full['clearance_sha256']==spec['clearance_sha256']
assert full['current_inputs']==spec['current_inputs']
for path,expected in full['current_inputs'].items():assert sha(Path(path).read_bytes())==expected
assert digest(full)==ids['FullContextDigest']==spec['FullContextDigest']
assert ids['AuthoritativeContextId']=='E1-AUTHORITATIVE-CONTEXT-sha256:'+digest(full)
assert ids['AuthoritativeContextId']==projection['authoritative_context_id']==spec['AuthoritativeContextId']
assert digest(projection)==ids['ModelProjectionDigest']==spec['ModelProjectionDigest']
assert projection['capture_sha256']==spec['capture_sha256'] and projection['clearance_sha256']==spec['clearance_sha256']
# Independent range reconstruction, without using derive().
expected_context={'schema':'E1-CLEARED-CONTEXT-1','sources':[]};expected_proofs=[];expected_task=None
for index,row in enumerate(clearance['inputs']):
 assert row['captured_sha256']==capture['inputs'][row['canonical_path']]['sha256']
 if row['classification']!='TRANSMIT':continue
 data=(blobs/row['captured_sha256']).read_bytes()
 assert data==Path(row['canonical_path']).read_bytes()
 selections=[]
 for span in row['spans']:
  part=data[span['start_byte']:span['end_byte_exclusive']];assert sha(part)==span['sha256']
  selections.append({'label':span['label'],'content':part.decode()})
 expected_proofs.append({'authoritative_source_identity':row['source_identity'],'path':row['canonical_path'],
  'captured_source_sha256':row['captured_sha256'],'clearance_entry':index,'clearance_entry_sha256':digest(row),
  'ranges':row['spans'],'projection_content_sha256':digest(selections)})
 if row['canonical_path']==spec['task_path']:
  assert row['designation']=='COMPLETE_FILE' and row['spans'][0]['start_byte']==0 and row['spans'][0]['end_byte_exclusive']==len(data)
  expected_task=data.decode()
 else:expected_context['sources'].append({'source':row['canonical_path'],'selections':selections})
assert len(expected_proofs)==6 and projection['items']==expected_proofs
assert projection['payload']=={'task':expected_task,'context':expected_context}
profile=read('PRODUCTION_PROFILE.json');launch=read('PRODUCTION_LAUNCH_RECORD.json')
profile_hash=digest(profile);assert profile_hash==launch['profile_sha256']==read('PROFILE_FINGERPRINT.json')['sha256']
assert profile['context_projection']==spec==launch['context_projection']
assert profile['production_task_sha256']==sha(expected_task.encode())==launch['production_task_sha256']
assert profile['production_context_sha256']==digest(expected_context)==launch['production_context_sha256']
assert profile['content_clearance_sha256']==digest(clearance)==launch['clearance_manifest_sha256']
oldprofile=json.loads((ACCEPTED/'PRODUCTION_PROFILE.json').read_text())
for key in ('runtime','effective_scope','model_transport','ownership','snapshot','audit','external_policy','operational_limits'):
 assert profile[key]==oldprofile[key],key
assert profile['model_transmission']['file_clearances']==oldprofile['model_transmission']['file_clearances']
assert profile['model_transmission']['evidence_paths']==oldprofile['model_transmission']['evidence_paths']
validate(profile['runtime'],ARGV,str(ROOT),list(INPUTS))
validate_transport(profile['model_transport'],profile['model_transport']['endpoint'],profile['model_transport']['model'])
receipt_path=PRE/'pd06_release_evidence/provisioning/RECEIPT.json';receipt=json.loads(receipt_path.read_text())
assert sha(receipt_path.read_bytes())==profile['provisioning_receipt_sha256']
assert provisioning(b,receipt,(SOURCE,))['ready']
directories={}
for row in profile['provisioning_plan']['directories']:
 fd=open_directory(row['path']);st=os.fstat(fd);os.close(fd);path=Path(row['path'])
 directories[str(path)]={'device':st.st_dev,'inode':st.st_ino,'mode':st.st_mode,'entries':sorted(x.name for x in path.iterdir())}
for rel in ('src/kge_forge/context','tests/context','docs/implementation'):assert directories[str(ROOT/rel)]['entries']==[]
assert not (ROOT/'src/kge_forge/__init__.py').exists()
assert InvocationOwnership(LEDGER).active() is None
assert InvocationOwnership(OUT/'live/ownership.jsonl').active() is None
scopes={x.name:_observe(x) for x in CGROUP_BASE.iterdir() if x.is_dir() and x.name.startswith('scope-')}
assert all(not r['members'] and r['populated']==0 for r in scopes.values())
events=[json.loads(x) for x in SUPERVISOR_AUDIT.read_text().splitlines()]
created={r.get('scope_id') for r in events if r.get('event')=='scope_created'}
closed={r.get('scope_id') for r in events if r.get('event')=='scope_closed'}
assert created<=closed
assert not any(any(str(v).startswith('auth-e1-') for v in r.get('owner',[])) for r in events if r.get('event')=='scope_created')
raw=dict(launch['authorization']);raw['context_binding']=b
for field in ('read_roots','write_roots','deny_roots','exec_bins','read_deny_roots','write_deny_roots','write_directory_roots'):raw[field]=tuple(raw[field])
raw['exec_argv_allowlist']=tuple(tuple(x) for x in raw['exec_argv_allowlist'])
auth=WorkAuthorization(**raw);assert auth.state=='INACTIVE'
assert json.loads(auth.context_projection)==spec and json.loads(auth.model_transmission)==profile['model_transmission']
assert json.loads(auth.execution_profile)==profile['runtime'] and json.loads(auth.model_transport)==profile['model_transport']
audit=Path('/tmp/pd06-r6-independent-'+auth.authorization_id+'.jsonl')
host=GovernedHost(auth,audit);runner=ResponsesReasoning(ReasoningOrchestrator(host))
assert runner._verify_context()==projection['payload']
runner.transmission.initial(expected_task,expected_context)
for item in expected_proofs:
 path=Path(item['path']);root=next(r for r in b.repos.values() if r in path.parents)
 assert host._path(str(root),str(path.relative_to(root)))==path
# Verify exact selected production policy on all input representations without
# activating E1 or dispatching governed reads. Only controller-held bytes are used.
probes=[]
for row in clearance['inputs']:
 path=Path(row['canonical_path']);root=next((r for r in b.repos.values() if r in path.parents),path.parent)
 data=(blobs/row['captured_sha256']).read_bytes().decode(errors='replace')
 call={'name':'governed_read','arguments':json.dumps({'repository':str(root),'path':str(path.relative_to(root)),'limit':65536})}
 result=runner.transmission.result(call,{'result':'SUCCEEDED','data':{'path':str(path),'content':data}})
 allow=row['classification']=='TRANSMIT' and row['designation']=='COMPLETE_FILE'
 assert (result['transmission']=='CLEARED')==allow
 for name in ('governed_list','governed_search','governed_status','governed_exec','governed_write','governed_patch','finish_task','authority_expansion_request'):
  out=runner.transmission.result({'name':name},{'result':'SUCCEEDED','data':data,'error':data,'sha256':row['captured_sha256']})
  assert set(out)=={'transmission','notice'} and out['transmission']=='REDACTED'
 probes.append({'path':str(path),'read_projection':result['transmission'],'alternate_representations':'REDACTED'})
# Every effect remains non-effecting under the actual inactive production auth.
arguments={
 'governed_read':{'repository':str(ROOT),'path':'docs/VISION.md','limit':10},
 'governed_list':{'repository':str(ROOT),'path':'docs','limit':10},
 'governed_search':{'repository':str(ROOT),'path':'docs','query':'E1','limit':10},
 'governed_write':{'repository':str(ROOT),'path':'src/kge_forge/__init__.py','content':'DENIED'},
 'governed_patch':{'repository':str(ROOT),'changes':[{'op':'write','path':'src/kge_forge/__init__.py','content':'DENIED'}]},
 'governed_exec':{'executable':ARGV[0],'argv':list(ARGV[1:]),'cwd':str(ROOT),'inputs':list(INPUTS)},
 'governed_status':{},'authority_expansion_request':{'capability':'shell','action':'run','resources':['/bin/sh'],'reason':'inactive verification'},
 'finish_task':{'summary':'inactive verification'}}
results={}
for name,args in arguments.items():
 results[name]=runner._dispatch({'name':name,'call_id':'r6-inactive-'+name,'arguments':json.dumps(args)})
 assert results[name]['result']==('SUCCEEDED' if name=='governed_status' else 'DENIED')
try:runner.run(expected_task,expected_context,1)
except ValueError as exc:assert str(exc)=='Programmer authorization not released'
else:raise AssertionError('inactive E1 invoked')
assert not host.invocations and host.scope is None and b.verify()
# Reconstruction uses the issued exact binding, with the complete audit staying local.
restored=GovernedHost(auth,audit);resumed=ResponsesReasoning(ReasoningOrchestrator(restored))
assert resumed.projection.verify()['projection']==projection
for destination in (audit,Path(launch['audit_destination']),Path(LEDGER)):
 assert all(Path(grant)!=destination and Path(grant) not in destination.parents for grant in auth.read_roots+auth.write_roots)
production_audit=Path(launch['audit_destination']);assert production_audit.stat().st_mode&0o777==0o600
parent=production_audit.parent
while parent!=Path('/tmp'):
 assert parent.stat().st_mode&0o777==0o700 and not parent.is_symlink();parent=parent.parent
assert profile['release_preconditions']==[]
assert not any(launch[k] for k in ('RELEASED','ELIGIBLE','DISPATCHED'))
synthetic=read('synthetic/REPORT.json');live=read('live/LIVE_REPORT.json')
assert synthetic['result']==live['result']=='PASS'
assert 'Ran 22 tests' in (OUT/'focused_tests.txt').read_text() and (OUT/'focused_tests.txt').read_text().rstrip().endswith('OK')
for rel,expected in read('SOURCE_SHA256.json').items():assert sha((ROOT/rel).read_bytes())==expected
write('TRANSMISSION_VERIFICATION.json',{'result':'PASS','universe':186,'probes':probes,'actual_API_calls':0,
 'model_context_exactly_selected':True,'proof_metadata_not_in_payload':True})
write('INACTIVE_VERIFICATION.json',{'result':'PASS','state':auth.state,'results':results,'host_invocations':0,
 'scope':None,'actual_E1_execution_observed':False,'audit':str(audit),'reconstruction_identities_match':True})
write('OWNERSHIP_AND_PROVISIONING.json',{'result':'PASS','active_E1_reservation':None,'active_scratch_reservation':None,
 'unclosed_scopes':sorted(created-closed),'scope_observations':scopes,'directories':directories,'receipt_sha256':sha(receipt_path.read_bytes())})
checks={key:'PASS' for key in ('accepted_186_capture_integrity','accepted_classification_unchanged','all_six_projection_ranges',
 'exact_task_identity','FullContextDigest','ModelProjectionDigest','AuthoritativeContextId','source_and_authority_attribution',
 'context_separation_qualification','no_LOCAL_ONLY_or_NEVER_TRANSMIT_in_synthetic_requests','stale_full_context_denial',
 'stale_projection_and_clearance_denial','policy_clearance_consistency','context_recovery','execution_QUIESCENT_and_sequential_gating',
 'tool_result_filtering','exact_profile_launch_binding','no_unresolved_configuration_fields','provisioning_evidence_and_directories',
 'no_active_or_uncertain_ExecutionScope','no_outstanding_ownership','audit_evidence_isolation','E1_INACTIVE',
 'E1_WP_001_never_executed_under_recorded_controller_history')}
write('PD06_VERIFICATION.json',{'checks':checks,'readiness':'PASS / READY FOR RESERVED ARCHITECT DECISION',
 'proposed_E1_B01':'PASS','proposed_eligibility':'ELIGIBLE only upon Architect PD06 release; currently INELIGIBLE',
 'actual':{'PD06':'UNRELEASED','E1':'INACTIVE','ELIGIBLE':False,'DISPATCHED':False},
 'final_Architect_decision_made':False,'remaining_material_gaps':[]})
# Preserve retrievable committed synthetic fixture objects using the already
# qualified process-free object reader, rather than relying on temporary paths.
from adapter.committed_objects import read_blob
for label in ('synthetic','live'):
 fixture_capture=json.loads((OUT/label/'authority/MANIFEST.json').read_text())
 fixture_root=Path(next(iter(fixture_capture['inputs']))).parent
 fixture_binding=CommittedContext(fixture_root/'CONTEXT_MANIFEST.json',fixture_capture['commit'])
 objects={};files={}
 paths={r['path'] for r in fixture_binding.sources.values()}|{'CONTEXT_MANIFEST.json',
   'src/kge_forge/__init__.py','src/kge_forge/context/probe.py','tests/context/test_fixture.py'}
 for relative in sorted(paths):
  data=read_blob(fixture_root,fixture_binding.capture_commit,relative,objects)
  assert data==(fixture_root/relative).read_bytes()
  files[relative]={'sha256':sha(data),'bytes_hex':data.hex()}
 write(label+'/COMMITTED_FIXTURE.json',{'commit':fixture_binding.capture_commit,
  'root':str(fixture_root),'files':files,'loose_objects_hex':{oid:data.hex() for oid,data in objects.items()},
  'source':'verified committed SHA1 commit/tree/blob objects; no Git process or repository hooks'})
# Seal both historical authority and its explicitly attributed current supplement.
current_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=str(ROOT),text=True).strip()
paths={Path(p) for p in capture['inputs']}
paths.update(ROOT/p for p in read('SOURCE_SHA256.json'))
paths.update(p for p in OUT.rglob('*') if p.is_file() and 'captures' not in p.parts and '__pycache__' not in p.parts)
paths.update({prior,ACCEPTED/'CONTENT_CLEARANCE_MANIFEST.json',ACCEPTED/'ARCHITECT_SELECTIONS.md',
 ACCEPTED/'CAPTURE_REFERENCE.json',audit,production_audit,Path(LEDGER),SUPERVISOR_AUDIT})
files={};stored={}
for path in sorted(paths):
 if path.name in ('CAPTURE_REFERENCE.json','FINGERPRINT_VERIFICATION.json') and path.parent==OUT:continue
 data=path.read_bytes();value=sha(data);files[str(path)]={'sha256':value,'bytes':len(data)};stored[value]=data
for row in capture['inputs'].values():stored[row['sha256']]=(blobs/row['sha256']).read_bytes()
final={'schema':'E1-PD06-RELEASE-CAPTURE-CANDIDATE-6','baseline':'E1-ARCH-1','work':'E1-WP-001',
 'current_Forge_HEAD':current_head,'qualified_implementation_sha256':digest(read('SOURCE_SHA256.json')),
 'historical_186_capture_sha256':spec['capture_sha256'],'historical_186_inputs':capture['inputs'],
 'content_clearance_file_sha256':spec['clearance_sha256'],'context_identities':ids,
 'production_profile_sha256':profile_hash,'production_task_sha256':sha(expected_task.encode()),
 'PD05':'Architect PASS / accepted; affected paths requalified','PD06':'UNRELEASED / reserved Architect decision',
 'QUALIFIED':True,'RELEASED':False,'ELIGIBLE':False,'DISPATCHED':False,'E1':'INACTIVE',
 'current_inputs':files,'post_provision_directories':directories,
 'limitations':'Content-addressed read-only evidence, not privileged WORM. HEAD plus exact uncommitted source inventory identifies implementation. No actual model API/E1 implementation run. Prior accepted transport/runtime/evidence limitations retained.'}
encoded=canonical(final).encode();fingerprint=sha(encoded);folder=OUT/'captures'/fingerprint
folder.mkdir(parents=True,exist_ok=False);(folder/'blobs').mkdir()
for value,data in stored.items():
 path=folder/'blobs'/value;path.write_bytes(data);path.chmod(0o444)
(folder/'MANIFEST.json').write_bytes(encoded);(folder/'MANIFEST.json').chmod(0o444)
for raw,row in files.items():
 assert sha(Path(raw).read_bytes())==row['sha256'],raw
 assert sha((folder/'blobs'/row['sha256']).read_bytes())==row['sha256'],raw
for row in capture['inputs'].values():assert sha((folder/'blobs'/row['sha256']).read_bytes())==row['sha256']
assert sha((folder/'MANIFEST.json').read_bytes())==fingerprint
identifier='E1-PD06-R6-CANDIDATE-20260916-'+fingerprint[:16]
write('CAPTURE_REFERENCE.json',{'identifier':identifier,'manifest':str(folder/'MANIFEST.json'),
 'sha256':fingerprint,'production_profile_sha256':profile_hash,'context_identities':ids,
 'QUALIFIED':True,'RELEASED':False,'ELIGIBLE':False,'DISPATCHED':False})
write('FINGERPRINT_VERIFICATION.json',{'result':'PASS','capture_sha256':fingerprint,'current_input_count':len(files),
 'historical_input_count':186,'stored_blobs_verified':True,'current_authoritative_bytes_verified':True,
 'profile_sha256':profile_hash,'material_differences':'Only authorized context/projection implementation and evidence supplement; accepted six-source clearance unchanged'})
print(json.dumps({'identifier':identifier,'sha256':fingerprint,'profile_sha256':profile_hash,'identities':ids,
 'PD06_readiness':'PASS / reserved Architect decision','E1':'INACTIVE','eligible':False,'dispatched':False}))
