import pathlib,json,hashlib
from adapter.planner import codec as c,model as m,proof_installation as pi,typed_proofs as tp
P=pathlib.Path('docs/plans/qualification');g=json.loads((P/'E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/accepted-support-graph.json').read_text());cap=json.loads(pathlib.Path(g['CAPSULE_SOURCE']['path']).read_text());s=c._unwire(cap['canonical_content']['bundle']).current
result=[]
for native in s.proof_contracts+s.typed_proofs:
 cfgs=[r for r in pi.records(s,'ROOT_SLOT_CONFIGURATION_SET') if any(x.target==native.target for x in pi.configuration(r.request)[-1])]
 assert len(cfgs)==1 and pi.support_current(s,cfgs[0]);cfg=pi.configuration(cfgs[0].request)
 entity=next(x for x in cfg[-2] if x.identity==native.provenance.identity)
 contract=next(x for x in cfg[-1] if x.target==native.target);assert pi.contract_current(s,contract)
 identity=c._wire(entity.identity);sources=[n['SOURCE_PIN'] for n in g['NODES'] if n.get('TYPE')=='SOURCE_CONTENT' and n['NATIVE_IDENTITY']==identity];assert len(sources)==1
 assert hashlib.sha256(pathlib.Path(sources[0]['path']).read_bytes()).hexdigest()==identity['sha256']
 assert c._wire(entity.identity) not in c._wire(native.supports)
 assert c._wire(entity.identity) not in c._wire(native.support_identities)
 cid='qualification-A15-proof-source-candidate-v1:'+hashlib.sha256(json.dumps([identity,c._wire(native.id)],sort_keys=True,separators=(',',':')).encode()).hexdigest()
 result.append({'candidate_id':cid,'content':identity,'pin':sources[0],'proof':c._wire(native.id),'owner':c._wire(native.target),'supports':c._wire(native.supports),'fingerprints':c._wire(native.support_identities),'configuration_current':True,'classification':'CONFIGURATION_ONLY','scope':native.scope,'lineage':native.lineage,'generation':native.generation,'provenance':c._wire(native.provenance)})
print(json.dumps(sorted(result,key=lambda x:x['candidate_id']),sort_keys=True))
