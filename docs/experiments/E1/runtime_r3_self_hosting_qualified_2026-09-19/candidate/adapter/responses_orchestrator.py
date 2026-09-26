"""Caller-owned, stateless Responses reasoning loop for the Programmer Agent."""
import json, os, urllib.request
from contextlib import nullcontext
from .orchestrator import PROTOCOL_VERSION

# Complete model-visible Programmer registry. Git is omitted until hook/filter
# and subprocess behavior is qualified.
TOOL_NAMES=('governed_read','governed_list','governed_search','governed_write',
            'governed_patch','governed_exec','governed_status',
            'authority_expansion_request','finish_task')
TO_ACTION={'governed_read':'read','governed_list':'list','governed_search':'search',
           'governed_write':'write','governed_patch':'patch','governed_exec':'exec',
           'governed_status':'status','authority_expansion_request':'authority_expansion',
           'finish_task':'finish'}

def _string(description=None):
    return {'type':'string', **({'description':description} if description else {})}
def _matches(value, schema):
    kind=schema.get('type')
    if 'enum' in schema and value not in schema['enum']: return False
    if kind=='string': return isinstance(value,str) and len(value)>=schema.get('minLength',0)
    # Range denial goes through the governed action path for attributable,
    # policy-safe diagnostics. The schema publishes the same runtime limits.
    if kind=='integer': return type(value) is int
    if kind=='array': return isinstance(value,list) and all(
        _matches(item,schema['items']) for item in value)
    if kind=='object':
        return (isinstance(value,dict) and
                set(value)==set(schema.get('required',[])) and
                all(_matches(value[key],spec) for key,spec in
                    schema.get('properties',{}).items()))
    return False
def tool_definitions():
    path={'repository':_string('Absolute designated repository root, not a repository alias; never expands grants.'),
          'path':_string('Repository-relative resource path; no absolute path, parent traversal or symlinks. Read/list/search still require read grants.')}
    specs={
      'governed_read':({**path,'limit':{'type':'integer','minimum':1,'maximum':65536,'description':'Maximum returned bytes, 1..65536 inclusive; reads from start, no offset. Returned content needs separate transmission clearance.'}},['repository','path','limit']),
      'governed_list':({**path,'limit':{'type':'integer','minimum':1,'maximum':1000,'description':'Maximum entries, 1..1000; path must be a permitted directory.'}},['repository','path','limit']),
      'governed_search':({**path,'query':{'type':'string','minLength':1,'description':'Nonempty literal substring; no regex. Directory only; at most 2000 scanned files, 1 MB per file, 500 characters per matching line.'},'limit':{'type':'integer','minimum':1,'maximum':100}},
                         ['repository','path','query','limit']),
      'governed_write':({**path,'content':_string('Whole replacement UTF-8 text; at most 1,000,000 encoded bytes. Exact write grants and parent-creation rules apply.')},['repository','path','content']),
      'governed_patch':({'repository':path['repository'],'changes':{'type':'array','minItems':1,'maxItems':1,'description':'Exactly one whole-file write; parent must already exist; no rename/delete/diff operations.','items':{
          'type':'object','additionalProperties':False,'properties':{
              'op':{'type':'string','enum':['write']},'path':path['path'],'content':_string('Whole replacement; at most 1,000,000 UTF-8 bytes.')},
          'required':['op','path','content']}}},['repository','changes']),
      'governed_exec':({'executable':_string('Exact released executable; no shell or unlisted program.'),'argv':{'type':'array','items':_string(),'description':'Exact released argument vector; not a shell command.'},
                        'cwd':_string('Exact released workspace root.'),'inputs':{'type':'array','items':_string(),'description':'Exact released bounded snapshot input paths; never dot, arbitrary paths, or controller evidence.'}},
                       ['executable','argv','cwd','inputs']),
      'governed_status':({},[]),
      'authority_expansion_request':({'capability':_string(),'action':_string(),
          'resources':{'type':'array','items':_string()},'reason':_string()},
          ['capability','action','resources','reason']),
      'finish_task':({'summary':_string('Programmer completion assessment only; does not grant Experiment acceptance.')},['summary'])}
    descriptions={'governed_status':'Read-only invocation status; separate transmission policy may redact it.',
        'authority_expansion_request':'Non-effecting request for additional authority. PENDING is not approval; never self-authorizes.',
        'finish_task':'Report Programmer completion only after authorized work; does not establish Architect acceptance.'}
    return [{'type':'function','name':name,
             'description':descriptions.get(name,'Governed KGE Forge operation; host authorization and separate result transmission clearance apply.'),
             'parameters':{'type':'object','additionalProperties':False,
                           'properties':specs[name][0],'required':specs[name][1]},
             'strict':True} for name in TOOL_NAMES]

