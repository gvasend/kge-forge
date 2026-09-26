"""Host-side cgroup-v2 execution-scope supervisor.

The supervisor owns only the delegated executor subtree and fails closed when
the subtree is unavailable or mounted read-only.
"""
from pathlib import Path
import json, os, re, threading, time, uuid
from .termination import TerminationEngine, PidfdSignaler

class SupervisorError(RuntimeError): pass
SCOPE_ID=re.compile(r'^scope-[0-9a-f]{32}$')
RECOVERY_ID=re.compile(r'^recovery-[0-9a-f]{32}$')

class HostScopeSupervisor:
    def __init__(self, base='/sys/fs/cgroup/unified/kge-forge/executor',
                 audit_path=None, signaler=None, termination_seconds=5,
                 grace_seconds=.5, poll_seconds=.05):
        self.base=Path(base).resolve(); self._scopes={}; self._lock=threading.RLock()
        self.audit_path=Path(audit_path).resolve() if audit_path else None
        if self.audit_path is not None and (self.audit_path==self.base or
                self.base in self.audit_path.parents):
            raise SupervisorError('supervisor evidence inside delegated subtree')
        self.termination=TerminationEngine(self,signaler or PidfdSignaler(),
            termination_seconds,grace_seconds,poll_seconds)
        if not self.base.is_dir(): raise SupervisorError('delegated cgroup subtree unavailable')
        if not (self.base/'cgroup.procs').exists(): raise SupervisorError('not a cgroup v2 subtree')
        if self.audit_path is not None: self._restore()
    def _audit(self,event):
        if self.audit_path is None: return
        self.audit_path.parent.mkdir(parents=True,exist_ok=True)
        fd=os.open(self.audit_path,os.O_WRONLY|os.O_APPEND|os.O_CREAT|os.O_NOFOLLOW,0o600)
        with os.fdopen(fd,'w') as stream:
            stream.write(json.dumps({'time_ns':time.monotonic_ns(),**event},sort_keys=True)+'\n')
            stream.flush(); os.fsync(stream.fileno())
    def _restore(self):
        if not self.audit_path.exists(): return
        try: lines=self.audit_path.read_text().splitlines()
        except OSError as exc: raise SupervisorError('supervisor audit unavailable') from exc
        for line in lines:
            try: event=json.loads(line)
            except ValueError as exc: raise SupervisorError('supervisor audit corrupt') from exc
            sid=event.get('scope_id')
            if event.get('event')=='scope_created':
                owner=event.get('owner')
                if not isinstance(sid,str) or not SCOPE_ID.fullmatch(sid) or \
                        not isinstance(owner,list) or \
                        len(owner)!=3 or not all(isinstance(item,str) and item for item in owner) or \
                        sid in self._scopes:
                    raise SupervisorError('supervisor owner audit corrupt')
                self._scopes[sid]={'path':self.base/sid,'state':'INDETERMINATE',
                    'owner':tuple(owner),'recovery_ids':set()}
            elif event.get('event')=='recovery_authorized':
                scope=self._scopes.get(sid)
                rid=event.get('recovery_request_id')
                if scope is None or not isinstance(rid,str) or \
                        not RECOVERY_ID.fullmatch(rid):
                    raise SupervisorError('supervisor recovery audit corrupt')
                if event.get('owner')!=list(scope['owner']) or \
                        event['recovery_request_id'] in scope['recovery_ids']:
                    raise SupervisorError('supervisor recovery audit contradictory')
                scope['recovery_ids'].add(event['recovery_request_id'])
        # Adoption never infers quiescence from an old audit entry; admission
        # stays closed until a new authoritative reconciliation.
    def create(self, execution_scope_id=None, owner=None):
        with self._lock:
            sid=execution_scope_id or 'scope-'+uuid.uuid4().hex
            if sid in self._scopes: raise SupervisorError('scope already exists')
            if owner is not None and (not isinstance(sid,str) or
                not SCOPE_ID.fullmatch(sid) or
                not isinstance(owner,tuple) or len(owner)!=3 or
                not all(isinstance(item,str) and item for item in owner)):
                raise SupervisorError('owned execution identity invalid')
            path=self.base/sid
            if not isinstance(sid,str) or not sid or sid in ('.','..') or \
                    path.parent!=self.base or path.resolve()!=path or path.is_symlink():
                raise SupervisorError('scope path substitution')
            try: path.mkdir()
            except OSError as e: raise SupervisorError('scope creation unavailable') from e
            self._scopes[sid]={'path':path,'state':'CREATED','owner':owner,'recovery_ids':set()}
            if owner is not None:
                self._audit({'event':'scope_created','scope_id':sid,'owner':list(owner)})
            return sid
    def authorize(self,sid,owner):
        scope=self._scopes.get(sid)
        if not scope or scope['owner'] is None or scope['owner']!=owner or \
                not SCOPE_ID.fullmatch(sid) or scope['path']!=self.base/sid or \
                scope['path'].is_symlink():
            raise SupervisorError('execution owner mismatch')
        return scope
    def admit(self, sid, pid):
        with self._lock:
            s=self._scopes.get(sid)
            if not s or s['state'] not in ('CREATED','OPEN'): raise SupervisorError('scope not admissible')
            try: (s['path']/'cgroup.procs').write_text(str(int(pid))); members=self.members(sid)
            except (OSError, ValueError) as e: raise SupervisorError('admission failed') from e
            if int(pid) not in members: raise SupervisorError('membership not verified')
            s['state']='ACTIVE'; return True
    def close(self, sid):
        with self._lock:
            s=self._scopes.get(sid)
            if not s: raise SupervisorError('unknown scope')
            if s['state'] in ('QUIESCENT','CLOSED','DRAINING'): return
            s['state']='CLOSED'
            if s['owner'] is not None:
                self._audit({'event':'scope_closed','scope_id':sid,'owner':list(s['owner'])})
    def members(self, sid):
        s=self._scopes.get(sid)
        if not s: raise SupervisorError('unknown scope')
        try: return [int(x) for x in (s['path']/'cgroup.procs').read_text().split()]
        except (OSError, ValueError) as e: raise SupervisorError('membership indeterminate') from e
    def quiescent(self, sid):
        with self._lock:
            s=self._scopes.get(sid)
            if not s or s['state'] not in ('CLOSED','DRAINING'): return False
            members=self.members(sid)
            try:
                events=dict(line.split() for line in (s['path']/'cgroup.events').read_text().splitlines())
            except (OSError, ValueError) as e: raise SupervisorError('population indeterminate') from e
            if events.get('populated') not in ('0','1'):
                raise SupervisorError('population indeterminate')
            if members or events['populated']=='1': s['state']='DRAINING'; return False
            s['state']='QUIESCENT'; return True
    def state(self, sid): return self._scopes[sid]['state']
    def terminate_reconcile(self,sid,owner,recovery_request_id):
        with self._lock:
            scope=self.authorize(sid,owner)
            if self.audit_path is None: raise SupervisorError('recovery audit unavailable')
            if not isinstance(recovery_request_id,str) or \
                    not RECOVERY_ID.fullmatch(recovery_request_id) or \
                    recovery_request_id in scope['recovery_ids']:
                raise SupervisorError('stale or replayed recovery request')
            self._audit({'event':'recovery_authorized','scope_id':sid,
                'owner':list(owner),'recovery_request_id':recovery_request_id,
                'prior_state':scope['state']})
            scope['recovery_ids'].add(recovery_request_id)
            return self.termination.run(sid,recovery_request_id)
