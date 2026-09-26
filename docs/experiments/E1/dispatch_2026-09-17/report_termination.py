"""Preserve terminal timing, findings and evidence references without changing Forge."""
import json,time,hashlib,datetime
from pathlib import Path
O=Path(__file__).resolve().parent
P=Path('/tmp/kge-forge-controller-authority/auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39/e1-programmer-dispatch-2026-09-17')
load=lambda n:json.loads((P/n).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
terminal=load('TERMINATION_RESULT.json');recovery=load('TERMINATION_INDEPENDENT_RECOVERY.json')
post=load('POST_RUN_EVIDENCE.json');programmer=load('PROGRAMMER_RESULT.json')
b=load('AUDIT_BEFORE.json');rows=[json.loads(x) for x in Path(b['path']).read_bytes()[b['bytes']:].splitlines()]
wall=time.time_ns();mono=time.monotonic_ns();offset=wall-mono
def iso(ns):return datetime.datetime.fromtimestamp(ns/1e9,datetime.timezone.utc).isoformat()
events=[{'event':r['event'],'monotonic_seconds':r['time'],'derived_utc':iso(offset+int(r['time']*1e9))} for r in rows if 'time' in r]
phases=sorted([load(p.name) for p in P.glob('PHASE_*.json')],key=lambda r:r['time_unix_ns'])
for phase in phases:phase['utc']=iso(phase['time_unix_ns'])
result_mtime=(P/'PROGRAMMER_RESULT.json').stat().st_mtime_ns
record={'final_state':'CANCELLED','classification':'INTERRUPTED_NO_EFFECTS','independent_recovery':recovery,'ownership':'RELEASED','scope':'NONE','quiescence':'No ExecutionScope created; controller exited; no pending actions or execution ownership; durable QUIESCENT recorded','provider':{'status':'Two completed response records; no outstanding request known at finalization; no cancellation sent','responses':programmer['result']['records'],'usage':'Unavailable: released client did not retain token/usage data','uncertainty':'Provider processing duration, token cost and internal activity not established; zero implementation effects does not imply zero provider activity'},'counts':{'model_requests':post['model_request_content_bound_count'],'action_requests':post['action_request_count'],'action_results':sum(r.get('event')=='action_result' for r in rows)},'known_implementation_effects':post['authoritative_product_changes'],'controller_events':events,'phase_timing':phases,'clock_calibration':{'wall_unix_ns':wall,'monotonic_ns':mono,'note':'Audit wall times derived from current clock offset, not contemporaneous provider timestamps'},'controller_result_file_mtime_utc':iso(result_mtime),'dispatch_to_result_seconds':(result_mtime-phases[0]['time_unix_ns'])/1e9,'termination_utc':iso(terminal['time_unix_ns']),'recovery_utc':iso(recovery['time_unix_ns']),'terminal_event':terminal['terminal']['event_id'],'findings':[{'id':'OBS-E1-001','title':'Operator Progress Observability','finding':'Live status did not adequately distinguish provider work, repeated controller verification, and non-progress. Earlier one-request/zero-action snapshot was superseded by two responses and one denied read.'},{'id':'OBS/EFF-E1-002','title':'Bounded Autonomous Resource Consumption','finding':'Operationally unacceptable autonomous turn duration without an effective end-to-end turn/no-progress budget. Exact provider latency and token consumption were not captured.'}],'anomalies':['Controller naturally returned INCOMPLETE before signal delivery; signal guard found PID absent and sent no signal.','One read was DENIED with read limit denied; raw request arguments were not durably retained.','INCOMPLETE return left invocation ownership reserved until explicit cancellation reconciliation.'],'implementation_changes_during_termination':False,'automatic_retry':False,'experiment_acceptance':'NOT ASSESSED; E1-WP-001 not successfully completed','evidence':[{'path':str(p),'sha256':sha(p.read_bytes())} for p in sorted(P.glob('*.json'))]}
with (O/'TERMINATION_REPORT.json').open('x') as f:json.dump(record,f,indent=2,sort_keys=True)
text=f'''# E1 invocation termination

Final invocation: **CANCELLED / INTERRUPTED_NO_EFFECTS**. Independent terminal recovery PASS; ownership released; model handoff ineligible. E1-WP-001 was not successfully completed. No replacement run or retry was made.

The controller returned INCOMPLETE before the attempted signal. The signal guard found the controller absent; no signal was sent. Two model responses were preserved. There was one read ActionRequest and one DENIED ActionResult (`read limit denied`), no ExecutionScope, and no authoritative product changes. No provider request was known outstanding at finalization; no provider cancellation was sent. Token usage and exact provider processing duration are unavailable.

Dispatch bootstrap: {phases[0]['utc']}. Result receipt filesystem timestamp: {iso(result_mtime)}. Elapsed: {record['dispatch_to_result_seconds']:.3f} seconds. Durable termination: {record['termination_utc']}. Independent recovery: {record['recovery_utc']}. The JSON report preserves raw monotonic events, derived wall times and their clock-calibration limitation.

**OBS-E1-001 — Operator Progress Observability:** status did not adequately distinguish useful provider/controller progress from prolonged verification or non-progress. The earlier one-request/zero-action observation was not the final count.

**OBS/EFF-E1-002 — Bounded Autonomous Resource Consumption:** the run exceeded acceptable duration without an effective end-to-end autonomous resource/no-progress budget. Provider usage cannot be inferred from controller effects. The apparent outstanding turn included substantial controller-verification intervals; the evidence does not establish that a provider request itself remained outstanding for two hours. Final provider message text was not retained, so its content is not reconstructed or characterized.

No Forge implementation or timeout behavior was changed during termination. Original release and experiment decisions remain historical authority. No implementation, canonical knowledge changes, tests, or acceptance-obligation completion were produced by this run. Architect assessment remains required.

Terminal event: `{record['terminal_event']}`.

See [TERMINATION_REPORT.json](TERMINATION_REPORT.json) for timing, model response identities, findings and all evidence hashes.
'''
with (O/'TERMINATION_REPORT.md').open('x') as f:f.write(text)
print(json.dumps({k:record[k] for k in ('final_state','classification','counts','termination_utc','recovery_utc','dispatch_to_result_seconds')}))
