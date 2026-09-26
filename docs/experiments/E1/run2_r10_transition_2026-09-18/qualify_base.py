"""Synthetic private authority/attempt/lifecycle qualification; no E1 inputs."""
import json,os,sys,tempfile,threading,time,unittest,subprocess
from pathlib import Path
from dataclasses import replace
from unittest.mock import patch
from adapter.tests.qualify_activation_transaction import fixture
from adapter.tests.test_controller_authority_store import private_fixture
from adapter.context_projection import canonical,digest,sha
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.invocation_attempt import BOUND,authenticate,claim,child_dispatch,require_claim
from adapter.invocation_issuance import issue_inactive,start_control
from adapter.run_control import RunControl,E1_POLICY,events,status,BudgetExceeded
from adapter.validation_spans import recording
from adapter.activation_transaction import ActivationTransaction
from adapter.authorization_lifecycle import reconstruct,LifecycleDenied

class Composition(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(prefix='synthetic-attempt-pair-');self.out=Path(self.tmp.name)
  _,a,audit,ref,_=fixture(self.out/'f',supervisor_identity={'fixture':'SYNTHETIC_NONLIVE'})
  original=json.loads(Path(ref['path']).read_bytes())
  audit.rename(self.out/'fixture_setup.evidence')
  c=RunControl(audit,{'authorization_id':a.authorization_id,'session_id':a.session_id,'invocation_id':a.turn_id,'work_package_id':a.work_package_id},E1_POLICY)
  c.close('SYNTHETIC_PREISSUANCE_FAILURE');c.emit('final_disposition',{'disposition':'BLOCKED_BEFORE_AUTHORIZATION_ISSUANCE','uncertainty':None})
  self.failed=audit;self.failed_bytes=audit.read_bytes()
  for k in BOUND:original.setdefault(k,'synthetic-'+k)
  old_id='E1-ARCHITECT-DISPATCH-sha256:'+digest(original)
  new={'authorization_id':a.authorization_id+'-B','session_id':a.session_id+'-B','turn_id':a.turn_id+'-B','revision':a.revision+1}
  op=json.loads(a.operational_binding);op['invocation_identity']=new
  self.auth=replace(a,**new,operational_binding=canonical(op));self.audit=self.out/'B.jsonl'
  p={'schema':'INVOCATION-ATTEMPT-BINDING-1','DispatchAuthorizationId':old_id,
    'dispatch':{'authority_id':old_id,'sha256':digest(original)},
    'predecessor':{'authorization_id':a.authorization_id,'audit':str(audit),'audit_sha256':sha(self.failed_bytes)},
    'invocation_identity':new,'audit':str(self.audit),'bindings':{k:original[k] for k in BOUND},
    'replacement_operational_binding_sha256':digest(op),'initial_state':'INACTIVE','ownership':'NONE',
    'automatic_retry':False,'reason':'Explicit synthetic Architect-authorized replacement after pre-effect failure'}
  p['InvocationAttemptId']='InvocationAttempt-sha256:'+digest({'dispatch':old_id,'predecessor':p['predecessor'],'invocation_identity':new,'audit':p['audit']})
  self.p=p;self.ref={'authority_id':'sha256:'+digest(p),'sha256':digest(p)}
  approval={'authority':'Architect','decision':'AUTHORIZE_SPECIFIC_REPLACEMENT_INVOCATION','proposal':self.ref,
    'DispatchAuthorizationId':old_id,'InvocationAttemptId':p['InvocationAttemptId'],'automatic_retry':False}
  source=dict(approval,channel='user');sr={'authority_id':'sha256:'+digest(source),'sha256':digest(source)}
  approval['authority_source']=sr
  # Capture B's immutable runtime dependencies without granting a production identity.
  temporary=dict(original,invocation_identity=new,authority_source=original['authority_source'])
  temporary['all_authorized_bindings']=dict(original['all_authorized_bindings'],audit=str(self.audit),operational_binding_sha256=digest(op))
  tempref=self.out/'SYNTHETIC_CAPTURE_ONLY_DISPATCH.json';tempref.write_text(canonical(temporary))
  base=private_fixture(self.auth,self.audit,{'path':str(tempref),'sha256':sha(tempref.read_bytes())},self.out/'base')
  records={k:{'bytes':base.resolve(k),'evidence':[]} for k in base.catalog['objects']}
  def add(k,v):records[k]={'bytes':canonical(v).encode(),'evidence':[]}
  add(old_id,original);add(self.ref['authority_id'],p);add(sr['authority_id'],source);add(old_id+':replacement-approval',approval)
  child=dict(original,invocation_identity=new,authority_source=sr,invocation_attempt=self.ref,parent_dispatch=p['dispatch'])
  child['all_authorized_bindings']=dict(original['all_authorized_bindings'],audit=str(self.audit),operational_binding_sha256=digest(op))
  self.child_id='E1-ARCHITECT-DISPATCH-sha256:'+digest(child);add(self.child_id,child)
  self.child_ref={'authority_id':self.child_id,'sha256':digest(child)}
  ledger=self.out/'attempts.jsonl';ledger.touch(mode=0o600)
  private=json.loads(canonical(dict(base.catalog['private_state']))) if False else {k:dict(v) for k,v in base.catalog['private_state'].items()}
  self.ledger_id=old_id+':attempt-ledger';private[self.ledger_id]={'path':str(ledger),'mutation':'APPEND_ONLY','mechanism':'invocation_attempt.claim'}
  self.store=ControllerAuthorityStore.materialize(self.out/'private',records,{},
    {'authority_source':sr,'release_identities':dict(base.applicability)},dict(base.applicability),list(base.catalog['programmer_roots']),private)
  base.close();self.s=self.store.session();self.s.__enter__()
  self.mock=patch('adapter.activation_transaction._host',return_value={'fixture':'SYNTHETIC_NONLIVE'});self.mock.start()
  self.tx=None
 def tearDown(self):
  if self.tx:self.tx.close()
  self.mock.stop();self.s.__exit__(None,None,None);self.store.close();self.tmp.cleanup()
 def issue(self):
  claim(self.store,self.ref,self.ledger_id)
  host=issue_inactive(self.auth,self.audit,self.child_ref)
  self.control=start_control(self.auth,self.audit,E1_POLICY)
  return host
 def activate(self):
  self.issue()
  with recording(self.control),self.control.span('validation'):
   self.tx=ActivationTransaction.activate(self.auth,self.audit,self.child_id)
  return self.tx
 def test_integrated_A_closed_B_active_independent_recovery(self):
  tx=self.activate();tx.close()
  spec={'root':str(self.store.root),'catalog_sha256':self.store.catalog_sha256,'applicability':self.store.applicability}
  code='''import json,sys
from unittest.mock import patch
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.activation_transaction import ActivationTransaction
s=ControllerAuthorityStore(**json.loads(sys.argv[1]))
with s.session(),patch('adapter.activation_transaction._host',return_value={'fixture':'SYNTHETIC_NONLIVE'}):
 a=reconstruct_authorization(s,sys.argv[2]);t=ActivationTransaction.recover(a,sys.argv[3],sys.argv[4]);print(json.dumps(t.recovery));t.close()
'''
  p=subprocess.run([sys.executable,'-c',code,canonical(spec),self.auth.authorization_id,str(self.audit),self.child_id],capture_output=True,text=True,timeout=30)
  self.assertEqual(p.returncode,0,p.stderr);r=json.loads(p.stdout);self.assertTrue(r['handoff_eligible']);self.assertIsNotNone(r['ownership'])
  rows=events(self.audit);self.assertEqual(rows[0]['event'],'authorization_issued')
  self.assertEqual(rows[0]['authorization']['state'],'INACTIVE')
  names=[r['event'] for r in rows];self.assertLess(names.index('authorization_lifecycle_activation_intent'),names.index('authorization_lifecycle_activated'))
  self.assertEqual(self.failed.read_bytes(),self.failed_bytes)
 def test_A_cannot_reopen_and_B_cannot_replay(self):
  with self.assertRaises(LifecycleDenied):issue_inactive(self.auth,self.failed,self.child_ref)
  self.issue();before=self.audit.read_bytes()
  with self.assertRaises(ValueError):claim(self.store,self.ref,self.ledger_id)
  with self.assertRaises(LifecycleDenied):issue_inactive(self.auth,self.audit,self.child_ref)
  self.assertEqual(before,self.audit.read_bytes())
 def test_no_claim_no_authority_and_missing_approval(self):
  with self.assertRaises(ValueError):issue_inactive(self.auth,self.audit,self.child_ref)
  original=self.store.resolve
  def missing(k):
   if k.endswith(':replacement-approval'):raise ValueError('missing selected Architect decision')
   return original(k)
  with patch.object(self.store,'resolve',side_effect=missing):
   with self.assertRaises(ValueError):claim(self.store,self.ref,self.ledger_id)
  self.assertFalse(self.audit.exists())
 def test_substitution_rejected(self):
  original=self.store.resolve
  for key in BOUND:
   p=json.loads(canonical(self.p));p['bindings'][key]='substituted'
   ref={'authority_id':'sha256:'+digest(p),'sha256':digest(p)}
   with patch.object(self.store,'resolve',side_effect=lambda k,p=p,ref=ref:canonical(p).encode() if k==ref['authority_id'] else original(k)):
    with self.assertRaises(ValueError):authenticate(self.store,ref)
 def test_effecting_or_uncertain_predecessor_rejected(self):
  with self.failed.open('a') as f:f.write(canonical({'event':'action_request','action_request_id':'synthetic-effect'})+'\n')
  with self.assertRaises(ValueError):claim(self.store,self.ref,self.ledger_id)
  self.assertFalse(self.audit.exists())
 def test_two_candidates_race_one_allocation(self):
  barrier=threading.Barrier(2);results=[]
  def go():
   barrier.wait()
   try:claim(self.store,self.ref,self.ledger_id);results.append('allocated')
   except (ValueError,LifecycleDenied):results.append('denied')
  threads=[threading.Thread(target=go) for _ in range(2)]
  for t in threads:t.start()
  for t in threads:t.join(5);self.assertFalse(t.is_alive())
  self.assertEqual(sorted(results),['allocated','denied'])
 def test_status_concurrent_with_lifecycle(self):
  self.issue();stop=threading.Event();count=[]
  def read():
   while not stop.is_set():
    try:status(self.audit);count.append(1)
    except ValueError:pass # partial read is unknown, never an authority assertion
    time.sleep(.01)
  t=threading.Thread(target=read);t.start()
  try:
   with recording(self.control),self.control.span('validation'):
    self.tx=ActivationTransaction.activate(self.auth,self.audit,self.child_id)
  finally:stop.set();t.join(3)
  self.assertFalse(t.is_alive());self.assertGreater(len(count),0)
 def test_telemetry_failure_after_ACTIVE_does_not_rollback(self):
  self.issue();emit=self.control.emit
  def fail(name,details):
   if name=='span_end' and details.get('name')=='validation':raise OSError('synthetic telemetry failure after authority commit')
   return emit(name,details)
  with patch.object(self.control,'emit',side_effect=fail),self.assertRaises(OSError):
   with recording(self.control),self.control.span('validation'):
    self.tx=ActivationTransaction.activate(self.auth,self.audit,self.child_id)
  self.tx.close();self.tx=ActivationTransaction.recover(self.auth,self.audit,self.child_id)
  self.assertTrue(self.tx.recovery['handoff_eligible'])
 def test_lifecycle_failure_not_hidden_by_telemetry(self):
  self.issue()
  with patch('adapter.activation_transaction.validate_production',side_effect=ValueError('synthetic validation failure')):
   with self.assertRaises(ValueError),recording(self.control),self.control.span('validation'):
    ActivationTransaction.activate(self.auth,self.audit,self.child_id)
  self.tx=ActivationTransaction.recover(self.auth,self.audit,self.child_id)
  self.assertEqual(self.tx.recovery['lifecycle_state'],'INACTIVE');self.assertFalse(self.tx.recovery['handoff_eligible'])

 def restart(self):
  spec={'root':str(self.store.root),'catalog_sha256':self.store.catalog_sha256,'applicability':self.store.applicability}
  code='''import json,sys
from unittest.mock import patch
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.activation_transaction import ActivationTransaction
s=ControllerAuthorityStore(**json.loads(sys.argv[1]))
with s.session(),patch('adapter.activation_transaction._host',return_value={'fixture':'SYNTHETIC_NONLIVE'}):
 a=reconstruct_authorization(s,sys.argv[2]);t=ActivationTransaction.recover(a,sys.argv[3],sys.argv[4]);print(json.dumps(t.recovery));t.close()
'''
  r=subprocess.run([sys.executable,'-c',code,canonical(spec),self.auth.authorization_id,str(self.audit),self.child_id],capture_output=True,text=True,timeout=30)
  self.assertEqual(r.returncode,0,r.stderr);return json.loads(r.stdout)
 def cut(self,name,eligible,owned,uncertain):
  self.issue()
  from adapter import activation_transaction as at
  append=at._append
  def crash(fd,row):
   append(fd,row)
   if row['event']==name:raise OSError('synthetic crash after durable '+name)
  with patch.object(at,'_append',side_effect=crash),self.assertRaises(OSError),recording(self.control),self.control.span('validation'):
   ActivationTransaction.activate(self.auth,self.audit,self.child_id)
  r=self.restart();self.assertEqual(r['handoff_eligible'],eligible);self.assertEqual(r['ownership'] is not None,owned)
  self.assertEqual(r['reconciliation_required'],uncertain)
 def test_restart_after_INACTIVE(self):
  claim(self.store,self.ref,self.ledger_id);issue_inactive(self.auth,self.audit,self.child_ref)
  r=self.restart();self.assertEqual(r['lifecycle_state'],'INACTIVE');self.assertFalse(r['handoff_eligible'])
 def test_restart_after_telemetry(self):
  self.issue();r=self.restart();self.assertEqual(r['lifecycle_state'],'INACTIVE');self.assertIsNone(r['ownership'])
 def test_restart_after_validation(self):self.cut('production_dispatch_validated',False,False,False)
 def test_restart_after_dispatch_fact(self):self.cut('authorization_lifecycle_dispatch_authorized',False,False,False)
 def test_restart_after_intent(self):self.cut('authorization_lifecycle_activation_intent',False,False,True)
 def test_restart_after_ownership(self):self.cut('invocation_reserved',False,True,True)
 def test_restart_after_ACTIVE(self):self.cut('authorization_lifecycle_activated',True,True,False)
 def test_telemetry_failure_inside_transaction_cannot_fabricate_ACTIVE(self):
  self.issue();emit=self.control.emit
  def fail(name,details):
   if name=='span_start' and details.get('name')=='model_projection':raise OSError('synthetic telemetry failure under lock')
   return emit(name,details)
  with patch.object(self.control,'emit',side_effect=fail),self.assertRaises(OSError),recording(self.control),self.control.span('validation'):
   ActivationTransaction.activate(self.auth,self.audit,self.child_id)
  r=self.restart();self.assertEqual(r['lifecycle_state'],'INACTIVE');self.assertIsNone(r['ownership'])
 def test_budget_alarm_inside_locked_validation(self):
  self.issue()
  from adapter import activation_transaction as at
  original=at.validate_production
  def delayed(*args,**kwargs):
   self.control.start=time.monotonic()-1799.8
   self.control._arm()
   time.sleep(.5)
   return original(*args,**kwargs)
  with patch.object(at,'validate_production',side_effect=delayed),self.assertRaises(BudgetExceeded),recording(self.control),self.control.span('validation'):
   ActivationTransaction.activate(self.auth,self.audit,self.child_id)
  rows=events(self.audit);self.assertTrue(any(r['event']=='budget_exhausted' for r in rows))
  self.assertFalse(any(r['event']=='authorization_lifecycle_activated' for r in rows))
 def test_two_different_successor_candidates_race(self):
  p=json.loads(canonical(self.p));p['invocation_identity']['authorization_id']+='-C';p['invocation_identity']['turn_id']+='-C';p['invocation_identity']['session_id']+='-C';p['audit']=str(self.out/'C.jsonl')
  p['InvocationAttemptId']='InvocationAttempt-sha256:'+digest({'dispatch':p['DispatchAuthorizationId'],'predecessor':p['predecessor'],'invocation_identity':p['invocation_identity'],'audit':p['audit']})
  ref={'authority_id':'sha256:'+digest(p),'sha256':digest(p)}
  approval={'authority':'Architect','decision':'AUTHORIZE_SPECIFIC_REPLACEMENT_INVOCATION','proposal':ref,'DispatchAuthorizationId':p['DispatchAuthorizationId'],'InvocationAttemptId':p['InvocationAttemptId'],'automatic_retry':False}
  source=dict(approval,channel='user');sr={'authority_id':'sha256:'+digest(source),'sha256':digest(source)};approval['authority_source']=sr
  records={k:{'bytes':self.store.resolve(k),'evidence':[]} for k in self.store.catalog['objects']}
  for k,v in ((ref['authority_id'],p),(sr['authority_id'],source),(p['DispatchAuthorizationId']+':replacement-approval',approval)):records[k]={'bytes':canonical(v).encode(),'evidence':[]}
  private={k:dict(v) for k,v in self.store.catalog['private_state'].items()}
  other=ControllerAuthorityStore.materialize(self.out/'other',records,{}, {'authority_source':sr,'release_identities':dict(self.store.applicability)},dict(self.store.applicability),list(self.store.catalog['programmer_roots']),private)
  barrier=threading.Barrier(2);results=[]
  def go(store,proposal):
   barrier.wait()
   try:claim(store,proposal,self.ledger_id);results.append('allocated')
   except (ValueError,LifecycleDenied):results.append('denied')
  ts=[threading.Thread(target=go,args=(self.store,self.ref)),threading.Thread(target=go,args=(other,ref))]
  try:
   for t in ts:t.start()
   for t in ts:t.join(5);self.assertFalse(t.is_alive())
   self.assertEqual(sorted(results),['allocated','denied'])
  finally:other.close()
 def test_bound_effecting_or_uncertain_predecessor_semantics(self):
  from adapter.invocation_attempt import predecessor_no_effects
  for event in ({'event':'authorization_issued','authorization':{}},
                {'event':'model_request_content_bound'},
                {'event':'action_request'},
                {'event':'execution_scope_created'}):
   self.failed.write_bytes(self.failed_bytes+(canonical(event)+'\n').encode())
   p=json.loads(canonical(self.p));p['predecessor']['audit_sha256']=sha(self.failed.read_bytes())
   with self.assertRaises(ValueError):predecessor_no_effects(p)
  self.failed.write_bytes(self.failed_bytes)
 def test_original_dispatch_substitution(self):
  original=self.store.resolve
  def substituted(k):
   b=original(k)
   if k==self.p['DispatchAuthorizationId']:
    d=json.loads(b);d['work_package_id']='different';return canonical(d).encode()
   return b
  with patch.object(self.store,'resolve',side_effect=substituted):
   with self.assertRaises(ValueError):authenticate(self.store,self.ref)
 def test_audit_contention_fails_without_blocking(self):
  import fcntl
  self.issue();fd=os.open(self.audit,os.O_RDWR);fcntl.flock(fd,fcntl.LOCK_EX)
  begin=time.monotonic()
  try:
   with self.assertRaises(BlockingIOError):ActivationTransaction.activate(self.auth,self.audit,self.child_id)
   self.assertLess(time.monotonic()-begin,5)
  finally:os.close(fd)
  self.assertEqual(self.restart()['lifecycle_state'],'INACTIVE')

if __name__=='__main__':unittest.main(verbosity=2)
