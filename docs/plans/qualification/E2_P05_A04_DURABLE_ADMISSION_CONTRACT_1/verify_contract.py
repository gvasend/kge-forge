"""Fresh static readers and preservation audit, never native execution/replay."""
import argparse
import ast
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from dataclasses import fields, replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
REPORT = ROOT / 'docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_P05_A04_DURABLE_ADMISSION_CONTRACT_1.json'
MARKDOWN = REPORT.with_suffix('.md')


def read(path):
    return json.loads(Path(path).read_bytes())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def reader(mode):
    spec = importlib.util.spec_from_file_location('a04_durable_contract', OUT / 'seal_contract.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.guard()
    c, m = module.c, module.m
    report = read(REPORT)
    assert report['RESULT'] == 'PASS'
    assert report['A04_DURABLE_TRANSACTION_IMPLEMENTATION_READY'] == 'YES'
    assert report['PROSPECTIVE_A04_EXECUTION_READY'] == 'NO'
    assert report['EXISTING_PATH_SATISFIES_CONTRACT_UNCHANGED'] == 'NO'
    assert report['A04_EXECUTED'] == report['P05_EXECUTED'] == report['P06_EXECUTED'] == 'NO'
    assert report['RUNTIME_MODIFIED'] == 'NO' and report['E1_ARTIFACTS_MODIFIED'] == 0
    assert report['P05_BOUND_STAGE_INPUTS'] == 10
    assert report['QUALIFICATION_TYPE'] == 'PROSPECTIVE_REPLACEMENT'
    assert report['ORIGINAL_A04_HISTORICAL_ANCESTRY'] == report['ORIGINAL_A03_HISTORICAL_OCCURRENCE'] == 'UNPROVEN'
    assert report['HISTORICAL_RECONSTRUCTION'] == report['PROSPECTIVE_A04_EVENT_IS_ORIGINAL_EVENT'] == 'NO'
    assert report['N_REAL_SATISFIED'] == 'NO'
    assert all(value == 'COMPLETE_CONTRACT_NOT_RUNTIME_QUALIFICATION'
               for value in report['IMPLEMENTATION_READINESS_GATES'].values())
    assert len(report['IMPLEMENTATION_READINESS_GATES']) == 11
    for pin in report['evidence'].values():
        assert sha(ROOT / pin['path']) == pin['raw_sha256'], pin['path']
    for pin in read(OUT / 'source-pins.json')['pins']:
        assert sha(ROOT / pin['path']) == pin['raw_sha256'], pin['path']
    overlay = read(OUT / 'versioned-overlay.json')
    assert not overlay['prior_sealed_artifacts_rewritten']
    for pin in overlay['preserved_files']:
        assert sha(ROOT / pin['path']) == pin['raw_sha256']
    old = read(ROOT / overlay['base_contract']['path'])
    assert old['RESULT'] == 'PARTIAL'
    assert report['SELECTED_OPTION'] == old['SELECTED_OPTION']
    assert report['AUTHORIZATION_SUBJECT'] == overlay['authorization_subject'] == old['AUTHORITATIVE_QUALIFICATION_SCOPE_SUBJECT']

    oracle = read(OUT / 'oracles/prospective-native-binding.json')
    assert not oracle['actual_execution_occurrence'] and not oracle['P05_binding_applied']
    assert not oracle['future_bundle_schema_currently_supported']
    rep = read(ROOT / oracle['native_event_oracle']['path'])
    event = c._unwire(rep['native_event'])
    supplied = c._unwire(old['EXPECTED_RESULT_ORACLE']['expected_result'])
    after = c._unwire(old['EXPECTED_RESULT_ORACLE']['expected_post_state'])
    start_path = ROOT / old['PROSPECTIVE_START']['START_PATH']['path']
    start = c._unwire(c.parse_json(start_path.read_bytes())['bundle'])
    before_id = c._identity(start_path.read_bytes(), 'planner-bundle-v1')
    assert c._bundle_bytes_admitted(start) == start_path.read_bytes()
    assert module.text_id(before_id) == oracle['EXPECTED_PRE_BUNDLE_ID']
    assert len(start.events) == 2 and not start.current.validation_instances
    assert event.sequence == 3 and oracle['array_index'] == 2
    assert event.parent_event == start.events[-1].identity
    assert event.parent_snapshot == c.snapshot_id(start.current) == supplied.expected_snapshot
    assert event.result == supplied and event.after_snapshot == c.snapshot_id(after)
    assert event.identity == c._event_identity(3, event.parent_snapshot, event.parent_event, supplied, event.after_snapshot)
    assert module.text_id(event.identity) == oracle['EXPECTED_EVENT_ID'] == report['COMPARISON_EVENT_ID']
    assert c._unwire(c._wire(event)) == event
    assert hashlib.sha256(c.snapshot_bytes(after)).hexdigest() == oracle['archive_expected_raw_sha256'] == event.after_snapshot.sha256
    assert module.text_id(event.after_snapshot) == report['COMPARISON_POST_SNAPSHOT_ID']
    assert {f.name for f in fields(m.ExecutionEvent)} == set(oracle['existing_event_schema'])
    assert 'validation_instances' not in {f.name for f in fields(m.SuppliedResult)}
    assert 'dossier_materializations' not in {f.name for f in fields(m.PersistenceBundle)}

    storage = read(OUT / 'snapshot-event-binding.json')
    binding_fields = storage['new_binding_type']['fields']
    assert [x['name'] for x in binding_fields] == ['event_identity', 'expected_bundle', 'source_additions']
    assert not storage['new_binding_type']['standalone_identity']
    assert storage['bundle_extension']['default'] == []
    assert 'validation_instances' in c.SET_FIELDS[m.Snapshot]
    assert 'inputs' not in c.SET_FIELDS.get(m.ValidationInstance, set())
    dossier_id = c._identity(c.canonical_bytes(c._wire(supplied.dossier)), 'planner-dossier-sha256')
    assert len(after.validation_instances) == len(storage['A04_member_bindings']) == 6
    for selector in storage['A04_member_bindings']:
        assert c._unwire(selector['snapshot']) == event.after_snapshot
        pid, did = c._unwire(selector['predicate']), c._unwire(selector['dossier'])
        matches = [v for v in after.validation_instances if v.predicate == pid]
        assert len(matches) == 1
        member = matches[0]
        assert member.dossier == did == dossier_id
        assert member.inputs == c._unwire(selector['ordered_inputs']) == (event.parent_snapshot, supplied.dossier.provenance.identity)
        assert member.currentness is m.ValidationState.ACCEPTED and member.result is m.ValidationOutcome.PASS
        assert (member.scope, member.lineage) == (start.current.context.scope, start.current.context.lineage)

    for collection in ('actions', 'statuses', 'knowledge', 'validation_instances'):
        values = getattr(after, collection)
        presentation = values[::-1] if mode == 'reverse' else values[1:] + values[:1] if mode == 'rotate' else values
        assert c.snapshot_id(replace(after, **{collection: presentation})) == event.after_snapshot

    pin = c._unwire(storage['A04_expected_source_additions'][0])
    assert pin not in start.sources and sha(ROOT / pin.path) == pin.identity.sha256
    binding = {'$type': 'DossierMaterializationBinding', 'event_identity': c._wire(event.identity),
               'expected_bundle': c._wire(before_id), 'source_additions': c._wire((pin,))}
    assert binding == oracle['binding_future_wire']
    projected_wire = c._wire(replace(start, events=start.events + (event,), current=after, sources=start.sources + (pin,)))
    projected_wire['dossier_materializations'] = [binding]
    future = {'schema': 'PLANNER-BUNDLE-1', 'bundle': projected_wire}
    assert future == oracle['future_bundle_wire']
    future_id = c._identity(c.canonical_bytes(future), 'planner-bundle-v1')
    assert module.text_id(future_id) == report['COMPARISON_FUTURE_BUNDLE_ID'] == oracle['EXPECTED_FUTURE_BUNDLE_ID_COMPARISON_ONLY']
    # Verify the currently missing capability remains missing. No registry patch.
    try:
        c._unwire(projected_wire)
    except m.PlannerError:
        pass
    else:
        raise AssertionError('future binding unexpectedly supported by current native codec')
    # The specified default omission leaves old bundle identity exact.
    old_wire = c._wire(start)
    assert 'dossier_materializations' not in old_wire
    assert c.canonical_bytes({'schema': 'PLANNER-BUNDLE-1', 'bundle': old_wire}) == start_path.read_bytes()

    identity = read(OUT / 'identity-order.json')
    assert identity['IDENTITY_CYCLE'] == report['IDENTITY_CYCLE'] == 'NO'
    order = identity['nodes_in_topological_order']
    assert len(set(order)) == len(order)
    assert all(order.index(a) < order.index(b) for a, b in identity['edges'])
    assert identity['event_payload_unchanged'] and identity['result_schema_unchanged'] and identity['snapshot_schema_unchanged']
    assert identity['no_new_identity_domains']

    # Pure native hash probes: changing a covered value changes Snapshot and event.
    member = after.validation_instances[0]
    changed = replace(member, provenance=replace(member.provenance, section=member.provenance.section + '/changed'))
    changed_after = replace(after, validation_instances=(changed,) + after.validation_instances[1:])
    changed_id = c.snapshot_id(changed_after)
    assert changed_id != event.after_snapshot
    assert c._event_identity(3, event.parent_snapshot, event.parent_event, supplied, changed_id) != event.identity
    changed_binding = dict(binding, expected_bundle=c._wire(replace(before_id, sha256='0' * 64)))
    changed_wire = dict(projected_wire, dossier_materializations=[changed_binding])
    assert c._identity(c.canonical_bytes({'schema': 'PLANNER-BUNDLE-1', 'bundle': changed_wire}), 'planner-bundle-v1') != future_id
    try:
        c.snapshot_id(replace(after, validation_instances=after.validation_instances + (member,)))
    except m.PlannerError:
        pass
    else:
        raise AssertionError('duplicate PredicateId accepted')

    negatives = read(OUT / 'negative-contract.json')
    assert len(negatives['durable_cases']) == negatives['inherited_count'] == len(old['NEGATIVE_SUITE']) == 24
    assert all(x['status'] == 'SEALED_NOT_RUN' for x in negatives['durable_cases'] + old['NEGATIVE_SUITE'])
    required = {'wrong PrepareResult', 'result not actually executed', 'wrong pre-state', 'wrong parent',
                'wrong post-Snapshot', 'tampered post-state', 'wrong event', 'wrong ledger', 'wrong append head',
                'validation bound to different Snapshot', 'missing validation binding', 'event without result',
                'result without event', 'duplicate retry', 'conflicting retry', 'replay creating second occurrence'}
    assert required.issubset({x['case'] for x in negatives['durable_cases']})
    replay = read(OUT / 'replay-contract.json')
    assert replay['status'] == 'SEALED_CONTRACT_NOT_IMPLEMENTED_OR_QUALIFIED'
    assert 'never call the live producer' in '\n'.join(replay['algorithm'])
    assert report['ACTUAL_DURABLE_TRANSACTION'] == report['ACTUAL_COLD_RESTORE'] == report['ACTUAL_REPLAY'] == 'NOT_RUN'
    assert report['ACTUAL_NEGATIVE_QUALIFICATION'] == 'NOT_RUN'
    assert not module.BARRED
    return {'role': 'STATIC_CONTRACT_IDENTITY_READER_NO_LIFECYCLE_OR_NATIVE_REPLAY', 'RESULT': 'PASS',
        'hash_seed': os.environ['PYTHONHASHSEED'], 'presentation': mode,
        'comparison_event_id': module.text_id(event.identity),
        'comparison_post_snapshot_id': module.text_id(event.after_snapshot),
        'comparison_future_bundle_id': module.text_id(future_id),
        'contract_sha256': sha(REPORT), 'barred_calls': module.BARRED,
        'checks': ['input/oracle pins preserved', 'native result/event/Snapshot schema and exact identities',
                   'unordered presentations and typed member selectors', 'default-omission compatibility contract',
                   'unimplemented bundle codec extension remains rejected', 'hash-bound mutation distinction',
                   'duplicate member rejection', 'identity DAG acyclic', 'negative expectations sealed not run']}


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
            raw = subprocess.check_output([sys.executable, str(Path(__file__).resolve()), '--reader', mode], cwd=str(ROOT), env=env)
            readers.append(json.loads(raw))
    assert len({(x['comparison_event_id'], x['comparison_post_snapshot_id'], x['comparison_future_bundle_id']) for x in readers}) == 1
    baseline = read(OUT / 'baseline.json')['files']
    changed = [p for p, old in baseline.items() if not (ROOT / p).is_file() or sha(ROOT / p) != old]
    assert not changed, changed
    current = set()
    for d in ('adapter/planner', 'docs/plans', 'docs/experiments/E1'):
        current.update(str(p.relative_to(ROOT)) for p in (ROOT / d).rglob('*')
            if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
    new_files = sorted(current - set(baseline))
    prefix = str(OUT.relative_to(ROOT)) + '/'
    allowed = {str(REPORT.relative_to(ROOT)), str(MARKDOWN.relative_to(ROOT))}
    assert all(p.startswith(prefix) or p in allowed for p in new_files), new_files
    assert not [p for p in OUT.glob('*.json') if re.fullmatch(r'(snapshot|event|bundle)-[0-9a-f]{64}\.json', p.name)]
    assert not (OUT / 'HEAD.json').exists()
    for p in OUT.glob('*.py'):
        ast.parse(p.read_text())
    diff = subprocess.run(['git', 'diff', '--check'], cwd=str(ROOT), stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, universal_newlines=True)
    assert diff.returncode == 0, diff.stdout + diff.stderr
    verification = {
        'schema': 'A04-DURABLE-ADMISSION-CONTRACT-VERIFICATION-1', 'RESULT': 'PASS',
        'scope': 'STATIC_CONTRACT_STRUCTURE_AND_NATIVE_CANONICAL_IDENTITY_INSPECTION',
        'independent_static_reader_count': len(readers), 'readers': readers,
        'native_durable_commit': 'NOT_RUN', 'native_cold_restore': 'NOT_RUN', 'native_replay': 'NOT_RUN',
        'future_runtime_negatives': 'SEALED_NOT_RUN', 'A04_executed': 'NO',
        'preexisting_files_checked': len(baseline), 'modified_preexisting_files': changed,
        'runtime_files_checked': sum(p.startswith('adapter/planner/') for p in baseline),
        'E1_files_checked': sum(p.startswith('docs/experiments/E1/') for p in baseline),
        'new_files': new_files, 'report_sha256': sha(REPORT), 'markdown_sha256': sha(MARKDOWN),
        'seal_script_sha256': sha(OUT / 'seal_contract.py'), 'verify_script_sha256': sha(Path(__file__).resolve()),
        'A04_DURABLE_TRANSACTION_IMPLEMENTATION_READY': 'YES', 'PROSPECTIVE_A04_EXECUTION_READY': 'NO',
        'P05_BOUND_STAGE_INPUTS': 10, 'RUNTIME_MODIFIED': 'NO', 'E1_ARTIFACTS_MODIFIED': 0,
        'PRODUCTION_EFFECT': 'NO', 'git_diff_check': 'PASS',
    }
    (OUT / 'verification.json').write_text(json.dumps(verification, sort_keys=True, indent=2) + '\n')
    print(json.dumps({key: verification[key] for key in ('RESULT', 'independent_static_reader_count',
        'preexisting_files_checked', 'modified_preexisting_files', 'runtime_files_checked', 'E1_files_checked', 'git_diff_check')}, sort_keys=True))


if __name__ == '__main__':
    main()
