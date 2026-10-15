"""Post-writer cold readers, historical replay, sealed isolated negatives."""
import hashlib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import replace
from pathlib import Path

from adapter.planner import codec as c, core, gates, model as m
from adapter.planner import installation as i, proof_installation as pi, typed_proofs as tp
from adapter.tests import qualify_finish_f03 as q, qualify_finish_f03_checks as checks
from adapter.tests.test_planner_typed_proofs import candidate

R = Path(__file__).resolve().parents[4]
D = R / 'docs/plans'
O = Path(__file__).resolve().parent
F = D / 'qualification/FINISH_F03_1'
P = 'DETERMINISTIC_PLANNER_V0_1_'


def read(path):
    return c.parse_json(Path(path).read_bytes())


def emit(name, value):
    (O / name).write_bytes(c.canonical_bytes(value))


def load(name):
    man = read(O / 'checkpoint-manifests.json')[name]
    return c.restore(Path(man['path']), c._unwire(man['bundle_id']), R)


def require_writer_pass():
    result = read(O / 'writer-result.json')
    assert result['RESULT'] == 'PASS' and result['P04_EXIT_PREDICATE'] is True
    assert not (O / 'first-counterexample.json').exists()
    return result


def prepare():
    require_writer_pass()
    manifests = read(O / 'checkpoint-manifests.json')
    entry = load('final-preexecution')
    prefix = c._prefix_bundle(entry, 8)
    source_man = read(F / 'reader-manifests/installed-source-configuration.json')
    assert c._wire(c.snapshot_id(prefix.current)) == source_man['state_id']
    path = O / 'checkpoints/installed-source-configuration/prefix.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    man = q.save(prefix, path)
    man.update(semantic_oracle=source_man['semantic_oracle'], writer_terminated=True,
               oracle_source=str((F / 'reader-manifests/installed-source-configuration.json').relative_to(R)))
    manifests['installed-source-configuration'] = man
    reader_dir = O / 'reader-manifests'
    reader_dir.mkdir(exist_ok=True)
    for name, value in manifests.items():
        assert value['writer_terminated'] is True
        (reader_dir / (name + '.json')).write_bytes(c.canonical_bytes(value))
    emit('reader-plan.json', {'hash_seeds': [0, 1, 7, 101], 'readers_per_checkpoint_seed': 3,
         'boundaries': sorted(manifests), 'total_comparisons': len(manifests) * 12,
         'writer_terminated_before_readers': True})
    print('READER_PLAN_READY', len(manifests) * 12, flush=True)


def readers():
    require_writer_pass()
    paths = sorted((O / 'reader-manifests').glob('*.json'))
    assert len(paths) == 11
    results = []
    logs = O / 'reader-logs'
    logs.mkdir(exist_ok=True)

    def run(path, seed, number):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED=str(seed), PYTHONPATH='.')
        p = subprocess.run([sys.executable, 'adapter/tests/qualify_finish_f03.py', 'reader', str(path)],
                           cwd=R, env=env, text=True, capture_output=True)
        (logs / (path.stem + '-' + str(seed) + '-' + str(number) + '.log')).write_text(p.stdout + p.stderr)
        assert p.returncode == 0, (path, seed, number, p.stderr)
        result = json.loads(p.stdout)
        manifest = read(path)
        assert (result['pid'], result['pid_namespace']) != (manifest['writer_pid'], manifest['writer_pid_namespace'])
        return {'boundary': path.stem, 'seed': seed, 'reader': number, 'exit_code': p.returncode,
                'status': 'PASS', 'result': result, 'writer_pid': manifest['writer_pid'],
                'writer_namespace': manifest['writer_pid_namespace'], 'writer_terminated': True}

    with ThreadPoolExecutor(max_workers=6) as pool:
        pending = [pool.submit(run, path, seed, number) for path in paths
                   for seed in (0, 1, 7, 101) for number in range(3)]
        for completed in as_completed(pending):
            results.append(completed.result())
            emit('cold-reader-results.json', sorted(results, key=lambda r: (r['boundary'], r['seed'], r['reader'])))
            if len(results) % 12 == 0 or len(results) == len(pending):
                print('COLD_READERS_PASS', len(results), '/', len(pending), flush=True)


