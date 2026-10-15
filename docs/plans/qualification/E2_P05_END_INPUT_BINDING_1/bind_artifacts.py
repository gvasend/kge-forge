"""Read-only evidence bindings. This is not an END runner or Planner adapter."""
import hashlib
import json
from pathlib import Path

from adapter.planner import codec as c, model as m, installation as install
from adapter.planner import typed_proofs as tp

ROOT = Path(__file__).resolve().parents[4]
DOCS = ROOT / 'docs/plans'
OUT = Path(__file__).resolve().parent
PREFIX = 'DETERMINISTIC_PLANNER_V0_1_'


def path(name, ext='json'):
    return DOCS / (PREFIX + name + '.' + ext)


def read(p):
    # Qualification reports include elapsed-time decimals. They are metadata;
    # native envelopes below use the strict parser and typed validation.
    return c.parse_json(p.read_bytes(), allow_floats=True)


def rel(p):
    return p.relative_to(ROOT).as_posix()


def pin(p, pointer=''):
    return {'path':rel(p),'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest(), 'pointer':pointer}


def uid(i):
    return i.namespace + ':' + i.sha256


def save(name, value):
    p = OUT / name
    p.write_bytes(c.canonical_bytes(value))
    return pin(p)


def main():
    plan = read(path('CANONICAL_QUALIFICATION_EXPERIMENT_1'))
    cases = {x['CASE_ID']:x for x in plan['cases']}
    end = cases['E2-END']
    interface = read(path('E2_PC04_END'))
    p04 = read(path('E2_P04_CANONICAL_EXECUTION_RETRY_1_RESULT'))
    p02 = read(path('E2_P02_RETRY_4_RESULT'))
    prefix = read(path('E2_P02_RETRY_3_RESULT'))
    p03 = read(path('P03_PROSPECTIVE_CHECKPOINT_QUALIFICATION_1'))
    scope_path = DOCS / 'qualification/P03_PROSPECTIVE_CHECKPOINT_1/sources/qualification-scope-authority.json'
    scope = read(scope_path)
    p03_contract_path = scope_path.with_name('qualification-contract.json')
    p03_contract = read(p03_contract_path)
    assert p02['result'] == p03['result'] == p04['RESULT'] == 'PASS'
    assert scope['selected_option'] == 'AUTHORIZE_PROSPECTIVE_P03_CHECKPOINT_QUALIFICATION'
    assert 'historical reconstruction' in scope['exclusions']

    # Native type/identity inspection, with no event application/admission/commit.
    snapshots = {}
    for name in ('E2_P02_INITIAL_SNAPSHOT','E2_AUTHORITATIVE_HANDOFF_SNAPSHOT_1',
                 'E2_HUMAN_DECISION_ALLOW_POST_SNAPSHOT_1'):
        p = path(name)
        state = c._unwire(c.parse_json(p.read_bytes())['snapshot'])
        m.validate_types(state,m.Snapshot)
        assert c.snapshot_bytes(state) == p.read_bytes()
        snapshots[name] = {'pin':pin(p,'/snapshot'),'id':uid(c.snapshot_id(state)),
                           'context':c._wire(state.context),'snapshot':c._wire(state)}
    target_path = path('E2_P04_CANONICAL_TARGET_BUNDLE_1')
    raw = target_path.read_bytes()
    bundle = c._unwire(c.parse_json(raw)['bundle'])
    m.validate_types(bundle,m.PersistenceBundle)
    assert c.canonical_bytes({'schema':'PLANNER-BUNDLE-1','bundle':c._wire(bundle)}) == raw
    algebraic_bundle = uid(c._identity(raw,'planner-bundle-v1'))
    assert algebraic_bundle == p04['FINAL_P04_BUNDLE_ID']
    assert uid(c.snapshot_id(bundle.current)) == p04['FINAL_STATE_ID']
    assert snapshots['E2_P02_INITIAL_SNAPSHOT']['id'].endswith(p02['initial_snapshot'])
    assert snapshots['E2_HUMAN_DECISION_ALLOW_POST_SNAPSHOT_1']['id'].endswith(p02['post_decision_snapshot'])
    events = [c._wire(e) for e in bundle.events]
    trace_path = DOCS / 'qualification/E2_P04_CANONICAL_EXECUTION_RETRY_1/execution-trace.json'
    trace = {x['checkpoint']:x for x in read(trace_path)}
    current = bundle.current
    native = c._wire(current)
    checkpoint_path = path('P03_PROSPECTIVE_CHECKPOINT_BUNDLE_1')
    old_checkpoint = c._unwire(c.parse_json(checkpoint_path.read_bytes())['bundle'])
    assert c._wire(old_checkpoint.initial) == c._wire(bundle.initial)
    assert c._wire(old_checkpoint.events) == c._wire(bundle.events[:2])
    assert all(p in bundle.sources for p in old_checkpoint.sources)
    assert old_checkpoint.policy == bundle.policy

    missing = [
        {'input':'E2-A03.native_result_event_trace','classification':'ARTIFACT_MISSING',
         'required':'Actual native result/event operands and parent/pre-state/after-state ancestry for CHECK and COLLECT, required by A03 and END.',
         'known_outputs':'P02 authoritative result PASS; trace native state IDs and E2-K-CHECK/E2-K-COLLECT retained.',
         'cannot_substitute':['report-only SuppliedResult labels','ActionResult PASS enum as event identity',
                             'KnowledgeId as event identity','freshly reconstructed events presented as historical execution',
                             'P03 authored completed-prefix premises'],
         'evidence':[pin(path('E2_P02_RETRY_3_RESULT'),'/events_admitted'),pin(OUT/'P02-native-event-artifact-search.json')]},
        {'input':'E2-A04.prepare_result_event_ancestry','classification':'ARTIFACT_MISSING',
         'required':'Actual PREPARE result event linked to the retained accepted dossier/handoff state; archive report/knowledge is not an ExecutionEvent.'},
        {'input':'E2-A05.recorded_decision_event_ancestry','classification':'ARTIFACT_MISSING',
         'required':'Original event-bearing decision trace, distinct from the later prospective RecordedDecision in another lineage.'},
        {'input':'E2-A06.request_wait_event_trace','classification':'ARTIFACT_MISSING',
         'required':'Native request-ready/waiting occurrence history; retained original gate history is empty.'},
        {'input':'END.original_prefix_to_checkpoint_to_target_ancestry','classification':'IDENTITY_MISMATCH',
         'required':'Full authoritative A01-A13 end-to-end historical path or explicitly governing END acceptance mapping.',
         'actual':'Original P02 post-state 8d77... is not the initial/prefix state of the authorized prospective P03/P04 ledger.',
         'limit':'P03 scope amendment binds A07/A08 fidelity, not original historical correspondence or a new END acceptance waiver.'}]

    contract = {
        'END_ID':'E2-END','END_TYPE':'EXPERIMENT_ACCEPTANCE_CASE',
        'native_model_entity':False,'native_Action_Root_Review_node':False,
        'authoritative_case':end,'source':pin(path('CANONICAL_QUALIFICATION_EXPERIMENT_1'),
            '/cases/'+str(next(i for i,x in enumerate(plan['cases']) if x['CASE_ID']=='E2-END'))),
        'matrix_source':pin(path('CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1','md')),
        'END_INPUTS':interface['dependencies'],'END_INPUT_COUNT':len(interface['dependencies']),
        'END_INPUT_TYPES':['canonical definitions/model','source/authority/proof/receipt contracts',
                           'independent phase/persistence oracles','qualified admission capability',
                           'determinism process/oracle interface','post-reentry continuation contract'],
        'stage_coverage_input_count':13,
        'END_REQUIRED_ACTIONS':['E2-COLLECT','E2-CHECK','E2-PREPARE','E2-DECIDE','E2-REENTER','E2-FINISH'],
        'END_REQUIRED_KNOWLEDGE':['E2-K-CHECK','E2-K-COLLECT','E2-K-PREPARE','decision-choice:E2-DECIDE','E2-K-REENTER','E2-K-FINISH'],
        'END_REQUIRED_PROOFS':['current obligation Proof computed at A11','complete independently source-bound SLOT_PROOF and ROOT_PROOF',
                               'dossier fact/check proofs at A04/A05'],
        'END_REQUIRED_EVENTS':['A03 acquisition result history','A04 PREPARE result','A05 recorded decision','A06 request/wait',
                               'A09 admitted Evidence/receipt pair','A10 validation/support','A11 dependent-action and decision reentry',
                               'A12 supplied permitted REENTER result','A13 exact deferred installs/proof admissions/FINISH result'],
        'END_REQUIRED_AUTHORITIES':'Only stage-specific applicable source/authentication/choice/USE/semantic/INSTALL authorities; no native END authority class.',
        'END_REQUIRED_CONFIGURATION':'Six O01 definitions, exact source/policy and all actual governed configuration history for the P04 path.',
        'END_COMPLETION_RULE':end['EXPECTED_STATE'],
        'END_CONTROL_RULE':'No END-specific native control transition. A13 terminal success only when declared goals proven; END qualification must satisfy all stage/persistence/determinism terms.',
        'binding_representation':'Read-only evidence manifest with explicit native identity domains/pointers; not a new canonical Planner object or Action operand.',
        'native_adapter_required':'NO; repository declares no native END consumer/input-slot API to adapt.',
        'contract_underspecification':'No authorized replacement relation from the missing original P02 event history to a complete END historical lifecycle is defined.'}
    contract_file = save('END-contract.json',contract)

    stage_events = {9:[10,11],10:[12],11:[13,14],12:[15],13:[16,17,18,19,20]}
    stage_checkpoint = {9:'post-a09',10:'post-a10',11:'post-a11',12:'post-a12',13:'isolated-p04-target'}
    archive = snapshots['E2_HUMAN_DECISION_ALLOW_POST_SNAPSHOT_1']['snapshot']
    old_knowledge = {x['id']['value']:x for x in archive['knowledge']}
    new_knowledge = {x.id.value:c._wire(x) for x in current.knowledge}
    reenter = next(a for a in current.actions if a.id.value == 'E2-REENTER')
    use_authorities = [c._wire(e) for e in current.entities if m.AuthorityClass.USE in e.permissions]
    def installation_authorities(sequences):
        return [{'role':'HISTORICAL_DEFINITION_INSTALL_AUTHORITY_NOT_EXECUTION_PERMISSION',
                 'event_sequence':n,'event_id':events[n-1]['identity'],
                 'authority':events[n-1]['result']['authority']} for n in sequences]
    inventory = []
    for number in range(1,14):
        name = 'E2-A%02d' % number
        owner = 'E2-P02' if number <= 6 else ('E2-P03' if number <= 8 else 'E2-P04')
        sources = []
        result = {'STEP_ID':name,'PURPOSE':cases[name]['PURPOSE'],'OWNING_PACKAGE':owner,
                  'canonical_owner_result':'PASS', 'canonical_execution_status':'AUTHORITATIVE_OWNER_PASS; evidence limits below',
                  'CANONICAL_RESULT':'Authoritative package PASS; stage-specific native values below',
                  'OUTPUTS':[], 'KNOWLEDGE_OUTPUTS':[], 'PROOFS':[], 'EVENTS':[], 'AUTHORITIES':[],
                  'source_classification':'CANONICAL_EXECUTION','binding_status':'BOUND',
                  'input_type':'Stage-specific native state/event plus comparison/occurrence evidence',
                  'canonical_contract':cases[name]}
        if number == 1:
            result['canonical_execution_status']='CANONICAL_CONFIGURATION_AND_O01_QUALIFICATION; NO_ACTION_EXECUTION_REQUIRED'
            result['source_classification']='CANONICAL_CONFIGURATION'
            result['OUTPUTS']=[{'SnapshotId':snapshots['E2_P02_INITIAL_SNAPSHOT']['id'],
                                'ActionIds':sorted(a['id']['value'] for a in snapshots['E2_P02_INITIAL_SNAPSHOT']['snapshot']['actions']),
                                'independent_O01':pin(path('E2_P01_RETRY_1_RESULT'),'/qualification_checks')}]
            sources=[pin(path('E2_P02_INITIAL_SNAPSHOT'),'/snapshot'),pin(path('E2_P01_RETRY_1_RESULT'))]
            result['FINAL_STATE_EFFECT']='Canonical six-Action initial universe; no knowledge/result occurrence from definitions.'
        elif number == 2:
            result['canonical_execution_status']='READ_ONLY_SELECTION_REPORTED_FOR_CANONICAL_INITIAL_STATE'
            result['OUTPUTS']=[{'selected_ActionId':{'$type':'ActionId','value':'E2-CHECK'},'initial_SnapshotId':snapshots['E2_P02_INITIAL_SNAPSHOT']['id'],
                                'expected_control':'RUNNABLE','selection_is_execution':False}]
            sources=[pin(path('E2_P02_INPUT_VALIDATION'),'/initial_selection'),pin(path('E2_P02_RETRY_3_RESULT'),'/trace/0')]
            result['FINAL_STATE_EFFECT']='No event/knowledge/root/slot mutation from selection.'
        elif number in (3,4):
            chosen=prefix['trace'][:2] if number==3 else prefix['trace'][2:]
            result['OUTPUTS']=[{'retained_native_trace_report':x} for x in chosen]
            names=['E2-K-CHECK','E2-K-COLLECT'] if number==3 else ['E2-K-PREPARE']
            result['KNOWLEDGE_OUTPUTS']=[{'native_KnowledgeId':old_knowledge[n]['id'],'record':old_knowledge[n],
                                         'archive_SnapshotId':snapshots['E2_HUMAN_DECISION_ALLOW_POST_SNAPSHOT_1']['id']} for n in names]
            result['binding_status']='MISSING_CANONICAL_OUTPUT'
            result['missing_part']='Native ExecutionEvent operand/identity/ancestry; reported result and archived KnowledgeRecord are present.'
            result['CANONICAL_RESULT']='Reported PASS; retained accepted KnowledgeRecords; original native event witnesses not recovered'
            result['FINAL_STATE_EFFECT']='Reported accepted bounded knowledge and producer completion; historical event chain not retained.'
            sources=[pin(path('E2_P02_RETRY_3_RESULT'),'/trace'),pin(path('E2_P02_RETRY_4_RESULT'),'/evidence_chain'),pin(path('E2_HUMAN_DECISION_ALLOW_POST_SNAPSHOT_1'),'/snapshot/knowledge')]
            if number==4:
                result['OUTPUTS'].append({'handoff_SnapshotId':snapshots['E2_AUTHORITATIVE_HANDOFF_SNAPSHOT_1']['id'],
                                          'dossier':archive['decisions'][0]['dossier']})
                result['PROOFS']=[{'kind':'Dossier fact/check proof and ValidationInstances','source':pin(path('E2_AUTHORITATIVE_HANDOFF_SNAPSHOT_1'),'/snapshot/validation_instances')}]
        elif number == 5:
            d=archive['decisions'][0]
            authorities=[x for x in archive['entities'] if x['id']['value']=='E2-GRANT']
            result['OUTPUTS']=[{'record':d['record'],'choice':d['recorded_choice'],'decision_state':d['stage'],
                                'post_SnapshotId':snapshots['E2_HUMAN_DECISION_ALLOW_POST_SNAPSHOT_1']['id']}]
            result['AUTHORITIES']=authorities
            result['CANONICAL_RESULT']=d['recorded_choice']
            result['KNOWLEDGE_OUTPUTS']=[old_knowledge['decision-choice:E2-DECIDE']]
            result['binding_status']='MISSING_CANONICAL_OUTPUT'
            result['missing_part']='Original RecordedDecision ExecutionEvent; accepted decision and bounded authority are retained in archive Snapshot.'
            result['FINAL_STATE_EFFECT']='Original decision recorded/DECIDE completed, bounded E2-GRANT, external wait reported; not the later prospective event.'
            sources=[pin(path('E2_HUMAN_DECISION_ALLOW_RETRY_1_RESULT')),pin(path('E2_HUMAN_DECISION_ALLOW_RETRY_1_TRACE')),pin(path('E2_HUMAN_DECISION_ALLOW_POST_SNAPSHOT_1'),'/snapshot/decisions')]
        elif number == 6:
            result['OUTPUTS']=[{'SnapshotId':snapshots['E2_HUMAN_DECISION_ALLOW_POST_SNAPSHOT_1']['id'],
                                'gate':archive['external_gates'][0],'external_wait_oracle':p02['external_wait_oracle']}]
            result['binding_status']='MISSING_CANONICAL_OUTPUT'
            result['missing_part']='Native request-ready/waiting event trace; retained old gate history is empty.'
            result['AUTHORITIES']=[{'role':'ORIGINAL_BOUNDED_USE_GRANT',
                                   'entity':next(x for x in archive['entities'] if x['id']['value']=='E2-GRANT')}]
            result['CANONICAL_RESULT']='EXTERNAL_WAIT reported; known rule/Evidence absent; native occurrence trace not recovered'
            result['FINAL_STATE_EFFECT']='Known-rule evidence-absent EXTERNAL_WAIT snapshot retained; occurrence/ancestry not supplied by gate stage.'
            sources=[pin(path('E2_P02_RETRY_4_RESULT'),'/external_wait_oracle'),pin(path('E2_HUMAN_DECISION_ALLOW_POST_SNAPSHOT_1'),'/snapshot/external_gates')]
        elif number in (7,8):
            result['source_classification']='AUTHORIZED_REPLACEMENT_QUALIFICATION'
            result['canonical_execution_status']='PASS_UNDER_ALREADY_AUTHORIZED_PROSPECTIVE_P03_SCOPE'
            result['OUTPUTS']=[{'native_checkpoint_bundle':p03['prospective_checkpoint_bundle_id'],
                                'SnapshotId':p03['prospective_checkpoint_state_id'],'append_head':p03['append_head'],
                                'qualification_scope_authority':p03['qualification_scope_authority_id'],
                                'original_historical_correspondence':'UNPROVEN'}]
            result['AUTHORITIES']=[{'scope_authority':p03['qualification_scope_authority_id'],'source':pin(scope_path)}]
            result['CANONICAL_RESULT']='Prospective checkpoint fidelity PASS at amended A07/A08 scope; original historical correspondence UNPROVEN'
            result['FINAL_STATE_EFFECT']='Exact prospective checkpoint persisted/terminated/cold-restored; valid P04 starting component. No original prefix history asserted.'
            sources=[pin(path('P03_PROSPECTIVE_CHECKPOINT_QUALIFICATION_1'),'/p03_original_case_evaluation'),pin(checkpoint_path),pin(scope_path),pin(p03_contract_path)]
        else:
            t=trace[stage_checkpoint[number]]
            result['canonical_execution_status']='COMMITTED_CANONICALLY; EXACT_OWNER_TRACE_AND_EVENT_WITNESSES'
            result['EVENTS']=[events[i-1] for i in stage_events[number]]
            result['OUTPUTS']=[{'pre_SnapshotId':t['pre_state'],'post_SnapshotId':t['post_state'],
                                'append_head':t['head'],'native_operands':t['operands']}]
            result['FINAL_STATE_EFFECT']=cases[name]['EXPECTED_STATE']
            sources=[pin(target_path,'/bundle/events'),pin(trace_path,'/'+str(list(trace).index(stage_checkpoint[number]))),pin(path('E2_P04_CANONICAL_EXECUTION_RETRY_1_RESULT'))]
            if number == 9:
                result['AUTHORITIES']=[{'role':'OPERATING_ATTEST_AUTHORITY_BINDING',
                    'binding':b} for b in events[3]['result'].get('authority_bindings',[])]
                result['AUTHORITIES'] += [{'role':'CANONICAL_AUTHENTICATION_ENTITY','entity':c._wire(e)}
                    for e in current.entities if m.AuthorityClass.ATTEST in e.permissions]
                result['AUTHORITIES'] += installation_authorities([3,4,5])
                result['CANONICAL_RESULT']='Actual EvidenceSourceAdmission and EVIDENCE_RECEIVED pair; received/NOT_EVALUATED'
                result['OUTPUTS'].append({'native_Evidence_EntityId':p04['EVIDENCE_ID'],'receipt_admission_reference':p04['RECEIPT_ID'],
                                         'semantic_Evidence_domain':'From exact admission operand; never substitute for native EntityId'})
            if number == 10:
                result['AUTHORITIES']=installation_authorities([6])
                result['authority_boundary']='Validation uses installed contract/source/validator rules; no new validation operating authority is inferred.'
                result['CANONICAL_RESULT']='Actual ValidationResult ACCEPTED and current support; no proof admission or reentry execution'
                result['OUTPUTS'].append({'ValidationResultId':p04['VALIDATION_RESULT_ID'],'SupportId':p04['SUPPORT_ID']})
            if number == 11:
                result['AUTHORITIES']=[{'role':'SEPARATE_C03_ACTION_AUTHORITY','entity':e} for e in use_authorities]
                result['authority_boundary']='Neither computed Proof nor ResumeEligibility nor reentry event is an authority grant.'
                result['CANONICAL_RESULT']='Computed obligation Proof satisfied; both canonical reentry events accepted; C03 eligible at post-A11 boundary'
                result['PROOFS']=[t['operands']['Proof'] if 'Proof' in t['operands'] else t['checks']['typed_obligation_Proof']['actual']]
                result['computed_C03']=t['operands']['C03']
                result['computed_result_identity']='No standalone Proof/ResumeEligibility ID; bound to exact canonical post-state and input identities.'
            if number == 12:
                result['AUTHORITIES']=[{'role':'ACTION_USE_AUTHORITY','entity':e} for e in use_authorities]
                result['AUTHORITIES'] += installation_authorities([7])
                result['Action_authority_predicate']=c._wire(reenter.authority)
                result['Action_requirement_predicates']=c._wire(reenter.requirements)
                result['CANONICAL_RESULT']='Native SuppliedResult PASS with exactly E2-K-REENTER; actual named Action completed'
                result['KNOWLEDGE_OUTPUTS']=[new_knowledge['E2-K-REENTER']]
            if number == 13:
                result['AUTHORITIES']=[{'role':'TYPED_PROOF_SEMANTIC_AUTHORITY',
                    'proof_id':c._wire(p.id),'authority_EntityId':c._wire(p.authority),
                    'authority_ArtifactIdentity':c._wire(p.authority_identity),
                    'entity':c._wire(next(e for e in current.entities if e.id == p.authority))}
                    for p in current.typed_proofs]
                result['AUTHORITIES'] += installation_authorities([8,9,16,18])
                result['CANONICAL_RESULT']='SLOT_PROOF/ROOT_PROOF accepted; slot RESOLVED/root SATISFIED; native FINISH PASS/E2-K-FINISH; terminal success'
                result['KNOWLEDGE_OUTPUTS']=[new_knowledge['E2-K-FINISH']]
                result['PROOFS']=[c._wire(p) for p in current.typed_proofs]
                result['OUTPUTS'].append({'root':c._wire(current.roots),'slot':c._wire(current.slots),
                                         'declared_goals':c._wire(current.goals),'P04_EXIT_PREDICATE':True})
        result['sources']=sources
        result['authoritative_result']=pin(path('E2_P02_RETRY_4_RESULT') if number<=6 else
            (path('P03_PROSPECTIVE_CHECKPOINT_QUALIFICATION_1') if number<=8 else
             path('E2_P04_CANONICAL_EXECUTION_RETRY_1_RESULT')))
        if number==1:
            result['actual_identity']={'native_SnapshotId':snapshots['E2_P02_INITIAL_SNAPSHOT']['id']}
        elif number==2:
            result['actual_identity']={'ActionId':prefix['trace'][0]['selected'],
                'selection_event_identity':'NOT_APPLICABLE; read-only selection',
                'snapshot':snapshots['E2_P02_INITIAL_SNAPSHOT']['id']}
        elif number<=6:
            result['actual_identity']={'event_witnesses':[],
                'status':'ORIGINAL_NATIVE_EVENT_IDENTITIES_NOT_RECOVERED; report/state identities retained separately'}
        elif number<=8:
            result['actual_identity']={'bundle':uid(c._identity(checkpoint_path.read_bytes(),'planner-bundle-v1')),
                'snapshot':uid(c.snapshot_id(old_checkpoint.current)),
                'scope':'AUTHORIZED_PROSPECTIVE_REPLACEMENT; original history UNPROVEN'}
        else:
            result['actual_identity']={'after_snapshot':events[stage_events[number][-1]-1]['after_snapshot'],
                'event_witnesses':[events[i-1]['identity'] for i in stage_events[number]]}
            result['existing_sealed_oracle_comparisons']=t['checks']
        result['currentness_rule']='Occurrence checked at authoritative historical boundary; support must be usable at its required consumer. Historical result is not current execution permission.'
        result['provenance_rule']='Exact pinned owner artifact/native identity and scope; no foreign-lineage/state substitution.'
        inventory.append(result)
    inventory_file=save('A01-A13-inventory.json',inventory)

    configuration=[]
    for rec in current.installed_definitions:
        descriptor,body=install.descriptor(rec.request.definition)
        event=bundle.events[rec.request.sequence-1]
        assert event.result==rec.request
        configuration.append({'event_sequence':event.sequence,'event_id':c._wire(event.identity),
            'parent_event':c._wire(event.parent_event),'pre_state':c._wire(event.parent_snapshot),'post_state':c._wire(event.after_snapshot),
            'operation':rec.request.operation.value,'definition_id':c._wire(rec.request.definition.id),
            'installed_definition_id':c._wire(rec.id),'definition_type':descriptor['definition_type'],
            'content_id':descriptor['content_id'],'source_pin':descriptor['source_pin'],'subject':descriptor['subject'],
            'installation_authority_id':c._wire(rec.request.authority.id),'scope':descriptor['scope'],
            'lineage':descriptor['lineage'],'generation':descriptor['generation'],
            'source_classification':'CANONICAL_CONFIGURATION','historical_occurrence':'BOUND',
            'installation_current_at_terminal':install.current(bundle,rec),
            'source_support_current':install.route_support_current(current,body) if descriptor['definition_type']=='EXTERNAL_RESOLUTION_CONTRACT' else install.current(bundle,rec),
            'current_consumer_applicability':'NO_LONGER_ACQUISITION_STAGE' if descriptor['definition_type']=='EXTERNAL_RESOLUTION_CONTRACT' else 'REQUIRED_ACTIVE_DEFINITION',
            'source':pin(target_path,'/bundle/events/'+str(event.sequence-1))})
    configuration.sort(key=lambda x:x['event_sequence'])
    assert [x['event_sequence'] for x in configuration]==[3,4,5,6,7,8,9,16,18]
    assert all(x['source_support_current'] for x in configuration)
    assert [x['event_sequence'] for x in configuration if not x['installation_current_at_terminal']]==[3]
    configuration_file=save('configuration-history.json',{'records':configuration,'ordering':'Native event sequence/ancestry preserved; not a freely permutable dependency set.',
                   'deferred_A13_count':2,'new_installations':0})

    # All incoming dependencies are explicit evidence edges, not invented native slots.
    edges=[]
    for item in inventory:
        edges.append({'source_node':item['STEP_ID'],'source_output':'Complete stage-specific evidence in A01-A13 inventory',
            'target_node':'E2-END','target_input':'A01-A13 stage oracle / native event-state coverage',
            'dependency_type':'CASE_COVERAGE_EVIDENCE','satisfaction_rule':item['canonical_contract']['EXPECTED_STATE']+'; '+item['canonical_contract']['PERSISTENCE_REQUIREMENT'],
            'currentness_rule':item['currentness_rule'],'provenance_rule':item['provenance_rule'],
            'binding_status':item['binding_status']})
    for number in range(1,13):
        edges.append({'source_node':'E2-A%02d'%number,'target_node':'E2-A%02d'%(number+1),
            'source_output':'Prior canonical stage output/state','target_input':cases['E2-A%02d'%(number+1)]['INITIAL_STATE'],
            'dependency_type':'LIFECYCLE_STATE_INPUT','satisfaction_rule':'Exact actual state/required artifacts; ordinary event ancestry where events occur.',
            'currentness_rule':'At target stage, not a persisted future permission','provenance_rule':'Same native lineage or explicitly authorized case-acceptance replacement only.',
            'binding_status':'AUTHORIZED_REPLACEMENT_ACCEPTANCE_NOT_HISTORICAL_ANCESTRY' if number==6 else ('BOUND' if number>=7 else 'HISTORICAL_TRACE_INCOMPLETE')})
    for idx,dependency in enumerate(interface['dependencies']):
        edges.append({'source_node':dependency,'source_output':'Qualified interface/contract','target_node':'E2-END',
            'target_input':interface['dependencies'][idx],'dependency_type':'DECLARED_PC04_INTERFACE',
            'satisfaction_rule':'Exact declared interface plus current stage binding; interface READY is not END execution PASS.',
            'currentness_rule':'Qualified semantic contract at its own scope; historical instances not portable by name.',
            'provenance_rule':'Canonical plan / immutable PC04 END interface, qualified capability records.',
            'binding_status':'DECLARED_INTERFACE_RETAINED'})
    dag_file=save('dependency-DAG.json',{'kind':'READ_ONLY_ACCEPTANCE_EVIDENCE_DAG','not_native_Planner_graph_mutation':True,
        'declared_interface_input_count':6,'required_stage_input_count':13,'explicit_edges':edges,
        'configuration_native_event_chain':configuration_file,'no_implicit_edges':True,
        'first_unsatisfied_dependency':missing[0]})

    original_grant=next(e for e in archive['entities'] if e['id']['value']=='E2-GRANT')
    identity_checks={
        'native_snapshots_exact':[{'path':v['pin'],'id':v['id'],'canonical_byte_roundtrip':'PASS'} for v in snapshots.values()],
        'actual_target_bundle_id':algebraic_bundle,'actual_target_snapshot_id':uid(c.snapshot_id(current)),
        'P03_current_P04_initial_and_two_event_prefix_exact':True,
        'ActionResult_identity_domain':'Native PASS is an enum, not a standalone result record. Result-witness event IDs exist for P04; no invented IDs for missing P02 events.',
        'Knowledge_identity_domain':'Native KnowledgeId is scoped by record provenance/state; same name does not equate original and prospective records.',
        'Proof_identity_domain':'A11 Proof is computed; A13 TypedProof has explicit native id; these are different representations.',
        'Evidence_domains':'Semantic/content/native EntityId/receipt/result identities recorded from exact actual admission operand; not interchangeable.',
        'original_grant':original_grant['identity'],'original_grant_context_applicable_to_target':original_grant['lineage']==current.context.lineage,
        'historical_knowledge_record_distinction':[{'KnowledgeId':old_knowledge[n]['id'],
             'original_provenance':old_knowledge[n]['provenance'],'target_provenance':new_knowledge[n]['provenance'],
             'same_native_record':old_knowledge[n]==new_knowledge[n],
             'target_occurrence_class':'AUTHORIZED_REPLACEMENT_INITIAL_PREMISE; not original P02 execution'} for n in ('E2-K-CHECK','E2-K-COLLECT','E2-K-PREPARE')],
        'current_native_typed_proof_usability':[{'ProofId':c._wire(p.id),'usable':tp.usable(current,p)} for p in current.typed_proofs],
        'historical_C03_eligible':trace['post-a11']['operands']['C03']['allowed'],
        'terminal_C03_eligible':read(DOCS/'qualification/E2_P05_READINESS_1/target-inspection.json')['checks']['ResumeEligibility_after_completion']['actual'],
        'old_initial_is_actual_P04_initial':snapshots['E2_P02_INITIAL_SNAPSHOT']['id']==uid(c.snapshot_id(bundle.initial)),
        'no_cross_domain_substitution':'PASS'}
    identity_file=save('identity-currentness-provenance.json',identity_checks)

    treatment={'decision':pin(scope_path),'contract':pin(p03_contract_path),
        'selected_option':scope['selected_option'],'authority':p03['qualification_scope_authority_id'],
        'A07_A08_input_sufficient':'YES_FOR_EXACT_AMENDED_PROSPECTIVE_CHECKPOINT_FIDELITY',
        'actual_P04_parent_prefix_matches_prospective_checkpoint':'YES',
        'original_P02_history_sufficient':'NOT_ESTABLISHED',
        'original_historical_correspondence':'UNPROVEN','scope_reopened':False,'new_authority_issued':False,
        'does_not_authorize':['Historical reconstruction','Converting authored completed-prefix premises to original execution events',
                              'Waiving or silently redefining E2-END full lifecycle requirements']}
    treatment_file=save('P03-replacement-treatment.json',treatment)
    bindings_file=save('canonical-bindings.json',{'stage_bindings':inventory,'classification_values':[
         'CANONICAL_EXECUTION','CANONICAL_CONFIGURATION','QUALIFICATION_EVIDENCE','AUTHORIZED_REPLACEMENT_QUALIFICATION','HISTORICAL_UNPROVEN'],
         'actual_target':pin(target_path),'configuration_history':configuration_file,
         'historical_unproven_edge':'Original prefix to prospective checkpoint',
         'qualification_only_oracles':'Comparison/interface roles only; not substituted for missing canonical lifecycle instances.'})
    oracle_path=OUT/'input-oracle.json'
    expected=read(oracle_path)
    checks=[]
    def compare(name,wanted,actual):checks.append({'term':name,'expected':wanted,'actual':actual,'pass':wanted==actual})
    compare('P04_target_bundle_identity',expected['target_bundle_id'],algebraic_bundle)
    compare('P04_target_snapshot_identity',expected['target_snapshot_id'],uid(c.snapshot_id(current)))
    compare('P04_event_sequence_types',expected['target_event_types'],[type(e.result).__name__ for e in bundle.events])
    compare('all13_stage_bindings_complete',True,all(x['binding_status']=='BOUND' for x in inventory))
    compare('A03_actual_native_event_witnesses_present',True,read(OUT/'P02-native-event-artifact-search.json')['native_event_match_count']>0)
    compare('two_exact_deferred_INSTALL_boundaries',[16,18],[x['event_sequence'] for x in configuration if x['event_sequence']>9])
    compare('P03_scope_decision',expected['P03_decision'],scope['selected_option'])
    compare('P03_no_historical_reconstruction',False,p03_contract['historical_reconstruction'])
    compare('P04_parent_state_continuity',True,all(e.parent_snapshot==bundle.events[i-1].after_snapshot for i,e in enumerate(bundle.events) if i))
    compare('P04_parent_event_continuity',True,all(e.parent_event==bundle.events[i-1].identity for i,e in enumerate(bundle.events) if i))
    compare('original_P02_poststate_matches_prospective_initial',True,p02['post_decision_snapshot']==c.snapshot_id(bundle.initial).sha256)
    stage_comparisons=[]
    for wanted,item in zip(expected['required_stage_inputs'],inventory):
        assert wanted['slot']==item['STEP_ID']
        stage_comparisons.append({'slot':wanted['slot'],
            'source':{'expected':wanted['EXPECTED_SOURCE'],'actual':item['authoritative_result'],
                      'pass':wanted['EXPECTED_SOURCE']==item['authoritative_result']['path']},
            'identity':{'expected':wanted['EXPECTED_IDENTITY'],'actual':item['actual_identity'],
                        'pass':wanted['EXPECTED_IDENTITY']==item['actual_identity']},
            'value_result':{'expected':wanted['EXPECTED_VALUE_RESULT'],'actual':item['CANONICAL_RESULT'],
                'status':'BOUND_TO_EXISTING_OWNER_RESULT_AND_NATIVE_INPUTS' if item['binding_status']=='BOUND' else 'INCOMPLETE_OCCURRENCE_EVIDENCE'},
            'provenance':{'expected':wanted['EXPECTED_PROVENANCE'],'actual_classification':item['source_classification'],
                'sources':item['sources'],'status':'BOUND_WITH_EXPLICIT_SCOPE' if item['binding_status']=='BOUND' else 'ORIGINAL_EVENT_PROVENANCE_MISSING'},
            'currentness':{'expected':wanted['EXPECTED_CURRENTNESS'],'actual_rule':item['currentness_rule'],
                'status':'BOUND_AT_REQUIRED_CONSUMER_BOUNDARY' if item['binding_status']=='BOUND' else 'HISTORICAL_OCCURRENCE_UNBOUND'},
            'binding_result':'PASS' if item['binding_status']=='BOUND' and wanted['EXPECTED_IDENTITY']==item['actual_identity'] else 'FAIL',
            'new_lifecycle_qualification_executed':False})
    oracle_file=save('input-oracle-comparison.json',{'RESULT':'FAIL','checks':checks,
            'per_slot_comparisons':stage_comparisons,
            'meaning':'Binding-completeness failure, not runtime counterexample or reversal of package PASS.',
            'first_missing_input':missing[0],'missing_identity_policy':'No fabricated expected event identity; required exact original event witness is unavailable.'})
    negative_path=DOCS/'qualification/E2_P05_READINESS_1/sealed-negative-oracles.json'
    negatives=read(negative_path)
    assert len(negatives['cases'])==16 and all(x['actual_execution']=='NOT_EXECUTED' for x in negatives['cases'])
    stop_file=save('stop-and-readiness.json',{'RESULT':'BLOCKED','E2_END_INPUT_GRAPH':'FAIL',
        'FIRST_MISSING_INPUT':missing[0],'MISSING_INPUTS':missing,
        'AMBIGUOUS_BINDINGS':[],'E2_P05_READY':'YES','P05_EXECUTION_READY':'NO',
        'STOP_AT':'A03 native historical result-event trace; no dependent full END qualification performed',
        'BINDING_ADAPTER':'NO_NATIVE_END_ADAPTER_REQUIRED; computed read-only evidence manifest',
        'DETERMINISM':'NOT_RUN_FOR_INCOMPLETE_END_GRAPH',
        'COLD_RESTORE':'Existing trusted P03/P04/P05-input evidence preserved; no new full END graph cold qualification past gap',
        'REPLAY':'P04 actual event chain bound; original A01-A13 historical replay cannot be bound without missing prefix',
        'P05_NEGATIVES':{'status':'16_SEALED_EXPECTATIONS_PRESERVED; NOT_EXECUTED','source':pin(negative_path)},
        'P05_EXECUTED':'NO','P06_EXECUTED':'NO','E2_END_EXECUTED':'NO','NEW_AUTHORITY_ISSUED':'NO','NEW_CANONICAL_OBJECTS':0,
        'NEXT_PACKAGE':'E2-END A03 ORIGINAL NATIVE EVENT-TRACE ARTIFACT RECOVERY',
        'runtime_counterexample':'NONE_ESTABLISHED; historical artifact/ancestry gap, no live run',
        'scope_limit':'Authentic artifact recovery only; inability to recover cannot be closed by fabricating events or broadening P03 authority.'})
    report={'schema':'E2-P05-END-INPUT-BINDING-1','WORK_PACKAGE':'E2-P05-END-INPUT-BINDING','RESULT':'BLOCKED',
        'E2_END_TYPE':contract['END_TYPE'],'E2_END_INPUT_COUNT':6,'A01_A13_REQUIRED_BINDING_COUNT':13,
        'A01_A13_BOUND_COUNT':sum(x['binding_status']=='BOUND' for x in inventory),
        'END_CONTRACT':contract_file,'A01_A13_INVENTORY':inventory_file,'END_DEPENDENCY_DAG':dag_file,
        'CANONICAL_BINDINGS':bindings_file,'BINDING_CLASSIFICATIONS':{x['STEP_ID']:{'source':x['source_classification'],'binding':x['binding_status']} for x in inventory},
        'P03_REPLACEMENT_QUALIFICATION_TREATMENT':treatment_file,'CONFIGURATION_HISTORY_BINDING':configuration_file,
        'MISSING_INPUTS':missing,'AMBIGUOUS_BINDINGS':[],
        'IDENTITY_CHECKS':identity_file,'CURRENTNESS_CHECKS':identity_file,'PROVENANCE_CHECKS':identity_file,
        'EXPECTED_INPUT_ORACLE':pin(oracle_path),'E2_END_INPUT_ORACLE':oracle_file,
        'E2_END_INPUT_GRAPH':'FAIL','BINDING_ADAPTER':'NONE_REQUIRED_FOR_ACCEPTANCE_EVIDENCE; NO_NATIVE_END_TYPE',
        'DETERMINISM':'NOT_RUN_AFTER_AUTHORITATIVE_GAP','COLD_RESTORE':{'target_inputs':'EXISTING_QUALIFIED_EVIDENCE_RETAINED','complete_END_graph':'NOT_RUN_AFTER_GAP'},
        'REPLAY':{'P04_chain':'BOUND_TO_ACTUAL_EVENTS','complete_A01_A13_history':'BLOCKED_MISSING_ORIGINAL_PREFIX'},
        'P05_NEGATIVES':{'status':'16_EXPECTATIONS_SEALED_UNCHANGED; NOT_EXECUTED','source':pin(negative_path)},
        'P05_INITIAL_ORACLE':'PASS_PREVIOUS37CHECKS_PRESERVED','P05_EXECUTION_READY':'NO','E2_P05_READY':'YES','E2_P04_RESULT':'PASS',
        'FIRST_MISSING_INPUT':missing[0]['input'],'FIRST_MISSING_CLASSIFICATION':'ARTIFACT_MISSING',
        'NEXT_PACKAGE':'E2-END A03 ORIGINAL NATIVE EVENT-TRACE ARTIFACT RECOVERY',
        'P05_EXECUTED':'NO','P06_EXECUTED':'NO','E2_END_EXECUTED':'NO','RUNTIME_MODIFIED':'NO',
        'P03_HISTORICAL_CORRESPONDENCE':'UNPROVEN','N_REAL_SATISFIED':'NO','E1_ARTIFACTS_MODIFIED':0,'PRODUCTION_EFFECT':'NO',
        'new_canonical_objects':0,'new_authorities':0,'evidence':{'binding_gate':stop_file,'source_search':pin(OUT/'P02-native-event-artifact-search.json')},
        'native_inspection':'Decode/type/canonical-byte/identity and pure source/proof support checks only; no apply_event/admission/commit/END runner called.'}
    source_paths={path('E2_P05_READINESS'),path('E2_P04_CANONICAL_EXECUTION_RETRY_1_RESULT'),target_path,
          path('CANONICAL_QUALIFICATION_EXPERIMENT_1'),path('CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1','md'),
          path('E2_PC04_END'),path('E2_P01_RETRY_1_RESULT'),path('E2_P02_RETRY_4_RESULT'),path('E2_P02_RETRY_3_RESULT'),
          path('E2_P02_INITIAL_SNAPSHOT'),path('E2_AUTHORITATIVE_HANDOFF_SNAPSHOT_1'),path('E2_HUMAN_DECISION_ALLOW_POST_SNAPSHOT_1'),
          path('E2_P02_INPUT_VALIDATION'),path('E2_HUMAN_DECISION_ALLOW_RETRY_1_RESULT'),path('E2_HUMAN_DECISION_ALLOW_RETRY_1_TRACE'),
          checkpoint_path,path('P03_PROSPECTIVE_CHECKPOINT_QUALIFICATION_1'),scope_path,p03_contract_path,trace_path,negative_path}
    source_paths.update((ROOT/'adapter/planner').glob('*.py'))
    report['SOURCE_PINS']=save('source-pins.json',{'files':[pin(p) for p in sorted(source_paths)],'raw_file_hashes_not_native_object_identities':True})
    preservation_path=OUT/'preservation.json'
    if preservation_path.exists():
        preservation=read(preservation_path)
        assert preservation['all_preexisting_files_unchanged'] and preservation['GIT_DIFF_CHECK']=='PASS'
        report['PRESERVATION']=pin(preservation_path)
        report['GIT_DIFF_CHECK']='PASS'
    path('E2_P05_END_INPUT_BINDING_1').write_bytes(c.canonical_bytes(report))
    print(json.dumps({'RESULT':'BLOCKED','required_stage_bindings':13,'bound_stage_inputs':report['A01_A13_BOUND_COUNT'],
                      'first_missing':report['FIRST_MISSING_INPUT'],'P05_EXECUTED':'NO','configuration_events_bound':len(configuration)}))


if __name__=='__main__':
    main()
