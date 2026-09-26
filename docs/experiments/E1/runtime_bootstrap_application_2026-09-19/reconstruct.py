"""Independent read-only production runtime reconstruction and entry checks."""
import json,sys,time,subprocess
from pathlib import Path
O=Path(__file__).resolve().parent;p=json.loads((O/'AUTHORIZED_SELECTION.json').read_bytes());sys.path.insert(0,p['consumer_root'])
from adapter import runtime_bootstrap as b,runtime_adoption as r
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,sha
s=ControllerAuthorityStore(**p['selected_store']);begin=time.monotonic()
try:
 state=b.reconstruct(s);assert state['runtime_head_established'] and state['state']=='SUCCESSOR_CURRENT'
 runtime_state=r.reconstruct(s);policy=r.policy(s);runtime=r.descriptor(s,runtime_state['current_descriptor'],live=True)
 binding={'runtime_head_authority':policy['id'],'runtime':state['runtime'],'head_event':state['head_event']}
 measured=[]
 for _ in range(3):
  t=time.monotonic();r.validate_invocation_runtime(s,binding,runtime['root']);measured.append(time.monotonic()-t)
 predecessor=dict(policy['release_context']);release=predecessor.pop('release_authority');new_release,new_ids=r.production_identities(s,release,predecessor,binding)
 _,record,selector=b.verify_records(s)
 t=time.monotonic();b.fresh_supervisor(s,record);host_seconds=time.monotonic()-t
 # Read-only replay gate observation; do not invoke establish again.
 with b.guard(s,policy) as fd:
  rows=b.history(fd,record,selector)
  assert [row['event'] for row in rows]==['BOOTSTRAP_INTENT','BOOTSTRAP_COMMITTED','BOOTSTRAP_RECORDED']
 journal=s.state_path(policy['journal']);bootstrap=s.state_path(policy['bootstrap_journal'])
 result={'result':'PASS','state':'R1_UNIQUE_CURRENT_RUNTIME','independent_process':True,'bootstrap_consumed':True,'replay_gate':'CLOSED_LINEAGE','runtime':runtime,'runtime_binding':binding,'runtime_ancestry':state['runtime_ancestry'],'release_authority':new_release,'runtime_authority_context':new_ids,'legacy_release_context':policy['release_context'],'S3':'PASS','S3_seconds':host_seconds,'runtime_head_verification_seconds':measured,'journal_sha256':sha(journal.read_bytes()),'bootstrap_journal_sha256':sha(bootstrap.read_bytes()),'seconds':time.monotonic()-begin,'invocation_created':False,'real_model_requests':0,'effects':0}
 (O/'INDEPENDENT_RECONSTRUCTION.json').write_bytes(encoded(result));print(encoded({k:v for k,v in result.items() if k!='runtime'}).decode())
finally:s.close()
