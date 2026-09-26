"""Isolated negative probes for reusable parsing, never production authority."""
import json,sys,tempfile,unittest,hashlib
from pathlib import Path
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O/'candidate'))
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,sha,pure_resolution,require_effect_boundary,AuthorityDenied
from adapter.run_control import RunControl,E1_POLICY,events,_verified_tail,decode_events
from adapter.operator_projection import observational_extension
from types import SimpleNamespace
class Reuse(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.r=Path(self.t.name);self.grant=self.r/'grant';self.grant.mkdir()
  self.data=encoded({'immutable':'history'});self.h=sha(self.data);self.i='sha256:'+self.h
  self.s=ControllerAuthorityStore.materialize(self.r/'store',{self.i:{'bytes':self.data,'evidence':[]}}, {},{'authority_source':{'sha256':'0'*64},'release_identities':{'ReleaseBasisId':'fixture','ReleaseDecisionId':'fixture'}},{'authorization_id':'fixture'},[str(self.grant)])
 def tearDown(self):self.s.close();self.t.cleanup()
 def test_batch_boundaries(self):
  @pure_resolution
  def verified():return self.s.resolve(self.i)
  with self.s.session():self.assertEqual(verified(),self.data)
  before=(self.s.root/'catalog.json').read_bytes()
  @pure_resolution
  def tamper():
   result=self.s.resolve(self.i);(self.s.root/'catalog.json').write_bytes(before+b' ');return result
  with self.s.session():
   with self.assertRaises(ValueError):tamper()
  (self.s.root/'catalog.json').write_bytes(before)
  with self.s.session():self.assertEqual(verified(),self.data)
 def test_effect_and_nested_authority_rejected(self):
  @pure_resolution
  def effect():require_effect_boundary()
  with self.s.session():
   with self.assertRaises(ValueError):effect()
   with self.assertRaises(ValueError):
    with self.s.session():pass
   require_effect_boundary()
 def test_object_and_placement_fresh(self):
  @pure_resolution
  def verify():return self.s.resolve(self.i)
  with self.s.session():
   self.assertEqual(verify(),self.data)
   (self.s.root/self.h).write_bytes(b'forged')
   with self.assertRaises(ValueError):verify()
  (self.s.root/self.h).write_bytes(self.data);self.grant.rmdir();self.grant.symlink_to(self.s.root)
  with self.assertRaises(ValueError):
   with self.s.session():verify()
 def test_incremental_matches_full_with_typed_interleave(self):
  p=self.r/'audit';c=RunControl(p,{'authorization_id':'test'},E1_POLICY)
  state=None
  for i in range(20):
   c.emit('activity',{'operation':'validation'})
   if i==5:
    with p.open('ab') as f:f.write(b'{"event":"synthetic_typed_record"}\n')
   data=p.read_bytes();state=_verified_tail(data,state);rows=decode_events(data)
   telemetry=[r for r in rows if r.get('schema')=='E1-RUN-CONTROL-1']
   self.assertEqual(state[1],len(telemetry));self.assertEqual(state[2],telemetry[-1]['record_sha256']);self.assertEqual(state[3].hexdigest(),sha(data))
  restarted=RunControl(p,{'authorization_id':'test'},E1_POLICY);restarted.emit('activity',{'operation':'validation'});events(p)
  for corrupt in (data[:-1],b''.join(reversed(data.splitlines(keepends=True))),data.replace(b'validation',b'corruption',1)):
   with self.assertRaises(ValueError):_verified_tail(corrupt,state)
 def test_history_reuse_closes_over_exact_dependencies(self):
  from adapter.controller_authority_store import reuse_pure_history
  source=self.r/'historical';source.write_bytes(b'exact historical evidence');calls=[]
  @reuse_pure_history
  def historical():
   calls.append(1);return {'sha256':sha(source.read_bytes())}
  @pure_resolution
  def phase(change=False):
   first=historical();self.assertEqual(first,historical())
   if change:source.write_bytes(b'changed')
   return first
  with self.s.session():
   phase();self.assertEqual(len(calls),2)
   with self.assertRaises(ValueError):phase(True)
   self.assertEqual(len(calls),4)
   phase();self.assertEqual(len(calls),6)
 def test_history_missing_and_caller_copy_do_not_confer_authority(self):
  from adapter.controller_authority_store import reuse_pure_history
  source=self.r/'historical';source.write_bytes(b'exact')
  @reuse_pure_history
  def historical():return {'sha256':sha(source.read_bytes())}
  @pure_resolution
  def phase():
   one=historical();one['sha256']='caller';self.assertNotEqual(one,historical());source.unlink()
  with self.s.session():
   with self.assertRaises(FileNotFoundError):phase()
   require_effect_boundary()
 def test_status_cycle_and_unknown_are_separate_from_predecessor(self):
  auth=SimpleNamespace(authorization_id='q',session_id='s',turn_id='t',work_package_id='w');identity={'authorization_id':'q','session_id':'s','invocation_id':'t','work_package_id':'w'}
  p=self.r/'audit';c=RunControl(p,identity,E1_POLICY);c.cycle=1
  prefix=p.read_bytes();c.emit('activity',{'operation':'model_projection'})
  self.assertTrue(observational_extension(prefix,p.read_bytes(),auth))
  from adapter.evidence_semantics import classify_record
  with self.assertRaises(ValueError):classify_record(events(p)[-1],identity)
  for event,details in [('span_start',{'name':'unknown'}),('model_request_start',{}),('budget_exhausted',{}),('ownership_acquired',{}),('uncertainty',{})]:
   before=p.read_bytes();c.emit(event,details);self.assertFalse(observational_extension(before,p.read_bytes(),auth))
 def test_legacy_projection_observation_strict_identity_and_schema(self):
  projection={k:'fixed-'+k for k in ('AuthoritativeContextId','FullContextDigest','ModelPayloadDigest','ModelProjectionBindingDigest','ModelProjectionDigest')}
  auth=SimpleNamespace(authorization_id='q',session_id='s',turn_id='t',work_package_id='w',operational_binding=json.dumps({'context_identities':projection}))
  row=dict(projection,authorization_id='q',session_id='s',turn_id='t',event='context_projection_verified',time=1.0)
  def encoded_row(value):return (json.dumps(value)+'\n').encode()
  self.assertTrue(observational_extension(b'',encoded_row(row),auth))
  for bad in (dict(row,ModelPayloadDigest='substituted'),dict(row,authorization_id='other'),dict(row,classification='NON_EFFECTING_OBSERVATION'),dict(row,time='unknown'),dict(row,event='model_request_started')):
   self.assertFalse(observational_extension(b'',encoded_row(bad),auth))
if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Reuse))
 (O/'REUSE_QUALIFICATION.json').write_text(json.dumps({'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'result':'PASS' if result.wasSuccessful() else 'FAIL'}))
 sys.exit(not result.wasSuccessful())
