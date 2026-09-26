"""Evidence-only analysis. Never edits the r12 evidence or runtime."""
import collections,hashlib,json
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parent/'run2_r12_dispatch_2026-09-18'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v):(O/n).write_text(json.dumps(v,indent=2,sort_keys=True))
expected=json.loads((R/'EVIDENCE_HASHES.json').read_bytes())
preserved={name:sha(R/name)==h for name,h in expected.items()}
assert all(preserved.values())
prior=json.loads((R/'HISTORICAL_BASELINE.json').read_bytes())
prior_checks={name:sha(Path(name))==h for name,h in prior.items() if name!='/tmp/kge-forge-e1-invocations.jsonl'}
assert all(prior_checks.values())
terminal=json.loads((R/'TERMINAL_EVIDENCE.json').read_bytes())
assert sha(Path('/tmp/kge-forge-e1-invocations.jsonl'))==terminal['ledger_sha256']
pin=json.loads((R/'CURRENT_PIN.json').read_bytes());assert sha(Path(pin['path']))==pin['sha256']
pub=json.loads(Path(pin['path']).read_bytes())
files={p.name:sha(p) for p in (Path(pub['runtime_root'])/'adapter').glob('*.py')}
candidate={p.name:sha(p) for p in (O/'candidate/adapter').glob('*.py')}
changed={n:{'old_sha256':files.get(n),'new_sha256':candidate.get(n)} for n in sorted(files.keys()|candidate.keys()) if files.get(n)!=candidate.get(n)}
save('IMPLEMENTATION_DELTA.json',{'applied_runtime':pub['runtime_root'],'applied_files':files,'candidate_files':candidate,'changes':changed,'applied':False})
save('HISTORICAL_PRESERVATION.json',{'r12_evidence_files':preserved,'prior_immutable_files':prior_checks,'ledger_matches_r12_terminal':True,'current_publication':pin,'runtime_identity':'sha256:'+hashlib.sha256(json.dumps(files,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'r13_created':False})
spans=json.loads((R/'PHASE_TIMING.json').read_bytes())['spans'];costs={}
for n in sorted({s['name'] for s in spans}):
 selected=[s for s in spans if s['name']==n];costs[n]={'calls':len(selected),'seconds_total':sum(s['seconds'] for s in selected),'max_seconds':max(s['seconds'] for s in selected),'inclusive_nested':True}
save('R12_COSTS.json',costs)
unknown=[]
for f in sorted((R/'operator_status').glob('*.json')):
 row=json.loads(f.read_bytes())
 if row['freshness']!='UNKNOWN':continue
 end=row['projection_generated'];start=end-row['projection_seconds']
 overlap=[{'operation':s['name'],'depth':s['depth']} for s in spans if s['start_wall']<end and s['end_wall']>start]
 cause=row['uncertainty']
 unknown.append({'file':str(f),'sha256':sha(f),'reported_cause':cause,'seconds':row['projection_seconds'],
 'classification':('MISSING_SOURCE_BEFORE_ISSUANCE' if 'FileNotFound' in cause else 'WHOLE_AUDIT_OR_LEDGER_SNAPSHOT_CHANGED' if cause=='UNSTABLE_SNAPSHOT' else 'PROJECTION_EXCEEDED_DEADLINE'),
 'cause_limit':('Exception did not retain the missing filename.' if 'FileNotFound' in cause else 'Original projection did not retain per-retry audit/ledger hashes; exact changed byte/source cannot be proved.' if cause=='UNSTABLE_SNAPSHOT' else '30-second projection deadline expired; per-retry inner timings were not retained.'),
 'overlapping_durable_operations':overlap})
save('UNKNOWN_STATUS_ANALYSIS.json',unknown)
phase={'pre_issuance':26.556,'activation':58.319,'independent_ACTIVE_recovery':69.358,'dispatcher_recovery':56.707,'host_construction':65.667}
save('R12_PHASES.json',{'historical_measurements_preserved':phase,'sum_named_phases_seconds':sum(phase.values()),'model_request_ready':False,'provider_requests':0,'budget_soft_warnings':5,'no_progress_hard_exhaustions':1})
nodes=[
 ('release_decision','IMMUTABLE_AND_ALREADY_VERIFIED','Original release, all applied material decisions, dispatch, exact runtime inventories','Before use and on dependency change','Raw byte hashes and private catalog pin','Each decision/projection/authorization verifier','attempt_history_decision'),
 ('historical_capture','IMMUTABLE_AND_ALREADY_VERIFIED','r8/r9/r10/r11 closed audits, original runtime inventories, captures, source pins','Fresh existence/content/placement; pure parsing may be reused','Original independently reconstructed captures','Every governance verify; repeated in projection/lifecycle/host','attempt_history_historical_capture'),
 ('attempt_ancestry','MUTABLE_REQUIRES_FRESH_CHECK','Ordered pinned predecessors plus CURRENT owner, scope and candidate head','Current facts on every authority gate','No owner/scope verdict may be cached','Every governance verify','attempt_history_ancestry'),
 ('catalog','REDUNDANT_DUPLICATE','Externally pinned catalog bytes and current root/private-state placement','Fresh bytes/placement every access; redundant hash may be replaced by exact byte equality','Previously hash-verified exact bytes, not caller PASS','Every resolve, state_path, require, witness','CURRENT_PROFILE.txt'),
 ('projection','MUTABLE_REQUIRES_FRESH_CHECK','Clearance, committed content, tool contract, current binding and repository inputs','Fresh mutable inputs; immutable derivation may be reused by identity','Released payload and projection fingerprints','dispatch binding, context verification, host, reasoning preparation','model_projection'),
 ('lifecycle','TRANSACTION_SPECIFIC','Ordered authorization audit and exact transaction prefix','At each transition under transaction fence','INACTIVE/intent/ACTIVE/terminal evidence','activation, recovery, host and handoff','activation_recovery'),
 ('ownership','MUTABLE_REQUIRES_FRESH_CHECK','Current ledger inode/content; exact attempt reservation; scope','Every reserve/recovery/handoff/cancel','Historical release is not current absence proof','All lifecycle gates','activation_recovery'),
 ('supervisor','MUTABLE_REQUIRES_FRESH_CHECK','Exact S3 birth/socket/cgroup/workspace/credentials plus authenticated succession','Fresh at required readiness gates','Immutable launch/decision verification can be separated from live observations','Production validator calls frozen peer with full bootstrap','fresh_supervisor'),
 ('telemetry','REDUNDANT_DUPLICATE','Audit prefix plus telemetry chain and durable ordering','Fresh byte prefix and suffix; no authority from telemetry','Verified prefix could support parsing reuse, not yet implemented','Every span entry/exit/warning/status','events'),
 ('remaining','UNKNOWN','Uninstrumented parent work, I/O contention and observer cost','Requires full staged end-to-end spans','No estimate is authorization or performance PASS','Gaps between nested historical timing records','UNKNOWN')]
save('DEPENDENCY_GRAPH.json',{'nodes':[dict(zip(('id','classification','input_identities','freshness','previous_verified_result','duplicate_sites','duration_source'),n)) for n in nodes],
 'edges':[['release_decision','historical_capture'],['historical_capture','attempt_ancestry'],['catalog','release_decision'],['catalog','historical_capture'],['attempt_ancestry','projection'],['projection','lifecycle'],['ownership','lifecycle'],['supervisor','lifecycle'],['lifecycle','telemetry']],
 'current_context':pub['operational_identities'],'qualification_note':'Graph records dependencies, not a new source of authority.'})
print(json.dumps({'changed_files':list(changed),'historical_files_verified':len(preserved),'unknown_observations':len(unknown)}))
