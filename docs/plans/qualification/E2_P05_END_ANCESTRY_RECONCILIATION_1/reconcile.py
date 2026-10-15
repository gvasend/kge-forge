"""Read-only END assurance recovery and proposed qualification mapping.

No Planner transition, native replay, new grant, or P05 execution is allowed.
Only existing native bytes, immutable identities and qualified scope records
are read. New JSON is documentary qualification evidence, not Planner state.
"""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path

from adapter.planner import codec as c, core, model as m

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
DOCS = ROOT / 'docs/plans'
PREFIX = 'DETERMINISTIC_PLANNER_V0_1_'
CURRENT = ROOT / 'docs/plans/qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_EXECUTION_1/P05-binding-rerun.json'
SOURCE_DIR = ROOT / 'docs/plans/qualification/E2_P05_END_INPUT_BINDING_1'
CALLS = []
REFRESH_OWN_DRAFT = False


def deny(name):
    def blocked(*args, **kwargs):
        CALLS.append(name)
        raise AssertionError('Reconciliation cannot execute ' + name)
    return blocked


for module, names in (
    (core, ('apply_receipt', 'apply_event', 'apply_result', 'recompute', 'resume_eligibility',
            '_inventory', 'apply_recorded_decision', 'apply_decision_reentry', 'admit_dossier_materialization')),
    (c, ('apply_event', '_replay', '_prefix_bundle', 'record_result', 'append_event',
         'commit_event', 'commit_result', 'save_bundle', 'restore', 'decode_bundle',
         'bundle_id', 'bundle_bytes', '_publish_head', 'admit_external_evidence'))):
    for symbol in names:
        setattr(module, symbol, deny(module.__name__ + '.' + symbol))


def read(path):
    return json.loads(Path(path).read_bytes())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ref(path, pointer='', line=None):
    path = Path(path)
    if not path.is_absolute():
        path = ROOT / path
    value = {'path': str(path.relative_to(ROOT)), 'pointer': pointer, 'raw_sha256': sha(path)}
    if line is not None:
        value['line'] = line
    return value


def aid(value):
    return None if value is None else value.namespace + ':' + value.sha256


def qid(namespace, value):
    return namespace + ':' + hashlib.sha256(c.canonical_bytes(value)).hexdigest()


def save(path, value):
    raw = (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + '\n').encode()
    if path.exists():
        if path.read_bytes() != raw:
            assert REFRESH_OWN_DRAFT and OUT in path.parents and path.name != 'baseline.json', 'Refuse to change an authoritative input'
            path.write_bytes(raw)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)


def pointers(value, path):
    for part in path.split('/')[1:]:
        part = part.replace('~1', '/').replace('~0', '~')
        value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def pins(value):
    if isinstance(value, dict):
        if 'path' in value and 'raw_sha256' in value:
            yield value
        for child in value.values():
            yield from pins(child)
    elif isinstance(value, list):
        for child in value:
            yield from pins(child)


def check_pins(value):
    checked = set()
    for item in pins(value):
        path = ROOT / item['path']
        assert sha(path) == item['raw_sha256'], item['path']
        if item.get('pointer') and path.suffix == '.json':
            pointers(read(path), item['pointer'])
        checked.add(item['path'])
    return checked


def bundle(path):
    raw = path.read_bytes()
    obj = read(path)
    native = c._unwire(obj['bundle'])
    m.validate_types(native, m.PersistenceBundle)
    assert raw == c._bundle_bytes_admitted(native)
    c._verify_sources(native, ROOT)
    c._check_snapshot_pins(native.initial, native.sources)
    c._check_snapshot_pins(native.current, native.sources)
    previous = None
    state = c.snapshot_id(native.initial)
    events = []
    for index, event in enumerate(native.events):
        assert event.sequence == index + 1 and event.parent_event == previous
        assert event.parent_snapshot == state
        assert event.identity == c._event_identity(event.sequence, event.parent_snapshot,
            event.parent_event, event.result, event.after_snapshot, event.resume_binding)
        if hasattr(event.result, 'expected_snapshot'):
            assert event.result.expected_snapshot == event.parent_snapshot
        # The native immutable event body is retained independently of its report.
        event_path = path.parent / ('event-' + event.identity.sha256 + '.json')
        assert event_path.read_bytes() == c.canonical_bytes(c._wire(event))
        events.append({'identity': aid(event.identity), 'type': type(event.result).__name__,
            'result': c._wire(event.result), 'parent': aid(event.parent_event),
            'pre_snapshot': aid(event.parent_snapshot), 'post_snapshot': aid(event.after_snapshot),
            'index': index, 'sequence': event.sequence, 'native_event': ref(event_path),
            'bundle_selector': ref(path, '/bundle/events/' + str(index))})
        previous, state = event.identity, event.after_snapshot
    assert state == c.snapshot_id(native.current)
    return native, {'source': ref(path), 'bundle_id': aid(c._identity(raw, 'planner-bundle-v1')),
        'initial_snapshot': aid(c.snapshot_id(native.initial)), 'current_snapshot': aid(c.snapshot_id(native.current)),
        'context': c._wire(native.current.context), 'events': events,
        'root': events[0]['identity'] if events else None,
        'head': events[-1]['identity'] if events else None,
        'initial_completed_actions': [s.id.value for s in native.initial.statuses if s.state is m.ActionState.COMPLETED],
        'native_ledger_coordinate': aid(c._identity(raw, 'planner-bundle-v1')) + '#/bundle/events',
        'source_policy_pins': c._wire(native.sources + (native.policy,)),
        'qualification_replay_not_executed_here': True}


