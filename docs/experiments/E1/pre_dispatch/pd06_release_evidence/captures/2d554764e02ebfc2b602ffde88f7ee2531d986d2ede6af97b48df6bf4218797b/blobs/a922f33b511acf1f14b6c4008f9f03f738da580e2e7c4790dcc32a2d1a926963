import sys,json
from pathlib import Path
sys.path.insert(0,'/home/gvasend/app/kge-forge')
from adapter.forward_bridge import ForwardBridge
from adapter.invocation_ownership import InvocationOwnership
out=Path('/tmp/pd06-execution-regression-20260916')
events=[json.loads(x) for x in (out/'controller.jsonl').read_text().splitlines()]
snapshot=next(e for e in events if e.get('event')=='execution_snapshot_created')
sid='scope-36f722e093db4e8c8bbdbfbab685bcc4'
bridge=ForwardBridge('session-g5-live','auth-g5-live',sid,'first',snapshot['workspace_root'])
receipt={'purpose':'Reconcile pre-admission sandbox failure by creating and closing empty bound scope; no production_spawn', 'scope':sid}
for op in ('create','close','quiescent'):
 receipt[op]=bridge.exchange(op)
assert receipt['quiescent']['quiescent']
owner=InvocationOwnership(out/'ownership.jsonl')
owner.release(sid,'first','session-g5-live','auth-g5-live')
assert owner.active() is None
receipt['active_reservation']=None
(out/'RECONCILIATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
