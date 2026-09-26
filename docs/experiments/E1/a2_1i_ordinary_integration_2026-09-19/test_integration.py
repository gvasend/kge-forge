"""Synthetic decisions and isolated journals; actual C2/R1 content identities."""
import importlib.util,json,sys,tempfile,multiprocessing,unittest,time,subprocess
from pathlib import Path
from unittest.mock import patch
O=Path(__file__).resolve().parent;E=O.parent
previous=E/'a2_1i_enrollment_qualification_2026-09-19'
spec=importlib.util.spec_from_file_location('enrollment_tests',previous/'test_enrollment.py')
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)
sys.path.insert(0,str(O/'candidate'))
import enrolled_adoption as a
from adapter import runtime_adoption as r
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,sha

class Fixture(t.Fixture):
 def __init__(self,*,enroll=True,grant_change=None,selected=True):
  super().__init__();self.times={}
  begin=time.monotonic()
  with t.en.lock(self.s,self.d,False) as fd:
   t.en.validate(self.s,self.d,self.c,self.q,self.g)
  self.times['enrollment_validation']=time.monotonic()-begin
  begin=time.monotonic()
  if enroll:self.row=self.enroll()
  else:
   self.row=r.seal('CONTINUATION-ENROLLMENT',{'schema':'CONTINUATION-ENROLLMENT-1','sequence':0,
     'previous':None,'delegation':self.d['id'],'candidate':self.c,'qualification':self.q,'decision':self.g,
     'predecessor':self.before['identity'],'head_event':self.state['head_event']})
  self.times['enrollment_transaction']=time.monotonic()-begin
  g={'schema':'ENROLLED-RUNTIME-ADOPTION-DECISION-1','authority':'Architect',
     'decision':'ADOPT_EXACT_ENROLLED_CONTINUATION','binding_kind':'QUALIFICATION_BINDING',
     'lineage':self.d['lineage'],'delegation':self.d['id'],'candidate':self.c,'enrollment':self.row['id'],
     'qualification':self.q,'predecessor':self.before['identity'],'successor':self.after['identity'],
     'head_event':self.state['head_event']}
  if grant_change:g.update(grant_change)
  self.adoption=self.add(r.seal('ENROLLED-RUNTIME-ADOPTION-DECISION',g))
  if selected:self.aliases['runtime-adoption-decision:'+self.adoption['sha256']]=self.adoption['authority_id']
  material=self.add({'authority':'Architect','decision':'QUALIFY_ORDINARY_ENROLLED_ADOPTION',
    'lineage':self.d['lineage'],'delegation':self.d['id'],'implementation_sha256':sha(Path(a.__file__).read_bytes()),
    'binding_kind':'QUALIFICATION_BINDING'})
  self.aliases['integration-decision:'+material['sha256']]=material['authority_id']
  self.integration=r.seal('ORDINARY-ADOPTION-INTEGRATION',{'schema':'ORDINARY-ADOPTION-INTEGRATION-1',
    'binding_kind':'QUALIFICATION_BINDING','lineage':self.d['lineage'],'delegation':self.d['id'],
    'implementation_sha256':sha(Path(a.__file__).read_bytes()),'authority':material,
    'anchor_runtime':self.before['identity'],'anchor_head':self.state['head_event'],'journal':'fixture:ordinary-adoption'})
  ref=self.add(self.integration);self.aliases[a.SELECTOR]=ref['authority_id']
  self.ledger=self.root/'adoption.jsonl';self.ledger.touch(mode=0o600)
  self.s.close()
  self.s=ControllerAuthorityStore.materialize(self.root/'integration-store',self.records,self.aliases,
    {'authority_source':material,'release_identities':self.d['context']},
    {'enrollment_delegation':self.d['id'],'ordinary_integration':self.integration['id']},[],{
    'fixture:enrollment-journal':{'path':str(self.journal),'mutation':'APPEND_ONLY','mechanism':'CONTINUATION-ENROLLMENT-1'},
    'fixture:ordinary-adoption':{'path':str(self.ledger),'mutation':'APPEND_ONLY','mechanism':'ENROLLED-RUNTIME-EVENT-1'}})
  self.pin={'root':str(self.s.root),'catalog_sha256':self.s.catalog_sha256,'applicability':self.s.applicability}
 def adopt(self):return a.adopt(self.s,self.base,self.c,self.row['id'],self.adoption)

