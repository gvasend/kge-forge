import pathlib,json,hashlib
from adapter.planner import codec as c,model as m,proof_installation as pi,installation as inst,action_installation as ai,core
Q=pathlib.Path('docs/plans/qualification');g=json.loads((Q/'E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/accepted-support-graph.json').read_text());b=c._unwire(json.loads(pathlib.Path(g['CAPSULE_SOURCE']['path']).read_text())['canonical_content']['bundle']);s=b.current
assert c._wire(c.snapshot_id(s))==g['PRESTATE_ID']
refs=set()
k=next(x for x in s.knowledge if x.id.value=='E2-K-REENTER');refs.add(k.provenance.identity)
for p in s.typed_proofs:
 refs.update((p.provenance.identity,p.authority_identity))
 refs.add(next(e.provenance.identity for e in s.entities if e.id==p.authority))
for r in s.installed_definitions:
 d=c.parse_json(r.request.definition.descriptor_json.encode())
 relevant=d['definition_type'] in pi.TYPES or (d['definition_type']=='ACTION_DEFINITION' and d['subject']['action']=='E2-FINISH')
 if relevant:
  refs.update(x for x in inst.support_ids(r.request) if x.kind is m.IdentityKind.CONTENT_IDENTITY)
a=next(a for a in s.actions if a.id.value=='E2-FINISH');refs.add(a.source.identity);refs.update(x.provenance.identity for x in a.accepted_inventory)
comp=core.recompute(s);assert comp.control is m.ControlState.RUNNABLE and m.ActionId('E2-FINISH') in comp.actionable
result={'CONTENT_DEPENDENCIES':sorted((c._wire(x) for x in refs),key=lambda x:json.dumps(x,sort_keys=True)),'PINNED':sum(x in {p.identity for p in b.sources} for x in refs),'UNPINNED':sum(x not in {p.identity for p in b.sources} for x in refs),'START_CONTROL':comp.control.value,'SNAPSHOT':c._wire(c.snapshot_id(s)),'DESCENDANT':c._wire(a.id),'PRODUCER_REQUIREMENTS':c._wire(next(a.requirements for a in s.actions if a.id==k.producer))}
print(json.dumps(result,sort_keys=True))
