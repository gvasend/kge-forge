"""Read-only comparison against immutable prior experiment fingerprints."""
import json,hashlib
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parent/'run2_r12_dispatch_2026-09-18'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
prior=json.loads((R/'HISTORICAL_BASELINE.json').read_text());r12=json.loads((R/'EVIDENCE_HASHES.json').read_text());checks={p:sha(p)==h for p,h in prior.items()};checks.update({str(R/p):sha(R/p)==h for p,h in r12.items()})
pin=json.loads((O/'R12_AUTHENTICATED_CAPTURE.json').read_text())['publication'];checks[pin['path']]=sha(pin['path'])==pin['sha256']
checks['/tmp/kge-forge-e1-invocations.jsonl']=sha('/tmp/kge-forge-e1-invocations.jsonl')=='dfc08c6bfa460e30eb5a5c615096c36644d97b61f4798c76829af8ba0f2d0056'
value={'result':'PASS' if all(checks.values()) else 'FAIL','checked_files':len(checks),'checks':checks,'real_ownership_ledger_unchanged':checks['/tmp/kge-forge-e1-invocations.jsonl'],'r13_created':False}
(O/'HISTORICAL_PRESERVATION.json').write_text(json.dumps(value,indent=2));assert all(checks.values());print(json.dumps({k:v for k,v in value.items() if k!='checks'}))
