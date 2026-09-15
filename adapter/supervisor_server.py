"""Narrow host-side Unix-socket facade for HostScopeSupervisor (A2.1f)."""
import json, os, socket, sys
import subprocess
from .host_supervisor import HostScopeSupervisor, SupervisorError
from .launch_broker import recv_frame, send_frame

def serve(path):
    try: os.unlink(path)
    except FileNotFoundError: pass
    s=socket.socket(socket.AF_UNIX); s.bind(path); os.chmod(path,0o600); s.listen(4)
    sup=HostScopeSupervisor()
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
            elif op=='create': out={'scope_id':sup.create(req.get('scope_id'))}
            elif op=='admit': out={'admitted':sup.admit(sid,req['pid'])}
            elif op=='members': out={'members':sup.members(sid)}
            elif op=='close': sup.close(sid); out={'state':sup.state(sid)}
            elif op=='quiescent': out={'quiescent':sup.quiescent(sid),'state':sup.state(sid)}
            else: raise SupervisorError('invalid operation')
        except Exception as e: out={'error':type(e).__name__+': '+str(e)}
        send_frame(f,out); c.close()

if __name__=='__main__': serve(sys.argv[1])
