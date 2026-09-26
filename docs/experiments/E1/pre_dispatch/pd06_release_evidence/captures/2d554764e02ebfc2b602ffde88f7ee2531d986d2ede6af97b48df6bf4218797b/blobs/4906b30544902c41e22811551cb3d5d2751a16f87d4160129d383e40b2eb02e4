from pathlib import Path
import json,hashlib,shutil,tempfile,sys,ssl,datetime
from adapter.context_binding import CommittedContext
from adapter.runnable_profile import authorization,canonical
from adapter.launch_profile import proposal
from adapter.governed_host import GovernedHost
from adapter.orchestrator import ReasoningOrchestrator
from adapter.responses_orchestrator import ResponsesReasoning,tool_definitions

root=Path('/home/gvasend/app/kge-forge');out=root/'docs/experiments/E1/pre_dispatch/pd05_final_evidence'
out.mkdir(exist_ok=True)
sha=lambda b:hashlib.sha256(b).hexdigest()
live=Path('/tmp/pd05-g5-live-final-v4-20260916')
for name in ['LIVE_REPORT.json','HOST_RECEIPT.json','controller.jsonl','ownership.jsonl']:
 shutil.copyfile(live/name,out/name)
(out/'snapshots').mkdir(exist_ok=True)
for p in (live/'snapshots').iterdir(): shutil.copyfile(p,out/'snapshots'/p.name)
shutil.copyfile('/tmp/pd05-final-regression.txt',out/'tests.txt')
b=CommittedContext(root/'docs/experiments/E1/pre_dispatch/CONTEXT_MANIFEST.json','5871bdce4f5b6539c84f69f4f2b2f94ee31be5cd')
a=authorization(b,b,'auth-e1-r3-INACTIVE-evidence',3,'session-e1-r3-INACTIVE-evidence','turn-e1-r3-INACTIVE-evidence')
assert a.state=='INACTIVE'
profile=proposal(b)
record=dict(a.__dict__)
record['context_binding']={'capture_commit':b.capture_commit,'context_sha256':b.digest,'work_id':b.manifest['work_id'],'baseline_id':b.manifest['baseline_id']}
profile['effective_scope']={k:record[k] for k in ['read_roots','write_roots','write_directory_roots','deny_roots','read_deny_roots','write_deny_roots','exec_bins','exec_argv_allowlist','shell','network']}
profile['captured_write_protections']=sorted(str(p) for p in b.protected_paths)
profile['tool_registry']=tool_definitions()
profile['model_information_categories']={'authorized':[
 'Committed E1 governing/context/task sources and identified metadata',
 'Ordinary files, names and bounded search matches returned by granted read/list/search after both repository hidden-path exclusions',
 'Governed in-scope implementation/test artifacts and bounded operation results, status, hashes, diagnostics and finish/expansion requests',
 'Caller-held prior model outputs and required encrypted reasoning continuation items'],
 'not_authorized':['credential/secret values','unrelated host information','private controller/supervisor audit contents','excluded real hidden directories'],
 'remaining_selection':'Real ordinary-content suitability/clearance is not proved by path grants. No secret scanning or model disclosure was performed; Architect must resolve any intended transmission outside the listed non-secret scope before release.'}
profile['model_execution_settings']={'max_cycles':12,'parallel_tool_calls':False,'previous_response_id':False,'reasoning_continuation':'encrypted_content',
 'TLS_runtime_selection':'ssl.PROTOCOL_TLS_CLIENT with default platform cipher suite, minimum TLSv1.2; explicit pinned CA file; no inherited proxy, CA environment or custom opener; redirects denied',
 'controller_python':{'path':str(Path(sys.executable).resolve()),'sha256':sha(Path(sys.executable).read_bytes()),'version':sys.version.split()[0],'openssl':ssl.OPENSSL_VERSION}}
profile['supervisor_binding']=json.loads((out/'HOST_RECEIPT.json').read_text())['supervisor']
profile['operational_limits']={'host_quiescence_wait_seconds':15,'bridge_socket_timeout_seconds':12,'supervisor_first_receipt_wait_seconds':10,
 'supervisor_first_receipt_max_bytes':65536,'snapshot_max_inputs':100,'snapshot_max_files':2000,'snapshot_max_bytes':67108864,'snapshot_max_file_bytes':8388608,
 'read_bytes':65536,'write_patch_bytes':1000000,'argv_count':64,'argv_total_bytes':8192,
 'stdout_stderr_limitation':'ActionResult carries the bound launcher start receipt and terminal exit/quiescence evidence, not a general captured stdout/stderr transcript. Fixture detailed results are recovered from hashed scratch artifacts. Payload excessive pipe output remains subject to timeout/indeterminate behavior; no successful output-capture claim.'}
profile['release_preconditions']=[
 {'id':'PROVISION','status':'ARCHITECT-SELECTION-PENDING','detail':'Exact required paths need recognized Architect provisioning authority and a receipt; none selected, none created; absent/unauthorized fails closed.'},
 {'id':'CONTENT','status':'ARCHITECT-SELECTION-PENDING','detail':'No secret-bearing ordinary file transmission is authorized by a read grant; resolve real-content suitability where needed.'},
 {'id':'CAPTURE','status':'ARCHITECT-SELECTION-PENDING','detail':'Final source/profile capture/release reference is not selected; working source hashes identify the qualified artifact, not a release.'},
 {'id':'FRESH_OWNERSHIP','status':'QUALIFIED','detail':'Common ledger and fail-closed mechanism qualified; fresh E1 global no-active/unaccounted check remains mandatory before release.'},
 {'id':'RUNTIME_RECHECK','status':'QUALIFIED','detail':'Exact binary paths/content, argv, cwd, inputs, environment and sealed derived inputs are rechecked; changed runtime or unsupported packed source denies.'}]
