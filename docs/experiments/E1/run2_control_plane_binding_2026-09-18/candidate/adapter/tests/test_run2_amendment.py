"""Private fixture decisions only: no real approval, launch, activation or dispatch."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from adapter.controller_authority_store import ControllerAuthorityStore, encoded, sha
from adapter.context_projection import digest
from adapter.run2_amendment import verify, sealed, RUN1_AUTH, PRIOR_RELEASE, PRIOR_AMENDMENT, PAYLOAD, SCOPES
from adapter.run_control import E1_POLICY

ROOT = Path(__file__).resolve().parents[2]
REMEDIATION = ROOT/'docs/experiments/E1/run2_remediation_2026-09-17'
PIN = Path('/tmp/kge-forge-controller-authority')/RUN1_AUTH/'supervisor-succession-adoption-2026-09-17/SUCCESSION_PUBLICATION.json'


def fixture():
    pin = PIN.read_bytes()
    assert sha(pin) == '95a2454b094f2b6e4af044cbfa8a8efd98a225866e2b19fc286a2d63abdacd4e'
    old = ControllerAuthorityStore(**json.loads(pin)['selected_store'])
    try:
        raw = json.loads(old.resolve(RUN1_AUTH))
        g = json.loads(raw['operational_binding'])['governance']
        records = {}
        def keep(ref):
            key='sha256:'+ref['sha256'];data=old.resolve(key)
            records[key]={'bytes':data,'evidence':[]}
            try:return json.loads(data)
            except ValueError:return None
        keep(g['release_basis'])
        decision=keep(g['release_decision']);keep(decision['authority_source'])
        prior=keep(g['material_release']['release_decision'])
        keep(prior['candidate']);keep(prior['authority_source'])
    finally:
        old.close()
    def put(value):
        data = encoded(value); h = sha(data)
        records['sha256:'+h] = {'bytes': data, 'evidence': []}
        return {'authority_id':'sha256:'+h,'sha256':h}
    def logical(ref): return {'authority_id':'sha256:'+ref['sha256'],'sha256':ref['sha256']}
    inventory = {str(p):sha(p.read_bytes()) for p in sorted((ROOT/'adapter').glob('*.py'))}
    iid = 'sha256:'+digest(inventory)
    # PASS applies solely inside this isolated fixture. It is not published.
    c = {'schema':'E1-RUN2-RELEASE-AMENDMENT-1', 'fixture':'SYNTHETIC_NEW_DECISIONS',
        'prior_release_authority':PRIOR_RELEASE,'prior_supervisor_amendment':PRIOR_AMENDMENT,
        'material_scopes':list(SCOPES),'ModelPayloadDigest':PAYLOAD,'budget_policy':E1_POLICY,
        'work_package':'E1-WP-001','new_invocation_required':True,'successor_instance':None,
        'host_launch_authorization':None,'original_release_decision':logical(g['release_decision']),
        'original_release_basis':logical(g['release_basis']),
        'prior_supervisor_decision':g['material_release']['release_decision'],
        'profile':put(json.loads((REMEDIATION/'PROPOSED_RUN2_PROFILE.json').read_bytes())),
        'payload':put(json.loads((REMEDIATION/'PROPOSED_MODEL_PAYLOAD.json').read_bytes())),
        'policy':put(json.loads((REMEDIATION/'PROPOSED_TRANSMISSION_AND_RUN_POLICY.json').read_bytes())),
        'implementation':put({'identity':iid,'inventory':inventory}),
        'qualification':put({'result':'PASS','implementation_identity':iid,'fixture':True}),
        'predecessor_operational_context':{k:g['identities'][k] for k in ('OperationalContextId','continuation_chain_digest')},
        'applicable_continuations':[]}
    candidate = sealed('E1-RUN2-RELEASE-AMENDMENT',c); cr = put(candidate)
    rid = 'E1-RELEASE-AUTHORITY-sha256:'+digest({'predecessor':PRIOR_RELEASE,'Run2AmendmentId':candidate['id']})
    head = {'OperationalContextId':'E1-OPERATIONAL-CONTEXT-sha256:'+digest({'predecessor':c['predecessor_operational_context']['OperationalContextId'],'Run2AmendmentId':candidate['id']}),
        'continuation_chain_digest':digest({'predecessor':c['predecessor_operational_context']['continuation_chain_digest'],'Run2AmendmentId':candidate['id']})}
    source = put({'authority':'Architect','channel':'user','decision':'AUTHORIZE_E1_RUN2_RELEASE','candidate':cr,'resulting_release_authority':rid})
    release = sealed('E1-RUN2-RELEASE-DECISION',{'authority':'Architect','decision':'AUTHORIZE_E1_RUN2_RELEASE','candidate':cr,'resulting_release_authority':rid,'authority_source':source})
    d = {'authority':'Architect','decision':'AUTHORIZE_E1_RUN2_DISPATCH','authorization_id':'synthetic-run2',
        'release_authority':rid,'release_decision':release['id'],'ModelPayloadDigest':PAYLOAD,'profile':c['profile'],'operational_context':head}
    dispatch_source = put(dict(d,channel='user'))
    dr = put(sealed('E1-RUN2-DISPATCH-DECISION',dict(d,authority_source=dispatch_source)))
    selected = {'candidate':cr,'release_decision':put(release),'dispatch_decision':dr,'continuations':[],'operational_context':head}
    return records,selected,put,head


class Run2DecisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base,cls.selection,_,cls.head = fixture()
    def setUp(self):
        self.records = copy.deepcopy(self.base); self.selected = copy.deepcopy(self.selection)
        self.tmp = tempfile.TemporaryDirectory(prefix='run2-decisions-synthetic-')
    def tearDown(self): self.tmp.cleanup()
    def check(self):
        self.records['synthetic-run2:run2-material'] = {'bytes':encoded(self.selected),'evidence':[]}
        s = ControllerAuthorityStore.materialize(Path(self.tmp.name)/'store',self.records,{},
            {'authority_source':self.selected['release_decision'],'release_identities':{'ReleaseBasisId':'SYNTHETIC_FIXTURE','ReleaseDecisionId':'SYNTHETIC_FIXTURE'}},
            dict(self.head,authorization_id='synthetic-run2'),[str(ROOT)])
        try:
            with s.session(): return verify('synthetic-run2')
        finally:s.close()
    def test_actual_predecessor_synthetic_new_decisions(self):
        self.assertTrue(self.check()['release_authority'].startswith('E1-RELEASE-AUTHORITY-sha256:'))
    def test_missing_release(self):
        del self.records[self.selected['release_decision']['authority_id']]
        with self.assertRaises(ValueError):self.check()
    def test_missing_dispatch(self):
        del self.records[self.selected['dispatch_decision']['authority_id']]
        with self.assertRaises(ValueError):self.check()
    def test_substituted_hash(self):
        self.selected['candidate']['sha256']='0'*64
        with self.assertRaises(ValueError):self.check()
    def test_repository_reference(self):
        self.selected['candidate']={'path':'/tmp/candidate','sha256':'0'*64}
        with self.assertRaises(ValueError):self.check()
    def test_reordered_decisions(self):
        self.selected['release_decision'],self.selected['dispatch_decision']=self.selected['dispatch_decision'],self.selected['release_decision']
        with self.assertRaises(ValueError):self.check()
    def test_stale_head(self):
        self.selected['operational_context']['continuation_chain_digest']='stale'
        with self.assertRaises(ValueError):self.check()
    def test_unapproved_continuation(self):
        self.selected['continuations']=[self.selected['candidate']]
        with self.assertRaises(ValueError):self.check()
    def test_run1_dispatch_cannot_be_reused(self):
        self.selected['dispatch_decision']=self.selected['release_decision']
        with self.assertRaises(ValueError):self.check()
    def test_independent_reopen(self):
        first=self.check()
        # Reconstruct a new catalog/object handle, no cached decisions.
        self.tmp.cleanup();self.tmp=tempfile.TemporaryDirectory(prefix='run2-reopen-synthetic-')
        self.assertEqual(first,self.check())

if __name__=='__main__': unittest.main()
