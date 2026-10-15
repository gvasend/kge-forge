"""Read-only representation readers and preservation audit, never A04."""
import argparse
import ast
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from dataclasses import fields, replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
REPORT = ROOT / 'docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_P05_A04_EVENT_VALIDATION_RECONCILIATION_1.json'
MARKDOWN = REPORT.with_suffix('.md')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reader(mode):
    spec = importlib.util.spec_from_file_location('a04_reconciliation', OUT / 'reconcile.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.guard()
    c, m = module.c, module.m
    result = json.loads(REPORT.read_bytes())
    assert result['RESULT'] == 'PASS' and result['PRIMARY_CLASSIFICATION'] == 'COMBINED'
    assert result['CLASSIFICATION_COMPONENTS'] == ['DOSSIER_OVERCONSTRAINED_EVENT_PAYLOAD', 'MISSING_ATOMIC_TRANSACTION_CAPABILITY']
    assert result['A04_EXECUTED'] == result['P05_EXECUTED'] == result['RUNTIME_MODIFIED'] == 'NO'
    assert result['PROSPECTIVE_A04_EXECUTION_READY'] == 'NO' and result['P05_BOUND_STAGE_INPUTS'] == 10
    assert result['CONTRACT_REVISION_APPLIED'] == 'YES_AS_VERSIONED_OVERLAY'
    assert result['N12_MAPPING']['mapping'] == result['N13_MAPPING']['mapping'] == 'PRESERVED'
    assert result['P05_ANCESTRY_ASSURANCE']['event_ancestry_requirement_retained']
    assert not result['P05_ANCESTRY_ASSURANCE']['state_only_evidence_accepted']
    assert len(result['DOSSIER_VALIDATIONS']) == 6
    for pin in result['evidence'].values():
        assert sha(ROOT / pin['path']) == pin['raw_sha256'], pin['path']
    for pin in json.loads((OUT / 'source-pins.json').read_bytes())['pins']:
        assert sha(ROOT / pin['path']) == pin['raw_sha256'], pin['path']
    overlay = json.loads((OUT / 'contract-revision-overlay.json').read_bytes())
    assert not overlay['prior_sealed_files_modified']
    prior = json.loads((ROOT / overlay['base_contract']['path']).read_bytes())
    assert prior['RESULT'] == 'PARTIAL'
    assert result['SELECTED_OPTION'] == prior['SELECTED_OPTION']
    assert result['AUTHORIZATION_SUBJECT'] == prior['AUTHORITATIVE_QUALIFICATION_SCOPE_SUBJECT']
    event_oracle = json.loads((OUT / 'oracles/composite-representation.json').read_bytes())
    assert not event_oracle['event_appended'] and not event_oracle['after_snapshot_is_occurred_state']
    event = c._unwire(event_oracle['native_event'])
    after = c._unwire(prior['EXPECTED_RESULT_ORACLE']['expected_post_state'])
    supplied = c._unwire(prior['EXPECTED_RESULT_ORACLE']['expected_result'])
    start = c._unwire(c.parse_json((ROOT / prior['PROSPECTIVE_START']['START_PATH']['path']).read_bytes())['bundle'])
    assert len(start.events) == 2 and not start.current.validation_instances
    m.validate_types(event, m.ExecutionEvent)
    assert event.result == supplied
    assert event.sequence == 3 and event.parent_event == start.events[-1].identity
    assert event.parent_snapshot == c.snapshot_id(start.current) == supplied.expected_snapshot
    assert event.after_snapshot == c.snapshot_id(after)
    assert event.identity == c._event_identity(3, event.parent_snapshot, event.parent_event, supplied, event.after_snapshot)
    assert module.text_id(event.identity) == result['EXPECTED_REPRESENTATIONAL_EVENT_ID']
    assert c._unwire(c._wire(event)) == event
    after_dossier_id = c._identity(c.canonical_bytes(c._wire(supplied.dossier)), 'planner-dossier-sha256')
    for item in result['DOSSIER_VALIDATIONS']:
        selector = item['IMMUTABLE_MEMBER_BINDING']
        assert c._unwire(selector['snapshot']) == event.after_snapshot
        pid, did = c._unwire(selector['predicate']), c._unwire(selector['dossier'])
        matching = [v for v in after.validation_instances if v.predicate == pid]
        assert len(matching) == 1
        v = matching[0]
        assert v.dossier == did == after_dossier_id
        assert c.canonical_bytes(c._wire(v)) == c.canonical_bytes(item['EXPECTED_NATIVE_VALUE'])
        assert v.result is m.ValidationOutcome.PASS and v.currentness is m.ValidationState.ACCEPTED
        assert (v.scope, v.lineage) == (after.context.scope, after.context.lineage)
        assert v.inputs == (event.parent_snapshot, supplied.dossier.provenance.identity)
        assert not item['ACTUAL_INSTANCE_ADMITTED']
    for collection in ('actions', 'statuses', 'knowledge', 'validation_instances'):
        values = getattr(after, collection)
        presentation = values[::-1] if mode == 'reverse' else values[1:] + values[:1] if mode == 'rotate' else values
        assert c.snapshot_id(replace(after, **{collection: presentation})) == event.after_snapshot
    assert 'validation_instances' not in {f.name for f in fields(m.SuppliedResult)}
    assert result['NATIVE_VALIDATION_REPRESENTATION']['standalone_native_identity'] is False
    assert result['NATIVE_EVENT_SCHEMA']['inline_validation_instances'] is False
    assert result['NATIVE_CORRELATION']['C_complete_A04_durable_transaction_already_native'] == 'NO'
    assert len(prior['NEGATIVE_SUITE']) == 24 and all(n['status'] == 'SEALED_NOT_RUN' for n in prior['NEGATIVE_SUITE'])
    assert not module.BARRED
    return {'role': 'STATIC_REPRESENTATION_READER_NO_EXECUTION_OR_NATIVE_REPLAY', 'result': 'PASS',
            'hash_seed': os.environ['PYTHONHASHSEED'], 'presentation': mode,
            'representational_event_id': module.text_id(event.identity), 'post_state_ORACLE_ONLY': module.text_id(event.after_snapshot),
            'validation_selectors': sorted(v.predicate.value for v in after.validation_instances),
            'barred_calls': module.BARRED, 'contract_sha256': sha(REPORT)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reader', choices=['original', 'reverse', 'rotate'])
    args = parser.parse_args()
    if args.reader:
        print(json.dumps(reader(args.reader), sort_keys=True))
        return
    readers = []
    for seed in (0, 1, 7, 101):
        for mode in ('original', 'reverse', 'rotate'):
            env = dict(os.environ, PYTHONHASHSEED=str(seed), PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(ROOT))
            output = subprocess.check_output([sys.executable, str(Path(__file__).resolve()), '--reader', mode], cwd=str(ROOT), env=env)
            readers.append(json.loads(output))
    assert len({(r['representational_event_id'], r['post_state_ORACLE_ONLY']) for r in readers}) == 1
    baseline = json.loads((OUT / 'baseline.json').read_bytes())
    altered = [path for path, old in baseline['files'].items() if not (ROOT / path).is_file() or sha(ROOT / path) != old]
    assert not altered, altered
    current = set()
    for prefix in ('docs/plans', 'adapter/planner', 'docs/experiments/E1'):
        current.update(str(p.relative_to(ROOT)) for p in (ROOT / prefix).rglob('*')
                       if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
    additions = sorted(current - set(baseline['files']))
    out_prefix = str(OUT.relative_to(ROOT)) + '/'
    allowed = {str(REPORT.relative_to(ROOT)), str(MARKDOWN.relative_to(ROOT))}
    assert all(x.startswith(out_prefix) or x in allowed for x in additions)
    assert REPORT.is_file() and MARKDOWN.is_file()
    for p in OUT.glob('*.py'):
        ast.parse(p.read_text())
    diff = subprocess.run(['git', 'diff', '--check'], cwd=str(ROOT), stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, universal_newlines=True)
    assert diff.returncode == 0, diff.stdout + diff.stderr
    verification = {
        'schema': 'A04-EVENT-VALIDATION-RECONCILIATION-VERIFICATION-1', 'RESULT': 'PASS',
        'check_scope': 'Representation/schema/native hash membership and immutable input preservation; no execution qualification',
        'independent_static_reader_count': len(readers), 'readers': readers,
        'schema_and_member_correlation': 'PASS', 'representation_hash_permutations': 'PASS',
        'actual_A04_execution': 'NOT_RUN', 'native_event_commit_and_ledger_replay': 'NOT_RUN',
        'future_24_negative_runtime_suite': 'NOT_RUN',
        'preexisting_files_checked': len(baseline['files']), 'modified_preexisting_files': altered,
        'runtime_files_checked': baseline['runtime_file_count'], 'E1_files_checked': baseline['frozen_E1_file_count'],
        'new_files': additions, 'report_sha256': sha(REPORT), 'markdown_sha256': sha(MARKDOWN),
        'verify_script_sha256': sha(Path(__file__).resolve()),
        'RUNTIME_MODIFIED': 'NO', 'E1_ARTIFACTS_MODIFIED': 0, 'PRODUCTION_EFFECT': 'NO',
        'P05_BOUND_STAGE_INPUTS': 10, 'PROSPECTIVE_A04_EXECUTION_READY': 'NO', 'git_diff_check': 'PASS',
    }
    (OUT / 'verification.json').write_text(json.dumps(verification, sort_keys=True, indent=2) + '\n')
    print(json.dumps({k: verification[k] for k in ('RESULT', 'independent_static_reader_count', 'preexisting_files_checked',
         'modified_preexisting_files', 'runtime_files_checked', 'E1_files_checked', 'git_diff_check')}, sort_keys=True))


if __name__ == '__main__':
    main()