profile['architect_status']={'PD-05':'PENDING','PD-06':'NOT AUTHORIZED','E1':'INACTIVE','E1-WP-001':'INELIGIBLE AND UNDISPATCHED','G1':'CLOSED/PASS','G2':'WRITE SEMANTICS CLOSED','G4':'CLOSED/PASS'}
profile['authority_sources']={
 'baseline':{'forge':'411cb5a9fabc71e482a414ed58387de0ff557e93','preparation':b.capture_commit,'service':'c9458a8698c90bd43137025fa7e1dc3c34c4e37a'},
 'current_supplement':'Architect final runnable-profile qualification instruction in this conversation; recorded in FINAL_PD05_RUNNABLE_QUALIFICATION_2026-09-16.md',
 'classification_rule':'Nested fields inherit the named field attribution unless an explicit pending condition overrides it. Newly selected concrete configuration is a proposal under delegated Architect preparation authority, not a release decision.'}
attrs={}
for k in profile:
 if k in ['work_id','capture_commit','context_sha256','effective_scope','captured_write_protections']:
  cls='baseline-derived';source='Captured CONTEXT_MANIFEST and E1-WP-001, narrowed by accepted G1/G2'
 elif k in ['ownership','audit','identity','snapshot','runtime','model_transport','model_execution_settings','external_policy','model_information_categories']:
  cls='newly Architect-selected';source='Current G5/G3/G6 mandate and conditional acceptance; concrete values prepared under delegated controller selection, with pending conditions listed separately'
 elif k in ['provisioning','release_preconditions']:
  cls='unresolved';source='Explicit pre-activation obligations; no approval inferred'
 else:
  cls='previously human/Architect-approved';source='Qualified A2 mechanism/current preservation instruction or non-effecting evidence metadata; final release still reserved'
 attrs[k]={'classification':cls,'source':source}
profile['field_attribution']=attrs
(out/'PROPOSED_PRODUCTION_PROFILE.json').write_text(json.dumps(profile,indent=2)+'\n')
(out/'PROFILE_SHA256.txt').write_text(sha(canonical(profile).encode())+'\n')
# Inactive checks using all implemented R3 fields, without a production launch.
watched=list(b.protected_paths)+[Path(p) for p in a.write_roots]+[Path(a.ownership_ledger)]
def observe(p):
 if not p.exists(): return None
 if p.is_dir(): return 'directory'
 return sha(p.read_bytes())
before={str(p):observe(p) for p in watched}
audit=Path(tempfile.mkdtemp(prefix='pd05-final-inactive-'))/'controller.jsonl'
h=GovernedHost(a,audit);r=ResponsesReasoning(ReasoningOrchestrator(h))
args={'governed_read':{'repository':str(root),'path':'docs/VISION.md','limit':100},
 'governed_list':{'repository':str(root),'path':'docs','limit':100},
 'governed_search':{'repository':str(root),'path':'docs','query':'E1','limit':100},
 'governed_write':{'repository':str(root),'path':'src/kge_forge/__init__.py','content':'MUST NOT WRITE'},
 'governed_patch':{'repository':str(root),'changes':[{'op':'write','path':'src/kge_forge/__init__.py','content':'MUST NOT PATCH'}]},
 'governed_exec':{'executable':profile['runtime']['argv'][0],'argv':profile['runtime']['argv'][1:],'cwd':str(root),'inputs':profile['runtime']['inputs']},
 'governed_status':{},'authority_expansion_request':{'capability':'shell','action':'run','resources':['/bin/sh'],'reason':'inactive final verification'},'finish_task':{'summary':'inactive verification'}}
results={}
for name,fields in args.items():
 results[name]=r._dispatch({'name':name,'call_id':'final-inactive-'+name,'arguments':json.dumps(fields)})
 assert results[name]['result']==('SUCCEEDED' if name=='governed_status' else 'DENIED')
 if name!='governed_status': assert results[name]['error']=='authorization not released'
try:r.run('NO IMPLEMENTATION',b.model_context(),1)
except ValueError as e:denial=str(e)
else:raise AssertionError('inactive model turn accepted')
assert not h.invocations and h.scope is None and h._pending is None
assert before=={str(p):observe(p) for p in watched}
shutil.copyfile(audit,out/'inactive_controller.jsonl')
(out/'INACTIVE_VERIFICATION.json').write_text(json.dumps({'authorization':record,'results':results,
 'model_denial':denial,'host_invocations':0,'scope':None,'watched_before':before,'watched_after_equal':True,
 'source_count':len(b.sources),'mandatory_closure_count':len(b.closure),'binding_verified':b.verify(),
 'provisioning':profile['provisioning']},indent=2)+'\n')
# The first snapshot supplies a complete exact acceptance-input inventory.
snapshots=[json.loads(p.read_text()) for p in sorted((out/'snapshots').glob('*.json'))]
(out/'ACCEPTANCE_INPUTS.json').write_text(json.dumps({'manifest_identity':profile['runtime']['acceptance'],
 'sources':snapshots[0]['acceptance']['sources'],
 'repository_mounts':snapshots[0]['acceptance']['repository_mounts'],
 'readonly_mounts':True,'scope_scratch_writable':True,
 'provenance':'verified loose commit/tree/blob objects plus source SHA256; current designated source bytes verified before each action',
 'actual_E1_implementation_executed':False},indent=2)+'\n')
print(json.dumps({'state':a.state,'inactive_denials':8,'host_invocations':0,'profile':str(out/'PROPOSED_PRODUCTION_PROFILE.json'),'live_qualification':json.loads((out/'LIVE_REPORT.json').read_text())['result']}))
