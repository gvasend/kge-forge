"""Trusted fixed-destination bridge for the isolated Bubblewrap control process."""
from pathlib import Path
import socket, subprocess
from .launch_broker import recv_frame, send_frame

SUPERVISOR_SOCKET='/tmp/a21m.sock'
ADAPTER_DIR=Path(__file__).resolve().parent

class BridgeError(RuntimeError): pass

class ForwardBridge:
    def __init__(self, session, authorization, scope, action, root):
        self.session=session; self.authorization=authorization; self.scope=scope
        self.action=action; self.root=str(Path(root).resolve()); self.sequence=0
    def exchange(self, op, **fields):
        if set(fields)&{'protocol_version','broker_request_id','action_request_id',
                        'session_id','authorization_id','execution_scope_id',
                        'scope_id','op'}:
            raise BridgeError('reserved execution binding supplied')
        self.sequence+=1; broker_id=f'{self.action}:{self.sequence}:{op}'
        request={'protocol_version':1,'broker_request_id':broker_id,
                 'action_request_id':self.action,'session_id':self.session,
                 'authorization_id':self.authorization,
                 'execution_scope_id':self.scope,'scope_id':self.scope,
                 'op':op,**fields}
        if (request['execution_scope_id']!=self.scope or
            request['scope_id']!=self.scope or request['action_request_id']!=self.action):
            raise BridgeError('request binding mismatch')
        argv=['/usr/bin/bwrap','--die-with-parent','--unshare-pid','--new-session',
              '--proc','/proc','--dev','/dev','--bind',self.root,'/scope',
              '--chdir','/scope','--ro-bind','/usr','/usr','--ro-bind','/bin','/bin',
              '--ro-bind','/lib','/lib','--ro-bind','/lib64','/lib64','--unshare-net',
              '--ro-bind',str(ADAPTER_DIR),'/adapter','python3','-m',
              'adapter.control_process',self.session,self.authorization,
              self.scope,self.action]
        child=None
        try:
            child=subprocess.Popen(argv,stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                                   stderr=subprocess.DEVNULL,
                                   env={'PATH':'/usr/bin:/bin','PYTHONPATH':'/'})
            send_frame(child.stdin,request)
            forwarded=recv_frame(child.stdout)
            if forwarded!=request: raise BridgeError('control request mismatch')
            with socket.socket(socket.AF_UNIX) as sock:
                sock.settimeout(12); sock.connect(SUPERVISOR_SOCKET)
                stream=sock.makefile('rwb',buffering=0)
                send_frame(stream,forwarded); response=recv_frame(stream)
            send_frame(child.stdin,response)
            confirmed=recv_frame(child.stdout)
            if (confirmed!=response or child.wait(timeout=5)!=0 or
                response.get('request_id')!=broker_id or
                response.get('execution_scope_id')!=self.scope or
                response.get('action_request_id')!=self.action):
                raise BridgeError('response binding mismatch')
            if 'error' in response: raise BridgeError(response['error'])
            return response
        except (OSError,EOFError,ValueError,subprocess.TimeoutExpired) as exc:
            raise BridgeError('supervisor channel indeterminate') from exc
        finally:
            if child is not None:
                if child.poll() is None: child.kill()
                child.wait()
                child.stdin.close(); child.stdout.close()
