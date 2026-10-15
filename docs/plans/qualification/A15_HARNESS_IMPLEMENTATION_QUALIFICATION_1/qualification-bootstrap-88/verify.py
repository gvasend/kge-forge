"""Independent typed-graph reachability and append-only register verification.
No runtime/gate imports, launch, service, probe, or synthetic test invocation.
"""
import copy,hashlib,json,pathlib
OUT=pathlib.Path(__file__).resolve().parent;ROOT=pathlib.Path(__file__).resolve().parents[5]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def reach_components(nodes,edges):
 adjacency={n:set() for n in nodes}
 for e in edges:adjacency[e['FROM']].add(e['TO'])
 reached={}
 for n in sorted(nodes):
  seen={n};todo=[n]
  while todo:
   v=todo.pop()
   for w in adjacency[v]-seen:seen.add(w);todo.append(w)
  reached[n]=seen
 groups={tuple(sorted(w for w in nodes if w in reached[n] and n in reached[w])) for n in nodes}
 return sorted([list(g) for g in groups])
def safety(s):
 assert s['gate_qualified'] is False and s['host_qualified'] is False,'unqualified capability'
 assert s['atomic_is_durable'] is False and s['name_is_consumption'] is False,'primitive substituted for complete once proof'
 assert s['duplicate_launch'] is False and s['failure_reopens'] is False,'one-use safety'
 assert s['circular_trust'] is False and s['admin_permission_verified'] is False,'unsupported trust'
 assert s['argv']==s['retained_argv'] and s['probe_limits']==s['retained_limits'],'scope changed'
 assert s['H77_execution'] is False and s['A15_execution'] is False and s['authority_issued'] is False,'effects included'
 assert s['bootstrap_qualified'] is False and s['technical_trust_root_qualified'] is False,'candidate treated as qualified'
 assert not any(len(c)>1 for c in reach_components(s['nodes'],s['revised_edges'])),'new bootstrap cycle'
 return {'RESULT':'PARTIAL','DEPENDENCY_CYCLE_CONFIRMED':'YES','INDEPENDENT_TRUST_ROOT_FOUND':'NO','BOOTSTRAP_QUALIFIED':'NO','AUTHORITY_DECISION_READY':'NO','DECISION_OPTIONS':[]}
