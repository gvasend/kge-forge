"""Synthetic S3 records over genuine immutable S1→S2 history; no launch."""
import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from adapter.controller_authority_store import ControllerAuthorityStore,encoded,sha
from adapter.context_projection import digest
from adapter.supervisor_succession import reconstruct,sealed,equivalent
from adapter.run2_context import supervisor_prefix
ROOT=Path(__file__).resolve().parents[2]

class SupervisorEpochTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  report=json.loads((ROOT/'docs/experiments/E1/run2_nonhost_closure_2026-09-17/PROBE_RESULT.json').read_bytes())
  old=ControllerAuthorityStore(**report['selected_store']);cls.tmp=tempfile.TemporaryDirectory(prefix='synthetic-supervisor-epoch-')
  records={k:{'bytes':(old.root/v['sha256']).read_bytes(),'evidence':[]} for k,v in old.catalog['objects'].items()}
  with old.session():prefix=supervisor_prefix(old)
  s2=json.loads(old.resolve(prefix['instance']));body=copy.deepcopy({k:v for k,v in s2.items() if k!='id'})
  body['process'].update(pid=414141,ppid=414140,start_ticks=424242,parent_start_ticks=424240)
  body['socket'].update(listener_pid=414141,listener_start_ticks=424242)
  binding=dict(body['runtime_binding'],**old.applicability);body['runtime_binding']=binding
  config=equivalent(dict(body,id='SYNTHETIC'))
  def put(value,alias=None):
   b=encoded(value);h=sha(b);records['sha256:'+h]={'bytes':b,'evidence':[]}
   if alias:records[alias]={'bytes':b,'evidence':[]}
   return 'sha256:'+h
  host={'schema':'SUPERVISOR-HOST-LAUNCH-1','authority':'HOST_OPERATOR','authorized_launch':True,
   'runtime_binding':binding,'process':body['process'],'configuration':config,
   'parent_start_identity':{'pid':414140,'boot_id':body['process']['boot_id'],'start_ticks':424240},
   'command_sha256':'SYNTHETIC','operator_authorization_id':'SYNTHETIC_NO_HOST_CONSENT',
   'delegated_before_credentials_dropped':True,'runtime_uid':1000,'runtime_gid':1000,'synthetic':True}
  body['host_launch']=put(host);s3=sealed('SupervisorInstance',body);put(s3,s3['id'])
  evidence={'schema':'SUPERVISOR-PREDECESSOR-EVIDENCE-1','instance_id':s2['id'],'runtime_binding':binding,
   'status':'UNAVAILABLE','authority':'HOST_OPERATOR','observation_id':'SYNTHETIC','observed_at':'SYNTHETIC',
   'process_absent':True,'listener_absent':True,'outstanding_scopes_accounted':True}
  q={'schema':'SUPERVISOR-QUALIFICATION-1','instance_id':s3['id'],'runtime_binding':binding,'result':'PASS',
   'configuration':config,'capture_sha256':'SYNTHETIC_NOT_HOST_QUALIFICATION'}
  row={'schema':'SUPERVISOR-SUCCESSION-1','sequence':2,'predecessor_event':prefix['head'],
   'predecessor_instance':s2['id'],'predecessor_status':'UNAVAILABLE','predecessor_evidence':put(evidence),
   'successor_instance':s3['id'],'reason':'SYNTHETIC_EPOCH_PROBE','host_launch':body['host_launch'],
   'qualification':put(q),'runtime_binding':binding}
  approval={'schema':'SUPERVISOR-SUCCESSION-AUTHORIZATION-1','authority':'Architect',
   'decision':'AUTHORIZE_SUPERVISOR_SUCCESSION','event_body_sha256':digest(row),'reason':row['reason']}
  aid=put(approval);cls.row=sealed('SupervisorSuccession',dict(row,architect_authorization=aid))
  cls.policy={'schema':'SUPERVISOR-SUCCESSION-POLICY-2','runtime_binding':binding,
   'historical_prefix':prefix['reference'],'anchor_id':s2['id'],'requirements':config,
   'authorized_succession_ids':[aid],'pinned_head':cls.row['id']}
  with patch('adapter.controller_authority_store.os.fsync'):
   cls.s=ControllerAuthorityStore.materialize(Path(cls.tmp.name)/'store',records,{},
    {'authority_source':{'sha256':'0'*64},'release_identities':old.applicability},old.applicability,list(old.catalog['programmer_roots']))
  cls.s2=s2;cls.s3=s3;cls.prefix=prefix;old.close()
 @classmethod
 def tearDownClass(cls):cls.s.close();cls.tmp.cleanup()
 def run_rows(self,rows,policy=None):
  with self.s.session():return reconstruct(self.s,policy or self.policy,b''.join(encoded(r)+b'\n' for r in rows))
 def test_valid_epoch_succession_and_recovery(self):
  a=self.run_rows([self.row]);b=self.run_rows([self.row]);self.assertEqual(a,b)
  self.assertEqual(a['instance'],self.s3);self.assertEqual(a['sequence'],2)
  self.assertEqual(json.loads(self.s.resolve(self.s2['id'])),self.s2)
 def test_replay_non_effecting(self):self.assertEqual(self.run_rows([self.row]),self.run_rows([self.row,self.row]))
 def test_reordered_or_wrong_binding_rejected(self):
  for change in ({'sequence':1},{'predecessor_event':None},{'runtime_binding':self.s2['runtime_binding']},{'predecessor_instance':self.s3['id']}):
   row=dict(self.row,**change);row.pop('id');row=sealed('SupervisorSuccession',row)
   with self.subTest(change=change),self.assertRaises(ValueError):self.run_rows([row])
 def test_no_event_only_recovers_historical_predecessor(self):
  p=dict(self.policy,pinned_head=self.prefix['head']);r=self.run_rows([],p)
  self.assertEqual(r['instance'],self.s2)
  self.assertNotEqual(r['instance']['runtime_binding'],p['runtime_binding'])

if __name__=='__main__':unittest.main()
