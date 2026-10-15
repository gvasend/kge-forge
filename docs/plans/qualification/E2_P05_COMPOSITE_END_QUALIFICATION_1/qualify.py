"""Bounded documentary composite END mapping; no Planner transition or P05 run."""
import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import importlib.util
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
SEALED = ROOT / 'docs/plans/qualification/E2_P05_END_ANCESTRY_RECONCILIATION_1'
DOCS = ROOT / 'docs/plans'
PREFIX = 'DETERMINISTIC_PLANNER_V0_1_'
OPTION = 'AUTHORIZE_COMPOSITE_P05_END_QUALIFICATION_MAPPING'
BASE_ID = 'qualification-END-evidence-graph-v1:d3979240252a12139aac34db1bb1cb2396c6860af371084b94118740ec23af15'
SUBJECT_ID = 'qualification-scope-subject-v1:12b2e68bea4d28c8da2cd35e15b9cb704b153288df40360ed0dc33e414402256'
DOSSIER_SHA = '955408c7d0977f7b49fe16206fb6a6373671a172139b0536e67dce0f8cbb64fa'

# Reuse the pinned read-only reconstruction. Its application/append/replay
# barriers are installed before any native object is inspected in this process.
spec = importlib.util.spec_from_file_location('sealed_END_reconstruction', SEALED / 'reconcile.py')
sealed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sealed)
c, m = sealed.c, sealed.m


class Rejection(Exception):
    def __init__(self, term, expected, actual):
        self.record = {'term': term, 'expected': expected, 'actual': actual}
        super().__init__(json.dumps(self.record, sort_keys=True))


def equal(term, actual, expected):
    if actual != expected:
        raise Rejection(term, expected, actual)


def read(path):
    return json.loads(Path(path).read_bytes())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ref(path, pointer=''):
    path = Path(path)
    return {'path': str(path.relative_to(ROOT)), 'pointer': pointer, 'raw_sha256': sha(path)}


def save(path, value):
    raw = (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + '\n').encode()
    if path.exists():
        equal('immutable qualification evidence ' + str(path), path.read_bytes().hex(), raw.hex())
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)


def authenticate():
    dossier_path = SEALED / 'aggregate-END-decision-dossier.json'
    dossier = read(dossier_path)
    verification = read(SEALED / 'verification.json')
    for pin in verification['reports'] + verification['scripts'] + [verification['dossier']]:
        equal('predecision seal ' + pin['path'], sha(ROOT / pin['path']), pin['raw_sha256'])
    equal('dossier raw identity', sha(dossier_path), DOSSIER_SHA)
    equal('subject identity', sealed.qid('qualification-scope-subject-v1', dossier['subject']), SUBJECT_ID)
    equal('subject recorded identity', dossier['subject_identity'], SUBJECT_ID)
    equal('sealed graph identity', dossier['subject']['graph_identity'], BASE_ID)
    sealed.check_pins(dossier['subject'])
    equal('four sealed bridge IDs', len(dossier['subject']['cross_component_edge_ids']), 4)
    option = next(row for row in dossier['options'] if row['option'] == OPTION)
    # The original unselected dossier is preserved. The new human selection is
    # captured separately; it is not a RecordedDecision or native grant.
    equal('old dossier remains unselected', dossier['selected_option'], 'NONE')
    equal('qualification only', dossier['subject']['qualification_only'], True)
    equal('no native permissions granted', dossier['subject']['no_native_authority_or_operation_granted'], True)
    auth = {'schema': 'P05-COMPOSITE-END-SCOPE-AUTHENTICATION-1',
        'SELECTED_OPTION': OPTION, 'SCOPE_AUTHENTICATION': 'PASS',
        'issuer': 'Authenticated human user of this session',
        'authentication': 'Explicit user-role selection through trusted conversation transport; no invented signature',
        'selected_user_statement': 'The human explicitly selected: AUTHORIZE_COMPOSITE_P05_END_QUALIFICATION_MAPPING',
        'qualification_scope_subject': SUBJECT_ID, 'dossier': ref(dossier_path),
        'graph_identity': BASE_ID, 'graph_content': dossier['subject']['graph_content'],
        'bridge_ids': dossier['subject']['cross_component_edge_ids'],
        'exact_authorized_option': option, 'pass_claim': dossier['subject']['pass_claim'],
        'excluded_claims': dossier['subject']['excluded_claims'],
        'consumer': dossier['subject']['consumer'], 'qualification_only': True,
        'no_material_sealed_term_changed': True, 'original_dossier_updated': False,
        'native_Action_authority': False, 'event_authority': False, 'INSTALL_authority': False,
        'native_END_authority': False, 'P05_execution_authority': False,
        'native_grant_issued': False, 'new_native_human_choice': False}
    auth['identity'] = sealed.qid('qualification-END-scope-authentication-v1', auth)
    return auth


