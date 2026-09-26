"""Versioned trusted interpretation of historical control telemetry.

Called only after pinned audit bytes, hash ordering, original implementation and
independent terminal recovery are authenticated. No record-supplied class is
accepted. This module observes; it cannot issue, reserve, dispatch or mutate.
Registry extensions require qualified implementation/schema authentication.
"""
import math
import json
from .context_projection import digest
from .run_control import E1_POLICY

OBSERVATION='NON_EFFECTING_OBSERVATION'
OPERATIONS={
 'context_reconstruction':'authority_bootstrap.reconstruct_authorization',
 'validation':'activation_transaction._validate_production',
 'model_projection':'context_projection.derive',
 'activation_recovery':'activation_transaction.ActivationTransaction.recover',
 'private_bootstrap':'authority_bootstrap.reconstruct_authorization',
 'host_construction':'controlled_dispatch.dispatch',
 'reasoning_construction':'controlled_dispatch.dispatch',
 'attempt_history_ancestry':'attempt_chain.ancestry',
 'attempt_history_decision':'attempt_chain.decision',
 'attempt_history_historical_capture':'attempt_chain.historical_capture',
}
EVENTS={k:OBSERVATION for k in ('invocation_start','span_start','span_end','activity',
 'budget_warning','budget_exhausted','warning_persisted','governance_observation')}
EVENTS.update(admission_closed='ADMISSION_RESTRICTION',final_disposition='TERMINAL_OBSERVATION')
NEGATIVE={
 'model_request_start':'MODEL_HANDOFF','model_request_started':'MODEL_HANDOFF',
 'model_request_sent':'MODEL_HANDOFF','provider_request_accepted':'MODEL_HANDOFF',
 'response_received':'MODEL_HANDOFF','model_content_binding':'MODEL_HANDOFF',
 'action_request':'ACTION_REQUEST','action_result':'PERSISTENT_EFFECT',
 'execution_scope_created':'EXECUTION_EFFECT','repository_effect':'PERSISTENT_EFFECT',
 'knowledge_effect':'PERSISTENT_EFFECT','implementation_effect':'PERSISTENT_EFFECT',
 'uncertainty':'UNCERTAINTY','ownership_acquired':'OWNERSHIP_STATE',
}
REGISTRY={'schema':'TRUSTED-EVIDENCE-SEMANTICS-1','version':1,
 'record_schema':'E1-RUN-CONTROL-1','events':EVENTS,'operations':OPERATIONS,
 'legacy_observations':{'context_projection_verified':{'class':OBSERVATION,'producer':'context_projection.ContextProjection.verify'}},
 'explicit_negative':NEGATIVE,'unknown':'REJECT',
 'classification_source':'qualified implementation, never record-supplied labels',
 'observation_authority':'NONE','historical_records':'UNCHANGED',
 'eligibility':'independent lifecycle/ownership/execution/handoff/effects/uncertainty checks required'}
REGISTRY_ID='EVIDENCE-SEMANTICS-sha256:'+digest(REGISTRY)
ENVELOPE={'schema','event','identity','cycle','monotonic','wall_time','boot_id',
 'sequence','previous','audit_prefix_sha256','policy_sha256','details','record_sha256'}
def require(ok,message):
 if not ok:raise ValueError(message)
