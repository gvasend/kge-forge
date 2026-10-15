"""Recover native representation and write a versioned contract correction.

No execution, replay, durable publication, or runtime edit is available here.
The event value constructed below is an unadmitted representation oracle.
"""
import ast
import hashlib
import json
from dataclasses import fields, replace, MISSING
from pathlib import Path
from typing import get_args, get_type_hints

from adapter.planner import codec as c, core, gates, model as m

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
PLANS = ROOT / 'docs/plans'
PREFIX = 'DETERMINISTIC_PLANNER_V0_1_'
NAME = PREFIX + 'E2_P05_A04_EVENT_VALIDATION_RECONCILIATION_1'
OLD_NAME = PREFIX + 'E2_P05_A04_PROSPECTIVE_ANCESTRY_CONTRACT_1'
LABELS = {
    'QUALIFICATION_TYPE': 'PROSPECTIVE_REPLACEMENT',
    'ORIGINAL_A04_HISTORICAL_ANCESTRY': 'UNPROVEN',
    'ORIGINAL_A03_HISTORICAL_OCCURRENCE': 'UNPROVEN',
    'HISTORICAL_RECONSTRUCTION': 'NO',
    'PROSPECTIVE_A04_EVENT_IS_ORIGINAL_EVENT': 'NO',
}
BARRED = []


def canon(value):
    return c.canonical_bytes(value)


def text_id(value):
    return value.namespace + ':' + value.sha256


def pin(path, pointer=''):
    path = Path(path).resolve()
    return {'path': str(path.relative_to(ROOT)), 'pointer': pointer,
            'raw_sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def save(name, value):
    path = OUT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(value, sort_keys=True, indent=2) + '\n').encode()
    if path.exists() and path.read_bytes() != raw:
        raise AssertionError('output conflict: ' + name)
    path.write_bytes(raw)
    return pin(path)


def location(path, symbol):
    tree = ast.parse((ROOT / path).read_text())
    node = next(n for n in ast.walk(tree) if isinstance(n, (ast.ClassDef, ast.FunctionDef)) and n.name == symbol)
    return dict(pin(ROOT / path), symbol=symbol, line=node.lineno, end_line=node.end_lineno)


def schema(cls):
    hints = get_type_hints(cls)
    result = []
    for f in fields(cls):
        item = {'field': f.name, 'type': str(hints[f.name]), 'wire_optional_default': f.name in c.P03_FIELDS.get(cls, set())}
        if f.default is not MISSING:
            item['default'] = c._wire(f.default)
        result.append(item)
    return {'native_type': cls.__name__, 'fields': result,
            'unordered_fields': sorted(c.SET_FIELDS.get(cls, set())),
            'unknown_fields_rejected': True}


def guard():
    def forbidden(name):
        def reject(*args, **kwargs):
            BARRED.append(name)
            raise AssertionError('contract-only inspection: ' + name)
        return reject
    for module, names in (
        (core, ('recompute', 'apply_event', 'apply_result', '_inventory', '_decision_result',
                'admit_dossier_materialization', 'apply_recorded_decision', 'apply_decision_reentry')),
        (c, ('_replay', 'apply_event', 'record_result', 'append_event', 'commit_event', 'commit_result',
             'save_bundle', 'restore', 'bundle_bytes', 'bundle_id', '_publish_head', '_prefix_bundle')),
        (gates, ('decision_readiness', 'evaluate_predicate', '_evaluate_predicate')),
    ):
        for name in names:
            if hasattr(module, name):
                setattr(module, name, forbidden(module.__name__ + '.' + name))