def load_inputs():
    wrapper = read(SEALED / 'qualified-evidence-graph.json')
    reconstructed = sealed.build()
    equal('independent graph reconstruction identity', reconstructed['graph_id'], BASE_ID)
    equal('graph body matches immutable definition', reconstructed['graph'], wrapper['graph'])
    equal('graph wrapper identity', wrapper['identity'], BASE_ID)
    graph = wrapper['graph']
    current = read(ROOT / graph['existing_stage_bindings_unchanged']['path'])
    equal('all stage rows retained exactly', [n['original_stage_binding_retained_exact'] for n in graph['stage_nodes']], current['stage_bindings'])
    equal('stage coverage', current['P05_BOUND_STAGE_INPUTS'], 13)
    equal('required stages', current['P05_REQUIRED_STAGE_INPUTS'], 13)
    natives = {role: c._unwire(read(ROOT / data['source']['path'])['bundle'])
               for role, data in graph['native_ledger_segments'].items()}
    return graph, natives


def component_checks(graph, natives):
    checks = {}
    for number in (3,4,5,6):
        node = graph['stage_nodes'][number - 1]
        row = node['original_stage_binding_retained_exact']
        result = read(ROOT / node['SOURCE_ARTIFACTS'][0]['path'])
        equal(node['STAGE'] + ' qualified occurrence/ancestry', result['RESULT'], 'PASS')
        equal(node['STAGE'] + ' END mapping', row['mapping_result'], 'PASS')
        equal(node['STAGE'] + ' local N12', row['N12_MAPPING'], 'PASS')
        equal(node['STAGE'] + ' local N13', row['N13_MAPPING'], 'PASS')
        sealed.check_pins(node)
        checks[node['STAGE']] = {'RESULT': 'PASS', 'binding': row,
            'result_source': node['SOURCE_ARTIFACTS'][0], 'native_identity': node['NATIVE_IDENTITY'],
            'source_lineage': node['SOURCE_LINEAGE'], 'N12': 'PASS', 'N13': 'PASS',
            'original_historical_status': 'UNPROVEN', 'scope_not_broadened': True}
    a03 = natives['A03']
    equal('actual A03 result types', [type(e.result).__name__ for e in a03.events], ['SuppliedResult','SuppliedResult'])
    equal('actual A03 bounded action results', [e.result.action.value for e in a03.events], ['E2-CHECK','E2-COLLECT'])
    equal('actual A03 outcomes', [e.result.result.value for e in a03.events], ['PASS','PASS'])
    equal('A03 original occurrence label', read(ROOT / graph['stage_nodes'][2]['SOURCE_ARTIFACTS'][0]['path'])['ORIGINAL_A03_HISTORICAL_OCCURRENCE'], 'UNPROVEN')
    a04, row04 = natives['A04'], graph['stage_nodes'][3]['original_stage_binding_retained_exact']
    equal('A04 is native extension of A03', a04.events[:2] == a03.events, True)
    equal('A04 result action', a04.events[-1].result.action.value, 'E2-PREPARE')
    equal('A04 result outcome', a04.events[-1].result.result.value, 'PASS')
    equal('A04 actual post-Snapshot', sealed.aid(c.snapshot_id(a04.current)), row04['replacement_post_snapshot'])
    equal('A04 six retained typed validation members', len(a04.current.validation_instances), 6)
    equal('A04 complete durable bundle binding', len(a04.dossier_materializations), 1)
    equal('A04 durable event binding', a04.dossier_materializations[0].event_identity, a04.events[-1].identity)
    equal('A04 original archive bytes', (ROOT / row04['native_original_post_snapshot']['path']).read_bytes().hex(), c.snapshot_bytes(a04.current).hex())
    checks['E2-A04']['typed_validation_binding'] = {'RESULT': 'PASS', 'members': 6,
        'post_Snapshot': row04['native_original_post_snapshot'], 'transaction_binding': row04['native_transaction_binding'],
        'immutable_selector': row04['immutable_member_selector'], 'event': sealed.aid(a04.events[-1].identity)}
    p03, p04 = natives['P03'], natives['P04']
    row05 = graph['stage_nodes'][4]['original_stage_binding_retained_exact']
    equal('A05 alternate original role', row05['alternate_event_original_role'], 'P03')
    equal('A05 alternate classification', row05['classification'], 'AUTHORIZED_ALTERNATE_NATIVE_EVIDENCE')
    equal('A05 exact retained decision', sealed.aid(p03.events[1].identity), row05['alternate_event_id'])
    equal('A05 native decision payload type', type(p03.events[1].result).__name__, 'RecordedDecision')
    equal('P03 native prefix remains in P04', p04.events[:2] == p03.events, True)
    for key in ('P03_event_is_original_A05_event','new_human_choice_created','new_native_grant_issued','new_execution'):
        equal('A05 exclusion ' + key, row05[key], False)
    equal('A05 pre-existing native authority entities unchanged', p03.initial.entities == p03.current.entities, True)
    mapping05 = read(ROOT / row05['sealed_mapping']['path'])
    equal('A05 existing choice identity', mapping05['RecordedDecision_binding']['choice_evidence_identity'], row05['existing_choice_identity'])
    equal('A05 no grant issuance proof', mapping05['RecordedDecision_binding']['grant_issuance_occurrence_proven'], False)
    checks['E2-A05']['limitations'] = row05['limitations']
    checks['E2-A05']['choice_identity'] = row05['existing_choice_identity']
    checks['E2-A05']['P03_EVENT_IS_ORIGINAL_A05_EVENT'] = 'NO'
    checks['E2-A05']['NEW_A05_OCCURRENCE_CREATED'] = 'NO'
    checks['E2-A05']['NEW_HUMAN_CHOICE_CREATED'] = 'NO'
    checks['E2-A05']['NEW_NATIVE_GRANT_ISSUED'] = 'NO'
    a06 = natives['A06']
    equal('A06 actual event type', [type(e.result).__name__ for e in a06.events], ['ExternalEvent','ExternalEvent'])
    equal('A06 phase order', [e.result.stage.value for e in a06.events], ['EVIDENCE_REQUEST_READY','WAITING_FOR_EXTERNAL_EVIDENCE'])
    equal('A06 native second parent', a06.events[1].parent_event, a06.events[0].identity)
    equal('A06 known rule', a06.initial.evidence_requirements[0].rule_known, True)
    equal('A06 no actual receipt', len(a06.current.receipt_admissions), 0)
    equal('A06 no validation/proof effect', len(a06.current.validation_instances) + len(a06.current.typed_proofs), 0)
    equal('no native command/replay called', sealed.CALLS, [])
    return checks


