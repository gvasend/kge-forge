"""Host-side cgroup-v2 execution-scope supervisor.

The supervisor owns only the delegated executor subtree and fails closed when
the subtree is unavailable or mounted read-only.
"""
from pathlib import Path
import threading, uuid

class SupervisorError(RuntimeError): pass

class HostScopeSupervisor:
    def __init__(self, base='/sys/fs/cgroup/unified/kge-forge/executor'):
        self.base=Path(base); self._scopes={}; self._lock=threading.Lock()
        if not self.base.is_dir(): raise SupervisorError('delegated cgroup subtree unavailable')
        if not (self.base/'cgroup.procs').exists(): raise SupervisorError('not a cgroup v2 subtree')
    def create(self, execution_scope_id=None):
        with self._lock:
            sid=execution_scope_id or 'scope-'+uuid.uuid4().hex
            if sid in self._scopes: raise SupervisorError('scope already exists')
            path=self.base/sid
            try: path.mkdir()
            except OSError as e: raise SupervisorError('scope creation unavailable') from e
            self._scopes[sid]={'path':path,'state':'CREATED'}; return sid
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
            if s['state'] in ('QUIESCENT','CLOSED'): return
            s['state']='CLOSED'
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
