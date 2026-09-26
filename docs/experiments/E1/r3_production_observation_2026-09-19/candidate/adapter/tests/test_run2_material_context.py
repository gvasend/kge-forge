"""Real historical context; malicious/synthetic prospective catalogs only."""
import copy,json,os,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,sha
from adapter.run2_context import content,verify_dispatch
from adapter.run2_amendment import sealed
from adapter.context_projection import digest

ROOT=Path(__file__).resolve().parents[2]
RESULT=ROOT/'docs/experiments/E1/run2_nonhost_closure_2026-09-17/PROBE_RESULT.json'

class MaterialContextTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  report=json.loads(RESULT.read_bytes());assert report['result']=='PASS_EXCEPT_CURRENT_SUPERVISOR'
  cls.s=ControllerAuthorityStore(**report['selected_store']);cls.app=dict(cls.s.applicability)
  cls.a=cls.app['authorization_id'];cls.raw=json.loads(cls.s.resolve(cls.a));cls.op=json.loads(cls.raw['operational_binding'])
  cls.base={k:{'bytes':(cls.s.root/v['sha256']).read_bytes(),'evidence':[]} for k,v in cls.s.catalog['objects'].items()}
  cls.private=json.loads(encoded(cls.s.catalog['private_state']));cls.roots=list(cls.s.catalog['programmer_roots'])
 @classmethod
 def tearDownClass(cls):cls.s.close()
 def setUp(self):
  self.records=copy.deepcopy(self.base);self.spec=copy.deepcopy(self.op['governance'])
  self.sel=json.loads(self.records[self.a+':run2-context']['bytes']);self.tmp=tempfile.TemporaryDirectory(prefix='run2-negative-')
 def tearDown(self):self.tmp.cleanup()
 def put(self,obj):
  b=encoded(obj);h=sha(b);self.records['sha256:'+h]={'bytes':b,'evidence':[]}
  return {'authority_id':'sha256:'+h,'sha256':h}
 def read(self,ref):return json.loads(self.records[ref['authority_id']]['bytes'])
 def candidate(self,change):
  c=self.read(self.sel['candidate']);body={k:v for k,v in c.items() if k!='id'};change(body)
  ref=self.put(sealed('E1-RUN2-RELEASE-AMENDMENT',body));self.sel['candidate']=ref;self.spec['candidate']=ref
 def check(self,full=False):
  self.records[self.a+':run2-context']={'bytes':encoded(self.sel),'evidence':[]}
  # Only fixture catalog durability is outside the subject of these negative
  # semantic probes. Initial actual candidate materialization uses real fsync.
  from unittest.mock import patch
  with patch('adapter.controller_authority_store.os.fsync'):
   s=ControllerAuthorityStore.materialize(Path(self.tmp.name)/'store',self.records,{},
    {'authority_source':self.sel['candidate'],'release_identities':self.app},self.app,self.roots,self.private)
  try:
   with s.session():
    if full in ('dispatch','dispatch_and_projection'):
     from adapter.authority_bootstrap import reconstruct_authorization
     auth=reconstruct_authorization(s,self.a)
     decision=json.loads(s.resolve(self.sel['dispatch_decision']['authority_id']))
     mode=verify_dispatch(auth,decision)
     if full=='dispatch_and_projection':
      from adapter.context_projection import derive
      result=derive(json.loads(auth.context_projection),auth.context_binding)
      self.assertEqual({k:result[k] for k in self.op['context_identities']},self.op['context_identities'])
     return mode
    if full:
     from adapter.run2_context import verify
     return verify(SimpleNamespace(spec=self.spec,_issued_digest=digest(self.spec)))
    return content(self.spec)
  finally:s.close()
 def test_valid_content(self):self.check()
 def test_missing_decision(self):
  del self.records[self.sel['release_decision']['authority_id']]
  with self.assertRaises(ValueError):self.check(full=True)
 def test_wrong_authority(self):
  r=self.read(self.sel['release_decision']);r.pop('id');r['authority']='Programmer'
  self.sel['release_decision']=self.put(sealed('E1-RUN2-RELEASE-DECISION',r))
  with self.assertRaisesRegex(ValueError,'release decision mismatch'):self.check(full=True)
 def test_stale_and_reordered_ancestry(self):
  self.candidate(lambda c:c['predecessor_operational_context'].update(continuation_chain_digest='stale'))
  with self.assertRaisesRegex(ValueError,'ancestry/payload/budget'):self.check()
 def test_payload_substitution(self):
  self.candidate(lambda c:c.update(ModelPayloadDigest='0'*64))
  with self.assertRaisesRegex(ValueError,'ancestry/payload/budget'):self.check()
 def test_budget_substitution(self):
  self.candidate(lambda c:c['budget_policy']['seconds']['phase'].__setitem__(1,9999))
  with self.assertRaisesRegex(ValueError,'ancestry/payload/budget'):self.check()
 def test_profile_substitution(self):
  def change(c):
   p=self.read(c['profile']);p['write_roots']=['/'];c['profile']=self.put(p)
  self.candidate(change)
  with self.assertRaisesRegex(ValueError,'profile changes authority'):self.check()
 def test_transmission_retention_substitution(self):
  def change(c):
   p=self.read(c['policy']);p['action_evidence']='ALL_PROTECTED_CONTENT';c['policy']=self.put(p)
  self.candidate(change)
  with self.assertRaisesRegex(ValueError,'transmission/retention'):self.check()
 def test_task_substitution(self):
  def change(c):
   p=self.read(c['payload']);p['payload']['task']='different work';c['payload']=self.put(p)
  self.candidate(change)
  with self.assertRaisesRegex(ValueError,'model payload substitution'):self.check()
 def test_implementation_substitution(self):
  def change(c):
   p=self.read(c['implementation']);name=next(iter(p['inventory']));p['inventory'][name]='0'*64
   p['identity']='sha256:'+digest(p['inventory']);c['implementation']=self.put(p)
  self.candidate(change)
  with self.assertRaisesRegex(ValueError,'implementation changed'):self.check()
 def test_unexplained_context_field(self):
  self.spec['unexplained']='authority'
  with self.assertRaisesRegex(ValueError,'operational spec changed'):self.check(full=True)
 def test_synthetic_issued_decisions_preserve_frozen_context(self):
  self.sel['mode']='ISSUED'
  release=self.read(self.sel['release_decision']);release.pop('id')
  release['decision']='AUTHORIZE_E1_RUN2_RELEASE'
  source={k:release[k] for k in ('authority','decision','candidate','resulting_release_authority','predecessor')}
  release['authority_source']=self.put(dict(source,channel='user'))
  release=sealed('E1-RUN2-RELEASE-DECISION',release);self.sel['release_decision']=self.put(release)
  d=self.read(self.sel['dispatch_decision']);d['decision']='DISPATCH_AUTHORIZED';d['release_decision']=release['id']
  expected={k:d[k] for k in ('authority','decision','release_authority','release_decision','ModelPayloadDigest','invocation_identity')}
  d['authority_source']=self.put(dict(expected,channel='user',binding_sha256=digest(d['all_authorized_bindings'])))
  self.sel['dispatch_decision']=self.put(d)
  self.assertEqual(self.check(full='dispatch_and_projection'),'ISSUED')
 def test_missing_run2_dispatch(self):
  del self.records[self.sel['dispatch_decision']['authority_id']]
  with self.assertRaises(ValueError):self.check(full='dispatch')
 def test_wrong_run2_dispatch_authority(self):
  d=self.read(self.sel['dispatch_decision']);d['authority']='Programmer'
  self.sel['dispatch_decision']=self.put(d)
  with self.assertRaisesRegex(ValueError,'cannot inherit'):self.check(full='dispatch')
 def test_historical_dispatch_cannot_inherit(self):
  c=self.read(self.sel['candidate']);prior=self.read(c['predecessor_authorization'])
  g=json.loads(prior['operational_binding'])['governance']
  amendment=self.read(g['material_release']['dispatch_amendment'])
  self.sel['dispatch_decision']=amendment['original_dispatch']
  with self.assertRaisesRegex(ValueError,'cannot inherit'):self.check(full='dispatch')
 def test_direct_production_gate_rejects_candidate(self):
  from adapter.run2_context import selection
  with self.s.session():
   with self.assertRaisesRegex(ValueError,'cannot authorize effects'):selection(self.a,issued=True)
 def test_dispatch_entry_rejects_prospective_before_audit_mutation(self):
  from adapter.controlled_dispatch import dispatch
  audit=Path(self.private[self.a+':audit']['path']);before=audit.read_bytes()
  with self.assertRaisesRegex(ValueError,'cannot authorize effects'):dispatch(self.s,self.a)
  self.assertEqual(audit.read_bytes(),before)
 def test_nonhost_report_cannot_be_activation_proof(self):
  from adapter.authorization_lifecycle import valid_validation
  # The production validator's emitted schema and identity are mandatory. A
  # non-host report has neither, even if its human-facing result contains PASS.
  proof={'schema':'NON-EFFECTING-RUN2-PREFLIGHT-1','result':'PASS_EXCEPT_CURRENT_SUPERVISOR'}
  self.assertFalse(valid_validation(proof,{}))

if __name__=='__main__':unittest.main()
