"""Append-only qualified PREPARED publication. Never issues an invocation."""
import json,hashlib,os,sys
from pathlib import Path
from adapter.context_projection import canonical,digest,sha
from adapter.controller_authority_store import ControllerAuthorityStore,_directory,_put,encoded
O=Path(sys.argv[1]);run=O/'candidate6'
def load(name):return json.loads((run/name).read_bytes())
pub=load('PREPARED_PUBLICATION.json');pre=load('PREFLIGHT.json');neg=load('NEGATIVE_PROBES.json');tests=load('INTEGRATED_TESTS.json');r8=load('R8_INDEPENDENT_RECOVERY.json')
assert pre['result']=='PASS_PENDING_SPECIFIC_ARCHITECT_ISSUANCE' and neg['result']=='PASS'
assert len(tests)==22 and all(t['returncode']==0 and not t['deadlock_timeout'] for t in tests)
assert not any(x['soft_exceeded'] or x['hard_exceeded'] for x in pre['diagnostics'])
assert 'Ran 41 tests' in (run/'REGRESSION_FINAL.log').read_text() and (run/'REGRESSION_FINAL.log').read_text().rstrip().endswith('OK')
assert 'Ran 2 tests' in (run/'DISPATCH_GATES.log').read_text() and (run/'DISPATCH_GATES.log').read_text().rstrip().endswith('OK')
assert r8['result']=='REJECTED_AS_REQUIRED'
historical=json.loads((O.parent/'run2_nonhost_closure_2026-09-17/FINAL_IMPLEMENTATION.json').read_bytes())
assert all(sha(Path(p).read_bytes())==h for p,h in historical['inventory'].items())
s=ControllerAuthorityStore(**pub['selected_store']);A=s.applicability['authorization_id']
with s.session():
 runtime=json.loads(s.resolve(pub['controller_runtime']['authority_id']));assert {p.name:sha(p.read_bytes()) for p in (Path(runtime['root'])/'adapter').glob('*.py')}==runtime['files']
 proposal=json.loads(s.resolve(pub['proposal']['authority_id']));assert not os.path.lexists(proposal['audit'])
 assert sha(Path(proposal['predecessor']['audit']).read_bytes())==proposal['predecessor']['audit_sha256']
 attempt_ledger=s.state_path(proposal['DispatchAuthorizationId']+':attempt-ledger');assert attempt_ledger.read_bytes()==b''
 snapshot_paths={proposal['predecessor']['audit']:proposal['predecessor']['audit_sha256'],
 '/tmp/kge-forge-e1-invocations.jsonl':'651ced1160af0760f8b46073972a88f9d1ffc2c8ed0394e900bfa05fec586fe7',
 '/tmp/kge-forge-e1-evidence/auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39/session-e1-50b26bdb12b44ec7a92e0c517c7de7c8/turn-e1-58d4a30dbf79478f8afc7b46a84caa47/controller.jsonl':'23d46d0fe282d322b731b309f7d48beebd676894ca0701e75c5468ed4fde427f'}
 assert all(sha(Path(p).read_bytes())==h for p,h in snapshot_paths.items())
 files=['PREFLIGHT.json','PRE_ISSUANCE_DIAGNOSTICS.json','NEGATIVE_PROBES.json','INTEGRATED_TESTS.json','REGRESSION_FINAL.log','DISPATCH_GATES.log','R8_INDEPENDENT_RECOVERY.json']
 q={'schema':'E1-RUN2-ATTEMPT-QUALIFICATION-1','result':'PASS','amendment':pub['amendment'],'controller_runtime':pub['controller_runtime'],
 'accepted_proposal':pub['proposal'],'continuation':pub['continuation'],'evidence':{name:sha((run/name).read_bytes()) for name in files},
 'synthetic_lifecycle_tests':22,'dispatch_boundary_tests':2,'regression_tests':41,'actual_context_negative_probes':29,
 'deadlock_detector_seconds':40,'deadlock_timeouts':0,'maximum_synthetic_test_seconds':max(t['seconds'] for t in tests),
 'actual_production_preflight':'PASS_PENDING_SPECIFIC_ARCHITECT_ISSUANCE','r8_disposition':r8['disposition'],
 'historical_hashes':snapshot_paths,'unchanged_supervisor_implementation':historical['identity'],
 'real_r9':{'issued':False,'active':False,'ownership':'NONE','audit_unused':True,'model_requests':0,'effects':0},
 'scope':['Actual prepared context, release/dispatch/attempt-decision authentication, private resolution, fresh S3 readiness and timing tested read-only.',
 'INACTIVE to ACTIVE and independent recovery tested using non-E1 synthetic identities and private stores; kernel supervisor observation mocked only in those synthetic transaction fixtures.',
 'No real r9 lifecycle transition or model handoff performed; specific Architect issuance approval remains absent.'],
 'materiality':{'issuance_order_and_lock_composition':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION','attempt_semantics_and_context_authentication':'MATERIAL_AUTHORITY_AMENDMENT',
 'profile_payload_tools_budgets_transmission_supervisor_execution_ownership_recovery_acceptance':'UNCHANGED'},
 'integration_corrections':['Disambiguated specific-approval and durable-issuance check names.','Dispatch now validates original durable INACTIVE issuance before authorization telemetry.']}
 qb=canonical(q).encode();qh=sha(qb);qr={'authority_id':'sha256:'+qh,'sha256':qh}
 selection=json.loads(s.resolve(A+':attempt-context'));assert selection['mode']=='PREPARED' and selection['specific_invocation_authorization'] is None
 selection['qualification']=qr;sb=canonical(selection).encode();sh=sha(sb)
 cat=json.loads(encoded(s.catalog));root=s.root.parent/'qualified-prepared-v2';root.mkdir(mode=0o700)
 fd=_directory(root)
 try:
  for h in {row['sha256'] for row in cat['objects'].values()}:_put(fd,h,(s.root/h).read_bytes())
  _put(fd,qh,qb);_put(fd,sh,sb)
  row=dict(cat['objects'][A+':attempt-context']);row['sha256']=qh;row['evidence']=[{'path':str(run/'QUALIFICATION.json'),'sha256':qh}];cat['objects'][qr['authority_id']]=row
  row=dict(cat['objects'][A+':attempt-context']);row['sha256']=sh;cat['objects'][A+':attempt-context']=row
  _put(fd,'catalog.json',canonical(cat).encode());os.fsync(fd)
 finally:os.close(fd)
 final=dict(pub,status='QUALIFIED_PREPARED_NO_INVOCATION_ISSUANCE_AUTHORITY',qualification=qr,
  selected_store={'root':str(root),'catalog_sha256':digest(cat),'applicability':dict(s.applicability)},
  original_dispatch=proposal['dispatch'],r9_authorization_id=A,specific_Architect_issuance_authorization=None)
 (run/'QUALIFICATION.json').write_bytes(qb)
 fb=canonical(final).encode();fd=_directory(root.parent)
 try:_put(fd,'QUALIFIED_AUTHORITY_PUBLICATION_V2.json',fb);os.fsync(fd)
 finally:os.close(fd)
 pin={'path':str(root.parent/'QUALIFIED_AUTHORITY_PUBLICATION_V2.json'),'sha256':sha(fb)}
 (O/'CURRENT_PIN.json').write_text(canonical(pin));(O/'AUTHORITY_PUBLICATION.json').write_bytes(fb)
 finalrun=O/'independent_reconstruction_v2';finalrun.mkdir();(finalrun/'PREPARED_PUBLICATION.json').write_bytes(fb)
 print(canonical({'publication_pin':pin,'qualification':qr,'status':final['status']}))
s.close()
