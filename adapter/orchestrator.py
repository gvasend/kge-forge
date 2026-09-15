"""Reasoning-only governed action protocol (A2.3)."""
from dataclasses import asdict
import json, hashlib, threading, time, uuid
from .governed_host import GovernedHost, WorkAuthorization, Denied, Indeterminate
from .context_binding import ContextDenied
from .invocation_ownership import OwnershipDenied

PROTOCOL_VERSION = 1
EFFECT_ACTIONS = {'write','patch','exec'}
ACTION_TYPES = {'read','list','search','write','patch','exec','status','authority_expansion','finish'}

class ProtocolError(Exception): pass

class ReasoningOrchestrator:
    def __init__(self, host):
        self.host=host; self.audit=host.audit
        prior=host.reconstruction or {'results':{},'requests':{}}
        self.results=dict(prior['results'])
        self._request_digests={rid:event['request_sha256']
            for rid,event in prior['requests'].items()}
        self._lock=threading.Lock(); self._inflight=set()
        self._dispatch_token=object(); host.bind_dispatcher(self._dispatch_token)
    def _id(self): return 'req-'+uuid.uuid4().hex
    def request(self, raw):
        if not isinstance(raw,dict) or raw.get('protocol_version') != PROTOCOL_VERSION: raise ProtocolError('invalid protocol version')
        rid=raw.get('action_request_id') or self._id()
        with self._lock:
            if rid in self.results:
                try: digest=hashlib.sha256(json.dumps(raw,sort_keys=True).encode()).hexdigest()
                except (TypeError,ValueError): digest=None
                if self._request_digests.get(rid)!=digest:
                    self.host._write({'event':'action_replay_denied',
                        'action_request_id':rid,'reason':'request digest changed'})
                    return {'action_request_id':rid,'result':'DENIED',
                            'error':'replayed ActionRequest identity changed'}
                return self.results[rid]
            if rid in self._inflight: return {'action_request_id':rid,'result':'DENIED','error':'request in flight'}
            self._inflight.add(rid)
        self.host.action_started(rid)
        typ=raw.get('type');
        if typ not in ACTION_TYPES: return self._deny(rid,'unknown action',raw)
        expected={'session_id':self.host.auth.session_id,'turn_id':self.host.auth.turn_id,'authorization_id':self.host.auth.authorization_id,'authorization_revision':self.host.auth.revision}
        for key,value in expected.items():
            if raw.get(key) != value: return self._deny(rid,'identity or authorization mismatch',raw)
        if typ=='exec' and ('scope_id' in raw or 'execution_scope_id' in raw):
            return self._deny(rid,'execution scope identity supplied by caller',raw)
        try: request_digest=hashlib.sha256(json.dumps(raw,sort_keys=True).encode()).hexdigest()
        except (TypeError,ValueError): return self._deny(rid,'request not serializable',raw)
        intent={'event':'action_request','action_request_id':rid,'type':typ,
                'session_id':expected['session_id'],'turn_id':expected['turn_id'],
                'authorization_id':expected['authorization_id'],
                'authorization_revision':expected['authorization_revision'],
                'work_package_id':self.host.auth.work_package_id,
                'request_sha256':request_digest}
        if self.host.auth.context_binding is not None:
            intent['context_sha256']=self.host.auth.context_binding.digest
            intent['capture_commit']=self.host.auth.context_binding.capture_commit
        if typ in EFFECT_ACTIONS:
            intent['target']=raw.get('path') if typ=='write' else raw.get('cwd') if typ=='exec' else \
                [change.get('path') for change in raw.get('changes',[]) if isinstance(change,dict)]
            if typ=='exec':
                intent['argv']=[raw.get('executable'),*raw.get('argv',[])] if \
                    isinstance(raw.get('argv',[]),list) else None
                intent['inputs']=raw.get('inputs')
            elif typ=='write' and isinstance(raw.get('content'),str):
                intent['content_sha256']=hashlib.sha256(raw['content'].encode()).hexdigest()
            elif typ=='patch' and isinstance(raw.get('changes'),list):
                intent['content_sha256']=[hashlib.sha256(change['content'].encode()).hexdigest()
                    if isinstance(change,dict) and isinstance(change.get('content'),str) else None
                    for change in raw['changes']]
        self.host._write(intent)
        self._request_digests[rid]=request_digest
        try:
            if self.host.auth.state!='ACTIVE' and typ!='status':
                raise Denied('authorization not released')
            if self.host._interruption_requested and typ in EFFECT_ACTIONS|{'finish'}:
                raise Denied('turn interrupted; new effects denied')
            if self.host.ownership is not None and typ in EFFECT_ACTIONS|{'finish'}:
                try: active_owner=self.host.ownership.active()
                except (OwnershipDenied,OSError) as exc:
                    raise Denied('execution ownership evidence unavailable') from exc
                if active_owner is not None:
                    raise Denied('prior execution ownership unresolved')
            if self.host.auth.context_binding is not None:
                try: self.host.auth.context_binding.verify()
                except ContextDenied as exc: raise Denied(str(exc)) from exc
            if (self.host.scope and self.host.scope.state!='QUIESCENT' and
                typ in EFFECT_ACTIONS|{'finish'}):
                raise Denied('prior scope not authoritatively quiescent')
            if typ=='read': result=self.host.governed_read(raw['repository'],raw['path'],int(raw.get('limit',65536)))
            elif typ=='list': result=self.host.governed_list(raw['repository'],raw['path'],int(raw.get('limit',100)))
            elif typ=='search': result=self.host.governed_search(raw['repository'],raw['path'],raw['query'],int(raw.get('limit',100)))
            elif typ=='write': result=self.host.governed_write(raw['repository'],raw['path'],raw['content'],rid)
            elif typ=='patch': result=self.host.governed_patch(raw['repository'],raw['changes'],rid)
            elif typ=='exec':
                argv=tuple([raw['executable'],*raw.get('argv',[])])
                permit=self.host.issue_exec_permit(rid,argv,raw['cwd'],raw.get('execution_scope_id'),
                                                   raw.get('inputs'),self._dispatch_token)
                result=self.host.governed_exec(argv,raw['cwd'],permit)
            elif typ=='status': result=self.host.status()
            elif typ=='authority_expansion': result=self.host.expansion(raw['capability'],raw['action'],raw.get('resources',[]),raw.get('reason',''))
            else: result={'summary':raw.get('summary',''),'status':'REQUESTED'}
            out={'action_request_id':rid,'result':'SUCCEEDED','type':typ,'data':result}
        except Indeterminate as e: out={'action_request_id':rid,'result':'INDETERMINATE','type':typ,'execution_scope_id':self.host.scope.id if self.host.scope else None,'error':str(e)}
        except (Denied,KeyError,ValueError,TypeError) as e: out={'action_request_id':rid,'result':'DENIED','type':typ,'error':str(e)}
        self.host._write({'event':'action_result','action_request_id':rid,'execution_scope_id':out.get('data',{}).get('execution_scope_id') if isinstance(out.get('data'),dict) else out.get('execution_scope_id'),'type':typ,'result':out['result'],'digest':hashlib.sha256(json.dumps(out,sort_keys=True).encode()).hexdigest(),'payload':out})
        with self._lock:
            self.results[rid]=out; self._inflight.discard(rid)
        self.host.action_terminal(rid)
        return out
    def _deny(self,rid,error,raw):
        try: digest=hashlib.sha256(json.dumps(raw,sort_keys=True).encode()).hexdigest()
        except (TypeError,ValueError): digest=None
        self._request_digests[rid]=digest
        self.host._write({'event':'action_request','action_request_id':rid,
            'type':'REJECTED','session_id':self.host.auth.session_id,
            'turn_id':self.host.auth.turn_id,
            'authorization_id':self.host.auth.authorization_id,
            'authorization_revision':self.host.auth.revision,
            'request_sha256':digest,'rejection':error})
        out={'action_request_id':rid,'result':'DENIED','error':error}
        self.host._write({'event':'action_result','action_request_id':rid,'result':'DENIED','error':error,
            'digest':hashlib.sha256(json.dumps(out,sort_keys=True).encode()).hexdigest(),
            'payload':out})
        with self._lock:
            self.results[rid]=out; self._inflight.discard(rid)
        self.host.action_terminal(rid)
        return out

def action(**fields): return {'protocol_version':PROTOCOL_VERSION, **fields}
