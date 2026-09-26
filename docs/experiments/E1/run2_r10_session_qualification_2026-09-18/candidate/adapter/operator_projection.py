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
from .run_control import status
from .context_projection import sha

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
                    if before!=audit.read_bytes() or ledger_before!=_read(fd):continue
                finally:os.close(fd)
                if time.monotonic()-start>=max_seconds:return unknown('PROJECTION_DEADLINE')
                result=dict(live,schema='E1-RECONCILED-OPERATOR-STATUS-1',projection_generated=time.time(),
                  projection_seconds=time.monotonic()-start,handoff_eligible=False,
                  authority_basis={'audit_sha256':sha(before),'ledger_sha256':sha(ledger_before),
                      'lifecycle_event':lifecycle['last_event_id']},
                  live_telemetry_freshness=live.get('freshness'),freshness='FRESH')
                result['lifecycle_state']=result['authorization_state']=lifecycle['state']
                result['ownership']='OWNERSHIP_HELD' if owner else 'NONE'
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
                elif owner or scope:return unknown('INACTIVE_OWNERSHIP_CONFLICT')
                if lifecycle['state'] not in ('CANCELLED','COMPLETED','REVOKED') and live.get('freshness')!='FRESH':
                    result.update(freshness='UNKNOWN',current_subphase=None,outstanding_operation=None,
                        uncertainty='STALE_LIVE_ACTIVITY_SOURCE')
                return result
        return unknown('UNSTABLE_SNAPSHOT')
    except (OSError,ValueError,RuntimeError,KeyError) as exc:
        return unknown('EVIDENCE_UNAVAILABLE_OR_INVALID:'+type(exc).__name__)