def candidate(graph, auth):
    defs = {e['edge_id']: e for e in graph['edges']}
    return {'schema': 'COMPOSITE-END-ACCEPTANCE-OVERLAY-1',
        'base_graph_identity': BASE_ID, 'scope_authentication_identity': auth['identity'], 'scope_subject': SUBJECT_ID,
        'selected_option': OPTION,
        'stage_bindings': [n['original_stage_binding_retained_exact'] for n in graph['stage_nodes']],
        'bridges': [{'definition': deepcopy(defs[identity]), 'accepted_classification': 'SEMANTIC_ACCEPTANCE_EDGE',
                     'native_handoff_proven': False, 'scope_authority': SUBJECT_ID}
                    for identity in auth['bridge_ids']],
        'component_mappings': {n['STAGE']: n['original_stage_binding_retained_exact'] for n in graph['stage_nodes'][2:6]},
        'historical_labels': deepcopy(graph['historical_labels']), 'pass_claim': auth['pass_claim'],
        'excluded_claims': list(auth['excluded_claims']), 'native_history_changed': False,
        'native_permissions_changed': False, 'continuous_original_lineage_proven': False,
        'continuous_new_mainline_proven': False,
        'A05_preexisting_grant_limitation': graph['stage_nodes'][4]['original_stage_binding_retained_exact']['limitations']['PREEXISTING_GRANT_LIMITATION'],
        'A05_original_role': 'P03', 'P03_EVENT_IS_ORIGINAL_A05_EVENT': False,
        'new_A05_occurrence': False, 'new_human_choice': False, 'new_native_grant': False,
        'native_permission_from_mapping': False,
        'N12_evaluation_mode': 'INDEPENDENT_AGGREGATE_TERMS', 'N13_evaluation_mode': 'INDEPENDENT_AGGREGATE_TERMS'}


