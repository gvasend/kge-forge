"""Bounded, read-only actual amended context qualification. No r10 issuance."""
import json,os,sys,time,signal
from pathlib import Path
from contextlib import contextmanager
from dataclasses import replace
sys.path.insert(0,json.loads((Path(sys.argv[1])/'PREPARED_PUBLICATION.json').read_bytes())['runtime_root'])
from adapter.context_projection import canonical,sha,derive
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.governance_continuation import verify_authorization
from adapter.activation_transaction import _validate_production,invocation
from adapter.invocation_ownership import InvocationOwnership
from adapter.authorization_lifecycle import reconstruct,LifecycleDenied
from adapter.invocation_issuance import issue_inactive
from adapter.controlled_dispatch import dispatch
from adapter.validation_spans import recording
from adapter.run_control import E1_POLICY,assert_admission,BudgetExceeded

run=Path(sys.argv[1]);pub=json.loads((run/'PREPARED_PUBLICATION.json').read_bytes());out=run/'PREFLIGHT.json'
records=[];seq=0
class Diagnostics:
 @contextmanager
 def span(self,name):
  global seq
  start=time.monotonic();wall=time.time();seq+=1;number=seq
  try:yield
  finally:
   duration=time.monotonic()-start
   records.append({'schema':'PRE_ISSUANCE_OPERATIONAL_DIAGNOSTIC-1','sequence':number,
     'operation':name,'wall_start':wall,'monotonic_start':start,'seconds':duration,
     'authorization_lifecycle':False,'soft_exceeded':duration>=30,'hard_exceeded':duration>=120})
   (run/'PRE_ISSUANCE_DIAGNOSTICS.json').write_text(canonical(records))
diag=Diagnostics()
def alarm(*_):raise TimeoutError('pre-issuance qualification phase exceeded 120 seconds')
def bounded(name,fn):
 signal.signal(signal.SIGALRM,alarm);signal.setitimer(signal.ITIMER_REAL,120)
 try:
  with diag.span(name):return fn()
 finally:signal.setitimer(signal.ITIMER_REAL,0);signal.signal(signal.SIGALRM,signal.SIG_DFL)
s=ControllerAuthorityStore(**pub['selected_store']);A=s.applicability['authorization_id'];results={}
with s.session(),recording(diag):
 a=bounded('cold_private_bootstrap',lambda:reconstruct_authorization(s,A))
 g=a.context_binding.governance;p=g.run7['proposal'];audit=Path(p['audit']);assert not os.path.lexists(audit)
 oldaudit=Path(p['predecessors'][-1]['audit']);failed=oldaudit.read_bytes();assert sha(failed)==p['predecessors'][-1]['audit_sha256']
 own=InvocationOwnership(a.ownership_ledger);ledger_before=Path(a.ownership_ledger).read_bytes()
 def validate():
  fd=own._locked()
  try:
   assert invocation(fd) is None and own._history(fd) is None
   return _validate_production(a,audit,pub['dispatch'],fd,_preissuance=True)
  finally:os.close(fd)
 results['cold_validation']=bounded('cold_preissuance_production_validation',validate)
 results['warm_validation']=bounded('warm_preissuance_production_validation',validate)
 op=bounded('operational_context_reconstruction',lambda:verify_authorization(a))
 projection=bounded('model_projection_validation',lambda:derive(json.loads(a.context_projection),a.context_binding))
 assert projection['ModelPayloadDigest']==p['bindings']['ModelPayloadDigest']
 def denied(name,fn):
  try:fn()
  except (ValueError,FileNotFoundError,BudgetExceeded) as e:results[name]={'result':'REJECTED','reason':str(e)}
  else:raise AssertionError(name+' unexpectedly accepted')
 denied('arbitrary_r11',lambda:verify_authorization(replace(a,authorization_id='auth-E1-arbitrary-r11')))
 denied('r11_issuance_without_specific_authorization',lambda:issue_inactive(a,audit,pub['dispatch']))
 denied('model_handoff_before_issuance',lambda:dispatch(s,A))
 from adapter.run_control import events
 rows=events(oldaudit);ident=next(r['identity'] for r in rows if r.get('schema')=='E1-RUN-CONTROL-1')
 denied('r10_admission_reopening',lambda:assert_admission(oldaudit,E1_POLICY,ident))
 assert oldaudit.read_bytes()==failed and Path(a.ownership_ledger).read_bytes()==ledger_before and not os.path.lexists(audit)
 results.update(result='PASS_PROSPECTIVE_R11_PENDING_SPECIFIC_ARCHITECT_ISSUANCE',authorization_id=A,audit_unused=True,
   model_requests=0,effects=0,issuance=False,activation=False,ownership='NONE',r10_immutable=True,
   context_identities={k:projection[k] for k in pub['context_identities']},
   validation_ids_created=False,phase_budget_seconds={'soft':30,'hard':120},diagnostics=records)
s.close()
out.write_text(canonical(results));print(canonical({'result':results['result'],'phases':records,'audit_unused':True}))
