"""Independent, inactive PD06 verification and unreleased final evidence capture."""
from pathlib import Path
import hashlib,json,os,subprocess,sys
ROOT=Path('/home/gvasend/app/kge-forge');sys.path.insert(0,str(ROOT))
from adapter.context_binding import CommittedContext
from adapter.runnable_profile import canonical,ARGV,INPUTS,validate
from adapter.model_transport import validate as transport_validate
from adapter.directory_provisioning import open_directory,SOURCE
from adapter.launch_profile import provisioning,LEDGER
from adapter.invocation_ownership import InvocationOwnership
from adapter.recovery_ledger import _observe,CGROUP_BASE,SUPERVISOR_AUDIT
from adapter.governed_host import WorkAuthorization,GovernedHost
from adapter.orchestrator import ReasoningOrchestrator
from adapter.responses_orchestrator import ResponsesReasoning
from adapter.model_transmission import digest
PRE=ROOT/'docs/experiments/E1/pre_dispatch';OUT=PRE/'pd06_final_clearance'
sha=lambda data:hashlib.sha256(data).hexdigest()
def read(name):return json.loads((OUT/name).read_text())
def write(name,value):(OUT/name).write_text(json.dumps(value,indent=2)+'\n')
clearance=read('CONTENT_CLEARANCE_MANIFEST.json');ref=clearance['candidate']
oldpath=Path(ref['manifest']);old=json.loads(oldpath.read_bytes());oldblobs=oldpath.parent/'blobs'
assert sha(oldpath.read_bytes())==ref['capture_sha256']
assert len(old['inputs'])==186
assert len(clearance['inputs'])==186 and set(r['canonical_path'] for r in clearance['inputs'])==set(old['inputs'])
for row in clearance['inputs']:
 path=row['canonical_path'];expected=old['inputs'][path]['sha256'];assert row['captured_sha256']==expected
 data=(oldblobs/expected).read_bytes();assert sha(data)==expected==sha(Path(path).read_bytes())
 assert row['classification'] in ('TRANSMIT','LOCAL_ONLY','NEVER_TRANSMIT')
 if row['classification']=='TRANSMIT':
  assert row['reason'] and row['authority_source'] and row['designation'] in ('COMPLETE_FILE','BOUNDED_CONTENT')
  for span in row['spans']:
   assert 0<=span['start_byte']<span['end_byte_exclusive']<=len(data)
   assert sha(data[span['start_byte']:span['end_byte_exclusive']])==span['sha256']
b=CommittedContext(PRE/'CONTEXT_MANIFEST.json','5871bdce4f5b6539c84f69f4f2b2f94ee31be5cd');assert b.verify()
p=read('PRODUCTION_PROFILE.json');launch=read('PRODUCTION_LAUNCH_RECORD.json')
profile_hash=sha(canonical(p).encode());assert profile_hash==launch['profile_sha256']
assert p['content_clearance_sha256']==sha(canonical(clearance).encode())==launch['clearance_manifest_sha256']
context=read('PRODUCTION_CONTEXT.json');task=(OUT/'PRODUCTION_TASK.md').read_bytes()
wp=str(PRE/'E1-WP-001.md');assert task==(oldblobs/old['inputs'][wp]['sha256']).read_bytes()
assert sha(task)==p['production_task_sha256']==launch['production_task_sha256']
assert p['production_context_sha256']==sha(canonical(context).encode())==launch['production_context_sha256']
# Reconstruct every selected model-visible excerpt independently from source ranges.
selected={r['canonical_path']:r for r in clearance['inputs'] if r['classification']=='TRANSMIT'}
assert set(x['source'] for x in context['sources'])==set(selected)-{wp}
for source in context['sources']:
 row=selected[source['source']];data=(oldblobs/row['captured_sha256']).read_bytes()
 assert len(source['selections'])==len(row['spans'])
 for value,span in zip(source['selections'],row['spans']):
  assert value=={'label':span['label'],'content':data[span['start_byte']:span['end_byte_exclusive']].decode()}
validate(p['runtime'],ARGV,str(ROOT),list(INPUTS))
transport_validate(p['model_transport'],p['model_transport']['endpoint'],p['model_transport']['model'])
oldprofile=json.loads((oldblobs/old['inputs'][str(PRE/'pd06_release_evidence/PROPOSED_PRODUCTION_PROFILE.json')]['sha256']).read_bytes())
assert all(p[k]==oldprofile[k] for k in ('runtime','effective_scope','model_transport','ownership','snapshot','audit','external_policy','operational_limits'))
receipt=json.loads((PRE/'pd06_release_evidence/provisioning/RECEIPT.json').read_text())
assert provisioning(b,receipt,(SOURCE,))['ready']
assert sha((PRE/'pd06_release_evidence/provisioning/RECEIPT.json').read_bytes())==p['provisioning_receipt_sha256']
directories={}
for row in p['provisioning_plan']['directories']:
 fd=open_directory(row['path']);os.close(fd)
 path=Path(row['path']);directories[str(path)]={'mode':oct(path.stat().st_mode&0o777),'entries':sorted(x.name for x in path.iterdir())}