def worker(pin,subject,out):
 s=ControllerAuthorityStore(**pin);base=ControllerAuthorityStore(**t.PIN['selected_store'])
 try:out.put(('PASS',a.adopt(s,base,*subject)['runtime']))
 except Exception as exc:out.put(('REJECT',str(exc)))
 finally:s.close();base.close()

class Tests(unittest.TestCase):
 def fixture(self,**kwargs):
  f=Fixture(**kwargs);self.addCleanup(f.close);return f
 def test_qualification_enrollment_presence_do_not_select(self):
  f=self.fixture();state=a.reconstruct(f.s,f.base)
  self.assertEqual(state['runtime'],f.before['identity']);self.assertEqual(f.ledger.read_bytes(),b'')
  with self.assertRaisesRegex(ValueError,'unaccounted runtime'):a.verify_selected_bytes(f.s,f.base,f.after['root'])
  with self.assertRaises(ValueError):f.enroll()
  self.assertEqual(a.reconstruct(f.s,f.base)['runtime'],f.before['identity'])
 def test_synthetic_exact_adoption_and_independent_reconstruction(self):
  f=self.fixture();s=f.adopt();self.assertEqual(s['runtime'],f.after['identity'])
  code='import sys,json;sys.path[:0]=json.loads(sys.argv[1]);from adapter.controller_authority_store import ControllerAuthorityStore;import enrolled_adoption as a;s=ControllerAuthorityStore(**json.loads(sys.argv[2]));b=ControllerAuthorityStore(**json.loads(sys.argv[3]));print(json.dumps(a.reconstruct(s,b)));s.close();b.close()'
  child=subprocess.run([sys.executable,'-B','-c',code,json.dumps([str(O/'candidate'),str(previous/'candidate'),t.PIN['consumer_root']]),json.dumps(f.pin),json.dumps(t.PIN['selected_store'])],capture_output=True,text=True,timeout=30)
  self.assertEqual(child.returncode,0,child.stderr);self.assertEqual(json.loads(child.stdout),s)
  self.assertEqual(a.verify_selected_bytes(f.s,f.base,f.after['root'])['runtime'],s['runtime'])
  self.assertEqual(s['ancestry'][-1],json.loads(f.records[f.c['authority_id']]['bytes'])['id'])
 def test_missing_adoption_decision(self):
  f=self.fixture(selected=False)
  with self.assertRaises(Exception):f.adopt()
  self.assertEqual(f.ledger.read_bytes(),b'')
 def test_unenrolled_candidate(self):
  f=self.fixture(enroll=False)
  with self.assertRaisesRegex(ValueError,'missing exact enrollment'):f.adopt()
 def test_wrong_actor_and_self_authorization(self):
  for actor in ('candidate-C2','runtime-R2','not-Architect'):
   f=self.fixture(grant_change={'authority':actor})
   with self.assertRaisesRegex(ValueError,'wrong adoption'):f.adopt()
 def test_wrong_successor(self):
  f=self.fixture(grant_change={'successor':'wrong-R2'})
  with self.assertRaises(ValueError):f.adopt()
 def test_wrong_predecessor(self):
  f=self.fixture(grant_change={'predecessor':'wrong-R1'})
  with self.assertRaises(ValueError):f.adopt()
 def test_wrong_candidate(self):
  f=self.fixture(grant_change={'candidate':{'authority_id':'wrong','sha256':'0'*64}})
  with self.assertRaises(ValueError):f.adopt()
 def test_stale_adoption_head(self):
  f=self.fixture(grant_change={'head_event':'old-head'})
  with self.assertRaises(ValueError):f.adopt()
 def test_replay(self):
  f=self.fixture();f.adopt();prior=f.ledger.read_bytes()
  with self.assertRaises(ValueError):f.adopt()
  self.assertEqual(prior,f.ledger.read_bytes())
 def test_competing_requests(self):
  f=self.fixture();out=multiprocessing.Queue();subject=(f.c,f.row['id'],f.adoption)
  ps=[multiprocessing.Process(target=worker,args=(f.pin,subject,out)) for _ in range(2)]
  for p in ps:p.start()
  for p in ps:p.join(30);self.assertFalse(p.is_alive())
  self.assertEqual(sorted(out.get(timeout=2)[0] for _ in ps),['PASS','REJECT'])
 def test_interruption_recovery(self):
  for stop in (0,1,2,3):
   f=self.fixture();original=a.append;count=[0]
   def cut(*args):
    if count[0]==stop:raise InterruptedError('synthetic interruption')
    count[0]+=1;return original(*args)
   with patch.object(a,'append',side_effect=cut):
    try:f.adopt()
    except InterruptedError:pass
   state=a.recover(f.s,f.base)
   self.assertEqual(state['runtime'],f.before['identity'] if stop<2 else f.after['identity'])
   self.assertIsNone(state['pending'])
 def test_torn_record_fails_closed(self):
  f=self.fixture();f.adopt();f.ledger.write_bytes(f.ledger.read_bytes()[:-1])
  with self.assertRaisesRegex(ValueError,'INDETERMINATE'):a.recover(f.s,f.base)
 def test_exact_R2_self_hosting_is_still_blocked(self):
  f=self.fixture();s=f.adopt()
  binding={'runtime_head_authority':f.d['lineage'],'runtime':s['runtime'],'head_event':s['head']}
  # This invokes the actual frozen R2 consumer, not the new integration helper.
  with self.assertRaisesRegex(ValueError,'not current adopted head'):
   r.validate_invocation_runtime(f.base,binding,f.after['root'])
 def test_reordered_adoption_history(self):
  f=self.fixture();f.adopt();rows=f.ledger.read_bytes().splitlines(True)
  f.ledger.write_bytes(rows[1]+rows[0]+rows[2])
  with self.assertRaises(ValueError):a.reconstruct(f.s,f.base)
 def test_arbitrary_filesystem_root_not_current(self):
  f=self.fixture();f.adopt()
  with self.assertRaisesRegex(ValueError,'unaccounted runtime'):a.verify_selected_bytes(f.s,f.base,'/tmp')
 def test_distinct_competing_candidates(self):
  f=self.fixture()
  def obj(ref):return json.loads(f.records[ref['authority_id']]['bytes'])
  def reseal(kind,value):return f.add(r.seal(kind,{k:v for k,v in value.items() if k!='id'}))
  c2=reseal('FUTURE-CONTINUATION-CANDIDATE',dict(obj(f.c),proposal_nonce='distinct-synthetic-competitor'))
  q2=reseal('CONTINUATION-QUALIFICATION-ATTESTATION',dict(obj(f.q),candidate=c2))
  g2=reseal('CONTINUATION-ENROLLMENT-DECISION',dict(obj(f.g),candidate=c2,qualification=q2))
  f.aliases['qualification-attestation:'+q2['sha256']]=q2['authority_id']
  f.aliases['enrollment-decision:'+g2['sha256']]=g2['authority_id']
  def publish(name):
   state=dict(f.s.catalog['private_state']);app=dict(f.s.applicability);f.s.close()
   f.s=ControllerAuthorityStore.materialize(f.root/name,f.records,f.aliases,
    {'authority_source':f.integration['authority'],'release_identities':f.d['context']},app,[],state)
   f.pin={'root':str(f.s.root),'catalog_sha256':f.s.catalog_sha256,'applicability':f.s.applicability}
  publish('competitor-enrollment')
  row2=t.en.enroll(f.s,f.base,c2,q2,g2,binding_kind='QUALIFICATION_BINDING')
  adoption2=reseal('ENROLLED-RUNTIME-ADOPTION-DECISION',dict(obj(f.adoption),candidate=c2,qualification=q2,enrollment=row2['id']))
  f.aliases['runtime-adoption-decision:'+adoption2['sha256']]=adoption2['authority_id'];publish('competitor-adoption')
  out=multiprocessing.Queue();subjects=[(f.c,f.row['id'],f.adoption),(c2,row2['id'],adoption2)]
  ps=[multiprocessing.Process(target=worker,args=(f.pin,x,out)) for x in subjects]
  for p in ps:p.start()
  for p in ps:p.join(30);self.assertFalse(p.is_alive())
  self.assertEqual(sorted(out.get(timeout=2)[0] for _ in ps),['PASS','REJECT'])
  self.assertEqual(len(a.reconstruct(f.s,f.base)['events']),3)

if __name__=='__main__':unittest.main(verbosity=2)
