import pathlib,json,hashlib
from adapter.planner import codec as c,model as m,gates,typed_proofs as tp
Q=pathlib.Path('docs/plans/qualification');g=json.loads((Q/'E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/accepted-support-graph.json').read_text());sourced=json.loads(pathlib.Path(g['CAPSULE_SOURCE']['path']).read_text());b=c._unwire(sourced['canonical_content']['bundle']);s=b.current
k=next(k for k in s.knowledge if k.id.value=='E2-K-REENTER');assert gates.current_completion(s,k.producer)
admissions=[]
for a in s.receipt_admissions:
 gate=next(g for g in s.external_gates if any(o.artifact==a.artifact and o.gate==g.id for o in s.receipt_observations));assert gates.check_receipt(s,gate,a.artifact).state is m.ProofState.PROVED
 e=next(e for e in s.entities if e.id==a.artifact);assert e.validation is m.ValidationState.ACCEPTED
 event=next(ev for ev in b.events if type(ev.result) is m.EvidenceSourceAdmission and ev.result.admission.artifact==a.artifact)
 admissions.append({'type':'ReceiptAdmission','artifact':c._wire(a.artifact),'event':c._wire(event.identity),'position':event.sequence,'source':c._wire(e.provenance.identity)})
for proof in s.typed_proofs:
 assert tp.usable(s,proof) and proof.validation is m.ValidationState.ACCEPTED
 ev=next(ev for ev in b.events if type(ev.result) is m.TypedProofAdmission and ev.result.proof.id==proof.id)
 admissions.append({'type':'TypedProofAdmission','proof':c._wire(proof.id),'target':c._wire(proof.target),'event':c._wire(ev.identity),'position':ev.sequence,'source':c._wire(proof.provenance.identity)})
refs=[]
for f in ['FINISH_F02_1/semantic-authority-request.json','FINISH_F02_1/bounded-installation-workflow.json','FINISH_F03_1/authenticated-decisions.json']:
 p=Q/f;refs.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
print(json.dumps({'CURRENT_KNOWLEDGE_PRODUCER':c._wire(k.producer),'CURRENT_RECEIPT_PRODUCER':c._wire(s.receipt_admissions[0].producer),'ADMISSION_WITNESSES':sorted(admissions,key=lambda x:x['position']),'REFERENCE_FILES':refs,'PRESTATE':c._wire(c.snapshot_id(s))},sort_keys=True))