def validate_candidate(value, graph, auth):
    # Exact pinned qualification policy. No input is admitted to a Planner API.
    equal('scope authentication reference', value['scope_authentication_identity'], auth['identity'])
    equal('scope subject', value['scope_subject'], SUBJECT_ID)
    equal('selected method', value['selected_option'], OPTION)
    equal('base graph comparison identity', value['base_graph_identity'], BASE_ID)
    equal('13 exact original stage bindings', value['stage_bindings'], [n['original_stage_binding_retained_exact'] for n in graph['stage_nodes']])
    defs = {e['edge_id']: e for e in graph['edges']}
    equal('exactly four bridges', len(value['bridges']), 4)
    equal('exact bridge identities/order', [b['definition']['edge_id'] for b in value['bridges']], auth['bridge_ids'])
    for bridge in value['bridges']:
        equal('exact sealed bridge definition', bridge['definition'], defs[bridge['definition']['edge_id']])
        equal('bridge acceptance classification', bridge['accepted_classification'], 'SEMANTIC_ACCEPTANCE_EDGE')
        equal('bridge cannot prove native handoff', bridge['native_handoff_proven'], False)
        equal('bridge qualification authority', bridge['scope_authority'], SUBJECT_ID)
    equal('exact local replacement mappings', value['component_mappings'],
          {n['STAGE']: n['original_stage_binding_retained_exact'] for n in graph['stage_nodes'][2:6]})
    equal('historical labels not upgraded', value['historical_labels'], graph['historical_labels'])
    equal('exact bounded PASS claim', value['pass_claim'], auth['pass_claim'])
    equal('all sealed excluded claims', value['excluded_claims'], auth['excluded_claims'])
    equal('A05 original role preserved', value['A05_original_role'], 'P03')
    equal('A05 pre-existing grant limitation preserved', value['A05_preexisting_grant_limitation'],
          graph['stage_nodes'][4]['original_stage_binding_retained_exact']['limitations']['PREEXISTING_GRANT_LIMITATION'])
    for flag in ('native_history_changed','native_permissions_changed','continuous_original_lineage_proven',
                 'continuous_new_mainline_proven','P03_EVENT_IS_ORIGINAL_A05_EVENT','new_A05_occurrence',
                 'new_human_choice','new_native_grant','native_permission_from_mapping'):
        equal('forbidden claim/effect ' + flag, value[flag], False)
    for name in ('N12','N13'):
        equal(name + ' may not be inferred from local PASS', value[name + '_evaluation_mode'], 'INDEPENDENT_AGGREGATE_TERMS')
    equal('not a composite native ledger', any(k in value for k in ('native_ledger_identity','native_ledger_root','native_append_head')), False)


