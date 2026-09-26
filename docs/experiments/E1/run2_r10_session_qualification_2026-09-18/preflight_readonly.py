import sys,json,time,signal
from pathlib import Path
sys.path.insert(0,'/tmp/forge-r9-context-69itwolf')
from adapter.context_projection import canonical,sha,derive
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.activation_transaction import ActivationTransaction
from adapter.attempt_context import readiness
from adapter.invocation_attempt import predecessor_no_effects
out=Path(__file__).parent; rows=[];result={}
def phase(name,fn):
 def expired(*_):raise TimeoutError('phase hard budget')
 signal.signal(signal.SIGALRM,expired);signal.setitimer(signal.ITIMER_REAL,120);t=time.monotonic();wall=time.time()
 try:return fn()
 finally:
  signal.setitimer(signal.ITIMER_REAL,0);elapsed=time.monotonic()-t
  rows.append(dict(name=name,seconds=elapsed,wall_start=wall,soft_exceeded=elapsed>=30,hard_exceeded=elapsed>=120))
  (out/'PRODUCTION_TIMING.json').write_text(canonical(rows))
pin=json.loads(Path('docs/experiments/E1/run2_r9_dispatch_2026-09-18/CURRENT_PIN.json').read_bytes());b=Path(pin['path']).read_bytes();assert sha(b)==pin['sha256'];pub=json.loads(b)
s=ControllerAuthorityStore(**pub['selected_store'])
try:
 with s.session():
  a=phase('cold_current_authority_bootstrap',lambda:reconstruct_authorization(s,s.applicability['authorization_id']))
  before=Path(pub['audit']).read_bytes();ledger=Path(a.ownership_ledger).read_bytes()
  def recovery():
   t=ActivationTransaction.recover(a,pub['audit'],pub['dispatch']['authority_id'])
   try:return dict(t.recovery)
   finally:t.close()
  result['terminal_recovery']=phase('independent_terminal_recovery',recovery)
  result['S3']=phase('fresh_supervisor_readiness',lambda:readiness(a,s,None,True,None))
  p=phase('current_projection_validation',lambda:derive(json.loads(a.context_projection),a.context_binding))
  result['identities']={k:p[k] for k in ('FullContextDigest','ModelPayloadDigest','ModelProjectionBindingDigest')}
  result['release_authority']=a.context_binding.governance.run5['release_authority']
  result['operational_ancestry']=a.context_binding.governance.identities
  try:predecessor_no_effects({'predecessor':{'audit':pub['audit'],'audit_sha256':sha(before),'authorization_id':a.authorization_id}})
  except ValueError as e:result['r9_as_next_predecessor']={'result':'REJECTED_BY_CURRENT_IMPLEMENTATION','reason':str(e)}
  else:raise AssertionError('unexpected predecessor acceptance')
  assert before==Path(pub['audit']).read_bytes() and ledger==Path(a.ownership_ledger).read_bytes()
  result.update(historical_state_unchanged=True,real_model_requests=0,effects=0,r10_production_validation='BLOCKED_NO_AUTHENTICATED_R10_CONTEXT')
except Exception as e:result['error']={'type':type(e).__name__,'message':str(e)}
finally:s.close();(out/'PRODUCTION_PREFLIGHT.json').write_text(canonical(result));print(canonical(result))
