"""Read-only terminal reconciliation and policy-safe experiment evidence."""
import json,sys,time,os,hashlib
from pathlib import Path
O=Path(__file__).parent
pin=json.loads((O/'CURRENT_PIN.json').read_bytes());b=Path(pin['path']).read_bytes();assert hashlib.sha256(b).hexdigest()==pin['sha256'];p=json.loads(b);sys.path.insert(0,p['runtime_root'])
from adapter.context_projection import canonical,sha
from adapter.controller_authority_store import ControllerAuthorityStore,_directory,_put
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.authorization_lifecycle import reconstruct
from adapter.recovery_ledger import reconstruct as recover_actions
from adapter.attempt_ownership import observe
from adapter.run_control import events
from adapter.operator_projection import project
s=ControllerAuthorityStore(**p['selected_store']);B=Path(p['private_run_root']);audit=Path(p['audit'])
def save(n,v):
 b=canonical(v).encode();fd=_directory(B)
 try:_put(fd,n,b);os.fsync(fd)
 finally:os.close(fd)
 (O/n).write_bytes(b)
try:
 with s.session():
  a=reconstruct_authorization(s,p['authorization_id']);raw=audit.read_bytes();rows=events(audit);life=reconstruct(raw,a,audit);actions=recover_actions(audit,a);owner,scope,ledger=observe(a.ownership_ledger)
  counts={k:sum(r.get('event')==v for r in rows) for k,v in {'model_requests':'model_request_start','model_responses':'response_received','model_content_bindings':'model_request_content_bound','ActionRequests':'action_request','ActionResults':'action_result','ExecutionScopes':'execution_scope_created'}.items()}
  trace=[{'index':i,'event':r.get('event'),'schema':r.get('schema'),'monotonic':r.get('monotonic',r.get('time')),'wall_time':r.get('wall_time'),'record_sha256':sha(canonical(r).encode()),'lifecycle_event_id':r.get('event_id'),'action_request_id':r.get('action_request_id'),'operation':r.get('type'),'result':r.get('result')} for i,r in enumerate(rows)]
  save('EVENT_TRACE.json',trace)
  safe_actions=[{'action_request_id':r.get('action_request_id'),'event':r['event'],'operation':r.get('type'),'result':r.get('result'),'request_sha256':r.get('request_sha256'),'argument_evidence':r.get('argument_evidence'),'result_sha256':r.get('digest'),'record_sha256':sha(canonical(r).encode())} for r in rows if r.get('event') in ('action_request','action_result')]
  save('ACTION_TRACE.json',safe_actions)
  control=[r for r in rows if r.get('schema')=='E1-RUN-CONTROL-1'];pending=[];spans=[]
  for r in control:
   if r['event']=='span_start':pending.append(r)
   elif r['event']=='span_end':
    st=pending.pop();assert st['details']['name']==r['details']['name']
    spans.append({'name':r['details']['name'],'cycle':r['cycle'],'start_wall':st['wall_time'],'end_wall':r['wall_time'],'seconds':r['monotonic']-st['monotonic'],'depth':len(pending),'start_sequence':st['sequence'],'end_sequence':r['sequence']})
  save('PHASE_TIMING.json',{'spans':spans,'unfinished_spans':[{'name':r['details']['name'],'sequence':r['sequence']} for r in pending]})
  save('BUDGET_HISTORY.json',[r for r in control if r['event'] in ('budget_warning','warning_persisted','budget_exhausted','admission_closed')])
  usage=[r['details'] for r in control if r['event']=='response_received'];save('USAGE.json',{'responses':usage,'token_budget_state':'USAGE_UNKNOWN','provider_compute_seconds':'UNKNOWN'})
  quiet=scope is None and actions['scope'] is None and not actions['incomplete']
  reconciled=life['state'] in ('CANCELLED','COMPLETED','REVOKED') and not life['uncertain'] and owner is None and quiet
  noneffect=not any(counts[k] for k in ('model_requests','model_content_bindings','ActionRequests','ExecutionScopes'))
  classification='INTERRUPTED_NO_EFFECTS' if reconciled and life['state']=='CANCELLED' and noneffect else 'INDETERMINATE' if not reconciled else 'RECONCILED_TERMINAL_REQUIRES_EFFECT_ASSESSMENT'
  facts={'lifecycle_state':life['state'],'lifecycle_phase':life['phase'],'classification':classification,'reconciled':reconciled,'ownership':owner,'ExecutionScope':scope,'QUIESCENT':quiet,'lifecycle_uncertainty':life['uncertain'],'counts':counts,'last_event_id':life['last_event_id'],'activation_event_id':life.get('activation_event',{}).get('event_id'),'audit_sha256':sha(raw),'audit_path':str(audit),'ledger_sha256':sha(ledger),'model_cycles':max([r['cycle'] for r in control] or [0]),'budget_warnings':sum(r['event']=='budget_warning' for r in control),'budget_exhaustions':sum(r['event']=='budget_exhausted' for r in control),'final_dispositions':[r['details'] for r in control if r['event']=='final_disposition'],'authority_requests':sum(r.get('type')=='authority_request' for r in rows if r.get('event')=='action_request')}
  save('TERMINAL_EVIDENCE.json',facts)
 status=project(s,a.authorization_id);save('FRESH_TERMINAL_OPERATOR_STATUS.json',status)
 assert raw==audit.read_bytes(),'audit changed during terminal inspection'
 print(canonical({'terminal':facts,'operator_lifecycle':status.get('lifecycle_state'),'operator_freshness':status.get('freshness')}))
finally:s.close()
