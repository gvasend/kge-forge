"""Exact prospective Run-2 context plus live kernel readiness predicates; no issuance."""
import json,time,os,fcntl
from pathlib import Path
from adapter.context_projection import sha,canonical
from adapter.authority_bootstrap import reconstruct_authorization
from adapter.controller_authority_store import ControllerAuthorityStore
from adapter.activation_transaction import validate_non_host,_host
from adapter.supervisor_succession import legacy_tuple
from adapter.run2_context import supervisor_prefix
from adapter.run_control import RunControl,E1_POLICY
from adapter.validation_spans import recording,span
O=Path(__file__).resolve().parent;F=O.parent/'run2_nonhost_closure_2026-09-17'
r=json.loads((F/'PROBE_RESULT.json').read_bytes());obs=json.loads((O/'POST_CLOSURE_OBSERVATIONS.json').read_bytes());p=obs['process']
expected={'process':p,'executable':{'path':obs['checks']['executable']['path'],'sha256':obs['checks']['executable']['sha256'],'argv':' '.join(obs['checks']['argv']['observed'])},'workspace':obs['checks']['workspace']['observed'],'cgroup':{'memberships':obs['checks']['cgroup']['memberships'].strip()}}
timing=Path('/tmp/kge-forge-s3-host-verification/production-timing.jsonl');assert not timing.exists()
control=RunControl(timing,{'authorization_id':'NON_EFFECTING_HOST_QUALIFICATION','session_id':'S3-post-closure','invocation_id':'S3-readiness-inspection','work_package_id':'E1-WP-001','OperationalContextId':r['operational_identities']['OperationalContextId']},E1_POLICY)
result={'mode':'NON_EFFECTING_PROSPECTIVE_CONTEXT_WITH_LIVE_CANDIDATE','model_requests':0,'ownership_acquired':False,'samples':[]}
try:
 with recording(control):
  begin=time.monotonic()
  with span('private_bootstrap'):
   store=ControllerAuthorityStore(**r['selected_store'])
   with store.session():auth=reconstruct_authorization(store,store.applicability['authorization_id'])
  result['bootstrap_seconds']=time.monotonic()-begin
  with store.session():
   selection=json.loads(store.resolve(auth.authorization_id+':run2-context'))
   prefix=supervisor_prefix(store);result['predecessor']={'instance':prefix['instance'],'head':prefix['head']}
   raw=json.loads(store.resolve(auth.authorization_id));ledger=os.open(auth.ownership_ledger,os.O_RDONLY)
   try:
    fcntl.flock(ledger,fcntl.LOCK_SH|fcntl.LOCK_NB)
    for label in ('cold','warm'):
     begin=time.monotonic()
     with span('validation'):
      proof=validate_non_host(auth,store.state_path(auth.authorization_id+':audit'),selection['dispatch_decision'],ledger)
      with span('validation'):host=_host(legacy_tuple(expected),check_scopes=True)
     result['samples'].append({'label':label,'seconds':time.monotonic()-begin,'nonhost_result':proof['result'],'live_kernel_readiness':'PASS','host':host})
   finally:os.close(ledger)
   result['context_identities']=proof['context_identities'];assert result['context_identities']==r['context_identities']
   result['current_authority_readiness']='NOT_ESTABLISHED: release and specific succession remain unissued/unapplied'
  store.close()
 result['result']='PASS_NON_EFFECTING_CONTEXT_AND_LIVE_KERNEL_PREDICATES'
except Exception as e:
 result.update(result='BLOCKED',error=type(e).__name__+': '+str(e));raise
finally:
 (O/'PRODUCTION_TIMING_RESULT.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 (O/'PRODUCTION_TIMING.jsonl').write_bytes(timing.read_bytes())
 print(json.dumps(result,sort_keys=True))