assert all(not directories[str(ROOT/rel)]['entries'] for rel in ('src/kge_forge/context','tests/context','docs/implementation'))
assert not (ROOT/'src/kge_forge/__init__.py').exists()
assert InvocationOwnership(LEDGER).active() is None
scopes={x.name:_observe(x) for x in CGROUP_BASE.iterdir() if x.is_dir() and x.name.startswith('scope-')}
assert all(not x['members'] and x['populated']==0 for x in scopes.values())
events=[json.loads(line) for line in SUPERVISOR_AUDIT.read_text().splitlines()]
created={e.get('scope_id') for e in events if e.get('event')=='scope_created'}
closed={e.get('scope_id') for e in events if e.get('event')=='scope_closed'}
assert created<=closed
assert not any(any(str(part).startswith('auth-e1-') for part in e.get('owner',[])) for e in events if e.get('event')=='scope_created')
# A separate inactive authorization/audit verifies effects remain denied.
raw=dict(launch['authorization']);raw['context_binding']=b
for field in ('read_roots','write_roots','deny_roots','exec_bins','read_deny_roots','write_deny_roots','write_directory_roots'):raw[field]=tuple(raw[field])
raw['exec_argv_allowlist']=tuple(tuple(x) for x in raw['exec_argv_allowlist'])
auth=WorkAuthorization(**raw);assert auth.state=='INACTIVE'
audit=Path(launch['audit_destination']);assert all(Path(grant) not in audit.parents for grant in auth.read_roots+auth.write_roots)
# Apply the already selected private audit-directory permissions; no product effects.
permissions=[]
parent=audit.parent
while parent!=Path('/tmp'):
 assert parent.is_dir() and not parent.is_symlink()
 os.chmod(parent,0o700);permissions.append({'path':str(parent),'mode':oct(parent.stat().st_mode&0o777)})
 parent=parent.parent
assert audit.stat().st_mode&0o777==0o600
# Use an independent audit, leaving the proposed controller issuance untouched.
check_audit=Path('/tmp/pd06-final-independent-'+auth.authorization_id+'.jsonl')
host=GovernedHost(auth,check_audit);runner=ResponsesReasoning(ReasoningOrchestrator(host))
requests={
 'governed_read':{'repository':str(ROOT),'path':'docs/VISION.md','limit':10},
 'governed_list':{'repository':str(ROOT),'path':'docs','limit':10},
 'governed_search':{'repository':str(ROOT),'path':'docs','query':'E1','limit':10},
 'governed_write':{'repository':str(ROOT),'path':'src/kge_forge/__init__.py','content':'MUST NOT WRITE'},
 'governed_patch':{'repository':str(ROOT),'changes':[{'op':'write','path':'src/kge_forge/__init__.py','content':'MUST NOT WRITE'}]},
 'governed_exec':{'executable':p['runtime']['argv'][0],'argv':p['runtime']['argv'][1:],'cwd':str(ROOT),'inputs':p['runtime']['inputs']},
 'governed_status':{},'authority_expansion_request':{'capability':'shell','action':'run','resources':['/bin/sh'],'reason':'inactive verification'},
 'finish_task':{'summary':'inactive verification'}}
results={}
for name,args in requests.items():
 results[name]=runner._dispatch({'name':name,'call_id':'final-'+name,'arguments':json.dumps(args)})
 assert results[name]['result']==('SUCCEEDED' if name=='governed_status' else 'DENIED')
try:runner.run(task.decode(),context,1)
except ValueError as e:assert str(e)=='Programmer authorization not released'
else:raise AssertionError('inactive E1 accepted')
assert host.scope is None and not host.invocations
# This compatibility failure follows directly from the unchanged qualified guard.
source=(ROOT/'adapter/responses_orchestrator.py').read_text()
assert 'if context!=binding.model_context():' in source
assert context!=b.model_context()
policy=json.loads(auth.model_transmission)
assert any(r['sha256']==digest({'task':task.decode(),'context':context}) for r in policy['initial_clearances'])
assert not any(r['sha256']==digest({'task':task.decode(),'context':b.model_context()}) for r in policy['initial_clearances'])
write('INACTIVE_AND_SCOPE_VERIFICATION.json',{'results':results,'state':auth.state,'host_invocations':0,
 'scope':None,'all_scopes':scopes,'unclosed_scopes':sorted(created-closed),'active_E1_reservation':None,
 'E1_supervisor_scope_creations':0,'product_directories':directories,'audit_permissions':permissions,
 'independent_audit':str(check_audit),'E1_WP_001_execution_observed':False})
