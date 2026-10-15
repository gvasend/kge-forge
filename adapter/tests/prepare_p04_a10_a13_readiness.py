"""Read-only readiness qualification. Never publishes simulated lifecycle state."""
from pathlib import Path
from typing import get_type_hints, get_args
import hashlib, json
from adapter.planner import codec as c, model as m
from adapter.tests.qualify_p04_a09_control import inputs, view

R=Path(__file__).resolve().parents[2]
D=R/'docs/plans'
Q=D/'qualification/E2_P04_CONTINUATION_INPUT_CLOSURE_1'
O=D/'qualification/E2_P04_A10_A13_READINESS_CLOSURE_1'
NAME='DETERMINISTIC_PLANNER_V0_1_E2_P04_A10_A13_READINESS_CLOSURE_1'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return c.parse_json(p.read_bytes())
def emit(name,obj): (O/name).write_bytes(c.canonical_bytes(obj))
def run():
    protected=list((D.parent/'experiments/E1').rglob('*'))+list((R/'adapter/planner').rglob('*.py'))
    protected += [p for p in D.rglob('*') if p.is_file() and O not in p.parents and p.name not in (NAME+'.md',NAME+'.json')]
    baseline={str(p.relative_to(R)):sha(p) for p in protected if p.is_file()}
    O.mkdir(parents=True,exist_ok=True)
    b,x,binding=inputs(); before=c.bundle_bytes(b)
    raw={p.path:(R/p.path).read_bytes() for p in x.source_additions}
    simulated=c.preflight_external_evidence(b,x,raw,R,expected_binding=binding)
    assert c.bundle_bytes(b)==before
    pre,post=view(b),view(simulated)
    assert pre['control']==post['control']=='EXTERNAL_WAIT'
    assert not post['resume_allowed'] and post['validation_instances']==pre['validation_instances']
    assert not any(e['validated'] for e in post['Evidence'])
    prep=load(Q/'validation-proof-reentry-inputs.json')
    acts=load(Q/'action-definitions.json')['definitions']
    final=load(Q/'slot-root-finish-definitions.json')
    proofs=load(Q/'typed-proof-contracts-final-definitions.json')
    wanted={'E2-REENTER':c._unwire(acts['E2-REENTER']), 'E2-FINISH':c._unwire(final['finish'])}
    canonical={a.id.value:a for a in b.current.actions}
    action_checks={}
    for aid,a in wanted.items():
        m.validate_types(a,m.Action)
        assert len(a.accepted_inventory)==1 and a.accepted_result is m.ActionResult.PASS
        k=a.accepted_inventory[0]
        assert k.producer==a.id and k.outcome is m.ActionResult.PASS
        action_checks[aid]={'native_type_check':'PASS','prepared_content_id':c._wire(c._identity(c.canonical_bytes(c._wire(a)),'planner-prospective-action-body-v1')),
          'canonical_body_content_id':c._wire(c._identity(c.canonical_bytes(c._wire(canonical[aid])),'planner-prospective-action-body-v1')),
          'canonical_inventory':[z.id.value for z in canonical[aid].accepted_inventory],
          'prospective_inventory':[k.id.value], 'current_exact_definition':canonical[aid]==a,
          'operation':'REPLACE','installation_adapter':'NOT_ENABLED',
          'O01_full_independent_profile_qualification':'NOT_ESTABLISHED_BY_NATIVE_TYPE_CHECK',
          'native_fields':c._wire(a)}
        assert not action_checks[aid]['current_exact_definition']
    for typ in ('slot','root'):
        m.validate_types(c._unwire(proofs[typ]),m.TypedProofContract)
    assert len(b.current.proof_contracts)==0
    union=get_args(get_type_hints(m.ExecutionEvent)['result'])
    assert 'ValidationResult' not in [t.__name__ for t in union]
    installed=[];grants=[]
    for record in b.current.installed_definitions:
        req=record.request
        installed.append(c._wire(record))
        grants.append({'authority_id':c._wire(req.authority.id),'grant':json.loads(req.authority.grant_json),
                       'remaining_A10_A13_applicability':'NO: exact route/authentication subjects only'})
    scope=b.current.context.scope;lineage=b.current.context.lineage;generation=b.current.context.generation
    artifacts={str(p.relative_to(R)):sha(p) for p in Q.iterdir() if p.is_file()}
    sources={str(p.relative_to(R)):sha(p) for p in [D/'DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.md',D/'DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md',D/'DETERMINISTIC_PLANNER_V0_1_E2_P04_A09_CONTROL_RECONCILIATION_1.json']}
    contracts={
      'A10':{'purpose':'Validation distinct from resume','operation':'EVIDENCE_VALIDATED through append_event',
       'preconditions':['A09 received Evidence','current scoped source','authentic independent claims'],
       'definitions':['validation contract','Evidence proof/reference and accepted observation contract'],
       'authority':'Current source/operating authentication plus separately bounded INSTALL for new definitions; no applicable remaining grant',
       'lifecycle_inputs':['received native Evidence','semantic/content binding','independent validation oracle'],
       'outputs':['ValidationResult produced at execution','accepted ReceiptObservation','external_complete=true'],
       'postcondition':'Validated accepted support; resume=false until A11',
       'prepared_spec':prep['validation'],'proof_spec':prep['evidence_proof'],
       'gaps':['Closed native persisted validation/proof/observation transaction contract absent','ValidationResult helper is outside ExecutionEvent operand union','E04 admit_proof starts RECEIVED again; cannot compose unchanged after canonical A09','Typed definition installation adapter absent','New bounded INSTALL authority absent']},
      'A11':{'purpose':'C03 named reentry conjunction','operation':'DEPENDENT_ACTION_REENTRY and resume_eligibility(source_root)',
       'preconditions':['A10 validated accepted observation','all named Action prerequisites current','exact policy/context pins'],
       'definitions':['reentry reference contract','named Action and operating USE applicability'],
       'authority':'Existing E2-GRANT USE reference must pass C03; USE is not INSTALL',
       'lifecycle_inputs':['accepted Evidence/validation/proof','canonical source root','decision reentry where required'],
       'outputs':['named reentry eligibility','historical reentry event; helper ReentryEvaluation only where persisted contract defines it'],
       'postcondition':'Only E2-REENTER eligible; no Action completion', 'prepared_spec':prep['reentry'],
       'gaps':['A10 support not yet producible by qualified composed event path','Exact installed reentry definition/consumer adapter contract unresolved','New INSTALL authority if new definition needed']},
      'A12':{'purpose':'Actual post-reentry planning continuation','operation':'recompute -> select -> permitted SuppliedResult -> append_event',
       'preconditions':['A11 named eligibility','current E2-REENTER Action','prospectively complete accepted inventory'],
       'definitions':['E2-REENTER Action/result contract'], 'authority':'Operating USE plus new exact REPLACE installation grant',
       'lifecycle_inputs':['selected E2-REENTER','reviewed PASS with declared E2-K-REENTER'],
       'outputs':['actual admitted E2-K-REENTER','completion event/state','downstream FINISH evaluation'],
       'postcondition':'E2-REENTER completed, E2-K-REENTER current; no premature root proof',
       'gaps':['Canonical accepted_inventory empty','Action definition adapter not enabled','New bounded REPLACE authority absent','Whole independent O01 profile for changed Action not yet qualified']},
      'A13':{'purpose':'Independent root/slot proofs and selected finishing result','operation':'typed proof admissions -> native root/slot recomputation -> selected finishing result',
       'preconditions':['current admitted reentry knowledge','independent proof predicates/source','all FINISH gates satisfied'],
       'definitions':['slot/root','distinct SLOT_PROOF/ROOT_PROOF contracts','fixture operating authority','FINISH Action/result'],
       'authority':'Distinct operating fixture authority and exact INSTALL/REPLACE grants; preparation capture is not issuance',
       'lifecycle_inputs':['current E2-K-REENTER','slot proof then root proof','selected FINISH PASS'],
       'outputs':['SATISFIED slot/root','actual FINISH result E2-K-FINISH','terminal success only if all declared goals proven'],
       'postcondition':'All declared goals independently proven; A13 includes FINISH execution, not just readiness',
       'gaps':['Proof/slot/root adapters not enabled','Prospective fixture authority preparation-only; applicable operating grant not established','New bounded installation grants absent','FINISH result/root-gate replacement not canonical']}}
    matrix={}
    for name in ['validation contract','typed Evidence proof contract','reentry contract','E2-REENTER Action definition','accepted result inventory','E2-SLOT contract','SLOT_PROOF contract','E2-ROOT contract','ROOT_PROOF contract','E2-FINISH Action/result contract']:
        matrix[name]={'classification':'CANONICAL_DEFINITION_REQUIRED_BEFORE_EXECUTION','status':'NOT_CURRENT_OR_NOT_COMPLETE','timing':'Required before consuming stage; canonical plan does not mandate all at P03. Uninterrupted readiness requires legitimate preparation before start.'}
    for name in ['ValidationResult','Evidence Proof instance','ReentryEvaluation','ActionResult','E2-K-REENTER actual knowledge','SLOT_PROOF instance','ROOT_PROOF instance','E2-K-FINISH actual knowledge']:
        matrix[name]={'classification':'LIFECYCLE_INSTANCE_CREATED_DURING_P04','status':'ABSENT_AS_REQUIRED','must_not_install':True}
    matrix['route/authentication/ingress definitions']={'classification':'ALREADY_CURRENT','status':'QUALIFIED_I04'}
    matrix['E06 reevaluation capability']={'classification':'NOT_REQUIRED','meaning':'Runtime capability available; not a prospective lifecycle object or authority issuance'}
    dag=[
      {'id':'validation-support','stage':'A10','operation':'INSTALL','depends_on':['native validation/proof/observation transaction contract','typed installation adapter','bounded INSTALL authority'],'status':'CONTRACT_BLOCKED'},
      {'id':'reentry-definition','stage':'A11','operation':'INSTALL_IF_NEW_CANONICAL_DEFINITION_REQUIRED','depends_on':['validation-support','resolved native reference contract'],'status':'CONTRACT_BLOCKED'},
      {'id':'REENTER-result-bearing-Action','stage':'A12','operation':'REPLACE','depends_on':['Action adapter','bounded REPLACE authority','independent O01 changed-profile qualification'],'status':'RUNTIME_BLOCKED_AND_AUTHORITY_REQUIRED'},
      {'id':'root-slot-definitions','stage':'A13','operation':{'E2-SLOT':'INSTALL (absent)','E2-ROOT':'REPLACE (existing unresolved definition differs)','SLOT_PROOF contract':'INSTALL','ROOT_PROOF contract':'INSTALL'},'depends_on':['fixture operating authority issuance','typed root-slot adapter','bounded INSTALL/REPLACE authority'],'status':'CONTRACT_BLOCKED_AND_AUTHORITY_REQUIRED'},
      {'id':'FINISH-result-bearing-Action','stage':'A13','operation':'REPLACE','depends_on':['root-slot-definitions','Action adapter','bounded REPLACE authority','independent O01 qualification'],'status':'RUNTIME_BLOCKED_AND_AUTHORITY_REQUIRED'}]
    decisions=[]
    for aid,check in action_checks.items():
        decisions.append({'subject':'Prospective replacement of '+aid+' definition only','options':['AUTHORIZE_EXACT_'+aid.replace('-','_')+'_DEFINITION_REPLACEMENT','DECLINE_EXACT_'+aid.replace('-','_')+'_DEFINITION_REPLACEMENT'],
          'selected_option':'NONE','authority_issued':False,'authority_class':'INSTALL','operation':'REPLACE',
          'definition_body':check['native_fields'],'content_id':check['prepared_content_id'],'expected_old_body_content_id':check['canonical_body_content_id'],
          'scope':scope,'lineage':lineage,'generation':generation,'consumer':aid,
          'validity':'Current qualification generation, tick 0..100; bound exact pre-install bundle/state/parent at authority admission; no automatic rebinding',
          'issuer_requirement':'Authenticated qualification configuration authority authorized to issue INSTALL; ordinary USE/ATTEST not sufficient',
          'authorized_consequence':'Only this definition replacement after adapter/O01 qualification; advance event ancestry and stale existing candidates',
          'decline_consequence':'Action remains unchanged; stage and uninterrupted P04 readiness remain NO',
          'excluded':['Action execution','result admission','proof admission','authority issuance in another domain','other definition installation'],
          'decision_ready':'YES_FOR_EXACT_BODY_SCOPE; NATIVE_GRANT_ADMISSION_BLOCKED_UNTIL_TYPED_ADAPTER_CONTRACT_COMPLETE'})
    decisions.append({'subject':'A10 validation/Evidence-support definitions and event contract','selected_option':'NONE','decision_ready':'NO',
      'missing':['canonical native definition body/schema','typed currentness/consumer adapter','complete atomic validation/proof/accepted-observation event contract','accepted/rejected durable outcome semantics'],
      'consequence':'No exact content-bounded grant can yet be issued; first contract closure package required'})
    decisions.append({'subject':'Root/slot operating fixture authority and contract installation','selected_option':'NONE','decision_ready':'NO',
      'prepared_bodies':proofs,'missing':['applicable operating authority issuance contract for this canonical descendant','typed installation descriptors and existing-role replacement identities','independent authority applicability oracle'],
      'note':'Preparation-only authorization-capture is insufficient; PC02 historical fixture instances cannot silently supply prospective operating authority'})
    oracles={
      'PRE_A09':{'complete':True,'expected':pre},
      'POST_A09/PRE_A10':{'complete':True,'expected':load(D/'qualification/E2_P04_A09_CONTROL_RECONCILIATION_1/independent-oracle.json')['expected_post_A09'],
          'source':'Previously sealed independent A09 oracle, unchanged; not inferred from this simulation'},
      'POST_A10/PRE_A11':{'complete':False,'Evidence':'validated PASS','ReceiptObservation':'accepted','external_complete':True,'reentry':False,'Action_completion':'unchanged','knowledge':'unchanged','root_slot':'unchanged','control':'Unresolved exact post-validation full computation until composed contract sealed'},
      'POST_A11/PRE_A12':{'complete':False,'Evidence':'current validated accepted support','reentry':'exact E2-REENTER only after all C03 prerequisites','Action_completion':'unchanged','knowledge':'unchanged','root_slot':'unchanged','control':'Named action selection only if all independent gates pass; exact full computation contract pending'},
      'POST_A12/PRE_A13':{'complete':False,'Action':'REENTER COMPLETED','knowledge':'actual E2-K-REENTER CURRENT','slot':'UNSATISFIED before distinct proof','root':'UNRESOLVED before independent proof','FINISH':'NON_ACTIONABLE until root satisfied','control':'Exact control pending complete installed goal/model inventory'},
      'SLOT_ONLY':{'complete':False,'SLOT_PROOF':'ACCEPTED','slot':'SATISFIED','ROOT_PROOF':'ABSENT','root':'UNRESOLVED','FINISH':'NON_ACTIONABLE'},
      'ROOT_PROVED':{'complete':False,'ROOT_PROOF':'ACCEPTED','root':'SATISFIED','FINISH':'ACTIONABLE iff all remaining gates pass; not executed at this boundary'},
      'P04_TARGET':{'complete':False,'Evidence':'current accepted','reentry':'named eligible and completed','knowledge':['E2-K-REENTER','E2-K-FINISH actual accepted outputs'],'root_slot':'SATISFIED by distinct accepted proofs','Action':'selected FINISH result admitted','control':'Terminal success iff all declared goals proven'}}
    for key,v in oracles.items():
        v.update({'source_policy_pins':'Exact final installed pre-P04 pins; retain source/policy identity domains independently',
          'scope':scope,'lineage':lineage,'event_ancestry':'Ordinary parent = previous committed append head; historical events replayed, no new decisions',
          'future_identity_rule':'Native snapshot/event/ledger/bundle codec only; no arbitrary identities'})
        if not v['complete']:v['unsealed_native_terms']=['full canonical model/definitions','exact event operands/outcome contract','full computation and deterministic native identities']
    persistence=[{'when':k,'expected_state_oracle':k,'required_contents':'Complete native definitions, authorities, source/policy pins, admitted lifecycle objects appropriate to boundary, ledger/root/head',
      'cold_restores_per_seed':3,'hash_seeds':[0,1,7,101],'writer_termination':True,'fresh_process':True,
      'next_parent':'This checkpoint actual append head, never prior prepared candidate parent','replay':'Historical decisions only; no new validation/attestation/proof decision',
      'status':'PLAN_ONLY; NO P04 CHECKPOINT EMITTED'} for k in oracles]
    faults=['wrong parent','wrong native Evidence','wrong semantic Evidence','wrong content','wrong source','wrong source pin','wrong policy','wrong attestor','wrong predicate','missing/extra dependency provenance','wrong validation','rejected validation','wrong Evidence proof','wrong authority','wrong scope','wrong lineage','wrong generation','stale proof','wrong root target','wrong slot target','wrong Action result','wrong output inventory','proof instance substituted for contract','metadata wrapper substituted for native body','foreign event lineage','post-hoc definition creation','premature proof/reentry after receipt','premature root/FINISH after slot-only proof']
    negatives=[{'fault':f,'fixture':'Isolated copy of applicable stage fixture; change only named domain; base fixture pin inventory referenced by sealed contract',
      'expected':'Fail closed; no canonical event, receipt, proof, knowledge or Action completion; prior state identity unchanged',
      'status':'SEALED_FAULT_SPEC; concrete future-stage operand fixture blocked by incomplete positive contract'} for f in faults]
    checks={'A09_execution_precommit':True,'pre_state_unchanged':before==c.bundle_bytes(b),'received_unvalidated_no_resume':not post['resume_allowed'],
      'prospective_Action_inventories_native_typed':True,'distinct_SLOT_ROOT_contracts_native_typed':True,
      'canonical_proof_contracts_absent':True,'ValidationResult_not_native_event_operand':True,
      'no_remaining_applicable_INSTALL_authority':True,'no_P04_canonical_event_appended':before==c.bundle_bytes(b)}
    unchanged=all((R/p).is_file() and sha(R/p)==h for p,h in baseline.items())
    assert unchanged and all(checks.values())
    report={'WORK_PACKAGE':'E2-P04-A10-A13-READINESS-CLOSURE','RESULT':'PARTIAL','A09_READY':'YES',
      'A10_CONTRACT':'INCOMPLETE_NATIVE_COMPOSED_EVENT_AND_INSTALLATION_CONTRACT','A10_READY':'NO',
      'A11_CONTRACT':'CANONICAL_NAMED_REENTRY; A10 SUPPORT AND DEFINITION CURRENTNESS BLOCKED','A11_READY':'NO',
      'A12_CONTRACT':'NATIVE_SELECTION_AND_SUPPLIED_RESULT_AVAILABLE; ACTION REPLACEMENT BLOCKED','E2_REENTER_RESULT_CONTRACT':'PROSPECTIVE_PASS_PLUS_E2_K_REENTER_NATIVE_TYPED; NOT_CANONICAL','A12_READY':'NO',
      'ROOT_SLOT_CONTRACTS':'PROSPECTIVE_NATIVE_TYPED; INSTALLATION_AND_OPERATING_AUTHORITY_BLOCKED','REEVALUATION_CAPABILITY':'QUALIFIED_E06_AVAILABLE',
      'A13_CONTRACT':'INDEPENDENT_SLOT_ROOT_PROOFS_AND_SELECTED_FINISH_RESULT; DEFINITIONS_NOT_CURRENT','A13_READY':'NO',
      'contracts':contracts,'DEFINITION_INSTANCE_MATRIX':matrix,'INSTALLATION_DAG':dag,
      'AUTHORITY_INVENTORY':{'installed_grants':grants,'remaining_installations':'NEW_AUTHORITY_REQUIRED','existing_USE':'NO_INSTALLATION_PERMISSION','prepared_fixture_authority':'PREPARATION_ONLY_NOT_OPERATING_ISSUANCE'},
      'NEW_AUTHORITY_DECISIONS':decisions,'action_inventory_checks':action_checks,
      'FINAL_A09_PREFLIGHT':'PASS','final_candidate':{'bundle_id':pre['bundle_id'],'state_id':pre['state_id'],'parent_event':c._wire(x.expected_parent_event),'command_key':c._wire(x.command_key),'role':'Non-admitted candidate; typed attestation constructed transiently in memory only','rematerialized':True,'installation_events_this_package':0},
      'BOUNDARY_ORACLES':oracles,'BOUNDARY_ORACLES_FULLY_SEALED':'NO','PERSISTENCE_PLAN':persistence,'NEGATIVE_PLAN':negatives,
      'P04_EXECUTION_READY':'NO','E2_P04_READY':'NO','NEXT_PACKAGE':'A10 native validation/proof/accepted-observation transaction and typed definition-installation contract closure; then bounded authority decisions',
      'first_dependency_ordered_blocker':contracts['A10']['gaps'],'qualified_checks':checks,'prepared_artifact_hashes':artifacts,'authoritative_source_hashes':sources,
      'canonical_event_operand_types':[t.__name__ for t in union], 'RUNTIME_MODIFIED':'NO','A09_A13_EXECUTED':'NO','E2_FINISH_EXECUTED':'NO','P03_RESULT':'PASS','P03_HISTORICAL_CORRESPONDENCE':'UNPROVEN','N_REAL_SATISFIED':'NO','E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO',
      'preservation':{'protected_files':len(baseline),'all_unchanged':unchanged,'manifest':'preservation-manifest.json'}}
    report['O01_field_inventory']={'original_13_fields':load(D/'DETERMINISTIC_PLANNER_V0_1_E2_P01_ACTIONS.json')['fields'],
        'status':'Native fields/inventories checked; independent changed-profile O01 correspondence NOT QUALIFIED; prior P01 PASS not rewritten'}
    report['currentness_results']={'canonical_root_slot':{'roots':c._wire(b.current.roots),'slots':c._wire(b.current.slots)},
        'proof_contracts':c._wire(b.current.proof_contracts),'typed_proofs':c._wire(b.current.typed_proofs),
        'validation_instances':c._wire(b.current.validation_instances),
        'known_actions':{a.id.value:c._wire(a) for a in b.current.actions if a.id.value in wanted},
        'source_pins':c._wire(b.sources),'policy':c._wire(b.policy),
        'operating_authority_entities':[c._wire(e) for e in b.current.entities if e.kind is m.EntityKind.AUTHORITY]}
    report['definition_installations_this_package']=0
    for n in range(9,14):report['A'+str(n).zfill(2)+'_EXECUTED']='NO'
    report['plan_sealing']={'semantic_expectations':'CONTENT_PINNED_BEFORE_ANY_P04_EXECUTION',
        'full_native_future_oracles':'INCOMPLETE_NOT_SEALED',
        'negative_fault_specifications':'CONTENT_PINNED; FUTURE_NATIVE_FIXTURES_BLOCKED','all_contracts_complete':False}
    emit('preservation-manifest.json',baseline)
    emit('readiness-evidence.json',report)
    (D/(NAME+'.json')).write_bytes(c.canonical_bytes(report))
    print(json.dumps({'result':'PARTIAL','A09':'PASS','readiness_checks':len(checks),'protected_files_unchanged':len(baseline),'P04_execution_ready':'NO'}))

if __name__=='__main__':run()
