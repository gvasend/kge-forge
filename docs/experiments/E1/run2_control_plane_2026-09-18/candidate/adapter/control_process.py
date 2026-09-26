"""Isolated framed control endpoint; payload has separate stdio."""
import sys
from .launch_broker import recv_frame, send_frame, BrokerProtocol

def run(session, authorization, scope, action):
    protocol=BrokerProtocol(session,authorization,scope,action)
    try:
        request=recv_frame(sys.stdin.buffer)
        protocol.validate(request)
        send_frame(sys.stdout.buffer,request)
        response=recv_frame(sys.stdin.buffer)
        if (response.get('request_id')!=request['broker_request_id'] or
            response.get('execution_scope_id')!=scope or
            response.get('action_request_id')!=action):
            raise ValueError('response binding mismatch')
        send_frame(sys.stdout.buffer,response)
        return 0
    except (EOFError,ValueError,KeyError):
        protocol.fail(); return 1

if __name__=='__main__': raise SystemExit(run(*sys.argv[1:5]))