def number(x):return type(x) in (float,int) and math.isfinite(x) and x>=0
def fields(d,keys):require(set(d)==set(keys.split()),'malformed observation fields')
def operation(x):require(x in OPERATIONS,'unclassified controller operation')
def classify_record(row,expected_identity):
 """Return trusted class; never use this return value as lifecycle authority."""
 e=row.get('event')
 if e in NEGATIVE:raise ValueError('disallowed predecessor evidence: '+NEGATIVE[e])
 require(row.get('schema')=='E1-RUN-CONTROL-1','unclassified telemetry schema')
 require(set(row)==ENVELOPE,'unclassified telemetry envelope')
 require(row['identity']==expected_identity and type(row['cycle']) is int and row['cycle']==0,'handoff or identity mismatch')
 require(row['policy_sha256']==digest(E1_POLICY),'budget policy substitution')
 require(number(row['monotonic']) and number(row['wall_time']) and type(row['sequence']) is int and row['sequence']>0,'invalid observation timing')
 require(type(row['boot_id']) is str and bool(row['boot_id']),'missing birth correlation')
 require(e in EVENTS and type(row['details']) is dict,'unknown telemetry event')
 d=row['details']
 if e=='invocation_start':fields(d,'')
 elif e=='span_start':fields(d,'name');operation(d['name'])
 elif e=='span_end':
  fields(d,'name admission_closed');operation(d['name']);require(type(d['admission_closed']) is bool,'invalid admission observation')
 elif e=='activity':fields(d,'operation');operation(d['operation'])
 elif e in ('budget_warning','budget_exhausted'):
  base='budget value operation last_progress'
  extended=' lock_wait_seconds warning_created_monotonic warning_created_wall'
  fields(d,base+extended if e=='budget_warning' and 'lock_wait_seconds' in d else base)
  require(d['budget'] in E1_POLICY['seconds'] or d['budget'] in ('requests','tokens'),'unknown budget')
  operation(d['operation'])
  require(all(number(v) for k,v in d.items() if k not in ('budget','operation')),'invalid budget value')
 elif e=='warning_persisted':
  fields(d,'append_and_fsync_seconds created_monotonic created_wall creation_to_persistence_seconds durable_monotonic durable_wall lock_wait_seconds warning_record_sha256 warning_sequence')
  require(all(number(v) for k,v in d.items() if k!='warning_record_sha256'),'invalid persistence timing')
  require(type(d['warning_record_sha256']) is str and len(d['warning_record_sha256'])==64,'unbound warning')
 elif e=='governance_observation':
  fields(d,'authorization ownership supervisor')
  require(d['authorization'] in ('INACTIVE','ACTIVATING','ACTIVE','CANCELLED') and d['ownership'] in ('NONE','HELD','OWNERSHIP_HELD','RELEASED') and d['supervisor'] in ('READY','UNKNOWN'),'unknown governance observation')
 elif e=='admission_closed':
  fields(d,'reason');require(type(d['reason']) is str and bool(d['reason']),'missing closure reason')
 elif e=='final_disposition':
  require(set(d) in ({'disposition','ownership','reason','uncertainty'},{'disposition','ownership','provider_uncertainty','terminal_event_id','uncertainty'}),'unknown terminal observation')
  require(d['disposition']=='CANCELLED' and d['ownership']=='RELEASED' and d.get('uncertainty') is None and d.get('provider_uncertainty') is None,'uncertain terminal observation')
 return EVENTS[e]

def qualified_prefix(rows,authorization_id):
 """Remove observations only from an in-memory eligibility view, never history.
 Authority/admission facts are retained for the original independent predicate.
 """
 require(bool(rows) and rows[0].get('event')=='authorization_issued','missing original issuance')
 a=rows[0]['authorization']
 expected={'authorization_id':authorization_id,'session_id':a['session_id'],
  'invocation_id':a['turn_id'],'work_package_id':'E1-WP-001'}
 out=[]
 for row in rows:
  if row.get('schema')=='E1-RUN-CONTROL-1':
   category=classify_record(row,expected)
   if category==OBSERVATION:continue
  elif row.get('event')=='context_projection_verified':
   keys={'AuthoritativeContextId','FullContextDigest','ModelPayloadDigest','ModelProjectionBindingDigest','ModelProjectionDigest'}
   require(set(row)==keys|{'authorization_id','session_id','turn_id','event','time'},'malformed projection verification')
   require(all(row[k]==a[k] for k in ('authorization_id','session_id','turn_id')),'projection attribution mismatch')
   op=json.loads(a['operational_binding'])
   require(all(row[k]==op['context_identities'][k] for k in keys),'projection identity substitution')
   require(number(row['time']),'invalid projection observation time')
   continue
  else:
   require(row.get('event') not in NEGATIVE,'effecting/uncertain predecessor fact')
   require(not any(k in row for k in ('evidence_class','classification')),'caller evidence classification')
  out.append(row)
 return out
