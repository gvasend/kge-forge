"""Author an empty prospective fixture and comparison-only A06 trace oracles.

Never apply, append, commit, restore or replay a lifecycle event. Expected
Snapshots/events/bundles are algebraic comparison data, excluded from inputs.
"""
import ast
import hashlib
import json
import re
from dataclasses import replace
from pathlib import Path

from adapter.planner import codec as c, core, gates, model as m
from adapter.planner.selector import POLICY_PIN, validate_policy

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
PLANS = ROOT / 'docs/plans'
PREFIX = 'DETERMINISTIC_PLANNER_V0_1_'
NAME = 'E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1'
SELECTED = 'AUTHORIZE_PROSPECTIVE_P05_A06_REQUEST_WAIT_QUALIFICATION'
SCOPE = 'E2-QUALIFICATION-ONLY'
LINEAGE = 'E2-P05-A06-PROSPECTIVE-QUALIFICATION-1'
GENERATION = 'E2-P05-A06-PROSPECTIVE-GENERATION-1'
LABELS = {
    'QUALIFICATION_TYPE': 'PROSPECTIVE_REPLACEMENT',
    'ORIGINAL_A06_HISTORICAL_REQUEST_WAIT_TRACE': 'UNPROVEN',
    'HISTORICAL_RECONSTRUCTION': 'NO',
    'PROSPECTIVE_A06_TRACE_IS_ORIGINAL_TRACE': 'NO'}
BARRED = []


def canonical(value):
    return c.canonical_bytes(value)


def aid(value):
    return None if value is None else value.namespace + ':' + value.sha256


