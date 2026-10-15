"""Read-only contract checks, independent processes, and preservation audit.

These checks do not execute or qualify PREPARE. Native replay/result/append
entry points are barred in every reader.
"""
import argparse
import ast
import hashlib
import json
import os
import subprocess
import sys
from dataclasses import fields, replace
from pathlib import Path
from typing import get_type_hints, get_args

from adapter.planner import codec as c, core, model as m

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
REPORT = ROOT / 'docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_P05_A04_PROSPECTIVE_ANCESTRY_CONTRACT_1.json'
MARKDOWN = REPORT.with_suffix('.md')
BARRED_CALLS = []


def canonical(value):
    return c.canonical_bytes(value)


def text_id(value):
    return value.namespace + ':' + value.sha256


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def guards():
    def forbidden(name):
        def fail(*args, **kwargs):
            BARRED_CALLS.append(name)
            raise AssertionError('A04 execution is forbidden: ' + name)
        return fail
    for mod, names in (
        (core, ('apply_result', 'apply_event', '_inventory', '_decision_result', 'recompute',
                'admit_dossier_materialization', 'apply_recorded_decision', 'apply_decision_reentry')),
        (c, ('record_result', 'append_event', 'commit_event', 'commit_result', '_replay',
             'decode_bundle', 'bundle_bytes', 'apply_event', 'replay')),
    ):
        for name in names:
            if hasattr(mod, name):
                setattr(mod, name, forbidden(mod.__name__ + '.' + name))


def check_pin(row):
    assert digest(ROOT / row['path']) == row['raw_sha256'], row['path']


def permute(items, mode):
    if mode == 'reverse':
        return items[::-1]
    if mode == 'rotate' and items:
        return items[1:] + items[:1]
    return items


