import json, pathlib, tempfile, unittest
from adapter.invocation_ownership import InvocationOwnership, OwnershipDenied

class InvocationOwnershipTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.root=pathlib.Path(self.temp.name)
        self.base=self.root/'executor'; self.base.mkdir()
        self.audit=self.root/'supervisor.jsonl'
        self.ledger=InvocationOwnership(self.root/'ownership.jsonl',self.base,self.audit)
        self.sid='scope-'+'a'*32
        self.scope=self.base/self.sid; self.scope.mkdir()
        (self.scope/'cgroup.procs').write_text('123')
        (self.scope/'cgroup.events').write_text('populated 1\n')
        self.audit.write_text(''.join(json.dumps(event)+'\n' for event in (
            {'event':'scope_created','scope_id':self.sid,'owner':['session','auth','action']},
            {'event':'scope_closed','scope_id':self.sid,'owner':['session','auth','action']})))
    def tearDown(self): self.temp.cleanup()
    def test_unresolved_reservation_survives_new_controller_and_requires_kernel_zero(self):
        self.ledger.reserve(self.sid,'action','session','auth',self.root/'controller.jsonl')
        restarted=InvocationOwnership(self.root/'ownership.jsonl',self.base,self.audit)
        with self.assertRaises(OwnershipDenied):
            restarted.reserve('scope-'+'b'*32,'other','session','auth',self.root/'other.jsonl')
        with self.assertRaises(OwnershipDenied):
            restarted.release(self.sid,'action','session','auth')
        (self.scope/'cgroup.procs').write_text('')
        (self.scope/'cgroup.events').write_text('populated 0\n')
        restarted.release(self.sid,'action','session','auth')
        self.assertIsNone(restarted.active())
        restarted.reserve('scope-'+'b'*32,'other','session','auth',self.root/'other.jsonl')
    def test_owner_substitution_and_missing_closure_do_not_release(self):
        self.ledger.reserve(self.sid,'action','session','auth',self.root/'controller.jsonl')
        (self.scope/'cgroup.procs').write_text('')
        (self.scope/'cgroup.events').write_text('populated 0\n')
        with self.assertRaises(OwnershipDenied):
            self.ledger.release(self.sid,'action','session','other')
        self.audit.write_text(json.dumps({'event':'scope_created','scope_id':self.sid,
            'owner':['session','auth','action']})+'\n')
        with self.assertRaises(OwnershipDenied):
            self.ledger.release(self.sid,'action','session','auth')
        self.assertIsNotNone(self.ledger.active())

if __name__=='__main__': unittest.main()