def build():
    plan_path = DOCS / (PREFIX + 'CANONICAL_QUALIFICATION_EXPERIMENT_1.json')
    plan = read(plan_path)
    case = {row['CASE_ID']: row for row in plan['cases']}
    current = read(CURRENT)
    assert current['P05_BOUND_STAGE_INPUTS'] == current['P05_REQUIRED_STAGE_INPUTS'] == 13
    assert all(row['binding_status'] == 'BOUND' for row in current['stage_bindings'])
    original = read(SOURCE_DIR / 'canonical-bindings.json')
    old_rows = {row['STEP_ID']: row for row in original['stage_bindings']}
    check_pins(current)
    check_pins(original)
    sources = {
        'plan': ref(DOCS / (PREFIX + 'CANONICAL_QUALIFICATION_EXPERIMENT_1.md'), line=30),
        'plan_END': ref(plan_path, '/cases/33'),
        'matrix_END': ref(DOCS / (PREFIX + 'CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md'), line=467),
        'matrix_N12': ref(DOCS / (PREFIX + 'CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md'), line=383),
        'matrix_N13': ref(DOCS / (PREFIX + 'CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md'), line=397),
        'current_stage_bindings': ref(CURRENT),
        'P05_readiness': ref(ROOT / 'docs/plans/qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_EXECUTION_1/P05-complete-readiness-result.json'),
        'END_interface': ref(DOCS / (PREFIX + 'E2_PC04_END.json')),
        'old_DAG': ref(SOURCE_DIR / 'dependency-DAG.json'),
        'old_END_contract': ref(SOURCE_DIR / 'END-contract.json'),
    }
    native_paths = {
        'A03': DOCS / (PREFIX + 'E2_P05_A03_PROSPECTIVE_OCCURRENCE_BUNDLE_1.json'),
        'A04': DOCS / (PREFIX + 'E2_P05_A04_PROSPECTIVE_ANCESTRY_BUNDLE_1.json'),
        'P03': DOCS / (PREFIX + 'P03_PROSPECTIVE_CHECKPOINT_BUNDLE_1.json'),
        'A06': DOCS / (PREFIX + 'E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_BUNDLE_1.json'),
        'P04': DOCS / (PREFIX + 'E2_P04_CANONICAL_TARGET_BUNDLE_1.json'),
    }
    natives, ledgers = {}, {}
    for role, path in native_paths.items():
        natives[role], ledgers[role] = bundle(path)
    # Actual overlaps are retained. Role names cannot invent distinct physical
    # lineage IDs, nor can matching names invent parent relationships.
    assert natives['A04'].initial == natives['A03'].initial
    assert natives['A04'].events[:2] == natives['A03'].events
    assert natives['A04'].events[2].parent_event == natives['A03'].events[-1].identity
    assert natives['A04'].events[2].parent_snapshot == c.snapshot_id(natives['A03'].current)
    assert natives['P04'].initial == natives['P03'].initial
    assert natives['P04'].events[:2] == natives['P03'].events
    assert natives['P04'].events[2].parent_event == natives['P03'].events[-1].identity
    assert ledgers['A06']['initial_snapshot'] != ledgers['P03']['current_snapshot']
    assert ledgers['A04']['current_snapshot'] != ledgers['P03']['initial_snapshot']
    assert natives['A06'].current.context.lineage != natives['P04'].current.context.lineage

    results, mappings = {}, {}
    for number, suffix in ((3, 'PROSPECTIVE_OCCURRENCE'), (4, 'PROSPECTIVE_ANCESTRY'),
                           (5, 'ALTERNATE_NATIVE_EVIDENCE'), (6, 'PROSPECTIVE_REQUEST_WAIT')):
        path = DOCS / (PREFIX + 'E2_P05_A%02d_%s_RESULT_1.json' % (number, suffix))
        result = read(path)
        assert result['RESULT'] == 'PASS'
        check_pins(result.get('evidence', {}))
        results[number] = ref(path)
    mappings[3] = ref(ROOT / 'docs/plans/qualification/E2_P05_A03_PROSPECTIVE_OCCURRENCE_CONTRACT_1/END-acceptance-mapping.json')
    mappings[4] = ref(ROOT / current['stage_bindings'][3]['sealed_mapping']['path'])
    mappings[5] = ref(ROOT / current['stage_bindings'][4]['sealed_mapping']['path'])
    mappings[6] = ref(ROOT / 'docs/plans/qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_EXECUTION_1/END-N12-N13-mapping-result.json')
    sources['P03_scope_dossier'] = ref(DOCS / (PREFIX + 'P03_CHECKPOINT_SCOPE_DECISION_DOSSIER_1.json'))
    sources['P03_qualified_result'] = ref(DOCS / (PREFIX + 'P03_PROSPECTIVE_CHECKPOINT_QUALIFICATION_1.json'))
    sources['P03_semantic_contract'] = ref(ROOT / 'docs/plans/qualification/P03_PROSPECTIVE_CHECKPOINT_1/sources/qualification-contract.json')
    scopes = []
    for number in (3, 4, 5, 6):
        row = current['stage_bindings'][number - 1]
        scopes.append({'name': 'A%02d' % number, 'decision': row['governing_decision'],
            'qualified_result': results[number], 'qualified_mapping': mappings[number],
            'applies_to': row['logical_required_input'], 'local_result': 'PASS',
            'aggregate_END_acceptance_authorized': False, 'historical_identity_replacement': False,
            'limitation': 'Named stage replacement only; original full prefix/END ancestry not waived'})
    scopes.append({'name': 'P03', 'decision': 'AUTHORIZE_PROSPECTIVE_P03_CHECKPOINT_QUALIFICATION',
        'qualified_result': sources['P03_qualified_result'], 'qualified_mapping': sources['P03_semantic_contract'],
        'applies_to': ['E2-A07', 'E2-A08', 'P03 named checkpoint fidelity and accepted P04 prerequisite'],
        'local_result': 'PASS', 'aggregate_END_acceptance_authorized': False,
        'historical_identity_replacement': False,
        'limitation': 'Portable fidelity at the new external checkpoint; authored completed-prefix premises do not prove executed original prefix'})

    inventory = []
    for index, row in enumerate(current['stage_bindings']):
        number, stage = index + 1, row['stage']
        old = old_rows[stage]
        assert stage == 'E2-A%02d' % number
        if number in (1, 2):
            artifacts = old['sources'] + [old['authoritative_result']]
            native = row['identity']
            original_snapshot = c._unwire(read(ROOT / old_rows['E2-A01']['sources'][0]['path'])['snapshot'])
            lineage = original_snapshot.context.lineage
            status = 'PROVEN_CANONICAL_DEFINITION_OR_READ_ONLY_SELECTION; NATIVE_OCCURRENCE_NOT_REQUIRED'
            local_mapping = {'type': 'CANONICAL_READ_ONLY_CASE', 'source': ref(SOURCE_DIR / 'canonical-bindings.json', '/stage_bindings/' + str(index))}
            n12 = 'SELECTION_NOT_EXECUTION; no completed result inferred from A02'
            n13 = 'ACTION_DEFINITIONS_NOT_ACTUAL_RESULTS'
        elif number == 3:
            artifacts = [results[3], mappings[3], ledgers['A03']['source']]
            native = {'bundle': ledgers['A03']['bundle_id'], 'events': [e['identity'] for e in ledgers['A03']['events']]}
            lineage = natives['A03'].current.context.lineage
            status, local_mapping, n12, n13 = 'ORIGINAL_UNPROVEN; ACTUAL_NEW_PROSPECTIVE_OCCURRENCE_PROVEN', mappings[3], 'PASS', 'PASS'
        elif number == 4:
            artifacts = [results[4], mappings[4], ledgers['A04']['source']]
            native = {'bundle': ledgers['A04']['bundle_id'], 'event': ledgers['A04']['events'][2]['identity'],
                      'post_Snapshot': ledgers['A04']['current_snapshot'], 'parent': ledgers['A04']['events'][2]['parent']}
            lineage = natives['A04'].current.context.lineage
            status, local_mapping, n12, n13 = 'ORIGINAL_UNPROVEN; ACTUAL_NEW_PROSPECTIVE_ANCESTRY_PROVEN', mappings[4], 'PASS', 'PASS'
        elif number == 5:
            artifacts = [results[5], mappings[5], row['native_event'], row['native_event_in_P04']]
            native = {'bundle': ledgers['P03']['bundle_id'], 'event': row['alternate_event_id'],
                      'choice': row['existing_choice_identity'], 'parent': row['alternate_parent_id'],
                      'decision_result_selector': row['native_result_reference']}
            lineage = row['alternate_context']['lineage']
            status, local_mapping, n12, n13 = 'ORIGINAL_A05_UNPROVEN; RETAINED_P03_EVENT_PROVEN', mappings[5], 'PASS', 'PASS'
        elif number == 6:
            artifacts = [results[6], mappings[6], ledgers['A06']['source']]
            native = {'bundle': ledgers['A06']['bundle_id'], 'events': [e['identity'] for e in ledgers['A06']['events']]}
            lineage = natives['A06'].current.context.lineage
            status, local_mapping, n12, n13 = 'ORIGINAL_UNPROVEN; ACTUAL_NEW_PROSPECTIVE_TWO_EVENT_TRACE_PROVEN', mappings[6], 'PASS', 'PASS'
        elif number in (7, 8):
            artifacts = old['sources'] + [ledgers['P03']['source']]
            native = row['identity']
            lineage = natives['P03'].current.context.lineage
            status = 'ORIGINAL_P03_CORRESPONDENCE_UNPROVEN; AUTHORIZED_NEW_CHECKPOINT_FIDELITY_PROVEN'
            local_mapping = sources['P03_qualified_result']
            n12, n13 = 'PERSISTENCE_NOT_NEW_EXECUTION; ACTUAL_RETAINED_NATIVE_EVENTS', 'FULL_TYPED_STATE_EQUALITY; NO_DECLARATION_PROMOTION'
        else:
            artifacts = [ledgers['P04']['source'], old['authoritative_result']]
            native = row['identity']
            lineage = natives['P04'].current.context.lineage
            status = 'PROVEN_ACTUAL_CANONICAL_P04_TAIL; ORIGINAL_PREFIX_LINK_UNPROVEN'
            local_mapping = ref(SOURCE_DIR / 'canonical-bindings.json', '/stage_bindings/' + str(index))
            n12, n13 = 'ACTUAL_ENROLLED_NATIVE_RESULT_EVENTS; COMPUTED_ELIGIBILITY_NOT_COMPLETION', 'EXACT_NATIVE_ACCEPTED_OUTPUT_AND_INDEPENDENT_TYPED_PROOFS'
        assert artifacts
        check_pins(artifacts)
        inventory.append({'STAGE': stage, 'SOURCE_ARTIFACTS': artifacts, 'NATIVE_IDENTITY': native,
            'SOURCE_LINEAGE': lineage, 'BINDING_CLASSIFICATION': row['classification'], 'HISTORICAL_STATUS': status,
            'END_MAPPING': local_mapping, 'N12_STATUS': n12, 'N13_STATUS': n13,
            'stage_binding': ref(CURRENT, '/stage_bindings/' + str(index)),
            'original_stage_binding_retained_exact': row,
            'canonical_oracle': case[stage], 'original_contract': old['canonical_contract'],
            'currentness_rule': old['currentness_rule'], 'provenance_rule': old['provenance_rule'],
            'scope_authority': scopes[number - 3] if number in (3, 4, 5, 6) else (scopes[-1] if number in (7, 8) else old['AUTHORITIES']),
            'not_an_aggregate_END_PASS': True})

    edges = []
    def edge(source, target, kind, status, relationship, assurance, evidence, proposal=None):
        record = {'source': source, 'target': target, 'classification': kind, 'current_status': status,
            'relationship': relationship, 'required_assurance': assurance, 'evidence': evidence,
            'native_parent_asserted': kind in ('CANONICAL_NATIVE_ANCESTRY', 'ORIGINAL_NATIVE_ANCESTRY') and
                relationship in ('EVENT_PARENT_AND_PRE_POST_SNAPSHOT', 'LIFECYCLE_STATE_INPUT'),
            'aggregate_semantic_acceptance_if_selected': proposal}
        record['edge_id'] = qid('qualification-END-edge-v1', record)
        edges.append(record)
        return record
    for node in inventory:
        classification = ('AUTHORIZED_PROSPECTIVE_REPLACEMENT' if node['STAGE'] in ('E2-A03', 'E2-A04', 'E2-A06', 'E2-A07', 'E2-A08')
            else 'AUTHORIZED_ALTERNATE_NATIVE_EVIDENCE' if node['STAGE'] == 'E2-A05' else 'SEMANTIC_ACCEPTANCE_EDGE')
        edge(node['STAGE'], 'E2-END', classification, 'BOUND_LOCAL_CASE_ONLY_AGGREGATE_PENDING',
             'CASE_COVERAGE_EVIDENCE', node['canonical_oracle']['EXPECTED_STATE'], node['SOURCE_ARTIFACTS'],
             'Accept this exact qualified case at its declared scope; never equate its event/lineage to the missing original')
    old_dag = read(SOURCE_DIR / 'dependency-DAG.json')
    causal = [e for e in old_dag['explicit_edges'] if e['dependency_type'] == 'LIFECYCLE_STATE_INPUT']
    for index, expected in enumerate(causal):
        source, target = expected['source_node'], expected['target_node']
        if index == 0:
            kind, status, evidence = 'SEMANTIC_ACCEPTANCE_EDGE', 'PROVEN_SHARED_ORIGINAL_SNAPSHOT_READ_ONLY', inventory[0]['SOURCE_ARTIFACTS'] + inventory[1]['SOURCE_ARTIFACTS']
        elif index == 2:
            kind, status, evidence = 'CANONICAL_NATIVE_ANCESTRY', 'PROVEN_IN_NEW_A03_A04_LEDGER_NOT_ORIGINAL', [ledgers['A03']['source'], ledgers['A04']['events'][2]['bundle_selector']]
        elif index == 6:
            kind, status, evidence = 'SEMANTIC_ACCEPTANCE_EDGE', 'PROVEN_SAME_NEW_CHECKPOINT_WRITER_READER_FIDELITY', inventory[6]['SOURCE_ARTIFACTS'] + inventory[7]['SOURCE_ARTIFACTS']
        elif index >= 7:
            kind, status, evidence = 'CANONICAL_NATIVE_ANCESTRY', 'PROVEN_P03_P04_NATIVE_TAIL_WITH_CONFIGURATION_BETWEEN_BOUNDARIES', [ledgers['P03']['source'], ledgers['P04']['source']]
        else:
            kind, status, evidence = 'UNPROVEN', 'NO_SINGLE_NATIVE_HANDOFF_CURRENT_SCOPE', inventory[index]['SOURCE_ARTIFACTS'] + inventory[index + 1]['SOURCE_ARTIFACTS']
        edge(source, target, kind, status, 'LIFECYCLE_STATE_INPUT', expected['target_input'], evidence,
             'SEMANTIC_ACCEPTANCE_EDGE_ONLY_UNDER_NEW_EXACT_AGGREGATE_SCOPE; cross-component post/pre identity equality is not claimed'
             if kind == 'UNPROVEN' else None)
    # Keep whole native segments; actual typed events are never rewritten as
    # scalar acceptance labels. Shared A03/P03 prefixes are de-duplicated.
    for role in ('A04', 'P04', 'A06'):
        ledger = ledgers[role]
        previous = 'NATIVE_START:' + ledger['initial_snapshot']
        for event in ledger['events']:
            edge(previous, event['identity'], 'CANONICAL_NATIVE_ANCESTRY', 'PROVEN_RETAINED_NATIVE_FIELDS',
                 'EVENT_PARENT_AND_PRE_POST_SNAPSHOT', 'Exact sequence/parent/pre/after/result/source/policy and within-ledger order',
                 [event['bundle_selector'], event['native_event']])
            previous = event['identity']
    interfaces = read(DOCS / (PREFIX + 'E2_PC04_END.json'))['dependencies']
    for index, interface in enumerate(interfaces):
        edge(interface, 'E2-END', 'SEMANTIC_ACCEPTANCE_EDGE', 'DECLARED_INTERFACE_CURRENT_FULL_END_PROCESS_BINDING_REQUIRED',
             'DECLARED_PC04_INTERFACE', 'Exact canonical definition/capability/oracle interface at required current consumers; READY is not execution PASS',
             [ref(DOCS / (PREFIX + 'E2_PC04_END.json'), '/dependencies/' + str(index))])

    configuration = read(SOURCE_DIR / 'configuration-history.json')
    for row in configuration['records']:
        event = natives['P04'].events[row['event_sequence'] - 1]
        assert aid(event.identity) == aid(c._unwire(row['event_id']))
        assert event.parent_event == c._unwire(row['parent_event'])
        assert event.parent_snapshot == c._unwire(row['pre_state']) and event.after_snapshot == c._unwire(row['post_state'])
        assert event.result.definition.id == c._unwire(row['definition_id'])
        assert event.result.authority.id == c._unwire(row['installation_authority_id'])
        edge(aid(event.identity), 'P04_CANONICAL_TAIL', 'CANONICAL_NATIVE_ANCESTRY', 'PROVEN_ACTUAL_CONFIG_HISTORY',
             'GOVERNED_CONFIGURATION_MEMBER', row['definition_type'] + ' / ' + row['operation'], [row['source']])
    assert [r['event_sequence'] for r in configuration['records']] == [3, 4, 5, 6, 7, 8, 9, 16, 18]
    for record in scopes:
        edge(record['decision'], 'SCOPE:' + record['name'], 'SEMANTIC_ACCEPTANCE_EDGE', 'AUTHORIZED_LOCAL_SCOPE_ONLY',
             'QUALIFICATION_SCOPE_MAPPING', record['applies_to'], [record['qualified_result'], record['qualified_mapping']],
             'Does not issue a native operating grant and does not independently authorize aggregate END acceptance')

    original_ideal = []
    for index, node in enumerate(inventory):
        number = index + 1
        occurrence = ('NOT_REQUIRED' if number in (1, 2, 7, 8) else 'PROVEN' if number >= 9 else 'UNPROVEN')
        connection = ('NOT_REQUIRED' if number == 1 else 'PROVEN' if number == 2 or number >= 10 else 'UNPROVEN')
        original_ideal.append({'stage': node['STAGE'], 'ideal_assurance': node['canonical_oracle'],
            'original_or_required_canonical_occurrence': occurrence,
            'original_exact_input_output_provenance_and_boundary_fidelity': 'UNPROVEN' if 3 <= number <= 8 else 'PROVEN',
            'same_original_mainline_predecessor_state_connection': connection,
            'replacement_substituted_in_this_ideal': False,
            'qualification_evidence_reference_only': node['SOURCE_ARTIFACTS'],
            'limitation': 'P04 native tail is actual canonical occurrence; PROVEN local tail does not prove original prefix continuity'
                if number >= 9 else 'Original state/report presence does not prove missing original occurrences or historical source/parent/ledger fidelity'})
    unproven = [{'stage': row['stage'], 'term': key, 'status': value}
                for row in original_ideal for key, value in row.items() if value == 'UNPROVEN']
    unproven += [{'term': term, 'status': 'UNPROVEN'} for term in (
        'ORIGINAL_A03_HISTORICAL_OCCURRENCE', 'ORIGINAL_A04_HISTORICAL_ANCESTRY',
        'ORIGINAL_A05_HISTORICAL_ANCESTRY', 'ORIGINAL_A06_HISTORICAL_REQUEST_WAIT_TRACE',
        'P03_HISTORICAL_CORRESPONDENCE', 'FULL_ORIGINAL_A01_A13_PARENT_CHAIN',
        'ORIGINAL_A05_CHOICE_TRUST_ROOT_ENVELOPE_AND_GRANT_ISSUANCE_HISTORY')]
    contract = {
        'END_ID': 'E2-END', 'END_TYPE': 'EXPERIMENT_ACCEPTANCE_CASE', 'earliest_sources': sources,
        'canonical_case': case['E2-END'], 'required_predecessors': [n['STAGE'] for n in inventory],
        'six_declared_interfaces': interfaces,
        'required_occurrence': 'Actual accepted native results/events for effecting stage cases; definitions/selection/control labels cannot replace them',
        'required_ancestry': 'Native parent_event, parent_snapshot, after_snapshot and ledger sequence within a mainline; immutable replay/source/policy bindings',
        'required_ordering': 'A01-A13 semantic mainline; no interchanged ordered events; received then validated then accepted reentry then actual result then independent proofs/FINISH',
        'required_states': 'Each independently sealed case oracle; same actual successor state is consumed at a causal handoff in the original END method',
        'required_provenance': 'Only canonical source bytes/defs, exact authority/context at each native consumer; expected answers harness-only',
        'required_authorities': 'Stage-local applicable native source/choice/USE/semantic/INSTALL authorities; no native END AuthorityClass',
        'source_uses_word_ancestry_for_whole_END': False,
        'whole_END_ancestry_term_origin': 'Later P05 binding/readiness recovery; inferred from canonical mainline and native append/replay contract, not a new primitive named by original matrix',
        'original_historical_ledger_identity_required': False,
        'single_native_mainline_required_by_unamended_method': True,
        'single_native_ledger_and_root_wording_explicit': False,
        'continuity_interpretation': 'Inference: sequential lifecycle execution across cold restore requires a native causal state/event chain. It may be a new independently authored reproduction, not the unavailable original historical run.',
        'per_stage_ancestry_alone_is_default_END': False,
        'already_authorized_aggregate_composite_acceptance': False,
        'proposed_method_is_acceptance_scope_amendment_not_historical_recovery': True,
    }
    graph = {'schema': 'E2-P05-END-QUALIFICATION-GRAPH-PROPOSAL-1', 'kind': 'COMPUTED_QUALIFICATION_EVIDENCE',
        'existing_stage_bindings_unchanged': ref(CURRENT), 'stage_nodes': inventory, 'edges': edges,
        'required_stage_count': 13, 'native_ledger_segments': ledgers,
        'role_lineage_policy': 'Role distinction retained even when physical native histories overlap; shared prefixes deduplicated, distinct histories never concatenated',
        'continuity_findings': {'A03_to_A04': 'Exact new native prefix extension PROVEN',
            'P03_A05_to_P04': 'Exact retained native prefix extension PROVEN',
            'A04_to_A05': 'UNPROVEN native connection', 'A05_to_A06': 'UNPROVEN native connection',
            'A06_to_P03_A07_checkpoint': 'UNPROVEN native connection', 'original_A02_to_new_A03': 'UNPROVEN native connection'},
        'P04_canonical_tail': {'bundle': ledgers['P04']['source'], 'entry_prefix_count': 9,
            'owned_A09_A13_sequence': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            'P03_native_prefix_events': 2, 'canonical_tail_root_parent': ledgers['P04']['events'][9]['parent'],
            'append_head': ledgers['P04']['head'], 'configuration': configuration,
            'never_fragmented_or_substituted': True},
        'authority': {'individual_scope_records': scopes, 'aggregate_selected_option': 'NONE',
            'aggregate_required_option': 'AUTHORIZE_COMPOSITE_P05_END_QUALIFICATION_MAPPING',
            'aggregate_authority_issued': False, 'native_authority_or_ledger_object': False},
        'historical_labels': {term: 'UNPROVEN' for term in (
            'ORIGINAL_A03_HISTORICAL_OCCURRENCE', 'ORIGINAL_A04_HISTORICAL_ANCESTRY',
            'ORIGINAL_A05_HISTORICAL_ANCESTRY', 'ORIGINAL_A06_HISTORICAL_REQUEST_WAIT_TRACE', 'P03_HISTORICAL_CORRESPONDENCE')},
        'graph_acceptance_status': 'NOT_AUTHORIZED_AS_AGGREGATE_END; INDIVIDUAL_13_STAGE_BINDINGS_REMAIN_VALID',
        'does_not_prove_one_A01_A13_execution': True, 'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO',
    }
    return {'graph': graph, 'graph_id': qid('qualification-END-evidence-graph-v1', graph),
            'contract': contract, 'original_ideal': original_ideal, 'original_unproven': unproven,
            'native_and_source_identity_checks': 'PASS', 'native_lifecycle_calls': CALLS}


