"""Close qualification into a private PREPARED store; never issue or allocate."""
import json,os,sys,shutil,difflib
from pathlib import Path
from adapter.context_projection import canonical,digest,sha
from adapter.controller_authority_store import ControllerAuthorityStore,_directory,_put,encoded
O=Path(sys.argv[1]);run=O/'candidate3';runtime_root=Path(__file__).parent
load=lambda p:json.loads(Path(p).read_bytes())
pub=load(run/'PREPARED_PUBLICATION.json');pre=load(run/'PREFLIGHT.json');neg=load(run/'NEGATIVE_CONTEXT.json')
assert pre['result']=='PASS_PROSPECTIVE_R10_PENDING_SPECIFIC_ARCHITECT_ISSUANCE' and neg['result']=='PASS'
assert not any(r['soft_exceeded'] or r['hard_exceeded'] for r in pre['diagnostics'])
for name,count in [('SYNTHETIC.log',21),('ATTEMPT_REGRESSIONS.log',38),('PRODUCTION_REGRESSIONS.log',41)]:
 t=(O/name).read_text();assert 'Ran '+str(count)+' tests' in t and t.rstrip().endswith('OK')
history=load(O.parent/'run2_r10_session_qualification_2026-09-18/HISTORICAL_HASHES.json')
proposal=load(O.parent/'run2_r10_session_qualification_2026-09-18/PROPOSED_R10_BINDING.json')
history[proposal['historical_r8']['audit']]=proposal['historical_r8']['audit_sha256']
history['/tmp/kge-forge-e1-evidence/auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39/session-e1-50b26bdb12b44ec7a92e0c517c7de7c8/turn-e1-58d4a30dbf79478f8afc7b46a84caa47/controller.jsonl']='23d46d0fe282d322b731b309f7d48beebd676894ca0701e75c5468ed4fde427f'
assert all(sha(Path(p).read_bytes())==h for p,h in history.items())
historical=load(O.parent/'run2_nonhost_closure_2026-09-17/FINAL_IMPLEMENTATION.json');assert all(sha(Path(p).read_bytes())==h for p,h in historical['inventory'].items())
s=ControllerAuthorityStore(**pub['selected_store']);A=s.applicability['authorization_id']
with s.session():
 runtime=json.loads(s.resolve(pub['controller_runtime']['authority_id']));assert {p.name:sha(p.read_bytes()) for p in (runtime_root/'adapter').glob('*.py')}==runtime['files']
 assert not os.path.lexists(proposal['audit']) and not Path(proposal['audit']).parent.parent.exists()
 assert s.state_path(proposal['DispatchAuthorizationId']+':attempt-ledger').read_bytes()==b''
 evidence=[run/'PREFLIGHT.json',run/'PRE_ISSUANCE_DIAGNOSTICS.json',run/'NEGATIVE_CONTEXT.json',O/'SYNTHETIC.log',O/'ATTEMPT_REGRESSIONS.log',O/'PRODUCTION_REGRESSIONS.log',O/'ACTUAL_TERMINAL_STATUS.json']
 q={'schema':'E1-RUN2-TERMINAL-ATTEMPT-QUALIFICATION-1','result':'PASS','amendment':pub['amendment'],'controller_runtime':pub['controller_runtime'],
 'accepted_proposal':pub['proposal'],'continuation':pub['continuation'],'evidence':{str(p):sha(p.read_bytes()) for p in evidence},
 'actual_preflight':'PASS_PROSPECTIVE_R10_PENDING_SPECIFIC_ARCHITECT_ISSUANCE','negative_probes':len(neg['probes']),
 'phase_budgets':{'soft':30,'hard':120},'synthetic_deadlock_watchdog_seconds':180,'restart_subprocess_watchdog_seconds':90,
 'real_r10':{'issued':False,'active':False,'owned':False,'audit_unused':True,'model_requests':0,'effects':0},
 'historical_hashes':history,'S3':pre['warm_validation']['host'],
 'scope':['Actual exact r10 private context/release/dispatch/attempt ancestry, live S3 readiness and full pre-issuance production validation.',
 'Synthetic non-E1 identities exercise issuance, activation, ownership, independent restart, dispatcher session acquisition, stub model transport, cancellation and status. No real r10 lifecycle mutation.',
 'Unissued r8 retains original verifier. Exact transition admits only independently reconstructed ACTIVE-to-CANCELLED pre-model r9. Issued-INACTIVE class is evaluated separately, not enabled for this exact transition.',
 'Prepared source authorizes construction and qualification only. Specific Architect amendment/continuation/issuance decision remains absent.'],
 'materiality':{'exact_r9_to_r10_attempt_ancestry':'MATERIAL_RELEASE_CHANGE','session_warning_status_corrections':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION_CANDIDATE','profile_payload_budgets_tools_execution_transmission_supervisor':'UNCHANGED'}}
 qb=canonical(q).encode();qh=sha(qb);qr={'authority_id':'sha256:'+qh,'sha256':qh}
 sel=json.loads(s.resolve(A+':terminal-attempt-context'));assert sel['mode']=='PREPARED' and sel['specific_invocation_authorization'] is None;sel['qualification']=qr
 sb=canonical(sel).encode();sh=sha(sb);cat=json.loads(encoded(s.catalog));root=s.root.parent/'qualified-prepared';root.mkdir(mode=0o700)
 fd=_directory(root)
 try:
  for h in {r['sha256'] for r in cat['objects'].values()}:_put(fd,h,(s.root/h).read_bytes())
  _put(fd,qh,qb);_put(fd,sh,sb)
  row=dict(cat['objects'][A+':terminal-attempt-context']);row.update(sha256=qh,evidence=[{'path':str(run/'QUALIFICATION.json'),'sha256':qh}]);cat['objects'][qr['authority_id']]=row
  row=dict(cat['objects'][A+':terminal-attempt-context']);row['sha256']=sh;cat['objects'][A+':terminal-attempt-context']=row
  _put(fd,'catalog.json',canonical(cat).encode());os.fsync(fd)
 finally:os.close(fd)
 final=dict(pub,status='QUALIFIED_PREPARED_NO_INVOCATION_ISSUANCE_AUTHORITY',qualification=qr,
  selected_store={'root':str(root),'catalog_sha256':digest(cat),'applicability':s.applicability},original_dispatch=proposal['dispatch'],specific_Architect_issuance_authorization=None)
 (run/'QUALIFICATION.json').write_bytes(qb);fb=canonical(final).encode();fd=_directory(root.parent)
 try:_put(fd,'QUALIFIED_AUTHORITY_PUBLICATION.json',fb);os.fsync(fd)
 finally:os.close(fd)
 (O/'CURRENT_PIN.json').write_text(canonical({'path':str(root.parent/'QUALIFIED_AUTHORITY_PUBLICATION.json'),'sha256':sha(fb)}));(O/'AUTHORITY_PUBLICATION.json').write_bytes(fb)
 (O/'HISTORICAL_PRESERVATION.json').write_text(canonical({'result':'PASS','hashes':history,'original_supervisor_implementation':historical['identity'],'real_r10_effects':0}))
 # Reviewable full delta, classified separately; no edits to production runtime.
 changed={};diff='';baseline=Path('/tmp/forge-r9-context-69itwolf/adapter')
 for f in sorted((runtime_root/'adapter').glob('*.py')):
  prior=(baseline/f.name).read_bytes() if (baseline/f.name).exists() else b''
  if prior!=f.read_bytes():
   target=O/'candidate/adapter'/f.name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(f.read_bytes())
   changed[f.name]={'before':sha(prior) if prior else None,'after':sha(f.read_bytes()),'classification':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION' if f.name in ('orchestration_boundary.py','operator_projection.py','run_control.py') else 'MATERIAL_ATTEMPT_TRANSITION_IMPLEMENTATION'}
   diff+=''.join(difflib.unified_diff(prior.decode().splitlines(True),f.read_text().splitlines(True),fromfile='released-r9/'+f.name,tofile='candidate-r10/'+f.name))
 (O/'IMPLEMENTATION_DELTA.json').write_text(canonical({'runtime':runtime,'changes':changed,'applied':False}));(O/'IMPLEMENTATION.patch').write_text(diff)
 for f in runtime_root.glob('*.py'):shutil.copyfile(f,O/f.name)
 print(canonical({'qualification':qr,'publication':final['status'],'candidate_release':final['release_authority']}))
s.close()
