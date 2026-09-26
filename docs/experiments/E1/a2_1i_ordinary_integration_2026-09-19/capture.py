"""Fresh read-only S3/history checks plus isolated enrollment/adoption timing."""
import json,sys,time,subprocess
from pathlib import Path
from unittest.mock import patch
O=Path(__file__).resolve().parent;E=O.parent;sys.path.insert(0,str(O))
import test_integration as q
from adapter.controller_authority_store import encoded,sha
from adapter import runtime_bootstrap as b,runtime_adoption as r
records=[];samples=[]
for index in range(3):
 measurements={'enrollment_append_io':0.0,'adoption_append_io':0.0,'head_commit_io':0.0}
 original_enroll=q.t.Fixture.enroll
 def measured_enroll(self):
  write=q.t.en.os.write;fsync=q.t.en.os.fsync
  def write_span(*args):
   t=time.monotonic()
   try:return write(*args)
   finally:measurements['enrollment_append_io']+=time.monotonic()-t
  def sync_span(*args):
   t=time.monotonic()
   try:return fsync(*args)
   finally:measurements['enrollment_append_io']+=time.monotonic()-t
  with patch.object(q.t.en.os,'write',side_effect=write_span),patch.object(q.t.en.os,'fsync',side_effect=sync_span):
   return original_enroll(self)
 with patch.object(q.t.Fixture,'enroll',measured_enroll):f=q.Fixture()
 try:
  measurements.update(f.times)
  t=time.monotonic();q.a.transition(f.s,f.d,f.c,f.row['id'],f.adoption);measurements['adoption_validation']=time.monotonic()-t
  original_append=q.a.append
  def measured_append(fd,p,s,event,subject):
   t=time.monotonic()
   try:return original_append(fd,p,s,event,subject)
   finally:
    dt=time.monotonic()-t;measurements['adoption_append_io']+=dt
    if event=='COMMITTED':measurements['head_commit_io']+=dt
  t=time.monotonic()
  with patch.object(q.a,'append',side_effect=measured_append):state=f.adopt()
  measurements['adoption_transaction']=time.monotonic()-t
  code='import sys,json;sys.path[:0]=json.loads(sys.argv[1]);from adapter.controller_authority_store import ControllerAuthorityStore;import enrolled_adoption as a;s=ControllerAuthorityStore(**json.loads(sys.argv[2]));b=ControllerAuthorityStore(**json.loads(sys.argv[3]));print(json.dumps(a.reconstruct(s,b)));s.close();b.close()'
  t=time.monotonic();child=subprocess.run([sys.executable,'-B','-c',code,json.dumps([str(O/'candidate'),str(q.previous/'candidate'),q.t.PIN['consumer_root']]),json.dumps(f.pin),json.dumps(q.t.PIN['selected_store'])],capture_output=True,text=True,timeout=120)
  measurements['independent_reconstruction']=time.monotonic()-t
  assert child.returncode==0,child.stderr
  assert json.loads(child.stdout)==state
  t=time.monotonic();q.a.verify_selected_bytes(f.s,f.base,f.after['root']);measurements['external_runtime_verification']=time.monotonic()-t
  binding={'runtime_head_authority':f.d['lineage'],'runtime':state['runtime'],'head_event':state['head']}
  try:r.validate_invocation_runtime(f.base,binding,f.after['root']);raise AssertionError('unexpected self-hosted adoption')
  except ValueError as exc:
   blocker=str(exc);assert 'not current adopted head' in blocker
  records.append({'index':index,'label':'cold_process_sample' if index==0 else 'warm_sample',
   'timings_seconds':measurements,'individual_soft_threshold':30,'individual_hard_threshold':120,
   'timing_pass':max(measurements.values())<30,'synthetic_state':state,
   'exact_R2_self_hosting':'BLOCKED','exact_R2_failure':blocker,'MODEL_REQUEST_READY':'NOT_REACHED'})
  samples.append({'candidate':json.loads(f.records[f.c['authority_id']]['bytes']),
    'candidate_ref':f.c,'qualification':json.loads(f.records[f.q['authority_id']]['bytes']),
    'delegation':f.d,'enrollment':f.row,'adoption':json.loads(f.records[f.adoption['authority_id']]['bytes']),
    'integration':f.integration,'store_pin':f.pin,'scope':'SYNTHETIC_ONLY_NOT_PRODUCTION_AUTHORITY'})
 finally:f.close()

base=q.t.ControllerAuthorityStore(**q.t.PIN['selected_store'])
try:
 p,record,selector=b.verify_records(base)
 t=time.monotonic();b.fresh_supervisor(base,record);supervisor_seconds=time.monotonic()-t
 current=b.reconstruct(base)
 prior=json.loads((E/'a2_1i_enrollment_2026-09-19/EVIDENCE.json').read_bytes())
 assert all(sha(Path(path).read_bytes())==digest for path,digest in prior['journal_hashes_unchanged'].items())
 R=E/'run2_r12_dispatch_2026-09-18'
 history=json.loads((R/'HISTORICAL_BASELINE.json').read_bytes())
 history.update({str(R/k):v for k,v in json.loads((R/'EVIDENCE_HASHES.json').read_bytes()).items()})
 proof=json.loads((E/'run2_control_plane_binding_2026-09-18/R12_AUTHENTICATED_CAPTURE.json').read_bytes())
 history[proof['publication']['path']]=proof['publication']['sha256']
 history['/tmp/kge-forge-e1-invocations.jsonl']=proof['terminal']['ledger_sha256']
 assert all(sha(Path(path).read_bytes())==digest for path,digest in history.items())
 output={'verdict':'BLOCKED_EXACT_R2_SELF_HOSTING','samples':records,
    'S3':'EXACT_EXCLUSIVE_READY','S3_seconds':supervisor_seconds,'production_runtime':current,
    'historical_files_passed':len(history),'unchanged_journals':prior['journal_hashes_unchanged'],
    'complete_post_adoption_premodel_timing':None,'qualification_only':True,
    'real_C2_enrolled':False,'real_C2_adopted':False,'r13_created':False,'model_requests':0,'E1_effects':0}
 for name,value in [('RESULT.json',output),('SYNTHETIC_RECORDS.json',samples)]:
  with (O/name).open('xb') as stream:stream.write(encoded(value))
 print(json.dumps({k:v for k,v in output.items() if k!='samples'},indent=2))
finally:base.close()
