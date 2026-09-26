"""Synthetic, non-effecting T1 argv representation regression tests."""
from copy import deepcopy
from dataclasses import asdict, replace
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from adapter.context_projection import canonical, digest, sha
from adapter.governed_host import Denied, GovernedHost, WorkAuthorization
from adapter.invocation_constructor import ConstructionDenied, construct_work_authorization


ARGV = ['/usr/bin/python3', '-B', '-m', 'unittest', 'discover', '-s',
        'tests/context', '-p', 'test_*.py', '-v']


def fixture():
    # Deliberately synthetic identities, never current E1 construction inputs.
    inputs = {key: 'test-only-' + key for key in (
        'InvocationAttemptId', 'DispatchAuthorizationId', 'specific_approval_id',
        'predecessor', 'eligibility', 'release_authority', 'OperationalContextId',
        'runtime', 'runtime_head', 'supervisor', 'succession_head', 'profile_sha256',
        'ModelPayloadDigest', 'transmission_retention', 'budget_policy',
        'implementation_identity', 'audit', 'lifecycle_envelope')}
    binding = {key: inputs[key] for key in ('InvocationAttemptId', 'DispatchAuthorizationId')}
    binding['bindings'] = {key: inputs[key] for key in ('release_authority', 'OperationalContextId')}
    inputs.update(canonical_binding=binding, binding_sha256=sha(canonical(binding).encode()),
                  initial_state='INACTIVE', ownership='NONE')
    fields = asdict(WorkAuthorization('test-only', 1, 'test-only-work', 'test-session',
                                     'test-turn', exec_bins=('python3',), state='INACTIVE'))
    fields['exec_argv_allowlist'] = [list(ARGV)]
    template = json.loads(canonical(dict(schema='WORK-AUTHORIZATION-TEMPLATE-1',
        state='INACTIVE', ownership='NONE', binding_digest=digest(inputs), fields_values=fields)))
    return inputs, template


class TemplateArgvTests(unittest.TestCase):
    def guard_decision(self, auth, argv):
        # Use the actual host guard without constructing a host or issuing a
        # permit. A deliberately supplied scope ID stops the matching case
        # after the comparison but before locks, snapshots, ownership or audit.
        token = object()
        root = str(Path(__file__).resolve().parent)
        stub = SimpleNamespace(auth=replace(auth, state='ACTIVE', read_roots=(root,)),
            _dispatcher_token=token, _interruption_requested=False,
            verify_lifecycle=Mock(), _write=Mock())
        with patch('adapter.governed_host.construct_snapshot') as snapshot:
            with self.assertRaises(Denied) as caught:
                GovernedHost.issue_exec_permit(stub, 'test-only-action', argv, root,
                    injected_scope_id='test-only-stop-before-effects', dispatcher_token=token)
            snapshot.assert_not_called()
            stub._write.assert_not_called()
        return str(caught.exception)

    def test_json_roundtrip_repairs_exact_mismatch_at_construction(self):
        inputs, template = fixture()
        before = deepcopy(template)
        raw_allowlist = template['fields_values']['exec_argv_allowlist']
        self.assertNotIn(tuple(ARGV), raw_allowlist)  # The original regression.
        artifact, auth = construct_work_authorization(inputs, template)
        self.assertIs(type(auth.exec_argv_allowlist), tuple)
        self.assertIs(type(auth.exec_argv_allowlist[0]), tuple)
        self.assertEqual(auth.exec_argv_allowlist, (tuple(ARGV),))
        self.assertEqual(auth.state, 'INACTIVE')
        self.assertEqual(template, before)
        self.assertEqual(construct_work_authorization(inputs, json.loads(canonical(template))),
                         (artifact, auth))
        self.assertEqual(canonical(auth.exec_argv_allowlist), canonical(raw_allowlist))
        self.assertEqual(self.guard_decision(auth, ARGV), 'execution scope identity supplied by caller')
        unhydrated = replace(auth, exec_argv_allowlist=raw_allowlist)
        self.assertEqual(self.guard_decision(unhydrated, ARGV), 'execution command outside exact allowlist')

    def test_non_equivalent_allowlists_fail_closed(self):
        alternatives = [
            ARGV + ['--extra'], ARGV[:-1],
            [ARGV[0], ARGV[2], ARGV[1], *ARGV[3:]],
            ['python3', *ARGV[1:]], ['/different/python3', *ARGV[1:]],
            [*ARGV[:-2], 'test_one.py', ARGV[-1]],
            [*ARGV[:-1], '-v '], [ARGV[0], ' '.join(ARGV[1:])],
            [*ARGV[:-1], '-V'], [*ARGV, ARGV[-1]],
        ]
        for other in alternatives:
            with self.subTest(allowlist=other):
                inputs, template = fixture()
                template['fields_values']['exec_argv_allowlist'] = [other]
                _, auth = construct_work_authorization(inputs, template)
                self.assertEqual(self.guard_decision(auth, ARGV),
                                 'execution command outside exact allowlist')
                # Equality is symmetric: the original policy rejects the altered argv too.
                _, original = construct_work_authorization(*fixture())
                self.assertEqual(self.guard_decision(original, other),
                                 'execution command outside exact allowlist')

    def test_malformed_values_are_rejected_without_coercion(self):
        malformed = [None, '', {}, tuple(), (tuple(ARGV),), [tuple(ARGV)],
                     [' '.join(ARGV)], [[]], [[1]], [[True]], [[None]],
                     [['']], [['python3', 'bad\x00arg']], [[['python3']]]]
        for value in malformed:
            with self.subTest(value=value):
                inputs, template = fixture()
                template['fields_values']['exec_argv_allowlist'] = value
                with self.assertRaisesRegex(ConstructionDenied, 'exec_argv_allowlist'):
                    construct_work_authorization(inputs, template)

    def test_preserves_order_duplicates_strings_and_detaches_input(self):
        inputs, template = fixture()
        commands = [list(ARGV), ['/usr/bin/python3', 'literal * space', 'é'], list(ARGV)]
        template['fields_values']['exec_argv_allowlist'] = commands
        _, auth = construct_work_authorization(inputs, template)
        self.assertEqual(auth.exec_argv_allowlist, tuple(tuple(row) for row in commands))
        commands[0][0] = 'changed'
        commands.append(['extra'])
        self.assertEqual(auth.exec_argv_allowlist[0], tuple(ARGV))
        self.assertEqual(len(auth.exec_argv_allowlist), 3)

    def test_explicit_empty_array_preserves_existing_representation(self):
        # Empty means no exact-argv restriction in the existing host. Do not
        # silently replace a missing/malformed/nonempty value with this sentinel.
        inputs, template = fixture()
        template['fields_values']['exec_argv_allowlist'] = []
        _, auth = construct_work_authorization(inputs, template)
        self.assertEqual(auth.exec_argv_allowlist, ())
        del template['fields_values']['exec_argv_allowlist']
        with self.assertRaisesRegex(ConstructionDenied, 'incomplete WorkAuthorization template'):
            construct_work_authorization(inputs, template)


if __name__ == '__main__':
    unittest.main()
