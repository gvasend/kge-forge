"""Narrow host-side Unix-socket facade for HostScopeSupervisor (A2.1f)."""
import json, os, select, socket, sys, time
import subprocess
from .host_supervisor import HostScopeSupervisor, SupervisorError
from .launch_broker import recv_frame, send_frame

RECOVERY_FIELDS={'protocol_version','broker_request_id','action_request_id',
    'session_id','authorization_id','execution_scope_id','scope_id','op',
    'recovery_request_id'}

def recovery_request(sup,req):
    try:
        if not isinstance(req,dict) or set(req)!=RECOVERY_FIELDS or \
                req.get('protocol_version')!=1 or \
                req.get('op')!='terminate_reconcile' or not req.get('broker_request_id') or \
                not req.get('session_id') or not req.get('authorization_id') or \
                not req.get('action_request_id') or not req.get('scope_id') or \
                req.get('execution_scope_id')!=req.get('scope_id'):
            raise SupervisorError('invalid governed recovery request')
        owner=(req['session_id'],req['authorization_id'],req['action_request_id'])
        out=sup.terminate_reconcile(req['scope_id'],owner,req['recovery_request_id'])
        return {'scope_id':req['scope_id'],'execution_scope_id':req['scope_id'],
            'action_request_id':req['action_request_id'],**out}
    except SupervisorError as exc:
        claim=req if isinstance(req,dict) else {}
        sup._audit({'event':'recovery_denied','claimed_scope_id':claim.get('scope_id'),
            'claimed_execution_scope_id':claim.get('execution_scope_id'),
            'claimed_owner':[claim.get('session_id'),claim.get('authorization_id'),
                             claim.get('action_request_id')],
            'recovery_request_id':claim.get('recovery_request_id'),'reason':str(exc)})
        raise

def serve(path):
    try: os.unlink(path)
    except FileNotFoundError: pass
    s=socket.socket(socket.AF_UNIX); s.bind(path); os.chmod(path,0o600); s.listen(4)
    sup=HostScopeSupervisor(audit_path=path+'.supervisor-audit.jsonl'); held={}; runs={}
    while True:
        c,_=s.accept()
        req={}
        try:
            f=c.makefile('rwb',buffering=0); req=recv_frame(f)
            if not isinstance(req,dict): raise SupervisorError('request object required')
            op=req.get('op'); sid=req.get('scope_id')
            if req.get('broker_request_id'):
                if (not req.get('session_id') or not req.get('authorization_id') or
                    not req.get('action_request_id') or not sid or
                    sid!=req.get('execution_scope_id') or
                    (sid in runs and req['action_request_id']!=runs[sid]['action_request_id'])):
                    raise SupervisorError('execution binding mismatch')
                if op!='create' and sid in sup._scopes and sup._scopes[sid]['owner'] is not None:
                    sup.authorize(sid,(req['session_id'],req['authorization_id'],
                                       req['action_request_id']))
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
            elif op=='production_spawn':
                aid=req.get('action_request_id')
                if not aid or not sid or sid!=req.get('execution_scope_id'):
                    raise SupervisorError('execution binding mismatch')
                argv=req.get('argv'); root=req.get('root')
                if (sid in runs or not isinstance(argv,list) or not argv or
                    not all(isinstance(x,str) and x for x in argv) or
                    not isinstance(root,str) or not os.path.isdir(root)):
                    raise SupervisorError('invalid production launch')
                p=subprocess.Popen(['python3','-m','adapter.exec_barrier',root,*argv],
                                   stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                                   stderr=subprocess.DEVNULL)
                try:
                    admitted=sup.admit(sid,p.pid)
                    admitted_ns=time.monotonic_ns()
                    initial_cgroup=open('/proc/%s/cgroup'%p.pid).read().splitlines()[-1]
                    if initial_cgroup!='0::/kge-forge/executor/'+sid:
                        raise SupervisorError('launcher cgroup mismatch')
                    p.stdin.write(b'1'); p.stdin.close()
                    deadline=time.monotonic()+10; buffer=b''
                    while b'\n' not in buffer and len(buffer)<65536:
                        remaining=deadline-time.monotonic()
                        if remaining<=0: raise SupervisorError('payload result timeout')
                        readable,_,_=select.select([p.stdout],[],[],remaining)
                        if not readable: raise SupervisorError('payload result timeout')
                        chunk=os.read(p.stdout.fileno(),4096)
                        if not chunk: raise SupervisorError('payload result unavailable')
                        buffer+=chunk
                    if b'\n' not in buffer: raise SupervisorError('payload result too large')
                    runs[sid]={'action_request_id':aid,'process':p}
                    out={'scope_id':sid,'execution_scope_id':sid,'action_request_id':aid,
                         'launcher_pid':p.pid,'admitted':admitted,
                         'admitted_ns':admitted_ns,'initial_cgroup':initial_cgroup,
                         'result_available_ns':time.monotonic_ns(),
                         'result':buffer.split(b'\n',1)[0].decode(errors='replace')}
                except Exception:
                    if p.poll() is None: p.kill()
                    p.wait(); sup.close(sid); raise
            elif op=='production_status':
                run=runs.get(sid)
                if not run or run['action_request_id']!=req.get('action_request_id'):
                    raise SupervisorError('execution binding mismatch')
                p=run['process']; out={'scope_id':sid,'action_request_id':run['action_request_id'],
                                      'launcher_pid':p.pid,'returncode':p.poll()}
            elif op=='create':
                owner=(req['session_id'],req['authorization_id'],req['action_request_id']) \
                    if req.get('broker_request_id') else None
                out={'scope_id':sup.create(req.get('scope_id'),owner)}
            elif op=='admit': out={'admitted':sup.admit(sid,req['pid'])}
            elif op=='members': out={'members':sup.members(sid)}
            elif op=='close': sup.close(sid); out={'state':sup.state(sid)}
            elif op=='quiescent': out={'quiescent':sup.quiescent(sid),'state':sup.state(sid)}
            elif op=='terminate_reconcile': out=recovery_request(sup,req)
            else: raise SupervisorError('invalid operation')
        except Exception as e:
            if isinstance(req,dict) and req.get('op')=='terminate_reconcile':
                try: sup._audit({'event':'recovery_handler_error',
                    'claimed_scope_id':req.get('scope_id'),
                    'recovery_request_id':req.get('recovery_request_id'),
                    'reason':type(e).__name__+': '+str(e)})
                except OSError: pass
            out={'error':type(e).__name__+': '+str(e)}
        if isinstance(req,dict) and req.get('broker_request_id'):
            out['request_id']=req['broker_request_id']
            out['execution_scope_id']=req.get('execution_scope_id')
            out['action_request_id']=req.get('action_request_id')
        send_frame(f,out); c.close()

if __name__=='__main__': serve(sys.argv[1])
