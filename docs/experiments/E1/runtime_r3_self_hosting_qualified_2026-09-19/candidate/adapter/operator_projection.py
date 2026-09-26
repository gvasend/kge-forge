"""Read-only reconciled operator status. Lifecycle/ledger dominate telemetry.

No saved PASS is trusted. Terminal history is freshly reconstructed even when
its last live heartbeat is old. Unreadable/changing evidence yields UNKNOWN.
"""
import os,time
from pathlib import Path
from .controller_authority_store import current,AuthorityDenied
from .authority_bootstrap import reconstruct_authorization
from .authorization_lifecycle import reconstruct
from .recovery_ledger import reconstruct as recover_actions
from .activation_transaction import invocation,_read
from .invocation_ownership import InvocationOwnership
from .run_control import status, decode_events
from .evidence_semantics import classify_record, OBSERVATION
from .context_projection import sha
from .attempt_ownership import attribute,lifecycle_ownership

def live_observation(row, identity):
    """UI-only interpretation; never used by predecessor/admission validation.

    Cycle attribution remains intact in durable evidence. Pure verification
    spans in any nonnegative cycle do not change lifecycle/ownership authority.
    Hash/order is verified on the original bytes before this schema-only view.
    """
    if type(row.get('cycle')) is not int or row['cycle']<0:return False
    view=dict(row,cycle=0)
    if row.get('event') in ('span_start','span_end'):
        details=dict(row.get('details',{}))
        if details.get('name') in ('supervisor_authority_dependencies','supervisor_live_identity_readiness','continuation_construction'):
            details['name']='validation'
            view['details']=details
    return classify_record(view,identity)==OBSERVATION

def observational_extension(before, after, auth):
    """Accept only byte-identical prefix plus authenticated harmless observation.

    Live admission restrictions always require a new snapshot, even though they
    may coexist with an eligible terminal predecessor under the separate policy.
    Unknown records, state transitions and effects always force a fresh snapshot.
    """
    if before == after:return True
    if not after.startswith(before) or (before and not before.endswith(b'\n')):return False
    rows=decode_events(after)
    count=len(before.splitlines())
    identity={'authorization_id':auth.authorization_id,'session_id':auth.session_id,
              'invocation_id':auth.turn_id,'work_package_id':auth.work_package_id}
    try:
        for row in rows[count:]:
            if row.get('event') in ('budget_exhausted','admission_closed','final_disposition'):return False
            if row.get('event')=='context_projection_verified':
                # Existing qualified legacy schema: only a content-identity
                # observation, never provider/model handoff or lifecycle state.
                from .evidence_semantics import number
                import json
                keys={'AuthoritativeContextId','FullContextDigest','ModelPayloadDigest','ModelProjectionBindingDigest','ModelProjectionDigest'}
                if set(row)!=keys|{'authorization_id','session_id','turn_id','event','time'}:return False
                if any(row[k]!=getattr(auth,k) for k in ('authorization_id','session_id','turn_id')):return False
                expected=json.loads(auth.operational_binding)['context_identities']
                if not number(row['time']) or any(row[k]!=expected[k] for k in keys):return False
            elif not live_observation(row,identity):return False
    except (ValueError,KeyError,TypeError):return False
    return True

