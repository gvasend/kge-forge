"""Projection of already-restored native terms; no producer invocation."""
import os
from common import *
from adapter.planner import validation_transaction as vt

def project(b):
    s=b.current; ingress=b.events[-2]; end=b.events[-1]; req=ingress.result
    equal('terminal admission type',type(req).__name__,'EvidenceSourceAdmission')
    equal('terminal receipt type',type(end.result).__name__,'ExternalEvent')
    equal('terminal received stage',end.result.stage.value,'EVIDENCE_RECEIVED')
    evidence=next(e for e in s.entities if e.id==req.entity.id)
    receipt=next(r for r in s.receipt_admissions if r.artifact==evidence.id)
    gate=next(g for g in s.external_gates if g.id==req.gate)
    comp=core.recompute(s)
    terms=dict(bundle=selection()['restore_manifest']['bundle_id'],snapshot=c._wire(c.snapshot_id(s)),
        evidence=c._wire(evidence),receipt=c._wire(receipt),
        receipt_identity=c._wire(vt.receipt(b,evidence.id)[2]),
        attestation_operand=c._wire(req.attestation_operand),ingress_operand=c._wire(req),
        ingress_event=c._wire(ingress),receipt_event=c._wire(end),
        ancestry=c._wire(b.events),ledger_root=c._wire(b.events[0].identity),append_head=c._wire(end.identity),
        sources=c._wire(b.sources),policy=c._wire(b.policy),policy_version=b.policy_version,
        context=c._wire(s.context),bundle_scope=b.scope,
        post_restore=dict(bundle_trust=True,stage=gate.stage.value,pending=gate.pending.value,
            receipt_present=True,receipt_current=receipt.attestation==req.attestation_operand.attestation.attestation_id,
            evidence_native_identity=evidence.id.value,validation=evidence.validation.value,
            evidence_validated=evidence.validated,control=comp.control.value,
            resume=core.resume_eligibility(b,ROOT).allowed,
            observations=c._wire(s.receipt_observations),validation_results=c._wire(s.validation_results),
            validation_support=c._wire(s.validation_support_records),typed_proofs=c._wire(s.typed_proofs)))
    return envelope(terms)

def validate(projection, invocation):
    check_refs(metadata())
    expected=read(OUT/'expected-projection.json'); expman=read(OUT/'expected-manifest.json')
    equal('projection identity integrity',projection['identity'],qid('projection',projection['body']))
    equal('manifest identity integrity',invocation['identity'],qid('manifest',invocation['body']))
    def compare(a,e,path=''):
        equal('field set '+path,set(a),set(e))
        for k in sorted(e):
            if isinstance(e[k],dict): compare(a[k],e[k],path+'/'+k)
            else: equal('term '+path+'/'+k,a[k],e[k])
    compare(projection,expected);compare(invocation,expman)
    return True

def reader(form):
    b=restore(form)
    m.validate_model(b.current)
    c.bundle_bytes(b,snapshot_resolver=c.snapshot_resolver(Path(selection()['restore_manifest']['path']).parent))
    p=project(b); inv=manifest(p);validate(p,inv)
    return dict(pid=os.getpid(),presentation=form,projection=p['identity'],manifest=inv['identity'],
        source='PASS',cold_restore='PASS',native_validation='PASS',post_restore_oracle='PASS',term_equality='PASS')

if __name__=='__main__':
    if sys.argv[1]=='reader': print(json.dumps(reader(sys.argv[2]),sort_keys=True))
    elif sys.argv[1]=='materialize':
        b=restore();p=project(b);inv=manifest(p);validate(p,inv)
        save('END-projection.json',p);save('invocation-input-manifest.json',inv)
        print('MATERIALIZATION_PASS')
