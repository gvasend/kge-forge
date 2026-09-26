"""Evidence-only post-run assessment; no model/lifecycle mutation."""
import json,hashlib,time
from pathlib import Path
from datetime import datetime,timezone,timedelta
from adapter.context_projection import canonical,sha
from adapter.run_control import events,status
O=Path('/home/gvasend/app/kge-forge/docs/experiments/E1/run2_r9_dispatch_2026-09-18')
def load(n):return json.loads((O/n).read_bytes())
pin=load('CURRENT_PIN.json');b=Path(pin['path']).read_bytes();assert sha(b)==pin['sha256'];p=json.loads(b);audit=Path(p['audit']);rows=events(audit)
cancel=load('CANCELLATION.json');recovery=load('INDEPENDENT_TERMINAL_RECOVERY.json');assert recovery['lifecycle_state']=='CANCELLED' and recovery['ownership'] is None and not recovery['handoff_eligible'] and not recovery['reconciliation_required']
counts={name:sum(r.get('event')==name for r in rows) for name in ('model_request_start','model_request_content_bound','response_received','action_request','action_result','execution_scope_created','authority_expansion')};assert not any(counts.values())
q=json.loads((O.parent/'run2_attempt_authority_2026-09-18/candidate6/QUALIFICATION.json').read_bytes())
historical={k:sha(Path(k).read_bytes())==v for k,v in q['historical_hashes'].items() if k!='/tmp/kge-forge-e1-invocations.jsonl'};assert all(historical.values())
impl=json.loads((O.parent/'run2_nonhost_closure_2026-09-17/FINAL_IMPLEMENTATION.json').read_bytes());assert all(sha(Path(k).read_bytes())==h for k,h in impl['inventory'].items())
timing=[r for r in rows if r.get('schema')=='E1-RUN-CONTROL-1'];stack=[];spans=[];warnings=[]
for r in timing:
 if r['event']=='span_start':stack.append(r)
 elif r['event']=='span_end':
  start=stack.pop();assert start['details']['name']==r['details']['name'];spans.append({'name':start['details']['name'],'start_wall':start['wall_time'],'end_wall':r['wall_time'],'seconds':r['monotonic']-start['monotonic'],'nested':bool(stack),'start_sequence':start['sequence'],'end_sequence':r['sequence']})
 elif r['event'] in ('budget_warning','budget_exhausted'):
  w={'event':r['event'],'wall_time':r['wall_time'],'details':r['details'],'sequence':r['sequence']}
  if stack and r['details']['budget']=='phase':w['warning_record_delay_seconds']=r['monotonic']-stack[0]['monotonic']-r['details']['value']
  warnings.append(w)
assert not stack
trace=[]
for i,r in enumerate(rows):
 row={'audit_index':i+1,'event':r['event'],'record_sha256':sha(canonical(r).encode())}
 for k in ('event_id','resulting_state','action_request_id','wall_time','monotonic','sequence'):
  if k in r:row[k]=r[k]
 trace.append(row)
(O/'EVENT_TRACE.json').write_text(canonical(trace));(O/'PHASE_TIMING.json').write_text(canonical(spans));(O/'BUDGET_HISTORY.json').write_text(canonical(warnings))
start=json.loads((Path(p['private_run_root'])/'ONE_ATTEMPT_STARTED').read_bytes());stop=load('ORCHESTRATION_STOP.json')
observations=[]
for name in ('IMMEDIATE_PRE_ISSUANCE.json','ATTEMPT_ALLOCATION.json','INACTIVE_ISSUANCE.json','INDEPENDENT_INACTIVE_RECOVERY.json','ACTIVE_COMMIT.json','INDEPENDENT_ACTIVE_RECOVERY.json','ORCHESTRATION_STOP.json','INDEPENDENT_STOP_RECOVERY_FAILURE.json','CANCELLATION.json','INDEPENDENT_TERMINAL_RECOVERY.json'):
 v=load(name);observations.append({'event':name,'known_observation_wall_time':v['wall_time'],'local_EDT':datetime.fromtimestamp(v['wall_time'],timezone(timedelta(hours=-4))).isoformat(),'evidence_sha256':sha((O/name).read_bytes())})
