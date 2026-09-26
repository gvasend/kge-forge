"""Read-only post-run inventory; does not execute product code or alter authority."""
import json,hashlib
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parents[3]
PRIVATE=Path('/tmp/kge-forge-controller-authority/auth-e1-wp-001-r7-94f511dfcdcc43ac837191f8732ced39/e1-programmer-dispatch-2026-09-17')
sha=lambda b:hashlib.sha256(b).hexdigest()
b=json.loads((PRIVATE/'AUDIT_BEFORE.json').read_bytes());data=Path(b['path']).read_bytes();assert sha(data[:b['bytes']])==b['sha256']
rows=[json.loads(x) for x in data[b['bytes']:].splitlines()]
requests=[r for r in rows if r.get('event')=='action_request'];results=[r for r in rows if r.get('event')=='action_result']
initial=json.loads((O/'PRODUCT_BEFORE.json').read_bytes());after={}
for rel in initial['product_paths']:
 p=R/rel
 for f in ([p] if p.is_file() else sorted(p.rglob('*')) if p.is_dir() else []):
  if f.is_file() and not f.is_symlink():after[str(f.relative_to(R))]=sha(f.read_bytes())
changed=[{'path':k,'before':initial['file_sha256'].get(k),'after':after.get(k)} for k in sorted(set(after)|set(initial['file_sha256'])) if initial['file_sha256'].get(k)!=after.get(k)]
trace=[{'request':q,'results':[r for r in results if r.get('action_request_id')==q.get('action_request_id')],'effects':[r for r in rows if r.get('action_request_id')==q.get('action_request_id') and r.get('event') not in ('action_request','action_result')]} for q in requests]
record={'model_request_content_bound_count':sum(r.get('event')=='model_request_content_bound' for r in rows),'model_request_ids_and_digests':[r for r in rows if r.get('event')=='model_request_content_bound'],'action_request_count':len(requests),'authoritative_product_changes':changed,'product_after_sha256':after,'action_trace':trace,'authority_expansion_requests':[r for r in rows if r.get('event')=='authority_expansion'],'execution_and_quiescence':[r for r in rows if any(s in r.get('event','') for s in ('execution_','recovery_'))],'interruptions':[r for r in rows if 'interrupt' in r.get('event','') or 'indeterminate' in r.get('event','')],'finish_results':[r for r in results if r.get('type')=='finish'],'transmission_decisions':[r for r in rows if r.get('event')=='model_transmission'],'audit':{'path':b['path'],'sha256':sha(data),'prefix_preserved':True},'acceptance':'No Experiment 1 or KGE Forge acceptance inferred.'}
p=PRIVATE/'POST_RUN_EVIDENCE.json'
with p.open('x') as f:json.dump(record,f,sort_keys=True,indent=2)
with (O/'POST_RUN_EVIDENCE_RECEIPT.json').open('x') as f:json.dump({'path':str(p),'sha256':sha(p.read_bytes())},f)
print(json.dumps({k:record[k] for k in ['model_request_content_bound_count','action_request_count','authoritative_product_changes','authority_expansion_requests','finish_results']}))
