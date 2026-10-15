"""Read-only contract/empty-input preflight; no A06 operation or replay."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess

from adapter.planner import codec as c, core, gates, model as m
from adapter.planner.selector import validate_policy

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
REPORT = ROOT / 'docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_P05_A06_PROSPECTIVE_REQUEST_WAIT_CONTRACT_1'
CALLS = []


def deny(name):
    def blocked(*args, **kwargs):
        CALLS.append(name)
        raise AssertionError('Unexecuted contract prohibits ' + name)
    return blocked


for module, names in (
    (core, ('apply_receipt', 'apply_event', 'apply_result', 'recompute', 'resume_eligibility',
            '_inventory', 'apply_recorded_decision', 'apply_decision_reentry', 'admit_dossier_materialization')),
    (c, ('apply_event', '_replay', '_prefix_bundle', 'record_result', 'append_event',
         'commit_event', 'commit_result', 'save_bundle', 'restore', 'decode_bundle',
         'bundle_id', 'bundle_bytes', '_publish_head', '_read_head', 'admit_external_evidence'))):
    for symbol in names:
        setattr(module, symbol, deny(module.__name__ + '.' + symbol))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def aid(identity):
    return None if identity is None else identity.namespace + ':' + identity.sha256


def refs(value):
    if isinstance(value, dict):
        if isinstance(value.get('path'), str) and isinstance(value.get('raw_sha256'), str):
            yield value
        for child in value.values():
            yield from refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from refs(child)


def resolve_pointer(value, expression):
    for token in expression.split('/')[1:]:
        token = token.replace('~1', '/').replace('~0', '~')
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def main():
    baseline = json.loads((OUT / 'baseline.json').read_bytes())['files']
    changed, missing, hash_cache = [], [], {}
    for path, expected in baseline.items():
        source = ROOT / path
        if not source.is_file():
            missing.append(path)
        else:
            actual = digest(source)
            hash_cache[path] = actual
            if actual != expected:
                changed.append(path)
    assert not changed and not missing, (changed, missing)
    listing = subprocess.run(['rg', '--files', '--hidden', '-g', '!.git', '-g', '!__pycache__',
                              '-g', '!node_modules', '-g', '!target'], cwd=str(ROOT),
                             capture_output=True, text=True, check=True)
    new_paths = sorted(set(listing.stdout.splitlines()) - set(baseline))
    allowed = {str(REPORT.with_suffix(ext).relative_to(ROOT)) for ext in ('.md', '.json')}
    prefix = str(OUT.relative_to(ROOT)) + '/'
    assert all(path.startswith(prefix) or path in allowed for path in new_paths), new_paths
    documents = {str(path.relative_to(ROOT)): json.loads(path.read_bytes())
                 for path in OUT.rglob('*.json') if path.name != 'verification.json'}
    report = json.loads(REPORT.with_suffix('.json').read_bytes())
    documents[str(REPORT.with_suffix('.json').relative_to(ROOT))] = report
    pins, pointers, json_cache = set(), set(), dict(documents)
    for document in documents.values():
        for ref in refs(document):
            source = ROOT / ref['path']
            assert source.is_file(), ref['path']
            if ref['path'] not in hash_cache:
                hash_cache[ref['path']] = digest(source)
            assert hash_cache[ref['path']] == ref['raw_sha256'], ref['path']
            pins.add(ref['path'])
            expression = ref.get('pointer', '')
            if expression and source.suffix == '.json':
                assert expression.startswith('/'), expression
                if ref['path'] not in json_cache:
                    json_cache[ref['path']] = json.loads(source.read_bytes())
                resolve_pointer(json_cache[ref['path']], expression)
                pointers.add((ref['path'], expression))
    authorization = json.loads((OUT / 'authorization-capture.json').read_bytes())
    dossier = json.loads((ROOT / authorization['scope_dossier']['path']).read_bytes())
    subject = 'qualification-scope-subject-v1:' + hashlib.sha256(c.canonical_bytes(dossier['subject'])).hexdigest()
    assert subject == dossier['subject_identity'] == authorization['scope_subject_identity']
    assert authorization['SELECTED_OPTION'] == report['SELECTED_OPTION'] == 'AUTHORIZE_PROSPECTIVE_P05_A06_REQUEST_WAIT_QUALIFICATION'
    assert dossier['selected_option'] == 'NONE' and not dossier['native_authority_issued']
    assert authorization['ADDITIONAL_AUTHORITY_REQUIRED'] == 'NO' and not authorization['native_operating_authority_required']
    assert authorization['native_grants_issued_or_reused'] == 0

    fixtures = json.loads((OUT / 'sealed-fixtures.json').read_bytes())
    all_fixtures = [fixtures['primary']] + fixtures['independent_reproductions']
    assert len(all_fixtures) == 4 and len({f['lineage'] for f in all_fixtures}) == 4
    queries = []
    for fixture in all_fixtures:
        raw = (ROOT / fixture['START_PATH']['path']).read_bytes()
        bundle = c._unwire(json.loads(raw)['bundle'])
        m.validate_types(bundle, m.PersistenceBundle)
        m.validate_model(bundle.initial)
        assert bundle.initial == bundle.current and not bundle.events and not bundle.dossier_materializations
        assert raw == c._bundle_bytes_admitted(bundle)
        assert aid(c._identity(raw, 'planner-bundle-v1')) == fixture['START_BUNDLE_ID']
        assert aid(c.snapshot_id(bundle.current)) == fixture['START_STATE_ID']
        assert fixture['LEDGER_ROOT'] is fixture['APPEND_HEAD'] is fixture['PARENT_EVENT_ID'] is None
        assert fixture['PROSPECTIVE_LINEAGE_DIFFERS_FROM_ORIGINAL']
        validate_policy(bundle.policy, bundle.policy_version)
        c._check_snapshot_pins(bundle.current, bundle.sources)
        c._verify_sources(bundle, ROOT)
        initial = bundle.current
        assert len(initial.actions) == 1 and initial.actions[0].id.value == 'E2-REENTER'
        assert all(status.state is m.ActionState.ACTION_ELIGIBLE for status in initial.statuses)
        assert not initial.entities and not initial.knowledge and not initial.decisions
        assert not initial.typed_proofs and not initial.validation_instances and not initial.validation_results
        assert not initial.installed_definitions and not initial.receipt_admissions and not initial.receipt_observations
        gate = initial.external_gates[0]
        request = gate.resolution_contracts[0]
        requirement = initial.evidence_requirements[0]
        assert gate.stage is m.ExternalStage.EXTERNAL_EVIDENCE_REQUIRED and not gate.history and gate.pending is None
        assert gate.validation is m.ValidationState.ACCEPTED and gate.contract_complete and requirement.rule_known
        assert c._wire(request) == fixture['REQUEST'] and c._wire(gate) == fixture['WAIT_GATE']
        assert request.scope == initial.context.scope and request.lineage == initial.context.lineage
        assert request.generation == initial.context.generation
        assert request.gate == gate.id and request.requirement == requirement.id
        assert request.proposition == requirement.proposition and request.target == requirement.target
        assert request.producers == requirement.producers and request.gate_source == gate.provenance.identity
        assert request.requirement_source == requirement.provenance.identity
        assert request.reentry == gate.reentry and request.held_actions == gate.held_actions
        source_contract = json.loads((ROOT / request.provenance.path).read_bytes())['contract']
        assert all(c._wire(getattr(request, key)) == value for key, value in source_contract.items())

        # Read-only initial admission query compared with an independently
        # authored oracle already sealed before this query. No future state
        # application and no result/selection coverage simulation is permitted.
        before = c.snapshot_bytes(initial)
        statuses, blocked, ready = core._actionability(initial)
        assert not ready
        projection = core.project(initial)
        computation = core._global_control(initial, core.Computation((), statuses, blocked, None, projection.defects))
        proof = gates.obligation_proof(initial, requirement.id)
        expected = json.loads((ROOT / fixture['EXPECTED_STATE_ORACLES']['pre-trace']['path']).read_bytes())
        assert computation.control.value == expected['CONTROL'] == 'EXTERNAL_WAIT'
        assert not computation.actionable and not computation.defects and computation.selection is None
        assert dict((s.id.value, s.state.value) for s in computation.statuses) == expected['computed_Action_status']
        assert list(dict(blocked)[initial.actions[0].id]) == expected['computed_blockers']
        assert proof.state.value == expected['obligation_Proof']['state'] and list(proof.reasons) == expected['obligation_Proof']['reasons']
        assert c.snapshot_bytes(initial) == before
        queries.append({'fixture': fixture['variant'], 'pre_state_static_oracle': 'PASS',
                        'control': computation.control.value, 'gate': gate.stage.value,
                        'actual_lifecycle_operation': False})
        comparison_states = []
        for boundary in ('pre-trace', 'request-ready', 'post-trace'):
            oracle = json.loads((ROOT / fixture['EXPECTED_STATE_ORACLES'][boundary]['path']).read_bytes())
            snapshot_path = ROOT / fixture['EXPECTED_STATE_ORACLES'][boundary + '_snapshot']['path']
            state = c._unwire(json.loads(snapshot_path.read_bytes())['snapshot'])
            m.validate_model(state)
            assert c.snapshot_bytes(state) == snapshot_path.read_bytes()
            assert aid(c.snapshot_id(state)) == oracle['snapshot_identity']
            assert oracle['comparison_only'] and not oracle['completed_Actions'] and not oracle['native_authorities']
            assert c._wire(state.external_gates[0])['stage']['value'] == oracle['gate_stage']
            for field in m.Snapshot.__dataclass_fields__:
                if field != 'external_gates':
                    assert getattr(state, field) == getattr(initial, field), (boundary, field)
            comparison_states.append(state)
        previous = None
        for index, event_spec in enumerate(fixture['EXPECTED_EVENT_ORACLE']):
            event = c._unwire(json.loads((ROOT / event_spec['expected_event_file']['path']).read_bytes()))
            m.validate_types(event, m.ExecutionEvent)
            assert type(event.result) is m.ExternalEvent and event.result.artifact is None
            assert event.sequence == index + 1 and event.parent_event == previous
            assert event.parent_snapshot == event.result.expected_snapshot == c.snapshot_id(comparison_states[index])
            assert event.after_snapshot == c.snapshot_id(comparison_states[index + 1])
            expected_id = c._event_identity(event.sequence, event.parent_snapshot, event.parent_event, event.result, event.after_snapshot)
            assert event.identity == expected_id and aid(expected_id) == event_spec['EVENT_ID']
            assert event_spec['comparison_only'] and event.resume_binding is None
            previous = event.identity

    mapping = json.loads((OUT / 'END-N12-N13-mapping.json').read_bytes())
    canonical_cases = json.loads((ROOT / mapping['N12']['source']['path']).read_bytes())
    for name in ('N12', 'N13'):
        assert resolve_pointer(canonical_cases, mapping[name]['source']['pointer']) == mapping[name]['canonical_case']
        assert mapping[name]['assurance_preserved'] and not mapping[name]['P05_global_' + name + '_case_pass_claimed']
    assert not mapping['N13']['inferred_from_N12'] and not mapping['END']['original_prefix_or_full_END_gap_waived']
    readiness = json.loads((OUT / 'post-A06-complete-P05-readiness-oracle.json').read_bytes())
    assert len(readiness['sixteen_expected_negative_cases']) == 16 and not readiness['13_of_13_is_sufficient_alone']
    assert not readiness['original_prefix_gap_waived'] and len(readiness['terms']) == 14
    negatives = json.loads((OUT / 'sealed-negative-oracles.json').read_bytes())
    assert negatives['case_count'] == len(negatives['cases']) == 27 and not negatives['executed']
    graph = json.loads((ROOT / readiness['current_graph']['path']).read_bytes())
    assert graph['P05_BOUND_STAGE_INPUTS'] == 12 and sum(row['binding_status'] == 'BOUND' for row in graph['stage_bindings']) == 12
    assert graph['stage_bindings'][5]['binding_status'] == 'MISSING_CANONICAL_OUTPUT'
    for key in ('PROSPECTIVE_A06_EXECUTED', 'P05_EXECUTED', 'P06_EXECUTED', 'RUNTIME_MODIFIED', 'PRODUCTION_EFFECT', 'N_REAL_SATISFIED'):
        assert report[key] == 'NO'
    assert report['RESULT'] == 'PASS' and report['PROSPECTIVE_A06_EXECUTION_READY'] == 'YES'
    assert report['P05_EXECUTION_READY'] == 'NO' and not CALLS
    for document in documents.values():
        assert not re.search(r'\b(?:TBD|TODO|TO_BE_DETERMINED)\b', json.dumps(document)), 'placeholder in sealed contract'
    for path in OUT.glob('*.py'):
        ast.parse(path.read_text(), str(path))
    md_path = REPORT.with_suffix('.md')
    links = re.findall(r'\]\(([^)]+)\)', md_path.read_text())
    for target in links:
        path = (md_path.parent / re.sub(r':\d+$', '', target)).resolve()
        assert path.is_file() or path == OUT / 'verification.json', target
    assert 'START_BUNDLE_ID' in md_path.read_text() and 'START_STATE_ID' in md_path.read_text()
    diff = subprocess.run(['git', 'diff', '--check'], cwd=str(ROOT), capture_output=True, text=True)
    assert diff.returncode == 0, diff.stdout + diff.stderr
    result = {
        'schema': 'E2-P05-A06-PROSPECTIVE-CONTRACT-VERIFICATION-1', 'RESULT': 'PASS',
        'contract_only': True, 'native_lifecycle_application_append_commit_restore_replay_calls': CALLS,
        'native_grants_choices_or_actual_events_created': 0, 'comparison_event_objects_enrolled': 0,
        'baseline_files_unchanged': len(baseline), 'changed_prior_files': changed, 'missing_prior_files': missing,
        'runtime_files_unchanged': sum(path.startswith('adapter/planner/') for path in baseline),
        'frozen_E1_files_unchanged': sum(path.startswith('docs/experiments/E1/') for path in baseline),
        'new_files_only_in_authorized_contract_destinations': True, 'new_files': new_paths,
        'native_empty_fixture_checks': queries, 'fixture_contexts_distinct': True,
        'scope_authentication': 'PASS', 'scope_subject_identity': subject,
        'exact_source_hashes_verified': len(pins), 'native_JSON_pointers_verified': len(pointers),
        'new_JSON_readability': 'PASS', 'new_Python_syntax': 'PASS', 'report_local_links_verified': len(links),
        'independent_algebraic_event_snapshot_identity_comparisons': 'PASS',
        'oracles_not_operation_inputs': True, 'placeholder_values': 0,
        'negative_suite': '27_SEALED_NOT_EXECUTED', 'N12_N13_assurance_contract': 'PRESERVED_NOT_EXECUTED',
        'full_P05_readiness_conjunction': '14_TERMS_SEALED; 13_OF_13_NOT_SUFFICIENT',
        'old_12_bound_rows_and_A03_A04_A05_scope_artifacts': 'UNCHANGED',
        'PROSPECTIVE_A06_EXECUTION_READY': 'YES', 'PROSPECTIVE_A06_EXECUTED': 'NO',
        'P05_BOUND_STAGE_INPUTS': 12, 'P05_EXECUTION_READY': 'NO',
        'report_pins': [{'path': str(path.relative_to(ROOT)), 'raw_sha256': digest(path)}
                        for path in (REPORT.with_suffix('.md'), REPORT.with_suffix('.json'))],
        'script_pins': [{'path': str(path.relative_to(ROOT)), 'raw_sha256': digest(path)} for path in OUT.glob('*.py')],
        'E1_ARTIFACTS_MODIFIED': 0, 'PRODUCTION_EFFECT': 'NO', 'git_diff_check': 'PASS'}
    (OUT / 'verification.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps({'verification': 'PASS', 'baseline_unchanged': len(baseline),
                     'new_fixtures': len(queries), 'A06_lifecycle_calls': CALLS,
                     'A06_execution_ready': 'YES', 'P05_bindings': '12/13', 'git_diff_check': 'PASS'}))


if __name__ == '__main__':
    main()
