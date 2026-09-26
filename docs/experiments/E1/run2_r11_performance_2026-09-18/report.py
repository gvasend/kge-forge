import json,hashlib
from pathlib import Path
O=Path(__file__).parent
load=lambda n:json.loads((O/n).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
pub=load('QUALIFIED_PUBLICATION.json');pre=load('PREFLIGHT.json');recovery=load('INDEPENDENT_RECONSTRUCTION.json');sealed=load('SEALED_PRODUCTION_PREFLIGHT.json');app=load('PERFORMANCE_APPLICABILITY.json')
pin=load('CURRENT_PIN.json');assert sha(Path(pin['path']).read_bytes())==pin['sha256']
assert recovery['identities']==pub['operational_identities'] and recovery['release_authority']==pub['release_authority']
assert sealed['publication']==pin and sealed['result']=='PASS'
warm=[r['seconds'] for r in pre['diagnostics'] if r['operation'].startswith('warm_preissuance_production_validation')]
cold=next(r['seconds'] for r in pre['diagnostics'] if r['operation']=='cold_preissuance_production_validation')
assert len(warm)==3 and max(warm)<30 and sealed['validation_seconds']<30
assert not any(r['hard_exceeded'] for r in pre['diagnostics'])
assert recovery['owner'] is None and recovery['scope'] is None and recovery['handoff_eligible'] is False
assert recovery['host']['SupervisorInstanceId']=='SupervisorInstance-sha256:83f22718a56ab733257208c6e1dfe9767a95e0d10b82f8583f222f88ee9669a2'
assert not Path(pub['audit']).parents[2].exists()
assert sha((O/'PROPOSED_R11_BINDING.json').read_bytes())=='50cd9be1a0f068ae05506380e3b8847820438098e48d345e5c70e56225694887'
base=load('PRESERVATION_BASELINE.json');base.update(load('HISTORICAL_BASELINE.json'))
assert all(sha(Path(p).read_bytes())==h for p,h in base.items())
for n in ('SYNTHETIC_FINAL_NEW.log','ACTUAL_NEW.log','SYNTHETIC_GRANT.log','HOST_REGRESSIONS.log','PERFORMANCE_TESTS_FINAL.log'):assert (O/n).read_text().rstrip().endswith('OK')
assert load('NEGATIVE_CONTEXT.json')['result']=='PASS'
r={'result':'RUN2_R11_READY_FOR_ARCHITECT_ISSUANCE','functional_qualification':'PASS','performance':'PASS',
 'optimization_classification':'NON_MATERIAL_IMPLEMENTATION_CONTINUATION_CANDIDATE','new_authoritative_checkpoint':False,'history_capture_identity':app['history_content_identity'],
 'authority_status':'PREPARED_ONLY_NOT_ADOPTED_NOT_ISSUED','candidate_id':pub['authorization_id'],'candidate_binding_sha256':pub['proposal']['sha256'],
 'candidate_binding_unchanged':True,'qualified_prepared_publication':pin,'implementation':pub['controller_runtime_identity'],
 'proposed_amendment_id':pub['amendment_id'],'proposed_amendment_file_sha256':pub['amendment']['sha256'],
 'proposed_continuation_id':pub['continuation_id'],'proposed_continuation_file_sha256':pub['continuation']['sha256'],
 'proposed_release_authority':pub['release_authority'],'proposed_operational_ancestry':pub['operational_identities'],'proposed_context_identities':pub['context_identities'],
 'currently_applied_release_authority':app['applied_release_unchanged'],
 'currently_applied_OperationalContextId':'E1-OPERATIONAL-CONTEXT-sha256:109c1fb95fee2e95f58cce8ca7723384092706fa33a4ef7ec051abfdcacea125',
 'currently_applied_chain_digest':'c34a47deb5b0c8ffc3839fd3520a10e1eeb065f6a9e4d4b4e180945c9cb22483',
 'timing':{'cold_validation':cold,'warm_validation':warm,'sealed_validation':sealed['validation_seconds'],'independent_cold_reconstruction':recovery['seconds'],'private_bootstrap':sealed['bootstrap_seconds'],'phase_soft_seconds':30,'phase_hard_seconds':120},
 'supervisor':recovery['host'],'ownership':'NONE','execution_scope':'NONE','audit_namespace':'ABSENT_UNUSED',
 'budgets':'UNCHANGED_PASS','status_qualification':'PASS_NON_E1_FIXTURE','preserved_files':len(base),
 'issued':False,'activated':False,'real_r11_model_requests':0,'real_r11_effects':0,'dispatched':False,'remaining_authority_gate':'Architect adoption of exact prepared amendment/continuation and specific r11 issuance authorization'}
(O/'FINAL_RESULT.json').write_text(json.dumps(r,sort_keys=True,indent=2))
spans=sealed['spans'];peer=sum(s['seconds'] for s in spans if s['operation']=='fresh_supervisor_peer');projections=sum(s['seconds'] for s in spans if s['operation']=='model_projection')
scale=load('COMPLEXITY.json')['results']
lines=['# r11 validation performance closure','',r['result'],'',
'Functional qualification PASS. Three final warm production samples and sealed-store validation are below the unchanged 30-second soft threshold. No required production phase exceeded 120 seconds. No issuance, activation, reservation, model request or dispatch occurred.','',
'## Root cause and correction','',
'The profiled baseline spent 25.026 seconds in 1,260 catalog checks, including 18.458 seconds in repeated private-placement predicates. Repeated historical-store construction reparsed and froze the same pinned catalogs. The three model projections repeated that work. Profiling overhead is excluded from acceptance samples.','',
'The staged correction shares canonical grant resolution and component comparisons within each fresh placement predicate. It reuses parsed pinned historical catalogs only for one production validation operation. Each borrow rechecks the catalog hash, applicability and placement; every historical witness object, audit, runtime inventory and mutable context input is still read and hashed. Current ownership, scopes, lifecycle, namespace, selected ancestry and genuine supervisor readiness remain fresh. Exceptions close every borrowed store; nested authority sessions still fail closed.','',
'No new authoritative checkpoint or stored PASS is introduced. The existing authenticated historical capture remains unchanged: `'+app['history_content_identity']+'`. This is deliberately conservative reuse of parsed immutable structure, not constant-time authorization from a summary.','',
'## Qualification','',
'86 test methods passed: 16 performance/freshness probes, 24 integrated non-E1 lifecycle/session/status/budget tests, 8 actual historical-identity tests, 6 specific-grant tests and 32 host regressions. The actual-context suite also rejected 19 substituted/missing authority cases. The outer sandbox initially prevented the bubblewrap namespace test; all 32 regressions subsequently passed on the host.','',
'Tamper, missing data, reordered/substituted predecessors, disposition/effect/ownership changes, wrong dispatch/context bindings, unknown head, stale catalog/applicability, changed grants/private paths and permissions fail closed. Fresh ownership/scope changes are observed between repeated calls. New-process reconstruction reproduces the exact sealed prepared context from pinned private objects and original evidence. See HISTORY_QUALIFICATION_MATRIX.json for all 16 requested history requirements; no new sufficient checkpoint is being qualified.','',
'## Production timing','',
'| Operation | Seconds |','|---|---:|',f'| Cold private bootstrap (sealed) | {sealed["bootstrap_seconds"]:.3f} |',f'| Cold production validation | {cold:.3f} |']
lines += [f'| Warm production validation {i+1} | {t:.3f} |' for i,t in enumerate(warm)]
lines += [f'| Sealed-store validation | {sealed["validation_seconds"]:.3f} |',f'| Independent cold reconstruction | {recovery["seconds"]:.3f} |','',
f'The sealed validation allocates {peer:.3f}s to the unchanged fresh supervisor peer and {projections:.3f}s to three complete model projections. The remaining {sealed["validation_seconds"]-peer-projections:.3f}s covers other controller predicates, store/context/dispatch/history checks and observation bookkeeping. Nested history spans must not be added again to enclosing projection spans. FINAL_PROFILE_SUMMARY.json accounts for native catalog hashing and resolver work; PRE_ISSUANCE_DIAGNOSTICS.json preserves correlated wall/monotonic spans. No interval is attributed to a model/provider.','',
'## Complexity','',
'The representative synthetic hash-linked history kernel uses the real private store and eight validation passes per operation. It is not a substitute for the production timings above.','',
'| Attempts | Complete catalog reconstruction median | Operation-scoped reuse median |','|---:|---:|---:|']
for row in scale:lines.append(f'| {row["attempts"]} | {row["measurements"]["complete_catalog_reconstruction"]["median"]:.4f}s | {row["measurements"]["operation_scoped_catalog_reuse"]["median"]:.4f}s |')
lines += ['','Complete historical-byte verification remains approximately linear over the measured range. Catalog parsing is once per distinct store per operation, rather than once per recursive use. No constant-time guarantee is claimed. This closes the current production threshold without changing what historical evidence is sufficient; very large ancestry will still require measurement.','',
'## Applicability and exact candidate','',
'Performance-only changes are a NON_MATERIAL_IMPLEMENTATION_CONTINUATION candidate: equivalent fresh placement checks, parsed pinned-catalog reuse and non-authorizing spans. The already-proposed material attempt-chain policy/capture representation is kept separate and remains unadopted. Performance artifacts are compared with the accepted functional candidate; they are not mislabeled as a non-material introduction of the entire new attempt policy.','',
'Candidate: `'+pub['authorization_id']+'`. Binding SHA-256: `'+pub['proposal']['sha256']+'`. Both remain unchanged. Its binding pins the applied predecessor and unchanged task/profile/payload/budget/dispatch/supervisor invariants. The complete new prepared runtime, effective amendment/continuation and context identities are recomputed below; accepting the old proposal does not by itself authorize these records.','',
'| Prepared record (not applied) | Exact identity |','|---|---|',
'| Implementation | `'+pub['controller_runtime_identity']+'` |',
'| Material amendment | `'+pub['amendment_id']+'` |',
'| Amendment file SHA-256 | `'+pub['amendment']['sha256']+'` |',
'| Implementation continuation | `'+pub['continuation_id']+'` |',
'| Continuation file SHA-256 | `'+pub['continuation']['sha256']+'` |',
'| Resulting release authority | `'+pub['release_authority']+'` |']
for k,v in pub['operational_identities'].items():lines.append('| '+k+' | `'+v+'` |')
for k,v in pub['context_identities'].items():lines.append('| '+k+' | `'+v+'` |')
lines += ['','The currently applied release remains `'+r['currently_applied_release_authority']+'`, with context `'+r['currently_applied_OperationalContextId']+'` and chain `'+r['currently_applied_chain_digest']+'`. No prepared record was adopted.','',
'## Current state and preservation','',
'S3 remains exact and READY: `'+recovery['host']['SupervisorInstanceId']+'`, succession `'+recovery['host']['SupervisorSuccessionHead']+'`. Fresh verification observes PID 1465900 / PPID 1465890 and the qualified socket/cgroup/workspace identity. Ownership NONE; ExecutionScope NONE; r11 namespace ABSENT. The qualified status/budget regressions pass; no live r11 status is claimed for an unissued invocation.','',
f'{len(base)} historical files, including prior qualification, r8/r9/r10 records and shared-ledger evidence, hash unchanged. r10 remains CANCELLED / INTERRUPTED_NO_EFFECTS. Zero real r11 model requests, ActionRequests, executions or implementation effects.','',
'The next step remains an Architect decision covering the exact prepared records and r11 issuance. No automatic invocation or retry is authorized.','']
(O/'REPORT.md').write_text('\n'.join(lines))
files={str(p.relative_to(O)):sha(p.read_bytes()) for p in O.rglob('*') if p.is_file() and '__pycache__' not in str(p) and p.name!='EVIDENCE_HASHES.json'}
(O/'EVIDENCE_HASHES.json').write_text(json.dumps(files,sort_keys=True,indent=2))
print(json.dumps({'result':r['result'],'timing':r['timing'],'release':r['proposed_release_authority'],'context':r['proposed_operational_ancestry']['OperationalContextId']}))