def bridge_checks(value, graph, natives, auth):
    nodes = {n['STAGE']: n for n in graph['stage_nodes']}
    answers = []
    for bridge in value['bridges']:
        definition = bridge['definition']
        source, target = definition['source'], definition['target']
        expected = definition['required_assurance']
        sealed.check_pins(definition)
        if (source,target) == ('E2-A02','E2-A03'):
            # Native replacement CHECK/COLLECT outputs exist independently of
            # the old selection record; no cross-Snapshot identity is equated.
            checks = {'original_selection_is_read_only': nodes[source]['NATIVE_IDENTITY']['selection_event_identity'],
                      'actual_selected_acquisition_result': natives['A03'].events[0].result.action.value,
                      'actual_results': [e.result.result.value for e in natives['A03'].events],
                      'outputs': [[k.id.value for k in e.result.knowledge] for e in natives['A03'].events],
                      'source_selected_Action': nodes[source]['NATIVE_IDENTITY']['ActionId']}
            equal('selection corresponds at semantic Action domain', checks['actual_selected_acquisition_result'], checks['source_selected_Action'])
            equal('actual bounded results', checks['actual_results'], ['PASS','PASS'])
        elif (source,target) == ('E2-A04','E2-A05'):
            checks = {'source_PREPARE_event': sealed.aid(natives['A04'].events[-1].identity),
                      'source_actual_dossier': c._wire(natives['A04'].events[-1].result.dossier),
                      'source_validation_count': len(natives['A04'].current.validation_instances),
                      'target_actual_decision': c._wire(natives['P03'].events[1].result),
                      'target_existing_choice': nodes[target]['original_stage_binding_retained_exact']['existing_choice_identity'],
                      'target_qualified_issuer_dossier_context': read(ROOT / nodes[target]['END_MAPPING']['path'])['RecordedDecision_binding'],
                      'cross_dossier_identity_equality_claimed': False}
            equal('source dossier validations available', checks['source_validation_count'], 6)
            equal('target native decision Action', natives['P03'].events[1].result.decision.value, 'E2-DECIDE')
        elif (source,target) == ('E2-A05','E2-A06'):
            initial = natives['A06'].initial
            gate = initial.external_gates[0]
            requirement = initial.evidence_requirements[0]
            checks = {'actual_retained_decision': sealed.aid(natives['P03'].events[1].identity),
                      'target_request': gate.resolution_contracts[0].request, 'target_gate': gate.id.value,
                      'target_start_stage': gate.stage.value, 'known_rule': requirement.rule_known,
                      'held_actions': [a.value for a in gate.held_actions], 'pending': gate.pending,
                      'target_receipts': len(initial.receipt_admissions),
                      'target_context': c._wire(initial.context),
                      'A05_grant_retaged_or_propagated_to_A06': False}
            equal('held named consumer', checks['held_actions'], ['E2-REENTER'])
            equal('known rule/missing Evidence boundary', (checks['known_rule'],checks['target_receipts'],checks['pending']), (True,0,None))
            equal('new A06 legal start', checks['target_start_stage'], 'EXTERNAL_EVIDENCE_REQUIRED')
        elif (source,target) == ('E2-A06','E2-A07'):
            wait = natives['A06'].current.external_gates[0]
            checkpoint = natives['P03'].current.external_gates[0]
            checks = {'source_wait_trace': [e.result.stage.value for e in natives['A06'].events],
                      'source_gate': wait.id.value, 'source_stage': wait.stage.value,
                      'target_gate': checkpoint.id.value, 'target_stage': checkpoint.stage.value,
                      'source_receipts': len(natives['A06'].current.receipt_admissions),
                      'target_receipts': len(natives['P03'].current.receipt_admissions),
                      'target_checkpoint': graph['native_ledger_segments']['P03']['source'],
                      'target_fidelity_qualification': nodes[target]['END_MAPPING'],
                      'target_wait_occurrence_inferred_from_Snapshot': False}
            equal('same qualified wait boundary class', checks['source_stage'], checks['target_stage'])
            equal('same named gate role', checks['source_gate'], checks['target_gate'])
            equal('both boundaries have no receipt', (checks['source_receipts'],checks['target_receipts']), (0,0))
        else:
            raise Rejection('no new fifth bridge', 'Four dossier pairs', [source,target])
        answers.append({'BRIDGE_ID': definition['edge_id'], 'SOURCE': source, 'TARGET': target,
            'SOURCE_LINEAGE': nodes[source]['SOURCE_LINEAGE'], 'TARGET_LINEAGE': nodes[target]['SOURCE_LINEAGE'],
            'TARGET_REQUIREMENT': expected, 'ASSURANCE_PRESERVED': checks,
            'HISTORICAL_EXCLUSION': 'No native same-state/parent/output-production connection between these component histories is proven',
            'SCOPE_AUTHORITY': auth['identity'], 'scope_subject': SUBJECT_ID, 'RESULT': 'PASS',
            'classification': 'SEMANTIC_ACCEPTANCE_EDGE', 'native_handoff_proven': False,
            'sealed_definition': definition})
    equal('bridge count', len(answers), 4)
    return answers


def edge_checks(graph, value):
    bridges = {b['definition']['edge_id'] for b in value['bridges']}
    answers = []
    for edge in graph['edges']:
        sealed.check_pins(edge['evidence'])
        definition = {k:v for k,v in edge.items() if k!='edge_id'}
        equal('sealed edge identity recipe', sealed.qid('qualification-END-edge-v1', definition), edge['edge_id'])
        classification = 'SEMANTIC_ACCEPTANCE_EDGE' if edge['edge_id'] in bridges else edge['classification']
        if edge['classification'] == 'UNPROVEN':
            equal('all unproven native links only mapped as exact authorized bridges', edge['edge_id'] in bridges, True)
            equal('no native bridge ancestry', edge['native_parent_asserted'], False)
        answers.append({'edge_id': edge['edge_id'], 'source': edge['source'], 'target': edge['target'],
            'sealed_classification': edge['classification'], 'accepted_classification': classification,
            'native_parent_asserted': edge['native_parent_asserted'], 'RESULT': 'PASS',
            'qualification_only_bridge': edge['edge_id'] in bridges, 'scope_subject': SUBJECT_ID if edge['edge_id'] in bridges else None})
    equal('all 70 exact edge definitions', len(answers), 70)
    return answers


