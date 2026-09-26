"""Read-only prerequisite check. No append, selection, issuance, or ownership API."""
import json,base64,time,socket,struct
from pathlib import Path
from adapter.context_projection import sha,digest,canonical
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.supervisor_observation import observe
from adapter.supervisor_succession import check_id,legacy_tuple,reconstruct
from adapter.supervisor_amendment import authenticated_policy
from adapter.activation_transaction import _host
from adapter.run2_context import supervisor_prefix
O=Path(__file__).resolve().parent;E=O.parent;Q=E/'run2_live_supervisor_qualification_2026-09-17/final';F=E/'run2_nonhost_closure_2026-09-17'
def read(p):return json.loads(p.read_bytes())
def write(n,v):(O/n).write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
r={'checks':{},'succession_applied':False,'release_applied':False,'Run2_activation':False,'Run2_ownership':False,'Run2_model_requests':0,'Run2_dispatch':False}
start=time.monotonic()
eventbytes=(Q/'PROPOSED_SUPERVISOR_SUCCESSION.json').read_bytes();assert sha(eventbytes)=='2a240244e9c2f04943e677b9ecf588b175f2189e899e709864f83d63402800d9'
event=json.loads(eventbytes);assert check_id(event,'SupervisorSuccession')=='SupervisorSuccession-sha256:b86bbb15d9d9d468b2de87926ad6b1cb4063218fd71eb5426089f689c0aecce8'
body={k:v for k,v in event.items() if k not in ('id','architect_authorization')};assert digest(body)=='5363653f7301b1e4c82d2aaaa89a778ae47e532325634a74f9cfa4a108f182bc'
r['checks']['exact_event_file_and_authorization_body']='PASS'
export=Path('/tmp/kge-forge-s3-host-verification/HOST_EXPORT.json').read_bytes();assert sha(export)=='1cbf36e93771828484dcb570a66b2f061608e813d65bd4efe0456db619e15361'
c=next(json.loads(base64.b64decode(x['base64'])) for x in json.loads(export)['body']['files'] if x['path'].endswith('/CANDIDATE_S3.json'))
assert observe(c)==c;_host(legacy_tuple(c),check_scopes=True)
r['checks']['same_complete_live_instance_and_idle_scopes']='PASS';r['SupervisorInstanceId']=c['id'];r['process']=c['process']
found=[]
for p in Path('/proc').iterdir():
 if not p.name.isdigit():continue
 try:cmd=(p/'cmdline').read_bytes().split(b'\0')
 except FileNotFoundError:continue
 if b'adapter.supervisor_server' in cmd:found.append(int(p.name))
assert found==[1465900] and not Path('/proc/1098552').exists() and not Path('/proc/57950').exists()
r['checks']['exclusivity_and_predecessor_absence']='PASS'
with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as sock:
 sock.settimeout(3);sock.connect('/tmp/a21m.sock');assert struct.unpack('3i',sock.getsockopt(socket.SOL_SOCKET,socket.SO_PEERCRED,12))==(1465900,1000,1000)
 data=b'{"op":"status"}';sock.sendall(struct.pack('!I',len(data))+data)
 def recv(n):
  b=b''
  while len(b)<n:
   v=sock.recv(n-len(b));assert v,'truncated status';b+=v
  return b
 n=struct.unpack('!I',recv(4))[0];assert n<=65536
 assert json.loads(recv(n))=={'status':'READY'}
r['checks']['protocol_READY']='PASS'
for name,h in read(F/'PACKAGE_MANIFEST.json').items():assert sha((F/name).read_bytes())==h,name
inv=read(F/'FINAL_IMPLEMENTATION.json');assert all(sha(Path(k).read_bytes())==v for k,v in inv['inventory'].items())
r['checks']['frozen_candidate_and_implementation']='PASS'
ledger=Path('/tmp/kge-forge-e1-invocations.jsonl');before=sha(ledger.read_bytes());assert before=='651ced1160af0760f8b46073972a88f9d1ffc2c8ed0394e900bfa05fec586fe7'
selected=read(F/'PROBE_RESULT.json');s=ControllerAuthorityStore(**selected['selected_store'])
with s.session():
 auth=reconstruct_authorization(s,s.applicability['authorization_id']);prefix=supervisor_prefix(s)
 historical=reconstruct(s,prefix['policy'],prefix['data'],historical_applicability=prefix['applicability'])
 r['historical_authority']={'instance':historical['instance']['id'],'head':historical['head'],'operational_context':prefix['applicability']}
 r['candidate_operational_context']=s.applicability
 r['checks']['historical_and_candidate_ancestry']='PASS'
 try:authenticated_policy(auth,s)
 except ValueError as exc:r['production_succession_gate']=str(exc)
 else:raise AssertionError('Unissued release unexpectedly accepted for succession')
 assert r['production_succession_gate']=='prospective Run-2 decisions cannot authorize effects'
 r['decision_mode']=json.loads(s.resolve(auth.authorization_id+':run2-context'))['mode']
s.close()
assert sha(ledger.read_bytes())==before and observe(c)==c
r['elapsed_seconds']=time.monotonic()-start
assert r['elapsed_seconds']<30
r['result']='BLOCKED_RELEASE_SUCCESSION_ORDERING'
r['blocking_requirement']='Production authorize_append -> authenticated_policy -> supervisor_policy requires mode ISSUED and an authenticated AUTHORIZE_E1_RUN2_RELEASE decision; current authorization explicitly withholds that decision.'
r['no_authority_reinterpretation']=True
write('REVALIDATION.json',r);print(json.dumps(r,sort_keys=True))
