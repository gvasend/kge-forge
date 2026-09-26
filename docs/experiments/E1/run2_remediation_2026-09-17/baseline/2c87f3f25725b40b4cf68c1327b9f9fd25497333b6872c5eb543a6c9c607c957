"""Fail-closed controller reconstruction from fsynced audit and live cgroup state."""
from pathlib import Path
import hashlib, json

CGROUP_BASE=Path('/sys/fs/cgroup/unified/kge-forge/executor')
SUPERVISOR_AUDIT=Path('/tmp/a21m.sock.supervisor-audit.jsonl')

class RecoveryDenied(RuntimeError): pass

def _events(path):
    try: return [json.loads(line) for line in Path(path).read_text().splitlines()]
    except (OSError,ValueError,TypeError) as exc:
        raise RecoveryDenied('durable audit unavailable or corrupt') from exc

def _observe(path):
    if path.is_symlink() or not path.is_dir():
        raise RecoveryDenied('scope cgroup unavailable or substituted')
    directories=[path]; members=set()
    for directory in directories:
        if len(directories)>128 or directory.is_symlink():
            raise RecoveryDenied('scope subtree exceeds observation bound')
        try:
            for child in sorted(directory.iterdir()):
                if child.is_symlink(): raise RecoveryDenied('scope subtree substituted')
                if child.is_dir(): directories.append(child)
            members.update(int(pid) for pid in (directory/'cgroup.procs').read_text().split())
        except (OSError,ValueError) as exc:
            raise RecoveryDenied('scope membership unavailable') from exc
        if len(members)>4096 or any(pid<=0 for pid in members):
            raise RecoveryDenied('scope membership invalid or unbounded')
    try: population=dict(line.split() for line in (path/'cgroup.events').read_text().splitlines())['populated']
    except (OSError,ValueError,KeyError) as exc:
        raise RecoveryDenied('scope population unavailable') from exc
    if population not in ('0','1') or (population=='0' and members):
        raise RecoveryDenied('scope membership/population contradictory')
    return {'members':sorted(members),'populated':int(population),'directories':len(directories)}

