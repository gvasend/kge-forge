"""Prepare non-admitted P04 inputs; never apply or commit a lifecycle event."""
from dataclasses import replace, fields
import hashlib
import json
from pathlib import Path
from adapter.planner import codec as c, model as m, core, evidence as ev
from adapter.planner import attestor, evidence_materializer as em
from adapter.planner import evidence_attestation as ea, action_materializer as am
from adapter.planner import typed_proofs as tp

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / 'docs/plans'
P = 'DETERMINISTIC_PLANNER_V0_1_'
OUT = D / 'qualification/E2_P04_CONTINUATION_INPUT_CLOSURE_1'
EXPECTED = m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY, 'planner-bundle-v1',
    'd1944fe18626778bebfc6c7693c7bdb5303e079668683e5fb99676ecbe46b859')


def read(suffix):
    return json.loads((D / (P+suffix)).read_text())


def definition_wire(obj):
    # These generic helper records are not registered codec event types.
    return {'qualification_definition_type':type(obj).__name__,
            'fields':{f.name:c._wire(getattr(obj,f.name)) for f in fields(obj)}}


def emit(name, obj):
    raw = c.canonical_bytes(obj)
    path = OUT/name
    if path.exists():
        assert path.read_bytes() == raw, 'draft input changed between preparations'
    else:
        path.write_bytes(raw)
    return m.Provenance(str(path.relative_to(ROOT)), c._identity(raw,'raw-file-sha256'),
                        '/', raw.decode(), 'P04-PROSPECTIVE-DEFINITION-1', SCOPE)