def write_outputs(value):
    graph = value['graph']
    save(OUT / 'qualified-evidence-graph.json', {'identity': value['graph_id'], 'graph': graph})
    save(OUT / 'END-ancestry-contract.json', value['contract'])
    save(OUT / 'original-history-ideal.json', {'kind': 'IDEAL_NOT_CLAIMED_OCCURRED',
        'terms': value['original_ideal'], 'unproven': value['original_unproven'],
        'one_original_retained_ledger_proven': False, 'replacement_substitution': False})
    save(OUT / 'native-segment-integrity.json', {'RESULT': 'PASS', 'segments': graph['native_ledger_segments'],
        'physical_lineages': sorted({l['context']['lineage'] for l in graph['native_ledger_segments'].values()}),
        'A03_A04_role_identity_preserved_despite_same_physical_lineage': True,
        'P03_A05_P04_role_identity_preserved_despite_shared_prefix': True,
        'same_lineage_name_alone_proves_parentage': False,
        'missing_original_native_events_recreated': False, 'native_lifecycle_calls': CALLS})
    save(OUT / 'edge-classifications.json', {'counts': dict(Counter(e['classification'] for e in graph['edges'])),
        'edges': graph['edges'], 'classification_means_actual_native_parent_only_when_flag_true': True,
        'unproven_edges': [e for e in graph['edges'] if e['classification'] == 'UNPROVEN']})
    n12_terms = [
        ('READ_ONLY_NOT_EXECUTED', 'A01/A02 declarations/selections have no accepted result-event claim', ['E2-A01','E2-A02']),
        ('ACTUAL_EFFECT_EVENT_REQUIRED', 'Every lifecycle result claim selects immutable admitted native event/result; A03/A04/A05/A06/P04 actual bodies/parents/positions pinned', ['E2-A03','E2-A04','E2-A05','E2-A06','P04_CANONICAL_TAIL']),
        ('NO_COMPOSITE_EVENT_FABRICATION', 'Graph ID and semantic edges are documentary; none becomes a native event/root/parent or producer instance', ['ALL_EDGES']),
        ('NO_PREMISE_TO_OCCURRENCE_PROMOTION', 'P03 initially completed CHECK/COLLECT/PREPARE and WAITING premises do not prove original execution; A05 grant pre-exists', ['E2-A05','E2-A07','E2-A08']),
        ('WITHIN_SEGMENT_ORDER_EXACT', 'Native parent/pre/post/sequence proven inside each retained segment; cross-segment order is a declared accepted assurance relation only if aggregate scope selected', ['ALL_NATIVE_SEGMENTS']),
        ('AGGREGATE_SCOPE_GUARD', 'No aggregate acceptance from the conjunction of local PASS flags without this exact new scope decision', ['E2-END']),
    ]
    n13_terms = [
        ('DEFINITION_RESULT_SEPARATION', 'Canonical definitions, expected oracle objects and actual supplied native results retain separate identities/roles', ['ALL_STAGES']),
        ('EXACT_OUTPUT_PROVENANCE', 'Knowledge/result claims selected from actual native event/state in their own source context; common names do not equate different records', ['E2-A03','E2-A04','P04_CANONICAL_TAIL']),
        ('NO_FOREIGN_LINEAGE_NATIVE_SUBSTITUTION', 'Semantic scope edge cannot be passed to Planner as evidence, authority, prerequisite, receipt or proof', ['ALL_CROSS_SEGMENT_EDGES']),
        ('INDEPENDENT_PROOF_AND_AUTHORITY', 'P04 actual Proof/C03/results/root-slot proofs retain exact native inputs and authority; A05 grants not inferred issued; A06 produces no later effects', ['E2-A05','E2-A06','P04_CANONICAL_TAIL']),
        ('HISTORICAL_LABELS_PRESERVED', 'Original four historical gaps and P03 correspondence remain UNPROVEN; no native identity alias', ['ALL_HISTORICAL_TERMS']),
        ('NO_GLOBAL_NEGATIVE_PASS_BY_LOCAL_MAPPING', 'Global P05 N13 and N12 tests remain required; static graph composition does not execute or pass them', ['E2-N12','E2-N13']),
    ]
    aggregates = {}
    for name, terms in (('N12', n12_terms), ('N13', n13_terms)):
        aggregates[name] = {'canonical_requirement': value['contract']['earliest_sources']['matrix_' + name],
            'canonical_case': read(DOCS / (PREFIX + 'CANONICAL_QUALIFICATION_EXPERIMENT_1.json'))['cases'][27 if name=='N12' else 28],
            'terms': [{'term': term, 'required_assurance': assurance, 'subjects': subjects,
                       'evidence': ref(OUT / 'qualified-evidence-graph.json'), 'structural_check': 'PASS',
                       'aggregate_acceptance': 'PENDING_EXACT_AGGREGATE_SCOPE_DECISION'} for term, assurance, subjects in terms],
            'composition_preserves_negative_assurance_if_exact_policy_selected': True,
            'full_original_native_handoff_assurance_preserved': False,
            'original_historical_gaps_remain_unproven': True,
            'N13_inferred_from_N12': False,
            'P05_global_case_executed': False,
            'CURRENT_RESULT': 'PRESERVATION_CONTRACT_COMPLETE; AGGREGATE_ACCEPTANCE_NOT_AUTHORIZED'}
    save(OUT / 'aggregate-N12-N13-contract.json', aggregates)
    exclusions = [
        'One original historical A01-A13 native execution lineage was retained and proven',
        'Cross-lineage post-state/pre-state equality or original parent continuity was recovered',
        'The P03 initial completed-prefix premises are original occurred events',
        'The retained P03/A05 decision issued its pre-existing grant',
        'New request bytes were transmitted to a real external service',
        'All current P05 negatives/D01/REG or P06 review already PASS',
        'A qualification semantic edge is native execution, reentry permission, proof or authority',
        'N_REAL, E1 migration or aggregate Planner release requirements are satisfied',
    ]
    oracle_terms = []
    for node in graph['stage_nodes']:
        oracle_terms.append({'term': node['STAGE'], 'evidence_sources': node['SOURCE_ARTIFACTS'],
            'classification': node['BINDING_CLASSIFICATION'], 'native_identity': node['NATIVE_IDENTITY'],
            'required_assurance': node['canonical_oracle'], 'historical_label': node['HISTORICAL_STATUS'],
            'scope_authority': node['scope_authority'], 'N12_mapping': node['N12_STATUS'], 'N13_mapping': node['N13_STATUS'],
            'current_local_input_check': 'PASS', 'aggregate_scope': 'PENDING'})
    oracle = {'schema': 'E2-P05-COMPOSITE-END-ACCEPTANCE-ORACLE-PROPOSAL-1', 'graph_identity': value['graph_id'],
        'stage_terms': oracle_terms, 'edge_terms': graph['edges'],
        'native_segments': graph['native_ledger_segments'], 'aggregate_N12_N13': ref(OUT / 'aggregate-N12-N13-contract.json'),
        'all_local_stage_bindings_required': 13, 'all_native_segments_must_survive_existing_restore_replay_oracles': True,
        'governing_scope_required': 'AUTHORIZE_COMPOSITE_P05_END_QUALIFICATION_MAPPING',
        'acceptance_rule': 'Exact graph + complete original local oracles/currentness/provenance/native segments + independently preserved N12/N13 + exact authenticated aggregate scope + all retained END persistence/determinism/interface obligations PASS',
        'preexecution_contract_check': 'PASS_IDENTITY_AND_STRUCTURE_ONLY', 'aggregate_scope_check': 'NOT_SELECTED',
        'END_case_verdict': 'NOT_EXECUTED_NOT_ACCEPTED',
        'six_interfaces_and_process_inputs': {'interfaces': value['contract']['six_declared_interfaces'],
            'expected': 'Each required current definition/capability/oracle/process interface must be bound under the selected method; immutable historical READY contracts alone are insufficient',
            'status': 'CONCRETE_FULL_END_EXECUTION_MANIFEST_BINDING_STILL_REQUIRED'},
        'P05_other_requirements': ref(ROOT / 'docs/plans/qualification/E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1/post-A06-complete-P05-readiness-oracle.json'),
        'PASS_CLAIM': 'Required Planner stage behaviors and local native occurrence/ancestry assurances are qualified through the exact explicitly authorized composite evidence mappings; cross-segment links are semantic acceptance edges.',
        'excluded_claims': exclusions, 'not_literal_full_native_mainline_equivalence': True}
    save(OUT / 'END-qualification-oracle.json', oracle)
    subject = {'schema': 'E2-P05-END-AGGREGATE-ACCEPTANCE-SUBJECT-1', 'consumer': 'E2-P05 / E2-END acceptance only',
        'graph_identity': value['graph_id'], 'graph_content': ref(OUT / 'qualified-evidence-graph.json'),
        'acceptance_oracle': ref(OUT / 'END-qualification-oracle.json'),
        'assurance_contract': ref(OUT / 'aggregate-N12-N13-contract.json'), 'unchanged_binding_graph': ref(CURRENT),
        'sources': value['contract']['earliest_sources'],
        'explicitly_changed_obligation': 'Native continuity across four unjoined component boundaries becomes declared semantic qualification acceptance under a new scope amendment; no native/history identity is changed',
        'cross_component_edge_ids': [e['edge_id'] for e in graph['edges'] if e['classification'] == 'UNPROVEN'],
        'qualification_only': True, 'expires_if_any_bound_content_or_authority_or_claim_changes': True,
        'pass_claim': oracle['PASS_CLAIM'], 'excluded_claims': exclusions,
        'unchanged_requirements': ['Every local stage oracle and native admission condition', 'P04 entire canonical tail',
            'Exact source/context/policy/authority/currentness at each native consumer',
            'Within-segment ordered native replay/persistence', 'All 16 P05 negatives, current D01 and REG',
            'Full prepared process/input manifests and P06 independent review', 'Historical limitations and N_REAL'],
        'no_native_authority_or_operation_granted': True, 'no_execution_authorization': True}
    subject_id = qid('qualification-scope-subject-v1', subject)
    options = [
        {'option': 'RETAIN_FULL_ORIGINAL_END_ANCESTRY_REQUIREMENT', 'selected': False,
         'meaning': 'Retain the original END method: complete native A01-A13 mainline continuity. This does not add an original historical-event-ID recovery requirement; a new independently prepared legitimate full END reproduction may satisfy the native method.',
         'consequences': ['Composite graph remains supplemental evidence only', '13/13 stage bindings remain unchanged',
            'P05 readiness remains NO while full native END input/history/manifests unbound',
            'No reproduction occurs until its independent start/inputs/authority/oracles are sealed',
            'Original historical UNPROVEN labels remain unchanged']},
        {'option': 'AUTHORIZE_COMPOSITE_P05_END_QUALIFICATION_MAPPING', 'selected': False,
         'meaning': 'Explicitly amend the aggregate END acceptance method for this exact graph: accept fully qualified native component segments plus exactly four named semantic bridge edges instead of asserting a single native A01-A13 causal execution.',
         'consequences': ['Qualification-scope authorization only; no native grant, event, result, proof or installation',
            'After authentication and separate mapping qualification, the named aggregate acceptance-method gap may close',
            'Neither a continuous original nor a continuous new A01-A13 native chain becomes proven',
            'Full P05 readiness must still independently check current interfaces, initial N08/N12 operands, processes, persistence/replay, authority subjects and all non-stage terms',
            'P05/P06 not authorized to execute merely by this choice; all current P05 cases remain required',
            'Every historical label, A05 pre-existing-grant limitation and stage-local scope remains unchanged']},
    ]
    dossier = {'schema': 'E2-P05-END-AGGREGATE-DECISION-DOSSIER-1', 'subject': subject, 'subject_identity': subject_id,
        'selected_option': 'NONE', 'options': options, 'decision_ready': True,
        'required_issuer': 'Authenticated owner of canonical E2 qualification scope; trusted conversation selection or independently authenticated explicit delegation',
        'required_authentication': ['Exact selected option token', 'This subject identity and dossier raw SHA-256',
            'Exact graph/source/oracle/mapping content hashes', 'Issuer and qualification-scope provenance',
            'No material changes between decision and authentication', 'Separate subsequent mapping qualification'],
        'source_precedent': value['contract']['earliest_sources']['P03_scope_dossier'],
        'native_authority_class': None, 'native_operating_grant_issued': False,
        'individual_scope_decisions_already_cover_aggregate_END': False,
        'user_authorizes_graph_recovery_and_decision_preparation_now': True,
        'user_has_selected_an_aggregate_option': False,
        'no_snapshot_report_only_alternative': True}
    save(OUT / 'aggregate-END-decision-dossier.json', dossier)
    save(OUT / 'reconciliation-findings.json', {
        'RESULT': 'PASS_CONTRACT_RECOVERY_AND_BOUNDED_DECISION_PREPARATION',
        'SINGLE_NATIVE_LINEAGE_REQUIRED': 'YES', 'SINGLE_NATIVE_LINEAGE_REQUIRED_domain': 'Unamended canonical mainline END execution method; explicit inference, not required original historical identity',
        'ORIGINAL_HISTORICAL_LINEAGE_REQUIRED': 'NO', 'SINGLE_NATIVE_LINEAGE_PROVEN': 'NO',
        'COMPOSITE_QUALIFICATION_PERMITTED': 'NO', 'COMPOSITE_QUALIFICATION_PERMITTED_domain': 'Current selected qualification scope; proposed new method requires the unselected aggregate decision',
        'COMPOSITE_QUALIFICATION_PROPOSAL_AVAILABLE': 'YES; explicit scope amendment with narrower integrated-history claim',
        'AGGREGATE_END_AUTHORITY_REQUIRED': 'YES', 'AGGREGATE_END_DECISION_READY': 'YES',
        'AGGREGATE_END_SELECTED_OPTION': 'NONE', 'AGGREGATE_SCOPE_SUBJECT_ID': subject_id,
        'COMPOSITE_GRAPH_IDENTITY': value['graph_id'], 'graph_is_native_ledger_or_Planner_object': False,
        'P05_BOUND_STAGE_INPUTS': 13, 'P05_REQUIRED_STAGE_INPUTS': 13,
        'P05_EXECUTION_READY': 'NO', 'P05_EXECUTED': 'NO', 'P06_EXECUTED': 'NO',
        'remaining_non_stage_preparation_not_closed': True,
        'no_existing_stage_bindings_altered': True, 'N_REAL_SATISFIED': 'NO',
        'RUNTIME_MODIFIED': 'NO', 'E1_ARTIFACTS_MODIFIED': 0, 'PRODUCTION_EFFECT': 'NO',
        'native_lifecycle_calls': CALLS, 'options': options,
        'NEXT_PACKAGE': 'E2-P05 AGGREGATE END QUALIFICATION-SCOPE DECISION; then authenticated mapping qualification/preparation',
    })


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--reader', type=int)
    parser.add_argument('--refresh-own-draft', action='store_true')
    args = parser.parse_args()
    REFRESH_OWN_DRAFT = args.refresh_own_draft
    result = build()
    assert not CALLS
    if args.reader is None:
        write_outputs(result)
    else:
        persisted = read(OUT / 'qualified-evidence-graph.json')
        assert result['graph_id'] == persisted['identity']
        assert c.canonical_bytes(result['graph']) == c.canonical_bytes(persisted['graph'])
        save(OUT / 'readers' / ('seed-%s-reader-%s.json' % (os.environ['PYTHONHASHSEED'], args.reader)),
             {'RESULT': 'PASS', 'graph_identity': result['graph_id'], 'semantic_bytes_sha256': result['graph_id'].split(':')[1],
              'seed': os.environ['PYTHONHASHSEED'], 'reader': args.reader, 'pid': os.getpid(),
              'writer_memory_available': False, 'reconstructs_only_from_trusted_authoritative_inputs': True,
              'native_lifecycle_calls': CALLS, 'aggregate_decision_selected': False})
    print(json.dumps({'RESULT': 'PASS_READ_ONLY', 'graph_identity': result['graph_id'],
                      'stage_count': 13, 'native_calls': CALLS, 'reader': args.reader}))