def main():
    guard()
    old_path = PLANS / (OLD_NAME + '.json')
    old = json.loads(old_path.read_bytes())
    assert old['RESULT'] == 'PARTIAL' and old['PROSPECTIVE_A04_EXECUTION_READY'] == 'NO'
    assert old['PROSPECTIVE_A04_EXECUTED'] == 'NO' and old['P05_BOUND_STAGE_INPUTS'] == 10
    assert old['SELECTED_OPTION'] == 'AUTHORIZE_PROSPECTIVE_P05_A04_ANCESTRY_QUALIFICATION'
    for evidence in old['EVIDENCE'].values():
        assert pin(ROOT / evidence['path'])['raw_sha256'] == evidence['raw_sha256']
    expected = old['EXPECTED_RESULT_ORACLE']
    supplied = c._unwire(expected['expected_result'])
    after = c._unwire(expected['expected_post_state'])
    validations = c._unwire(expected['expected_validation_instances'])
    m.validate_types(supplied, m.SuppliedResult)
    m.validate_model(after)
    assert text_id(c.snapshot_id(after)) == expected['expected_post_state_id']
    start_path = ROOT / old['PROSPECTIVE_START']['START_PATH']['path']
    start = c._unwire(c.parse_json(start_path.read_bytes())['bundle'])
    assert c._bundle_bytes_admitted(start) == start_path.read_bytes()
    assert text_id(c._identity(start_path.read_bytes(), 'planner-bundle-v1')) == old['PROSPECTIVE_START']['START_BUNDLE_ID']
    assert len(start.events) == 2 and not start.current.validation_instances
    assert supplied.expected_snapshot == c.snapshot_id(start.current)
    dossier_id = c._identity(canon(c._wire(supplied.dossier)), 'planner-dossier-sha256')
    assert text_id(dossier_id) == expected['expected_dossier_id']
    assert tuple(after.validation_instances) == validations
    assert len(validations) == 6 and {v.proposition for v in validations} == {x.value for x in m.SUPPORTED_DOSSIER_CHECKS}
    for v in validations:
        assert v.dossier == dossier_id and v.inputs[0] == supplied.expected_snapshot
        assert v.inputs[1] == supplied.dossier.provenance.identity
    new_pin = c._unwire(old['EXPECTED_EVENT_ORACLE']['EVENT_PAYLOAD']['source_additions'][0])
    assert new_pin not in start.sources and hashlib.sha256((ROOT / new_pin.path).read_bytes()).hexdigest() == new_pin.identity.sha256
    sources = [pin(PLANS / (PREFIX + tail)) for tail in (
        'E2_P05_A04_PROSPECTIVE_ANCESTRY_CONTRACT_1.md', 'E2_P05_A04_PROSPECTIVE_ANCESTRY_CONTRACT_1.json',
        'E2_P05_A04_EVENT_ANCESTRY_RECOVERY_1.md', 'E2_P05_A04_EVENT_ANCESTRY_RECOVERY_1.json',
        'E2_P05_END_INPUT_BINDING_1.md', 'E2_P05_END_INPUT_BINDING_1.json',
        'E2_P05_A03_PROSPECTIVE_OCCURRENCE_RESULT_1.json',
        'E2_P05_A03_PROSPECTIVE_OCCURRENCE_BUNDLE_1.json',
        'CANONICAL_QUALIFICATION_EXPERIMENT_1.json', 'CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md',
        'E2_T02_RESULT.md', 'E2_T02_RESULT.json', 'E2_PC01_SOURCES.json')]
    binding_path = PLANS / 'qualification/E2_P05_END_INPUT_BINDING_1/input-oracle.json'
    binding = json.loads(binding_path.read_bytes())
    a04_binding = next(x for x in binding['required_stage_inputs'] if x['slot'] == 'E2-A04')
    assert a04_binding['EXPECTED_IDENTITY']['identity_domain'] == 'planner-event-v1'
    assert a04_binding['EXPECTED_IDENTITY']['no_surrogate'] == 'Snapshot/KnowledgeId/result label cannot replace an event identity'
    sources.append(pin(binding_path))
    current_binding = PLANS / 'qualification/E2_P05_A03_PROSPECTIVE_OCCURRENCE_EXECUTION_1/P05-binding-rerun.json'
    assert json.loads(current_binding.read_bytes())['P05_BOUND_STAGE_INPUTS'] == 10
    sources.append(pin(current_binding))
    sources += [pin(ROOT / p) for p in json.loads((OUT / 'baseline.json').read_bytes())['files'] if p.startswith('adapter/planner/')]
    scope_path = ROOT / old['AUTHORITY']['QUALIFICATION_SCOPE_AUTHORIZATION']['retained_dossier']['path']
    scope = json.loads(scope_path.read_bytes())
    assert 'qualification-scope-subject-v1:' + hashlib.sha256(canon(scope['subject'])).hexdigest() == old['AUTHORITATIVE_QUALIFICATION_SCOPE_SUBJECT']
    sources.append(pin(scope_path))
    save('source-pins.json', {'pins': sources})

    event_schema = dict(schema(m.ExecutionEvent),
        envelope_role='Existing native ExecutionEvent; no dedicated historical PREPARE tag',
        payload_field='result', A04_payload_branch='SuppliedResult',
        result_variants=[x.__name__ for x in get_args(get_type_hints(m.ExecutionEvent)['result'])],
        inline_validation_instances=False, dedicated_validation_reference_field=False,
        existing_transitive_reference='after_snapshot -> complete immutable Snapshot, including validation_instances',
        generic_reference_extension_allowed=False,
        extra_scope_lineage_command_or_validation_fields_allowed=False,
        reference_domains={'parent_snapshot': 'planner-snapshot-v1', 'parent_event': 'planner-event-v1',
                           'after_snapshot': 'planner-snapshot-v1', 'identity': 'planner-event-v1'})
    result_schema = dict(schema(m.SuppliedResult),
        result_meaning='Actual bounded producer outcome/knowledge and optional prepared dossier',
        standalone_ActionResult_entity_or_identity=False,
        direct_event_reference='ExecutionEvent.result stores the full typed SuppliedResult value, not a separate result ID',
        validations='ValidationInstances are a separate T02 argument; not fields of SuppliedResult or DecisionDossier',
        decision_checks='DecisionDossier.checks stores typed check metadata/PredicateId references, not the evaluated outcomes',
        dossier_validation_flag='Dossier currentness only; cannot substitute for the six independently evaluated records')
    validation_schema = dict(schema(m.ValidationInstance),
        native_storage='Snapshot.validation_instances: Tuple[ValidationInstance,...]',
        standalone_native_identity=False, GraphEntity=False,
        unique_native_selector='PredicateId is unique within a Snapshot; dossier ArtifactIdentity must also match',
        immutable_member_binding='(event.after_snapshot, ValidationInstance.predicate, ValidationInstance.dossier) plus full canonical native member value',
        record_currentness='Persisted ValidationOutcome/currentness/provenance, subject to native invalidation',
        computed_fields_not_serialized_as_instances=['Proof views returned by _evaluate_predicate', 'Readiness/Computation'],
        restore_validation_outcome='Retain original typed evaluation result; do not replace with a new independent validation decision')
    schemas = {'ExecutionEvent': event_schema, 'SuppliedResult': result_schema,
               'DecisionDossier': schema(m.DecisionDossier), 'DecisionCheck': schema(m.DecisionCheck),
               'ValidationInstance': validation_schema, 'PersistenceBundle': schema(m.PersistenceBundle),
               'locations': [location('adapter/planner/model.py', x) for x in
                             ('ExecutionEvent', 'SuppliedResult', 'DecisionDossier', 'DecisionCheck', 'ValidationInstance', 'Snapshot', 'PersistenceBundle')],
               'codec_locations': [location('adapter/planner/codec.py', x) for x in ('_wire', '_unwire', 'snapshot_id', '_event_identity')]}
    save('native-schemas.json', schemas)

    inventory = []
    rules = old['PROSPECTIVE_INPUTS']
    for i, v in enumerate(validations):
        rule = next(x for x in rules if x['INPUT_ID'] == 'VALIDATOR-RULE-' + v.proposition)
        locator = {'snapshot': c._wire(c.snapshot_id(after)), 'predicate': c._wire(v.predicate), 'dossier': c._wire(v.dossier)}
        inventory.append({
            'VALIDATION_ID': v.predicate.value,
            'VALIDATION_ID_DOMAIN': 'Native PredicateId selector, not a standalone ValidationInstance content ID',
            'TYPE': 'ValidationInstance', 'SUBJECT': text_id(v.dossier), 'PROPOSITION': v.proposition,
            'VALUE': {'result': v.result.value, 'currentness': v.currentness.value},
            'SOURCE': rule['SOURCE'], 'PROVENANCE': c._wire(v.provenance),
            'INPUTS': c._wire(v.inputs), 'SCOPE': v.scope, 'LINEAGE': v.lineage,
            'GENERATION_BINDING': 'Snapshot.context and exact pre-state identity; ValidationInstance has no generation field',
            'CONSUMER': 'gates._evaluate_predicate -> decision_readiness -> T02 admission/Planner Computation',
            'WHY_REQUIRED': rule['CANONICAL_CONTENT'],
            'CURRENT_PROPOSED_EVENT_FIELD': 'Old required-event-operands.validation_instances[%d]; descriptor only, not an existing native event field' % i,
            'CURRENT_NATIVE_STATE_FIELD': 'Snapshot.validation_instances member selected by this PredicateId',
            'REPRESENTATION_CLASSIFICATION': 'SEPARATE_NATIVE_ENTITY',
            'classification_note': 'Requested storage-category label: separately typed state record, not GraphEntity/EntityId or separately indexed object',
            'IMMUTABLE_MEMBER_BINDING': locator,
            'EXPECTED_NATIVE_VALUE': c._wire(v), 'ACTUAL_INSTANCE_ADMITTED': False,
            'live_validator_recomputation_required_on_restore': False,
        })
    save('dossier-validation-inventory.json', {'role': 'EXPECTED_INPUT_RESULT_INVENTORY_NOT_ADMITTED', **LABELS,
        'validations': inventory, 'required_instance_count': 6,
        'separate_fact_predicates': ['E2-KP-CHECK', 'E2-KP-COLLECT'],
        'descriptive_checks_not_validation_instances': ['ASSUMPTIONS_CONSEQUENCES', 'DOWNSTREAM_QUALIFICATION', 'NO_INVENTED_FACTS']})

    # The native envelope can express the existing result + immutable after
    # Snapshot. This proves representation, never successful admission.
    event_id = c._event_identity(3, supplied.expected_snapshot, start.events[-1].identity, supplied, c.snapshot_id(after))
    event = m.ExecutionEvent(3, supplied.expected_snapshot, start.events[-1].identity,
                             supplied, c.snapshot_id(after), event_id)
    m.validate_types(event, m.ExecutionEvent)
    assert canon(c._wire(c._unwire(c._wire(event)))) == canon(c._wire(event))
    representation_oracle = {
        **LABELS, 'role': 'COMPARISON_ONLY_NATIVE_EVENT_VALUE_NOT_ADMITTED_NOT_ENROLLED',
        'native_event': c._wire(event), 'EXPECTED_REPRESENTATIONAL_EVENT_ID': text_id(event_id),
        'after_snapshot': text_id(event.after_snapshot),
        'after_snapshot_source': pin(PLANS / (OLD_NAME + '.json'), '/EXPECTED_RESULT_ORACLE/expected_post_state'),
        'after_snapshot_is_occurred_state': False,
        'typed_members': [x['IMMUTABLE_MEMBER_BINDING'] for x in inventory],
        'source_addition': c._wire(new_pin),
        'native_serialization_round_trip': 'PASS', 'native_admission_preflight': 'NOT_RUN_NOT_SUPPORTED',
        'event_appended': False, 'snapshot_or_event_file_saved_as_native_store_artifact': False,
        'oracle_excluded_from_execution_inputs': True,
    }
    save('oracles/composite-representation.json', representation_oracle)
    correlation = {
        **LABELS, 'representation': 'ExecutionEvent + inline SuppliedResult/dossier + immutable post-Snapshot ValidationInstances + source-pinned PersistenceBundle',
        'A_inline_values_required_by_P05': 'NO',
        'B_dedicated_validation_object_refs_already_native': 'NO; no standalone ValidationInstance ID or validation-ref field',
        'B_transitive_snapshot_reference_already_native': 'YES; after_snapshot binds all typed Snapshot members',
        'C_transaction_atomicity_required': 'YES',
        'C_complete_A04_durable_transaction_already_native': 'NO',
        'D_exact_native_composite_representation': 'YES; existing types suffice for value/hash representation, not current operation/replay admission',
        'event_result': 'event.result is full SuppliedResult; Action/outcome/knowledge/dossier are inside its native canonical body',
        'result_dossier_identity': text_id(dossier_id),
        'post_state_identity': text_id(event.after_snapshot),
        'post_state_members': 'Hash exact PLANNER-SNAPSHOT-1 bytes, then select unique typed members by PredicateId; each must bind the same dossier/body and exact input state/source.',
        'no_report_pointer_as_identity': True, 'new_validation_identity_namespace': False,
        'native_command_id': 'NONE for ordinary SuppliedResult; HEAD.command=None. No required command identity is invented.',
        'parent_correlation': {'event.parent_snapshot': text_id(event.parent_snapshot),
                               'result.expected_snapshot': text_id(supplied.expected_snapshot),
                               'event.parent_event': text_id(event.parent_event)},
        'generation_scope_lineage': 'Verify immutable pre/post Snapshot.context and each validation scope/lineage; source/provenance binds same experiment.',
        'bundle_and_HEAD': 'Trusted post-bundle identity binds initial/events/current/source index/policy. Native HEAD.previous binds exact prior bundle; enrollment/sequence/parent links required separately.',
        'support_provenance': 'Keep complete typed record provenance and exact raw source pins; an unchecked path or a report label is insufficient.',
        'lossless_membership': 'Given verified post-Snapshot bytes, every ValidationInstance field is retained and recoverable; it is not inferred from readiness or status.',
        'actual_A04_transaction_available': False,
    }
    save('native-correlation.json', correlation)
    terms = [
        ('event occurrence', 'Actual native ExecutionEvent, enrolled once in the exact continued ledger', 'Event + ledger', True),
        ('payload/result', 'Existing full SuppliedResult/action/PASS/knowledge/dossier in ExecutionEvent.result', 'Inline result value', True),
        ('parent/pre-state', 'parent_event and parent_snapshot; result.expected_snapshot; enrolled predecessor continuity', 'Event identity fields + native predecessor', True),
        ('ledger position', 'sequence3/index2 and exact CHECK->COLLECT->PREPARE membership; root/head', 'Event sequence + bundle.events', True),
        ('typed validation outcomes', 'Six exact typed Snapshot records linked by after_snapshot and dossier/predicate/input binding', 'Separate native Snapshot state', False),
        ('output', 'Exact E2-K-PREPARE in actual result and post-Snapshot knowledge; producer/provenance equality', 'Inline result plus separate typed KnowledgeRecord state', True),
        ('post-state', 'after_snapshot equals recomputed/verified canonical native Snapshot identity', 'Event identity reference + full native Snapshot', True),
        ('source/provenance', 'Exact record values and source pins, with source enrollment at same semantic transaction', 'Native result/state provenance + bundle.sources', False),
        ('control/readiness', 'DECISION_READY/HUMAN_HANDOFF recomputed over admitted typed inputs', 'Computed read-only oracle', False),
    ]
    assurance = {
        **LABELS, 'P05_input': a04_binding, 'terms': [
            {'term': t, 'minimum_witness': w, 'native_location': loc, 'event_field_required': inline,
             'assurance_preserved': True} for t, w, loc, inline in terms],
        'no_inline_validation_mandate_in_authoritative_plan_matrix_or_P05': True,
        'event_ancestry_requirement_retained': True, 'state_only_evidence_accepted': False,
        'actual_occurrence_and_transaction_commit_still_required': True,
        'historical_scope': 'Original A04 ancestry remains UNPROVEN. A future admitted composite may close only the authorized prospective A04 replacement term.',
        'END_representation': 'Read-only experiment acceptance witness graph, not a native aggregate Action',
        'N12': {'mapping': 'PRESERVED', 'original': 'Selection/history cannot fabricate completion/knowledge/event',
                'composite': 'Require actual supplied result + native admitted event + enrolled parent/ledger + complete typed post-state; selection alone has none of these',
                'runtime_negative_qualification': 'NOT_RUN'},
        'N13': {'mapping': 'PRESERVED', 'original': 'Output declaration is not an actual result',
                'composite': 'Require fresh actual producer result and independently evaluated validations admitted in the native transaction; declaration/oracle/snapshot alone cannot establish occurrence',
                'runtime_negative_qualification': 'NOT_RUN'},
        'old_24_negative_controls': 'Unchanged; event payload tampering means actual supported payload/reference/body association tampering, not absence of a nonexistent inline field',
        'P05_BOUND_STAGE_INPUTS': 10, 'binding_closed_here': False,
    }
    save('P05-N12-N13-assurance.json', assurance)
    transaction = {
        'state_atomicity_supported': 'T02 returns one immutable TransitionReport only after accepted result/dossier/six checks; failure has no partial returned state',
        'state_effects': ['PREPARE completion', 'E2-K-PREPARE knowledge', 'Action.prepared_dossier',
                          'Decision.dossier/history/readiness', 'Snapshot.validation_instances'],
        'existing_durable_boundary': 'codec.commit_event takes trusted current head under local lock, record_result/apply_event computes post-state, save_bundle validates/replays and writes immutable event/bundle artifacts, then _publish_head atomically replaces HEAD',
        'one_payload_requirement': False,
        'durable_visibility': 'Canonical transaction is published at trusted HEAD, not at first immutable file write; crash-created orphan files do not establish acceptance',
        'A04_integration_gap': 'No event dispatcher calls T02 with its validation tuple. SuppliedResult has no such operand. Current replay reads only event.result, not post/current state as historical operand.',
        'ordinary_path_fails_for_sealed_start': 'Action.prepared_dossier=None; ordinary validate_result compares supplied dossier with None. It also cannot introduce independent typed instances through the result field.',
        'source_gap': 'Sealed new dossier source is offline. Per-event source-addition/prefix/retry handling recognizes other typed admissions, not T02 materialization.',
        'replay_gap': 'PersistenceBundle retains initial/events/current, not a separately addressable after-Snapshot object per event. Event.after_snapshot is a hash, not an object lookup implementation. Current _replay requires apply_event to regenerate each exact after_snapshot.',
        'HEAD_correlation_gap': 'Existing SuppliedResult HEAD.command=None and _prefix_bundle replays only supported event results; a report transaction ID cannot supply missing historical operands.',
        'other_native_validation_transaction': 'ValidationSupportAdmission is specialized to Evidence/receipt/validation-contract/support A10. It has typed outcomes and command identity but does not implement dossier/check admission; reuse as A04 would change semantics.',
        'T02_report_limit': 'T02 runtime_transaction.atomic=true and encode_decode replay PASS refer to state materialization/typed Snapshot retention. No append-only parallel store is claimed; this does not establish complete event-bearing transaction replay.',
        'implementation_qualified_for_A04_durable_transaction': False,
        'locations': [],
    }
    # Build location lists separately so Python 3.8 accepts the expression.
    transaction['locations'] = [location('adapter/planner/core.py', 'admit_dossier_materialization'),
        location('adapter/planner/core.py', 'apply_event'), location('adapter/planner/gates.py', 'validate_result')]
    transaction['locations'] += [location('adapter/planner/codec.py', name) for name in
        ('_replay', 'record_result', 'save_bundle', 'restore', '_publish_head', '_read_head', 'commit_event', '_prefix_bundle')]
    transaction['locations'] += [location('adapter/planner/validation_transaction.py', name) for name in ('apply', 'commit')]
    save('transaction-and-replay-gap.json', transaction)
    capability = {
        'required': True, 'operation': 'GENERIC_PERSISTED_DOSSIER_MATERIALIZATION',
        'semantic_input_contract': ['Trusted exact pre-bundle/state/head/context', 'Actual bounded SuppliedResult including dossier',
                                    'Six independently evaluated typed ValidationInstances with exact subject/input/source/currentness',
                                    'Sealed raw source additions and provenance'],
        'unchanged_semantics': 'Invoke existing T02 admission for selected decision-input Action; no validation Boolean, new authority, human choice or extra Action execution.',
        'identity_contract': 'Native event identity binds supported full result plus immutable before/after Snapshot identities and parent/sequence. Exact ValidationInstance values must be reachable under after_snapshot and subject/input native bindings.',
        'durable_contract': 'Atomically publish complete native event/result/output/dossier/validation state/source pins/post-bundle under the trusted current HEAD. No partial accepted occurrence or validation set can be exposed as P05 occurrence evidence.',
        'replay_operand_contract': 'Retain all original typed evaluation outcomes in a deterministically recoverable native representation for each historical materialization. Resolve content by immutable native identity, verify subject/parent/pre-state/input/source, and reproduce exact T02 state effects. Never use latest mutable state or writer memory as historical operand.',
        'serialization_constraint': 'An inline typed materialization operand is one possible future implementation; a lossless native detached/reference operand is another only with an explicit codec/archive resolver contract. Neither is currently registered for A04. No storage layout is invented or implemented here.',
        'source_contract': 'Bind new raw source pins at the same historical event boundary, preserve exact prefix-source inventory, and verify ValidationInstance/dossier provenance on cold restore/replay.',
        'preflight_execution_equivalence': 'Same canonical result, tuple and source content validated and consumed; no substitution between stages.',
        'failure_atomicity': ['No successful event with missing/failed/misbound validation', 'No completed PREPARE/knowledge/dossier without its required occurrence event',
                              'No validation tuple treated as proof of occurrence on its own', 'No head advancement or partial provenance on failure'],
        'idempotence': 'Same admitted semantic operation must preserve exactly one event/state effect; conflicting result/tuple/content or stale parent fails closed. Existing state-level T02 no-op does not establish durable exactly-once behavior.',
        'required_qualification': ['Complete native operation/replay representation contract before implementation',
                                   'Positive state+event+ledger/source correlation', 'Old 24 negatives',
                                   'Failure injection before native HEAD publication', 'Idempotence/conflict',
                                   'Cold readers/replay from exact retained start', 'Historical detached operand retention if chosen',
                                   'Seeds0,1,7,101 and native unordered presentations'],
        'complete_native_operation_contract_already_established': False,
        'implementation_in_this_package': False,
    }
    save('minimum-generic-capability.json', capability)
    revision = {
        **LABELS, 'base_contract': pin(old_path), 'base_markdown': pin(PLANS / (OLD_NAME + '.md')),
        'revision_type': 'VERSIONED_REPRESENTATION_AND_ORACLE_OVERLAY',
        'prior_sealed_files_modified': False, 'CONTRACT_REVISION_REQUIRED': 'YES',
        'CONTRACT_REVISION_APPLIED': 'YES_AS_THIS_OVERLAY',
        'revised_requirement': 'Remove mandatory inline validation_instances/source_additions in the A04 event payload. Require native typed values and source pins to be atomically admitted and immutably correlated through event/result/dossier/post-Snapshot/bundle/parent/ledger.',
        'superseded_terms': ['Old required-event-operands as a mandatory serialized event.result shape',
                             'Event identity unavailability solely because validation values are not inline',
                             'Missing validation-reference field alone as an execution blocker'],
        'preserved_terms': ['Exact human scope subject', 'Exact start/native Action/inputs/source content',
                            'Exact bounded result and validation values', 'Exact post-state/dossier identities',
                            '24 negative assurance expectations', 'Parent/index/root/head rules',
                            'Original historical UNPROVEN labels', 'A04-only END replacement mapping',
                            'N12/N13, persistence/replay/determinism requirements', 'No runtime or A04 execution'],
        'replacement_event_representation_oracle': pin(OUT / 'oracles/composite-representation.json'),
        'PROSPECTIVE_A04_EXECUTION_READY': 'NO',
        'remaining_blocker': 'Missing durable T02 materialization/ledger/source enrollment and historical replay operand integration, not inability to serialize typed Snapshot members',
    }
    save('contract-revision-overlay.json', revision)

    probes = []
    for mode in ('original', 'reverse', 'rotate'):
        vals = validations if mode == 'original' else validations[::-1] if mode == 'reverse' else validations[1:] + validations[:1]
        alternate = replace(after, validation_instances=vals)
        assert c.snapshot_id(alternate) == c.snapshot_id(after)
        assert c._event_identity(3, event.parent_snapshot, event.parent_event, supplied, c.snapshot_id(alternate)) == event.identity
        probes.append({'probe': 'unordered_validation_membership_' + mode, 'result': 'PASS', 'event_id': text_id(event.identity)})
    changed_v = replace(validations[0], provenance=replace(validations[0].provenance, section='/different-source-section'))
    altered = replace(after, validation_instances=(changed_v,) + validations[1:])
    assert c.snapshot_id(altered) != event.after_snapshot
    assert c._event_identity(3, event.parent_snapshot, event.parent_event, supplied, c.snapshot_id(altered)) != event.identity
    probes.append({'probe': 'changed_typed_validation_changes_Snapshot_and_event_binding', 'result': 'PASS'})
    duplicate = replace(after, validation_instances=validations + (validations[0],))
    try:
        m.validate_model(duplicate)
    except m.PlannerError as exc:
        assert str(exc) == 'duplicate identifier'
        probes.append({'probe': 'duplicate_native_validation_selector_rejected', 'result': 'PASS', 'reason': str(exc)})
    else:
        raise AssertionError('duplicate native validation accepted')
    unsupported_wire = c._wire(supplied)
    unsupported_wire['validation_instances'] = c._wire(validations)
    try:
        c._unwire(unsupported_wire)
    except m.PlannerError as exc:
        probes.append({'probe': 'adding_inline_validation_field_to_SuppliedResult_rejected', 'result': 'PASS', 'reason': str(exc)})
    else:
        raise AssertionError('event schema extended unexpectedly')
    save('static-representation-probes.json', {'role': 'STRUCTURAL_HASH_PROBES_NOT_A04_EXECUTION', **LABELS,
        'probes': probes, 'forbidden_calls': BARRED, 'event_admission_replay_or_transaction_run': False})
    assert not BARRED
    report = {
        'schema': 'E2-P05-A04-EVENT-VALIDATION-RECONCILIATION-1',
        'WORK_PACKAGE': 'E2-P05-A04-EVENT-VALIDATION-RECONCILIATION', 'RESULT': 'PASS', **LABELS,
        'SELECTED_OPTION': old['SELECTED_OPTION'], 'AUTHORIZATION_SUBJECT': old['AUTHORITATIVE_QUALIFICATION_SCOPE_SUBJECT'],
        'DOSSIER_VALIDATIONS': inventory, 'NATIVE_EVENT_SCHEMA': event_schema,
        'NATIVE_RESULT_SCHEMA': result_schema, 'NATIVE_VALIDATION_REPRESENTATION': validation_schema,
        'TRANSACTION_BOUNDARY': transaction, 'ATOMICITY_MODEL': 'SINGLE_SEMANTIC_COMMIT_OF_EVENT_PLUS_TYPED_STATE_AND_SOURCE_PINS_NOT_ONE_REQUIRED_PAYLOAD',
        'EVENT_REQUIRED_FIELDS': [f.name for f in fields(m.ExecutionEvent) if f.name != 'resume_binding'],
        'SEPARATELY_BOUND_FIELDS': ['Snapshot.validation_instances', 'Snapshot.actions[].prepared_dossier',
                                  'Snapshot.decisions[].dossier/history', 'Snapshot.knowledge', 'Snapshot.context',
                                  'PersistenceBundle.sources/policy/current/events'],
        'COMPUTED_FIELDS': ['Proof views for fact/check predicates', 'DecisionReadiness', 'Planner Computation/selection/control'],
        'NATIVE_CORRELATION': correlation, 'REPLAY_CORRELATION': transaction['replay_gap'],
        'P05_ANCESTRY_ASSURANCE': assurance, 'N12_MAPPING': assurance['N12'], 'N13_MAPPING': assurance['N13'],
        'PRIMARY_CLASSIFICATION': 'COMBINED',
        'CLASSIFICATION_COMPONENTS': ['DOSSIER_OVERCONSTRAINED_EVENT_PAYLOAD', 'MISSING_ATOMIC_TRANSACTION_CAPABILITY'],
        'NOT_ESTABLISHED': ['EVENT_SCHEMA_DEFECT', 'MISSING_TYPED_REFERENCE_CAPABILITY', 'ACCEPTANCE_CONTRACT_INCOMPLETE'],
        'MINIMUM_CORRECTION': {'contract': revision, 'generic_capability': capability},
        'CONTRACT_REVISION_REQUIRED': 'YES', 'CONTRACT_REVISION_APPLIED': 'YES_AS_VERSIONED_OVERLAY',
        'RUNTIME_CAPABILITY_REQUIRED': 'YES', 'RUNTIME_IMPLEMENTATION_PERFORMED': 'NO',
        'PROSPECTIVE_A04_EXECUTION_READY': 'NO', 'FIRST_REMAINING_BLOCKER': 'GENERIC_DURABLE_DOSSIER_MATERIALIZATION_AND_HISTORICAL_REPLAY_OPERAND_INTEGRATION',
        'EXPECTED_REPRESENTATIONAL_EVENT_ID': text_id(event.identity), 'EXPECTED_EVENT_IS_OCCURRED': False,
        'A04_EXECUTED': 'NO', 'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO', 'P05_BOUND_STAGE_INPUTS': 10,
        'P05_NEXT_MISSING_INPUT': 'E2-A04.prepare_result_event_ancestry', 'P05_EXECUTION_READY': 'NO',
        'P03_HISTORICAL_CORRESPONDENCE': 'UNPROVEN', 'N_REAL_SATISFIED': 'NO',
        'RUNTIME_MODIFIED': 'NO', 'E1_ARTIFACTS_MODIFIED': 0, 'PRODUCTION_EFFECT': 'NO',
        'NEXT_PACKAGE': 'GENERIC-PERSISTED-DOSSIER-MATERIALIZATION-TRANSACTION-CONTRACT',
        'evidence': {str(p.relative_to(OUT)): pin(p) for p in sorted(OUT.rglob('*.json')) if p.name != 'baseline.json'},
        'verification_path': str((OUT / 'verification.json').relative_to(ROOT)),
    }
    report['evidence']['reconcile.py'] = pin(Path(__file__))
    target = PLANS / (NAME + '.json')
    assert not target.exists()
    target.write_text(json.dumps(report, sort_keys=True, indent=2) + '\n')
    print(json.dumps({'RESULT': report['RESULT'], 'PRIMARY_CLASSIFICATION': 'COMBINED',
        'EXPECTED_REPRESENTATIONAL_EVENT_ID': text_id(event.identity),
        'PROSPECTIVE_A04_EXECUTION_READY': 'NO', 'A04_EXECUTED': 'NO', 'FORBIDDEN_CALLS': BARRED}, sort_keys=True))


if __name__ == '__main__':
    main()