def replay():
    require_writer_pass()
    entry = load('final-preexecution')
    target = load('isolated-p04-target')
    count = len(entry.events)
    assert c._bundle_bytes_admitted(c._prefix_bundle(target, count)) == c._bundle_bytes_admitted(entry)
    current = entry
    rows = []
    expected_types = ['EvidenceSourceAdmission', 'ExternalEvent', 'ValidationSupportAdmission',
                      'ExternalEvent', 'DecisionReentry', 'SuppliedResult', 'InstallDefinition',
                      'TypedProofAdmission', 'InstallDefinition', 'TypedProofAdmission', 'SuppliedResult']
    for index, event in enumerate(target.events[count:]):
        assert type(event.result).__name__ == expected_types[index]
        assert event.parent_event == current.events[-1].identity and event.parent_snapshot == c.snapshot_id(current.current)
        state = core.apply_event(current.current, event.result).snapshot
        additions = event.result.source_additions if type(event.result) in (m.InstallDefinition, m.EvidenceSourceAdmission) else ()
        current = replace(current, events=current.events + (event,), current=state, sources=current.sources + additions)
        # Native replay validates recorded authority/assessment/proof history;
        # it issues nothing and does not rerun validation as a live decision.
        if type(event.result) is m.EvidenceSourceAdmission:
            paired = target.events[event.sequence]
            assert type(paired.result) is m.ExternalEvent and paired.result.stage is m.ExternalStage.EVIDENCE_RECEIVED
            assert paired.parent_event == event.identity and paired.result.artifact == event.result.entity.id
            # The ingress prefix is private inside one atomic A09 transaction.
            # Native canonical replay must validate it with its next receipt.
            replay_check = 'VALIDATED_WITH_PAIRED_RECEIPT_AT_A09_ATOMIC_BOUNDARY'
        else:
            c._replay(current)
            replay_check = 'PASS'
        assert c.snapshot_id(current.current) == event.after_snapshot
        rows.append({'sequence': event.sequence, 'type': type(event.result).__name__,
                     'event': c._wire(event.identity), 'parent': c._wire(event.parent_event),
                     'state': c._wire(c.snapshot_id(current.current)), 'status': 'PASS', 'native_replay_check': replay_check})
    assert c._bundle_bytes_admitted(current) == c._bundle_bytes_admitted(target)
    assert q.semantic_view(current) == q.semantic_view(target)
    assert [x['sequence'] for x in rows if x['type'] == 'InstallDefinition'] == [16, 18]
    result = {'RESULT': 'PASS', 'seed': os.environ.get('PYTHONHASHSEED'), 'pid': os.getpid(),
        'pid_namespace': os.readlink('/proc/self/ns/pid'), 'entry': c._wire(c.bundle_id(entry)),
        'target': c._wire(c.bundle_id(current)), 'rows': rows,
        'configuration_event_count': 2, 'new_authority_or_live_execution_calls': 0,
        'method': 'Historical input/event replay from exact entry at native atomic boundaries; no new epistemic decisions or durable publication.',
        'initial_comparison_failure_retained': 'replay-initial-attempt.json'}
    emit('replay-seed-' + str(os.environ.get('PYTHONHASHSEED')) + '.json', result)
    print('REPLAY_REPRODUCTION_PASS', os.environ.get('PYTHONHASHSEED'), flush=True)


def permutations():
    require_writer_pass()
    rows = {}
    manifests = read(O / 'checkpoint-manifests.json')
    for name, man in manifests.items():
        b = load(name)
        expected = read(F / ('reader-manifests/' + name + '.json'))['semantic_oracle']
        row = {}
        for mode in ('reverse', 'rotate'):
            changed = checks.permute(b, mode)
            assert c._bundle_bytes_admitted(changed) == Path(man['path']).read_bytes()
            m.validate_model(changed.current)
            assert q.semantic_view(changed) == expected
            assert c.snapshot_id(c._replay(changed)) == c.snapshot_id(b.current)
            row[mode] = {'canonical_bytes': 'PASS', 'identity': 'PASS', 'model_admission': 'PASS',
                         'Computation_Proof_C03': 'PASS', 'replay': 'PASS'}
        def reversed_keys(x):
            if type(x) is dict:
                return {k: reversed_keys(x[k]) for k in reversed(list(x))}
            if type(x) is list:
                return [reversed_keys(v) for v in x]
            return x
        altered_wire = reversed_keys(c._wire(b))
        assert c.canonical_bytes(altered_wire) == c.canonical_bytes(c._wire(b))
        altered = c._unwire(altered_wire)
        assert q.semantic_view(altered) == expected
        row['object_key_order'] = 'PASS'
        rows[name] = row
        emit('unordered-permutations.json', rows)
        print('PERMUTATIONS_PASS', name, flush=True)


