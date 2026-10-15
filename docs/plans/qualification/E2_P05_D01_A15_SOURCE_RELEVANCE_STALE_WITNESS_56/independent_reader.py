import pathlib,json,hashlib
from adapter.planner import codec as c,model as m,typed_proofs as tp,proof_installation as pi,installation as inst
Q=pathlib.Path('docs/plans/qualification');g=json.loads((Q/'E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/accepted-support-graph.json').read_text());b=c._unwire(json.loads(pathlib.Path(g['CAPSULE_SOURCE']['path']).read_text())['canonical_content']['bundle']);s=b.current
rows=[]
for p in s.typed_proofs:
 assert tp.usable(s,p) and p.validation is m.ValidationState.ACCEPTED
 ev=next(e for e in b.events if type(e.result) is m.TypedProofAdmission and e.result.proof.id==p.id)
 relevant=[r for r in pi.records(s,'ROOT_SLOT_CONFIGURATION_SET') if any(x.id==p.contract for x in pi.configuration(r.request)[-1])];assert len(relevant)==1 and p.provenance.identity in inst.support_ids(relevant[0].request)
 rows.append({'SOURCE':c._wire(p.provenance.identity),'PROOF':c._wire(p.id),'SUPPORTS':c._wire(p.supports),'EVENT':c._wire(ev.identity),'POSITION':ev.sequence,'TARGET':c._wire(p.target),'COMMON_CURRENT_CONFIGURATION':c._wire(relevant[0].id)})
a=s.receipt_admissions[0];entity=next(e for e in s.entities if e.id==a.artifact);event=next(e for e in b.events if type(e.result) is m.EvidenceSourceAdmission and e.result.admission.artifact==a.artifact)
assert any(p.obligation in {cl.requirement for cl in a.claims} for p in s.predicates if p.id in next(x.requirements for x in s.actions if x.id.value=='E2-REENTER'))
print(json.dumps({'TYPED_PROOF_ROWS':sorted(rows,key=lambda x:x['TARGET']['value']),'RECEIPT':{'SOURCE':c._wire(entity.provenance.identity),'ARTIFACT':c._wire(entity.id),'EVENT':c._wire(event.identity),'POSITION':event.sequence},'SNAPSHOT':c._wire(c.snapshot_id(s))},sort_keys=True))
