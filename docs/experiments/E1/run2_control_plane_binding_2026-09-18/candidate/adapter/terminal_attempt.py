"""Strict evidence predicate for terminal, pre-model replacement eligibility.

Called only with independently reconstructed lifecycle/actions and checked audit
history. A positive result is eligibility, never issuance or retry authority.
Unknown event types fail closed; no inference about unobserved provider activity.
"""
from .run_control import events
from .context_projection import sha
SAFE_CONTROL={'invocation_start','span_start','span_end','activity','budget_warning','warning_persisted',
 'governance_observation','admission_closed','final_disposition'}
SAFE_FACTS={'authorization_issued','production_dispatch_validated',
 'authorization_lifecycle_dispatch_authorized','authorization_lifecycle_activation_intent',
 'authorization_lifecycle_activated','authorization_lifecycle_terminal',
 'controller_reconstructed','interruption_requested','architectural_state'}
def classify(rows,lifecycle,actions,ownership,scope,authorization_id):
 if ownership is not None or scope is not None:raise ValueError('owned or non-quiescent predecessor')
 if actions.get('scope') is not None or actions.get('incomplete') or actions.get('results'):
  raise ValueError('effecting or unreconciled predecessor actions')
 if lifecycle.get('uncertain') or lifecycle.get('state')!='CANCELLED':
  raise ValueError('terminal CANCELLED predecessor required')
 if not rows or rows[0].get('event')!='authorization_issued' or rows[0]['authorization'].get('state')!='INACTIVE':
  raise ValueError('valid initial INACTIVE issuance required')
 if rows[0]['authorization'].get('authorization_id')!=authorization_id:raise ValueError('predecessor identity substituted')
 closed=False;active=False
 for row in rows:
  e=row.get('event')
  if row.get('schema')=='E1-RUN-CONTROL-1':
   if e not in SAFE_CONTROL or row['identity']['authorization_id']!=authorization_id or row['cycle']!=0:
    raise ValueError('model/provider/action activity or unknown telemetry')
   if e=='activity' and row.get('details',{}).get('operation') not in {
    'context_reconstruction','validation','activation_recovery','private_bootstrap','host_construction','reasoning_construction'}:
    raise ValueError('unqualified predecessor activity')
   if e in ('span_start','span_end') and row.get('details',{}).get('name') not in {
    'context_reconstruction','validation','model_projection','activation_recovery','private_bootstrap','host_construction','reasoning_construction'}:
    raise ValueError('unqualified predecessor span')
   closed|=e=='admission_closed'
  elif e not in SAFE_FACTS:raise ValueError('unknown or effecting predecessor fact')
  if e=='authorization_lifecycle_activated':active=True
  if e in ('controller_reconstructed','architectural_state','interruption_requested'):
   if row.get('scope') not in (None,'NONE') or row.get('scope_id') is not None:raise ValueError('surviving or historical execution scope')
   if e=='architectural_state' and row.get('state')!='QUIESCENT':raise ValueError('non-quiescent predecessor')
 if not closed:raise ValueError('predecessor admission not durably closed')
 if rows[-1].get('event')!='authorization_lifecycle_terminal' or rows[-1].get('resulting_state')!='CANCELLED':
  raise ValueError('authoritative terminal fact must close predecessor')
 return 'ACTIVE_CANCELLED_PRE_MODEL_NO_EFFECTS' if active else 'ISSUED_INACTIVE_CANCELLED_NO_EFFECTS'