def main():
 old=OUT.parent/'system-probe-authority-87';idx=read(old/'evidence-index.json')
 for p,h in idx['FILES'].items():assert sha(ROOT/p)==h
 graph=read(OUT/'dependency-cycle-graph.json');body=dict(graph);identity=body.pop('IDENTITY');assert hashlib.sha256(canon(body)).hexdigest()==identity['sha256']
 for e in graph['EDGES']:assert sha(ROOT/e['SOURCE_PIN']['path'])==e['SOURCE_PIN']['raw_sha256']
 # Separate reconstruction of the current selected route, not authority lifecycle.
 expected={('GATE_ACTIVE_QUALIFICATION','HOST_RESOURCE_ENFORCEMENT_QUALIFICATION'),('HOST_RESOURCE_ENFORCEMENT_QUALIFICATION','INDEPENDENT_EVIDENCE'),('INDEPENDENT_EVIDENCE','SYSTEM_LEVEL_PROBE'),('SYSTEM_LEVEL_PROBE','QUALIFIED_ONE_USE_LAUNCH'),('QUALIFIED_ONE_USE_LAUNCH','GATE_ACTIVE_QUALIFICATION')}
 assert expected<={(e['FROM'],e['TO']) for e in graph['EDGES']}
 assert any(e['TYPE']=='STRATEGY_CHOICE' for e in graph['EDGES'] if e['FROM']=='QUALIFIED_ONE_USE_LAUNCH' and e['TO']=='GATE_ACTIVE_QUALIFICATION')
 components=reach_components(graph['NODES'],graph['EDGES']);cyclic=[g for g in components if len(g)>1];assert len(cyclic)==1 and set(cyclic[0])=={'GATE_ACTIVE_QUALIFICATION','HOST_RESOURCE_ENFORCEMENT_QUALIFICATION','INDEPENDENT_EVIDENCE','SYSTEM_LEVEL_PROBE','QUALIFIED_ONE_USE_LAUNCH'}
 assert read(OUT/'minimal-cyclic-component.json')['MINIMAL_CYCLIC_COMPONENT']==cyclic[0]
 strategy=read(OUT/'minimum-cycle-breaking-strategy.json');inventory=read(OUT/'bootstrap-candidate-inventory.json');assert [c['CANDIDATE'] for c in inventory['CANDIDATES']]==['A','B','C'] and all(c['QUALIFIED'] is False for c in inventory['CANDIDATES'])
 for c in inventory['CANDIDATES']:
  for name in ('TRUST_ROOT','AUTHORITY_SOURCE','COMMAND_IDENTITY','CONSUMPTION_IDENTITY','ATOMICITY_GUARANTEE','DURABILITY_GUARANTEE','CONCURRENCY_GUARANTEE','CRASH_RECOVERY_RULE','RESOURCE_BOUNDARY','EVIDENCE_BOUNDARY','QUALIFICATION_REQUIREMENTS','CURRENT_STATUS'):assert name in c
 assert strategy['ORIGINAL_ONE_USE_INVARIANTS_UNCHANGED']=={'attempts':1,'retries':0,'failure_reopens':False,'unknown_reopens':False}
 spec=read(OUT.parent/'system-process-enforcement-86/transient-service-specification.json');subject=read(OUT/'proposed-bootstrap-authority-subject.json');assert subject['EXACT_TARGET_ARGV']==spec['EXACT_COMMAND_ARGV'] and subject['TARGET_NOT_EXECUTABLE_UNDER_THIS_SUBJECT'] is True
 assert subject['ISSUED_AUTHORITY'] is None and subject['DECISION_OPTIONS']==[]
 sb=dict(subject);sid=sb.pop('EXACT_SUBJECT_IDENTITY');assert hashlib.sha256(canon(sb)).hexdigest()==sid['sha256']
 assert subject['PROPOSED_SOURCE_BOUNDARY']==['adapter/qualification_bootstrap/systemd_pids_once.py','adapter/tests/test_systemd_pids_bootstrap.py']
 oldreg=read(OUT/'lessons-register-before.json');reg=read(ROOT/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');assert reg['POLICY']==oldreg['POLICY'] and reg['REGISTER_ID']==oldreg['REGISTER_ID'] and reg['EVENTS'][:-1]==oldreg['EVENTS']
 previous='0'*64
 for event in reg['EVENTS']:
  eb={k:v for k,v in event.items() if k!='EVENT_HASH'};assert event['PREVIOUS_EVENT_HASH']==previous and hashlib.sha256(json.dumps(eb,sort_keys=True,separators=(',',':')).encode()).hexdigest()==event['EVENT_HASH'];previous=event['EVENT_HASH']
 latest=reg['EVENTS'][-1];assert latest==read(OUT/'ll11-appended-event.json') and latest['LESSON']['LESSON_ID']=='LL-11' and latest['EVENT_TYPE']=='LESSON_RECORDED' and latest['WORK_PACKAGE']=='88'
 assert len({e['LESSON']['LESSON_ID'] for e in reg['EVENTS'] if e['EVENT_TYPE']=='LESSON_RECORDED'})==11
 for p in latest['LESSON']['EVIDENCE']:assert sha(ROOT/p['path'])==p['raw_sha256']
 assert (ROOT/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.md').read_bytes().startswith((OUT/'lessons-register-before.md').read_bytes())
 # Complete Lesson content identity independently of the event-chain hash.
 lid={'kind':'CONTENT_IDENTITY','namespace':'planner-reasoning-lesson-v1','sha256':hashlib.sha256(canon(latest['LESSON'])).hexdigest()}
 state={'gate_qualified':False,'host_qualified':False,'atomic_is_durable':False,'name_is_consumption':False,'duplicate_launch':False,'failure_reopens':False,'circular_trust':False,'admin_permission_verified':False,'argv':subject['EXACT_TARGET_ARGV'],'retained_argv':spec['EXACT_COMMAND_ARGV'],'probe_limits':spec['LIMITS'],'retained_limits':spec['LIMITS'],'H77_execution':False,'A15_execution':False,'authority_issued':False,'bootstrap_qualified':strategy['BOOTSTRAP_QUALIFIED'],'technical_trust_root_qualified':inventory['INDEPENDENT_QUALIFIED_EXECUTION_TRUST_ROOT_FOUND'],'nodes':graph['NODES'],'revised_edges':strategy['REVISED_GRAPH_EDGES']}
 ready=safety(state);negatives=[]
 mutants=[('gate assumed qualified','gate_qualified',True),('host inferred from documentation','host_qualified',True),('atomic creation called durable','atomic_is_durable',True),('service name treated as consumption','name_is_consumption',True),('duplicate admitted','duplicate_launch',True),('failure reopens','failure_reopens',True),('self-referential trust','circular_trust',True),('admin permission inferred','admin_permission_verified',True),('broader command','argv',state['argv']+['extra']),('broader resources','probe_limits',dict(state['probe_limits'],MAX_SERVICE_TASKS=99)),('H77 execution','H77_execution',True),('A15 execution','A15_execution',True),('premature authority','authority_issued',True),('design called qualified','bootstrap_qualified',True),('technical root assumed','technical_trust_root_qualified',True),('bootstrap again depends on host target','revised_edges',state['revised_edges']+[{'FROM':'BOOTSTRAP_MECHANISM','TO':'HOST_RESOURCE_ENFORCEMENT_QUALIFICATION'}])]
 for name,key,value in mutants:
  mutation=copy.deepcopy(state);mutation[key]=value
  try:safety(mutation)
  except AssertionError:negatives.append({'CONTROL':name,'RESULT':'REJECTED'})
  else:raise AssertionError('negative accepted: '+name)
 result={'READINESS':ready,'MINIMAL_CYCLIC_COMPONENT':cyclic[0],'REVISED_CYCLIC_COMPONENTS':[g for g in reach_components(graph['NODES'],strategy['REVISED_GRAPH_EDGES']) if len(g)>1],'BOOTSTRAP_CANDIDATES_EVALUATED':3,'PREFERRED_BOOTSTRAP_STRATEGY':strategy['PREFERRED_BOOTSTRAP_STRATEGY'],'PROPOSED_AUTHORITY_SUBJECT':sid,'LESSONS_REGISTER_VERIFIED':True,'LESSON_APPENDED':True,'LESSON_ID':'LL-11','OLD_EVENTS_PRESERVED':len(oldreg['EVENTS']),'NEW_EVENT_COUNT':len(reg['EVENTS']),'PREVIOUS_HEAD':oldreg['EVENTS'][-1]['EVENT_HASH'],'REGISTER_HEAD':previous,'LESSON_CONTENT_IDENTITY':lid,'NEGATIVES':negatives,'PROBES_TESTS_SERVICES_EXECUTED':0}
 result['SEMANTIC_IDENTITY']={'kind':'CONTENT_IDENTITY','namespace':'qualification-h88-independent-verification-v1','sha256':hashlib.sha256(canon(result)).hexdigest()};print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
