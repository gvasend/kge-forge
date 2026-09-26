import json,sys,time
from pathlib import Path
from unittest.mock import patch
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O))
import test_runtime as t
from adapter import ordinary_runtime as a,continuation_enrollment as en
from adapter.controller_authority_store import encoded
Q=t.Q;measurements=[]
for index in range(3):
 f=t.Fixture();row={'sample':index,'seconds':{}}
 try:
  # New isolated fixture representing the authenticated R1 anchor, before C3
  # enrollment/adoption. Original qualification and production journals untouched.
  f.ledger.write_bytes(b'');f.enrollment.write_bytes(b'')
  p,d,_=a.policy(f.s)
  def measure(name,fn):
   begin=time.monotonic()
   try:return fn()
   finally:row['seconds'][name]=time.monotonic()-begin
  measure('enrollment_validation',lambda:en.validate(f.s,d,Q['continuation_ref'],Q['enrollment']['qualification'],Q['enrollment']['decision']))
  recorded=measure('enrollment_transaction',lambda:a.enroll(f.s,Q['continuation_ref'],Q['enrollment']['qualification'],Q['enrollment']['decision']))
  measure('adoption_validation',lambda:a.transition(f.s,d,Q['continuation_ref'],recorded['id'],Q['adoption_ref']))
  append=a.append;commit=[]
  def timed_append(fd,p,s,event,subject):
   start=time.monotonic()
   try:return append(fd,p,s,event,subject)
   finally:
    if event=='COMMITTED':commit.append(time.monotonic()-start)
  with patch.object(a,'append',side_effect=timed_append):
   state=measure('adoption_transaction',lambda:a.adopt(f.s,None,Q['continuation_ref'],recorded['id'],Q['adoption_ref']))
  row['seconds']['runtime_head_commit']=commit[0]
  b=a.binding(f.s)
  verified=measure('self_hosting_validation',lambda:a.validate_executing_runtime(f.s,b))
  assert verified['runtime']==Q['R3']['identity']
  measure('runtime_head_verification',lambda:a.binding(f.s))
  child=measure('independent_self_hosting_process',lambda:t.child_validate(f.pin,Q['R3']['root'],b))
  assert child.returncode==0,child.stderr
  assert json.loads(child.stdout)==verified
  er4=measure('future_R4_enrollment',lambda:a.enroll(f.s,Q['R4_ref'],Q['R4_enrollment']['qualification'],Q['R4_enrollment']['decision']))
  measure('future_R4_eligibility',lambda:a.eligible(f.s,Q['R4_ref'],er4['id']))
  assert a.reconstruct(f.s)['runtime']==Q['R3']['identity']
  row.update(R3_self_hosting='PASS',R4='ELIGIBLE_UNADOPTED',store=f.pin,phase_soft_threshold=30,phase_hard_threshold=120)
  row['performance_pass']=max(row['seconds'].values())<30;measurements.append(row)
 finally:f.close()
with (O/'RUNTIME_TIMING.json').open('xb') as out:out.write(encoded(measurements))
print(json.dumps(measurements,indent=2))
