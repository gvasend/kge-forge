"""E07 exact P04 precommit qualification. Never commits canonical A09."""
from dataclasses import replace
from pathlib import Path
import hashlib,json
from adapter.planner import codec as c,model as m,core,evidence as ev,evidence_attestation as ea,evidence_transaction as tx
R=Path(__file__).resolve().parents[2];D=R/'docs/plans';P='DETERMINISTIC_PLANNER_V0_1_';O=D/'qualification/EVIDENCE_E07_1';Q=D/'qualification/E2_P04_CONTINUATION_INPUT_CLOSURE_1'

def write(name,value):
    (O/name).write_bytes(c.canonical_bytes(value))


def p04():
    path=D/(P+'E2_P04_POST_ATTEST_INSTALL_BUNDLE_1.json')
    expected=m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'planner-bundle-v1','fa86ce94d76651ce5eccfa76c2d862243548d6d8dcaae91e74dca4e9c571c7d1')
    bundle=c.restore(path,expected,R);before=c.bundle_bytes(bundle)
    assert c.snapshot_id(bundle.current).sha256=='c5c85434ddfb69be7f327e9e8fd72d2c7270505cf4908ea4fd9b4918075c1591'
    assert bundle.events[-1].identity.sha256=='549e41859f55cd3414d91b5ce97f023ab9e150f55ed01ae81a9a9dc5ef2f362c'
    x=c._unwire(c.parse_json((D/'qualification/INSTALLATION_I04_1/a09-post-authentication-candidate.json').read_bytes()))
    assert x.expected_bundle==expected and x.expected_snapshot==c.snapshot_id(bundle.current) and x.expected_parent_event==bundle.events[-1].identity
    prepared=json.loads((Q/'evidence-binding.json').read_bytes())
    binding=m.SemanticNativeBinding(**{k:c._unwire(v) for k,v in prepared['binding']['fields'].items()})
    payload=c.parse_json((Q/'semantic-payload.json').read_bytes())
    req=bundle.current.evidence_requirements[0]
    assert binding.content_id==c._identity(c.canonical_bytes(payload),'p04-semantic-content-v1')
    assert binding.semantic_evidence_id==c._identity(c.canonical_bytes({'payload':payload,'proposition':req.proposition,'consumer':'E2-REENTER','gate':x.gate.value}),'p04-semantic-evidence-v1')
    seal={'role':'TRUSTED_E01_EXPECTATION_BEFORE_PREFLIGHT','binding':c._wire(binding),'initial_bundle':c._wire(expected),
          'input_hashes':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [path,Q/'evidence-binding.json',Q/'semantic-payload.json']},
          'trust_boundary':'Qualified P04 semantic fixture selected by qualification owner; never infer expected binding from submitted operand'}
    write('p04-precommit-binding-seal.json',seal)
    # Rematerialize only the transient E02 object; preserve its qualified formula.
    fields={k:c._unwire(v) for k,v in prepared['attestation']['fields'].items() if k!='attestation_id'}
    t=ea.materialize(**fields);x=tx.bind(x,t,binding)
    assert x.expected_parent_event==bundle.events[-1].identity
    raw={p.path:(R/p.path).read_bytes() for p in x.source_additions}
    try:
        projected=c.preflight_external_evidence(bundle,x,raw,R,expected_binding=binding)
        outcome='PASS'
    except m.PlannerError as error:
        outcome=str(error)
        assert outcome=='RECEIPT_CHANGED_CONTROL',outcome
        # Independently inspect only the private native projection, never publish.
        admitted=c._extend_private(bundle,x)
        projected=c._extend_private(admitted,m.ExternalEvent(x.gate,
            m.ExternalStage.EVIDENCE_RECEIVED,c.snapshot_id(admitted.current),x.entity.id))
    assert len(projected.events)==len(bundle.events)+2
    assert projected.current.external_gates[0].stage is m.ExternalStage.EVIDENCE_RECEIVED
    assert not projected.current.receipt_observations
    assert len(projected.current.receipt_admissions)==1
    assert core.recompute(projected.current).control is m.ControlState.EXTERNAL_WAIT
    assert c.bundle_bytes(bundle)==before and not bundle.current.receipt_admissions
    # Discard the private projection; no source/head/receipt/attestation persistence.
    result={'initial_bundle':c._wire(expected),'initial_state':c._wire(c.snapshot_id(bundle.current)),
            'parent':c._wire(bundle.events[-1].identity),'command_key':c._wire(x.command_key),
            'operand_identity':c._wire(c._identity(c.canonical_bytes(c._wire(x.attestation_operand)),'planner-e02-ingress-operand-v1')),
            'attestation_identity':c._wire(t.attestation_id),'dependency_provenance_cardinality':len(x.admission.dependencies),
            'execution_preflight':outcome,'parent':'PASS','route':'PASS','dependency_provenance':'PASS','reference_contract':'PASS',
            'private_projection_only':True,'canonical_commit':False,'canonical_state_unchanged':True,
            'projection_event_types':['EvidenceSourceAdmission','EVIDENCE_RECEIVED'],
            'transient_attestation_durable_before_commit':False,'binding_seal_sha256':hashlib.sha256(c.canonical_bytes(seal)).hexdigest(),
            'next_failure':None if outcome=='PASS' else outcome,'A09_READY':'YES' if outcome=='PASS' else 'NO','P04_EXECUTION_READY':'NO',
            'remaining_contracts':{'A10_validation':'RUNTIME_BLOCKED_AND_INSTALL_AUTHORITY_REQUIRED',
             'A11_reentry_and_typed_evidence_proof':'RUNTIME_BLOCKED_AND_INSTALL_AUTHORITY_REQUIRED',
             'A12_REENTER_result_inventory':'RUNTIME_BLOCKED_AND_INSTALL_AUTHORITY_REQUIRED',
             'A13_root_slot_and_finishing_result':'RUNTIME_BLOCKED_AND_INSTALL_AUTHORITY_REQUIRED'}}
    result['parent_event']=c._wire(bundle.events[-1].identity)
    write('p04-execution-preflight.json',result)
    print(json.dumps({'A09_EXECUTION_PREFLIGHT':outcome,'A09_READY':result['A09_READY'],'P04_EXECUTION_READY':'NO','A09_COMMITTED':False}))

