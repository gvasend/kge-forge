import pathlib,json,hashlib
from adapter.planner import codec as c,model as m,proof_installation as pi,typed_proofs as tp
P=pathlib.Path('docs/plans/qualification')
g=json.loads((P/'E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/accepted-support-graph.json').read_text());cap=json.loads(pathlib.Path(g['CAPSULE_SOURCE']['path']).read_text());s=c._unwire(cap['canonical_content']['bundle']).current
# Direct native collections avoid producer graph-index logic.
subjects=[]
for a in s.actions:subjects.append((c._wire(a.id),'Action','YES'))
for r in s.roots:subjects.append((c._wire(r.id),'RootCondition','YES' if any(p.target==r.id and tp.usable(s,p) for p in s.typed_proofs) else 'UNDETERMINED'))
for v in s.slots:subjects.append((c._wire(v.id),'ValueSlot','YES' if any(p.target==v.id and tp.usable(s,p) for p in s.typed_proofs) else 'UNDETERMINED'))
for k in s.knowledge:subjects.append((c._wire(k.id),'KnowledgeRecord','UNDETERMINED'))
for e in s.entities:subjects.append((c._wire(e.id),'GraphEntity','UNDETERMINED'))
for r in s.evidence_requirements:subjects.append((c._wire(r.id),'EvidenceRequirement','UNDETERMINED'))
d01=json.loads((P/'E2_P05_D01_A15_RETAINED_DATA_BINDING_45/binding-D01.json').read_text())['VALUE'];expected={json.dumps(r['ROOT_ID'],sort_keys=True) for r in d01};subjects=[r for r in subjects if json.dumps(r[0],sort_keys=True) in expected];assert len(subjects)==21
links=[]
for installed in pi.records(s,'ROOT_SLOT_CONFIGURATION_SET'):
 cfg=pi.configuration(installed.request)
 assert pi.support_current(s,installed)
 for p in s.proof_contracts+s.typed_proofs:
  for entity in cfg[-2]:
   if entity.identity==p.provenance.identity:
    contracts=[x for x in cfg[-1] if x.provenance.identity==entity.identity or x.authority==entity.id]
    matches=[x for x in contracts if x.target==p.target]
    assert len(matches)==1 and pi.contract_current(s,matches[0])
    links.append({'proof':c._wire(p.id),'content':c._wire(entity.identity),'contract':c._wire(matches[0].id),'installed':c._wire(installed.id)})
print(json.dumps({'SUBJECTS':sorted(subjects,key=lambda x:json.dumps(x[0],sort_keys=True)),'SOURCE_ROLE_LINKS':sorted(links,key=lambda x:x['proof']['sha256']),'PRESTATE':c._wire(c.snapshot_id(s))},sort_keys=True))
