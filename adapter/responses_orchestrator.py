"""Caller-owned, stateless Responses reasoning loop for the Programmer Agent."""
import json, os, urllib.request
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

def _string(): return {'type':'string'}
def _matches(value, schema):
    kind=schema.get('type')
    if kind=='string': return isinstance(value,str)
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
    path={'repository':_string(),'path':_string()}
    specs={
      'governed_read':({**path,'limit':{'type':'integer'}},['repository','path','limit']),
      'governed_list':({**path,'limit':{'type':'integer'}},['repository','path','limit']),
      'governed_search':({**path,'query':_string(),'limit':{'type':'integer'}},
                         ['repository','path','query','limit']),
      'governed_write':({**path,'content':_string()},['repository','path','content']),
      'governed_patch':({'repository':_string(),'changes':{'type':'array','items':{
          'type':'object','additionalProperties':False,'properties':{
              'op':_string(),'path':_string(),'content':_string()},
          'required':['op','path','content']}}},['repository','changes']),
      'governed_exec':({'executable':_string(),'argv':{'type':'array','items':_string()},
                        'cwd':_string(),'inputs':{'type':'array','items':_string()}},
                       ['executable','argv','cwd','inputs']),
      'governed_status':({},[]),
      'authority_expansion_request':({'capability':_string(),'action':_string(),
          'resources':{'type':'array','items':_string()},'reason':_string()},
          ['capability','action','resources','reason']),
      'finish_task':({'summary':_string()},['summary'])}
    return [{'type':'function','name':name,
             'description':'Governed KGE Forge operation; host authorization applies.',
             'parameters':{'type':'object','additionalProperties':False,
                           'properties':specs[name][0],'required':specs[name][1]},
             'strict':True} for name in TOOL_NAMES]

class ResponsesReasoning:
    def __init__(self, orchestrator, model='gpt-5',
                 endpoint='https://api.openai.com/v1/responses'):
        self.orchestrator=orchestrator; self.model=model; self.endpoint=endpoint
        self.response_id=None; self.records=[]; self.finished=False
    def _call(self, payload):
        req=urllib.request.Request(self.endpoint,data=json.dumps(payload).encode(),
          headers={'Authorization':'Bearer '+os.environ['OPENAI_API_KEY'],
                   'Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=60) as response:
            return json.loads(response.read())
    def _dispatch(self, call):
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
        if name=='finish_task' and result['result']=='SUCCEEDED': self.finished=True
        return result
    def run(self, task, context, max_cycles=12):
        if self.orchestrator.host.auth.state!='ACTIVE':
            raise ValueError('Programmer authorization not released')
        binding=self.orchestrator.host.auth.context_binding
        if binding is not None:
            binding.verify()
            if context!=binding.model_context():
                raise ValueError('Programmer context must be controller-constructed')
        input_items=[{'role':'user','content':[{'type':'input_text',
            'text':task+'\nContext:\n'+json.dumps(context)}]}]
        for _ in range(max_cycles):
            if binding is not None: binding.verify()
            payload={'model':self.model,'input':input_items,'tools':tool_definitions(),
                     'parallel_tool_calls':False,'store':False,
                     'include':['reasoning.encrypted_content']}
            response=self._call(payload); self.response_id=response.get('id')
            output=response.get('output',[])
            self.records.append({'response_id':self.response_id,
                                 'output_types':[item.get('type') for item in output]})
            calls=[item for item in output if item.get('type')=='function_call']
            if not calls:
                return {'status':'COMPLETE' if self.finished else 'INCOMPLETE',
                        'response_id':self.response_id,'cycles':len(self.records),
                        'records':self.records}
            continuation=[*input_items,*output]
            for call in calls:
                result=self._dispatch(call)
                continuation.append({'type':'function_call_output',
                    'call_id':call.get('call_id'),'output':json.dumps(result)})
            input_items=continuation
        return {'status':'LOOP_BOUND','response_id':self.response_id,
                'cycles':len(self.records),'records':self.records}