def read_contract(mode):
    guards()
    contract = json.loads(REPORT.read_bytes())
    assert contract['RESULT'] == 'PARTIAL' and contract['PROSPECTIVE_A04_EXECUTION_READY'] == 'NO'
    assert contract['PROSPECTIVE_A04_EXECUTED'] == contract['P05_EXECUTED'] == contract['P06_EXECUTED'] == 'NO'
    assert contract['P05_BOUND_STAGE_INPUTS'] == 10
    assert contract['ORIGINAL_A04_HISTORICAL_ANCESTRY'] == 'UNPROVEN'
    assert contract['HISTORICAL_RECONSTRUCTION'] == contract['PROSPECTIVE_A04_EVENT_IS_ORIGINAL_EVENT'] == 'NO'
    assert contract['QUALIFICATION_TYPE'] == 'PROSPECTIVE_REPLACEMENT'
    assert contract['ADDITIONAL_AUTHORITY_REQUIRED'] == 'NO'
    assert contract['N12_MAPPING_PRESERVED'] == contract['N13_MAPPING_PRESERVED'] == 'YES'
    for row in contract['EVIDENCE'].values():
        check_pin(row)
    reference_pins = json.loads((OUT / 'authoritative-inputs.json').read_bytes())
    for row in reference_pins['pins'] + reference_pins['runtime_files']:
        check_pin(row)
    scope_path = ROOT / contract['AUTHORITY']['QUALIFICATION_SCOPE_AUTHORIZATION']['retained_dossier']['path']
    scope = json.loads(scope_path.read_bytes())
    subject_id = 'qualification-scope-subject-v1:' + hashlib.sha256(canonical(scope['subject'])).hexdigest()
    assert subject_id == contract['AUTHORITATIVE_QUALIFICATION_SCOPE_SUBJECT'] == scope['subject_identity']
    assert contract['SELECTED_OPTION'] == 'AUTHORIZE_PROSPECTIVE_P05_A04_ANCESTRY_QUALIFICATION'

    spec = contract['PROSPECTIVE_START']
    start_path = ROOT / spec['START_PATH']['path']
    check_pin(spec['START_PATH'])
    bundle = c._unwire(c.parse_json(start_path.read_bytes())['bundle'])
    m.validate_types(bundle, m.PersistenceBundle)
    assert start_path.read_bytes() == c._bundle_bytes_admitted(bundle)
    assert text_id(c._identity(start_path.read_bytes(), 'planner-bundle-v1')) == spec['START_BUNDLE_ID']
    assert text_id(c.snapshot_id(bundle.current)) == spec['START_STATE_ID']
    assert spec['LEDGER_ID'] == spec['START_BUNDLE_ID'] + '#/bundle/events'
    assert len(bundle.events) == 2 and bundle.current.context.lineage != 'E2-CANONICAL-BASELINE-1'
    before_id, parent_id = c.snapshot_id(bundle.initial), None
    for i, e in enumerate(bundle.events, 1):
        assert e.sequence == i and e.parent_event == parent_id and e.parent_snapshot == before_id
        assert e.identity == c._event_identity(i, before_id, parent_id, e.result, e.after_snapshot, e.resume_binding)
        before_id, parent_id = e.after_snapshot, e.identity
    assert before_id == c.snapshot_id(bundle.current)
    assert text_id(parent_id) == spec['PARENT_EVENT_ID'] == spec['APPEND_HEAD']
    assert text_id(bundle.events[0].identity) == spec['LEDGER_ROOT']
    c._verify_sources(bundle, ROOT)
    action = next(a for a in bundle.current.actions if a.id.value == 'E2-PREPARE')
    decision = next(d for d in bundle.current.decisions if d.input_action == action.id)
    assert action.prepared_dossier is None and action.authority is None
    assert decision.dossier is None and decision.record is None and decision.recorded_choice is None
    assert not bundle.current.validation_instances
    assert 'E2-K-PREPARE' not in {k.id.value for k in bundle.current.knowledge}

    oracle = contract['EXPECTED_RESULT_ORACLE']
    expected = c._unwire(oracle['expected_post_state'])
    result = c._unwire(oracle['expected_result'])
    instances = c._unwire(oracle['expected_validation_instances'])
    m.validate_model(expected)
    assert result.expected_snapshot == c.snapshot_id(bundle.current)
    assert result.action == action.id and result.result is m.ActionResult.PASS
    assert result.knowledge == action.accepted_inventory
    assert len(instances) == 6
    assert {v.proposition for v in instances} == {x.value for x in m.SUPPORTED_DOSSIER_CHECKS}
    expected_dossier_id = c._identity(canonical(c._wire(result.dossier)), 'planner-dossier-sha256')
    assert text_id(expected_dossier_id) == oracle['expected_dossier_id']
    for v in instances:
        assert v.dossier == expected_dossier_id and v.result is m.ValidationOutcome.PASS
        assert v.currentness is m.ValidationState.ACCEPTED
        assert (v.scope, v.lineage) == (bundle.current.context.scope, bundle.current.context.lineage)
    assert {k.id.value for k in expected.knowledge} == {'E2-K-CHECK', 'E2-K-COLLECT', 'E2-K-PREPARE'}
    assert next(s for s in expected.statuses if s.id == action.id).state is m.ActionState.COMPLETED
    assert next(s for s in expected.statuses if s.id == decision.action).state is m.ActionState.ACTIONABLE
    assert next(d for d in expected.decisions if d.action == decision.action).stage is m.DecisionStage.DECISION_READY
    assert next(d for d in expected.decisions if d.action == decision.action).record is None
    for field in fields(m.Snapshot):
        if field.name not in ('actions', 'statuses', 'knowledge', 'decisions', 'validation_instances'):
            assert getattr(expected, field.name) == getattr(bundle.current, field.name)
    assert text_id(c.snapshot_id(expected)) == oracle['expected_post_state_id']
    new_source = contract['EXPECTED_EVENT_ORACLE']['EVENT_PAYLOAD']['source_additions'][0]
    native_pin = c._unwire(new_source)
    assert native_pin not in bundle.sources
    assert digest(ROOT / native_pin.path) == native_pin.identity.sha256
    assert result.dossier.provenance.path == native_pin.path
    assert all(v.provenance.path == native_pin.path for v in instances)

    event_spec = contract['EXPECTED_EVENT_ORACLE']
    assert event_spec['EXPECTED_EVENT_ID'] is None and not event_spec['native_payload_oracle_complete']
    assert event_spec['PARENT_EVENT_ID'] == spec['APPEND_HEAD']
    assert event_spec['PRE_STATE_ID'] == spec['START_STATE_ID']
    assert event_spec['POST_STATE_ID'] == oracle['expected_post_state_id']
    union = get_args(get_type_hints(m.ExecutionEvent)['result'])
    assert [t.__name__ for t in union] == contract['NATIVE_INTERFACE_GAP']['supported_event_result_variants']
    assert 'validation_instances' not in {f.name for f in fields(m.SuppliedResult)}
    assert event_spec['EVENT_PAYLOAD']['current_durable_native_variant'] == 'ABSENT'
    assert not event_spec['EVENT_PAYLOAD']['wire_tag_added']
    assert contract['END_MAPPING']['prospective_binding']['status'] == 'NOT_EXECUTED_NOT_BOUND'
    assert contract['END_MAPPING']['original_historical_binding']['original_event_id'] is None
    assert contract['END_MAPPING']['maximum_stage_count_after_A04_only'] == 11
    assert len(contract['NEGATIVE_SUITE']) == 24
    assert all(n['status'] == 'SEALED_NOT_RUN' for n in contract['NEGATIVE_SUITE'])
    assert contract['READINESS_GATES']['gates']['native_event_payload_oracle_complete'] == 'FAIL'
    assert contract['READINESS_GATES']['gates']['native_durable_event_path_qualified'] == 'FAIL'

    # Only presentation permutations declared unordered by the native codec.
    def presentation(snapshot):
        changes = {f: permute(getattr(snapshot, f), mode) for f in c.SET_FIELDS[m.Snapshot]
                   if type(getattr(snapshot, f)) is tuple}
        return replace(snapshot, **changes)
    permuted_start = replace(bundle, initial=presentation(bundle.initial),
        current=presentation(bundle.current), sources=permute(bundle.sources, mode))
    assert c._bundle_bytes_admitted(permuted_start) == c._bundle_bytes_admitted(bundle)
    expected_presentation = presentation(expected)
    new_dossier = replace(result.dossier,
        **{f: permute(getattr(result.dossier, f), mode) for f in c.SET_FIELDS[m.DecisionDossier]})
    assert canonical(c._wire(new_dossier)) == canonical(c._wire(result.dossier))
    assert c.snapshot_id(expected_presentation) == c.snapshot_id(expected)
    assert not BARRED_CALLS
    return {
        'role': 'CONTRACT_STATIC_READER_NOT_A04_EXECUTION_QUALIFICATION',
        'result': 'PASS', 'hash_seed': os.environ.get('PYTHONHASHSEED'), 'presentation': mode,
        'contract_sha256': digest(REPORT), 'start_bundle_id': spec['START_BUNDLE_ID'],
        'expected_post_state_ORACLE_ONLY': oracle['expected_post_state_id'],
        'scope_subject_id': subject_id, 'forbidden_calls': BARRED_CALLS,
        'native_durable_event_path': 'MISSING', 'A04_execution': 'NOT_RUN',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reader', choices=['original', 'reverse', 'rotate'])
    args = parser.parse_args()
    if args.reader:
        print(json.dumps(read_contract(args.reader), sort_keys=True))
        return
    readers = []
    for seed in (0, 1, 7, 101):
        for mode in ('original', 'reverse', 'rotate'):
            env = dict(os.environ, PYTHONHASHSEED=str(seed), PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(ROOT))
            raw = subprocess.check_output([sys.executable, str(Path(__file__).resolve()), '--reader', mode],
                                          cwd=str(ROOT), env=env)
            readers.append(json.loads(raw))
    assert len({(r['start_bundle_id'], r['expected_post_state_ORACLE_ONLY'], r['scope_subject_id'])
                for r in readers}) == 1
    baseline = json.loads((OUT / 'baseline.json').read_bytes())
    changed = [path for path, old in baseline['files'].items()
               if not (ROOT / path).is_file() or digest(ROOT / path) != old]
    assert not changed, changed
    current = set()
    # Audit the same preservation roots. New files must be our two requested
    # reports or this one qualification directory, never runtime or E1.
    frozen = 'docs/experiments/E1'
    for directory in ('docs/plans', 'adapter/planner', frozen):
        current.update(str(p.relative_to(ROOT)) for p in (ROOT / directory).rglob('*')
                       if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
    prefix = str(OUT.relative_to(ROOT)) + '/'
    allowed_report = {str(REPORT.relative_to(ROOT)), str(MARKDOWN.relative_to(ROOT))}
    added = sorted(current - set(baseline['files']))
    assert all(path.startswith(prefix) or path in allowed_report for path in added), added
    assert REPORT.is_file() and MARKDOWN.is_file()
    for p in OUT.glob('*.py'):
        ast.parse(p.read_text())
    diff = subprocess.run(['git', 'diff', '--check'], cwd=str(ROOT), stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, universal_newlines=True)
    assert diff.returncode == 0, diff.stdout + diff.stderr
    result = {
        'schema': 'A04-PROSPECTIVE-CONTRACT-VERIFICATION-1', 'result': 'PASS',
        'qualification_type': 'CONTRACT_ONLY_NO_A04_EXECUTION',
        'report_sha256': digest(REPORT), 'markdown_sha256': digest(MARKDOWN),
        'validate_seal_sha256': digest(Path(__file__).resolve()),
        'readers': readers, 'static_independent_reader_count': len(readers),
        'static_identity_permutation_comparison': 'PASS',
        'positive_A04_path': 'NOT_RUN', 'runtime_cold_restore_replay': 'NOT_RUN',
        'negative_execution': 'NOT_RUN', 'negative_contract_count': 24,
        'preexisting_files_checked': len(baseline['files']), 'changed_preexisting_files': changed,
        'frozen_E1_files_checked': baseline['frozen_E1_root_file_count'],
        'runtime_files_checked': baseline['runtime_file_count'], 'new_files': added,
        'inventory_exclusions': ['__pycache__ directories', '.pyc files; same scope as inherited baseline'],
        'PROSPECTIVE_A04_EXECUTION_READY': 'NO', 'P05_BOUND_STAGE_INPUTS': 10,
        'RUNTIME_MODIFIED': 'NO', 'E1_ARTIFACTS_MODIFIED': 0, 'PRODUCTION_EFFECT': 'NO',
        'git_diff_check': 'PASS',
    }
    (OUT / 'verification.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('result', 'static_independent_reader_count',
        'preexisting_files_checked', 'frozen_E1_files_checked', 'runtime_files_checked',
        'changed_preexisting_files', 'git_diff_check')}, sort_keys=True))


if __name__ == '__main__':
    main()
