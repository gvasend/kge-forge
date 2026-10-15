"""Exact P04 A09 diagnosis/requalification; all canonical transitions remain private."""
from dataclasses import replace
from pathlib import Path
import hashlib,json,sys
from adapter.planner import codec as c,core,gates,model as m,evidence_attestation as ea,evidence_transaction as tx
R=Path(__file__).resolve().parents[2];D=R/'docs/plans';O=D/'qualification/E2_P04_A09_CONTROL_RECONCILIATION_1';Q=D/'qualification/E2_P04_CONTINUATION_INPUT_CLOSURE_1'
BID=m.ArtifactIdentity(m.IdentityKind.CONTENT_IDENTITY,'planner-bundle-v1','fa86ce94d76651ce5eccfa76c2d862243548d6d8dcaae91e74dca4e9c571c7d1')
def emit(name,obj):
    (O/name).write_bytes(c.canonical_bytes(obj))
def inputs():
    b=c.restore(D/'DETERMINISTIC_PLANNER_V0_1_E2_P04_POST_ATTEST_INSTALL_BUNDLE_1.json',BID,R)
    x=c._unwire(c.parse_json((D/'qualification/INSTALLATION_I04_1/a09-post-authentication-candidate.json').read_bytes()))
    prepared=c.parse_json((Q/'evidence-binding.json').read_bytes())
    expected=m.SemanticNativeBinding(**{k:c._unwire(v) for k,v in prepared['binding']['fields'].items()})
    payload=c.parse_json((Q/'semantic-payload.json').read_bytes());req=b.current.evidence_requirements[0]
    assert expected.content_id==c._identity(c.canonical_bytes(payload),'p04-semantic-content-v1')
    assert expected.semantic_evidence_id==c._identity(c.canonical_bytes({'payload':payload,'proposition':req.proposition,'consumer':'E2-REENTER','gate':x.gate.value}),'p04-semantic-evidence-v1')
    t=ea.materialize(**{k:c._unwire(v) for k,v in prepared['attestation']['fields'].items() if k!='attestation_id'})
    return b,tx.bind(x,t,expected),expected

def view(b):
    s=b.current;comp=core.recompute(s)
    return {'control':comp.control.value,'actionable':[a.value for a in comp.actionable],
        'selected':comp.selection.selected.value if comp.selection else None,
        'decision_ready':[[a.value for a in batch] for batch in comp.human_batches],
        'statuses':{a.id.value:a.state.value for a in s.statuses},
        'computed_statuses':{a.id.value:a.state.value for a in comp.statuses},
        'blocked':c._wire(comp.blocked),'roots':{r.id.value:r.state.value for r in s.roots},
        'slots':{r.id.value:r.state.value for r in s.slots},
        'knowledge':[k.id.value for k in s.knowledge],
        'Evidence':[{'id':e.id.value,'validated':e.validated,'validation':e.validation.value} for e in s.entities if e.kind is m.EntityKind.EVIDENCE],
        'validation_instances':len(s.validation_instances),'typed_proofs':len(s.typed_proofs),
        'proof_contracts':len(s.proof_contracts),'receipt_observations':len(s.receipt_observations),
        'receipt_admissions':len(s.receipt_admissions),
        'gate':[{'id':g.id.value,'stage':g.stage.value,'pending':g.pending.value if g.pending else None,
                 'external_complete':gates.external_complete(s,g)} for g in s.external_gates],
        'resume_allowed':core.resume_eligibility(b,R).allowed,
        'state_id':c._wire(c.snapshot_id(s)),'bundle_id':c._wire(c.bundle_id(b))}