def aggregate_checks(graph, value, components, bridges, edges):
    contract = read(SEALED / 'aggregate-N12-N13-contract.json')
    answers = {}
    for name in ('N12','N13'):
        rows = []
        for term in contract[name]['terms']:
            key = term['term']
            if key == 'READ_ONLY_NOT_EXECUTED':
                equal('A02 no native selection event', graph['stage_nodes'][1]['NATIVE_IDENTITY']['selection_event_identity'], 'NOT_APPLICABLE; read-only selection')
                evidence = [graph['stage_nodes'][i]['SOURCE_ARTIFACTS'] for i in (0,1)]
            elif key == 'ACTUAL_EFFECT_EVENT_REQUIRED':
                equal('actual scoped component results individually checked', [components['E2-A%02d'%i]['RESULT'] for i in (3,4,5,6)], ['PASS']*4)
                equal('all canonical tail events', len(graph['native_ledger_segments']['P04']['events']), 20)
                evidence = components
            elif key == 'NO_COMPOSITE_EVENT_FABRICATION':
                equal('all accepted bridges remain semantic', [b['native_handoff_proven'] for b in bridges], [False]*4)
                equal('no native replay/application/commit', sealed.CALLS, [])
                evidence = {'base_graph': BASE_ID, 'bridge_ids': [b['BRIDGE_ID'] for b in bridges], 'native_calls': []}
            elif key == 'NO_PREMISE_TO_OCCURRENCE_PROMOTION':
                equal('original labels stay UNPROVEN', set(value['historical_labels'].values()), {'UNPROVEN'})
                equal('pre-existing-grant exclusion', value['new_native_grant'], False)
                evidence = {'initial_completed_premises': graph['native_ledger_segments']['P03']['initial_completed_actions'],
                            'A05_limitation': value['A05_preexisting_grant_limitation']}
            elif key == 'WITHIN_SEGMENT_ORDER_EXACT':
                equal('native parents cannot migrate onto bridged edges', any(e['native_parent_asserted'] for e in edges if e['qualification_only_bridge']), False)
                evidence = graph['native_ledger_segments']
            elif key == 'AGGREGATE_SCOPE_GUARD':
                equal('explicit selected aggregate scope', value['selected_option'], OPTION)
                equal('exact scope subject', value['scope_subject'], SUBJECT_ID)
                evidence = {'selected_option': OPTION, 'scope_subject': SUBJECT_ID}
            elif key == 'DEFINITION_RESULT_SEPARATION':
                equal('N13 not local flag inference', value['N13_evaluation_mode'], 'INDEPENDENT_AGGREGATE_TERMS')
                evidence = {'definition_cases': ['E2-A01','E2-A02'], 'actual_event_sources': graph['native_ledger_segments']}
            elif key == 'EXACT_OUTPUT_PROVENANCE':
                equal('all 13 immutable original bindings', value['stage_bindings'], [n['original_stage_binding_retained_exact'] for n in graph['stage_nodes']])
                evidence = {'native_scoped_outputs': [n['NATIVE_IDENTITY'] for n in graph['stage_nodes']], 'shared_name_is_identity_equivalence': False}
            elif key == 'NO_FOREIGN_LINEAGE_NATIVE_SUBSTITUTION':
                equal('semantic mapping cannot grant permission', value['native_permission_from_mapping'], False)
                equal('no native history mutation', value['native_history_changed'], False)
                evidence = {'separate_native_contexts': [l['context'] for l in graph['native_ledger_segments'].values()], 'mapped_edges': bridges}
            elif key == 'INDEPENDENT_PROOF_AND_AUTHORITY':
                equal('A05 no grant issuance inference', components['E2-A05']['NEW_NATIVE_GRANT_ISSUED'], 'NO')
                equal('P04 canonical unfragmented tail', graph['P04_canonical_tail']['never_fragmented_or_substituted'], True)
                evidence = {'P04': graph['P04_canonical_tail'], 'A05': components['E2-A05'], 'A06': components['E2-A06']}
            elif key == 'HISTORICAL_LABELS_PRESERVED':
                equal('all five original historical terms preserved', value['historical_labels'], graph['historical_labels'])
                equal('continuous original proof excluded', value['continuous_original_lineage_proven'], False)
                evidence = value['historical_labels']
            elif key == 'NO_GLOBAL_NEGATIVE_PASS_BY_LOCAL_MAPPING':
                equal('N13 evaluated independently', value['N13_evaluation_mode'], 'INDEPENDENT_AGGREGATE_TERMS')
                evidence = {'P05_N12_executed': False, 'P05_N13_executed': False, 'local_mapping_is_global_case_PASS': False}
            else:
                raise Rejection('no new aggregate assurance interpretation', 'Sealed N12/N13 term', key)
            rows.append(dict(term, RESULT='PASS', actual_evidence=evidence))
        equal(name + ' all six original aggregate terms evaluated', len(rows), 6)
        answers[name] = {'RESULT': 'PASS', 'canonical_case': contract[name]['canonical_case'], 'terms': rows,
                         'global_P05_case_executed': False, 'full_continuous_mainline_proven': False}
    return answers


