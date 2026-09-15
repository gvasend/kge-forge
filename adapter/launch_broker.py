"""Minimal host launch-broker framed channel (A2.1i)."""
import json, struct

MAX_FRAME=65536

def send_frame(stream, value):
    data=json.dumps(value,separators=(',',':')).encode()
    if len(data)>MAX_FRAME: raise ValueError('frame too large')
    stream.write(struct.pack('!I',len(data))+data); stream.flush()

def recv_frame(stream):
    h=stream.read(4)
    if len(h)!=4: raise EOFError('truncated frame')
    n=struct.unpack('!I',h)[0]
    if n==0 or n>MAX_FRAME: raise ValueError('invalid frame length')
    b=stream.read(n)
    if len(b)!=n: raise EOFError('truncated frame')
    try: return json.loads(b)
    except json.JSONDecodeError as e: raise ValueError('invalid json') from e

class BrokerProtocol:
    def __init__(self, session, authorization, scope):
        self.session=session; self.authorization=authorization; self.scope=scope; self.seen=set(); self.closed=False
    def validate(self, req):
        if self.closed: raise ValueError('channel closed')
        if req.get('protocol_version')!=1: raise ValueError('protocol mismatch')
        rid=req.get('action_request_id')
        if not rid or rid in self.seen: raise ValueError('replay or missing request')
        if req.get('session_id')!=self.session or req.get('authorization_id')!=self.authorization or req.get('execution_scope_id')!=self.scope: raise ValueError('binding mismatch')
        if req.get('op') not in {'create','admit','members','close','quiescent'}: raise ValueError('operation denied')
        self.seen.add(rid); return True
    def fail(self): self.closed=True
