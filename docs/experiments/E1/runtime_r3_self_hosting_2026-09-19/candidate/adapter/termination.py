"""Bounded, scope-selected pidfd termination with kernel reconciliation."""
from pathlib import Path
import ctypes, errno, os, platform, signal, time

class TerminationError(RuntimeError): pass

MAX_DIRECTORIES=128
MAX_MEMBERS=4096

class PidfdSignaler:
    def __init__(self): self.libc=ctypes.CDLL(None,use_errno=True)
    def _syscall(self,number,*args):
        result=self.libc.syscall(number,*args)
        if result<0:
            number=ctypes.get_errno()
            raise OSError(number,os.strerror(number))
        return result
    def _open(self,pid):
        if hasattr(os,'pidfd_open'): return os.pidfd_open(pid,0)
        if platform.machine()!='x86_64': raise TerminationError('pidfd unavailable')
        return self._syscall(434,pid,0)
    def _send(self,fd,signum):
        if hasattr(signal,'pidfd_send_signal'):
            return signal.pidfd_send_signal(fd,signum)
        if platform.machine()!='x86_64': raise TerminationError('pidfd signal unavailable')
        return self._syscall(424,fd,signum,ctypes.c_void_p(0),0)
    def signal(self,pid,signum,scope_cgroup):
        try: fd=self._open(pid)
        except OSError as exc:
            if exc.errno==errno.ESRCH: return 'DISAPPEARED'
            raise TerminationError('pidfd open failed') from exc
        try:
            try: lines=Path('/proc/%s/cgroup'%pid).read_text().splitlines()
            except OSError as exc:
                if exc.errno==errno.ENOENT: return 'DISAPPEARED'
                raise TerminationError('member cgroup unreadable') from exc
            paths=[line[3:] for line in lines if line.startswith('0::')]
            if len(paths)!=1 or not (paths[0]==scope_cgroup or
                                    paths[0].startswith(scope_cgroup+'/')):
                raise TerminationError('member left authorized scope')
            try: self._send(fd,signum)
            except OSError as exc:
                if exc.errno==errno.ESRCH: return 'DISAPPEARED'
                raise TerminationError('pidfd signal failed') from exc
            return 'DELIVERED'
        finally: os.close(fd)

class TerminationEngine:
    def __init__(self,supervisor,signaler,termination_seconds,grace_seconds,poll_seconds):
        self.sup=supervisor; self.signaler=signaler
        self.window=termination_seconds; self.grace=grace_seconds; self.poll=poll_seconds
        if not 0<self.window<=15 or not 0<=self.grace<=self.window or \
                not 0<self.poll<=.5:
            raise TerminationError('invalid bounded termination configuration')
    def _observe(self,sid):
        path=self.sup._scopes[sid]['path']; base=self.sup.base
        if path!=base/sid or path.is_symlink() or not path.is_dir():
            raise TerminationError('scope cgroup unavailable or substituted')
        directories=[path]; members=set()
        for directory in directories:
            if len(directories)>MAX_DIRECTORIES or directory.is_symlink() or \
                    base not in directory.parents:
                raise TerminationError('scope subtree uncertain')
            try:
                for child in sorted(directory.iterdir()):
                    if child.is_symlink(): raise TerminationError('scope subtree symlink')
                    if child.is_dir(): directories.append(child)
                for raw in (directory/'cgroup.procs').read_text().split():
                    pid=int(raw)
                    if pid<=0: raise ValueError('invalid member')
                    members.add(pid)
                if len(members)>MAX_MEMBERS: raise TerminationError('member bound exceeded')
            except (OSError,ValueError) as exc:
                raise TerminationError('scope membership observation failed') from exc
        try:
            events=dict(line.split() for line in (path/'cgroup.events').read_text().splitlines())
        except (OSError,ValueError) as exc:
            raise TerminationError('scope population observation failed') from exc
        populated=events.get('populated')
        if populated not in ('0','1') or (populated=='0' and members):
            raise TerminationError('scope membership/population contradictory')
        return {'members':sorted(members),'populated':int(populated),
                'directories':len(directories)}
    def run(self,sid,recovery_request_id):
        scope=self.sup._scopes[sid]
        actions=[]; observations=[]; deadline=time.monotonic()+self.window
        def observe(phase):
            evidence=self._observe(sid); observations.append(evidence)
            self.sup._audit({'event':'recovery_observation','scope_id':sid,
                'recovery_request_id':recovery_request_id,'phase':phase,**evidence})
            return evidence
        def finish(result,reason=None):
            scope['state']='QUIESCENT' if result=='QUIESCENT' else 'INDETERMINATE'
            final={'result':result,'state':scope['state'],
                   'observation_count':len(observations),
                   'termination_action_count':len(actions),
                   'initial_observation':observations[0] if observations else None,
                   'final_observation':observations[-1] if observations else None}
            if reason: final['reason']=reason
            self.sup._audit({'event':'recovery_final','scope_id':sid,
                'recovery_request_id':recovery_request_id,**final})
            return final
        try:
            prior_state=scope['state']
            self.sup.close(sid)
            if scope['state'] not in ('CLOSED','DRAINING','QUIESCENT'):
                raise TerminationError('admission not closed')
            initial=observe('initial')
            if initial['populated']==0 and not initial['members']:
                return finish('QUIESCENT')
            if prior_state=='QUIESCENT':
                raise TerminationError('post-quiescent population anomaly')
            scope['state']='DRAINING'
            for phase,signum,limit in (('TERM',signal.SIGTERM,
                min(deadline,time.monotonic()+self.grace)),
                ('KILL',signal.SIGKILL,deadline)):
                sent=set()
                while time.monotonic()<limit:
                    current=observe(phase)
                    if current['populated']==0 and not current['members']:
                        return finish('QUIESCENT')
                    for pid in current['members']:
                        if pid in sent or time.monotonic()>=deadline: continue
                        target='/kge-forge/executor/'+sid
                        self.sup._audit({'event':'termination_intent','scope_id':sid,
                            'recovery_request_id':recovery_request_id,'pid':pid,
                            'signal':phase,'expected_cgroup':target})
                        delivery=self.signaler.signal(pid,signum,target)
                        action={'pid':pid,'signal':phase,'delivery':delivery}
                        actions.append(action); sent.add(pid)
                        self.sup._audit({'event':'termination_action','scope_id':sid,
                            'recovery_request_id':recovery_request_id,**action})
                    time.sleep(self.poll)
            last=observe('final')
            if last['populated']==0 and not last['members']:
                return finish('QUIESCENT')
            return finish('INDETERMINATE',
                'bounded termination window expired with surviving population')
        except (TerminationError,OSError,ValueError) as exc:
            return finish('INDETERMINATE',str(exc))