def project(store,authorization_id,max_seconds=30,snapshot_attempts=3):
    start=time.monotonic()
    def unknown(reason):
        return {'schema':'E1-RECONCILED-OPERATOR-STATUS-1','authorization_id':authorization_id,
          'projection_generated':time.time(),'freshness':'UNKNOWN','lifecycle_state':'UNKNOWN',
          'ownership':'UNKNOWN','uncertainty':reason,'handoff_eligible':False,
          'projection_seconds':time.monotonic()-start}
    if current() is not None:raise AuthorityDenied('operator projection owns one authority session')
    try:
        with store.session():
            auth=reconstruct_authorization(store,authorization_id)
            planned=Path(store.catalog['private_state'][authorization_id+':audit']['path'])
            if not os.path.lexists(planned):
                # A freshly observed absent source is useful status, not proof
                # that an authorization was never issued or may be reissued.
                from .attempt_ownership import observe
                owner,scope,data=observe(auth.ownership_ledger)
                store._verify_catalog()
                if not os.path.lexists(planned):
                    if time.monotonic()-start>=max_seconds:return unknown('PROJECTION_DEADLINE')
                    return {'schema':'E1-RECONCILED-OPERATOR-STATUS-1','authorization_id':authorization_id,
                      'projection_generated':time.time(),'projection_seconds':time.monotonic()-start,
                      'freshness':'FRESH','lifecycle_state':'NOT_ESTABLISHED',
                      'operational_state':'AWAITING_LIFECYCLE_EVIDENCE','audit_namespace':'ABSENT',
                      'ownership':'NONE' if owner is None and scope is None else 'RECONCILIATION_REQUIRED',
                      'handoff_eligible':False,'uncertainty':'NO_AUTHORITATIVE_LIFECYCLE_EVIDENCE',
                      'authority_basis':{'catalog_sha256':store.catalog_sha256,'ledger_sha256':sha(data)},
                      'supervisor_readiness':'UNKNOWN','budget_state':'UNKNOWN',
                      'model_requests':None,'responses':None,'action_requests':None,'action_results':None,
                      'last_event_age':None,'last_substantive_progress':None}
            audit=store.state_path(authorization_id+':audit');ledger=store.state_path(authorization_id+':ownership')
            for _ in range(snapshot_attempts):
                if time.monotonic()-start>=max_seconds:return unknown('PROJECTION_DEADLINE')
                before=audit.read_bytes();fd=os.open(ledger,os.O_RDONLY|os.O_NOFOLLOW)
                try:
                    ledger_before=_read(fd);identity=os.fstat(fd);path_identity=os.stat(ledger,follow_symlinks=False)
                    if (identity.st_dev,identity.st_ino)!=(path_identity.st_dev,path_identity.st_ino):return unknown('LEDGER_REPLACED')
                    lifecycle=reconstruct(before,auth,audit)
                    actions=recover_actions(audit,auth)
                    owner=invocation(fd);scope=InvocationOwnership.__new__(InvocationOwnership)._history(fd)
                    live=status(audit)
                    after=audit.read_bytes()
                    if not observational_extension(before,after,auth) or ledger_before!=_read(fd):continue
                finally:os.close(fd)
                if time.monotonic()-start>=max_seconds:return unknown('PROJECTION_DEADLINE')
                attribute(owner,scope,[],{'authorization_id':auth.authorization_id,'session_id':auth.session_id},audit)
                ownership_state=lifecycle_ownership(lifecycle,owner,scope)
                result=dict(live,schema='E1-RECONCILED-OPERATOR-STATUS-1',projection_generated=time.time(),
                  projection_seconds=time.monotonic()-start,handoff_eligible=False,
                  authority_basis={'audit_sha256':sha(before),'ledger_sha256':sha(ledger_before),
                      'lifecycle_event':lifecycle['last_event_id'],
                      'observed_audit_sha256':sha(after),
                      'observation_only_extension':before!=after},
                  live_telemetry_freshness=live.get('freshness'),freshness='FRESH')
                result['state']=result['lifecycle_state']=result['authorization_state']=lifecycle['state']
                if 'reason' in result:result['activity_reason']=result.pop('reason')
                result['ownership']=ownership_state
                result['authority_freshness']='FRESH'
                result['activity_freshness']=live.get('freshness','UNKNOWN')
                result['operational_state']='ACTIVATING' if lifecycle['phase'] in ('DISPATCH_AUTHORIZED','ACTIVATION_INDETERMINATE') else lifecycle['state']
                result['uncertainty']='LIFECYCLE_RECONCILIATION_REQUIRED' if lifecycle['uncertain'] else None
                if lifecycle['state'] in ('CANCELLED','COMPLETED','REVOKED'):
                    if owner or scope or actions['incomplete'] or (actions['scope'] and actions['scope']['state']!='QUIESCENT'):
                        return unknown('TERMINAL_RECONCILIATION_INCOMPLETE')
                    result.update(ownership='RELEASED',architectural_state='QUIESCENT',current_subphase=None,
                       outstanding_operation=None,uncertainty=None,terminal_disposition={
                       'disposition':lifecycle['state'],'ownership':'RELEASED','uncertainty':None,
                       'source':'AUTHORITATIVE_LIFECYCLE_AND_RECOVERY'})
                elif lifecycle['state']=='ACTIVE':
                    if owner!=lifecycle['activation_event']['ownership_reservation']:
                        return unknown('ACTIVE_OWNERSHIP_CONFLICT')
                    if live.get('terminal_disposition'):
                        result['terminal_disposition']=None
                        result['uncertainty']='PROVISIONAL_TERMINAL_NOT_RECONCILED'
                elif (owner or scope) and lifecycle['phase']!='ACTIVATION_INDETERMINATE':return unknown('INACTIVE_OWNERSHIP_CONFLICT')
                if lifecycle['state'] not in ('CANCELLED','COMPLETED','REVOKED') and live.get('freshness')!='FRESH':
                    result.update(activity_freshness='UNKNOWN',current_subphase='UNKNOWN',outstanding_operation='UNKNOWN',
                        activity_uncertainty='STALE_OR_ABSENT_LIVE_ACTIVITY_SOURCE')
                elif lifecycle['state']=='ACTIVE' and (live.get('cycle',0)>0 or live.get('current_subphase') in ('host_construction','reasoning_construction','model_cycle','model_request','transport')):
                    result['operational_state']='DISPATCHING'
                return result
        return unknown('UNSTABLE_SNAPSHOT')
    except (OSError,ValueError,RuntimeError,KeyError) as exc:
        return unknown('EVIDENCE_UNAVAILABLE_OR_INVALID:'+type(exc).__name__)
