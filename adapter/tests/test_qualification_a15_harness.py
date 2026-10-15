"""Grant-bounded fake-protocol qualification. No native Planner imports/calls.

Process tests are denied unless independent metadata confinement preflight passes.
Expected records are constructed directly here, never from worker execution.
"""
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
from adapter.qualification_a15 import contracts as c
from adapter.qualification_a15 import supervisor as s

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / 'docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1'


def independent_expected(request, initial):
    # Direct declared fake-rule oracle. Does not import/call worker derivation.
    p = request['payload']
    after = {'scope': c.SCOPE, 'support_current': False, 'protected': initial['protected']}
    return c.record('PUBLISHED_OUTPUT', {
        'request_identity': request['identity'], 'initial_snapshot_identity': p['initial_snapshot_identity'],
        'source_identity': p['source_identity'],
        'event_identity': c.identity({'initial': p['initial_snapshot_identity'],
            'source': p['source_identity'], 'variant': p['variant_id']}, 'qualification-a15-fake-event-v1'),
        'after_snapshot_identity': c.identity(after, 'qualification-a15-fake-snapshot-v1'),
        'typed_state': after, 'proof_validation': 'FAKE_STALE', 'proof_usability': False,
        'target_satisfaction': False, 'admission_stale': 'FAKE_CURRENT_VALIDATION_WITHDRAWN',
        'control': 'FAKE_BLOCKED', 'resume': {'allowed': False, 'actions': [],
            'reasons': ['FAKE_SUPPORT_WITHDRAWN'], 'supporting_identities': []},
        'ordered_trace': ['FAKE_RESTORE', 'FAKE_RECORD_RESULT', 'FAKE_SAVE'],
        'protected_state': initial['protected']})


def prepare_inputs(scratch):
    scratch = Path(scratch)
    (scratch / 'fixtures').mkdir()
    (scratch / 'outputs').mkdir()
    (scratch / 'outputs' / 'probe').mkdir()
    p71 = ROOT / 'docs/plans/qualification/E2_P05_D01_A15_IMPLEMENTATION_TEST_GRANT_ISSUANCE_71'
    grants = list(p71.glob('issued-implementation-test-grant-*.json'))
    c.require(len(grants) == 1, 'EXACT_GRANT_REQUIRED')
    proof = {'grant': json.loads(grants[0].read_text()),
        'effective_reference': json.loads((p71 / 'effective-implementation-test-grant-reference.json').read_text()),
        'owner_decision': json.loads((p71 / 'project-owner-decision.json').read_text()),
        'approved_subject': json.loads((ROOT / 'docs/plans/qualification/E2_P05_D01_A15_IMPLEMENTATION_TEST_AUTHORITY_70/implementation-test-authority-subject.json').read_text())}
    c.authorize_proof(proof)
    (scratch / 'proof.json').write_bytes(c.canonical(proof))
    code = {name: c.raw_hash((ROOT / name).read_bytes()) for name in s.SOURCE_FILES}
    initial = {'scope': c.SCOPE, 'support_current': True, 'protected': {'fixture_history': 'FAKE_IMMUTABLE'}}
    bindings, requests = [], []
    for variant in ('SYNTHETIC-ONE', 'SYNTHETIC-TWO'):
        case = 'T70-CAPTURE'
        row = scratch / 'fixtures' / case / variant
        row.mkdir(parents=True)
        out = scratch / 'outputs' / case / variant
        out.mkdir(parents=True)
        raw = 'SYNTHETIC-A15-TEST:INDEPENDENT-FAKE-SOURCE:' + variant
        source = {'kind': 'CONTENT_IDENTITY', 'namespace': 'raw-file-sha256', 'sha256': c.raw_hash(raw.encode())}
        initial_id = c.identity(initial, 'qualification-a15-fake-snapshot-v1')
        request = c.record('WORKER_REQUEST', {'case_id': case, 'variant_id': variant,
            'initial_snapshot_identity': initial_id, 'source_identity': source, 'operation': 'FAKE_RECORD_SAVE'})
        fixture = {'schema': 'A15-FAKE-FIXTURE-1', 'scope': c.SCOPE, 'variant_id': variant,
            'source_content': raw, 'source_identity': source,
            'initial_state': initial, 'initial_snapshot_identity': initial_id}
        (row / 'request.json').write_bytes(c.canonical(request))
        (row / 'fixture.json').write_bytes(c.canonical(fixture))
        (row / 'expected.json').write_bytes(c.canonical(independent_expected(request, initial)))
        binding = {'schema': 'A15-EXECUTION-BINDING-1', 'role': 'WORKER',
            'request_identity': request['identity'], 'request_path': str(row / 'request.json'),
            'fixture_path': str(row / 'fixture.json'), 'expected_path': str(row / 'expected.json'),
            'output_directory': str(out), 'proof_path': str(scratch / 'proof.json'),
            'code_hashes': code, 'fault': 'NONE', 'exit_evidence': None}
        Path(str(row / 'request.json') + '.binding').write_bytes(c.canonical(binding))
        bindings.append(binding);requests.append(request)
    sup = c.record('SUPERVISOR_REQUEST', {'case_id': 'T70-CAPTURE',
        'variant_requests': [r['identity'] for r in requests]})
    return proof, code, requests, bindings, sup


