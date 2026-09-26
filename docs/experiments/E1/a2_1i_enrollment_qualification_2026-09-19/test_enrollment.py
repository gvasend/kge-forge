"""Isolated enrollment stores, real C2 content and read-only production R1.
Synthetic qualification/enrollment decisions never enter production catalogs.
"""
import importlib.util, json, multiprocessing, sys, tempfile, unittest, os, fcntl
from unittest.mock import patch
from pathlib import Path
O=Path(__file__).resolve().parent; E=O.parent
PIN=json.loads((E/'runtime_bootstrap_application_2026-09-19/AUTHORIZED_SELECTION.json').read_bytes())
sys.path.insert(0,PIN['consumer_root']);sys.path.insert(0,str(O/'candidate'))
from adapter import runtime_adoption as r
from adapter.controller_authority_store import ControllerAuthorityStore, encoded, sha
import continuation_enrollment as en

class Fixture:
 def __init__(self, mutation=None):
  self.root=Path(tempfile.mkdtemp(prefix='enrollment-qualification-'));self.root.chmod(0o700)
  self.base=ControllerAuthorityStore(**PIN['selected_store']);self.records={};self.aliases={}
  self.state=r.reconstruct(self.base);p=r.policy(self.base)
  before=r.descriptor(self.base,self.state['current_descriptor'],live=True)
  content=json.loads((E/'runtime_c2_qualification_2026-09-19/CONTENT_CANDIDATE.json').read_bytes())
  after={'schema':'RUNTIME-INVENTORY-1','identity':content['successor'],'files':content['successor_files'],'root':PIN['consumer_root']}
  for d in (before,after):
   for n,h in d['files'].items():
    data=(Path(d['root'])/'adapter'/n).read_bytes();assert sha(data)==h;self.add(data)
  self.before=before;self.after=after
  self.c=self.add(r.seal('FUTURE-CONTINUATION-CANDIDATE',{'schema':'FUTURE-CONTINUATION-CANDIDATE-1',
    'predecessor':self.add(before),'successor':self.add(after),'delta':content['delta'],
    'lineage':p['id'],'context':p['release_context'],
    'content_candidate':{'id':content['id'],'sha256':sha((E/'runtime_c2_qualification_2026-09-19/CONTENT_CANDIDATE.json').read_bytes())}}))
  src={'authority':'Architect','decision':'DELEGATE_FUTURE_ENROLLMENT','lineage':p['id'],
       'binding_kind':'QUALIFICATION_BINDING','capability':'ENROLL_EXACT_QUALIFIED_CONTINUATION_ONLY'}
  self.d=r.seal('CONTINUATION-ENROLLMENT-DELEGATION',{'schema':'CONTINUATION-ENROLLMENT-DELEGATION-1',
   'lineage':p['id'],'context':p['release_context'],'binding_kind':'QUALIFICATION_BINDING',
   'capability':src['capability'],'authority_source':self.add(src),'mechanism_sha256':sha(Path(en.__file__).read_bytes()),
   'qualification_policy':'fixture:exact-content-and-enrollment-contract','journal':'fixture:enrollment-journal'})
  self.q=self.add(r.seal('CONTINUATION-QUALIFICATION-ATTESTATION',{'schema':'CONTINUATION-QUALIFICATION-ATTESTATION-1',
   'candidate':self.c,'result':'PASS','qualification_policy':self.d['qualification_policy'],
   'binding_kind':'QUALIFICATION_BINDING','evidence':[self.add({'scope':'SYNTHETIC_ENROLLMENT_CONTRACT_ONLY',
   'inventory_and_delta_verified':True,'not_production_C2_qualification':True})]}))
  self.g=self.add(r.seal('CONTINUATION-ENROLLMENT-DECISION',{'schema':'CONTINUATION-ENROLLMENT-DECISION-1',
   'authority':'Architect','decision':'ENROLL_ONLY','delegation':self.d['id'],'candidate':self.c,
   'qualification':self.q,'binding_kind':'QUALIFICATION_BINDING','head_event':self.state['head_event']}))
  self.aliases={'qualification-attestation:'+self.q['sha256']:self.q['authority_id'],
                'enrollment-decision:'+self.g['sha256']:self.g['authority_id']}
  if mutation:mutation(self)
  self.aliases[en.DELEGATION]=self.add(self.d)['authority_id']
  self.journal=self.root/'enrollment.jsonl';self.journal.touch(mode=0o600)
  self.s=ControllerAuthorityStore.materialize(self.root/'store',self.records,self.aliases,
    {'authority_source':self.add(self.d),'release_identities':p['release_context']},
    {'enrollment_delegation':self.d['id']},[],{'fixture:enrollment-journal':{
      'path':str(self.journal),'mutation':'APPEND_ONLY','mechanism':'CONTINUATION-ENROLLMENT-1'}})
  self.pin={'root':str(self.s.root),'catalog_sha256':self.s.catalog_sha256,'applicability':self.s.applicability}
 def add(self,value):
  data=value if isinstance(value,bytes) else encoded(value);h=sha(data)
  self.records['sha256:'+h]={'bytes':data,'evidence':[]};return {'authority_id':'sha256:'+h,'sha256':h}
 def grant(self,**changes):
  g=json.loads(self.records[self.g['authority_id']]['bytes']);g.pop('id');g.update(changes)
  self.g=self.add(r.seal('CONTINUATION-ENROLLMENT-DECISION',g));self.aliases['enrollment-decision:'+self.g['sha256']]=self.g['authority_id']
 def enroll(self):return en.enroll(self.s,self.base,self.c,self.q,self.g,binding_kind='QUALIFICATION_BINDING')
 def eligible(self,row):return en.require_eligible(self.s,self.base,self.c,row['id'],binding_kind='QUALIFICATION_BINDING')
 def close(self):self.s.close();self.base.close()

