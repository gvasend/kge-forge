"""Non-live private authority qualification; no E1 identity or supervisor launch."""
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch
import json
import os
import subprocess
import sys
import tempfile
import unittest

from adapter.controller_authority_store import (ControllerAuthorityStore, AuthorityDenied,
    roots_for, read_authority_ref, encoded, sha)
from adapter.authority_bootstrap import capture_inputs, selection, reconstruct_authorization
from adapter.tests.qualify_activation_transaction import fixture
from adapter.activation_transaction import ActivationTransaction
from adapter.authorization_lifecycle import dispatch_binding
from adapter.context_projection import canonical, derive
from adapter.governed_host import GovernedHost, WorkAuthorization, Denied
from adapter.execution_snapshot import construct, SnapshotDenied
from adapter.model_transmission import TransmissionBoundary


def private_fixture(auth, audit, ref, root):
    records = capture_inputs(auth, audit, ref)
    aliases, applicability, provenance, private = selection(auth, audit, ref)
    return ControllerAuthorityStore.materialize(root, records, aliases, provenance,
        applicability, roots_for(auth), private)


class ControllerAuthorityStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='authority-store-unit-')
        self.out = Path(self.temp.name)
        self.root, self.auth, self.audit, self.ref, self.projection = fixture(
            self.out/'fixture', supervisor_identity={'synthetic_host': 'NON_LIVE'})
        self.store = private_fixture(self.auth, self.audit, self.ref, self.out/'private')
        self.dispatch_id = 'E1-ARCHITECT-DISPATCH-sha256:'+self.ref['sha256']

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def test_logical_profile_dispatch_provisioning_and_restart(self):
        op = json.loads(self.auth.operational_binding)
        with self.store.session():
            restored = reconstruct_authorization(self.store, self.auth.authorization_id)
            self.assertEqual(dispatch_binding(restored, self.audit, self.ref),
                             dispatch_binding(self.auth, self.audit, self.ref))
            self.assertEqual(derive(json.loads(restored.context_projection), restored.context_binding)
                             ['ModelPayloadDigest'], self.projection['ModelPayloadDigest'])
            profile = json.loads(read_authority_ref(op['governance']['released_profile']))
            receipt = json.loads(self.store.resolve('sha256:'+profile['provisioning_receipt_sha256']))
            self.assertEqual(receipt['result'], 'PASS')
        with ControllerSession(self.store) as restarted:
            self.assertEqual(reconstruct_authorization(restarted, self.auth.authorization_id).authorization_id,
                             self.auth.authorization_id)

    def test_repository_substitution_does_not_select_authority(self):
        op = json.loads(self.auth.operational_binding)
        selected = [self.ref, op['governance']['released_profile'], op['governance']['release_decision']]
        originals = [(Path(ref['path']), Path(ref['path']).read_bytes()) for ref in selected]
        for path, _ in originals:
            path.write_bytes(b'UNTRUSTED REPOSITORY EVIDENCE')
        try:
            with self.store.session():
                restored = reconstruct_authorization(self.store, self.auth.authorization_id)
                dispatch_binding(restored, self.audit, self.ref)
                for ref, (_, data) in zip(selected, originals):
                    self.assertEqual(read_authority_ref(ref), data)
        finally:
            for path, data in originals:
                path.write_bytes(data)

    def test_unknown_path_missing_hash_and_catalog_substitution(self):
        with self.assertRaises(AuthorityDenied): self.store.resolve(self.ref['path'])
        with self.assertRaises(AuthorityDenied): self.store.resolve('sha256:'+'0'*64)
        identity = 'sha256:'+self.ref['sha256']
        path = self.store.location(identity)
        data = path.read_bytes()
        path.write_bytes(b'SUBSTITUTION')
        with self.assertRaises(AuthorityDenied): self.store.resolve(identity)
        path.write_bytes(data)
        missing = path.with_suffix('.missing'); path.rename(missing)
        try:
            with self.store.session():
                with self.assertRaises(OSError): read_authority_ref(self.ref)
        finally: missing.rename(path)
        catalog = self.store.root/'catalog.json'; data = catalog.read_bytes()
        catalog.write_bytes(data+b' ')
        with self.assertRaises(AuthorityDenied): self.store.resolve(identity)
        catalog.write_bytes(data)

    def test_incomplete_provenance_stale_and_store_in_grant(self):
        bad = dict(self.store.applicability, authorization_id='other')
        with self.assertRaises(AuthorityDenied): ControllerAuthorityStore(self.store.root, self.store.catalog_sha256, bad)
        with self.assertRaises(AuthorityDenied):
            self.store.require(replace(self.auth, read_roots=(*self.auth.read_roots, str(self.store.root))))
        c = json.loads(encoded(self.store.catalog)); first = next(iter(c['objects']))
        c['objects'][first]['authority_source'] = ''
        other = self.out/'invalid'; other.mkdir(mode=0o700)
        p = other/'catalog.json'; p.write_bytes(encoded(c)); p.chmod(0o600)
        with self.assertRaises(AuthorityDenied): ControllerAuthorityStore(other, sha(p.read_bytes()), self.store.applicability)

    def test_programmer_and_snapshot_and_transmission_denied(self):
        # Separate synthetic path-only identity; never activate E1 to probe grants.
        auth = WorkAuthorization('probe', 1, 'SYNTHETIC', 'probe-session', 'probe-turn',
            read_roots=self.auth.read_roots, write_roots=self.auth.write_roots,
            write_directory_roots=self.auth.write_directory_roots,
            model_transmission=self.auth.model_transmission)
        host = GovernedHost(auth, self.out/'probe-audit.jsonl')
        repo = str(self.store.root)
        calls = [lambda: host.governed_read(repo, 'catalog.json'),
                 lambda: host.governed_list(repo, '.'),
                 lambda: host.governed_search(repo, '.', 'schema'),
                 lambda: host.governed_write(repo, 'catalog.json', 'bad'),
                 lambda: host.governed_patch(repo, [{'op':'write','path':'catalog.json','content':'bad'}])]
        for call in calls:
            with self.assertRaises(Denied): call()
        with self.assertRaises(SnapshotDenied):
            construct(self.store.root, ['catalog.json'], lambda p: host._path(repo,p),
                      self.out, 'denied-snapshot')
        boundary = TransmissionBoundary(host)
        forged = {'name':'governed_read','arguments':canonical({'repository':repo,'path':'catalog.json'})}
        result = boundary.result(forged, {'result':'SUCCEEDED','data':{'path':str(self.store.root/'catalog.json'),
                                                                     'content':'PRIVATE'}})
        self.assertEqual(result['transmission'], 'REDACTED')

    def test_activation_ownership_handoff_recovery_synthetic(self):
        # Only host observations are simulated; all authority, transaction,
        # ownership, durable audit and recovery verifiers are production code.
        with self.store.session(), patch('adapter.activation_transaction._host', return_value={'synthetic':'NON_LIVE'}):
            restored = reconstruct_authorization(self.store, self.auth.authorization_id)
            tx = ActivationTransaction.activate(restored, self.audit, self.dispatch_id)
            try:
                self.assertTrue(tx.verify_handoff())
                self.assertIsNotNone(tx.reservation)
            finally: tx.close()
            tx = ActivationTransaction.recover(restored, self.audit, self.dispatch_id)
            try: self.assertTrue(tx.recovery['handoff_eligible'])
            finally: tx.close()
        command = [sys.executable, '-m', 'adapter.tests.test_controller_authority_store', '--recover',
                   str(self.store.root), self.store.catalog_sha256, canonical(self.store.applicability),
                   str(self.audit), canonical(self.dispatch_id)]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        self.assertTrue(json.loads(result.stdout)['handoff_eligible'])

    def test_production_cannot_fall_back_to_repository(self):
        before = self.audit.read_bytes()
        with self.assertRaises(AuthorityDenied): ActivationTransaction.activate(self.auth, self.audit, self.dispatch_id)
        self.assertEqual(self.audit.read_bytes(), before)
        with self.store.session():
            from adapter.authorization_lifecycle import LifecycleDenied
            with self.assertRaises(LifecycleDenied):
                ActivationTransaction.activate(self.auth,self.audit,self.ref)
            from adapter.activation_transaction import validate_production
            fd = os.open(self.auth.ownership_ledger,os.O_RDONLY)
            try:
                with self.assertRaises(LifecycleDenied):
                    validate_production(self.auth,self.audit,self.ref,fd)
            finally:os.close(fd)
        self.assertEqual(self.audit.read_bytes(),before)

    def test_governed_finish_terminal_audit_uses_private_authority(self):
        from adapter.orchestrator import ReasoningOrchestrator, action
        with self.store.session(), patch('adapter.activation_transaction._host', return_value={'synthetic':'NON_LIVE'}):
            tx = ActivationTransaction.activate(self.auth, self.audit, self.dispatch_id)
            try:
                host = GovernedHost(tx.auth, self.audit); tx.attach(host)
                orch = ReasoningOrchestrator(host)
                request = action(action_request_id='synthetic-finish', type='finish',
                    session_id=tx.auth.session_id, turn_id=tx.auth.turn_id,
                    authorization_id=tx.auth.authorization_id, authorization_revision=tx.auth.revision,
                    summary='synthetic private authority completion')
                result = orch.request(request)
                self.assertEqual(result['result'], 'SUCCEEDED')
                tx.complete(host, 'synthetic-finish')
            finally: tx.close()
            recovered = ActivationTransaction.recover(self.auth, self.audit, self.dispatch_id)
            try:
                self.assertEqual(recovered.recovery['lifecycle_state'], 'COMPLETED')
                self.assertIsNone(recovered.recovery['ownership'])
            finally: recovered.close()

    def test_payload_namespace_cannot_reach_store(self):
        workspace = self.out/'payload'; workspace.mkdir()
        code = ('from pathlib import Path; '
                'p=Path('+repr(str(self.store.root))+'); '
                'assert not p.exists(); '
                'assert not Path("/scope/catalog.json").exists(); '
                'print("PRIVATE_AUTHORITY_UNREACHABLE")')
        result = subprocess.run([sys.executable, '-m', 'adapter.exec_barrier', str(workspace),
                                 '/usr/bin/python3', '-c', code], input=b'1',
                                capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        self.assertEqual(result.stdout.strip(), b'PRIVATE_AUTHORITY_UNREACHABLE')

    def test_private_resolution_through_governed_exec_and_quiescence(self):
        from adapter.tests.test_production_exec import BridgeFactory, FakeSupervisorBridge
        from adapter.orchestrator import ReasoningOrchestrator, action
        from adapter.runnable_profile import ARGV, INPUTS
        class ProfileBridge(FakeSupervisorBridge):
            def exchange(self, op, **fields):
                result = super().exchange(op, **fields)
                if op == 'production_spawn':
                    result['result'] = canonical({'kind':'governed_launch_receipt',
                        'runtime_policy_sha256':fields['argv'][0].split('=',1)[1]})
                return result
        class ProfileFactory(BridgeFactory):
            def __call__(self,*args): return ProfileBridge(self,*args)
        bridge = ProfileFactory(); bridge.release.set()
        def supervisor_events(_path):
            return [{'event':event,'scope_id':scope,'owner':[session,authorization,rid]}
                    for session,authorization,scope,rid,_ in bridge.bindings
                    for event in ('scope_created','scope_closed')]
        with self.store.session(), \
             patch('adapter.activation_transaction._host', return_value={'synthetic':'NON_LIVE'}), \
             patch('adapter.governed_host.ForwardBridge', bridge), \
             patch('adapter.invocation_ownership._observe', return_value={'members':[],'populated':0,'directories':1}), \
             patch('adapter.invocation_ownership._events', side_effect=supervisor_events):
            tx = ActivationTransaction.activate(self.auth, self.audit, self.dispatch_id)
            try:
                host = GovernedHost(tx.auth, self.audit); tx.attach(host)
                orch = ReasoningOrchestrator(host)
                result = orch.request(action(action_request_id='synthetic-exec',type='exec',
                    session_id=tx.auth.session_id,turn_id=tx.auth.turn_id,
                    authorization_id=tx.auth.authorization_id,authorization_revision=tx.auth.revision,
                    executable=ARGV[0],argv=list(ARGV[1:]),cwd=str(self.root),inputs=list(INPUTS)))
                self.assertEqual(result['result'],'SUCCEEDED', result)
                self.assertEqual(host.scope.state,'QUIESCENT')
                self.assertIsNone(host.ownership.active())
                self.assertIn('execution_scope_quiescent', self.audit.read_text())
            finally:tx.close()


class ControllerSession:
    def __init__(self, store): self.previous = store
    def __enter__(self):
        self.store = ControllerAuthorityStore(self.previous.root, self.previous.catalog_sha256, self.previous.applicability)
        self.session = self.store.session(); self.session.__enter__()
        return self.store
    def __exit__(self, *args):
        self.session.__exit__(*args); self.store.close()


if __name__ == '__main__':
    if len(sys.argv)>1 and sys.argv[1]=='--recover':
        store = ControllerAuthorityStore(sys.argv[2], sys.argv[3], json.loads(sys.argv[4]))
        with store.session(), patch('adapter.activation_transaction._host', return_value={'synthetic':'NON_LIVE'}):
            auth = reconstruct_authorization(store, store.applicability['authorization_id'])
            tx = ActivationTransaction.recover(auth, Path(sys.argv[5]), json.loads(sys.argv[6]))
            print(canonical(tx.recovery)); tx.close()
        store.close()
    else:
        unittest.main()