class ResponsesReasoning:
    def __init__(self, orchestrator, model='gpt-5',
                 endpoint='https://api.openai.com/v1/responses'):
        self.orchestrator=orchestrator; self.model=model; self.endpoint=endpoint
        raw=orchestrator.host.auth.model_transport
        self.transport=json.loads(raw) if raw else None
        if self.transport is not None:
            from .model_transport import validate
            validate(self.transport,endpoint,model)
        from .model_transmission import TransmissionBoundary
        self.transmission=TransmissionBoundary(orchestrator.host)
        from .context_projection import ContextProjection
        self.projection=ContextProjection(orchestrator.host) if orchestrator.host.auth.context_projection else None
        self._bound_authorization=orchestrator.host.auth
        self.response_id=None; self.records=[]; self.finished=False
        self.control=getattr(orchestrator.host,'run_control',None)
        if self.control is None and self.transmission.policy and self.transmission.policy.get('run_control'):
            from .run_control import RunControl
            host=orchestrator.host
            self.control=RunControl(host.audit,{'authorization_id':host.auth.authorization_id,
                'session_id':host.auth.session_id,'invocation_id':host.auth.turn_id,
                'work_package_id':host.auth.work_package_id},self.transmission.policy['run_control'])
            host.run_control=self.control
    def _span(self,name):
        return self.control.span(name) if self.control else nullcontext()
    def _call(self, payload):
        from .controller_authority_store import require_effect_boundary
        require_effect_boundary()
        from .control_plane_binding import forbid_effect
        forbid_effect(self.orchestrator.host.auth)
        if self.transport is not None:
            from .model_transport import opener, request
            req=request(self.transport,self.endpoint,payload,
                        os.environ[self.transport['credential_environment_reference']])
            with opener(self.transport).open(req,timeout=self.transport['timeout_seconds']) as response:
                if self.control:
                    rid=response.headers.get('x-request-id')
                    self.control.emit('transport_headers_received',{'provider_request_id':
                        rid if isinstance(rid,str) and len(rid)<=200 and all(c.isalnum() or c in '_-' for c in rid) else None})
                return json.loads(response.read())
        req=urllib.request.Request(self.endpoint,data=json.dumps(payload).encode(),
          headers={'Authorization':'Bearer '+os.environ['OPENAI_API_KEY'],
                   'Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=60) as response:
            return json.loads(response.read())
    def _verify_context(self):
        with self._span('validation'):
            return self._verify_context_body()
    from .controller_authority_store import pure_resolution

    @pure_resolution
    def _verify_context_body(self):
        self.orchestrator.host.verify_lifecycle()
        if self.control and self.orchestrator.host.activation_transaction:
            self.control.emit('governance_observation',{'authorization':self.orchestrator.host.auth.state,
                'ownership':'HELD','supervisor':'READY'})
        if self.orchestrator.host.auth is not self._bound_authorization:
            raise ValueError('reasoning authorization changed')
        if self.transmission.policy != (json.loads(self._bound_authorization.model_transmission)
                                       if self._bound_authorization.model_transmission else None):
            raise ValueError('transmission policy changed')
        if self.projection is not None:
            return self.projection.verify()['projection']['payload']
        binding=self._bound_authorization.context_binding
        if binding is not None:
            binding.verify()
            if self._bound_authorization.work_package_id=='E1-WP-001' and self._bound_authorization.state=='ACTIVE':
                raise ValueError('E1 requires separated context projection')
        return None
    def _dispatch(self, call):
        self._verify_context()
        name=call.get('name'); call_id=call.get('call_id')
        if self.finished:
            return {'action_request_id':call_id,'result':'DENIED',
                    'error':'programmer already finished'}
        registered={item['name']:item for item in tool_definitions()}
        try: args=json.loads(call.get('arguments','{}'))
        except (TypeError,ValueError): args=None
        schema=registered.get(name,{}).get('parameters',{})
        if (not call_id or not isinstance(args,dict) or name not in TO_ACTION or
            set(args)!=set(schema.get('required',[])) or
            not all(_matches(args[key],spec) for key,spec in
                    schema.get('properties',{}).items()) or
            any(key in args for key in ('type','scope_id','execution_scope_id'))):
            return {'action_request_id':call_id,'result':'DENIED',
                    'error':'invalid registered tool request'}
        if name=='governed_exec' and '.' in args['inputs']:
            return {'action_request_id':call_id,'result':'DENIED',
                    'error':'execution inputs must name bounded paths'}
        raw={**args,'protocol_version':PROTOCOL_VERSION,'action_request_id':call_id,
             'type':TO_ACTION[name],
             'session_id':self.orchestrator.host.auth.session_id,
             'turn_id':self.orchestrator.host.auth.turn_id,
             'authorization_id':self.orchestrator.host.auth.authorization_id,
             'authorization_revision':self.orchestrator.host.auth.revision}
        result=self.orchestrator.request(raw)
        if name=='finish_task' and result['result']=='SUCCEEDED':
            self.finished=True
            self.terminal_action_id=call['call_id']
        return result
    def run(self, task, context, max_cycles=12):
        from .run_control import BudgetExceeded
        try:
            result=self._run(task,context,max_cycles)
            if self.control:
                if result['status']!='COMPLETE':
                    self._stop(result['status'])
                else:self.control.emit('final_disposition',{'disposition':'COMPLETED',
                    'ownership':'RELEASED' if self.orchestrator.host.activation_transaction else 'NONE'})
            return result
        except BaseException as exc:
            if self.control:
                self._stop('BUDGET_EXHAUSTED' if isinstance(exc,BudgetExceeded) else 'INTERRUPTED')
            raise
    def _stop(self,reason):
        if getattr(self,'_stopped',False):return
        self._stopped=True
        host=self.orchestrator.host
        self.control.close(reason)
        host.revoke()
        tx=host.activation_transaction
        if tx:
            result=tx.cancel(host,reason)
        else:
            uncertain=host.status()['architectural_state']!='QUIESCENT'
            result={'disposition':'INDETERMINATE' if uncertain else 'CANCELLED',
                'ownership':'UNKNOWN' if uncertain else 'NONE',
                'uncertainty':'RECONCILIATION_REQUIRED' if uncertain else None}
        unresolved=self.control.requests!=self.control.responses
        self.control.emit('final_disposition',dict(result,reason=reason,
            provider_uncertainty='REQUEST_OUTCOME_UNKNOWN' if unresolved else None,
            provider_termination='LOCAL_INTERRUPTION_ONLY_NO_PROVIDER_CANCELLATION_CONFIRMED' if unresolved else 'NO_OUTSTANDING_REQUEST_OBSERVED'))
    def _run(self, task, context, max_cycles):
        if self.orchestrator.host.auth.state!='ACTIVE':
            raise ValueError('Programmer authorization not released')
        binding=self.orchestrator.host.auth.context_binding
        selected=self._verify_context()
        if selected is not None:
            if {'task':task,'context':context}!=selected:
                raise ValueError('model payload differs from cleared projection')
            task,context=selected['task'],selected['context']
        elif binding is not None and context!=binding.model_context():
            raise ValueError('Programmer context must be controller-constructed')
        self.transmission.initial(task,context)
        from .context_projection import model_input
        input_items=model_input({'task':task,'context':context})
        history=[]
        for _ in range(max_cycles):
            if self.control:self.control.next_cycle();self.control.emit('preparation_start',{})
            selected=self._verify_context()
            if selected is not None and selected!={'task':task,'context':context}:
                raise ValueError('model projection changed during continuation')
            self.transmission.initial(task,context)
            # Re-evaluate all prior governed results under current verified policy.
            input_items=model_input({'task':task,'context':context})
            with self._span('continuation_construction'):
                for old_output, old_results in history:
                    input_items.extend(old_output)
                    for old_call, old_result in old_results:
                        input_items.append({'type':'function_call_output',
                            'call_id':old_call.get('call_id'),
                            'output':json.dumps(self.transmission.result(old_call,old_result))})
            self._verify_context()
            payload={'model':self.model,'input':input_items,'tools':tool_definitions(),
                     'parallel_tool_calls':False,'store':False,
                     'include':['reasoning.encrypted_content']}
            from .context_projection import digest as content_digest, model_payload_digest
            if json.loads(self.orchestrator.host.auth.operational_binding or '{}').get('governance',{}).get('schema')==8:
                # Scope is authenticated by the same production validation above.
                # Stop BEFORE request binding, request counters, transport or tools.
                self.control.check(admit_model=True)
                result={'status':'MODEL_REQUEST_READY','ModelPayloadDigest':model_payload_digest({'task':task,'context':context}),
                        'ModelRequestDigest':content_digest(payload),'ready_monotonic':__import__('time').monotonic(),
                        'model_requests':0,'provider_requests':0}
                self.control.emit('model_request_ready',result)
                binding=self.orchestrator.host.auth.context_binding.governance.run8['binding']
                if __import__('pathlib').Path(binding['qualification_root']).name=='hard-cancellation':
                    while True:
                        self.control.check()
                        __import__('time').sleep(0.25)
                return result
            self.orchestrator.host._write({'event':'model_request_content_bound',
                'ModelPayloadDigest':model_payload_digest({'task':task,'context':context}),
                'ModelRequestDigest':content_digest(payload)})
            if self.control:
                self.control.emit('preparation_end',{})
                self.control.check(admit_model=True);self.control.requests+=1
                self.control.emit('model_request_start',{'request_digest':content_digest(payload)})
            with self._span('provider_transport'):
                if self.control:self.control.emit('transport_start',{})
                response=self._call(payload)
                if self.control:self.control.response(response)
            with self._span('response_validation'):self._verify_context()
            self.response_id=response.get('id')
            output=response.get('output',[])
            self.records.append({'response_id':self.response_id,
                                 'output_types':[item.get('type') for item in output]})
            calls=[item for item in output if item.get('type')=='function_call']
            if self.control:self.control.emit('tool_extraction',{'count':len(calls),
                'registered_operations':[c.get('name') if c.get('name') in TOOL_NAMES else 'UNKNOWN' for c in calls]})
            if not calls:
                transaction=self.orchestrator.host.activation_transaction
                if self.finished and transaction is not None:
                    transaction.complete(self.orchestrator.host,self.terminal_action_id)
                return {'status':'COMPLETE' if self.finished else 'INCOMPLETE',
                        'response_id':self.response_id,'cycles':len(self.records),
                        'records':self.records}
            results=[]
            for call in calls:
                with self._span('action_dispatch'):result=self._dispatch(call)
                results.append((call,result))
                if self.control and result['result']=='SUCCEEDED' and result['type'] in ('read','write','patch','exec'):
                    if result['type']=='read' and self.transmission.result(call,result).get('transmission')!='CLEARED':
                        continue
                    # Outcome content identity, not fresh call IDs, defeats equivalent repeats.
                    data=result.get('data',{})
                    meaningful={k:v for k,v in data.items() if k not in ('scope_id','execution_scope_id',
                        'action_request_id','launcher_pid','snapshot_manifest_sha256')}
                    if result['type']=='exec':meaningful={'result':data.get('result'),'quiescent':data.get('quiescent')}
                    self.control.progress_event(content_digest({'type':result['type'],'data':meaningful}),'GOVERNED_RESULT')
            history.append((output,results))
            if self.control:self.control.emit('cycle_end',{});self.control.cycle_start=None
        return {'status':'LOOP_BOUND','response_id':self.response_id,
                'cycles':len(self.records),'records':self.records}
