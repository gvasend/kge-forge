import json,hashlib,sys
from pathlib import Path
O=Path(__file__).resolve().parent;Q=O.parent/'run2_control_plane_binding_2026-09-18';R=O.parent/'run2_r12_dispatch_2026-09-18'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
prior=json.loads((R/'HISTORICAL_BASELINE.json').read_bytes());r12=json.loads((R/'EVIDENCE_HASHES.json').read_bytes());checks={p:sha(p)==h for p,h in prior.items()};checks.update({str(R/p):sha(R/p)==h for p,h in r12.items()})
proof=json.loads((Q/'R12_AUTHENTICATED_CAPTURE.json').read_bytes());pin=proof['publication'];checks[pin['path']]=sha(pin['path'])==pin['sha256'];checks['/tmp/kge-forge-e1-invocations.jsonl']=sha('/tmp/kge-forge-e1-invocations.jsonl')==proof['terminal']['ledger_sha256'];assert all(checks.values())
current=json.loads((O/'INDEPENDENT_RECONSTRUCTION.json').read_bytes());sys.path.insert(0,current['runtime']['root'])
from adapter.attempt_chain import classify_terminal
from adapter.run_control import events
assert sha(proof['terminal']['audit'])==proof['terminal']['audit_sha256']
classification=classify_terminal(events(proof['terminal']['audit']),proof['terminal'],proof['authorization']['authorization_id'],True)
assert classification=='ACTIVE_CANCELLED_PRE_MODEL_NO_EFFECTS'
(O/'HISTORICAL_PRESERVATION.json').write_text(json.dumps({'result':'PASS','checked_files':len(checks),'checks':checks,'r12_safe_predecessor':classification,'real_ownership_ledger_unchanged':True},indent=2)+'\n')
print(json.dumps({'result':'PASS','files':len(checks),'r12':classification}))
