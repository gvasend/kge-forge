"""Verify recovery evidence and preservation without any native operation/replay."""
import ast
import collections
import hashlib
import json
from pathlib import Path
import re
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[3]
REPORT = ROOT / 'docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_P05_A06_REQUEST_WAIT_TRACE_RECOVERY_1'
STAGES = {'EVIDENCE_REQUEST_READY', 'WAITING_FOR_EXTERNAL_EVIDENCE'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode()


def pointer(value, expression):
    for token in expression.split('/')[1:]:
        token = token.replace('~1', '/').replace('~0', '~')
        value = value[int(token)] if isinstance(value, list) else value[token]
    return value


def pinned_refs(value):
    if isinstance(value, dict):
        if isinstance(value.get('path'), str) and isinstance(value.get('raw_sha256'), str):
            yield value
        for item in value.values():
            yield from pinned_refs(item)
    elif isinstance(value, list):
        for item in value:
            yield from pinned_refs(item)


def main():
    baseline = json.loads((OUT / 'baseline.json').read_bytes())['files']
    changed, missing = [], []
    hash_cache = {}
    for name, expected in baseline.items():
        path = ROOT / name
        if not path.is_file():
            missing.append(name)
            continue
        actual = digest(path)
        hash_cache[name] = actual
        if actual != expected:
            changed.append(name)
    assert not changed and not missing, (changed, missing)

    listing = subprocess.run(['rg', '--files', '--hidden', '-g', '!.git', '-g', '!__pycache__',
                              '-g', '!node_modules', '-g', '!target'], cwd=str(ROOT),
                             capture_output=True, text=True, check=True)
    new_files = sorted(set(listing.stdout.splitlines()) - set(baseline))
    allowed_reports = {str(REPORT.with_suffix(ext).relative_to(ROOT)) for ext in ('.md', '.json')}
    evidence_prefix = str(OUT.relative_to(ROOT)) + '/'
    assert all(name.startswith(evidence_prefix) or name in allowed_reports for name in new_files), new_files

    docs = {path.name: json.loads(path.read_bytes()) for path in OUT.glob('*.json')
            if path.name != 'verification.json'}
    report_path = REPORT.with_suffix('.json')
    report = json.loads(report_path.read_bytes())
    pins, strict_pointers = set(), set()
    json_cache = {}
    # Search pointers in decoded prose fragments are discovery locations, not
    # necessarily file-level RFC 6901 pointers. Independently inspect real JSON
    # pointers on the final native records, oracle, report and source dossier.
    strict_docs = {
        'authoritative-source-pins.json', 'trace-contract-and-assurance.json',
        'candidate-and-losslessness-analysis.json', 'scope-decision-dossier.json',
        'P05-binding-frontier.json', 'native-state-and-ledger-inspection.json'}
    for name, document in list(docs.items()) + [('report', report)]:
        for ref in pinned_refs(document):
            relative = ref['path']
            source = ROOT / relative
            assert source.is_file(), relative
            if relative not in hash_cache:
                hash_cache[relative] = digest(source)
            actual = hash_cache[relative]
            assert actual == ref['raw_sha256'], (relative, ref['raw_sha256'], actual)
            pins.add((relative, actual))
            expression = ref.get('pointer', '')
            if expression and source.suffix == '.json' and (name in strict_docs or name == 'report'):
                assert expression.startswith('/'), expression
                if relative not in json_cache:
                    json_cache[relative] = json.loads(source.read_bytes())
                pointer(json_cache[relative], expression)
                strict_pointers.add((relative, expression))

    search = docs['search-summary.json']
    event_search = docs['event-search.json']
    persistence = docs['persistence-search.json']
    native = docs['native-state-and-ledger-inspection.json']
    frontier = docs['P05-binding-frontier.json']
    dossier = docs['scope-decision-dossier.json']
    assurance = docs['trace-contract-and-assurance.json']['assurance']
    assert search['parse_errors'] == search['empty_files'] == 0
    assert search['request_wait_native_event_identities'] == 0
    assert search['request_wait_native_command_representations'] == 0
    assert search['request_wait_identity_bodies'] == 0
    assert not event_search['request_wait_events']
    assert not event_search['identity_bodies']
    assert len(event_search['unique_events']) == search['native_event_identities']
    assert len(event_search['external_events']) == search['native_ExternalEvent_identities']
    external_stages = collections.Counter(row['event']['result']['stage']['value']
                                         for row in event_search['external_events'])
    assert external_stages == {'EVIDENCE_RECEIVED': 6, 'DEPENDENT_ACTION_REENTRY': 3}
    assert len(persistence['bundles']) == search['bundle_representations']
    assert len(persistence['heads']) == search['HEAD_representations']
    assert len(persistence['genesis_ledgers']) == search['genesis_representations']
    for bundle in persistence['bundles']:
        assert not any(row.get('stage') in STAGES for row in bundle['events'])
    assert search['native_operations_or_replay'] == search['events_constructed'] == 0
    assert search['events_appended'] == search['authorities_issued'] == 0
    assert not native['barred_calls'] and native['A06_NATIVE_OPERATION_CALLS'] == 0
    assert native['native_events_created'] == native['native_replay_calls'] == 0
    for key in ('original_initial', 'original_handoff', 'original_post_decision_wait'):
        assert native[key]['gate']['stage']['value'] == 'WAITING_FOR_EXTERNAL_EVIDENCE'
        assert native[key]['gate']['history'] == []
        assert native[key]['model_admission'] == 'PASS'
        assert all(all(row['relations'].values()) for row in native[key]['resolution_contracts'])
    query = native['original_post_decision_wait']['read_only_wait_query']
    assert query['control'] == 'EXTERNAL_WAIT' and not query['actionable']
    assert not query['human_ready'] and query['selected'] is None
    assert query['obligation_proof']['state'] != 'PROVED'
    for key in ('P03_prospective_checkpoint', 'P04_canonical_target', 'A04_prospective_frontier'):
        assert not native[key]['request_wait_events']
        assert all(all(row['checks'].values()) for row in native[key]['events'])
        assert native[key]['native_result_application_or_replay'] == 'NOT_RUN'

    source_graph = json.loads((ROOT / frontier['source']['path']).read_bytes())
    assert frontier['stage_bindings'] == source_graph['stage_bindings']
    rows = frontier['stage_bindings']
    assert len(rows) == 13 and sum(row['binding_status'] == 'BOUND' for row in rows) == 12
    assert rows[5]['binding_status'] == 'MISSING_CANONICAL_OUTPUT'
    assert source_graph['additional_unresolved_END_gate'] == frontier['global_END_gap']
    assert not frontier['13_of_13_entry_gate_reached']
    assert frontier['P05_EXECUTION_READY'] == 'NO'
    subject_id = 'qualification-scope-subject-v1:' + hashlib.sha256(canonical(dossier['subject'])).hexdigest()
    assert subject_id == dossier['subject_identity'] == report['SCOPE_DECISION_SUBJECT_ID']
    assert dossier['options'] == dossier['subject']['scope_options'] == report['SCOPE_OPTIONS']
    assert dossier['selected_option'] == report['SELECTED_SCOPE_OPTION'] == 'NONE'
    assert not dossier['native_authority_issued'] and not dossier['A06_reproduced']
    assert not dossier['execution_contract_ready']
    assert all(not option['selected'] for option in dossier['options'])
    assert dossier['subject']['acceptable_alternate_native_trace'] is None
    assert assurance['END']['result'] == 'BLOCKED_MISSING_NATIVE_TRACE'
    assert assurance['N12']['result'] == assurance['N13']['result'] == 'NOT_CLOSED_FOR_A06'
    assert not assurance['N13']['inferred_from_N12']
    assert not assurance['END']['global_full_END_gap_waived']
    assert report['RESULT'] == 'BLOCKED' and report['LOSSLESS_RECOVERY'] == 'NO'
    assert report['TRACE_CLASSIFICATION'] == 'NO_NATIVE_TRACE'
    assert report['E2_A06_REQUEST_WAIT_EVENT_TRACE'] == 'FAIL'
    assert report['P05_BOUND_STAGE_INPUTS'] == 12 and report['P05_REQUIRED_STAGE_INPUTS'] == 13
    for key in ('P05_EXECUTED', 'P06_EXECUTED', 'A06_EXECUTED_OR_REPRODUCED',
                'RUNTIME_MODIFIED', 'PRODUCTION_EFFECT', 'N_REAL_SATISFIED'):
        assert report[key] == 'NO'
    for key in ('ORIGINAL_A03_HISTORICAL_OCCURRENCE', 'ORIGINAL_A04_HISTORICAL_ANCESTRY',
                'ORIGINAL_A05_HISTORICAL_ANCESTRY', 'ORIGINAL_A06_HISTORICAL_TRACE',
                'P03_HISTORICAL_CORRESPONDENCE'):
        assert report[key] == 'UNPROVEN'

    script_pins = []
    for script in sorted(OUT.glob('*.py')):
        ast.parse(script.read_text(), str(script))
        script_pins.append({'path': str(script.relative_to(ROOT)), 'raw_sha256': digest(script)})
    links = []
    md_path = REPORT.with_suffix('.md')
    for target in re.findall(r'\]\(([^)]+)\)', md_path.read_text()):
        source = re.sub(r':\d+$', '', target)
        resolved = (md_path.parent / source).resolve()
        assert resolved.is_file() or resolved == OUT / 'verification.json', target
        links.append(target)
    for path in [md_path, report_path] + list(OUT.glob('*.py')):
        assert all(line == line.rstrip() for line in path.read_text().splitlines()), path
    diff = subprocess.run(['git', 'diff', '--check'], cwd=str(ROOT), capture_output=True, text=True)
    assert diff.returncode == 0, diff.stdout + diff.stderr

    result = {
        'schema': 'E2-P05-A06-RECOVERY-VERIFICATION-1', 'RESULT': 'PASS',
        'verification_scope': 'Read-only recovery metadata, native decode/hash inspections and preservation; no lifecycle execution or native replay',
        'preexisting_files_checked': len(baseline), 'preexisting_files_changed': changed,
        'preexisting_files_missing': missing,
        'new_files': new_files, 'all_new_files_are_recovery_reports_or_metadata': True,
        'native_runtime_files_unchanged': sum(name.startswith('adapter/planner/') for name in baseline),
        'adapter_files_unchanged': sum(name.startswith('adapter/') for name in baseline),
        'frozen_E1_files_unchanged': sum(name.startswith('docs/experiments/E1/') for name in baseline),
        'E1_ARTIFACTS_MODIFIED': 0, 'RUNTIME_MODIFIED': 'NO',
        'pinned_source_files_verified': len(pins), 'strict_native_JSON_pointers_verified': len(strict_pointers),
        'new_JSON_documents_parseable': len(docs) + 1, 'new_scripts_syntax': 'PASS',
        'script_pins': script_pins, 'local_report_links_checked': len(links),
        'report_and_companion_pins': [
            {'path': str(path.relative_to(ROOT)), 'raw_sha256': digest(path)}
            for path in (md_path, report_path)],
        'subject_identity': subject_id, 'subject_hash_exact': True,
        'selected_scope_option': 'NONE', 'native_authorities_issued': 0,
        'native_occurrence_events_created_or_appended': 0, 'native_lifecycle_or_replay_calls': 0,
        'request_wait_native_events_found': 0, 'request_wait_native_commands_found': 0,
        'lossless_native_event_identity_bodies_found': 0,
        'P05_graph_source_unchanged': True, 'all_12_prior_bound_rows_unchanged': True,
        'P05_BOUND_STAGE_INPUTS': 12, 'P05_REQUIRED_STAGE_INPUTS': 13, 'P05_EXECUTION_READY': 'NO',
        'original_history_limits_preserved': True, 'independent_N12_N13_mapping_not_promoted_to_PASS': True,
        'no_complete_alternate_trace_or_selected_replacement': True,
        'git_diff_check': 'PASS', 'new_evidence_whitespace': 'PASS'}
    (OUT / 'verification.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps({'verification': 'PASS', 'baseline_files_unchanged': len(baseline),
                      'E1_unchanged': result['frozen_E1_files_unchanged'],
                      'P05_bound': 12, 'scope_option_selected': 'NONE', 'git_diff_check': 'PASS'}))


if __name__ == '__main__':
    main()