def reconstruct(controller_audit, authorization, supervisor_audit=SUPERVISOR_AUDIT,
                cgroup_base=CGROUP_BASE):
    """Return a snapshot; no old terminal result or quiescence is trusted alone."""
    path=Path(controller_audit)
    from .authorization_lifecycle import requires_lifecycle, reconstruct as lifecycle_reconstruct, LifecycleDenied
    lifecycle_required = requires_lifecycle(authorization)
    if not path.exists():
        if lifecycle_required and authorization.state == 'ACTIVE':
            raise RecoveryDenied('ACTIVE lacks original INACTIVE and durable activation history')
        return None
    events=_events(path)
    lifecycle = None
    if lifecycle_required:
        try: lifecycle = lifecycle_reconstruct(path.read_bytes(), authorization, path)
        except (LifecycleDenied, ValueError, KeyError, OSError) as exc:
            raise RecoveryDenied('authorization lifecycle denied: ' + str(exc)) from exc
    issued=[event['authorization'] for event in events
            if event.get('event')=='authorization_issued']
    if not issued: raise RecoveryDenied('authorization issuance missing')
    expected={**authorization.__dict__}
    if authorization.context_binding is not None:
        binding=authorization.context_binding
        expected['context_binding']={'context_sha256':binding.digest,
            'capture_commit':binding.capture_commit,
            'baseline_id':binding.manifest.get('baseline_id'),
            'work_id':binding.manifest.get('work_id')}
    expected=json.loads(json.dumps(expected,sort_keys=True))
    for old in issued:
        # Earlier issued authorizations predate the optional continuation field.
        # Empty means no supplement; a nonempty new binding still cannot replace it.
        old = dict(old)
        old.setdefault('operational_binding', '')
        if lifecycle is None and old!=expected:
            raise RecoveryDenied('effective authorization changed across restart')
    requests={}; results={}; scopes={}; interruption=False
    for event in events:
        name=event.get('event'); rid=event.get('action_request_id')
        if name=='action_request':
            if rid in requests or any(event.get(key)!=getattr(authorization,key)
                    for key in ('session_id','turn_id','authorization_id')) or \
                    event.get('authorization_revision')!=authorization.revision:
                raise RecoveryDenied('action request identity contradictory')
            requests[rid]=event
        elif name=='action_result':
            if rid not in requests or rid in results: raise RecoveryDenied('action result contradictory')
            payload=event.get('payload')
            if payload is not None and hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()!=event.get('digest'):
                raise RecoveryDenied('action result digest mismatch')
            results[rid]=payload if payload is not None else {
                'action_request_id':rid,'result':'INDETERMINATE',
                'error':'old terminal payload absent from durable audit'}
        elif name=='interruption_requested': interruption=True
        elif name in ('execution_snapshot_created','execution_scope_reserved',
                      'execution_scope_created','execution_scope_closed',
                      'execution_scope_quiescent','recovery_scope_quiescent',
                      'execution_scope_indeterminate','recovery_scope_indeterminate'):
            sid=event.get('execution_scope_id')
            if not isinstance(sid,str) or not sid.startswith('scope-'):
                raise RecoveryDenied('scope identity missing')
            scope=scopes.setdefault(sid,{'events':set(),'action_request_id':rid})
            if rid and scope['action_request_id'] not in (None,rid):
                raise RecoveryDenied('scope action substitution')
            scope['action_request_id']=rid or scope['action_request_id']
            scope['events'].add(name)
            if name=='execution_snapshot_created':
                scope['workspace_root']=event.get('workspace_root')
                scope['source_root']=event.get('source_root')
    incomplete=[]
    for rid,request in requests.items():
        if rid not in results:
            incomplete.append(rid)
            results[rid]={'action_request_id':rid,'result':'INDETERMINATE',
                          'type':request['type'],'error':'controller interrupted before terminal result'}
    if len(scopes)>1:
        # A turn may have sequential scopes; only the latest can be active.
        ordered=[event['execution_scope_id'] for event in events
                 if event.get('event')=='execution_scope_reserved']
        if len(ordered)!=len(set(ordered)) or set(ordered)!=set(scopes):
            raise RecoveryDenied('scope reservation chain contradictory')
        for sid in ordered[:-1]:
            if 'execution_scope_quiescent' not in scopes[sid]['events']:
                raise RecoveryDenied('prior sequential scope lacks terminal quiescence')
        latest=ordered[-1]
    else: latest=next(iter(scopes),None)
    current=None; category='COMPLETED'
    if latest:
        scope=scopes[latest]
        if not all(name in scope['events'] for name in
                   ('execution_scope_reserved','execution_snapshot_created','execution_scope_created')):
            category='UNCERTAIN'; current={'scope_id':latest,'eligible_for_reconcile':False}
        else:
            owners={}
            for event in _events(supervisor_audit):
                if event.get('event')=='scope_created':
                    sid=event.get('scope_id'); owner=event.get('owner')
                    if sid in owners or not isinstance(owner,list) or len(owner)!=3:
                        raise RecoveryDenied('supervisor owner audit contradictory')
                    owners[sid]=tuple(owner)
            owner=(authorization.session_id,authorization.authorization_id,
                   scope['action_request_id'])
            if owners.get(latest)!=owner:
                category='UNCERTAIN'; current={'scope_id':latest,'eligible_for_reconcile':False}
            else:
                try: observation=_observe(Path(cgroup_base)/latest)
                except RecoveryDenied:
                    category='UNCERTAIN'; current={'scope_id':latest,'eligible_for_reconcile':False}
                else:
                    terminal=('execution_scope_quiescent' in scope['events'] or
                              'recovery_scope_quiescent' in scope['events'])
                    supervisor_closed=any(event.get('event')=='scope_closed' and
                        event.get('scope_id')==latest and event.get('owner')==list(owner)
                        for event in _events(supervisor_audit))
                    if terminal and supervisor_closed and \
                            observation['members']==[] and observation['populated']==0:
                        category='INTERRUPTED' if interruption else 'COMPLETED'
                        state='QUIESCENT'
                    elif observation['populated']==1 or observation['members']:
                        category='ACTIVE'; state='INDETERMINATE'
                    else:
                        category='UNCERTAIN'; state='INDETERMINATE'
                    current={'scope_id':latest,'action_request_id':scope['action_request_id'],
                        'workspace_root':scope['workspace_root'],'source_root':scope['source_root'],
                        'observation':observation,'state':state,
                        'eligible_for_reconcile':category in ('ACTIVE','UNCERTAIN')}
    if any(result['result']=='INDETERMINATE' for result in results.values()) and category=='COMPLETED':
        category='UNCERTAIN'
    return {'category':category,'interruption_requested':interruption,
            'requests':requests,'results':results,'incomplete':incomplete,
            'scope':current,'authorization_lifecycle':lifecycle}