coverage={f'WP1-AC{i:02}':{'result':'NOT_EXERCISED','reason':'Invocation stopped before the first Programmer request; no implementation or work-package tests.'} for i in range(1,10)}
result={'invocation_authorization_id':p['r9_authorization_id'],'disposition':'CANCELLED','classification':'INTERRUPTED_NO_EFFECTS','outcome_kind':'CONTROLLER_ORCHESTRATION_FAILURE_NOT_PROGRAMMER_OUTCOME',
 'root_cause':{'reason':'nested authority selection forbidden','exception':'AuthorityDenied','caller':'run.py:70 invokes controlled_dispatch.dispatch inside an existing store.session()','callee':'controlled_dispatch.dispatch opens its own store.session(); controller_authority_store.session rejects nesting before entering the body','production_code_modified':False,'retry_performed':False},
 'independent_terminal_recovery':recovery,'ownership':'RELEASED','scope':'NONE','architectural_state':'QUIESCENT','model_handoff_eligible':False,
 'counts':counts,'model_cycles':0,'provider_wait_seconds':None,'provider_wait_reason':'NOT_ENTERED','usage':'USAGE_UNKNOWN','usage_reason':'No model request was initiated; no provider usage was returned; no enforced token ceiling claimed.',
 'budget_history':warnings,'hard_budget_exhaustions':0,'phase_timing':spans,'timing_observations':observations,
 'elapsed_seconds':{'controller_entry_to_dispatch_failure':stop['controller_elapsed'],'controller_entry_to_durable_cancellation_observation':cancel['wall_time']-start['wall_time'],'controller_entry_to_independent_terminal_recovery':recovery['wall_time']-start['wall_time']},
 'implementation_produced':None,'authoritative_repository_changes':[],'canonical_knowledge_changes':[],'work_package_tests':[],'acceptance_coverage':coverage,
 'governance_checks':['Exact r9 authority, ancestry and live S3 readiness PASS before issuance','Durable original INACTIVE first; independent INACTIVE and no ownership PASS','Qualified intent/reservation/ACTIVE transaction PASS','Independent ACTIVE+OWNED+current bindings+READY recovery PASS','Nested authority-session guard rejected orchestration before model handoff','Admission remained closed; typed interruption/cancellation released ownership','Independent CANCELLED+NO_OWNERSHIP recovery PASS'],
 'execution_quiescence':{'execution_scopes':0,'active_execution_ownership':False,'governed_interruption_recorded':True,'architectural_QUIESCENT_recorded':True,'supervisor_terminate_required':False},
 'denials':[{'layer':'controller authority-store session selection','reason':'nested authority selection forbidden','Programmer_ActionRequest':False}],
 'corrective_Programmer_behavior':'NOT_EXERCISED','authority_expansion_requests':[],
 'recovery_history':['Independent INACTIVE reconstruction PASS','Independent ACTIVE+OWNED reconstruction PASS','Dispatch composition failed before model request','Provisional INDETERMINATE telemetry and durable admission closure preserved','Immediate stop recovery failed; no ownership release inferred','Governed interruption + typed cancellation established QUIESCENT and released ownership','Independent terminal recovery PASS'],
 'uncertainty':{'persistent_effects':'NONE_UNRESOLVED','ownership':'RESOLVED_RELEASED','provider':'NO_R9_MODEL_REQUEST_INITIATED','historical_provisional_indeterminate':'Preserved; superseded by durable cancellation and independent terminal recovery'},
 'observability_anomalies':['Status retained the prior INACTIVE governance observation while ACTIVE commit awaited independent recovery.','The activation-recovery soft warning recorded at approximately 47.39s although its budget value was 30s; a 17.39s delay is observed. Source inspection indicates synchronous telemetry waited on the child recovery audit lock. Hard-deadline behavior under prolonged cross-process lock contention was not exercised.','After admission closed, the status projection retained provisional INDETERMINATE telemetry and later correctly reported stale UNKNOWN; terminal ownership must be read from independent recovery, not that stale projection.'],
 'human_intervention_history':['Specific Architect r9 authorization supplied before this run','Environment approvals permitted exact frozen-controller execution and genuine host observation','No routine Programmer decision, replacement launch, or new invocation was requested','Assistant reconciled the orchestration failure under the authorized governed cancellation/recovery semantics'],
 'historical_Run1_r8_integrity':historical,'released_supervisor_implementation_unchanged':impl['identity'],
 'audit':{'path':str(audit),'sha256':sha(audit.read_bytes()),'records':len(rows)},'activation_event_id':next(r['event_id'] for r in rows if r['event']=='authorization_lifecycle_activated'),
 'reservation_id':load('ACTIVE_COMMIT.json')['reservation']['reservation_id'],'terminal_event_id':cancel['terminal_event_id'],
 'r10_created':False,'automatic_retry':False,'Experiment_1_acceptance':'NOT_ESTABLISHED','E1_WP_001_completion':'NOT_COMPLETED'}
