"""Non-effecting current-runtime context validation; no invocation issuance."""
import json,sys,time,tempfile,signal
from pathlib import Path
O=Path(__file__).resolve().parent;Q=O.parent/'runtime_r3_self_hosting_qualified_2026-09-19';pin=json.loads((O/'AUTHORIZED_SELECTION.json').read_bytes());adopted=json.loads((O/'ADOPTION_RESULT.json').read_bytes());proof=json.loads((Q/'R12_AUTHENTICATED_CAPTURE.json').read_bytes());sys.path.insert(0,pin['runtime_root'])
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,sha
from adapter.context_binding import CommittedContext
from adapter.context_projection import derive
from adapter.attempt_chain import classify_terminal
from adapter.run_control import events
signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(TimeoutError('120-second phase hard threshold')));signal.alarm(120)
start=time.monotonic();pub=json.loads(Path(proof['publication']['path']).read_bytes());assert sha(Path(proof['publication']['path']).read_bytes())==proof['publication']['sha256']
old=ControllerAuthorityStore(**pub['selected_store']);runtime=ControllerAuthorityStore(**pin['selected_store']);root=Path(tempfile.mkdtemp(prefix='r3-readonly-production-context-'));root.chmod(0o700)
app=dict(adopted['context'],authorization_id=proof['authorization']['authorization_id'],**runtime.applicability)
records={}
for store in (old,runtime):
 for k in store.catalog['objects']:records[k]={'bytes':store.resolve(k),'evidence':[]}
historical_runtime=json.loads(old.resolve(pub['controller_runtime']['authority_id']))
for name,h in historical_runtime['files'].items():
 data=(Path(historical_runtime['root'])/'adapter'/name).read_bytes();assert sha(data)==h
 records.setdefault('sha256:'+h,{'bytes':data,'evidence':[]})
s=ControllerAuthorityStore.materialize(root/'store',records,{}, {'authority_source':pin['grant'],'release_identities':adopted['context']},app,old.catalog['programmer_roots'],dict(old.catalog['private_state'],**runtime.catalog['private_state']))
raw=proof['authorization'];spec=json.loads(raw['operational_binding'])['governance'];spec.update(ordinary_runtime=adopted['binding'],identities=adopted['context'])
out={'qualification_only_view':True,'historical_invocation_not_rebound':True,'real_invocations_created':0,'model_requests':0,'E1_effects':0,'selected_store':{'root':str(s.root),'catalog_sha256':s.catalog_sha256,'applicability':s.applicability}}
try:
 with s.session():
  t=time.monotonic();context=CommittedContext(raw['context_binding']['path'],raw['context_binding']['capture_commit'],spec);projection=derive(json.loads(raw['context_projection']),context);out['validation_seconds']=time.monotonic()-t
  assert projection['ModelPayloadDigest']=='d675d581c80f43e691a31da73ccf17fd4bcc6b00d3a5331f26b9294e294e1538'
  out['projection']={k:projection[k] for k in ('ModelPayloadDigest','FullContextDigest','ModelProjectionBindingDigest')}
 out['r12_predecessor']=classify_terminal(events(proof['terminal']['audit']),proof['terminal'],raw['authorization_id'],True)
 assert out['r12_predecessor']=='ACTIVE_CANCELLED_PRE_MODEL_NO_EFFECTS';out['result']='PASS'
except Exception as exc:
 import traceback;traceback.print_exc()
 out.update(result='BLOCKED',error=type(exc).__name__+': '+str(exc))
finally:
 out['seconds']=time.monotonic()-start
 with (O/'PRODUCTION_CONTEXT_VALIDATION_COMPLETE_BYTES.json').open('xb') as f:f.write(encoded(out))
 s.close();old.close();runtime.close()
print(json.dumps(out,indent=2));sys.exit(0 if out['result']=='PASS' else 1)