def worker(pin,base_pin,c,q,g,out):
 s=ControllerAuthorityStore(**pin);base=ControllerAuthorityStore(**base_pin)
 try:out.put(('PASS',en.enroll(s,base,c,q,g,binding_kind='QUALIFICATION_BINDING')['id']))
 except Exception as exc:out.put(('REJECT',str(exc)))
 finally:s.close();base.close()

class Tests(unittest.TestCase):
 def fixture(self,mutation=None):
  f=Fixture(mutation);self.addCleanup(f.close);return f
 def test_exact_real_candidate_eligibility_not_adoption(self):
  f=self.fixture();row=f.enroll();self.assertEqual(f.eligible(row),row)
  self.assertEqual(r.reconstruct(f.base)['current_runtime'],f.before['identity'])
  self.assertEqual(r.reconstruct(f.base)['head_event'],f.state['head_event'])
  # Established ordinary validator still cannot treat enrollment as adoption.
  with self.assertRaisesRegex(ValueError,'unselected adoption authority'):r.transition(f.base,r.policy(f.base),f.c,f.g)
 def test_qualified_unenrolled_rejected(self):
  f=self.fixture()
  with self.assertRaisesRegex(ValueError,'absent or mismatched'):f.eligible({'id':'absent'})
 def test_enrollment_replay_non_effecting(self):
  f=self.fixture();f.enroll();prior=f.journal.read_bytes()
  with self.assertRaisesRegex(ValueError,'replay'):f.enroll()
  self.assertEqual(prior,f.journal.read_bytes())
 def test_other_candidate_after_enrollment(self):
  f=self.fixture();row=f.enroll();f.c=dict(f.c,sha256='0'*64)
  with self.assertRaises(ValueError):f.eligible(row)
 def test_unauthorized_actor(self):
  f=self.fixture(lambda f:f.grant(authority='candidate-producer'))
  with self.assertRaisesRegex(ValueError,'unauthorized'):f.enroll()
  self.assertEqual(f.journal.read_bytes(),b'')
 def test_object_presence_is_not_enrollment_authority(self):
  f=self.fixture(lambda f:f.aliases.pop('enrollment-decision:'+f.g['sha256']))
  with self.assertRaises(Exception):f.enroll()
 def test_qualification_without_trusted_attestation(self):
  f=self.fixture(lambda f:f.aliases.pop('qualification-attestation:'+f.q['sha256']))
  with self.assertRaises(Exception):f.enroll()
 def test_stale_head_decision(self):
  f=self.fixture(lambda f:f.grant(head_event='stale-head'))
  with self.assertRaisesRegex(ValueError,'stale enrollment'):f.enroll()
 def test_wrong_qualification_binding(self):
  f=self.fixture(lambda f:f.grant(qualification=f.c))
  with self.assertRaises(ValueError):f.enroll()
 def test_missing_delegation(self):
  f=self.fixture()
  # Missing pinned delegation bytes must fail; only isolated copy is changed.
  target=f.s.root/sha(encoded(f.d));target.unlink()
  with self.assertRaises(Exception):f.enroll()
 def test_wrong_delegation(self):
  f=self.fixture(lambda f:f.grant(delegation='unrelated-lineage'))
  with self.assertRaises(ValueError):f.enroll()
 def test_qualification_cannot_be_used_in_production(self):
  f=self.fixture()
  with self.assertRaisesRegex(ValueError,'boundary'):
   en.enroll(f.s,f.base,f.c,f.q,f.g,binding_kind='PRODUCTION_ENROLLMENT')
 def test_torn_record_blocks(self):
  f=self.fixture();row=f.enroll();f.journal.write_bytes(f.journal.read_bytes()[:-1])
  with self.assertRaisesRegex(ValueError,'INDETERMINATE'):f.eligible(row)
 def test_changed_record_blocks(self):
  f=self.fixture();row=f.enroll();x=dict(row,head_event='substituted');f.journal.write_bytes(encoded(x)+b'\n')
  with self.assertRaises(ValueError):f.eligible(row)
 def test_concurrent_same_enrollment_only_one_event(self):
  f=self.fixture();out=multiprocessing.Queue();ps=[multiprocessing.Process(target=worker,args=(f.pin,PIN['selected_store'],f.c,f.q,f.g,out)) for _ in range(2)]
  for p in ps:p.start()
  for p in ps:p.join(20);self.assertFalse(p.is_alive())
  self.assertEqual(sorted(out.get(timeout=2)[0] for _ in ps),['PASS','REJECT'])
  self.assertEqual(len(f.journal.read_bytes().splitlines()),1)
 def test_restart(self):
  f=self.fixture();row=f.enroll();s=ControllerAuthorityStore(**f.pin)
  try:self.assertEqual(en.require_eligible(s,f.base,f.c,row['id'],binding_kind='QUALIFICATION_BINDING'),row)
  finally:s.close()
 def test_synthetic_head_change_invalidates_enrollment(self):
  f=self.fixture();row=f.enroll()
  # Explicit fault injection at the authenticated reconstruction boundary.
  # This is a freshness unit probe, not a production runtime transition.
  changed=dict(f.state,current_runtime=f.after['identity'],head_event='synthetic-later-head')
  with patch.object(r,'reconstruct_locked',return_value=changed):
   with self.assertRaisesRegex(ValueError,'stale enrollment'):f.eligible(row)
 def test_synthetic_wrong_predecessor_blocks(self):
  f=self.fixture();changed=dict(f.state,current_runtime='synthetic-other-predecessor')
  with patch.object(r,'reconstruct_locked',return_value=changed):
   with self.assertRaisesRegex(ValueError,'stale enrollment'):f.enroll()
  self.assertEqual(f.journal.read_bytes(),b'')
 def test_private_candidate_substitution_blocks(self):
  f=self.fixture();row=f.enroll();(f.s.root/f.c['sha256']).write_bytes(b'{}')
  with self.assertRaises(Exception):f.eligible(row)
 def test_private_qualification_substitution_blocks(self):
  f=self.fixture();(f.s.root/f.q['sha256']).write_bytes(b'{}')
  with self.assertRaises(Exception):f.enroll()
 def test_fsync_interruption_recovers_exact_record(self):
  f=self.fixture()
  with patch.object(en.os,'fsync',side_effect=InterruptedError('fixture interruption')):
   with self.assertRaises(InterruptedError):f.enroll()
  row=json.loads(f.journal.read_bytes())
  self.assertEqual(f.eligible(row),row)
  with self.assertRaisesRegex(ValueError,'replay'):f.enroll()
 def test_head_stays_locked_through_enrollment_append(self):
  f=self.fixture();write=en.os.write
  path=f.base.state_path(r.policy(f.base)['journal'])
  def observe(fd,data):
   other=os.open(path,os.O_RDONLY)
   try:
    with self.assertRaises(BlockingIOError):fcntl.flock(other,fcntl.LOCK_EX|fcntl.LOCK_NB)
   finally:os.close(other)
   return write(fd,data)
  with patch.object(en.os,'write',side_effect=observe):f.enroll()

if __name__=='__main__':unittest.main(verbosity=2)