class FakeProtocolQualification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.scratch = Path('/tmp') / ('kge-a15-harness-test-' + uuid.uuid4().hex)
        cls.scratch.mkdir(mode=0o700)
        cls.observations = []
        cls.proof, cls.code, cls.requests, cls.bindings, cls.request = prepare_inputs(cls.scratch)
        cls.campaign = s.Campaign(cls.scratch, cls.observations.append)
        # A failing control blocks every test, without retry or fallback.
        try:
            cls.preflight = s.verify_environment(cls.campaign, ROOT,
                cls.scratch / 'outputs' / 'probe', cls.code)
        except Exception as exc:
            record = {'result': 'BLOCKED_BEFORE_FAKE_TESTS', 'failure': str(exc),
                'observations': cls.observations, 'scratch': str(cls.scratch), 'native_calls': 0}
            (EVIDENCE / ('preflight-blocked-' + os.environ.get('PYTHONHASHSEED', 'unset') + '.json')).write_text(json.dumps(record, sort_keys=True, indent=2))
            raise

    @classmethod
    def tearDownClass(cls):
        # Only this campaign-owned scratch tree, never retained inputs/evidence.
        if hasattr(cls, 'scratch'):
            c.private_path(cls.scratch, cls.scratch)
            shutil.rmtree(cls.scratch)

    def test_01_complete_process_protocol(self):
        result = s.run_supervisor(self.request, self.bindings, self.campaign,
            ROOT, lambda request: c.authorize_proof(self.proof))
        c.validate(result, 'SUPERVISOR_RESULT')
        self.assertEqual(len(result['payload']['variant_results']), 2)
        for binding, row in zip(self.bindings, result['payload']['variant_results']):
            expected = c.read_exact(binding['expected_path'])
            self.assertEqual(row['worker']['payload']['published_output_identity'], expected['identity'])
            self.assertEqual(len(row['readers']), 4)
            for reader in row['readers']:
                self.assertTrue(reader['payload']['matched'])
        exits = [o for o in self.observations if o['kind'] == 'child_exit']
        self.assertEqual(len({o['host_child_pid'] for o in exits}), len(exits))
        self.assertTrue(all(o['exit_status'] == 0 for o in exits))
        evidence = {'result': 'PASS', 'semantic_result': result,
            'semantic_identity': c.identity(result, 'qualification-a15-fake-qualification-result-v1'),
            'observations': self.observations, 'categories': ['T70-' + n for n in (
                'PROCESS','INPUT','DISPATCH','CAPTURE','SERIALIZE','PUBLISH','EXIT',
                'HANDOFF','READER','COMPARE','ISOLATION','FAILURE','DETERMINISM')],
            'native_calls': 0, 'limits': c.LIMITS, 'source_hashes': self.code}
        (EVIDENCE / ('fake-results-seed-' + os.environ.get('PYTHONHASHSEED', 'unset') + '.json')).write_text(json.dumps(evidence, sort_keys=True, indent=2))

    def test_02_exact_schemas_and_authority(self):
        for field in ('schema', 'version', 'role', 'phase', 'grant_identity', 'identity'):
            request = copy.deepcopy(self.requests[0])
            request[field] = 'wrong'
            with self.assertRaises(c.ProtocolError):
                c.validate(request, 'WORKER_REQUEST')
        request = copy.deepcopy(self.requests[0]);request['extra'] = True
        with self.assertRaises(c.ProtocolError):c.validate(request, 'WORKER_REQUEST')
        bad = copy.deepcopy(self.proof);bad['grant']['RECORD']['PERMITTED_SOURCE_FILES'].append('adapter/planner/core.py')
        with self.assertRaises(c.ProtocolError):c.authorize_proof(bad)

    def test_03_source_and_dispatch(self):
        fixture = c.read_exact(self.bindings[0]['fixture_path'])
        fixture['source_content'] += 'tampered'
        with self.assertRaises(c.ProtocolError):c.validate_synthetic_input(fixture, self.requests[0])
        p = dict(self.requests[0]['payload'], operation='apply_event')
        with self.assertRaises(c.ProtocolError):c.validate(c.record('WORKER_REQUEST', p), 'WORKER_REQUEST')

    def test_04_serialization_and_completeness(self):
        expected = c.read_exact(self.bindings[0]['expected_path'])
        self.assertEqual(c.canonical(expected), c.canonical(c.parse(c.canonical(expected))))
        with self.assertRaises(c.ProtocolError):c.parse('{"a":1,"a":2}')
        with self.assertRaises(c.ProtocolError):c.parse('{"a":1.5}')
        p = copy.deepcopy(expected['payload']);p['resume']['reasons'] = ['wrong']
        with self.assertRaises(c.ProtocolError):c.compare_complete_output(c.record('PUBLISHED_OUTPUT', p), expected)

    def test_05_failure_and_isolation(self):
        with self.assertRaises(c.ProtocolError):
            c.publish(self.bindings[0]['output_directory'], 'published-output.json', {})
        bad = copy.deepcopy(self.bindings[0]);bad['output_directory'] = self.bindings[1]['output_directory']
        with self.assertRaises(c.ProtocolError):c.validate_binding(bad, 'WORKER', self.requests[0], self.scratch)
        with self.assertRaises(c.ProtocolError):s.observe_child_exit({'kind':'child_exit', 'exit_status':1, 'timeout':False, 'started_ns':1,'exit_observed_ns':2})
        p = copy.deepcopy(self.bindings[0]);p['exit_evidence'] = {'writer_exit_observed':True}
        with self.assertRaises(c.ProtocolError):c.validate_binding(p, 'WORKER', self.requests[0], self.scratch)
        with self.assertRaises(c.ProtocolError):s._environment(999)

if __name__ == '__main__':
    unittest.main()
