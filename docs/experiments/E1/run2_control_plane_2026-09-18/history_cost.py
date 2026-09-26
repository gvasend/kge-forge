"""Cost of unchanged original audit decoding and semantic evaluation, read-only."""
import hashlib,json,sys,time
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parent/'run2_r12_dispatch_2026-09-18'
pin=json.loads((R/'CURRENT_PIN.json').read_bytes());raw=Path(pin['path']).read_bytes()
assert hashlib.sha256(raw).hexdigest()==pin['sha256'];p=json.loads(raw);sys.path.insert(0,p['runtime_root'])
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.attempt_chain import predecessor_nodes,classify_terminal
from adapter.run_control import events
s=ControllerAuthorityStore(**p['selected_store'])
try:
 with s.session():
  a=reconstruct_authorization(s,p['r12_authorization_id'])
  nodes,failed=predecessor_nodes(a.context_binding.governance.run7['predecessor'])
  refs=[failed]+[dict(n['terminal'],authorization_id=n['authorization']['authorization_id']) for n in nodes]
  own=json.loads((O/'R12_PREDECESSOR.json').read_bytes())
  refs.append({'authorization_id':a.authorization_id,'audit':p['audit'],'audit_sha256':own['audit_sha256']})
finally:s.close()
rows=[]
for ref in refs:
 path=Path(ref['audit']);assert hashlib.sha256(path.read_bytes()).hexdigest()==ref['audit_sha256']
 samples=[]
 for _ in range(4):
  t=time.monotonic();decoded=events(path);samples.append(time.monotonic()-t)
 rows.append({'authorization_id':ref['authorization_id'],'audit_sha256':ref['audit_sha256'],'bytes':path.stat().st_size,'records':len(decoded),'decode_seconds':samples})
semantic=[]
for _ in range(4):
 t=time.monotonic();result=classify_terminal(decoded,own,a.authorization_id,True);semantic.append(time.monotonic()-t)
assert result=='ACTIVE_CANCELLED_PRE_MODEL_NO_EFFECTS'
out={'scope':'ORIGINAL_AUDIT_HASH_ORDER_DECODING_NOT_FULL_CHAIN_AUTHORIZATION','attempts':rows,
 'cumulative_warm_decode_seconds_by_history_length':[sum(r['decode_seconds'][-1] for r in rows[:n]) for n in range(1,len(rows)+1)],
 'r12_semantic_evaluation_seconds':semantic,'history_truncated':False,'current_mutable_checks_cached':False}
(O/'HISTORY_COST.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
