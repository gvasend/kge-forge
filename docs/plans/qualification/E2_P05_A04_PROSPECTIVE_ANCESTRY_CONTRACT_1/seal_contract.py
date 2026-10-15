"""Seal an A04 contract; never evaluate or apply an A04 transition.

Expected typed results/states are comparison-only algebraic descriptions. The
missing durable dossier operand is recorded, not registered or simulated.
"""
import ast
import hashlib
import json
from dataclasses import fields, replace
from pathlib import Path
from typing import get_type_hints, get_args

from adapter.planner import codec as c, core, model as m

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
PLANS = ROOT / 'docs/plans'
PREFIX = 'DETERMINISTIC_PLANNER_V0_1_'
SELECTED = 'AUTHORIZE_PROSPECTIVE_P05_A04_ANCESTRY_QUALIFICATION'
REPORT_NAME = PREFIX + 'E2_P05_A04_PROSPECTIVE_ANCESTRY_CONTRACT_1'
LABELS = {
    'QUALIFICATION_TYPE': 'PROSPECTIVE_REPLACEMENT',
    'ORIGINAL_A04_HISTORICAL_ANCESTRY': 'UNPROVEN',
    'HISTORICAL_RECONSTRUCTION': 'NO',
    'PROSPECTIVE_A04_EVENT_IS_ORIGINAL_EVENT': 'NO',
}
EXPECTED_START = {
    'START_BUNDLE_ID': 'planner-bundle-v1:b4a7494aa5617b4c913d23addf338361959a75d9cfee13b3ba2308f8ccb69a39',
    'START_STATE_ID': 'planner-snapshot-v1:3af1c42da8555f4756be47fec23114bc00a8974ef830ef49ece16e67d9d4508f',
    'LEDGER_ROOT': 'planner-event-v1:db8bc77aa2f5bd161272ed2e54993bf6d1c74b63d202d15af329ab64b51edd2c',
    'APPEND_HEAD': 'planner-event-v1:d6ac0bb81a978ed5b8d8eb10195e75f75aba1af34c284e093f0ec8b70a797e8f',
    'PARENT_EVENT_ID': 'planner-event-v1:d6ac0bb81a978ed5b8d8eb10195e75f75aba1af34c284e093f0ec8b70a797e8f',
}


def canon(value):
    return c.canonical_bytes(value)


def identity(value):
    return value.namespace + ':' + value.sha256


def content_id(value, namespace):
    return namespace + ':' + hashlib.sha256(canon(value)).hexdigest()


