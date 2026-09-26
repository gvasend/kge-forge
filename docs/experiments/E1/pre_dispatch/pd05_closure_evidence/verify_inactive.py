"""Evidence-only denial checks; never activates or executes the E1 package."""
import hashlib,json,tempfile
from pathlib import Path
from adapter.context_binding import CommittedContext
from adapter.authority_profile import programmer_authorization
from adapter.governed_host import GovernedHost
from adapter.orchestrator import ReasoningOrchestrator
from adapter.responses_orchestrator import ResponsesReasoning

out=Path(__file__).resolve().parent
root=out.parents[4]
b=CommittedContext(out.parent/'CONTEXT_MANIFEST.json','5871bdce4f5b6539c84f69f4f2b2f94ee31be5cd')
proposal=json.loads((out/'PROPOSED_E1_PROFILE.json').read_text())
a=programmer_authorization(b,'auth-pd05-r2-inactive-evidence',2,
    'session-pd05-r2-inactive-evidence','turn-pd05-r2-inactive-evidence',
    exec_argv_allowlist=proposal['execution']['exact_top_level_argv_allowlist'])
assert a.state=='INACTIVE'
# Only supported WorkAuthorization fields are instantiated. Proposed cwd/input/
# environment requirements are not claimed implemented by this constructor.
def observe(p):
    p=Path(p)
    if not p.exists(): return {'exists':False}
    if p.is_dir(): return {'exists':True,'type':'directory'}
    return {'exists':True,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
watched=sorted(set(str(p) for p in b.protected_paths)|set(a.write_roots)|{a.ownership_ledger})
before={p:observe(p) for p in watched}
tmp=Path(tempfile.mkdtemp(prefix='pd05-r2-inactive-'))
h=GovernedHost(a,tmp/'audit.jsonl'); r=ResponsesReasoning(ReasoningOrchestrator(h))
forge=str(b.repos['forge'])
requests={
 'governed_read':{'repository':forge,'path':'docs/VISION.md','limit':100},
 'governed_list':{'repository':forge,'path':'docs','limit':100},
 'governed_search':{'repository':forge,'path':'docs','query':'E1','limit':100},
 'governed_write':{'repository':forge,'path':'src/kge_forge/__init__.py','content':'MUST NOT WRITE'},
 'governed_patch':{'repository':forge,'changes':[{'op':'write','path':'src/kge_forge/__init__.py','content':'MUST NOT PATCH'}]},
 'governed_exec':{'executable':a.exec_argv_allowlist[0][0],'argv':list(a.exec_argv_allowlist[0][1:]),'cwd':forge,'inputs':proposal['execution']['authorized_source_inputs']},
 'governed_status':{},
 'authority_expansion_request':{'capability':'shell','action':'run','resources':['/bin/sh'],'reason':'inactive denial evidence'},
 'finish_task':{'summary':'inactive denial evidence'}}
results={}
for name,args in requests.items():
    result=r._dispatch({'name':name,'call_id':'inactive-r2-'+name,'arguments':json.dumps(args)})
    assert result['result']==('SUCCEEDED' if name=='governed_status' else 'DENIED')
    if name!='governed_status': assert result['error']=='authorization not released'
    results[name]=result
try: r.run('INACTIVE CHECK ONLY',b.model_context(),1)
except ValueError as e: model_denial=str(e)
else: raise AssertionError('inactive model run accepted')
assert not h.invocations and h.scope is None and h._pending is None
assert before=={p:observe(p) for p in watched}
record=dict(a.__dict__);record['context_binding']={'capture_commit':b.capture_commit,'context_sha256':b.digest}
(out/'inactive_r2_audit.jsonl').write_bytes(h.audit.read_bytes())
(out/'INACTIVE_VERIFICATION.json').write_text(json.dumps({'profile_state':a.state,
 'materialized_supported_fields_only':record,'proposed_fields_not_enforced':['exact source cwd','exact input list','PYTHONPATH payload environment'],
 'results':results,'model_call_denial':model_denial,'host_invocations':0,'scope':None,
 'before':before,'after_equal':True,'source_verification':b.verify(),
 'production_ownership_ledger_unchanged':True},indent=2)+'\n')
print('INACTIVE: all eight non-status actions denied; zero host invocations/scopes; protected sources and product targets unchanged.')
