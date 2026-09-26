"""Produce policy-safe Architect evidence from the terminated invocation."""
import json,hashlib,datetime,os
from pathlib import Path
O=Path(__file__).parent;root=Path('/home/gvasend/app/kge-forge')
def load(p):return json.loads(Path(p).read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def write(n,v):(O/n).write_text(json.dumps(v,sort_keys=True,indent=2))
pin=load(O/'CURRENT_PIN.json');pub=load(pin['path']);rows=list(map(json.loads,Path(pub['audit']).read_text().splitlines()));facts=load(O/'TERMINAL_EVIDENCE.json')
assert facts['classification']=='INTERRUPTED_NO_EFFECTS' and all(n==0 for n in facts['counts'].values())
assert load(O/'INDEPENDENT_TERMINAL_RECOVERY.json')['lifecycle_state']=='CANCELLED'
write('FIRST_ACTION_MILESTONE.json',{'milestone':'FIRST_REAL_PROGRAMMER_ACTION_REQUEST','status':'NOT_REACHED','model_cycle':None,'operation':None,'authorization_disposition':None,'reason':'Independent ACTIVE recovery failed before dispatcher entry','model_requests':0,'ActionRequests':0})
trace=[{'index':i,'event':r.get('event'),'schema':r.get('schema'),'time':r.get('time'),'wall_time':r.get('wall_time'),'monotonic':r.get('monotonic'),'record_sha256':sha(json.dumps(r,sort_keys=True,separators=(',',':')).encode()),'lifecycle_event_id':r.get('event_id'),'action_request_id':r.get('action_request_id')} for i,r in enumerate(rows)]
write('EVENT_TRACE.json',trace)
control=[r for r in rows if r.get('schema')=='E1-RUN-CONTROL-1'];stack=[];spans=[]
for r in control:
 if r['event']=='span_start':stack.append(r)
 elif r['event']=='span_end':
  start=stack.pop();assert start['details']['name']==r['details']['name']
  spans.append({'operation':r['details']['name'],'cycle':r['cycle'],'start_wall':start['wall_time'],'end_wall':r['wall_time'],'seconds':r['monotonic']-start['monotonic'],'nested_depth':len(stack),'start_sequence':start['sequence'],'end_sequence':r['sequence']})
write('PHASE_TIMING.json',spans);write('BUDGET_HISTORY.json',[r for r in control if r['event'] in ('budget_warning','warning_persisted','budget_exhausted','admission_closed')])
marker=load(Path(pub['private_run_root'])/'ONE_ATTEMPT_STARTED');timeline=[{'event':'DRIVER_START','wall_time':marker['wall_time'],'elapsed':0,'certainty':'KNOWN_DRIVER_MARKER'}]
for n in ('IMMEDIATE_PRE_ISSUANCE.json','INACTIVE_ISSUANCE.json','INDEPENDENT_INACTIVE_RECOVERY.json','ACTIVE_COMMIT.json','INDEPENDENT_ACTIVE_RECOVERY_FAILURE.json','ORCHESTRATION_STOP.json','CANCELLATION.json','INDEPENDENT_TERMINAL_RECOVERY.json'):
 v=load(O/n);timeline.append({'event':n,'wall_time':v['wall_time'],'elapsed':v['controller_elapsed'],'certainty':'KNOWN_REPORT_TIME_AFTER_OPERATION','child_seconds':v.get('seconds')})
for t in timeline:t['EDT']=datetime.datetime.fromtimestamp(t['wall_time'],datetime.timezone(datetime.timedelta(hours=-4))).isoformat(timespec='milliseconds')
write('TIMELINE.json',timeline)
files={}
for n in ('src/kge_forge/__init__.py','src/kge_forge/context','tests/context','docs/implementation/E1-WP-001.md'):
 p=root/n
 if p.is_file():files[n]=sha(p.read_bytes())
 elif p.is_dir():
  for f in p.rglob('*'):
   if f.is_file() and not f.is_symlink():files[str(f.relative_to(root))]=sha(f.read_bytes())
base=load(O/'PRODUCT_BASELINE.json')['files'];changes={k:{'before':base.get(k),'after':files.get(k)} for k in set(base)|set(files) if base.get(k)!=files.get(k)};assert changes=={}
write('PRODUCT_EFFECTS.json',{'implementation_produced':False,'authoritative_product_changes':changes,'canonical_knowledge_changes':[],'governed_tests':[],'execution_scopes':[],'work_package_exercised':False})
write('ACCEPTANCE_COVERAGE.json',{f'WP1-AC{i:02}':{'result':'NOT_EXERCISED','reason':'No Programmer model or action request reached'} for i in range(1,10)})
old=load(root/'docs/experiments/E1/run2_r10_transition_2026-09-18/candidate3/QUALIFICATION.json')['historical_hashes'];ledger='/tmp/kge-forge-e1-invocations.jsonl'
assert all(sha(Path(p).read_bytes())==h for p,h in old.items() if p!=ledger)
data=Path(ledger).read_bytes();prefix=b'';tail=None
for line in data.splitlines(keepends=True):
 prefix+=line
 if sha(prefix)==old[ledger]:tail=data[len(prefix):];break
assert tail is not None;extra=list(map(json.loads,tail.splitlines()));assert [x['event'] for x in extra]==['invocation_reserved','invocation_released']
assert extra[0]['authorization_id']==pub['r10_authorization_id'] and extra[0]['reservation_id']==extra[1]['reservation_id'] and extra[1]['terminal_event_id']==facts['terminal_event_id']
write('HISTORICAL_PRESERVATION.json',{'result':'PASS','immutable_files_checked':len(old)-1,'ownership_ledger_original_prefix_preserved':True,'new_ledger_events':extra,'r8_unchanged':True,'r9_unchanged':True,'Run1_unchanged':True})
write('FINAL_RESULT.json',{'invocation':pub['r10_authorization_id'],'disposition':'CANCELLED','classification':'INTERRUPTED_NO_EFFECTS','independent_terminal_recovery':'PASS','ownership':'RELEASED','architectural_state':'QUIESCENT','ExecutionScope':'NONE',
 'failed_gate':'INDEPENDENT_ACTIVE_RECOVERY','dispatcher_entered':False,'counts':facts['counts'],'model_cycles':0,'first_action_milestone':'NOT_REACHED','implementation_effects':0,'product_changes':0,'knowledge_changes':0,'tests':0,'acceptance_coverage':'WP1-AC01..09 NOT_EXERCISED',
 'token_usage':'USAGE_UNKNOWN','token_usage_detail':'No r10 model requests and no provider usage returned; no asserted token ceiling.',
 'budget_warnings':sum(r['event']=='budget_warning' for r in control),'budget_exhaustions':sum(r['event']=='budget_exhausted' for r in control),'budget_thresholds_changed':False,
 'activation_event':facts['activation_event_id'],'reservation':facts['reservation_id'],'terminal_event':facts['terminal_event_id'],'audit_sha256':facts['audit_sha256'],
 'authority_application':'APPLIED_PRESERVED','release_authority':pub['release_authority'],'OperationalContextId':pub['operational_identities']['OperationalContextId'],
 'provider_processing_duration':'NOT_APPLICABLE_NO_REQUEST','uncertainty':None,'failure_diagnostic_limitation':'Original failed recovery stderr retained only as SHA-256; isolated forensic reproduction and frozen source explain the captured-successor-ownership rejection.',
 'operator_status':'LIVE_OBSERVER_UNKNOWN_DURING_FAILURE; FRESH_TERMINAL_RECONSTRUCTION_CANCELLED_RELEASED_QUIESCENT',
 'operator_interventions':['Corrected observer output directory 0755 to 0700 and restarted read-only observer','Fresh terminal status reconstruction after cached observer remained UNKNOWN'],
 'authority_expansion_requests':[],'retry':False,'r11_created':False,'Experiment1_acceptance':'NOT_DETERMINED'})
print(json.dumps({'timeline':timeline,'spans':spans,'terminal_status_seconds':load(O/'FRESH_TERMINAL_OPERATOR_STATUS.json')['projection_seconds']}))