def pin(path, pointer=''):
    path = Path(path).resolve()
    return {'path': str(path.relative_to(ROOT)), 'pointer': pointer,
            'raw_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def save(name, value, canonical=False):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = canon(value) if canonical else (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()
    if path.exists() and path.read_bytes() != raw:
        raise ValueError('sealed file conflict: ' + name)
    path.write_bytes(raw)
    return pin(path)


def source_location(path, name):
    tree = ast.parse((ROOT / path).read_text())
    node = next(n for n in ast.walk(tree)
                if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name == name)
    return dict(pin(ROOT / path), symbol=name, line=node.lineno, end_line=node.end_lineno)


FORBIDDEN_CALLS = []


def bar(name):
    def forbidden(*args, **kwargs):
        FORBIDDEN_CALLS.append(name)
        raise AssertionError('contract-only operation forbidden: ' + name)
    return forbidden


def install_guards():
    for module, names in (
        (core, ('recompute', 'apply_result', 'apply_event', '_inventory', '_decision_result',
                'admit_dossier_materialization', 'apply_recorded_decision', 'apply_decision_reentry')),
        (c, ('_replay', 'apply_event', 'record_result', 'append_event', 'commit_event',
             'commit_result', 'decode_bundle', 'bundle_bytes', 'replay')),
    ):
        for name in names:
            if hasattr(module, name):
                setattr(module, name, bar(module.__name__ + '.' + name))


def main():
    install_guards()
    authoritative_names = [
        'E2_P05_A04_EVENT_ANCESTRY_RECOVERY_1.md', 'E2_P05_A04_EVENT_ANCESTRY_RECOVERY_1.json',
        'E2_P05_END_INPUT_BINDING_1.md', 'E2_P05_END_INPUT_BINDING_1.json',
        'E2_P05_READINESS.md', 'E2_P05_READINESS.json',
        'E2_P05_A03_PROSPECTIVE_OCCURRENCE_RESULT_1.md',
        'E2_P05_A03_PROSPECTIVE_OCCURRENCE_RESULT_1.json',
        'E2_P05_A03_PROSPECTIVE_OCCURRENCE_BUNDLE_1.json',
        'CANONICAL_QUALIFICATION_EXPERIMENT_1.md', 'CANONICAL_QUALIFICATION_EXPERIMENT_1.json',
        'CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md', 'E2_PC01_SOURCES.json',
        'E2_PC01_FIXTURES.json', 'E2_T02_RESULT.md', 'E2_T02_RESULT.json',
        'E2_P04_CANONICAL_EXECUTION_RETRY_1_RESULT.json', 'E2_P04_CANONICAL_TARGET_BUNDLE_1.json',
    ]
    references = [pin(PLANS / (PREFIX + name)) for name in authoritative_names]
    scope_path = PLANS / 'qualification/E2_P05_A04_EVENT_ANCESTRY_RECOVERY_1/scope-decision-dossier.json'
    scope = json.loads(scope_path.read_bytes())
    subject_id = content_id(scope['subject'], 'qualification-scope-subject-v1')
    assert subject_id == scope['subject_identity']
    assert subject_id == 'qualification-scope-subject-v1:4b57d7fc27d1c0b63deaece9d0be47c72e8e6d7b40e7a54ea7a56d6a641c85ac'
    option = next(x for x in scope['options'] if x['option'] == SELECTED)
    assert option['decision_ready'] and not option['future_execution_contract_already_complete']
    references.append(pin(scope_path))
    cases = json.loads((PLANS / (PREFIX + 'CANONICAL_QUALIFICATION_EXPERIMENT_1.json')).read_bytes())['cases']
    by_case = {x['CASE_ID']: x for x in cases}
    assert by_case['E2-A04']['OPERATION'] == 'Apply preparation result then recompute'
    assert by_case['E2-N12']['EXPECTED_STATE'] == 'No native result accepted; ledger/knowledge not fabricated'
    assert by_case['E2-N13']['EXPECTED_STATE'] == 'Reject wrong event/result; knowledge/root/slot unchanged'

    start_path = PLANS / (PREFIX + 'E2_P05_A03_PROSPECTIVE_OCCURRENCE_BUNDLE_1.json')
    # Decode fields only. No replay, native result application, or new fixture.
    start = c._unwire(c.parse_json(start_path.read_bytes())['bundle'])
    m.validate_types(start, m.PersistenceBundle)
    m.validate_model(start.initial)
    m.validate_model(start.current)
    assert start_path.read_bytes() == c._bundle_bytes_admitted(start)
    observed = {
        'START_BUNDLE_ID': identity(c._identity(start_path.read_bytes(), 'planner-bundle-v1')),
        'START_STATE_ID': identity(c.snapshot_id(start.current)),
        'LEDGER_ROOT': identity(start.events[0].identity),
        'APPEND_HEAD': identity(start.events[-1].identity),
        'PARENT_EVENT_ID': identity(start.events[-1].identity),
    }
    assert observed == EXPECTED_START and len(start.events) == 2
    previous = None
    predecessor_snapshot = c.snapshot_id(start.initial)
    for position, event in enumerate(start.events, 1):
        assert event.sequence == position and event.parent_event == previous
        assert event.parent_snapshot == predecessor_snapshot
        assert event.identity == c._event_identity(position, event.parent_snapshot,
            previous, event.result, event.after_snapshot, event.resume_binding)
        previous, predecessor_snapshot = event.identity, event.after_snapshot
    assert predecessor_snapshot == c.snapshot_id(start.current)
    assert [e.result.action.value for e in start.events] == ['E2-CHECK', 'E2-COLLECT']
    c._verify_sources(start, ROOT)
    context = start.current.context
    assert context.lineage == 'E2-P05-A03-PROSPECTIVE-QUALIFICATION-1'
    assert context.lineage != 'E2-CANONICAL-BASELINE-1'
    assert context.scope == 'E2-QUALIFICATION-ONLY' and context.tick == 0
    action = next(a for a in start.current.actions if a.id.value == 'E2-PREPARE')
    decision = next(d for d in start.current.decisions if d.input_action == action.id)
    assert action.authority is None and action.prepared_dossier is None
    assert action.operation is m.OperationClass.DECISION_INPUT_ACQUISITION
    assert decision.dossier is None and decision.record is None and decision.recorded_choice is None
    assert not start.current.validation_instances and not start.current.entities
    assert {k.id.value for k in start.current.knowledge} == {'E2-K-CHECK', 'E2-K-COLLECT'}
    assert all(s.state is m.ActionState.COMPLETED for s in start.current.statuses
               if s.id.value in ('E2-CHECK', 'E2-COLLECT'))
    assert next(s for s in start.current.statuses if s.id == action.id).state is not m.ActionState.COMPLETED
    frontier_path = PLANS / 'qualification/E2_P05_A03_PROSPECTIVE_OCCURRENCE_EXECUTION_1/P05-binding-rerun.json'
    frontier = json.loads(frontier_path.read_bytes())
    assert frontier['P05_BOUND_STAGE_INPUTS'] == 10
    assert frontier['P05_NEXT_MISSING_INPUT'] == 'E2-A04.prepare_result_event_ancestry'
    references.append(pin(frontier_path))
    authorization = {
        **LABELS, 'selected_option': SELECTED, 'subject_identity': subject_id,
        'issuer': 'HUMAN_EXPLICIT_CURRENT_CONVERSATION_INSTRUCTION',
        'verification': 'Exact selected option and unchanged retained subject content; no native signature/grant invented',
        'selected_option_source': 'Current user message, AUTHORITATIVE HUMAN DECISION',
        'retained_dossier': pin(scope_path), 'retained_dossier_modified': False,
        'applicable_scope': scope['subject']['prospective_scope'],
        'AUTHORIZATION_SUBJECT_MATCH': 'PASS', 'QUALIFICATION_SCOPE_AUTHORIZATION': 'PASS',
        'native_operating_authority_issued': False, 'install_authority_issued': False,
        'execution_in_this_package_authorized': False,
    }
    save('authenticated-scope-decision.json', authorization)
    start_spec = {
        **LABELS, **observed, 'START_PATH': pin(start_path),
        'LEDGER_ID': observed['START_BUNDLE_ID'] + '#/bundle/events',
        'ledger_identity_domain': 'Content-addressed PersistenceBundle and events pointer; no native LedgerId field',
        'scope': context.scope, 'lineage': context.lineage, 'generation': context.generation,
        'tick': context.tick, 'policy': c._wire(start.policy),
        'policy_version': start.policy_version, 'bundle_scope': start.scope,
        'sources': c._wire(start.sources), 'event_count': 2,
        'prefix_events': [{'sequence': e.sequence, 'event_id': identity(e.identity),
                           'ActionId': e.result.action.value, 'pre_state': identity(e.parent_snapshot),
                           'post_state': identity(e.after_snapshot)} for e in start.events],
        'start_form': 'EXISTING_RETAINED_EVENT_BEARING_AUTHORIZED_A03_PROSPECTIVE_BUNDLE',
        'PROSPECTIVE_LINEAGE_DIFFERS_FROM_ORIGINAL': 'YES',
        'new_genesis_or_authority': False, 'prefix_reexecution': False,
        'state_rebound_or_reset': False, 'A03_replacement_reopened': False,
        'verification': 'Pure canonical identities, native field typing, parent/sequence links and physical source/policy pins; prior A03 cold-restore/replay PASS is retained, not rerun here',
    }
    save('prospective-start.json', start_spec)
    declaration_path = PLANS / (PREFIX + 'E2_PC01_SOURCES.json')
    declarations = json.loads(declaration_path.read_bytes())
    original = next(x for x in declarations['declarations'] if x['id'] == action.id.value)
    assert original['authority'] == [] and original['accepted_result'] == 'PASS'
    assert original['output']['id'] == 'E2-K-PREPARE'
    assert original['output']['statement'] == 'Bounded decision inputs prepared'
    assert action.accepted_result is m.ActionResult.PASS and len(action.accepted_inventory) == 1
    output_contract = action.accepted_inventory[0]
    assert output_contract.id.value == 'E2-K-PREPARE' and output_contract.producer == action.id
    assert output_contract.statement == 'prospective output contract for E2-PREPARE'
    native_definition = {
        **LABELS, 'A04_ID': 'E2-A04', 'A04_TYPE': 'Acceptance case over E2-PREPARE Action',
        'A04_ACTION_ID': action.id.value, 'earliest_case': dict(pin(PLANS / (PREFIX + 'CANONICAL_QUALIFICATION_EXPERIMENT_1.json')), pointer='/cases/3'),
        'earliest_concrete_definition': dict(pin(declaration_path), pointer='/declarations/2'),
        'canonical_declaration': original, 'native_start_Action': c._wire(action),
        'native_Action_content': content_id(c._wire(action), 'a04-contract-native-action-v1'),
        'PRECONDITIONS': ['Completed CHECK and COLLECT', 'Current accepted E2-K-CHECK and E2-K-COLLECT',
                          'PREPARE selected by the current Planner', 'No recorded human decision', 'Exact start state/head'],
        'AUTHORITY': 'No PREPARE operating grant: native Action.authority=None and canonical authority=[]; qualification scope separately selected',
        'NATIVE_OPERATION': 'core.admit_dossier_materialization(snapshot, SuppliedResult, Tuple[ValidationInstance,...])',
        'EXPECTED_RESULT': 'Actual PASS; exactly one E2-K-PREPARE output; complete independently checked dossier',
        'POSTCONDITION': 'PREPARE completed; dossier and six typed validations admitted; DECISION_READY/HUMAN_HANDOFF; no decision choice/grant/downstream execution',
        'output_text_comparison': {
            'earliest_declaration': original['output']['statement'],
            'exact_admitted_prospective_inventory': output_contract.statement,
            'classification': 'DISCLOSED_LITERAL_DIFFERENCE_IN_ALREADY_AUTHORED_PROSPECTIVE_A03_START',
            'oracle_choice': 'Exact native accepted inventory; no Action rewrite. Canonical A04 case requires result/readiness, not literal statement equality.',
            'source_accepted_as_actual_result': False,
        },
    }
    save('A04-definition.json', native_definition)

    supported = sorted(m.SUPPORTED_DOSSIER_CHECKS, key=lambda x: x.value)
    assert len(supported) == 6
    rule_text = {
        'QUESTION_SCOPE': 'Question and scope equal the sealed qualification-only source, with no additional subject.',
        'SOURCE_PROVENANCE': 'Raw source identity/path/section/excerpt match; CHECK/COLLECT native records and predecessor event bindings remain exact.',
        'CONCRETE_ALTERNATIVES': 'Alternatives equal ALLOW_QUALIFICATION_MAPPING and DECLINE; no empty or added option.',
        'AUTHORITY_BOUNDARY': 'USE for E2 mapping only is prospective; independent grant still required; no production, E1 or proof authority is issued.',
        'DECISION_FACTS_COMPLETE': 'Both declared fact predicates refer to accepted CHECK/COLLECT outputs with completed producers in the sealed pre-state.',
        'INDEPENDENT_VALIDATION': 'All other checks are evaluated from source/current inputs independently of producer result and oracle files; typed bindings/currentness are exact.',
    }
    source_body = {
        'schema': 'E2-P05-A04-PROSPECTIVE-DOSSIER-DEFINITION-1', **LABELS,
        'role': 'Prospective source declaration/validator rules; no result or event asserted',
        'scope': context.scope, 'lineage': context.lineage, 'generation': context.generation,
        'selected_scope_subject': subject_id, 'governing_PC01': pin(declaration_path, '/prospective_dossier'),
        'dossier_declaration': declarations['prospective_dossier'],
        'validation_rules': rule_text, 'validation_input_binding': [observed['START_STATE_ID'], 'THIS_RAW_SOURCE_IDENTITY'],
        'checks_native': [x.value for x in supported],
        'checks_descriptive_only': sorted(set(declarations['prospective_dossier']['checks']) - {x.value for x in supported}),
        'no_actual_validation_instances': True, 'no_world_facts': True, 'production_effect': False,
    }
    source_pin = save('inputs/dossier-source.json', source_body, canonical=True)
    source_raw = (ROOT / source_pin['path']).read_bytes()
    source_identity = c._identity(source_raw, 'raw-file-sha256')
    native_pin = m.ArtifactPin(source_pin['path'], source_identity)
    provenance = m.Provenance(source_pin['path'], source_identity, '/dossier_declaration',
        canon(source_body['dossier_declaration']).decode(), 'PROSPECTIVE_A04_AUTHORED_DOSSIER_DEFINITION', context.scope)
    fixture = json.loads((PLANS / (PREFIX + 'E2_PC01_FIXTURES.json')).read_bytes())
    template_dossier = c._unwire(next(x for x in fixture['native_actions']
                                    if x['id']['value'] == action.id.value)['prepared_dossier'])
    dossier = replace(template_dossier, provenance=provenance,
        checks=tuple(replace(ch, provenance=provenance) for ch in template_dossier.checks))
    m.validate_types(dossier, m.DecisionDossier)
    dossier_identity = c._identity(canon(c._wire(dossier)), 'planner-dossier-sha256')
    # These are comparison-only expected values, never admitted instances.
    expected_instances = tuple(m.ValidationInstance(
        next(ch.predicate for ch in dossier.checks if ch.kind is kind), kind.value,
        dossier_identity, (c.snapshot_id(start.current), source_identity),
        m.ValidationOutcome.PASS, context.scope, context.lineage,
        m.ValidationState.ACCEPTED, provenance) for kind in supported)
    supplied = m.SuppliedResult(action.id, m.ActionResult.PASS, (output_contract,),
                                c.snapshot_id(start.current), dossier)
    m.validate_types(supplied, m.SuppliedResult)
    for instance in expected_instances:
        m.validate_types(instance, m.ValidationInstance)
    inputs = []
    for input_id, native_type, value, source_ref, currentness in (
        ('CURRENT_CANONICAL_PROSPECTIVE_STATE', 'Snapshot', start.current, pin(start_path, '/bundle/current'), 'Exact snapshot identity and pinned tick/context'),
        ('PREPARE_ACTION_DEFINITION', 'Action', action, pin(start_path, '/bundle/current/actions'), 'Admitted in exact starting state; not completed'),
        ('DECISION_INPUT_BINDING', 'Decision', decision, pin(start_path, '/bundle/current/decisions'), 'Input Action=PREPARE; no dossier/choice/record'),
    ):
        inputs.append({'INPUT_ID': input_id, 'TYPE': native_type,
            'CONTENT_ID': content_id(c._wire(value), 'a04-contract-input-content-v1'),
            'CANONICAL_CONTENT': c._wire(value), 'SOURCE': source_ref,
            'PROVENANCE': 'Exact retained native content, not an original historical witness',
            'SCOPE': context.scope, 'LINEAGE': context.lineage, 'GENERATION': context.generation,
            'CURRENTNESS': currentness})
    for record in start.current.knowledge:
        inputs.append({'INPUT_ID': record.id.value, 'TYPE': 'KnowledgeRecord',
            'CONTENT_ID': content_id(c._wire(record), 'a04-contract-input-content-v1'),
            'SEMANTIC_ID': record.id.value, 'CANONICAL_CONTENT': c._wire(record),
            'SOURCE': pin(start_path, '/bundle/current/knowledge'), 'PROVENANCE': c._wire(record.provenance),
            'SCOPE': context.scope, 'LINEAGE': context.lineage, 'GENERATION': context.generation,
            'CURRENTNESS': 'KNOWN_COMPLETE / ACCEPTED; producer completed and prior native event result binds this record'})
    inputs.append({'INPUT_ID': 'PROSPECTIVE_DOSSIER_SOURCE', 'TYPE': 'Authored definition / raw ArtifactPin',
        'CONTENT_ID': identity(source_identity), 'CANONICAL_CONTENT': source_body,
        'SOURCE': source_pin, 'PROVENANCE': c._wire(provenance),
        'SCOPE': context.scope, 'LINEAGE': context.lineage, 'GENERATION': context.generation,
        'CURRENTNESS': 'Raw pin verified offline; NOT YET A CANONICAL SOURCE ADDITION; must be enrolled atomically by the missing durable integration'})
    for kind in supported:
        inputs.append({'INPUT_ID': 'VALIDATOR-RULE-' + kind.value, 'TYPE': 'Independent validation rule, not ValidationInstance',
            'CONTENT_ID': identity(source_identity), 'CONTENT_POINTER': '/validation_rules/' + kind.value,
            'CANONICAL_CONTENT': rule_text[kind.value], 'SOURCE': source_pin, 'PROVENANCE': c._wire(provenance),
            'SCOPE': context.scope, 'LINEAGE': context.lineage, 'GENERATION': context.generation,
            'CURRENTNESS': 'Rule selected before execution; actual typed evaluation result must be produced at the pinned pre-state'})
    save('prospective-inputs.json', {'role': 'SEALED_INPUTS_NOT_RESULTS', **LABELS,
        'inputs': inputs, 'source_addition_required': c._wire(native_pin),
        'ValidationInstance_inputs_order': 'Ordered tuple (pre-state identity, source identity); codec does not declare this field unordered',
        'no_prospective_instance_installation': True})
    producer = {
        'schema': 'A04-PROSPECTIVE-BOUNDED-PRODUCER-CONTRACT-1', **LABELS,
        'start': pin(start_path), 'source': source_pin, 'ActionId': action.id.value,
        'type': 'Bounded qualification-only native SuppliedResult plus independently evaluated dossier validations',
        'construct_fresh_result': 'Read the current admitted native Action result contract, produce one new bounded PASS KnowledgeRecord and dossier from the pinned authored source. This is synthetic qualification output, not an external-world fact.',
        'construct_validations': 'Evaluate each of the six sealed rules independently; create fresh typed ValidationInstances binding the actual dossier content identity, exact pre-state/source inputs, scope and lineage. Do not copy expected-instance bytes as decisions.',
        'execution_read_allowlist': [pin(start_path), source_pin] + [pin(ROOT / s.path, s.pointer) for s in start.sources] + [pin(ROOT / start.policy.path)],
        'excluded_inputs': ['All oracles/*', 'expected result/event/post-state', 'historical handoff Snapshot', 'reports as occurrence witnesses'],
        'commit_allowed_now': False,
    }
    save('inputs/bounded-producer-contract.json', producer, canonical=True)
    authority = {
        **LABELS, 'QUALIFICATION_SCOPE_AUTHORIZATION': authorization,
        'native_Action_authority': None, 'canonical_authority_requirements': [],
        'ADDITIONAL_AUTHORITY_REQUIRED': 'NO',
        'PROSPECTIVE_A04_AUTHORITY_DECISION_REQUIRED': 'NO',
        'PROSPECTIVE_A04_AUTHORITY_DECISION_READY': 'NO',
        'reason': 'No native PREPARE operating or INSTALL grant is required for dossier-result admission. The selected qualification-scope decision applies to this new bounded lineage continuation; it grants no runtime repair permission.',
        'source_permission': 'Authored qualification-only dossier bytes under the selected experiment scope; no production semantics',
        'new_grants_issued': [], 'missing_installation_set_established': False,
        'future_RUNTIME_implementation_authorized_here': False,
    }
    save('authority.json', authority)

    # Algebraic expected state from the authoritative T02 field effects, not
    # apply_result/recompute output. It is not a persisted occurrence witness.
    final_history = decision.history + (m.DecisionStage.DECISION_INPUT_ACQUISITION,
        m.DecisionStage.DECISION_DOSSIER_READY, m.DecisionStage.DECISION_READY)
    expected_after = replace(start.current,
        actions=tuple(replace(a, prepared_dossier=dossier) if a.id == action.id else a for a in start.current.actions),
        statuses=tuple(replace(s, state=m.ActionState.COMPLETED) if s.id == action.id else
                       replace(s, state=m.ActionState.ACTIONABLE) if s.id == decision.action else s
                       for s in start.current.statuses),
        knowledge=tuple(sorted(start.current.knowledge + (output_contract,), key=lambda k: k.id.value)),
        decisions=tuple(replace(d, dossier=dossier, stage=m.DecisionStage.DECISION_READY,
                               history=final_history) if d.action == decision.action else d for d in start.current.decisions),
        validation_instances=expected_instances)
    m.validate_model(expected_after)
    after_id = c.snapshot_id(expected_after)
    unaffected = {f.name: getattr(expected_after, f.name) == getattr(start.current, f.name)
                  for f in fields(m.Snapshot)
                  if f.name not in ('actions', 'statuses', 'knowledge', 'decisions', 'validation_instances')}
    assert all(unaffected.values())
    result_oracle = {
        **LABELS, 'role': 'EXPECTED_ORACLE_ONLY_NOT_EXECUTED_NOT_ADMITTED',
        'result_type': 'SuppliedResult', 'outcome': 'PASS', 'outputs': ['E2-K-PREPARE'],
        'expected_result': c._wire(supplied), 'expected_dossier_id': identity(dossier_identity),
        'expected_validation_instances': c._wire(expected_instances),
        'expected_post_state_id': identity(after_id), 'expected_post_state': c._wire(expected_after),
        'expected_control': 'HUMAN_HANDOFF', 'expected_decision_readiness': 'DECISION_READY',
        'expected_postcondition': {
            'PREPARE_COMPLETED': True, 'E2_K_PREPARE_ADMITTED': True,
            'dossier_current': True, 'native_validation_count': 6,
            'human_choice_recorded': False, 'grant_issued': False,
            'REENTER_EXECUTED': False, 'FINISH_EXECUTED': False,
            'new_root_or_slot_proof': False,
        }, 'unchanged_snapshot_fields': unaffected,
        'computed_oracle_source': 'Canonical A04/PC01 semantics and documented T02 field effects; no future runtime output',
        'native_positive_qualification_run': False,
    }
    save('oracles/expected-result-and-state.json', result_oracle)
    payload_contract = {
        **LABELS, 'role': 'REQUIRED_OPERANDS_ONLY_NOT_A_NATIVE_EVENT_OR_RESULT_VARIANT',
        'SuppliedResult': c._wire(supplied), 'validation_instances': c._wire(expected_instances),
        'source_additions': [c._wire(native_pin)],
        'expected_bundle': observed['START_BUNDLE_ID'], 'expected_parent_event': observed['PARENT_EVENT_ID'],
        'existing_typed_ingredients': ['SuppliedResult', 'DecisionDossier', 'ValidationInstance', 'ArtifactPin'],
        'current_durable_native_variant': 'ABSENT',
        'wire_tag_added': False, 'event_fabricated': False,
    }
    save('oracles/required-event-operands.json', payload_contract)
    union = get_args(get_type_hints(m.ExecutionEvent)['result'])
    assert m.SuppliedResult in union
    assert not any(x.__name__ == 'DossierMaterializationAdmission' for x in union)
    gap = {
        **LABELS, 'TRANSACTION_INTERFACE_GAP': 'PERSISTED_DOSSIER_VALIDATION_OPERAND_MISSING',
        'state_operation': source_location('adapter/planner/core.py', 'admit_dossier_materialization'),
        'state_operation_operands': ['snapshot', 'SuppliedResult', 'Tuple[ValidationInstance,...]'],
        'state_operation_output': 'TransitionReport(snapshot, effects, Computation); no ExecutionEvent/ledger append',
        'ordinary_path': ['codec.record_result', 'core.apply_event', 'core.apply_result',
                          'core._inventory', 'core._decision_result', 'ExecutionEvent', 'codec.append_event', 'codec._replay'],
        'ordinary_result_fields': [f.name for f in fields(m.SuppliedResult)],
        'supported_event_result_variants': [x.__name__ for x in union],
        'locations': [source_location('adapter/planner/codec.py', 'record_result'),
                      source_location('adapter/planner/core.py', 'apply_event'),
                      source_location('adapter/planner/core.py', 'apply_result'),
                      source_location('adapter/planner/model.py', 'ExecutionEvent'),
                      source_location('adapter/planner/gates.py', 'validate_result'),
                      source_location('adapter/planner/codec.py', '_replay')],
        'plain_result_failure': 'Current Action.prepared_dossier=None; ordinary validate_result compares any supplied dossier against that definition. Even preloading it would not supply the missing typed validations atomically.',
        'source_pin_gap': 'New dossier-source pin is offline. Source addition/replay enrollment currently has explicit paths for EvidenceSourceAdmission/InstallDefinition, not a dossier materialization event.',
        'minimum_required_generic_integration': {
            'semantics': 'Durably carry exact existing T02 SuppliedResult + ValidationInstance tuple and raw source addition; validate pinned pre-state/current parent; invoke unchanged T02 admission atomically with event+source pins+bundle.',
            'identity': 'Full typed operand must participate in existing ExecutionEvent canonical hash; omitting validations or source additions is forbidden.',
            'preflight_execution_equivalence': 'Same canonical operand/source pins validated and consumed; no alternate reconstruction or authenticated Boolean.',
            'atomicity': 'No durable knowledge/dossier/validation/completion without the one native event and complete post-bundle; failure preserves exact start/head.',
            'retry': 'Same authorized semantic operation creates one occurrence; conflict/stale parent fails closed. Existing T02 state no-op alone does not establish ledger idempotence.',
            'replay': 'Replay historical typed validation outcomes with their original input bindings; do not make new validator decisions.',
        },
        'integration_implemented_or_qualified': False, 'runtime_modified': False,
        'why_not_bypass': ['Direct state admission followed by handcrafted event is not native event execution',
                           'Snapshot reset loses genuine parent ancestry',
                           'ValidationInstances cannot be installed as definitions',
                           'Expected oracle bytes cannot be admitted as actual results'],
        'missing_predicate_installation_inferred': False,
        'predicate_reference_rule': 'Native validate_p03/validate_p04 include ValidationInstance predicate IDs; dossier readiness consumes those typed instances. No six-predicate install requirement is established.',
    }
    save('native-interface-gap.json', gap)
    event_oracle = {
        **LABELS, 'role': 'PARTIALLY_SEALED_NATIVE_EVENT_REQUIREMENT_NOT_OCCURRED',
        'EVENT_TYPE': 'ExecutionEvent', 'EVENT_PAYLOAD': payload_contract,
        'PARENT_EVENT_ID': observed['PARENT_EVENT_ID'], 'PRE_STATE_ID': observed['START_STATE_ID'],
        'POST_STATE_ID': identity(after_id), 'RESULT_BINDINGS': 'Exact actual typed SuppliedResult/ValidationInstances in required-event-operands.json',
        'OUTPUT_BINDINGS': {'KnowledgeId': 'E2-K-PREPARE', 'producer': 'E2-PREPARE',
                            'dossier_identity': identity(dossier_identity), 'actual_output_content': c._wire(output_contract)},
        'scope': context.scope, 'lineage': context.lineage, 'generation': context.generation,
        'provenance': {'Action': c._wire(action.source), 'output': c._wire(output_contract.provenance),
                       'dossier_and_validations': c._wire(provenance)},
        'LEDGER_APPEND_SEMANTICS': {'retained_prefix_event_count': 2, 'new_sequence': 3, 'event_array_index': 2,
                                  'root': observed['LEDGER_ROOT'], 'new_head': 'Actual third event identity',
                                  'append_count': 1, 'other_events_permitted': False},
        'identity_rule': 'planner-event-v1:sha256(canonical_bytes({sequence:3,parent:_wire(pre_state),parent_event:_wire(parent),result:_wire(full_native_operand),after:_wire(post_state)})); no resume_binding for this non-REENTER result',
        'EXPECTED_EVENT_ID': None,
        'EXPECTED_EVENT_ID_UNAVAILABLE_REASON': 'Full native serializable dossier-materialization operand is absent; no guessed wire tag/hash is sealed.',
        'native_payload_oracle_complete': False,
        'result_oracle_ingredients_content_id': content_id(payload_contract, 'a04-required-event-operands-v1'),
    }
    save('oracles/event-oracle.json', event_oracle)
    ancestry = {
        **LABELS, 'role': 'SEALED_ANCESTRY_ACCEPTANCE_RULES_EXECUTION_BLOCKED',
        'occurrence_assurance': ['Actual native PREPARE result admitted', 'Complete native event payload retained'],
        'ancestry_assurance': ['Exact predecessor enrolled', 'Exact pre/post state link',
                              'Single actual append at index2/sequence3', 'Retained root/parent continuity',
                              'Actual result/output/dossier/validation bound to the enrolled event'],
        'required_terms': event_oracle,
        'pass_rule': 'Every event, result, output, parent, pre/post, ledger, position, source/policy, context and provenance equality must pass after native atomic admission, persistence, independent cold restore and replay. A report/snapshot alone is insufficient.',
        'historically_unavailable_fields_to_prove': ['complete event payload', 'actual parent', 'ledger membership/position',
                                                   'event-to-preparation-result/readiness linkage'],
        'post_ledger_id_rule': 'Actual post-A04 planner-bundle-v1 content identity plus #/bundle/events; prefix must equal exact START ledger.',
        'snapshot_alone_sufficient': False, 'occurrence_without_parent_sufficient': False,
        'PROSPECTIVE_A04_ANCESTRY': 'NOT_EVALUATED',
    }
    save('oracles/ancestry-oracle.json', ancestry)
    ordering = {
        **LABELS, 'predecessor': start_spec['prefix_events'][-1],
        'root': start_spec['prefix_events'][0], 'A04_sequence': 3, 'A04_index': 2,
        'successor': 'NONE_REQUIRED_AT_A04_HEAD',
        'successor_rule_if_descendant_presented': 'Its parent_event must equal actual A04 event ID; parent_snapshot must equal actual A04 after_snapshot; index/sequence4. Never infer successor from report order.',
        'P05_scope_limit': 'This proves new prospective prefix -> A04 only. No original A03/A04 ancestry, A05/A06 binding or uninterrupted original END history is implied.',
        'history_permutation_allowed': False,
    }
    save('oracles/ordering-oracle.json', ordering)
    mapping = {
        **LABELS, 'target': 'E2-A04.prepare_result_event_ancestry',
        'E2_END_TYPE': 'EXPERIMENT_ACCEPTANCE_CASE',
        'representation': 'Read-only P05 qualification evidence graph; not a native Action input entity',
        'future_binding_classification': 'AUTHORIZED_PROSPECTIVE_REPLACEMENT',
        'required_PASS_terms': ['Actual native A04 ancestry', 'Exact sealed result/postcondition',
                                'Cold restore/replay/determinism', 'All negatives', 'N12 mapping', 'N13 mapping', 'Historical labeling'],
        'original_historical_binding': {'status': 'UNPROVEN', 'original_event_id': None,
                                        'original_parent_id': None, 'original_ledger_position': None},
        'prospective_binding': {'status': 'NOT_EXECUTED_NOT_BOUND', 'qualification_scope_subject': subject_id,
                                'prospective_lineage': context.lineage, 'event_id': None},
        'no_identity_aliasing': True, 'no_original_ancestry_edges_changed': True,
        'current_stage_count': 10, 'maximum_stage_count_after_A04_only': 11, 'total_stages': 13,
        'remaining_stages_not_closed': ['E2-A05', 'E2-A06'],
        'full_original_END_ancestry_waived': False,
        'successful_later_execution': 'Create new read-only binding evidence with exact new artifact/path/pointer/event/parent IDs; keep original historical fields UNPROVEN. Recheck only to the next missing input; do not execute P05.',
    }
    save('END-replacement-mapping.json', mapping)
    n12 = {
        'case': by_case['E2-N12'], 'source': pin(PLANS / (PREFIX + 'CANONICAL_QUALIFICATION_EXPERIMENT_1.json'), '/cases/27'),
        'ORIGINAL_ASSURANCE': 'Selection or report history alone cannot establish execution/completion or fabricate ledger/knowledge.',
        'PROSPECTIVE_ASSURANCE': 'Require one actual admitted typed result/event at the sealed parent/index; selection-only/no-result control must preserve exact pre-state/head/knowledge.',
        'N12_MAPPING_PRESERVED': 'YES', 'preserved': 'Native prospective occurrence/ancestry and selection-execution separation objective',
        'not_preserved': 'Original historical A04 event, parent or original uninterrupted END lineage',
        'qualification_status': 'SEALED_NOT_RUN', 'closure_condition': 'Runtime negative and positive event enrollment checks must pass before END binding.',
    }
    n13 = {
        'case': by_case['E2-N13'], 'source': pin(PLANS / (PREFIX + 'CANONICAL_QUALIFICATION_EXPERIMENT_1.json'), '/cases/28'),
        'ORIGINAL_ASSURANCE': 'Admitted Action/output declaration is not an actual supplied result; wrong event/result leaves knowledge/root/slot unchanged.',
        'PROSPECTIVE_ASSURANCE': 'Pre-start PREPARE output is inventory only. Fresh bounded producer result and independent validations must be admitted by the native transaction; declarations/oracles/reports are rejected as occurrence.',
        'N13_MAPPING_PRESERVED': 'YES', 'preserved': 'Prospective-definition versus actual-admission distinction and unchanged root/slot on rejection',
        'not_preserved': 'Original historical result-to-event linkage; no original event identity reconstructed',
        'qualification_status': 'SEALED_NOT_RUN', 'closure_condition': 'Declaration-as-result negative and actual output/event binding checks must pass before END binding.',
    }
    save('N12-N13-assurance-mapping.json', {'N12': n12, 'N13': n13, **LABELS})
    negatives = [
        ('WRONG_A04_INPUT', 'Change current CHECK/COLLECT input/content', 'Input contract/pre-state'),
        ('WRONG_PREPARE_RESULT', 'FAIL or non-native result for sealed positive command', 'Exact typed PASS'),
        ('WRONG_OUTPUT', 'Missing/extra/wrong producer/content E2-K-PREPARE', 'Exact bounded native inventory'),
        ('WRONG_PARENT', 'Use any parent other than retained COLLECT head', 'Parent equality'),
        ('WRONG_PRE_STATE', 'Use another snapshot identity', 'Pre-state equality'),
        ('WRONG_EVENT_PAYLOAD', 'Omit/tamper dossier/validation/result operand', 'Complete typed operand equality and native identity'),
        ('WRONG_LEDGER', 'Present event in a foreign bundle/ledger', 'Exact start-prefix and ledger enrollment'),
        ('WRONG_APPEND_POSITION', 'Place at another index/sequence', 'Index2/sequence3'),
        ('WRONG_PREDECESSOR', 'Parent not enrolled immediately before A04', 'Native predecessor link'),
        ('WRONG_SUCCESSOR_IF_PRESENTED', 'Present descendant with different parent/pre-state', 'Conditional index3/sequence4 continuity'),
        ('WRONG_AUTHORITY', 'Use foreign scope grant or pretend PREPARE issued decision/USE authority', 'Scope authorization exact; no new grant/state effect'),
        ('WRONG_SCOPE', 'Use a production/foreign qualification scope', 'Context/source/validation exact scope'),
        ('WRONG_LINEAGE', 'Substitute original or foreign lineage', 'Exact prospective context'),
        ('WRONG_PROVENANCE', 'Tamper source identity/path/section/excerpt', 'Raw pins and exact native provenance'),
        ('FOREIGN_EVENT', 'Use another experiment event with matching status', 'Native event/result/parent and source binding'),
        ('SNAPSHOT_AS_ANCESTRY', 'Present completed snapshot without enrolled A04 event', 'Occurrence+ancestry independently required'),
        ('REPORT_AS_ANCESTRY', 'Present report chronology/result summary as event', 'Retained native identity fields required'),
        ('OCCURRENCE_WITHOUT_PARENT_PROOF', 'Present event without parent enrollment', 'Root-to-A04 native prefix continuity'),
        ('PROSPECTIVE_LABELED_HISTORICAL', 'Claim original ancestry recovered', 'Immutable historical labels'),
        ('PROSPECTIVE_AS_ORIGINAL_IDENTITY', 'Alias new event/parent to original missing IDs', 'Separate original/prospective bindings'),
        ('SELECTION_AS_COMPLETION_N12', 'No actual supplied result; selection/history only', 'No completion/knowledge/event/head change'),
        ('DECLARATION_AS_RESULT_N13', 'Supply Action/output declaration or oracle file as actual result', 'Reject non-result and no root/slot/knowledge/head change'),
        ('MISSING_OR_INVALID_INDEPENDENT_VALIDATION', 'Omit/duplicate/fail/stale a required instance or supply validation Boolean', 'Six unique exact typed PASS/current dossier-bound validations'),
        ('EVENT_WITHOUT_ATOMIC_NATIVE_ADMISSION', 'Handcraft event after direct state reset/admission', 'Native persisted operation and replay proof required'),
    ]
    negative_specs = [{'id': 'A04-PROSPECTIVE-N%02d' % i, 'case': name, 'mutation': mutation,
                       'oracle': oracle, 'status': 'SEALED_NOT_RUN',
                       'expected': 'FAIL_CLOSED', 'writer_isolation': True,
                       'durable_effect_rule': 'Any rejected command leaves its exact pre-state/head unchanged; evidence tampering must fail witness/mapping checks and never mutate the successful lineage.'}
                      for i, (name, mutation, oracle) in enumerate(negatives, 1)]
    save('negative-contract.json', {'schema': 'A04-PROSPECTIVE-SEALED-NEGATIVES-1', **LABELS,
                                  'count': len(negative_specs), 'cases': negative_specs})
    persistence = {
        **LABELS, 'role': 'FUTURE_EXECUTION_OBLIGATIONS_NOT_PERFORMED',
        'bundle_type': 'Native PersistenceBundle preserving the actual start.initial, two original prospective prefix events and exactly one new admitted PREPARE event',
        'required_retention': ['Actual parent/payload/result/dossier/validations/output', 'Exact index2/sequence3',
                               'Expected post-state', 'Raw source additions/provenance', 'Policy/scope/lineage/generation', 'Root/head'],
        'required_bundle_identity': 'Actual planner-bundle-v1 canonical content identity; not computed until the supported full native event operand exists',
        'atomicity': 'Result/knowledge/Action completion/dossier/validations/event/source pins/post-bundle/append head are one semantic commit.',
        'writer_termination': 'Persist native head, terminate writer process, clear inherited objects; independent readers receive paths/IDs only.',
        'cold_restore': {'hash_seeds': [0, 1, 7, 101], 'readers_per_seed': 3, 'total_independent_readers': 12,
                         'oracles': 'Reconstruct full parent/result/ledger/post-state binding from durable bytes, not writer memory; compare exact primary identities.'},
        'replay': 'From exact sealed start prefix, reproduce the one historical dossier event, supplied result and recorded validation outcomes exactly once; no fresh validator decision and no A05/A06 execution.',
        'independent_reproductions': {'hash_seeds': [0, 1, 7, 101], 'writers_per_seed': 3, 'total': 12,
                                     'history_isolation': 'New distinct process/store/run provenance label for every reproduction; same sealed prospective lineage and semantic source identities; never append another A04 to the primary history.',
                                     'identity_policy': 'Equal semantic inputs may have equal content-addressed event IDs in distinct stores. Run identity is separate; never relabel any reproduction as the original historical occurrence.',
                                     'preparation': 'Load the exact two-event sealed start, not an already-completed A04 state.'},
        'determinism': {'seeds': [0, 1, 7, 101], 'unordered_presentations': ['original', 'reverse', 'rotate'],
                        'permitted': 'Only codec.SET_FIELDS collections: Snapshot actions/statuses/knowledge/validation_instances, dossier checks/alternatives/required_facts, SuppliedResult knowledge, PersistenceBundle sources.',
                        'ordered_fields': ['Event history/sequence/parent chain', 'Decision.history', 'ValidationInstance.inputs'],
                        'R05': 'Membership preserved; duplicates rejected where identifiers are unique. Do not change ordered ValidationInstance.inputs under the ValidationResult input-identity set rule.',
                        'compare': 'Canonical start/post identities, full typed payload, event and semantic Computation; no object/hash ordering dependence.'},
        'current_execution_status': 'NOT_RUN; durable operand adapter absent',
    }
    save('persistence-replay-contract.json', persistence)
    execution = {
        **LABELS, 'package': 'E2-P05-A04-PROSPECTIVE-ANCESTRY-QUALIFICATION-EXECUTION',
        'entry_gate': ['Contract PASS and EXECUTION_READY YES', 'Generic durable dossier adapter independently qualified',
                       'Exact retained start and all input/source/runtime pins', 'Scope decision subject match',
                       'No additional authority required', 'Complete native event wire identity oracle',
                       'N12/N13 mappings preserved; negative cases sealed'],
        'sequence': ['Load exact retained A03 post-bundle; read-only trust replay of existing prefix is allowed, but do not execute CHECK/COLLECT to manufacture a new start',
                     'Verify source/policy/context/selection/currentness and independent sealed inputs',
                     'Produce fresh bounded PREPARE result and independently evaluated typed validations',
                     'Run complete native preflight and compare immutable result/event/post-state oracles',
                     'Execute/admit PREPARE once using the qualified atomic durable operation',
                     'Capture actual event/payload/parent/pre-post/outputs/index/ledger; compare ancestry oracle',
                     'Persist exact post-A04 bundle; terminate writer; cold restore',
                     'Replay, independent reproductions, hash seeds/unordered presentations; run 24 negatives in isolation',
                     'Evaluate N12/N13 and historical labels; apply only authorized A04 END replacement mapping',
                     'Rerun binding frontier, record count and first missing stage; stop without P05/P06 execution'],
        'stop_on_divergence': ['FIRST_COUNTEREXAMPLE', 'EXPECTED', 'ACTUAL', 'STATE_ID', 'EVENT_ID', 'CLASSIFICATION'],
        'no_live_repair': True, 'no_new_contract_or_authority_at_execution': True,
        'permitted_configuration_installations': [],
        'currently_executable': False,
    }
    save('later-execution-contract.json', execution)
    readiness = {
        **LABELS, 'gates': {
            'scope_subject_authenticated': 'PASS', 'start_sealed': 'PASS', 'inputs_sealed': 'PASS',
            'authority_resolved': 'PASS', 'result_oracle_sealed': 'PASS',
            'native_event_payload_oracle_complete': 'FAIL', 'native_durable_event_path_qualified': 'FAIL',
            'ancestry_acceptance_rules_sealed': 'PASS', 'ordering_rules_sealed': 'PASS',
            'END_mapping_sealed': 'PASS', 'N12_mapping_preserved': 'PASS', 'N13_mapping_preserved': 'PASS',
            'persistence_replay_plan_sealed': 'PASS', 'negative_suite_sealed': 'PASS',
        }, 'FIRST_BLOCKER': 'NO_NATIVE_PERSISTED_DOSSIER_MATERIALIZATION_OPERAND_OR_EVENT_PATH',
        'exact_missing_term': 'ExecutionEvent.result cannot encode the existing T02 validation-instance tuple or enroll its source addition atomically; replay cannot reproduce the operation.',
        'start_identity_TBD_terms': [], 'new_operating_authority_required': False,
        'native_event_id_guessed': False, 'PROSPECTIVE_A04_EXECUTION_READY': 'NO',
        'PROSPECTIVE_A04_AUTHORITY_DECISION_REQUIRED': 'NO',
        'PROSPECTIVE_A04_AUTHORITY_DECISION_READY': 'NO',
        'PROSPECTIVE_A04_EXECUTED': 'NO', 'P05_BOUND_STAGE_INPUTS': 10,
        'P05_NEXT_MISSING_INPUT': 'E2-A04.prepare_result_event_ancestry', 'P05_EXECUTION_READY': 'NO',
        'NEXT_PACKAGE': 'GENERIC-NATIVE-PERSISTED-DOSSIER-MATERIALIZATION-INTEGRATION-CONTRACT-AND-QUALIFICATION',
        'next_package_is_separate': 'Selected scope excludes runtime repair/implementation. No such change is performed or silently authorized here.',
    }
    save('readiness.json', readiness)
    save('authoritative-inputs.json', {'pins': references, 'runtime_files':
        [pin(path) for path in sorted((ROOT / 'adapter/planner').glob('*.py'))]})
    save('contract-only-inspection.json', {
        **LABELS, 'canonical_start_identity': 'PASS', 'native_types': 'PASS',
        'retained_prefix_identity_parent_index': 'PASS', 'raw_source_policy_pins': 'PASS',
        'algebraic_expected_post_model_typing': 'PASS', 'full_positive_execution': 'NOT_RUN',
        'event_append_or_replay': 'NOT_RUN', 'native_Event_payload_available': False,
        'forbidden_calls': FORBIDDEN_CALLS, 'actual_results_or_events_created': 0,
    })
    assert not FORBIDDEN_CALLS
    preservation = {
        **LABELS, 'P01_P04': 'PASS', 'PROSPECTIVE_A04_EXECUTED': 'NO', 'P05_EXECUTED': 'NO',
        'P06_EXECUTED': 'NO', 'P05_BOUND_STAGE_INPUTS': 10,
        'ORIGINAL_A03_HISTORICAL_OCCURRENCE': 'UNPROVEN', 'P03_HISTORICAL_CORRESPONDENCE': 'UNPROVEN',
        'N_REAL_SATISFIED': 'NO', 'RUNTIME_MODIFIED': 'NO', 'E1_ARTIFACTS_MODIFIED': 0, 'PRODUCTION_EFFECT': 'NO',
    }
    evidence = {str(path.relative_to(OUT)): pin(path) for path in sorted(OUT.rglob('*.json'))
                if path.name not in ('baseline.json', 'verification.json')}
    evidence['seal_contract.py'] = pin(Path(__file__))
    report = {
        'schema': 'E2-P05-A04-PROSPECTIVE-ANCESTRY-CONTRACT-1',
        'WORK_PACKAGE': 'E2-P05-A04-PROSPECTIVE-ANCESTRY-CONTRACT', 'RESULT': 'PARTIAL',
        'SELECTED_OPTION': SELECTED, **preservation,
        'AUTHORITATIVE_QUALIFICATION_SCOPE_SUBJECT': subject_id,
        'A04_DEFINITION': native_definition, 'PROSPECTIVE_START': start_spec,
        'PROSPECTIVE_INPUTS': inputs, 'AUTHORITY': authority,
        'EXPECTED_RESULT_ORACLE': result_oracle,
        'EXPECTED_EVENT_ORACLE': event_oracle,
        'ANCESTRY_ORACLE': ancestry, 'ORDERING_ORACLE': ordering,
        'END_MAPPING': mapping, 'N12_MAPPING': n12, 'N13_MAPPING': n13,
        'PERSISTENCE_CONTRACT': persistence,
        'COLD_RESTORE_CONTRACT': persistence['cold_restore'], 'REPLAY_CONTRACT': persistence['replay'],
        'INDEPENDENT_REPRODUCTION_CONTRACT': persistence['independent_reproductions'],
        'DETERMINISM_CONTRACT': persistence['determinism'], 'NEGATIVE_SUITE': negative_specs,
        'NATIVE_INTERFACE_GAP': gap, 'READINESS_GATES': readiness,
        'ADDITIONAL_AUTHORITY_REQUIRED': 'NO',
        'PROSPECTIVE_A04_AUTHORITY_DECISION_REQUIRED': 'NO',
        'PROSPECTIVE_A04_AUTHORITY_DECISION_READY': 'NO', 'PROSPECTIVE_A04_EXECUTION_READY': 'NO',
        'N12_MAPPING_PRESERVED': 'YES', 'N13_MAPPING_PRESERVED': 'YES',
        'EVIDENCE': evidence,
        'NEXT_PACKAGE': readiness['NEXT_PACKAGE'],
        'verification_path': str((OUT / 'verification.json').relative_to(ROOT)),
    }
    report_path = PLANS / (REPORT_NAME + '.json')
    assert not report_path.exists()
    report_path.write_bytes((json.dumps(report, sort_keys=True, indent=2) + '\n').encode())
    print(json.dumps({'RESULT': report['RESULT'], 'START': observed,
        'EXPECTED_POST_STATE_ORACLE_ONLY': identity(after_id),
        'dossier_oracle_identity': identity(dossier_identity), 'negative_controls_sealed': len(negative_specs),
        'PROSPECTIVE_A04_EXECUTION_READY': 'NO', 'FORBIDDEN_CALLS': FORBIDDEN_CALLS}, sort_keys=True))


if __name__ == '__main__':
    main()