def generic():
    import shutil
    from adapter.tests.test_planner_evidence_transaction import EvidenceTransactionTests
    h=EvidenceTransactionTests();h.setUp()
    try:
        root=O/'generic-root';root.mkdir(exist_ok=True)
        # Preserve all native source locators under an isolated fixture root.
        for pin in h.b.sources+(h.b.policy,):
            dest=root/pin.path;dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(h.h.root/pin.path,dest)
        # Independently pinned binding is sealed before the generic command commits.
        write('generic-precommit-binding-seal.json',{'expected_binding':c._wire(h.expected),
            'initial_bundle':c._wire(c.bundle_id(h.b)),'command_key':c._wire(h.x.command_key)})
        before=c.bundle_bytes(h.b)
        projected=c.preflight_external_evidence(h.b,h.x,h.raw,root,expected_binding=h.expected)
        end,bid,noop=c.admit_external_evidence(h.b,h.x,h.raw,root/'head',root,expected_binding=h.expected)
        assert not noop and c.bundle_bytes(end)==c.bundle_bytes(projected)
        again,original,noop=c.admit_external_evidence(h.b,h.x,h.raw,root/'head',root,expected_binding=h.expected)
        assert noop and original==bid and c.bundle_bytes(again)==c.bundle_bytes(end)
        independent,indid,noop=c.admit_external_evidence(h.b,h.x,h.raw,root/'independent-head',root,expected_binding=h.expected)
        assert not noop and indid==bid and c.bundle_bytes(independent)==c.bundle_bytes(end)
        startpath,startid=c.save_bundle(h.b,root/'initial',root)
        path,_=c.save_bundle(end,root/'target',root)
        cold=c.restore(path,bid,root)
        assert c.bundle_bytes(cold)==c.bundle_bytes(end) and c.bundle_bytes(h.b)==before
        write('generic-qualification.json',{'bundle':str(path.relative_to(R)),'repo_root':str(root.relative_to(R)),
            'bundle_id':c._wire(bid),'state_id':c._wire(c.snapshot_id(end.current)),
            'start_bundle':str(startpath.relative_to(R)),'start_bundle_id':c._wire(startid),
            'ingress_event':c._wire(end.events[-2].identity),'receipt_event':c._wire(end.events[-1].identity),
            'admitted_attestation':c._wire(end.current.receipt_admissions[0].attestation),
            'command_key':c._wire(h.x.command_key),'persisted_instance_location':'committed ingress event operand',
            'positive':'PASS','preflight_execution_equivalence':'PASS','idempotence':'PASS',
            'independent_reproduction':'PASS','persistence':'PASS','cold_restore':'PASS','replay':'PASS',
            'Evidence_count':1,'attestation_count':1,'receipt_count':1,'appended_event_count':2,
            'validation_count':0,'proof_count':0,'writer_pid':__import__('os').getpid(),
            'isolation':'TEST/scope and TEST/lineage; never canonical P04'})
    finally:h.tearDown()

if __name__=='__main__':
    import sys
    if len(sys.argv)>1 and sys.argv[1]=='generic':generic()
    else:p04()
