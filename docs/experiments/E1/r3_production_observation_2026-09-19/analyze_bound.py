"""Read-only aggregate of measured qualification evidence, no authority claims."""
import json,hashlib,collections
from pathlib import Path
O=Path(__file__).resolve().parent
pubs=json.loads((O/'QUALIFICATION_BINDINGS.json').read_text());summary=[]
for p in pubs:
 root=Path(p['audit']).parent
 if not (root/'PATH_RESULT.json').exists():continue
 result=json.loads((root/'PATH_RESULT.json').read_text());rows=[json.loads(x) for x in Path(p['audit']).read_text().splitlines()]
 timings=[json.loads(x) for x in (root/'qualification-phases.jsonl').read_text().splitlines()]
 status=[json.loads(x) for x in (root/'STATUS.jsonl').read_text().splitlines()];stack=[];spans=[]
 for r in rows:
  if r.get('event')=='span_start':stack.append(r)
  elif r.get('event')=='span_end' and stack:
   a=stack.pop();spans.append({'name':a['details']['name'],'start':a['monotonic'],'end':r['monotonic'],'seconds':r['monotonic']-a['monotonic'],'nesting':len(stack)})
 ready=next((r for r in rows if r.get('event')=='model_request_ready'),None);prep=next((r for r in rows if r.get('event')=='preparation_start'),None)
 dispatcher_start=next((r['monotonic'] for r in timings if r.get('phase')=='dispatcher_to_ready_or_stop' and r['event']=='phase_start'),None)
 dispatcher=[r for r in spans if r['nesting']==0 and dispatcher_start is not None and r['start']>=dispatcher_start and ready and r['end']<=ready['monotonic']]
 phase_limits=[r['seconds'] for r in result['phases']]+[r['seconds'] for r in dispatcher]
 preparation=ready['monotonic']-prep['monotonic'] if ready and prep else None
 if preparation is not None:phase_limits.append(preparation)
 terminal=next((r for r in reversed(rows) if r.get('resulting_state')=='CANCELLED'),None)
 final_status=status[-1] if status else {}
 violations=[r for r in rows if r.get('event') in ('model_request_start','transport_start','model_request_content_bound','action_request','action_result','execution_scope_created','repository_effect','knowledge_effect','implementation_effect')]
 own=json.loads(root.joinpath('ownership.jsonl').read_text().splitlines()[-1]) if root.joinpath('ownership.jsonl').stat().st_size else None
 one={'case':p['name'],'authorization_id':p['authorization_id'],'qualification_only':True,'result':result['result'],
   'phases':result['phases'],'dispatcher_spans':dispatcher,'model_cycle_preparation_seconds':preparation,
   'cumulative_model_request_ready_seconds':result.get('cumulative_model_request_ready_seconds'),'maximum_individual_phase_seconds':max(phase_limits),
   'performance_pass':bool(ready) and max(phase_limits)<30 and result['cumulative_model_request_ready_seconds']<240,
   'freshness_counts':dict(collections.Counter(r.get('freshness') for r in status)),
   'status_samples':[{'generated':r['projection_generated'],'freshness':r.get('freshness'),'cause':r.get('uncertainty') or r.get('activity_uncertainty') or 'CURRENT_AUTHENTICATED_EVIDENCE','lifecycle':r.get('lifecycle_state'),'ownership':r.get('ownership'),'subphase':r.get('current_subphase'),'operational_state':r.get('operational_state'),'cycle':r.get('cycle'),'activity_freshness':r.get('activity_freshness'),'seconds':r.get('projection_seconds')} for r in status],
   'max_status_seconds':max((r.get('projection_seconds',0) for r in status),default=0),
   'terminal_status':{k:final_status.get(k) for k in ('freshness','lifecycle_state','ownership','architectural_state','uncertainty')},
   'terminal_recovery':result.get('terminal_recovery'),'last_ownership_event':own,
   'warnings':[r for r in rows if r.get('event')=='budget_warning'],'exhaustion':[r for r in rows if r.get('event')=='budget_exhausted'],
   'substantive_progress_events':sum(r.get('event')=='substantive_progress' for r in rows),'forbidden_real_request_effect_records':len(violations),
   'audit_sha256':hashlib.sha256(Path(p['audit']).read_bytes()).hexdigest(),'audit_path':p['audit']}
 if terminal:
  observation=next((r for r in status if r.get('lifecycle_state')=='CANCELLED' and r.get('ownership')=='RELEASED'),None)
  closed=[r for r in rows if r.get('event')=='admission_closed'];final=[r for r in rows if r.get('event')=='final_disposition']
  if observation and closed and final:
   one['terminal_projection_convergence_seconds_bounds']={'lower':max(0,observation['projection_generated']-final[-1]['wall_time']),'upper':max(0,observation['projection_generated']-closed[-1]['wall_time']),'basis':'terminal append/release bounded by admission_closed and final_disposition; lifecycle record has no fabricated timestamp'}
 if ready and dispatcher:
  one['dispatcher_precontrol_bootstrap_seconds']=dispatcher[0]['start']-dispatcher_start
  one['dispatcher_other_controller_glue_seconds']=ready['monotonic']-dispatcher_start-sum(r['seconds'] for r in dispatcher)-(dispatcher[0]['start']-dispatcher_start)
 summary.append(one)
(O/'PRODUCTION_MEASUREMENTS.json').write_text(json.dumps({'schema':'BOUND-PRODUCTION-QUALIFICATION-MEASUREMENTS-1','samples':summary},indent=2))
print(json.dumps([{k:s.get(k) for k in ('case','result','cumulative_model_request_ready_seconds','model_cycle_preparation_seconds','maximum_individual_phase_seconds','performance_pass','freshness_counts','terminal_status')} for s in summary],indent=2))