def negatives():
    require_writer_pass()
    # Reuse the sealed F02 suite unchanged. Change only evidence destinations
    # and read-only checkpoint lookup; no live canonical transaction is called.
    q.O = O
    checks.O = O
    checks.load = load
    checks.load_manifest = lambda man: c.restore(Path(man['path']), c._unwire(man['bundle_id']), R)
    emit('configuration-manifest.json', read(O / 'checkpoint-manifests.json')['final-preexecution'])
    checks.negatives()
    canonical_head_before = (O / 'canonical-store/HEAD.json').read_bytes()
    slot_contract = load('slot-contract')
    root_contract = load('root-contract')
    post = load('post-a12')
    root = load('post-root-proof')
    target = load('isolated-p04-target')
    entry = load('final-preexecution')
    sc = next(p for p in slot_contract.current.proof_contracts if p.proof_type is m.TypedProofKind.SLOT_PROOF)
    rc = next(p for p in root_contract.current.proof_contracts if p.proof_type is m.TypedProofKind.ROOT_PROOF)
    fin = next(a for a in root.current.actions if a.id.value == 'E2-FINISH')
    supplied = m.SuppliedResult(fin.id, fin.accepted_result, fin.accepted_inventory, c.snapshot_id(root.current))
    rows = []
    def reject(label, fn):
        try:
            fn()
        except (m.PlannerError, ValueError) as error:
            rows.append({'case': label, 'status': 'PASS', 'reason': str(error)})
        else:
            raise AssertionError(label)
    for change in [{'proof_type': m.TypedProofKind.ROOT_PROOF}, {'proposition': 'wrong'},
                   {'target': m.SlotId('wrong')}, {'authority': m.EntityId('old-PC02')},
                   {'scope': 'foreign'}, {'lineage': 'foreign'}, {'generation': 'foreign'},
                   {'support_identities': (c._identity(b'bad', 'wrong'),)}, {'validation': m.ValidationState.STALE}]:
        bad = replace(candidate(sc), **change); bad = replace(bad, id=tp.identity(bad))
        reject('wrong slot proof ' + str(change), lambda bad=bad: c.record_result(slot_contract, m.TypedProofAdmission(bad, c.snapshot_id(slot_contract.current))))
    reject('slot proof without actual knowledge', lambda: core.apply_event(entry.current, m.TypedProofAdmission(candidate(sc), c.snapshot_id(entry.current))))
    reject('root proof without installed contract/satisfied slot', lambda: c.record_result(slot_contract, m.TypedProofAdmission(candidate(rc), c.snapshot_id(slot_contract.current))))
    reject('SLOT_PROOF substituted as ROOT_PROOF', lambda: c.record_result(root_contract, m.TypedProofAdmission(replace(candidate(sc), contract=rc.id), c.snapshot_id(root_contract.current))))
    for ref in (m.EntityId('P04-A13-INDEPENDENT-ROOT-SOURCE-1'), rc.authority):
        invalid = c.record_result(root_contract, m.ProofDependencyChange((ref,), c.snapshot_id(root_contract.current), rc.provenance))
        reject('root proof invalid source/semantic authority ' + ref.value, lambda invalid=invalid: c.record_result(invalid, m.TypedProofAdmission(candidate(rc), c.snapshot_id(invalid.current))))
    for field, value in [('proposition', 'wrong'), ('target', m.ConditionId('wrong')), ('authority', m.EntityId('old-PC02'))]:
        bad = replace(candidate(rc), **{field: value}); bad = replace(bad, id=tp.identity(bad))
        reject('wrong root ' + field, lambda bad=bad: c.record_result(root_contract, m.TypedProofAdmission(bad, c.snapshot_id(root_contract.current))))
    reject('FINISH early', lambda: c.record_result(post, replace(supplied, expected_snapshot=c.snapshot_id(post.current))))
    for label, change in [('wrong outcome', {'result': m.ActionResult.FAIL}), ('missing output', {'knowledge': ()}),
                          ('extra output', {'knowledge': supplied.knowledge + (replace(supplied.knowledge[0], id=m.KnowledgeId('extra')),)}),
                          ('wrong Action', {'action': m.ActionId('E2-REENTER')})]:
        reject('FINISH ' + label, lambda change=change: c.record_result(root, replace(supplied, **change)))
    invalidations = []
    for ref in (m.KnowledgeId('E2-K-REENTER'), m.EntityId('P04-A13-INDEPENDENT-ROOT-SOURCE-1'), rc.authority):
        invalid = c.record_result(root, m.ProofDependencyChange((ref,), c.snapshot_id(root.current), rc.provenance))
        assert invalid.current.roots[0].state is m.ConditionState.UNRESOLVED and fin.id not in core.recompute(invalid.current).actionable
        after = c.record_result(target, m.ProofDependencyChange((ref,), c.snapshot_id(target.current), rc.provenance))
        assert len(after.current.typed_proofs) == 2 and any(e.result == supplied for e in after.events)
        assert not core.recompute(after.current).actionable
        invalidations.append({'dependency': c._wire(ref), 'pre_FINISH_readiness_withdrawn': True,
                              'post_FINISH_history_retained_no_reexecution': True})
    for state in (replace(root.current, statuses=tuple(replace(s, terminal_failure=True, state=m.ActionState.BLOCKED) if s.id == fin.id else s for s in root.current.statuses)),
                  replace(root.current, actions=tuple(replace(a, blocked_terminal=True) if a.id == fin.id else a for a in root.current.actions), statuses=tuple(replace(s, state=m.ActionState.BLOCKED) if s.id == fin.id else s for s in root.current.statuses))):
        assert fin.id not in core.recompute(tp.reevaluate(state, state, (rc.target,), rc.provenance)).actionable
        rows.append({'case': 'terminal FINISH not force reopened', 'status': 'PASS'})
    assert len(rows) == 24
    emit('additional-negative-results.json', rows)
    emit('invalidation-results.json', invalidations)
    assert canonical_head_before == (O / 'canonical-store/HEAD.json').read_bytes()
    print('SEALED_NEGATIVES_PASS', 30 + len(rows), flush=True)


if __name__ == '__main__':
    {'prepare': prepare, 'readers': readers, 'replay': replay,
     'permutations': permutations, 'negatives': negatives}[sys.argv[1]]()
