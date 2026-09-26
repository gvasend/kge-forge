"""PD-06 synthetic committed qualification, no E1 implementation or API calls."""
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from adapter.directory_provisioning import plan, provision
from adapter.model_transmission import production_policy, digest
from adapter.governed_host import GovernedHost
from adapter.orchestrator import ReasoningOrchestrator
from adapter.responses_orchestrator import ResponsesReasoning
from adapter.runnable_profile import authorization
from adapter.context_binding import CommittedContext
from adapter.tests.test_runnable_profile import fixture, git


def qualify(out):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    # Isolate this declared synthetic regression from legitimately appended E1
    # historical decisions. Production current-source checks remain unchanged.
    root, binding, acceptance = fixture(synthetic_acceptance=True)
    markers = {'public.txt': 'PUBLIC_SYNTHETIC_CONTENT',
               'uncleared.txt': 'UNCLEARED_SYNTHETIC_CONTENT',
               'evidence/record.txt': 'EVIDENCE_SYNTHETIC_CONTENT',
               'private/state.txt': 'PRIVATE_SYNTHETIC_CONTENT',
               'credentials.txt': 'SECRET_SYNTHETIC_CONTENT'}
    for rel, content in markers.items():
        p = root / rel; p.parent.mkdir(exist_ok=True); p.write_text(content)
    git(root, 'add', '.'); git(root, 'commit', '-qm', 'Synthetic PD06 disclosure fixture')
    binding = CommittedContext(binding.path, git(root, 'rev-parse', 'HEAD'))
    for hidden in ('.codex', '.agents'):
        (root / hidden).mkdir(); (root / hidden / 'marker').write_text('HIDDEN_SYNTHETIC_CONTENT')
    auth = authorization(binding, acceptance, 'pd06-fixture', 4, 's-pd06', 't-pd06', True)
    policy = production_policy(binding)
    policy['private_paths'] = [str(root / 'private')]
    policy['credential_paths'] = [str(root / 'credentials.txt')]
    policy['evidence_paths'] = [str(root / 'evidence')]
    policy['authority_source'] = 'Synthetic qualification clearance; not E1 clearance'
    task = 'Synthetic fixture only'
    context = binding.model_context()
    policy['initial_clearances'] = [{'sha256': digest({'task': task, 'context': context}),
        'category': 'cleared-reasoning-context', 'authority_source': policy['authority_source']}]
    def clearance(path, category='ordinary'):
        return {'path': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                'category': category, 'authority_source': policy['authority_source']}
    # Even a generic ordinary-file clearance cannot override sensitive classes.
    policy['file_clearances'] = [clearance(root / p) for p in
        ('public.txt', 'credentials.txt', 'private/state.txt', 'evidence/record.txt')]
    auth = replace(auth, model_transmission=json.dumps(policy))
    host = GovernedHost(auth, out / 'transmission-audit.jsonl')
    runner = ResponsesReasoning(ReasoningOrchestrator(host))
    probes = []
    counter = 0
    def probe(name, args):
        nonlocal counter
        counter += 1
        call = {'name': name, 'call_id': 'probe-' + str(counter), 'arguments': json.dumps(args)}
        local = runner._dispatch(call)
        external = runner.transmission.result(call, local)
        probes.append({'name': name, 'args': args, 'local': local, 'external': external})
        return local, external
    for rel in ['public.txt', 'uncleared.txt', 'package.txt', 'evidence/record.txt',
                'private/state.txt', 'credentials.txt']:
        local, external = probe('governed_read', {'repository': str(root), 'path': rel, 'limit': 65536})
        assert local['result'] == 'SUCCEEDED'
        assert ('content' in external) == (rel == 'public.txt')
    for rel in ['.', 'evidence', 'private']:
        for name in ('governed_list', 'governed_search'):
            args = {'repository': str(root), 'path': rel, 'limit': 100}
            if name == 'governed_search': args['query'] = 'SYNTHETIC'
            _, external = probe(name, args)
            assert external['transmission'] == 'REDACTED'
            assert not any(marker in json.dumps(external) for marker in markers.values())
    for hidden in ('.git', '.codex', '.agents'):
        for name in ('governed_read', 'governed_list', 'governed_search'):
            args = {'repository': str(root), 'path': hidden, 'limit': 100}
            if name == 'governed_search': args['query'] = 'SYNTHETIC'
            local, external = probe(name, args)
            assert local['result'] == 'DENIED' and external['transmission'] == 'REDACTED'
    # Prefix reads, changed content, path aliases, errors, write/patch hashes and echoes
    # never become implicit content clearance.
    _, external = probe('governed_read', {'repository': str(root), 'path': 'public.txt', 'limit': 3})
    assert external['transmission'] == 'REDACTED'
    for name in ('governed_write', 'governed_patch', 'governed_exec', 'governed_status',
                 'authority_expansion_request', 'finish_task'):
        external = runner.transmission.result({'name': name},
            {'result': 'SUCCEEDED', 'data': {'content': 'SECRET_SYNTHETIC_CONTENT',
                                           'sha256': 'SENSITIVE_HASH', 'summary': 'PRIVATE'}})
        assert set(external) == {'transmission', 'notice'}
        for status in ('DENIED', 'INDETERMINATE'):
            assert external == runner.transmission.result({'name': name}, {'result': status})
    (root / 'public-link.txt').symlink_to(root / 'public.txt')
    _, external = probe('governed_read', {'repository': str(root), 'path': 'public-link.txt', 'limit': 65536})
    assert external['transmission'] == 'REDACTED'
    (root / 'copied-private.txt').write_text(markers['private/state.txt'])
    local, external = probe('governed_read', {'repository': str(root), 'path': 'copied-private.txt', 'limit': 65536})
    assert local['result'] == 'SUCCEEDED' and external['transmission'] == 'REDACTED'
    (root / 'public.txt').write_text('CHANGED_UNCLEARED_CONTENT')
    local, external = probe('governed_read', {'repository': str(root), 'path': 'public.txt', 'limit': 65536})
    assert local['result'] == 'SUCCEEDED' and external['transmission'] == 'REDACTED'
    (root / 'public.txt').write_text(markers['public.txt'])
    _, external = probe('governed_read', {'repository': str(root), 'path': '../outside', 'limit': 65536})
    assert external['transmission'] == 'REDACTED'
    # Actual continuation, no overridden dispatcher and no network.
    class ModelFixture(ResponsesReasoning):
        def __init__(self, orch):
            super().__init__(orch); self.payloads = []
        def _call(self, payload):
            self.payloads.append(json.loads(json.dumps(payload)))
            n = len(self.payloads)
            if n in (1, 2):
                rel = 'public.txt' if n == 1 else 'package.txt'
                return {'output': [{'type': 'function_call', 'name': 'governed_read',
                    'call_id': 'loop-' + str(n), 'arguments': json.dumps({
                        'repository': str(root), 'path': rel, 'limit': 65536})}]}
            if n == 3:
                return {'output': [{'type': 'function_call', 'name': 'finish_task',
                    'call_id': 'loop-finish', 'arguments': '{"summary":"synthetic complete"}'}]}
            return {'output': []}
    loop = ModelFixture(runner.orchestrator)
    assert loop.run(task, context, 4)['status'] == 'COMPLETE'
    serialized = json.dumps(loop.payloads)
    assert 'PUBLIC_SYNTHETIC_CONTENT' in serialized
    assert (root / 'package.txt').read_text() not in serialized
    for rel, marker in markers.items():
        if rel != 'public.txt': assert marker not in serialized
    # Separate protected clearance works only with explicit protected classification.
    for category, expected in [('ordinary', 'REDACTED'), ('explicitly-cleared-governing', 'CLEARED')]:
        selected = dict(policy, file_clearances=[clearance(root / 'package.txt', category)])
        test_auth = replace(auth, authorization_id='clear-' + category,
                            model_transmission=json.dumps(selected))
        test_host = GovernedHost(test_auth, out / ('clear-' + category + '.jsonl'))
        test_runner = ResponsesReasoning(ReasoningOrchestrator(test_host))
        call = {'name': 'governed_read', 'call_id': 'cleared', 'arguments': json.dumps({
            'repository': str(root), 'path': 'package.txt', 'limit': 65536})}
        local = test_runner._dispatch(call)
        assert test_runner.transmission.result(call, local)['transmission'] == expected
    try: runner.transmission.initial('uncleared initial task', context)
    except ValueError: pass
    else: raise AssertionError('uncleared initial content accepted')
    events = [json.loads(line) for line in host.audit.read_text().splitlines()]
    assert {'ALLOW', 'REDACT', 'DENY'} <= {e.get('decision') for e in events if e.get('event') == 'model_transmission'}
    assert binding.verify()
    provisioning = []
    for variant in ('pass', 'symlink', 'wrong-type', 'unexpected-existing', 'unlisted', 'active'):
        base = Path(tempfile.mkdtemp(prefix='pd06-provision-')); repo = base / 'forge'; repo.mkdir()
        (repo / 'docs').mkdir(); (repo / 'docs/baseline.txt').write_text('Synthetic committed baseline')
        git(repo, 'init', '-q'); git(repo, 'add', '.'); git(repo, 'commit', '-qm', 'Synthetic provisioning baseline')
        commit = git(repo, 'rev-parse', 'HEAD')
        record = plan(repo, commit)
        if variant == 'symlink': (repo / 'src').symlink_to(repo / 'docs', target_is_directory=True)
        if variant == 'wrong-type': (repo / 'src').write_text('wrong type')
        if variant == 'unexpected-existing': (repo / 'src').mkdir()
        if variant == 'unlisted': record['directories'] = record['directories'][1:]
        from adapter.tests.test_pd05_file_authority import inventory
        before = inventory(repo)
        try:
            receipt = provision(record, out / ('provision-' + variant + '.jsonl'),
                                'ACTIVE' if variant == 'active' else 'INACTIVE')
        except (ValueError, OSError):
            assert variant != 'pass'
            assert before == inventory(repo)
            receipt = {'result': 'DENIED', 'no_effects': True}
        else:
            assert variant == 'pass'
            after = inventory(repo)
            changed = sorted(k for k in after if k not in before)
            assert changed == sorted(r['path'][len(str(repo)) + 1:] for r in record['directories']
                                     if r['controller_provisioning_required'])
            assert all(before[k] == after[k] for k in before)
        provisioning.append({'variant': variant, 'commit': commit, 'plan': record, 'receipt': receipt,
                             'before': before, 'after': inventory(repo)})
    report = {'result': 'PASS', 'fixture_commit': binding.capture_commit,
              'context_sha256': binding.digest, 'transmission_policy': policy, 'probes': probes,
              'model_payloads': loop.payloads, 'provisioning': provisioning,
              'real_model_calls': 0, 'E1_executed': False}
    (out / 'BOUNDARY_REPORT.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


class ReleaseBoundaryTests(unittest.TestCase):
    def test_committed_boundaries(self):
        with tempfile.TemporaryDirectory(prefix='pd06-qualification-') as out:
            self.assertEqual(qualify(out)['result'], 'PASS')


if __name__ == '__main__': unittest.main()
