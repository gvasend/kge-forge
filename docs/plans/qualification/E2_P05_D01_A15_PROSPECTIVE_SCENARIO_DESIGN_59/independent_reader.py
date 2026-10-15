import pathlib,json,hashlib
from adapter.planner import codec as c,model as m,typed_proofs as tp,proof_installation as pi,installation as inst
Q=pathlib.Path('docs/plans/qualification');g=json.loads((Q/'E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/accepted-support-graph.json').read_text());b=c._unwire(json.loads(pathlib.Path(g['CAPSULE_SOURCE']['path']).read_text())['canonical_content']['bundle']);s=b.current
# Independent recursive target/support inventory; no supplied design target list used as oracle.
pending=[s.goals[0].target];seen=set();rows=[]
while pending:
 target=pending.pop()
 if target in seen:continue
 seen.add(target)
 applicable=[p for p in s.typed_proofs if p.target==target and tp.usable(s,p)]
 for p in applicable:
  rows.append({'target':c._wire(p.target),'proof':c._wire(p.id),'source':c._wire(p.provenance.identity),'supports':c._wire(p.supports)})
  pending.extend(x for x in p.supports if type(x) in (m.ConditionId,m.SlotId))
assert len(rows)==2
sources={json.dumps(x['source'],sort_keys=True) for x in rows};assert len(sources)==2
print(json.dumps({'OWNED_PROOF_ROWS':sorted(rows,key=lambda r:r['target']['value']),'START_SNAPSHOT':c._wire(c.snapshot_id(s)),'EVENT_HEAD':c._wire(b.events[-1].identity),'EVENT_COUNT':len(b.events),'NO_NATIVE_INVALIDATION':True},sort_keys=True))
