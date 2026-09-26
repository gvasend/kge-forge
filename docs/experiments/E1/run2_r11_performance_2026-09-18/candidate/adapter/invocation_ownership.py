"""Controller-owned durable single-active execution reservation."""
from pathlib import Path
import fcntl, json, os, re
from .recovery_ledger import _observe, _events, RecoveryDenied, CGROUP_BASE, SUPERVISOR_AUDIT

class OwnershipDenied(RuntimeError): pass
SCOPE_ID=re.compile(r'^scope-[0-9a-f]{32}$')

class InvocationOwnership:
    def __init__(self,path,cgroup_base=CGROUP_BASE,supervisor_audit=SUPERVISOR_AUDIT):
        self.path=Path(path).resolve(); self.base=Path(cgroup_base)
        self.activation_owner=None
        self.supervisor_audit=Path(supervisor_audit)
        self.path.parent.mkdir(parents=True,exist_ok=True)
    def _locked(self):
        fd=os.open(self.path,os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600)
        fcntl.flock(fd,fcntl.LOCK_EX)
        return fd
    def _history(self,fd):
        os.lseek(fd,0,os.SEEK_SET)
        size=os.fstat(fd).st_size
        if size>10_000_000: raise OwnershipDenied('ownership audit exceeds bound')
        data=b''
        while len(data)<size:
            part=os.read(fd,size-len(data))
            if not part: raise OwnershipDenied('ownership audit truncated')
            data+=part
        try: records=[json.loads(line) for line in data.decode().splitlines()]
        except (ValueError,UnicodeError) as exc: raise OwnershipDenied('ownership audit corrupt') from exc
        active=None
        invocation=None
        if data and not data.endswith(b'\n'): raise OwnershipDenied('ownership history truncated')
        for record in records:
            if record.get('event')=='invocation_reserved':
                if invocation is not None or active is not None: raise OwnershipDenied('competing invocation')
                invocation=record
            elif record.get('event')=='invocation_released':
                if invocation is None or active is not None or record.get('reservation_id')!=invocation.get('reservation_id'):
                    raise OwnershipDenied('invalid invocation release')
                invocation=None
            elif record.get('event')=='reserved':
                if active is not None or not all(record.get(key) for key in
                        ('scope_id','action_request_id','session_id','authorization_id','controller_audit')):
                    raise OwnershipDenied('ownership chain contradictory')
                if invocation is not None and any(record.get(k)!=invocation.get(k) for k in ('authorization_id','session_id','controller_audit')):
                    raise OwnershipDenied('execution not owned by invocation')
                active=record
            elif record.get('event')=='released':
                if active is None or record.get('scope_id')!=active['scope_id'] or \
                        record.get('action_request_id')!=active['action_request_id']:
                    raise OwnershipDenied('ownership release contradictory')
                active=None
            else: raise OwnershipDenied('ownership event unknown')
        return active
    def _append(self,fd,record):
        os.lseek(fd,0,os.SEEK_END)
        os.write(fd,(json.dumps(record,sort_keys=True)+'\n').encode()); os.fsync(fd)
    def reserve(self,scope_id,action_request_id,session_id,authorization_id,controller_audit):
        if not SCOPE_ID.fullmatch(scope_id): raise OwnershipDenied('scope identity invalid')
        from .activation_transaction import execution_guard
        gate=execution_guard(self)
        fd=None
        try:
            fd=self._locked()
            if self._history(fd) is not None:
                raise OwnershipDenied('prior execution reservation unresolved')
            self._append(fd,{'event':'reserved','scope_id':scope_id,
                'action_request_id':action_request_id,'session_id':session_id,
                'authorization_id':authorization_id,
                'controller_audit':str(Path(controller_audit).resolve())})
        finally:
            if fd is not None: os.close(fd)
            if gate is not None: os.close(gate)
    def release(self,scope_id,action_request_id,session_id,authorization_id):
        fd=self._locked()
        try:
            active=self._history(fd)
            if active is None or any(active[key]!=value for key,value in (
                    ('scope_id',scope_id),('action_request_id',action_request_id),
                    ('session_id',session_id),('authorization_id',authorization_id))):
                raise OwnershipDenied('ownership identity mismatch or stale release')
            try: observation=_observe(self.base/scope_id)
            except RecoveryDenied as exc: raise OwnershipDenied(str(exc)) from exc
            if observation['members'] or observation['populated']!=0:
                raise OwnershipDenied('execution scope remains populated')
            owner=[session_id,authorization_id,action_request_id]
            try: events=_events(self.supervisor_audit)
            except RecoveryDenied as exc: raise OwnershipDenied(str(exc)) from exc
            created=[event for event in events if event.get('event')=='scope_created' and
                     event.get('scope_id')==scope_id and event.get('owner')==owner]
            closed=[event for event in events if event.get('event')=='scope_closed' and
                    event.get('scope_id')==scope_id and event.get('owner')==owner]
            if len(created)!=1 or not closed:
                raise OwnershipDenied('supervisor owner or admission closure unproved')
            self._append(fd,{'event':'released','scope_id':scope_id,
                'action_request_id':action_request_id,
                'kernel_observation':observation})
        finally: os.close(fd)
    def active(self):
        fd=self._locked()
        try: return self._history(fd)
        finally: os.close(fd)
