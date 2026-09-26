import json,hashlib
from pathlib import Path
O=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
b=Path('docs/experiments/E1/run2_r12_dispatch_2026-09-18')
expected=json.loads((b/'HISTORICAL_BASELINE.json').read_text())
expected.update({str(b/k):v for k,v in json.loads((b/'EVIDENCE_HASHES.json').read_text()).items()})
p=json.loads((O/'R12_AUTHENTICATED_CAPTURE.json').read_text())
expected[p['publication']['path']]=p['publication']['sha256']
expected[p['terminal']['audit']]=p['terminal']['audit_sha256']
expected['/tmp/kge-forge-e1-invocations.jsonl']=p['terminal']['ledger_sha256']
rows=[{'path':k,'expected':v,'actual':sha(k),'pass':sha(k)==v} for k,v in expected.items()]
result={'result':'PASS' if all(r['pass'] for r in rows) else 'FAIL','checks':len(rows),'records':rows}
(O/'HISTORICAL_PRESERVATION.json').write_text(json.dumps(result,indent=2))
print(json.dumps({'result':result['result'],'checks':len(rows)}))
assert result['result']=='PASS'