def prepare():
    global SCOPE
    b = c.restore(D/(P+'P03_PROSPECTIVE_CHECKPOINT_BUNDLE_1.json'), EXPECTED, ROOT)
    s = b.current
    ctx = s.context
    SCOPE = ctx.scope
    prebytes = c.bundle_bytes(b)
    assert core.recompute(s).control is m.ControlState.EXTERNAL_WAIT
    g = s.external_gates[0]
    r = next(x for x in s.evidence_requirements if x.id in g.requirements)
    OUT.mkdir(parents=True,exist_ok=True)
    auth = emit('authorization-capture.json', {
        'subject':'E2-P04 continuation input closure',
        'issuer':'Authenticated human user of this session; user-role instruction',
        'sequence':1,'date':'2026-10-04','scope':ctx.scope,'lineage':ctx.lineage,
        'checkpoint_bundle':c._wire(EXPECTED),'checkpoint_state':c._wire(c.snapshot_id(s)),
        'parent_event':c._wire(b.events[-1].identity),
        'permission':'Prepare scoped candidate ATTEST/fixture definitions and independent preflight; no admission, lifecycle execution, checkpoint alteration or runtime repair',
        'authentication':'Trusted conversation transport; not a cryptographic human signature',
        'native_admission_status':'DEFINITION_ONLY_NOT_INSTALLED'})
    issuer = m.ArtifactIdentity(m.IdentityKind.AUTHORITY_IDENTITY,
                                'p04-qualification-input-issuer-v1',auth.identity.sha256)
    ac = attestor.AttestContract(r.producers[0],r.id,g.id,ctx.scope,ctx.lineage,100,auth)
    # T04 returns an offline definition-bearing snapshot.  It is NOT adopted
    # as b.current, persisted as a start, or used for admission preflight.
    chain = attestor.materialize(s,issuer,ac,auth.identity)
    emit('attest-definitions.json', {'status':'CANDIDATE_NOT_INSTALLED',
        'contract':definition_wire(ac),'authority':c._wire(chain.authority),
        'authority_predicate':c._wire(chain.authority_predicate),
        'attestor':c._wire(chain.attestor),'source_predicate':c._wire(chain.attestor_predicate)})
    semantic = read('E2_P03_SYNTHETIC_EVIDENCE_CONTRACT_1.json')
    payload = dict(semantic['payload'],scope=ctx.scope,lineage=ctx.lineage,generation=ctx.generation)
    payload_prov = emit('semantic-payload.json',payload)
    content = c._identity(c.canonical_bytes(payload),'p04-semantic-content-v1')
    semantic_id = c._identity(c.canonical_bytes({'payload':payload,
        'proposition':r.proposition,'consumer':'E2-REENTER','gate':g.id.value}),
        'p04-semantic-evidence-v1')
    # Reuse only source/target/proposition semantics. No historical request is loaded.
    seed = m.ReceiptAdmission(m.EntityId('UNMATERIALIZED-CANDIDATE'),r.producers[0],r.target,
        (m.EvidenceClaim(r.id,m.ProofState.PROVED),),chain.attestor_predicate.id,auth)
    materialized = em.materialize(semantic_evidence_id=semantic_id,content_id=content,
        gate=g.id,context=ctx,proposition=r.proposition,source_pin=r.producers[0],
        attestor=chain.attestor.identity,attestor_predicate=chain.attestor_predicate.id,admission=seed)
    raw = materialized.canonical_provenance
    rawpath = OUT/'native-payload.json'
    if rawpath.exists(): assert rawpath.read_bytes()==raw
    else: rawpath.write_bytes(raw)
    entity = replace(materialized.entity,provenance=replace(materialized.entity.provenance,
        path=str(rawpath.relative_to(ROOT))),validated=False,validation=m.ValidationState.NOT_EVALUATED)
    ingress = m.EvidenceIngressContract('PLANNER-EVIDENCE-INGRESS-1',g.id,g.receipt_action,
        g.requirements,chain.attestor_predicate.id,'TEST-rule-owner governing-rule source',
        ctx.scope,ctx.lineage,ctx.generation,100,auth)
    wire = c._wire(ingress);wire.pop('provenance')
    ingress_prov = emit('ingress-contract.json',{'schema':'PLANNER-EVIDENCE-INGRESS-1','contract':wire})
    ingress = replace(ingress,provenance=ingress_prov)
    route = m.ExternalResolutionContract('TEST-REQUEST',g.id,r.id,r.proposition,r.target,
        r.producers,ingress.source_class,r.provenance.identity,g.provenance.identity,
        g.receipt_action,g.reentry,g.held_actions,ctx.scope,ctx.lineage,ctx.generation,auth)
    wire = c._wire(route);wire.pop('$type');wire.pop('provenance')
    route_prov = emit('resolution-contract.json',{'schema':'EXTERNAL-RESOLUTION-CONTRACT-1','contract':wire})
    route = replace(route,provenance=route_prov)
    admission = replace(seed,artifact=entity.id,provenance=entity.provenance,
        dependencies=tuple(sorted({ingress_prov,g.provenance,r.provenance,route_prov,auth},
                                 key=lambda p:(p.path,p.identity.sha256))))
    attestation = ea.materialize(attestor_authority=chain.authority.identity,
        attestor=chain.attestor.identity,source_predicate=chain.attestor_predicate.id,
        source_pin=admission.producer,native_entity=entity.id,semantic_evidence=semantic_id,
        content=content,proposition=r.proposition,gate=g.id,scope=ctx.scope,
        lineage=ctx.lineage,provenance=entity.provenance.identity)
    ea.validate(attestation,entity=entity,contract=ingress,gate=g.id,context=ctx,
        source_pin=admission.producer,semantic_evidence=semantic_id,content=content,
        proposition=r.proposition,attestor=chain.attestor.identity)
    request = m.EvidenceSourceAdmission('PLANNER-EVIDENCE-ADMISSION-1',EXPECTED,
        c.snapshot_id(s),b.events[-1].identity,EXPECTED,g.id,g.receipt_action,g.requirements,
        ingress_prov.identity,(m.ArtifactPin(entity.provenance.path,entity.identity),),entity,
        admission,ev.field_bindings(entity,admission,ingress))
    request = replace(request,command_key=ev.command_key(request))
    assert ev.ingress(request)==ingress
    m.validate_types(request,m.EvidenceSourceAdmission)
    emit('a09-candidate.json',c._wire(request))
    emit('evidence-binding.json',{'semantic':c._wire(semantic_id),'content':c._wire(content),
        'binding':definition_wire(materialized.binding),'entity':c._wire(entity),
        'attestation':definition_wire(attestation),'status':'FRESH_NON_ADMITTED'})
    declarations = read('E2_PC01_SOURCES.json')['declarations']
    actions = {}
    for aid in ('E2-REENTER','E2-FINISH'):
        action = next(a for a in s.actions if a.id.value==aid)
        declaration = next(d for d in declarations if d['id']==aid)
        # The result semantics are unchanged; native provenance/context is the
        # existing prospective Action source, not the historical instance.
        actions[aid] = am.materialize_action(action,declaration)
        assert actions[aid].accepted_inventory and actions[aid].pass_model_complete
    emit('action-definitions.json',{'status':'STANDALONE_DEFINITIONS_NOT_INSTALLED',
        'definitions':{k:c._wire(v) for k,v in actions.items()},
        'result_source':P+'E2_PC01_SOURCES.json','requires_finish_root_gate':True,
        'requires_nonterminal_prerequisite_contract':True})
    fixture_spec = read('E2_PC02_ROOT_SLOT_FIXTURE_AUTHORITY_1.json')
    fixture_prov = emit('root-slot-definition-contract.json',{
        'status':'NON_ADMITTED_PROSPECTIVE_DEFINITIONS','scope':ctx.scope,
        'lineage':ctx.lineage,'generation':ctx.generation,'authority_capture':c._wire(auth.identity),
        'source_semantics':{k:dict(fixture_spec[k],lineage=ctx.lineage) for k in
            ('e2_slot_contract','e2_root_contract','slot_proof_contract','root_proof_contract')},
        'historical_authority_reused':False,'installation_path':'UNRESOLVED'})
    fixture_authority=m.GraphEntity(m.EntityId('P04-FIXTURE-AUTHORITY:'+auth.identity.sha256),
        m.EntityKind.AUTHORITY,issuer,auth,ctx.scope,ctx.lineage,ctx.generation,100,
        permissions=(m.AuthorityClass.DECIDE,))
    knowledge=actions['E2-REENTER'].accepted_inventory[0]
    khash=c._identity(c.canonical_bytes(c._wire(knowledge)),'planner-proof-support-v1')
    slotc=m.TypedProofContract(EXPECTED,m.TypedProofKind.SLOT_PROOF,'E2-SLOT-PROPOSITION',
        m.SlotId('E2-SLOT'),(knowledge.id,),(khash,),ctx.scope,ctx.lineage,ctx.generation,100,
        fixture_authority.id,fixture_authority.identity,fixture_prov)
    slotc=replace(slotc,id=tp.identity(slotc))
    # Predicted future proof identity is algebra only, not a TypedProof instance.
    future=c._wire(slotc);future.pop('id');future.pop('validation',None);future['$type']='TypedProof'
    future['contract']=c._wire(slotc.id)
    future_id=c._identity(c.canonical_bytes(future),'planner-TypedProof-v1')
    root_support=c._identity(c.canonical_bytes(c._wire((future_id,))),'planner-proof-support-v1')
    rootc=m.TypedProofContract(EXPECTED,m.TypedProofKind.ROOT_PROOF,'E2-ROOT-PROPOSITION',
        m.ConditionId('E2-ROOT'),(m.SlotId('E2-SLOT'),),(root_support,),ctx.scope,ctx.lineage,
        ctx.generation,100,fixture_authority.id,fixture_authority.identity,fixture_prov)
    rootc=replace(rootc,id=tp.identity(rootc))
    m.validate_types(slotc,m.TypedProofContract);m.validate_types(rootc,m.TypedProofContract)
    emit('typed-proof-contracts.json',{'status':'CONTRACT_CANDIDATES_NOT_INSTALLED',
        'slot':c._wire(slotc),'root':c._wire(rootc),
        'fixture_authority':c._wire(fixture_authority),
        'support_fingerprint_rule':'Exact declared knowledge and algebraically predicted future slot proof; actual currentness still independently checked at admission',
        'proof_instances_created':0})
    checks={
        'trusted_initial_bundle':True,'state_external_wait':True,
        'parent_bundle':request.expected_bundle==c.bundle_id(b),
        'parent_snapshot':request.expected_snapshot==c.snapshot_id(s),
        'parent_event':request.expected_parent_event==b.events[-1].identity,
        'command_key':request.command_key==ev.command_key(request),
        'candidate_schema_types':True,'ingress_canonical_contract':ev.ingress(request)==ingress,
        'evidence_bound_attestation_offline_binding':True,
        'source_payload_identity':entity.identity==c._identity(raw,'raw-file-sha256'),
        'scope_lineage_generation':(entity.scope,entity.lineage,entity.generation)==(ctx.scope,ctx.lineage,ctx.generation),
        'receipt_route_installed':any(x.requirement==r.id for x in g.resolution_contracts),
        'ingress_pin_in_parent_source_index':any(p.identity==ingress_prov.identity for p in b.sources),
        'native_ATTEST_predicate_installed':any(p.id==admission.authentication for p in s.predicates),
        'native_ATTEST_authority_installed':any(e.id==chain.attestor.id for e in s.entities),
        'REENTER_result_definition_installed':next(x for x in s.actions if x.id.value=='E2-REENTER')==actions['E2-REENTER'],
        'root_slot_contracts_installed':slotc in s.proof_contracts and rootc in s.proof_contracts,
        'native_persisted_definition_installation_available':False,
    }
    # Pure negative checks only; no evidence.apply/core.apply_event invoked.
    wrong_parent=replace(request,expected_parent_event=request.expected_snapshot)
    assert wrong_parent.expected_parent_event!=b.events[-1].identity
    negative={'wrong_parent':'REJECTED_BY_EXACT_PARENT_ORACLE'}
    for label,changed in [('wrong_scope',replace(ctx,scope='WRONG')),
                          ('wrong_lineage',replace(ctx,lineage='WRONG'))]:
        try:ea.validate(attestation,entity=entity,contract=ingress,gate=g.id,context=changed,
            source_pin=admission.producer,semantic_evidence=semantic_id,content=content,
            proposition=r.proposition,attestor=chain.attestor.identity)
        except m.PlannerError as e:negative[label]=str(e)
        else:raise AssertionError(label+' accepted')
    # Pure native rejection preflight against the exact canonical pre-state.
    # No command is appended/committed and no admitted Snapshot may be returned.
    try:
        ev.apply(s,request,attestation)
    except m.PlannerError as e:
        native_rejection=str(e)
    else:
        raise AssertionError('unexpected admission: definitions absent in exact checkpoint')
    assert c.bundle_bytes(b)==prebytes
    assert c.restore(D/(P+'P03_PROSPECTIVE_CHECKPOINT_BUNDLE_1.json'),EXPECTED,ROOT)==b
    result={'initial_bundle':c._wire(EXPECTED),'initial_state':c._wire(c.snapshot_id(s)),
        'parent_event':c._wire(b.events[-1].identity),'ledger_id':None,
        'ledger_note':'Native PersistenceBundle exposes ordered ExecutionEvents, not a separate LedgerId',
        'checkpoint_context':c._wire(ctx),'candidate':c._wire(request),
        'source_pins':c._wire(b.sources),'policy_pin':c._wire(b.policy),
        'semantic_id':c._wire(semantic_id),'content_id':c._wire(content),
        'native_evidence_id':c._wire(entity.id),'checks':checks,
        'negative_nonmutating_checks':negative,'native_admission_preflight':'FAIL:'+native_rejection,
        'offline_definitions_verified':True,'canonical_state_unchanged':True,
        'evidence_or_receipt_admitted':False,'validation_results_created':0,
        'proof_instances_created':0,'actions_executed':0}
    emit('preparation-evidence.json',result)
    print(json.dumps({'parent_binding':'PASS','offline_materialization':'PASS',
        'A09_preflight':'BLOCKED','failed_checks':[k for k,v in checks.items() if not v],
        'native_evidence':entity.id.value}))


if __name__=='__main__':
    prepare()
