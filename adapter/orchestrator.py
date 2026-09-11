"""Reasoning-only governed action protocol (A2.3)."""
from dataclasses import asdict
import json, hashlib, time, uuid
from .governed_host import GovernedHost, WorkAuthorization, Denied

PROTOCOL_VERSION = 1
EFFECT_ACTIONS = {'write','patch','exec'}
ACTION_TYPES = {'read','write','patch','exec','status','authority_expansion','finish'}

class ProtocolError(Exception): pass

class ReasoningOrchestrator:
    def __init__(self, host):
        self.host=host; self.results={}; self.audit=host.audit
    def _id(self): return 'req-'+uuid.uuid4().hex
    def request(self, raw):
        if not isinstance(raw,dict) or raw.get('protocol_version') != PROTOCOL_VERSION: raise ProtocolError('invalid protocol version')
        rid=raw.get('action_request_id') or self._id()
        if rid in self.results: return self.results[rid]
        typ=raw.get('type');
        if typ not in ACTION_TYPES: return self._deny(rid,'unknown action')
        expected={'session_id':self.host.auth.session_id,'turn_id':self.host.auth.turn_id,'authorization_id':self.host.auth.authorization_id,'authorization_revision':self.host.auth.revision}
        for key,value in expected.items():
            if raw.get(key) != value: return self._deny(rid,'identity or authorization mismatch')
        try:
            if typ=='read': result=self.host.governed_read(raw['repository'],raw['path'],int(raw.get('limit',65536)))
            elif typ=='write': result=self.host.governed_write(raw['repository'],raw['path'],raw['content'])
            elif typ=='patch': result=self.host.governed_patch(raw['repository'],raw['changes'])
            elif typ=='exec': result=self.host.governed_exec(tuple([raw['executable'],*raw.get('argv',[])]),raw['cwd'])
            elif typ=='status': result=self.host.status()
            elif typ=='authority_expansion': result=self.host.expansion(raw['capability'],raw['action'],raw.get('resources',[]),raw.get('reason',''))
            else: result={'summary':raw.get('summary',''),'status':'REQUESTED'}
            out={'action_request_id':rid,'result':'SUCCEEDED','type':typ,'data':result}
        except (Denied,KeyError,ValueError,TypeError) as e: out={'action_request_id':rid,'result':'DENIED','type':typ,'error':str(e)}
        self.results[rid]=out; self.host._write({'event':'action_result','action_request_id':rid,'type':typ,'result':out['result'],'digest':hashlib.sha256(json.dumps(out,sort_keys=True).encode()).hexdigest()}); return out
    def _deny(self,rid,error):
        out={'action_request_id':rid,'result':'DENIED','error':error};self.results[rid]=out;self.host._write({'event':'action_result','action_request_id':rid,'result':'DENIED','error':error});return out

def action(**fields): return {'protocol_version':PROTOCOL_VERSION, **fields}
