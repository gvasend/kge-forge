"""Narrow host-side Unix-socket facade for HostScopeSupervisor (A2.1f)."""
import json, os, socket, sys, time
import subprocess
from .host_supervisor import HostScopeSupervisor, SupervisorError
from .launch_broker import recv_frame, send_frame

def serve(path):
    try: os.unlink(path)
    except FileNotFoundError: pass
    s=socket.socket(socket.AF_UNIX); s.bind(path); os.chmod(path,0o600); s.listen(4)
    sup=HostScopeSupervisor(); held={}
    while True:
        c,_=s.accept()
        try:
            f=c.makefile('rwb',buffering=0); req=recv_frame(f); op=req.get('op'); sid=req.get('scope_id')
            if op=='status': out={'status':'READY'}
            elif op=='spawn_barrier':
                if not sid: raise SupervisorError('scope required')
                p=subprocess.Popen(['python3','-c','import sys; sys.stdin.buffer.read(1)'],stdin=subprocess.PIPE)
                # Child inherits supervisor's delegated parent cgroup; admit it
                # before releasing the start barrier.
                out={'pid':p.pid,'scope_id':sid,'initial_cgroup':open('/proc/%s/cgroup'%p.pid).read()}
                out['admitted']=sup.admit(sid,p.pid)
                out['members']=sup.members(sid)
                p.stdin.write(b'1'); p.stdin.flush(); out['released']=True
            elif op=='qual_spawn':
                if not sid: raise SupervisorError('scope required')
                read_fd, write_fd=os.pipe()
                p=subprocess.Popen(['python3','-m','adapter.qual_launcher',str(read_fd)],
                                   stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                                   pass_fds=(read_fd,))
                os.close(read_fd)
                try:
                    admitted=sup.admit(sid,p.pid)
                    admission_ns=time.monotonic_ns()
                    p.stdin.write(b'1'); p.stdin.close()
                    result=json.loads(p.stdout.readline())
                    p.wait(timeout=5)
                    held[sid]=write_fd
                    out={'admitted':admitted,'admission_ns':admission_ns,
                         'launcher_pid':p.pid,'launcher_exit_ns':time.monotonic_ns(),
                         'launcher_returncode':p.returncode, **result}
                except Exception:
                    os.close(write_fd); p.kill(); p.wait(); raise
            elif op=='qual_release':
                if sup.state(sid) not in ('CLOSED','DRAINING'): raise SupervisorError('scope must be closed')
                fd=held.pop(sid); os.write(fd,b'1'); os.close(fd)
                out={'released_ns':time.monotonic_ns()}
            elif op=='create': out={'scope_id':sup.create(req.get('scope_id'))}
            elif op=='admit': out={'admitted':sup.admit(sid,req['pid'])}
            elif op=='members': out={'members':sup.members(sid)}
            elif op=='close': sup.close(sid); out={'state':sup.state(sid)}
            elif op=='quiescent': out={'quiescent':sup.quiescent(sid),'state':sup.state(sid)}
            else: raise SupervisorError('invalid operation')
        except Exception as e: out={'error':type(e).__name__+': '+str(e)}
        send_frame(f,out); c.close()

if __name__=='__main__': serve(sys.argv[1])
