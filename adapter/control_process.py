"""Dedicated stdio control process; payload stdio is separate (A2.1j)."""
import subprocess, sys
from .launch_broker import recv_frame, send_frame, BrokerProtocol

def run(payload_argv):
    # Control stdin/stdout are reserved for framed supervisor traffic. Payload
    # receives independent pipes and can never write into this stream.
    proto=None
    try:
        while True:
            req=recv_frame(sys.stdin.buffer)
            if proto is None:
                proto=BrokerProtocol(req.get('session_id'),req.get('authorization_id'),req.get('execution_scope_id'))
            proto.validate(req)
            send_frame(sys.stdout.buffer, {'ok':True,'request_id':req['action_request_id']})
    except (EOFError,ValueError):
        if proto: proto.fail()
        return 1

if __name__=='__main__': raise SystemExit(run(sys.argv[1:]))