def pin(path, pointer=''):
    path = ROOT / path if isinstance(path, str) else path
    return {'path': str(path.relative_to(ROOT)), 'pointer': pointer,
            'raw_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def save(name, value, *, native=False):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = canonical(value) if native else (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()
    if path.exists() and path.read_bytes() != raw:
        raise ValueError('sealed output differs: ' + str(path.relative_to(ROOT)))
    path.write_bytes(raw)
    return pin(path)


def function_source(path, symbol):
    tree = ast.parse((ROOT / path).read_text())
    node = next(n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == symbol)
    return dict(pin(path), symbol=symbol, line=node.lineno, end_line=node.end_lineno)


def bar_paths():
    def deny(name):
        def blocked(*args, **kwargs):
            BARRED.append(name)
            raise AssertionError('Contract-only package forbids ' + name)
        return blocked
    for module, names in (
        (core, ('apply_receipt', 'apply_event', 'apply_result', 'recompute', 'resume_eligibility',
                '_inventory', 'apply_recorded_decision', 'apply_decision_reentry', 'admit_dossier_materialization')),
        (c, ('apply_event', '_replay', '_prefix_bundle', 'record_result', 'append_event',
             'commit_event', 'commit_result', 'save_bundle', 'restore', 'decode_bundle',
             'bundle_id', 'bundle_bytes', '_publish_head', '_read_head', 'admit_external_evidence'))):
        for name in names:
            setattr(module, name, deny(module.__name__ + '.' + name))


def authored_source(variant, filename, body, lineage, generation):
    value = dict(body, **LABELS, scope=SCOPE, lineage=lineage, generation=generation,
                 qualification_only=True, production_effect=False, selected_scope_option=SELECTED)
    source = save('inputs/' + variant + '/sources/' + filename, value, native=True)
    raw = (ROOT / source['path']).read_bytes()
    identity = c._identity(raw, 'raw-file-sha256')
    provenance = m.Provenance(source['path'], identity, '/', raw.decode(),
                              'PROSPECTIVE_A06_AUTHORED_DEFINITION', SCOPE)
    return provenance, m.ArtifactPin(source['path'], identity), source


def fixture(variant, lineage, generation, request_template, governing):
    # Fresh boundary-only native model: no copied state, completed Action,
    # human choice, grant or old event prefix. The Action is only a typed held
    # consumer symbol; it does not replace/qualify canonical A12's definition.
    gate_id, requirement_id = m.GateId('E2-GATE'), m.EvidenceId('E2-EXTERNAL-REQUIREMENT')
    action_id = m.ActionId('E2-REENTER')
    root_id = m.ConditionId('E2-ROOT')
    proof_id = m.PredicateId('E2-EXTERNAL-PROOF')
    authority_id = m.PredicateId('E2-USE-AUTHORITY')
    proposition = request_template['proposition']
    target = c._unwire(request_template['target'])
    producers = tuple(c._unwire(item) for item in request_template['producers'])
    gate_source, gate_pin, gate_ref = authored_source(variant, 'gate-requirement.json', {
        'schema': 'E2-P05-A06-GATE-REQUIREMENT-SOURCE-1',
        'governing_canonical_case': governing,
        'gate': 'E2-GATE', 'requirement': 'E2-EXTERNAL-REQUIREMENT',
        'proposition': proposition, 'target': c._wire(target), 'producers': c._wire(producers),
        'validation_rule_known': True, 'actual_evidence_available': False,
        'contract_complete': True, 'gate_validation': 'ACCEPTED',
        'receipt_action': 'TEST-RECEIVE', 'reentry': ['E2-REENTER'], 'held_actions': ['E2-REENTER'],
        'boundary': 'EXTERNAL_EVIDENCE', 'goal': 'E2-ROOT',
        'initial_stage': 'EXTERNAL_EVIDENCE_REQUIRED', 'initial_history': [],
        'no_producer_availability_or_authentication_assertion': True}, lineage, generation)
    action_source, action_pin, action_ref = authored_source(variant, 'held-action.json', {
        'schema': 'E2-P05-A06-HELD-CONSUMER-SCAFFOLD-1', 'id': 'E2-REENTER',
        'operation': 'DETERMINISTIC_MAPPING', 'effect': 'NON_EFFECTING',
        'native_role': 'Unexecuted held/reentry consumer of the exact A06 gate',
        'requirements': ['E2-EXTERNAL-PROOF'], 'authority': 'E2-USE-AUTHORITY',
        'authority_available': False, 'accepted_inventory': [], 'pass_model_complete': False,
        'initial_status': 'ACTION_ELIGIBLE',
        'canonical_Action_definition_replaced': False,
        'does_not_qualify_REENTER_execution_or_its_result': True,
        'A03_A04_A05_prefix_instances_included': False,
        'earlier_Action_prerequisites': 'Outside this isolated A06 event contract; no prior completion or decision is asserted',
        'native_event_requires_only_existing_held_Action_reference': True,
        'canonical_Action_semantics_source': pin(PLANS / (PREFIX + 'E2_PC01_SOURCES.json'), '/declarations/4')}, lineage, generation)
    resolution_source, resolution_pin, resolution_ref = authored_source(variant, 'resolution.json', {
        'schema': 'EXTERNAL-RESOLUTION-CONTRACT-1',
        'contract': {
            'request': request_template['request'], 'gate': c._wire(gate_id),
            'requirement': c._wire(requirement_id), 'proposition': proposition,
            'target': c._wire(target), 'producers': c._wire(producers),
            'source_class': request_template['source_class'],
            'requirement_source': c._wire(gate_pin.identity), 'gate_source': c._wire(gate_pin.identity),
            'receipt_action': 'TEST-RECEIVE', 'reentry': c._wire((action_id,)),
            'held_actions': c._wire((action_id,)), 'scope': SCOPE, 'lineage': lineage, 'generation': generation}}, lineage, generation)
    resolution = m.ExternalResolutionContract(
        request_template['request'], gate_id, requirement_id, proposition, target, producers,
        request_template['source_class'], gate_pin.identity, gate_pin.identity, 'TEST-RECEIVE',
        (action_id,), (action_id,), SCOPE, lineage, generation, resolution_source)
    requirement = m.EvidenceRequirement(requirement_id, proposition, target, producers, gate_source, True)
    gate = m.ExternalGate(gate_id, (requirement_id,), 'TEST-RECEIVE', (action_id,), (action_id,),
                          m.ExternalStage.EXTERNAL_EVIDENCE_REQUIRED, gate_source,
                          resolution_contracts=(resolution,))
    action = m.Action(action_id, m.OperationClass.DETERMINISTIC_MAPPING, m.EffectClass.NON_EFFECTING,
                      (), action_source, (), requirements=(proof_id,), authority=authority_id)
    state = m.Snapshot(
        (action,), (m.ActionStatus(action_id, m.ActionState.ACTION_ELIGIBLE),),
        (m.RootCondition(root_id, m.ConditionState.UNRESOLVED),), (), (),
        predicates=(m.Predicate(proof_id, m.PredicateKind.EVIDENCE_OBLIGATION, obligation=requirement_id),
                    m.Predicate(authority_id, m.PredicateKind.AUTHORITY,
                                unavailable='A06 does not issue or consume downstream REENTER operating authority')),
        context=m.EvaluationContext(SCOPE, lineage, generation, 0),
        evidence_requirements=(requirement,), external_gates=(gate,),
        boundaries=(m.ControlBoundary(gate_id, m.BoundaryKind.EXTERNAL_EVIDENCE, (action_id,), gate_source),),
        goals=(m.Goal(root_id, (action_id,), gate_source),))
    sources = (gate_pin, action_pin, resolution_pin)
    bundle = m.PersistenceBundle(state, (), state, sources, POLICY_PIN,
                                 'E1-SELECTION-1-P06', 'PARTIAL_HISTORICAL_REPLAY')
    m.validate_model(state)
    m.validate_types(bundle, m.PersistenceBundle)
    validate_policy(bundle.policy, bundle.policy_version)
    c._check_snapshot_pins(state, sources)
    c._verify_sources(bundle, ROOT)
    assert not state.entities and not state.decisions and not state.knowledge
    assert not bundle.events and all(s.state is not m.ActionState.COMPLETED for s in state.statuses)
    start_ref = save('inputs/' + variant + '/start-bundle.json',
                     {'schema': 'PLANNER-BUNDLE-1', 'bundle': c._wire(bundle)}, native=True)
    start_id = c.snapshot_id(state)
    start_bundle_id = c._identity((ROOT / start_ref['path']).read_bytes(), 'planner-bundle-v1')
    assert (ROOT / start_ref['path']).read_bytes() == c._bundle_bytes_admitted(bundle)

    # Independent algebraic oracle: apply the legal stage/history rewrite
    # declared by the recovered contract, without calling native application.
    ready_gate = replace(gate, stage=m.ExternalStage.EVIDENCE_REQUEST_READY,
                         history=(m.ExternalStage.EXTERNAL_EVIDENCE_REQUIRED, m.ExternalStage.EVIDENCE_REQUEST_READY))
    ready_state = replace(state, external_gates=(ready_gate,))
    wait_gate = replace(gate, stage=m.ExternalStage.WAITING_FOR_EXTERNAL_EVIDENCE,
                        history=(m.ExternalStage.EXTERNAL_EVIDENCE_REQUIRED, m.ExternalStage.EVIDENCE_REQUEST_READY,
                                 m.ExternalStage.WAITING_FOR_EXTERNAL_EVIDENCE))
    wait_state = replace(state, external_gates=(wait_gate,))
    ready_id, wait_id = c.snapshot_id(ready_state), c.snapshot_id(wait_state)
    commands = (m.ExternalEvent(gate_id, m.ExternalStage.EVIDENCE_REQUEST_READY, start_id),
                m.ExternalEvent(gate_id, m.ExternalStage.WAITING_FOR_EXTERNAL_EVIDENCE, ready_id))
    events = []
    for position, (command, before, after) in enumerate(zip(commands, (start_id, ready_id), (ready_id, wait_id)), 1):
        parent = None if position == 1 else events[0].identity
        event_id = c._event_identity(position, before, parent, command, after)
        events.append(m.ExecutionEvent(position, before, parent, command, after, event_id))
    ready_bundle = replace(bundle, events=(events[0],), current=ready_state)
    wait_bundle = replace(bundle, events=tuple(events), current=wait_state)
    expected_ready_bundle_id = c._identity(c._bundle_bytes_admitted(ready_bundle), 'planner-bundle-v1')
    expected_wait_bundle_id = c._identity(c._bundle_bytes_admitted(wait_bundle), 'planner-bundle-v1')
    expected = {}
    for name, snapshot, expected_bundle in (
        ('pre-trace', state, bundle), ('request-ready', ready_state, ready_bundle), ('post-trace', wait_state, wait_bundle)):
        view = {
            'comparison_only': True, 'oracle_authorship': 'Independent canonical stage/history algebra; no runtime operation output used',
            'snapshot_identity': aid(c.snapshot_id(snapshot)),
            'bundle_comparison_identity': aid(c._identity(c._bundle_bytes_admitted(expected_bundle), 'planner-bundle-v1')),
            'CONTROL': 'EXTERNAL_WAIT', 'actionable': [], 'human_ready': [], 'selected': None,
            'persisted_Action_status': {'E2-REENTER': 'ACTION_ELIGIBLE'},
            'computed_Action_status': {'E2-REENTER': 'BLOCKED'},
            'computed_blockers': ['AUTHORITY_REQUIRED', 'EXTERNAL_GATE:E2-GATE', 'PREDICATE:E2-EXTERNAL-PROOF:UNKNOWN'],
            'obligation_Proof': {'state': 'UNKNOWN', 'reasons': ['PROOF_RULE_KNOWN_EVIDENCE_MISSING']},
            'ResumeEligibility': {'allowed': False, 'actions': [], 'required_missing_predicates': ['REENTRY_STAGE_REQUIRED', 'ACCEPTED_REENTRY_EVENT_MISSING']},
            'root': {'E2-ROOT': 'UNRESOLVED'}, 'slots': [], 'receipt': [], 'evidence': [],
            'validation_results': [], 'support': [], 'typed_proofs': [],
            'ActionResults': [], 'completed_Actions': [], 'Knowledge': [], 'human_decisions': [], 'native_authorities': [],
            'source_policy_currentness': 'Exact native pins, supported policy, scoped tick-0 context; no invalidation',
            'scope': SCOPE, 'lineage': lineage, 'generation': generation,
            'gate_stage': snapshot.external_gates[0].stage.value,
            'gate_history': [x.value for x in snapshot.external_gates[0].history],
            'event_count': len(expected_bundle.events),
            'append_head': aid(expected_bundle.events[-1].identity) if expected_bundle.events else None}
        expected[name] = save('oracles/' + variant + '/' + name + '.json', view)
        expected[name + '_snapshot'] = save('oracles/' + variant + '/' + name + '-snapshot.json',
                                           {'schema': 'PLANNER-SNAPSHOT-1', 'snapshot': c._wire(snapshot)}, native=True)
    event_spec = []
    for index, event in enumerate(events):
        event_ref = save('oracles/' + variant + '/event-' + str(index + 1) + '.json', c._wire(event), native=True)
        event_spec.append({
            'EVENT_ID': aid(event.identity), 'EVENT_TYPE': 'ExecutionEvent', 'RESULT_TYPE': 'ExternalEvent',
            'EVENT_PAYLOAD': c._wire(event.result), 'EVENT_PARENT': aid(event.parent_event),
            'PRE_STATE_ID': aid(event.parent_snapshot), 'POST_STATE_ID': aid(event.after_snapshot),
            'LEDGER_POSITION': index, 'SEQUENCE': event.sequence, 'REQUEST_BINDING': resolution_ref,
            'request_binding_native_path': '/snapshot/external_gates/0/resolution_contracts/0/request',
            'GATE_BINDING': 'E2-GATE', 'RESULT_CONTROL_BINDING': expected['request-ready' if index == 0 else 'post-trace'],
            'scope': SCOPE, 'lineage': lineage, 'generation': generation,
            'provenance': c._wire(gate_source), 'proof_or_resume_binding_operand': None,
            'comparison_only': True, 'expected_event_file': event_ref})
    input_ref = save('inputs/' + variant + '/input-manifest.json', {
        **LABELS, 'schema': 'E2-P05-A06-SEALED-INPUTS-1',
        'START_BUNDLE': start_ref, 'sources': [gate_ref, action_ref, resolution_ref],
        'source_pins': c._wire(sources), 'policy': c._wire(POLICY_PIN),
        'policy_version': bundle.policy_version, 'context': c._wire(state.context),
        'request': c._wire(resolution), 'requirement': c._wire(requirement), 'gate': c._wire(gate),
        'actual_command_1': c._wire(commands[0]),
        'actual_command_2_construction': 'Construct ExternalEvent(E2-GATE, WAITING_FOR_EXTERNAL_EVIDENCE, actual post-ready Snapshot ID, artifact=None); actual ID must equal sealed ready ID before construction',
        'native_operating_authority_required': False,
        'authority_reference_is_not_a_grant': 'Expected producer AUTHORITY_IDENTITY and unavailable Action authority predicate confer no native permission',
        'fixture_role': 'Fresh A06-only native boundary subgraph; not a canonical six-Action installation or complete END initial model',
        'prior_prefix_completions_or_choice_asserted': False,
        'no_original_event_parent_or_history_carried_over': True,
        'writer_input_allowlist': [start_ref['path']] + [r['path'] for r in (gate_ref, action_ref, resolution_ref)] + [POLICY_PIN.path],
        'comparison_oracles_are_not_Planner_inputs': True})
    return {
        'variant': variant, 'lineage': lineage, 'generation': generation, 'scope': SCOPE,
        'START_PATH': start_ref, 'INPUTS': input_ref,
        'START_BUNDLE_ID': aid(start_bundle_id), 'START_STATE_ID': aid(start_id),
        'LEDGER_ID': aid(start_bundle_id) + '#/bundle/events',
        'LEDGER_ID_DOMAIN': 'Native content-addressed bundle/events coordinate; no separate native LedgerId',
        'LEDGER_ROOT': None, 'APPEND_HEAD': None, 'PARENT_EVENT_ID': None,
        'null_ledger_terms_mean': 'Exact native empty ledger; sequence 1 has null parent. Not a placeholder or missing identity.',
        'FORM': 'Fresh prospectively authored empty-history ordinary PersistenceBundle; no GENESIS or copied prefix',
        'REQUEST': c._wire(resolution), 'REQUEST_CONTENT_ID': aid(resolution_pin.identity),
        'WAIT_GATE': c._wire(gate), 'GATE_CONTENT_ID': aid(gate_pin.identity),
        'EXPECTED_EVENT_ORACLE': event_spec, 'EXPECTED_STATE_ORACLES': expected,
        'EXPECTED_POST_READY_BUNDLE_ID': aid(expected_ready_bundle_id),
        'EXPECTED_POST_WAIT_BUNDLE_ID': aid(expected_wait_bundle_id),
        'EXPECTED_POST_READY_STATE_ID': aid(ready_id), 'EXPECTED_POST_WAIT_STATE_ID': aid(wait_id),
        'EXPECTED_POST_WAIT_ROOT': aid(events[0].identity), 'EXPECTED_POST_WAIT_HEAD': aid(events[1].identity),
        'static_type_source_policy_admission': 'PASS; no event application, append, save/restore or replay',
        'PROSPECTIVE_LINEAGE_DIFFERS_FROM_ORIGINAL': lineage != 'E2-CANONICAL-BASELINE-1'}


def main():
    bar_paths()
    recovery_path = PLANS / (PREFIX + 'E2_P05_A06_REQUEST_WAIT_TRACE_RECOVERY_1.json')
    recovery = json.loads(recovery_path.read_bytes())
    assert recovery['RESULT'] == 'BLOCKED' and recovery['P05_BOUND_STAGE_INPUTS'] == 12
    assert recovery['TRACE_CLASSIFICATION'] == 'NO_NATIVE_TRACE' and recovery['LOSSLESS_RECOVERY'] == 'NO'
    scope_path = ROOT / recovery['evidence']['scope-decision-dossier.json']['path']
    assert pin(scope_path)['raw_sha256'] == recovery['evidence']['scope-decision-dossier.json']['raw_sha256']
    scope = json.loads(scope_path.read_bytes())
    subject = 'qualification-scope-subject-v1:' + hashlib.sha256(canonical(scope['subject'])).hexdigest()
    assert subject == scope['subject_identity'] == recovery['SCOPE_DECISION_SUBJECT_ID']
    assert subject == 'qualification-scope-subject-v1:037fab02c085551aa3a11e5d3b7e4224d21e1f5373db0528778989cf33851cf1'
    option = next(row for row in scope['options'] if row['option'] == SELECTED)
    assert not option['selected'] and not scope['native_authority_issued']
    for ref in scope['subject']['governing_source_pins']:
        assert pin(ref['path'])['raw_sha256'] == ref['raw_sha256'], ref['path']
    plan_path = PLANS / (PREFIX + 'CANONICAL_QUALIFICATION_EXPERIMENT_1.json')
    by_case = {row['CASE_ID']: row for row in json.loads(plan_path.read_bytes())['cases']}
    assert by_case['E2-A06']['OPERATION'] == 'Native request-ready then waiting events'
    assert by_case['E2-N12']['EXPECTED_STATE'] == 'No native result accepted; ledger/knowledge not fabricated'
    assert by_case['E2-N13']['EXPECTED_STATE'] == 'Reject wrong event/result; knowledge/root/slot unchanged'
    governing = pin(plan_path, '/cases/5')
    graph_path = ROOT / 'docs/plans/qualification/E2_P05_A05_ALTERNATE_NATIVE_EVIDENCE_1/P05-binding-rerun.json'
    graph = json.loads(graph_path.read_bytes())
    assert graph['P05_BOUND_STAGE_INPUTS'] == 12 and graph['stage_bindings'][5]['binding_status'] == 'MISSING_CANONICAL_OUTPUT'
    assert graph['original_full_END_ancestry_waived'] is False
    fixtures = [fixture('primary', LINEAGE, GENERATION, recovery['REQUEST_BINDING']['contract'], governing)]
    for index in (1, 2, 3):
        fixtures.append(fixture('reproduction-' + str(index), LINEAGE + '-REPRODUCTION-' + str(index),
                                GENERATION + '-REPRODUCTION-' + str(index), recovery['REQUEST_BINDING']['contract'], governing))
    primary = fixtures[0]
    fixture_ref = save('sealed-fixtures.json', {'schema': 'E2-P05-A06-SEALED-FIXTURE-SET-1',
        **LABELS, 'primary': primary, 'independent_reproductions': fixtures[1:],
        'oracles_not_execution_inputs': True, 'native_lifecycle_operations': 0})
    function_refs = [function_source(path, name) for path, name in (
        ('adapter/planner/model.py', 'ExternalEvent'), ('adapter/planner/model.py', 'ExecutionEvent'),
        ('adapter/planner/model.py', 'validate_p05'), ('adapter/planner/core.py', 'apply_receipt'),
        ('adapter/planner/core.py', '_global_control'), ('adapter/planner/core.py', 'resume_eligibility'),
        ('adapter/planner/codec.py', 'record_result'), ('adapter/planner/codec.py', 'append_event'),
        ('adapter/planner/codec.py', 'commit_event'), ('adapter/planner/codec.py', '_replay'),
        ('adapter/planner/codec.py', 'restore'), ('adapter/planner/codec.py', '_event_identity'),
        ('adapter/planner/model.py', 'validate_predicate_contracts'))]
    source_names = [
        'E2_P05_A06_REQUEST_WAIT_TRACE_RECOVERY_1.md', 'E2_P05_A06_REQUEST_WAIT_TRACE_RECOVERY_1.json',
        'E2_P05_END_INPUT_BINDING_1.md', 'E2_P05_END_INPUT_BINDING_1.json',
        'E2_P05_READINESS.md', 'E2_P05_READINESS.json',
        'E2_P05_A03_PROSPECTIVE_OCCURRENCE_RESULT_1.json', 'E2_P05_A04_PROSPECTIVE_ANCESTRY_RESULT_1.json',
        'E2_P05_A05_ALTERNATE_NATIVE_EVIDENCE_RESULT_1.json',
        'CANONICAL_QUALIFICATION_EXPERIMENT_1.md', 'CANONICAL_QUALIFICATION_EXPERIMENT_1.json',
        'CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md', 'E2_PC01_SOURCES.json',
        'E2_P04_CANONICAL_TARGET_BUNDLE_1.json', 'E2_T01_RESULT.md', 'DURABLE_ADMISSION_D01_RESULT.json']
    sources = [pin(PLANS / (PREFIX + name)) for name in source_names] + [pin(scope_path), pin(graph_path)] + function_refs
    source_ref = save('authoritative-source-pins.json', {'sources': sources, 'selected_scope_subject': subject})
    authorization = {
        **LABELS, 'schema': 'E2-P05-A06-AUTHENTICATED-SCOPE-CAPTURE-1',
        'SELECTED_OPTION': SELECTED, 'issuer': 'Authenticated human user of this session',
        'authentication': 'Explicit user-role selection on trusted conversation transport; no invented signature or external issuer ID',
        'scope_subject_identity': subject, 'scope_dossier': pin(scope_path),
        'recovery_result': pin(recovery_path), 'all_original_dossier_source_hashes_match': True,
        'selection_is_new_capture_not_modification_of_original_unselected_dossier': True,
        'authorized_option_exact': option, 'qualification_scope_authentication': 'PASS',
        'selected_scope_applicable': 'YES to these new A06-only fixtures and conditional acceptance mapping',
        'sealed_fixture_set': fixture_ref, 'subjects': [{'lineage': f['lineage'], 'generation': f['generation'],
             'start_bundle': f['START_BUNDLE_ID'], 'request_content': f['REQUEST_CONTENT_ID'], 'gate_content': f['GATE_CONTENT_ID']} for f in fixtures],
        'native_operating_authority_required': False, 'ADDITIONAL_AUTHORITY_REQUIRED': 'NO',
        'event_authority_operand': 'NONE in ExternalEvent/apply_receipt',
        'downstream_REENTER_authority': 'Separate and explicitly unavailable; no Action execution in this contract or future A06 trace',
        'GENESIS_authority_required': False, 'GENESIS_reason': 'Fresh ordinary empty ledger, not adoption of an existing historical checkpoint',
        'INSTALL_authority_required': False, 'INSTALL_reason': 'Initial qualification definitions only; no change to any canonical lineage',
        'native_grants_issued_or_reused': 0, 'original_choice_or_grant_retagged': False,
        'exclusions': option['does_not_authorize'] + ['A07/A08/P04 replayed as new occurrences', 'Full original-prefix/END correspondence waiver']}
    authorization_ref = save('authorization-capture.json', authorization)
    trace = {
        'schema': 'E2-P05-A06-PROSPECTIVE-NATIVE-TRACE-ORACLE-1', **LABELS,
        'A06_ID': 'E2-A06', 'A06_TYPE': 'Canonical acceptance case; two native ExternalEvent phase results in ExecutionEvents',
        'canonical_case': by_case['E2-A06'], 'canonical_source': governing,
        'TRACE_SHAPE': 'EXTERNAL_EVIDENCE_REQUIRED -> EVIDENCE_REQUEST_READY -> WAITING_FOR_EXTERNAL_EVIDENCE',
        'native_event_count': 2, 'native_result_types': ['ExternalEvent', 'ExternalEvent'],
        'PRE_TRACE_ORACLE': primary['EXPECTED_STATE_ORACLES']['pre-trace'],
        'REQUEST_READY_ORACLE': primary['EXPECTED_STATE_ORACLES']['request-ready'],
        'EVENT_ORACLE': primary['EXPECTED_EVENT_ORACLE'],
        'POST_TRACE_ORACLE': primary['EXPECTED_STATE_ORACLES']['post-trace'],
        'ORDERING_ORACLE': {
            'indices': [0, 1], 'sequences': [1, 2], 'first_parent_event': None,
            'first_pre_snapshot': primary['START_STATE_ID'],
            'second_parent_event': primary['EXPECTED_EVENT_ORACLE'][0]['EVENT_ID'],
            'second_pre_snapshot': primary['EXPECTED_POST_READY_STATE_ID'],
            'root': primary['EXPECTED_POST_WAIT_ROOT'], 'append_head': primary['EXPECTED_POST_WAIT_HEAD'],
            'ledger_coordinate': primary['EXPECTED_POST_WAIT_BUNDLE_ID'] + '#/bundle/events',
            'root_or_parent_is_not_timestamp_report_order': True,
            'no_extra_event_before_between_or_after': True, 'no_original_prefix_parent_asserted': True},
        'REQUEST_ID': primary['REQUEST']['request'], 'REQUEST_ID_DOMAIN': 'Native string in ExternalResolutionContract; not a standalone EventId/RequestId entity',
        'request_definition_content': primary['REQUEST_CONTENT_ID'],
        'request_occurrence': 'Native acceptance of request readiness; no network transmission, receipt or request-object creation is inferred',
        'wait_occurrence': 'Actual admitted waiting-stage result with request-ready parent in the new prospective ledger',
        'EXTERNAL_WAIT_entry': 'Waiting stage entered for this occurrence at event 2. Global control may already be EXTERNAL_WAIT because the boundary is exposed.',
        'preexisting_control_resolution': {
            'pre_control': 'EXTERNAL_WAIT', 'post_control': 'EXTERNAL_WAIT',
            'pre_wait_stage_accepted': False, 'pre_accepted_request_ready_event': False,
            'no_global_control_change_required_by_canonical_A06': True,
            'preexisting_wait_negative_meaning': 'Reject Snapshot-only/preaccepted WAITING history supplied as this trace. Do not reject the legitimate pretrace EXTERNAL_WAIT computation or invent runnable work to change it.'},
        'result_output_relation': 'ExternalEvent is the actual phase result; expected_snapshot/gate plus immutable after_snapshot bind request and state. No standalone ActionResult/output/knowledge ID exists for A06.',
        'scope_lineage_provenance_binding': 'Native event does not have added context fields; parent/after Snapshot identities bind exact context, gate/requirement/request provenance and source/policy through bundle pins',
        'identity_dependency_order': 'Fresh source bytes -> definitions -> pre-Snapshot -> expected/actual phase result -> after-Snapshot -> event hash -> ordered ledger -> bundle hash',
        'identity_cycle': False, 'expected_objects_are_comparison_only': True,
        'PROSPECTIVE_A06_REQUEST_WAIT_TRACE_PASS_IFF': [
            'Exact sealed start/request/gate/source/policy/context and scope decision verified before execution',
            'Two actual native transitions and exactly two accepted native events match full independently authored event/Snapshot/bundle oracles',
            'Event 1 parent null and sequence 1; event 2 parent event 1 and sequence 2; pre/after/expected Snapshot continuity exact',
            'Same native ledger coordinate with exact indices/root/head and no additional event',
            'Current known-rule/missing-evidence contract, held Action, zero result/receipt/Knowledge/proof/validation/reentry/completion effects match post oracle',
            'Writer termination, independent cold readers, replay and deterministic reproductions pass',
            'Sealed negatives fail closed and A06-only END/N12/N13 mapping passes without historical relabeling']}
    trace_ref = save('trace-and-state-oracles.json', trace)

    # Every mutation is an acceptance test, not a claim that every alternative
    # well-formed native object is forbidden by the generic Planner API.
    negative_rows = [
        ('wrong_request', 'Sealed-input guard', 'Change resolution.request', 'Reject pin/content correspondence before event commit'),
        ('wrong_gate', 'Native apply_receipt and sealed-input guard', 'Foreign gate ID in command', 'Reject unknown/exact-gate mismatch'),
        ('wrong_dependency', 'Sealed-input guard', 'Different requirement/proposition/target or unknown-rule A14', 'Reject known-rule A06 contract mismatch'),
        ('wrong_parent', 'Native ledger admission/restore', 'Foreign or non-null first parent / different second parent', 'Reject ledger parent continuity'),
        ('wrong_pre_state', 'Native apply_receipt', 'Different expected_snapshot', 'Reject external event pre-state mismatch'),
        ('wrong_event_type', 'Typed admission plus occurrence oracle', 'Replace ExternalEvent with SuppliedResult/reevaluation', 'Reject or nonmatching trace; no A06 binding'),
        ('wrong_event_payload', 'Native type/stage admission and oracle', 'Change stage/artifact/payload fields', 'Reject phase/schema/payload mismatch'),
        ('wrong_request_binding', 'Source/contract input and Snapshot oracle', 'Same string but different contract content', 'Reject native source/context correspondence'),
        ('wrong_gate_binding', 'Sealed-input guard', 'Reentry/held Action or gate source changed', 'Reject exact binding mismatch'),
        ('wrong_event_ordering', 'Native apply_receipt/ledger admission', 'Waiting submitted before request-ready or reverse ledger', 'Reject illegal external lifecycle transition/ancestry'),
        ('wrong_ledger', 'Trusted bundle/occurrence oracle', 'Valid events from another fixture ledger', 'Reject exact bundle/lineage/ledger correspondence'),
        ('wrong_ledger_position', 'Native ledger admission', 'Skip/repeat sequence or insert intervening event', 'Reject sequence or exact two-event completeness'),
        ('wrong_authority', 'Scope/context preflight', 'Use P03/INSTALL/USE authority instead of scope decision or claim an event grant', 'Reject qualification authorization mismatch; no new authority'),
        ('wrong_scope', 'Sealed-input guard', 'Different scope with recomputed hashes', 'Reject trusted scope subject and input identity'),
        ('wrong_lineage', 'Sealed-input guard', 'Historical/P03/A03/A04/foreign lineage', 'Reject, never splice history'),
        ('wrong_generation', 'Sealed-input guard', 'Foreign generation or tick', 'Reject exact generation/currentness'),
        ('wrong_provenance', 'Pinned source/Snapshot guard', 'Changed origin/method/content', 'Reject source identity/content correspondence'),
        ('wait_without_request_ready', 'Native apply_receipt', 'WAIT command against start', 'Reject illegal adjacent-stage transition'),
        ('request_without_wait', 'Complete occurrence oracle', 'Persist only legal event 1', 'Intermediate state allowed but full A06 trace FAIL; no binding'),
        ('snapshot_substituted_for_trace', 'Occurrence oracle', 'Matching final Snapshot without two events', 'Reject occurrence/order assurance'),
        ('report_substituted_for_trace', 'Occurrence oracle', 'PASS prose or hashes without native event bodies', 'Reject missing native witness'),
        ('preexisting_wait_instead_of_occurrence', 'Start plus occurrence oracle', 'Start already WAITING or point to retained wait Snapshot', 'Reject sealed start/actual trace mismatch; scalar pre-control alone is allowed'),
        ('later_evidence_transition', 'Exact event allowlist and post oracle', 'RECEIVED/VALIDATED/REENTRY or added Evidence/receipt/result', 'Reject extra phase/side effect; no live repair'),
        ('prospective_labeled_historical', 'Historical/END mapping guard', 'Claim original A06 trace proved/reconstructed', 'Reject mapping despite any valid new events'),
        ('prospective_identity_substituted_original', 'Identity/mapping guard', 'Alias prospective event to missing historical ID/parent', 'Reject historical identity replacement'),
        ('oracle_used_as_operation_input', 'Writer input allowlist', 'Supply expected Snapshot/event/bundle to native admission', 'Reject, only native results from sealed actual transitions qualify'),
        ('broadened_full_END_or_A05_mapping', 'Scope mapping guard', 'Close original prefix/A05/full-END solely from A06 pair', 'Reject scope expansion')]
    negatives = {'schema': 'E2-P05-A06-SEALED-NEGATIVE-ORACLES-1', **LABELS,
        'case_count': len(negative_rows), 'executed': False,
        'cases': [{'id': 'A06-QN-%02d' % (index + 1), 'name': name, 'boundary': boundary,
                   'isolated_mutation': mutation, 'expected': expected,
                   'successful_lineage_unchanged': True, 'actual_execution': 'NOT_EXECUTED'}
                  for index, (name, boundary, mutation, expected) in enumerate(negative_rows)],
        'fail_closed_definition': 'No successful A06 acceptance mapping/binding on any mismatching candidate; native rejection where native contract forbids the mutation, otherwise exact pinned acceptance oracle rejection',
        'no_attacker_rehash_as_trust_anchor': True, 'original_expected_oracles_never_edited': True}
    negatives_ref = save('sealed-negative-oracles.json', negatives)
    durability = {
        'schema': 'E2-P05-A06-PERSISTENCE-REPLAY-CONTRACT-1',
        'direct_D01_dossier_transaction_required': False,
        'native_path': 'codec.commit_event -> record_result/append_event -> core.apply_event/apply_receipt -> immutable Snapshot/event/bundle -> atomic HEAD publication',
        'reason_not_D01': 'A06 is already a registered ExternalEvent with deterministic state application. No PrepareResult, typed dossier ValidationInstances or DossierMaterializationBinding exists in this stage.',
        'native_sources': function_refs, 'transaction_count': 2,
        'atomic_unit': 'Each actual phase result + its post-state, occurrence event and complete PersistenceBundle/head',
        'legal_intermediate': 'A durable request-ready checkpoint with event 1 is valid; it is not a complete accepted A06 trace until waiting/event 2 commits',
        'post_bundle_contents': ['exact sealed initial Snapshot', 'two ordered actual ExecutionEvents', 'exact actual WAITING post-Snapshot',
                                  'all three sealed source pins', 'supported policy pin/version', 'PARTIAL_HISTORICAL_REPLAY'],
        'forbidden_contents': ['Evidence/receipt/validation/support/proof', 'ActionResult/Knowledge/completion', 'human choice/native grant',
                               'installed definitions', 'persisted ResumeEligibility'],
        'first_commit': 'Against exact empty start, event 1 only; actual after-state/event/bundle must equal independently sealed ready oracles',
        'second_commit': 'Against restored/verified post-ready current HEAD; construct command from actual ready Snapshot; event 2 only',
        'partial_failure': 'Before HEAD publication authoritative old bundle remains. After publication reader sees complete new bundle; staged unreachable immutable files are not an accepted occurrence.',
        'exact_retry': 'append_event is identity-idempotent for an already-enrolled identical event. commit_event stale parent/old expected Snapshot rejects; acknowledge a persisted event read-only only after exact native identity/payload checks. No silent rewind/new command.',
        'cold_restore': {'checkpoints': ['SEALED_START', 'POST_REQUEST_READY', 'POST_WAIT'],
            'writer_terminates': True, 'reader_memory_access': False,
            'reader_inputs': 'Trusted bundle identity/path, native immutable event files, sealed source bytes, supported policy and pinned code; expected files are comparison-only',
            'reader_operation': 'codec.restore with trusted expected bundle ID, then core.recompute/obligation_proof/resume_eligibility',
            'comparisons': ['full canonical Snapshot/bundle/event bytes and identities', 'request/gate/context/provenance',
                            'source/policy pins', 'parents/indices/sequence/root/head', 'post control/absence oracles', 'no resumed Action/permission']},
        'historical_replay': {'operation': 'codec.restore/_replay consumes recorded ExternalEvent results from the sealed prospective initial Snapshot',
            'new_occurrence_created': False, 'new_external_send_or_decision': False, 'new_events_appended': 0,
            'repeat_replay': 'Same two event/result identities, state and bundle; never record_result/commit_event while validating history',
            'original_historical_A06_proved': False},
        'determinism': {'hash_seeds': [0, 1, 7, 101], 'primary_independent_writers': 4,
            'cold_readers_per_checkpoint_per_seed': 3, 'primary_cold_reader_processes': 36,
            'independent_new_fixture_reproductions': 3, 'reproduction_seed': 0, 'reproduction_final_cold_readers_each': 3,
            'fresh_inputs_for_reproductions': [f['INPUTS'] for f in fixtures[1:]],
            'same_fixture': 'Exact canonical native identities, full state/Computation/trace; no salt/UUID/timestamp',
            'different_sealed_fixture': 'Own new context/source/history/event IDs must match its own presealed oracle; compare A06 semantic projection, not equality with primary IDs',
            'unordered_permutations': ['original', 'reversed', 'rotated'],
            'permitted_fields': ['object key order', 'Snapshot.predicates', 'PersistenceBundle.sources'],
            'ordered_fields_never_permuted': ['causal ExecutionEvents', 'ExternalGate.history'],
            'singleton_set_fields': 'Invariant under their only permutation; request string and proposition are not sets'},
        'independent_reproduction_semantic_projection': ['typed phase order', 'known-rule/missing-evidence proposition/target/producer',
            'native request string and exact gate/held Action names', 'null-first-parent then exact own event-1 parent',
            'sequence/ledger positions', 'exact source/context applicability within each fixture',
            'EXTERNAL_WAIT with no action/receipt/proof/result/Knowledge/authority effect'],
        'qualification_only_histories_never_spliced_into_P04': True}
    durability_ref = save('persistence-replay-determinism-contract.json', durability)
    mapping = {
        'schema': 'E2-P05-A06-END-N12-N13-MAPPING-CONTRACT-1', **LABELS,
        'selected_scope': authorization_ref, 'binding_classification': 'AUTHORIZED_PROSPECTIVE_REPLACEMENT',
        'END': {'input': 'E2-A06.request_wait_event_trace', 'source': 'Future actual primary fixture native two-event ledger and post-bundle, checked against presealed oracles',
            'expected_native_event_ids': [e['EVENT_ID'] for e in primary['EXPECTED_EVENT_ORACLE']],
            'expected_post_bundle_id': primary['EXPECTED_POST_WAIT_BUNDLE_ID'],
            'accept_only_if': trace['PROSPECTIVE_A06_REQUEST_WAIT_TRACE_PASS_IFF'],
            'no_original_event_id_or_parent_substitution': True, 'original_prefix_or_full_END_gap_waived': False,
            'scope_effect': 'A06 stage occurrence/order witness only, not P05 PASS or full original historical lifecycle'},
        'N12': {'source': pin(plan_path, '/cases/27'), 'canonical_case': by_case['E2-N12'],
            'original_assurance': 'Selection/history alone cannot establish execution/result; no ledger or Knowledge is fabricated',
            'prospective_assurance': 'Require two actual native phase results, admitted events and state/ledger ancestry; reject request declaration, selection, Snapshot or report as actual occurrence',
            'assurance_preserved': True, 'historical_assurance_not_preserved': 'Original event identities/ancestry remain UNPROVEN',
            'required_controls': ['snapshot_substituted_for_trace', 'report_substituted_for_trace', 'request_without_wait', 'oracle_used_as_operation_input'],
            'P05_global_N12_case_pass_claimed': False},
        'N13': {'source': pin(plan_path, '/cases/28'), 'canonical_case': by_case['E2-N13'],
            'original_assurance': 'A prospective output/Action definition is not an actual supplied result; wrong event/result cannot create Knowledge/root/slot effects',
            'prospective_assurance': 'Fresh request/source/Action scaffold and expected events are definitions/comparisons; only actual accepted native phase events satisfy occurrence. Evidence/proof/reentry/Action completion remain absent.',
            'assurance_preserved': True, 'historical_assurance_not_preserved': 'Original occurrence, source applicability and prefix-to-P04 ancestry remain UNPROVEN',
            'required_controls': ['wrong_event_type', 'wrong_request_binding', 'later_evidence_transition', 'prospective_identity_substituted_original'],
            'inferred_from_N12': False, 'P05_global_N13_case_pass_claimed': False},
        'N12_MAPPING_PRESERVED': 'YES', 'N13_MAPPING_PRESERVED': 'YES',
        'actual_mapping_qualification': 'NOT_EXECUTED',
        'P05_graph_effect': {'before': 12, 'after_only_if_future_A06_qualifies': 13, 'required': 13,
            'only_changed_stage': 'E2-A06', 'twelve_existing_bound_rows': 'Byte-equivalent graph values/source pins retained',
            'original_historical_trace': 'UNPROVEN', 'current_bound_graph': pin(graph_path)}}
    mapping_ref = save('END-N12-N13-mapping.json', mapping)
    p05_dir = PLANS / 'qualification/E2_P05_READINESS_1'
    negative_p05 = json.loads((p05_dir / 'sealed-negative-oracles.json').read_bytes())
    assert len(negative_p05['cases']) == 16
    readiness_terms = [
        ('P04_INITIAL_ORACLE', 'All prior 37 trusted P04 entry/target checks rechecked on exact unchanged target', 'PASS_RETAINED; future recheck required'),
        ('STAGE_BINDINGS', 'Exactly 13 required stages each uniquely bound with its governing scope and native identity; A06 actual qualification PASS', '12/13; future conditional 13/13'),
        ('GLOBAL_END_BINDINGS', 'All six END interfaces and all case edges/currentness/provenance/ordered causal histories bound; no silent splicing', 'Full original prefix-to-checkpoint-to-target ancestry or separately governing full END acceptance mapping remains unresolved'),
        ('CONFIGURATION_HISTORY', 'Nine actual P04 INSTALL/REPLACE occurrences at sequences 3,4,5,6,7,8,9,16,18 with exact authority/source/parent/ordering', 'Bound retained; recheck exact history'),
        ('IDENTITY_DOMAINS', 'Semantic Evidence, native entity, content, receipt, result/support, Knowledge, proof and event identities remain distinct; no original/prospective alias', 'Preserved; recheck all global bindings'),
        ('CURRENTNESS', 'Required definitions/sources/support current at declared consumer boundary; historical event occurrence is not present execution permission', 'Retained checks; full graph must be re-evaluated'),
        ('PROVENANCE', 'Exact source/policy/context and authoritative scope decisions on every original/replacement input; no out-of-scope fixture use', 'Separate A03/A04/A05/A06/P03 limits preserved'),
        ('P05_NEGATIVE_READINESS', 'Sixteen unchanged N01-N16 expectations and all isolated seed/mutation/native before-state bindings ready; actual PASS verdicts are later P05 outputs', 'Expectations sealed; remaining N08/N12 and full END operands require preparation'),
        ('PERSISTENCE_PLAN', 'Concrete writer/termination/reader/checkpoint input manifests and trusted IDs for complete END/D01 and all positive/negative boundaries', 'Plan sealed; full END process bindings remain unresolved'),
        ('REPLAY_PLAN', 'Recorded history reconstructs all required states/identities; independent END reproduction under governing scope does not splice histories or issue unapproved authority', 'Plan sealed; full END history/source/parent binding unresolved'),
        ('AUTHORITY_APPLICABILITY', 'Each consumer has only its own applicable authority; no END authority invented, old-lineage grants retagged, or A06 scope broadened', 'No new authority issued; END reproduction subjects not yet completely bound'),
        ('QUALIFIED_CAPABILITIES_CURRENT_DEFINITIONS', 'Every actual operation/definition needed by prepared P05 graph remains qualified/current under exact pinned code/contracts', 'No new capability/definition need established; recheck complete prepared graph'),
        ('NON_STAGE_END_INPUTS', 'PC01/PC02/PC03/T01/D01/post-reentry interfaces, A14-A16 and D01/REG current input states/negative fixtures bound', 'Must evaluate independently of 13/13 stage count'),
        ('NO_UNRESOLVED_PREPARATION', 'No missing source, input, adapter, authority, correspondence or process manifest remains', 'NO while global END mapping/process/negative operands unresolved')]
    readiness = {
        'schema': 'E2-P05-COMPLETE-POST-A06-READINESS-ORACLE-1',
        'governing_readiness': pin(p05_dir / 'readiness-gates.json'),
        'END_contract': pin(PLANS / 'qualification/E2_P05_END_INPUT_BINDING_1/END-contract.json'),
        'current_graph': pin(graph_path), 'independent_initial_oracle': pin(p05_dir / 'initial-oracle.json'),
        'configuration_history': pin(PLANS / 'qualification/E2_P05_END_INPUT_BINDING_1/configuration-history.json'),
        'persistence_plan': pin(p05_dir / 'persistence-plan.json'), 'replay_plan': pin(p05_dir / 'replay-plan.json'),
        'negative_oracles': pin(p05_dir / 'sealed-negative-oracles.json'),
        'sixteen_expected_negative_cases': [{'case': n['CASE_ID'], 'expected': n['EXPECTED_STATE'], 'source': n['source']} for n in negative_p05['cases']],
        'expected_future_stage_effect': '12 -> 13 only if actual A06 trace and separate END/N12/N13 mappings qualify',
        'terms': [{'id': ident, 'predicate': rule, 'current_status': status, 'future_actual': 'REQUIRED_EVALUATION_NOT_RUN'} for ident, rule, status in readiness_terms],
        'P05_EXECUTION_READY_rule': 'YES iff all terms PASS on the actual complete prepared input graph; otherwise NO and record first dependency-ordered missing term',
        '13_of_13_is_sufficient_alone': False, 'original_prefix_gap_waived': False,
        'expected_after_A06_with_only_this_scope': '13/13 stage coverage is possible; P05_EXECUTION_READY remains NO if the separately unresolved global END/preparation terms have not closed',
        'P05_future_case_PASS_logs_are_prerequisite_inputs': False,
        'P05_or_P06_execution_authorized': False,
        'P03_historical_correspondence_or_N_REAL_reopened': False,
        'evaluation_is_read_only_metadata': True}
    readiness_ref = save('post-A06-complete-P05-readiness-oracle.json', readiness)
    execution_contract = {
        'schema': 'E2-P05-A06-LATER-EXECUTION-CONTRACT-1', **LABELS,
        'work_package': 'E2-P05-A06-PROSPECTIVE-REQUEST-WAIT-QUALIFICATION-EXECUTION-1',
        'entry': [authorization_ref, fixture_ref, trace_ref, negatives_ref, durability_ref, mapping_ref, readiness_ref],
        'required_verdicts': {'contract': 'PASS', 'PROSPECTIVE_A06_EXECUTION_READY': 'YES', 'ADDITIONAL_AUTHORITY_REQUIRED': 'NO', 'PROSPECTIVE_A06_EXECUTED': 'NO'},
        'steps': [
            'Verify all contract/code/source/scope hashes, labels, exact sealed start and empty ledger; no substituted fixture',
            'Bootstrap only an unchanged start store; commit actual request-ready command once with ordinary native commit_event',
            'Compare actual result/event/Snapshot/bundle with ready oracle; STOP on first mismatch',
            'Persist ready checkpoint and terminate writer; restore in fresh process; verify exact parent/head and current request/gate',
            'Construct waiting command from actual ready Snapshot; require sealed identity equality; commit once through native path',
            'Compare exact two-event trace, order, parents, state/absence/control/source/policy/context and final bundle',
            'Persist immutable native events and bundle; terminate writer; run cold readers and historical replay without appending',
            'Run four primary hash-seed writers, three distinct presealed reproductions and permitted permutations',
            'Run all isolated sealed A06 negatives; preserve successful lineage and native failure boundaries',
            'Evaluate authorized A06-only END mapping and N12/N13 independently; keep historical labels/IDs distinct',
            'If all qualify, create read-only new binding evidence changing only A06 from missing to AUTHORIZED_PROSPECTIVE_REPLACEMENT',
            'Re-evaluate all thirteen rows and every sealed global P05 readiness term; identify first remaining non-stage blocker'],
        'STOP_ON_DIVERGENCE': ['FIRST_COUNTEREXAMPLE', 'EXPECTED', 'ACTUAL', 'STATE_ID', 'EVENT_ID', 'CLASSIFICATION'],
        'no_live_repair': True, 'no_reselection_of_request_sources_authority_or_expected_values': True,
        'expected_data_is_not_operation_input': True, 'no_P05_P06_A07_A13_execution': True,
        'no_INSTALL_or_grant_or_human_choice': True}
    execution_ref = save('later-execution-contract.json', execution_contract)
    report = {
        'schema': 'E2-P05-A06-PROSPECTIVE-REQUEST-WAIT-CONTRACT-RESULT-1',
        'WORK_PACKAGE': 'E2-P05-A06-PROSPECTIVE-REQUEST-WAIT-CONTRACT', 'RESULT': 'PASS', **LABELS,
        'SELECTED_OPTION': SELECTED, 'SCOPE_AUTHENTICATION': 'PASS',
        'A06_DEFINITION': {'case': by_case['E2-A06'], 'type': trace['A06_TYPE'], 'source': governing},
        'TRACE_SHAPE': trace['TRACE_SHAPE'], 'PROSPECTIVE_START': primary,
        'PROSPECTIVE_INPUTS': primary['INPUTS'],
        'REQUEST': {'REQUEST_ID': primary['REQUEST']['request'], 'REQUEST_TYPE': 'ExternalResolutionContract.request:str',
            'CONTENT_ID': primary['REQUEST_CONTENT_ID'], 'contract': primary['REQUEST'],
            'standalone_native_RequestId_exists': False, 'CURRENTNESS': 'Exact scoped tick-0 request/source/Snapshot binding; no invalidation'},
        'WAIT_GATE': primary['WAIT_GATE'], 'AUTHORITY': authorization,
        'PRE_TRACE_ORACLE': trace['PRE_TRACE_ORACLE'], 'EVENT_ORACLE': trace['EVENT_ORACLE'],
        'ORDERING_ORACLE': trace['ORDERING_ORACLE'], 'POST_TRACE_ORACLE': trace['POST_TRACE_ORACLE'],
        'DURABLE_TRANSACTION': durability['native_path'],
        'PERSISTENCE_CONTRACT': durability_ref, 'COLD_RESTORE_CONTRACT': durability['cold_restore'],
        'REPLAY_CONTRACT': durability['historical_replay'],
        'INDEPENDENT_REPRODUCTION_CONTRACT': {'fixtures': fixtures[1:], 'count': 3, 'semantics': durability['independent_reproduction_semantic_projection']},
        'DETERMINISM_CONTRACT': durability['determinism'], 'NEGATIVE_SUITE': negatives,
        'END_MAPPING': mapping['END'], 'N12_MAPPING': mapping['N12'], 'N13_MAPPING': mapping['N13'],
        'N12_MAPPING_PRESERVED': 'YES', 'N13_MAPPING_PRESERVED': 'YES',
        'POST_A06_EXPECTED_BINDINGS': '13/13 only if later actual A06 qualification PASS',
        'POST_A06_P05_READINESS_ORACLE': readiness,
        'PROSPECTIVE_A06_AUTHORITY_DECISION_REQUIRED': 'NO', 'ADDITIONAL_AUTHORITY_REQUIRED': 'NO',
        'PROSPECTIVE_A06_EXECUTION_READY': 'YES', 'PROSPECTIVE_A06_EXECUTED': 'NO',
        'P05_BOUND_STAGE_INPUTS': 12, 'P05_REQUIRED_STAGE_INPUTS': 13, 'P05_EXECUTION_READY': 'NO', 'E2_P05_READY': 'YES',
        'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO',
        'ORIGINAL_A03_HISTORICAL_OCCURRENCE': 'UNPROVEN', 'ORIGINAL_A04_HISTORICAL_ANCESTRY': 'UNPROVEN',
        'ORIGINAL_A05_HISTORICAL_ANCESTRY': 'UNPROVEN', 'P03_HISTORICAL_CORRESPONDENCE': 'UNPROVEN', 'N_REAL_SATISFIED': 'NO',
        'E2_P04_RESULT': 'PASS', 'RUNTIME_MODIFIED': 'NO', 'E1_ARTIFACTS_MODIFIED': 0, 'PRODUCTION_EFFECT': 'NO',
        'GIT_DIFF_CHECK': 'PASS', 'NATIVE_LIFECYCLE_CALLS': len(BARRED),
        'native_type_source_policy_checks': 'PASS on unexecuted input fixture and algebraic comparison data; no positive-path qualification claimed',
        'pre_trace_control_distinction': trace['preexisting_control_resolution'],
        'comparison_oracles_used_as_Planner_inputs': False, 'full_END_scope_gap_waived': False,
        'NEXT_PACKAGE': execution_contract['work_package'],
        'evidence': {'authorization': authorization_ref, 'sealed_fixture_set': fixture_ref, 'sources': source_ref,
            'trace_oracles': trace_ref, 'negatives': negatives_ref, 'durability': durability_ref,
            'END_N12_N13_mapping': mapping_ref, 'P05_readiness': readiness_ref, 'later_execution': execution_ref},
        'verification': {'path': str((OUT / 'verification.json').relative_to(ROOT))}}
    assert not BARRED
    report_ref = save('../../' + PREFIX + NAME + '.json', report)
    # OUT is qualification/<package>; ../../ reaches docs/plans.
    write_markdown(report, primary, subject, len(negative_rows))
    print(json.dumps({'RESULT': 'PASS', 'scope_authentication': 'PASS', 'start_bundle': primary['START_BUNDLE_ID'],
        'expected_events': 2, 'negatives_sealed': len(negative_rows), 'PROSPECTIVE_A06_EXECUTION_READY': 'YES',
        'A06_executed': False, 'P05_bindings': '12/13', 'P05_execution_ready': 'NO', 'native_lifecycle_calls': BARRED}))


def write_markdown(report, primary, subject, negative_count):
    events = primary['EXPECTED_EVENT_ORACLE']
    md = '''# E2-P05 A06 prospective request/wait qualification contract 1

**RESULT = PASS — CONTRACT ONLY. PROSPECTIVE_A06_EXECUTION_READY = YES.** The explicit human decision is authenticated against the unchanged A06 recovery dossier. A fresh native start, request/gate/source/context, two independent event/state comparison oracles, ordering, persistence/replay, three separate reproduction fixtures, negative controls and A06-only END/N12/N13 mapping are sealed. **A06 remains unexecuted; P05 remains 12/13 and P05_EXECUTION_READY = NO.**

The [machine-readable companion](DETERMINISTIC_PLANNER_V0_1_E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1.json) carries exact native bytes/identities and all contract terms. Expected objects under `oracles/` are comparison data; they are never execution operands or enrolled events.

## Human decision and historical labels

Selected option: **AUTHORIZE_PROSPECTIVE_P05_A06_REQUEST_WAIT_QUALIFICATION**. The issuer is the authenticated human user of this session; authentication is the explicit user-role instruction through the trusted conversation transport. The [capture](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1/authorization-capture.json) binds the unchanged [recovery dossier](qualification/E2_P05_A06_REQUEST_WAIT_TRACE_RECOVERY_1/scope-decision-dossier.json), subject **SUBJECT_ID**, and every original source hash. No signature, native grant or human choice is invented. The old unselected dossier is not rewritten.

```text
QUALIFICATION_TYPE = PROSPECTIVE_REPLACEMENT
ORIGINAL_A06_HISTORICAL_REQUEST_WAIT_TRACE = UNPROVEN
HISTORICAL_RECONSTRUCTION = NO
PROSPECTIVE_A06_TRACE_IS_ORIGINAL_TRACE = NO
```

The scope permits only a new A06 known-rule/missing-evidence experiment and conditional replacement mapping. It does not prove original events/parents/positions, close the full original-prefix/END gap, issue authority, reproduce A05, change P03's scope or execute P05/P06.

## Canonical A06 and assurance

The earliest [canonical A06 matrix case](DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md:75), also `/cases/5` in the canonical plan JSON, owns native **request-ready then waiting events**. Preconditions are held reentry, known validation rule, unavailable Evidence and exact route/producers/context. Its oracle is EXTERNAL_WAIT, no actionable/human-ready selection or receipt, obligation not PROVED and resume false. A07's checkpoint is a later case.

[ExternalEvent](../../adapter/planner/model.py:1158) has only `gate`, `stage`, `expected_snapshot` and optional `artifact`. [apply_receipt](../../adapter/planner/core.py:590) admits adjacent stages on an accepted gate and exact pre-Snapshot; request-ready also requires a complete contract. No request acquisition/sending or Action execution occurs here.

```text
EXTERNAL_EVIDENCE_REQUIRED
  -> EVIDENCE_REQUEST_READY
  -> WAITING_FOR_EXTERNAL_EVIDENCE
```

The witness proves actual native request readiness and entry into the governed waiting stage, with two phase results, exact parent/pre/after Snapshot bindings, native ledger membership/positions, request/gate/source context and post-control/absence state. It does not prove a network transmission. A Snapshot containing a request and EXTERNAL_WAIT proves state, not either occurrence, causation or ordering. No ActionResult/Knowledge/output is produced by this native operation.

## Prospective start and input identities

The [sealed fixture set](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1/sealed-fixtures.json) contains a primary fixture and three independently authored, distinct reproduction lineages. The primary [start bundle](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1/inputs/primary/start-bundle.json) is a fresh empty-history ordinary PersistenceBundle; its initial and current Snapshot are identical. It does not rewind/retag any original, P03, P04 or A03/A04 state. No GENESIS adoption, canonical installation or completed-prefix premise occurs.

| Term | Exact primary value |
|---|---|
| Scope | E2-QUALIFICATION-ONLY |
| Lineage | E2-P05-A06-PROSPECTIVE-QUALIFICATION-1 |
| Generation / tick | E2-P05-A06-PROSPECTIVE-GENERATION-1 / 0 |
| START_BUNDLE_ID | START_BUNDLE |
| START_STATE_ID | START_STATE |
| LEDGER_ID | START_LEDGER |
| LEDGER_ROOT / APPEND_HEAD / PARENT_EVENT_ID | null / null / null — native empty ledger |
| Request / gate / requirement | TEST-REQUEST / E2-GATE / E2-EXTERNAL-REQUIREMENT |
| Request content source | REQUEST_CONTENT |
| Gate/requirement content source | GATE_CONTENT |

`LEDGER_ID` is the native bundle identity plus its events coordinate. Ordinary PersistenceBundle exposes no separate LedgerId. `TEST-REQUEST` is the exact native request string, not a standalone issuance/event identity; its scoped full ExternalResolutionContract is in the [input manifest](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1/inputs/primary/input-manifest.json). That contract pins the exact proposition, target TEST-target/content `a`×64, expected producer TEST-rule-owner/authority-identity `b`×64, source class, receipt TEST-RECEIVE and held/reentry E2-REENTER. Producer identity is a reference, not a new grant or proof of producer availability. Known validation rule does not prove the requested governing-rule proposition.

The minimum native boundary fixture contains only the typed held consumer, root, predicate, requirement, gate, control boundary and route needed by A06. Its E2-REENTER Action is **unexecuted qualification scaffolding**: it supplies the held consumer symbol, unresolved obligation and explicitly unavailable downstream USE-authority predicate. It is not the canonical A12 Action definition, does not qualify REENTER execution/result and is not installed into any canonical lineage. The canonical six-Action definition remains unchanged; earlier completion/decision/Knowledge/grant instances are absent. This A06-only isolation cannot satisfy original prefix ancestry or the six-interface/full-model END requirement.

All four fixture lineages differ from the original historical lineage. All source files and source/policy/context/native identities are sealed now. Future writers may read only their exact start/input definitions and pinned policy; oracle files are comparator inputs and never Planner inputs. No request, source, authority or expected answer may be chosen after execution.

## Authority and pre-trace control

**ADDITIONAL_AUTHORITY_REQUIRED = NO.** Native request-ready/wait commands have no authority field and do not execute an Action. The selected qualification scope applies to these fresh qualification definitions. Existing P03/GENESIS/INSTALL/USE grants are neither reused nor retagged; no GraphEntity authority, RecordedDecision or new choice exists. REENTER authority remains a separate unavailable premise, and all later phases are excluded.

The exact pre-state has E2-GATE at **EXTERNAL_EVIDENCE_REQUIRED**, `history=[]`, no accepted events and no request-ready or waiting occurrence. The request/receipt contract is complete and the rule is known, so the next legal operation can declare request readiness; it cannot complete reentry because required external Evidence is absent.

Native global control may already compute **EXTERNAL_WAIT** when the external boundary is exposed with no internal/human work. The immutable Snapshot has no persisted CONTROL field. This contract does not fabricate a pre-control value or unrelated runnable Action to force a scalar transition. “EXTERNAL_WAIT not yet entered for this occurrence” means the waiting-stage event is absent, not that the read-only control enum must differ. The negative for preexisting wait rejects an already-WAITING start or a state-only substitute for the new sequence, while permitting the legitimate pre-trace control computation.

## Independently sealed events and states

[Trace/state oracles](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1/trace-and-state-oracles.json) are authored from the canonical adjacent-stage/history rules. No native transition was simulated or applied to obtain expected answers. Expected event/Snapshot/bundle hashes use unchanged native codecs. Event identity does not acquire inline request/context/authority fields: native pre/after Snapshot bindings carry exact request/gate/provenance/context, and the bundle carries source/policy pins.

| Boundary | Event / parent / position | Required state |
|---|---|---|
| Request-ready | EVENT_ONE; null parent; index 0 / sequence 1 | READY_STATE; history REQUIRED → READY |
| Waiting | EVENT_TWO; EVENT_ONE parent; index 1 / sequence 2 | WAIT_STATE; history REQUIRED → READY → WAITING |

The first command binds START_STATE; the second binds the **actual** post-ready Snapshot, which must equal READY_STATE before it is submitted. Exactly two events may exist; no event can be inserted between them. Final ledger root is EVENT_ONE, head is EVENT_TWO, and its coordinate is WAIT_BUNDLE#/bundle/events. Root/head/position/parent bindings use native IDs, never time or report order.

The [pre](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1/oracles/primary/pre-trace.json), [request-ready](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1/oracles/primary/request-ready.json) and [post](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1/oracles/primary/post-trace.json) oracles seal exact Snapshots and complete unchanged domain inventories. All require EXTERNAL_WAIT, no actionable/human-ready/selected Action, UNKNOWN obligation with PROOF_RULE_KNOWN_EVIDENCE_MISSING, no receipt/Evidence/validation/support/proof/reentry eligibility, no Knowledge/ActionResult/completion and unresolved root. Persisted Action status remains ACTION_ELIGIBLE; computed actionability is BLOCKED. Only gate stage/history and event-ledger/bundle identities change.

## Durability, restore, replay and independent reproduction

The [durable contract](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1/persistence-replay-determinism-contract.json) uses existing **codec.commit_event / record_result / append_event / apply_receipt / atomic HEAD publication**. A06 already has a registered replayable ExternalEvent. It does not require D01's PREPARE/dossier transaction, typed ValidationInstances or an event-payload extension.

Each phase result, occurrence event, post-Snapshot and bundle/head commits atomically. A request-ready checkpoint alone is a valid intermediate state; it cannot qualify the complete A06 trace. After event 1, terminate the writer and restore the exact ready bundle before event 2. After event 2, terminate again and cold-restore the final complete ledger. Unreachable staged files before HEAD publication are not a durable accepted occurrence. Ordinary stale-parent retry rejects; existing append-event identity idempotence must never be used to invent a second phase occurrence.

Fresh readers receive trusted identities, actual native event files, source/policy bytes and pinned code, without writer memory. They recover all request/gate/context and event parent/position/root/head bindings, exact canonical state and derived control/absence results. Historical replay consumes the recorded two ExternalEvents and applies their deterministic state effects; it does not send a request, choose a new result, append an event or prove original A06 history.

Seal: primary writers under seeds **0,1,7,101**, **three cold readers per START/READY/WAIT checkpoint per seed** (36 primary reads), and **three independent reproduction fixtures**, each at seed 0 with three final cold readers. Reproductions have distinct presealed contexts/source/history/event identities; compare each to its own oracle and compare declared A06 semantic projection across histories. Within one fixture, exact native bytes/identities must be stable under seeds and original/reversed/rotated permitted unordered presentation. Object keys, predicate sets and source-pin sets may permute; causal events and gate history must retain order. Singleton sets have only one permutation.

## Negatives and END/N12/N13

**NEGATIVE_COUNT** [negative controls](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1/sealed-negative-oracles.json) are sealed, unexecuted and assigned to native or exact trusted acceptance boundaries. They cover request/gate/dependency, parent/pre-state, event type/payload/bindings/order, ledger/position, authority/scope/lineage/generation/provenance, missing readiness/wait, state/report surrogates, preexisting wait, later evidence, historical relabeling/identity substitution, oracle operands and full-END scope expansion. Every negative must fail closed for qualification; a valid request-ready-only intermediate state fails **complete trace acceptance**, rather than being mislabeled an illegal native state. Generic native APIs may accept other well-formed models; the sealed experiment must reject every out-of-scope substitution.

The [END/N12/N13 mapping](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1/END-N12-N13-mapping.json) consumes only the future **actual primary native two-event witness**, after all comparisons/persistence/replay/determinism/negatives pass, as **AUTHORIZED_PROSPECTIVE_REPLACEMENT** for `E2-A06.request_wait_event_trace`. Expected event files are not witnesses. No new ID is substituted for the unknown original event/parent/position.

N12 is recovered independently: selection/history is not execution/result, and no ledger/Knowledge may be fabricated. The mapping requires actual native phase results and enrollment, rejecting definitions, selections, Snapshots and reports as occurrences. N13 is separate: prospective output/Action declarations are not actual supplied results. The mapping separates request/scaffold/oracle definitions from the actual phase events and preserves absent Knowledge/root/slot/reentry/Action completion effects. **Both mappings are preserved by contract; neither global P05 negative nor actual A06 qualification is claimed PASS here.** Original occurrence/ancestry and full prefix remain UNPROVEN.

## Complete post-A06 P05 readiness oracle

Future successful qualification may change only A06, taking stage coverage **12 → 13 / 13** and retaining all twelve prior bindings with exact source pins. The [complete readiness oracle](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1/post-A06-complete-P05-readiness-oracle.json) requires independent re-evaluation of the P04 initial oracle, full stage graph, six global END interfaces and ancestry, nine actual configuration occurrences, identity/currentness/provenance, sixteen unchanged P05 negative expectations and concrete isolated operands, persistence/reader manifests, replay bindings, authorities, qualified capabilities/current definitions and all non-stage END/A14-A16/D01/REG input requirements.

**13/13 alone does not imply P05_EXECUTION_READY.** The original prefix-to-checkpoint-to-target relationship or separately governing full-END mapping remains unresolved and is not waived by A06 scope. Full-END process/negative fixture bindings must also be completed. The future evaluator returns YES only when every prepared-execution term passes; otherwise NO with the first remaining dependency-ordered blocker. Future P05 verdicts/logs are outputs, not invented preparation inputs. P05 PASS and P06 review readiness remain later outcomes; N_REAL and historical P03 correspondence are not reopened.

## Later execution and preservation

The [later execution contract](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1/later-execution-contract.json) verifies the exact start and all seals, commits request-ready then waiting once, captures native results/events, terminates/cold-restores, replays without appending, runs presealed reproductions/negatives, evaluates END/N12/N13, then reruns the full binding/readiness predicate. It stops on any mismatch and records FIRST_COUNTEREXAMPLE, EXPECTED, ACTUAL, STATE_ID, EVENT_ID and CLASSIFICATION. No live repair, new authority or configuration, A05 reproduction or P05 execution is allowed.

[Verification](qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1/verification.json) compares the entire pre-work baseline and all older seals; verifies source/fixture/oracle identities, code/source/inputs and expected-payload separation; confirms zero barred lifecycle/application/append/restore/replay calls; and checks git diff --check. Expected successor/event objects are comparison-only. Only fresh empty inputs and contract metadata are written.

```text
WORK_PACKAGE = E2-P05-A06-PROSPECTIVE-REQUEST-WAIT-CONTRACT
RESULT = PASS (CONTRACT ONLY)
SELECTED_OPTION = AUTHORIZE_PROSPECTIVE_P05_A06_REQUEST_WAIT_QUALIFICATION
ORIGINAL_A06_HISTORICAL_REQUEST_WAIT_TRACE = UNPROVEN
A06_DEFINITION = CANONICAL_KNOWN_RULE_MISSING_EVIDENCE_REQUEST_WAIT_CASE
TRACE_SHAPE = REQUEST_READY_EXTERNAL_EVENT -> WAITING_EXTERNAL_EVENT
AUTHORITY = QUALIFICATION_SCOPE_APPLICABLE; NO_NATIVE_EVENT_GRANT_OPERAND
PROSPECTIVE_A06_AUTHORITY_DECISION_REQUIRED = NO
END_MAPPING = AUTHORIZED_PROSPECTIVE_REPLACEMENT_FOR_A06_ONLY
N12_MAPPING = PRESERVED_BY_SEALED_CONTRACT; NOT_EXECUTED
N13_MAPPING = PRESERVED_BY_SEALED_CONTRACT; NOT_EXECUTED
POST_A06_EXPECTED_BINDINGS = 13/13 ONLY_IF_ACTUAL_A06_QUALIFICATION_PASSES
POST_A06_P05_READINESS_ORACLE = COMPLETE_CONJUNCTION; FULL_END_SCOPE_GAP_NOT_WAIVED
PROSPECTIVE_A06_EXECUTION_READY = YES
PROSPECTIVE_A06_EXECUTED = NO
P05_BOUND_STAGE_INPUTS = 12
P05_EXECUTION_READY = NO
P05_EXECUTED = NO
P06_EXECUTED = NO
ORIGINAL_A03_HISTORICAL_OCCURRENCE = UNPROVEN
ORIGINAL_A04_HISTORICAL_ANCESTRY = UNPROVEN
ORIGINAL_A05_HISTORICAL_ANCESTRY = UNPROVEN
P03_HISTORICAL_CORRESPONDENCE = UNPROVEN
N_REAL_SATISFIED = NO
RUNTIME_MODIFIED = NO
E1_ARTIFACTS_MODIFIED = 0
PRODUCTION_EFFECT = NO
git diff --check = PASS
```
'''
    replacements = {
        'SUBJECT_ID': subject, 'START_BUNDLE': primary['START_BUNDLE_ID'],
        'START_STATE': primary['START_STATE_ID'], 'START_LEDGER': primary['LEDGER_ID'],
        'REQUEST_CONTENT': primary['REQUEST_CONTENT_ID'], 'GATE_CONTENT': primary['GATE_CONTENT_ID'],
        'EVENT_ONE': events[0]['EVENT_ID'], 'EVENT_TWO': events[1]['EVENT_ID'],
        'READY_STATE': primary['EXPECTED_POST_READY_STATE_ID'], 'WAIT_STATE': primary['EXPECTED_POST_WAIT_STATE_ID'],
        'WAIT_BUNDLE': primary['EXPECTED_POST_WAIT_BUNDLE_ID'], 'NEGATIVE_COUNT': str(negative_count)}
    for token, value in replacements.items():
        md = re.sub(r'\b' + re.escape(token) + r'\b', lambda match: value, md)
    path = PLANS / (PREFIX + NAME + '.md')
    if path.exists() and path.read_text() != md:
        raise ValueError('sealed report conflict')
    path.write_text(md)


if __name__ == '__main__':
    main()