def run(mode):
    b,x,expected=inputs();before=c.bundle_bytes(b)
    if mode=='diagnose':
        oracle={'role':'PRE_EXECUTION_ORACLE; EXPECTATIONS, NOT CANONICAL EXECUTION',
         'authority_sources':{'A09':'acceptance matrix E2-A09','A10':'acceptance matrix E2-A10','separation':'EVIDENCE-E03 lifecycle result'},
         'initial_bundle':c._wire(BID),'expected_post_A09':{
           'control':'EXTERNAL_WAIT','control_classification':'DERIVABLE; no declared validation Action, unsatisfied independent proof and named reentry, exposed external boundary',
           'actionable':[],'selected':None,'decision_ready':[],
           'Evidence_received':True,'Evidence_validated':False,'Evidence_validation':'NOT_EVALUATED',
           'gate_stage':'EVIDENCE_RECEIVED','pending':x.entity.id.value,
           'receipt_admissions_added':1,'receipt_observations_added':0,
           'validation_instances_added':0,'typed_proofs_added':0,'proof_contracts_added':0,
           'REENTER_completed':False,'REENTER_actionable':False,'FINISH_actionable':False,
           'knowledge_added':0,'root_slot_unchanged':True,'resume_allowed':False},
         'allowed_delta':['one Evidence entity (received, not validated)','one authenticated ReceiptAdmission','active gate stage/pending/history','E03 derived ActionStatus projection','two native event records and source addition'],
         'A10_stage_prerequisite_ready':True,'A10_executable_contract_ready':False,
         'validation_work_classification':'next external lifecycle event; no A10 scheduler Action is declared',
         'cold_restore_expected_control':'EXTERNAL_WAIT','replay_expected_control':'EXTERNAL_WAIT; no A10 performed'}
        emit('independent-oracle.json',oracle)
    else:
        oracle=c.parse_json((O/'independent-oracle.json').read_bytes())
    raw={p.path:(R/p.path).read_bytes() for p in x.source_additions}
    try:
        after=c.preflight_external_evidence(b,x,raw,R,expected_binding=expected)
        failure=None
    except m.PlannerError as e:
        failure=str(e);assert mode=='diagnose' and failure=='RECEIPT_CHANGED_CONTROL'
        # Only ordinary native functions construct actual simulated effects.
        admitted=c._extend_private(b,x)
        after=c._extend_private(admitted,m.ExternalEvent(x.gate,m.ExternalStage.EVIDENCE_RECEIVED,c.snapshot_id(admitted.current),x.entity.id))
        after=replace(after,sources=b.sources+x.source_additions)
    actual=view(after);pre=view(b);exp=oracle['expected_post_A09']
    entity=next(e for e in after.current.entities if e.id==x.entity.id)
    checks={'control':actual['control']==exp['control'],'actionable':actual['actionable']==[],
            'selected':actual['selected'] is None,'decision_ready':actual['decision_ready']==[],
            'received':actual['gate'][0]['stage']=='EVIDENCE_RECEIVED' and actual['gate'][0]['pending']==x.entity.id.value,
            'unvalidated':not entity.validated and entity.validation is m.ValidationState.NOT_EVALUATED,
            'no_validation':after.current.validation_instances==b.current.validation_instances,
            'no_proof':after.current.typed_proofs==b.current.typed_proofs,
            'no_proof_contract_admission':after.current.proof_contracts==b.current.proof_contracts,
            'no_observation_acceptance':after.current.receipt_observations==b.current.receipt_observations,
            'no_resume':not actual['resume_allowed'],'no_external_complete':not actual['gate'][0]['external_complete'],
            'no_knowledge':after.current.knowledge==b.current.knowledge,
            'root_slot_unchanged':after.current.roots==b.current.roots and after.current.slots==b.current.slots,
            'no_action_completion':{s.id for s in after.current.statuses if s.state is m.ActionState.COMPLETED}=={s.id for s in b.current.statuses if s.state is m.ActionState.COMPLETED},
            'two_private_events':len(after.events)==len(b.events)+2,
            'canonical_unchanged':c.bundle_bytes(b)==before,
            'no_canonical_commit':True}
    assert all(checks.values()),checks
    if mode=='diagnose':assert failure=='RECEIPT_CHANGED_CONTROL'
    else:assert failure is None
    diff={k:{'pre':c._wire(v),'post':c._wire(vars(core.recompute(after.current))[k])} for k,v in vars(core.recompute(b.current)).items() if v!=vars(core.recompute(after.current))[k]}
    result={'mode':mode,'execution_preflight':'PASS' if failure is None else failure,'pre':pre,'post':actual,
       'independent_oracle_comparisons':checks,'computation_differences':diff,'A09_READY':'YES' if failure is None else 'NO',
       'P04_EXECUTION_READY':'NO','A09_A13_EXECUTED':'NO','transient_attestation_persisted_before_commit':False,
       'command_key':c._wire(x.command_key),'parent':c._wire(x.expected_parent_event),
       'oracle_sha256':hashlib.sha256((O/'independent-oracle.json').read_bytes()).hexdigest()}
    emit(mode+'-trace.json',result)
    print(json.dumps({'mode':mode,'execution_preflight':result['execution_preflight'],'oracle_checks':len(checks),'all_pass':True,'A09_A13_EXECUTED':'NO'}))
if __name__=='__main__':run(sys.argv[1])
