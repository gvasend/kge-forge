"""Fixed-destination framed bridge between Bubblewrap stdio and supervisor socket."""
import socket, sys
from .launch_broker import recv_frame, send_frame, BrokerProtocol

def run(sock_path, child_argv):
    sup=socket.socket(socket.AF_UNIX); sup.settimeout(10); sup.connect(sock_path)
    import subprocess
    child=subprocess.Popen(child_argv,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    sr=sup.makefile('rwb', buffering=0)
    exchanges=0
    try:
        while True:
            req=recv_frame(child.stdout)
            # Validate the envelope before forwarding; destination is fixed.
            if not isinstance(req,dict) or req.get('protocol_version')!=1: raise ValueError('invalid protocol')
            if not isinstance(req,dict): raise ValueError('invalid envelope')
            send_frame(sr,req)
            resp=recv_frame(sr)
            if resp.get('request_id') not in (None, req.get('action_request_id')): raise ValueError('response correlation mismatch')
            send_frame(child.stdin,resp)
            exchanges += 1
    except (EOFError,ValueError,OSError):
        if child.poll() is None: child.kill()
        return 0 if exchanges else 1

if __name__=='__main__': raise SystemExit(run(sys.argv[1],sys.argv[2:]))
