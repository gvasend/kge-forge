"""Caller-owned Responses API loop for A2.4.

The API client is reasoning-only: no built-in tools are requested. All effects are
dispatched through ReasoningOrchestrator.
"""
import json, os, urllib.request
from .orchestrator import ReasoningOrchestrator, PROTOCOL_VERSION

TOOL_NAMES=('governed_read','governed_list','governed_search','governed_write','governed_patch','governed_exec','governed_status','governed_git_status','governed_git_diff','authority_expansion_request','finish_task')
def tool_definitions():
    specs={'governed_read':({'path':{'type':'string'}},['path']), 'finish_task':({'summary':{'type':'string'}},['summary'])}
    out=[]
    for n in TOOL_NAMES:
        props,required=specs.get(n,({},[]))
        out.append({'type':'function','name':n,'description':'Governed action; authorization is enforced by the orchestrator.','parameters':{'type':'object','additionalProperties':False,'properties':props,'required':required},'strict':True})
    return out

class ResponsesReasoning:
    def __init__(self, orchestrator, model='gpt-5.4', endpoint='https://api.openai.com/v1/responses'):
        self.orchestrator=orchestrator; self.model=model; self.endpoint=endpoint; self.response_id=None; self.records=[]
    def _call(self, payload):
        req=urllib.request.Request(self.endpoint,data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+os.environ['OPENAI_API_KEY'],'Content-Type':'application/json'})
        with urllib.request.urlopen(req,timeout=60) as r: return json.loads(r.read())
    def run(self, task, context, max_cycles=8):
        input_items=[{'role':'user','content':[{'type':'input_text','text':task+'\nContext:\n'+json.dumps(context)}]}]
        for _ in range(max_cycles):
            payload={'model':self.model,'input':input_items,'tools':tool_definitions(),'parallel_tool_calls':False,'store':False}
            response=self._call(payload); self.response_id=response.get('id'); self.records.append({'response_id':self.response_id,'output_types':[x.get('type') for x in response.get('output',[])]})
            calls=[x for x in response.get('output',[]) if x.get('type')=='function_call']
            if not calls: return {'status':'FINISHED','response_id':self.response_id,'cycles':len(self.records),'records':self.records}
            outputs=list(response.get('output',[]))
            for call in calls:
                args=json.loads(call.get('arguments','{}')); args.update({'protocol_version':PROTOCOL_VERSION,'action_request_id':call.get('call_id'),'type':args.pop('type',call.get('name')),'session_id':self.orchestrator.host.auth.session_id,'turn_id':self.orchestrator.host.auth.turn_id,'authorization_id':self.orchestrator.host.auth.authorization_id,'authorization_revision':self.orchestrator.host.auth.revision})
                result=self.orchestrator.request(args); outputs.append({'type':'function_call_output','call_id':call.get('call_id'),'output':json.dumps(result)})
            input_items=outputs
        return {'status':'LOOP_BOUND','response_id':self.response_id,'cycles':len(self.records),'records':self.records}