NEGATIVE_NAMES = ['missing_bridge','extra_bridge','changed_bridge_source','changed_bridge_target',
    'wrong_A03_replacement','wrong_A04_replacement','wrong_A05_P03_event','wrong_A06_replacement',
    'historical_label_upgraded','A05_relabeled_original','preexisting_grant_limitation_removed',
    'native_ancestry_across_semantic_bridge','continuous_mainline_claim',
    'aggregate_N12_assumed_local','aggregate_N13_assumed_local','permission_inferred_from_mapping']


def seal():
    auth = authenticate()
    graph, natives = load_inputs()
    save(OUT / 'scope-authentication.json', auth)
    save(OUT / 'entry-gate.json', {'RESULT':'PASS','scope_authentication':auth['identity'],
        'base_graph': BASE_ID, 'stage_count':13,'semantic_bridge_count':4,'native_lifecycle_calls':sealed.CALLS})
    save(OUT / 'negative-plan.json', {'schema':'COMPOSITE-END-NEGATIVE-PLAN-1','sealed_before_qualification':True,
        'origin':'Sixteen explicitly required user controls evaluated against immutable dossier definitions, exclusions and N12/N13 terms; dossier has no separately enumerated negative-case file',
        'sealed_dossier':ref(SEALED / 'aggregate-END-decision-dossier.json'),
        'cases':[{'id':'END-CN-%02d'%(i+1),'name':name,'expected':'REJECT_BEFORE_COMPOSITE_ACCEPTANCE',
                  'mutation_scope':'Isolated documentary candidate only; no native source or existing binding mutation'} for i,name in enumerate(NEGATIVE_NAMES)],
        'new_acceptance_criteria':False,'P05_global_negatives_executed':False})
    print(json.dumps({'SCOPE_AUTHENTICATION':'PASS','graph':BASE_ID,'four_bridges':auth['bridge_ids'],'negative_controls_sealed':16}))


def qualify(write=True):
    auth = authenticate()
    equal('new scope capture matches current human authentication', read(OUT / 'scope-authentication.json'), auth)
    graph, natives = load_inputs()
    components = component_checks(graph,natives)
    value = candidate(graph,auth)
    validate_candidate(value,graph,auth)
    bridges = bridge_checks(value,graph,natives,auth)
    edges = edge_checks(graph,value)
    aggregates = aggregate_checks(graph,value,components,bridges,edges)
    result = {'schema':'QUALIFIED-COMPOSITE-END-MAPPING-1','base_graph_identity':BASE_ID,
        'base_graph_definition':ref(SEALED / 'qualified-evidence-graph.json'),
        'scope_authentication':ref(OUT / 'scope-authentication.json'), 'overlay':value,
        'component_checks':components,'bridge_checks':bridges,'edge_checks':edges,
        'aggregate_N12':aggregates['N12'],'aggregate_N13':aggregates['N13'],
        'all_original_stage_bindings_and_native_histories_unchanged':True,
        'qualified_mapping_only_not_P05_execution':True}
    result['qualification_identity'] = sealed.qid('qualification-composite-END-acceptance-v1', result)
    if write:
        save(OUT / 'qualified-composite-mapping.json',result)
        save(OUT / 'bridge-results.json',{'RESULT':'PASS','count':4,'bridges':bridges})
        save(OUT / 'component-results.json',{'RESULT':'PASS','components':components,'A04_is_not_a_fifth_semantic_bridge':True})
        save(OUT / 'edge-results.json',{'RESULT':'PASS','edges':edges,'accepted_counts':dict(Counter(e['accepted_classification'] for e in edges))})
        save(OUT / 'aggregate-N12-N13-results.json',aggregates)
    return result,graph,auth


