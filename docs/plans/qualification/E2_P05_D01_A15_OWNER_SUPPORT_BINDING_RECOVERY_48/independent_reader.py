import json,pathlib,hashlib
from adapter.planner import codec,model,typed_proofs
base=pathlib.Path('docs/plans/qualification')
g=json.loads((base/'E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/accepted-support-graph.json').read_text())
cap=json.loads(pathlib.Path(g['CAPSULE_SOURCE']['path']).read_text())
s=codec._unwire(cap['canonical_content']['bundle']).current
proofs=[]
for proof in s.typed_proofs:
 assert typed_proofs.usable(s,proof)
 for support,fingerprint in zip(proof.supports,proof.support_identities):assert typed_proofs.support_identity(s,support)==fingerprint
 proofs.append({'proof':codec._wire(proof.id),'target':codec._wire(proof.target),'supports':codec._wire(proof.supports)})
k=next(x for x in s.knowledge if x.id.value=='E2-K-REENTER')
source=next(n for n in g['NODES'] if n.get('TYPE')=='SOURCE_CONTENT' and n['NATIVE_IDENTITY']==codec._wire(k.provenance.identity))
raw=pathlib.Path(source['SOURCE_PIN']['path']).read_bytes();assert hashlib.sha256(raw).hexdigest()==k.provenance.identity.sha256
out={'EXACT_KNOWLEDGE_SOURCE':codec._wire(k.provenance.identity),'KNOWLEDGE':codec._wire(k.id),'SOURCE_PIN':source['SOURCE_PIN'],'PROOFS':sorted(proofs,key=lambda r:r['target']['value']),'PRESTATE':codec._wire(codec.snapshot_id(s)),'CONTEXT':codec._wire(s.context)}
print(json.dumps(out,sort_keys=True))