checks={
 'original_186_fingerprints':'PASS','content_clearance_spans_and_hashes':'PASS',
 'production_task_exact_captured_bytes':'PASS','complete_186_transmission_classification':'PASS',
 'TRANSMIT_necessity_and_read_authority':'PASS','excluded_tool_result_representations':'PASS',
 'provisioning_directories_and_evidence':'PASS','profile_launch_configuration_binding':'PASS',
 'unchanged_execution_transport_and_grants':'PASS','unresolved_authority_selections':'NONE',
 'required_model_context_compatible_with_clearance':'FAIL',
 'no_active_or_uncertain_scope':'PASS','no_outstanding_E1_reservation':'PASS',
 'audit_evidence_isolation':'PASS','E1_remains_INACTIVE':'PASS','E1_WP_001_never_executed_under_recorded_controller_history':'PASS'}
write('VERIFICATION.json',{'checks':checks,'result':'FAIL / PD06 UNRELEASED',
 'blocker':'Qualified loop requires uncleared gate/controller context; selected minimum context is rejected. A separately scoped context-projection change and regression evidence are needed, not broader disclosure authority.',
 'release_record_prepared':False,'proposed_E1_B01':'BLOCKED','proposed_E1_WP_001_eligibility':'INELIGIBLE',
 'actual':{'E1':'INACTIVE','RELEASED':False,'ELIGIBLE':False,'DISPATCHED':False},
 'final_Architect_decision_made':False})
# Final capture includes all original authoritative inputs plus the new selections,
# exact proposals, verification results and their controller-private audits.
current_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=str(ROOT),text=True).strip()
assert current_head==old['implementation_HEAD']
inputs=dict(old['inputs']);blobs={key:(oldblobs/key).read_bytes() for key in {x['sha256'] for x in inputs.values()}}
additional=set(x for x in OUT.iterdir() if x.is_file() and x.name not in ('CAPTURE_REFERENCE.json','FINGERPRINT_VERIFICATION.json'))
additional|={oldpath,audit,check_audit}
for path in sorted(additional):
 data=path.read_bytes();value=sha(data);blobs[value]=data;inputs[str(path)]={'sha256':value,'bytes':len(data)}
final={'schema':'E1-PD06-FINAL-EVIDENCE-CAPTURE-1','kind':'UNRELEASED; not a final release record',
 'baseline':'E1-ARCH-1','work':'E1-WP-001','prior_candidate_sha256':ref['capture_sha256'],
 'current_Forge_HEAD':current_head,'implementation_worktree_sha256':old['implementation_worktree_sha256'],
 'profile_sha256':profile_hash,'production_task_sha256':sha(task),'clearance_manifest_sha256':sha(canonical(clearance).encode()),
 'architect_selections_sha256':sha((OUT/'ARCHITECT_SELECTIONS.md').read_bytes()),
 'PD05':'PASS / Architect accepted','PD06':'UNRELEASED / context compatibility failure',
 'E1':'INACTIVE','RELEASED':False,'ELIGIBLE':False,'DISPATCHED':False,
 'inputs':inputs,'post_provision_directories':directories,
 'new_artifact_classification':'Release records and verification machinery remain LOCAL_ONLY; raw audits remain NEVER_TRANSMIT. PRODUCTION_TASK.md and PRODUCTION_CONTEXT.json are exact derived payload copies of the six selected source clearances, not additional independent source authority.',
 'storage_limitation':'Read-only content-addressed bytes, not privileged write-once storage; subsequent material changes require new capture and verification.'}
encoded=canonical(final).encode();fingerprint=sha(encoded);folder=OUT/'captures'/fingerprint
folder.mkdir(parents=True,exist_ok=False);(folder/'blobs').mkdir()
for key,data in blobs.items():
 dest=folder/'blobs'/key;dest.write_bytes(data);dest.chmod(0o444)
(folder/'MANIFEST.json').write_bytes(encoded);(folder/'MANIFEST.json').chmod(0o444)
for path,row in inputs.items():
 assert sha(Path(path).read_bytes())==row['sha256'],path
 assert sha((folder/'blobs'/row['sha256']).read_bytes())==row['sha256'],path
assert sha((folder/'MANIFEST.json').read_bytes())==fingerprint
identifier='E1-PD06-FINAL-EVIDENCE-20260916-'+fingerprint[:16]
write('CAPTURE_REFERENCE.json',{'identifier':identifier,'manifest':str(folder/'MANIFEST.json'),
 'sha256':fingerprint,'production_profile_sha256':profile_hash,
 'release_record_prepared':False,'RELEASED':False,'ELIGIBLE':False,'DISPATCHED':False})
write('FINGERPRINT_VERIFICATION.json',{'result':'PASS','capture_sha256':fingerprint,'input_count':len(inputs),
 'profile_sha256':profile_hash,'authoritative_input_bytes_match':True,'stored_blobs_match':True,
 'clearance_universe':186,'PD06_readiness':'FAIL: fixed model-context compatibility',
 'fingerprint_definition':'SHA256 of canonical compact sorted-key JSON for manifests/profiles; input rows hash exact bytes'})
print(json.dumps({'identifier':identifier,'capture_sha256':fingerprint,'profile_sha256':profile_hash,
 'counts':clearance['counts'],'verification':checks,'release_record_prepared':False}))
