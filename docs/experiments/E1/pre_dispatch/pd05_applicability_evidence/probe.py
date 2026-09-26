import sys, pathlib, json, hashlib, subprocess, dataclasses, tempfile, datetime
sys.path.insert(0,'/home/gvasend/app/kge-forge')
from adapter.context_binding import CommittedContext
from adapter.authority_profile import programmer_authorization
from adapter.governed_host import GovernedHost
from adapter.orchestrator import ReasoningOrchestrator, ACTION_TYPES, action
from adapter.responses_orchestrator import TOOL_NAMES, TO_ACTION, tool_definitions, ResponsesReasoning
root=pathlib.Path('/home/gvasend/app/kge-forge'); out=root/'docs/experiments/E1/pre_dispatch/pd05_applicability_evidence'
sha=lambda b:hashlib.sha256(b).hexdigest()
cap='5871bdce4f5b6539c84f69f4f2b2f94ee31be5cd'
b=CommittedContext(root/'docs/experiments/E1/pre_dispatch/CONTEXT_MANIFEST.json',cap)
a=programmer_authorization(b,'auth-pd05-inactive-evidence',1,'session-pd05-inactive-evidence','turn-pd05-inactive-evidence')
assert a.state=='INACTIVE' and not a.exec_bins and not a.exec_argv_allowlist
old=[json.loads(x) for x in pathlib.Path('/tmp/a2-e1-profile-probe.jsonl').read_text().splitlines()][0]['authorization']
record=dict(a.__dict__);record['context_binding']={'context_sha256':b.digest,'capture_commit':cap,'baseline_id':b.manifest['baseline_id'],'work_id':b.manifest['work_id']}
assert all(record[k]==v or isinstance(record[k],tuple) and list(record[k])==v for k,v in old.items() if k not in ('authorization_id','session_id','turn_id'))
def tree(p):
 if not p.exists(): return {'exists':False}
 if p.is_file(): return {'exists':True,'sha256':sha(p.read_bytes())}
 return {'exists':True,'files':{str(f.relative_to(p)):sha(f.read_bytes()) for f in sorted(p.rglob('*')) if f.is_file() and not f.is_symlink()}}
watched=[pathlib.Path(p) for p in a.write_roots]+list(b.protected_paths)+[pathlib.Path(a.ownership_ledger)]
before={str(p):tree(p) for p in watched}
auditdir=pathlib.Path(tempfile.mkdtemp(prefix='pd05-inactive-evidence-'))
h=GovernedHost(a,auditdir/'audit.jsonl'); o=ReasoningOrchestrator(h)
base={'session_id':a.session_id,'turn_id':a.turn_id,'authorization_id':a.authorization_id,'authorization_revision':a.revision}
fields={'read':dict(repository=str(root),path='docs/VISION.md'), 'list':dict(repository=str(root),path='docs'), 'search':dict(repository=str(root),path='docs',query='E1'), 'write':dict(repository=str(root),path='src/kge_forge/context/pd05_unreleased_probe.txt',content='UNRELEASED PROBE MUST NOT WRITE'), 'patch':dict(repository=str(root),changes=[dict(op='write',path='src/kge_forge/__init__.py',content='UNRELEASED PROBE MUST NOT PATCH')]), 'exec':dict(executable='python3',argv=['-c','pass'],cwd=str(root),inputs=[]), 'status':{}, 'authority_expansion':dict(capability='shell',action='run',resources=['/bin/sh'],reason='inactive denial evidence'), 'finish':dict(summary='inactive denial evidence')}
results={k:o.request(action(type=k,action_request_id='pd05-'+k,**base,**v)) for k,v in fields.items()}
assert set(fields)==ACTION_TYPES==set(TO_ACTION.values()) and set(TOOL_NAMES)==set(TO_ACTION)
for k,v in results.items():
 assert (v['result']=='SUCCEEDED') if k=='status' else (v['result']=='DENIED' and v['error']=='authorization not released')
try: ResponsesReasoning(o).run('NO IMPLEMENTATION; inactive denial probe',b.model_context(),1)
except ValueError as e: model_denial=str(e)
else: raise AssertionError('inactive model loop accepted')
assert not h.invocations and h.scope is None and h._pending is None and a.state=='INACTIVE'
after={str(p):tree(p) for p in watched}; assert before==after
# Policy-only resolution, no contents read and no model action or ACTIVE profile.
paths={}
for alias,r in b.repos.items():
 for hidden in ('.git','.codex','.agents'):
  try: h._path(str(r),hidden+'/config'); disposition='RESOLVES_INSIDE_READ_GRANT'
  except Exception as e: disposition=type(e).__name__+': '+str(e)
  paths[alias+'/'+hidden]=disposition
source_rows=[]
for sid,s in b.sources.items():
 rev=s.get('revision',cap); p=b.repos[s['repository']]/s['path']
 blob=subprocess.check_output(['/usr/bin/git','-C',str(b.repos[s['repository']]),'cat-file','blob',rev+':'+s['path']])
 source_rows.append(dict(id=sid,repository=s['repository'],path=s['path'],revision=rev,sha256=s['sha256'],working_matches=sha(p.read_bytes())==s['sha256'],committed_matches=sha(blob)==s['sha256']))
quals=[]
for name,p in [('bound','/tmp/a2-bound-evidence-57ac5751b64f4233bf18609e308e53a7/audit.jsonl'),('recovery','/tmp/a2-live-recovery-evidence-4ec219720ec445b196aef14770bbf09d/controller.jsonl'),('recovery_second','/tmp/a2-live-recovery-evidence-4ec219720ec445b196aef14770bbf09d/controller-second.jsonl'),('ownership','/tmp/a2-live-recovery-evidence-4ec219720ec445b196aef14770bbf09d/ownership.jsonl'),('restart','/tmp/a2-controller-restart-evidence-ab206fa10725415a87ee0fe7945a125c/controller.jsonl')]:
 p=pathlib.Path(p)
 if not p.exists(): quals.append({'name':name,'path':str(p),'available':False});continue
 data=p.read_bytes(); events=[json.loads(x) for x in data.splitlines()]; (out/(name+'.jsonl')).write_bytes(data)
 quals.append({'name':name,'path':str(p),'available':True,'sha256':sha(data),'events':len(events),'authorizations':[e['authorization'] for e in events if e.get('event')=='authorization_issued'],'action_results':[{'id':e.get('action_request_id'),'type':e.get('type'),'result':e.get('result')} for e in events if e.get('event')=='action_result']})
(out/'inactive_audit.jsonl').write_bytes(h.audit.read_bytes())
report={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'head':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'capture':cap,'context_sha256':b.digest,'source_count':len(b.sources),'mandatory_closure':sorted(b.closure),'profile':record,'same_as_historical_prepared_profile_except_probe_ids':True,'tool_definitions':tool_definitions(),'action_types':sorted(ACTION_TYPES),'sources':source_rows,'inactive_results':results,'model_loop_denial':model_denial,'host_invocations':len(h.invocations),'scope':None,'watched_before':before,'watched_after_equal':before==after,'path_policy_resolution_without_read':paths,'qualification_artifacts':quals,'state':json.loads((root/'docs/experiments/E1/pre_dispatch/STATE.json').read_text())}
(out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ('head','source_count','same_as_historical_prepared_profile_except_probe_ids','host_invocations','scope','watched_after_equal','path_policy_resolution_without_read')},indent=2))