(O/'FINAL_RESULT.json').write_text(canonical(result))
lines=['# E1 Run-2 r9 termination report','','**CANCELLED / INTERRUPTED_NO_EFFECTS. Independent terminal recovery PASS. Ownership RELEASED.**','',
 'This was a controller orchestration failure before the first Programmer request, not a Programmer outcome. The wrapper called `controlled_dispatch.dispatch` while already inside `store.session()`. The dispatcher owns its own session; the existing nested-selection guard correctly rejected the call. No guard or production implementation was modified, and dispatch was not retried.','',
 'r9 completed durable INACTIVE issuance, independent INACTIVE recovery, the qualified activation transaction, and independent ACTIVE+OWNED recovery with current release bindings and S3 READY. Following the orchestration failure, admission closed. The first stop recovery failed and provisional uncertainty was retained. Subsequent governed interruption and typed cancellation established QUIESCENT with no ExecutionScope, released ownership, and passed fresh independent terminal recovery.','',
 '| Measure | Result |','|---|---|','| Model cycles / requests / responses | 0 / 0 / 0 |','| ActionRequests / ActionResults | 0 / 0 |','| Executions / implementation effects | 0 / 0 |','| Ownership | Released; no current reservation |','| ExecutionScope | None |','| Token usage | USAGE_UNKNOWN; no request or provider usage record |','| Provider latency | Not applicable: transport was never entered |','| Implementation / authoritative repository / canonical knowledge changes | None |','| Work-package tests / authority expansion | None |','',
 '| Controller phase | Duration |','|---|---|']
lines += ['| '+r['name']+' | %.3f seconds |'%r['seconds'] for r in spans if not r['nested']]
lines += ['', 'Controller entry to dispatch failure: %.3fs. Durable cancellation was observed %.3fs after controller entry; independent terminal recovery completed at %.3fs.'%(result['elapsed_seconds']['controller_entry_to_dispatch_failure'],result['elapsed_seconds']['controller_entry_to_durable_cancellation_observation'],result['elapsed_seconds']['controller_entry_to_independent_terminal_recovery']),'',
 'Two phase soft warnings occurred. No hard budget exhausted, threshold was extended, or timer reset to continue work. The full activation transaction exceeded the 30-second soft threshold even though the earlier read-only cold/warm validations took approximately 26.8 seconds. Independent activation recovery also exceeded the soft threshold while remaining below 120 seconds.','',
 'The recovery warning was durably recorded about 17.39 seconds after its 30-second threshold value. Synchronous telemetry waiting for the independent recovery process’s audit lock is the source-supported explanation; this was finite contention, not an observed deadlock. Hard-stop behavior under prolonged cross-process contention was not demonstrated by this run.','',
 '| Known observation | EDT timestamp |','|---|---|']
lines += ['| '+v['event']+' | '+v['local_EDT']+' |' for v in observations]
lines += ['', 'The timestamps above are receipt/observation timestamps. They do not invent provider timestamps or exact lifecycle commit wall times where the underlying record lacks one. Detailed durable span timing is in PHASE_TIMING.json.','',
 'All WP1-AC01 through WP1-AC09 acceptance obligations are **NOT EXERCISED**. There is no Programmer completion assessment, implementation, test command/result, or product acceptance evidence. Successful governance transitions do not satisfy the implementation work package.','',
 'Operator-status snapshots distinguish the validation/recovery phases and show zero model/action counts and budget warnings. Two limitations remain visible: the prior INACTIVE governance observation persisted until independent ACTIVE recovery was recorded; and after cancellation the old provisional INDETERMINATE telemetry remained in the closed run-control stream. The projection subsequently returned stale UNKNOWN. The authoritative final state comes from the cancellation event and independent terminal recovery, not the stale projection. Historical telemetry was not rewritten or reopened.','',
 'The exact r8 closed audit and Run-1 audit are unchanged, as are all 39 files of the released supervisor implementation. r9’s allocation, activation, ownership and cancellation remain append-only history. No r10 or replacement invocation was created.','',
 '- Activation: `'+result['activation_event_id']+'`','- Reservation: `'+result['reservation_id']+'`','- Cancellation: `'+result['terminal_event_id']+'`','- Final audit SHA-256: `'+result['audit']['sha256']+'`','',
 'Evidence: [structured result](FINAL_RESULT.json), [event trace](EVENT_TRACE.json), [timing](PHASE_TIMING.json), [budget history](BUDGET_HISTORY.json), [cancellation](CANCELLATION.json), [independent terminal recovery](INDEPENDENT_TERMINAL_RECOVERY.json), and [orchestration failure](ORCHESTRATION_STOP.json). Full authoritative audit remains controller-private.','',
 'No unresolved persistent-effect or ownership uncertainty remains after terminal recovery. No provider request was initiated by r9. Experiment 1 PASS and KGE Forge v0.1 acceptance are not established. Stop for Architect review; no retry is authorized by this report.']
(O/'REPORT.md').write_text('\n'.join(lines)+'\n')
(O/'EVIDENCE_HASHES.json').write_text(canonical({str(f.relative_to(O)):sha(f.read_bytes()) for f in sorted(O.rglob('*')) if f.is_file() and f.name!='EVIDENCE_HASHES.json'}))
print(canonical({'disposition':result['disposition'],'classification':result['classification'],'ownership':result['ownership'],'model_requests':counts['model_request_start'],'report_sha256':sha((O/'REPORT.md').read_bytes())}))