def negatives():
    result,graph,auth = qualify(False)
    expected = read(OUT / 'negative-plan.json')['cases']
    answers = []
    for case in expected:
        value = deepcopy(result['overlay'])
        name = case['name']
        if name=='missing_bridge': value['bridges'].pop()
        elif name=='extra_bridge': value['bridges'].append(deepcopy(value['bridges'][0]))
        elif name=='changed_bridge_source': value['bridges'][0]['definition']['source']='E2-A01'
        elif name=='changed_bridge_target': value['bridges'][0]['definition']['target']='E2-A04'
        elif name.startswith('wrong_A'):
            stage={'wrong_A03_replacement':'E2-A03','wrong_A04_replacement':'E2-A04','wrong_A05_P03_event':'E2-A05','wrong_A06_replacement':'E2-A06'}[name]
            # Use retained, well-formed native event identities from a different
            # required result/phase, rather than an arbitrary invalid PASS flag.
            if stage=='E2-A03':
                value['component_mappings'][stage]['replacement_native_event_ids'][0]=graph['native_ledger_segments']['P04']['events'][14]['identity']
            elif stage=='E2-A04':
                value['component_mappings'][stage]['replacement_event_id']=graph['native_ledger_segments']['A03']['events'][1]['identity']
            elif stage=='E2-A05':
                value['component_mappings'][stage]['alternate_event_id']=graph['native_ledger_segments']['P04']['events'][19]['identity']
            else:
                value['component_mappings'][stage]['native_event_ids'][0]=graph['native_ledger_segments']['P04']['events'][12]['identity']
        elif name=='historical_label_upgraded': value['historical_labels']['ORIGINAL_A03_HISTORICAL_OCCURRENCE']='PROVEN'
        elif name=='A05_relabeled_original': value['P03_EVENT_IS_ORIGINAL_A05_EVENT']=True
        elif name=='preexisting_grant_limitation_removed': value['A05_preexisting_grant_limitation']='Grant issued by decision'
        elif name=='native_ancestry_across_semantic_bridge': value['bridges'][0]['native_handoff_proven']=True
        elif name=='continuous_mainline_claim': value['continuous_new_mainline_proven']=True
        elif name=='aggregate_N12_assumed_local': value['N12_evaluation_mode']='LOCAL_PASS_FLAGS_ONLY'
        elif name=='aggregate_N13_assumed_local': value['N13_evaluation_mode']='LOCAL_PASS_FLAGS_ONLY'
        elif name=='permission_inferred_from_mapping': value['native_permission_from_mapping']=True
        else: raise AssertionError('Unsealed negative')
        try:
            validate_candidate(value,graph,auth)
        except Rejection as error:
            answers.append(dict(case,RESULT='PASS',actual_rejection=error.record,native_mutation=False))
        else:
            raise Rejection('aggregate negative accepted',case['name'],'ACCEPTED')
    save(OUT / 'negative-results.json',{'RESULT':'PASS','count':16,'cases':answers,
        'qualification_identity_unchanged':read(OUT/'qualified-composite-mapping.json')['qualification_identity'],
        'successful_graph_and_native_sources_unchanged':True})
    print(json.dumps({'NEGATIVE_SUITE':'PASS','cases':16}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['seal','qualify','negatives','reader']);p.add_argument('--index',type=int,default=0)
    args=p.parse_args()
    try:
        if args.mode=='seal':seal()
        elif args.mode=='negatives':negatives()
        else:
            result,graph,auth=qualify(args.mode=='qualify')
            if args.mode=='reader':
                equal('fresh reconstruction exact semantic/qualification identity', result,read(OUT/'qualified-composite-mapping.json'))
                save(OUT/'readers'/('seed-%s-reader-%s.json'%(os.environ['PYTHONHASHSEED'],args.index)),
                    {'RESULT':'PASS','pid':os.getpid(),'seed':os.environ['PYTHONHASHSEED'],'reader':args.index,
                     'base_graph_identity':BASE_ID,'qualification_identity':result['qualification_identity'],
                     'stage_count':13,'bridge_count':4,'edge_count':70,'native_lifecycle_calls':sealed.CALLS,
                     'writer_memory_available':False,'no_runtime_replay':True})
            print(json.dumps({'RESULT':'PASS_MAPPING_STRUCTURE','mode':args.mode,'base_graph':BASE_ID,
                              'qualification_identity':result['qualification_identity'],'native_calls':sealed.CALLS}))
    except Exception as error:
        save(OUT/('STOP-'+args.mode+'.json'),{'FIRST_COUNTEREXAMPLE':error.record if isinstance(error,Rejection) else str(error),
            'classification':'SEALED_MAPPING_OR_HARNESS_DIVERGENCE','P05_EXECUTED':'NO','native_lifecycle_calls':sealed.CALLS})
        raise
