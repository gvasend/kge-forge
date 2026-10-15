"""Independent metadata trust/authority qualification; no bootstrap/gate imports."""
import copy,hashlib,json,pathlib,subprocess,sys
OUT=pathlib.Path(__file__).resolve().parent;ROOT=pathlib.Path(__file__).resolve().parents[5]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def acyclic(nodes,edges):
 adj={n:[] for n in nodes};degree={n:0 for n in nodes}
 for e in edges:adj[e['FROM']].append(e['TO']);degree[e['TO']]+=1
 todo=sorted(n for n in nodes if degree[n]==0);seen=[]
 while todo:
  n=todo.pop(0);seen.append(n)
  for w in adj[n]:
   degree[w]-=1
   if degree[w]==0:todo.append(w);todo.sort()
 return len(seen)==len(nodes)
LIMITS={'MAX_LIVE_CHILDREN':2,'MAX_CHILD_LAUNCHES':16,'CHILD_CPU_SECONDS':5,'CHILD_WALL_SECONDS':10,'CHILD_ADDRESS_SPACE_BYTES':134217728,'CHILD_FILE_BYTES':65536,'CHILD_FDS':32,'CAMPAIGN_WALL_SECONDS':30,'CAMPAIGN_WRITTEN_BYTES':1048576,'AUTOMATIC_RETRIES':0}
PATHS=['adapter/qualification_bootstrap/systemd_pids_once.py','adapter/tests/test_systemd_pids_bootstrap.py']
TESTS=['B89-'+s for s in ['COMMAND_REJECTION','GRANT_REJECTION','FIRST_CONSUMPTION','DUPLICATE_CONSUMPTION','CONCURRENT_CLAIMS','PARTIAL_RECORD','CRASH_BEFORE_LAUNCH','CRASH_AFTER_CONSUMPTION','LAUNCH_FAILURE','UNKNOWN_COMPLETION','AUDIT_FAILURE','REVOCATION','RESOURCE_MISMATCH','ZERO_RETRIES']]
def assess(s):
 assert acyclic(s['nodes'],s['edges']),'circular foundation'
 assert not set(s['nodes'])&{'GATE_ACTIVE_QUALIFICATION','HOST_RESOURCE_ENFORCEMENT_QUALIFICATION','SYSTEM_LEVEL_PROBE','QUALIFIED_ONE_USE_LAUNCH','INDEPENDENT_EVIDENCE'},'original target prerequisite'
 assert s['exclusive_status']=='IMPLEMENTED_NOT_QUALIFIED' and s['generic_os_status']=='OBSERVED_ONLY','unsupported facility promotion'
 assert s['command_id'] is not None and s['argv']==s['retained_argv'],'command pin'
 assert s['issued_probe_grant'] is None and s['construction_grant'] is None,'unissued effective grant'
 assert s['duplicate_allowed'] is False and s['crash_reopens'] is False and s['unknown_reopens'] is False,'once rule'
 assert s['file_fsync'] and s['directory_fsync'] and s['readonly_confirm'],'durability layer missing'
 assert s['arbitrary_commands'] is False and s['actual_permissions_verified'] is False,'unrestricted/assumed launch'
 assert s['source_paths']==PATHS and s['limits']==LIMITS and s['tests']==TESTS,'unbounded scope'
 assert s['no_systemd'] and s['no_sudo'] and s['no_H77'] and s['no_A15'] and s['no_BWRAP'],'effects included'
 assert s['issued_authority'] is None and s['bootstrap_behavior_qualified'] is False and s['active_ready'] is False,'premature issuance/qualification'
 assert s['explicit_narrow_trust_adoption'] and s['all_unknown_entries_deny'],'qualification trust not explicit'
 return {'RESULT':'PASS','RESULT_BOUNDARY':'independently qualified conditional construction/inert-test subject only','PACKAGE_88_CYCLE_AUTHENTICATED':'YES','LL_11_PRESERVED':'YES','TRUST_ROOT_INVENTORY_COMPLETE':'YES','BOOTSTRAP_TRUST_GRAPH_ACYCLIC':'YES','INDEPENDENT_TRUST_CONTRACT_COMPLETE':'YES','COORDINATOR_SPEC_COMPLETE':'YES','ONE_ATTEMPT_CONTRACT_COMPLETE':'YES','CONSTRUCTION_SCOPE_COMPLETE':'YES','INERT_TEST_SCOPE_COMPLETE':'YES','RESOURCE_BOUNDARY_COMPLETE':'YES','BOOTSTRAP_CONSTRUCTION_DECISION_READY':'YES','ACTIVE_INERT_TEST_READY':'NO','BOOTSTRAP_MECHANISM_QUALIFIED':'NO'}
def main():
 old=OUT.parent/'qualification-bootstrap-88';idx=read(old/'evidence-index.json')
 for p,h in {**idx['FILES'],**idx['CURRENT_LESSONS_REGISTER_PINS']}.items():assert sha(ROOT/p)==h
 graph88=read(old/'dependency-cycle-graph.json');scc88=read(old/'minimal-cyclic-component.json');assert len(scc88['MINIMAL_CYCLIC_COMPONENT'])==5
 # Independent transitive reachability confirms original SCC and replacement.
 def components(nodes,edges):
  adj={n:set() for n in nodes}
  for e in edges:adj[e['FROM']].add(e['TO'])
  reach={}
  for n in nodes:
   seen={n};todo=[n]
   while todo:
    v=todo.pop()
    for w in adj[v]-seen:seen.add(w);todo.append(w)
   reach[n]=seen
  return {tuple(sorted(w for w in nodes if w in reach[n] and n in reach[w])) for n in nodes}
 cs=[list(c) for c in components(graph88['NODES'],graph88['EDGES']) if len(c)>1];assert sorted(cs)==[scc88['MINIMAL_CYCLIC_COMPONENT']]
 strategy88=read(old/'minimum-cycle-breaking-strategy.json');assert not any(len(c)>1 for c in components(graph88['NODES'],strategy88['REVISED_GRAPH_EDGES']))
 inv=read(OUT/'trust-root-inventory.json');inventory={r['CAPABILITY_ID']:r for r in inv['ROOTS']};assert len(inventory)==12 and inv['QUALIFIED_COMPLETE_BOOTSTRAP_EXECUTOR'] is False
 for r in inv['ROOTS']:
  assert r['CURRENT_STATUS'] in ['INDEPENDENTLY_QUALIFIED','IMPLEMENTED_NOT_QUALIFIED','OBSERVED_ONLY','PROPOSED','UNDETERMINED']
  for p in r['EXISTING_QUALIFICATION_EVIDENCE']:assert sha(ROOT/p['path'])==p['raw_sha256']
  if 'path' in r['EXACT_IDENTITY']:assert sha(ROOT/r['EXACT_IDENTITY']['path'])==r['EXACT_IDENTITY']['raw_sha256']
 charter=json.loads(subprocess.check_output([sys.executable,'docs/plans/qualification/KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_ADOPTION_66/reader.py'],cwd=str(ROOT),text=True));assert charter['CHARTER_EFFECTIVE'] and [x['STATE'] for x in charter['ORDERED_LIFECYCLE']]==['DRAFT','REVIEWED','APPROVED','EFFECTIVE']
 subject=read(OUT/'proposed-construction-test-authority-subject.json');content=dict(subject);sid=content.pop('CONTENT_IDENTITY');assert hashlib.sha256(canon(content)).hexdigest()==sid['sha256']
 assert subject['EFFECTIVE_CHARTER']==charter['CHARTER_CONTENT_IDENTITY'] and subject['EFFECTIVE_LIFECYCLE']==charter['ORDERED_LIFECYCLE'][-1]['EVIDENCE_IDENTITY']
 for p in subject['CONTRACT_PINS'].values():assert sha(ROOT/p['path'])==p['raw_sha256']
 spec=read(OUT/'command-specific-coordinator-specification.json');body=dict(spec);specid=body.pop('COORDINATOR_IDENTITY');assert hashlib.sha256(canon(body)).hexdigest()==specid['sha256']
 retained=read(OUT.parent/'system-process-enforcement-86/transient-service-specification.json');assert spec['EXACT_COMMAND_ARGUMENT_VECTOR']==retained['EXACT_COMMAND_ARGV'] and spec['EXECUTABLE_PINS']==retained['EXECUTABLE_PINS']
 assert spec['SOURCE_CODE_IDENTITY'] is None and spec['APPROVED_PROBE_SUBJECT']['ACTUAL_LATER_APPROVAL'] is None
 env=read(OUT/'resource-and-environment-contract.json');tests=read(OUT/'inert-synthetic-qualification-specification.json');assert tests['EXACT_TEST_COUNT']==14 and tests['EXPECTED_HELPER_LAUNCHES']==10<=16 and tests['ACTIVE_CAMPAIGN_SEED']==0
 for test in tests['TESTS']:
  b=dict(test);i=b.pop('EXPECTED_OUTPUT_SPEC_IDENTITY');assert hashlib.sha256(canon(b)).hexdigest()==i['sha256'] and test['EXPECTED_RETRY_COUNT']==0
 once=read(OUT/'one-attempt-consumption-contract.json');assert once['MAX_LAUNCH_ATTEMPTS']==1 and once['ACTUAL_GRANT_KEY'] is None and once['POWER_LOSS_DURABILITY_CLAIMED'] is False
 ordered=once['REQUIRED_ORDER'];assert 'file fsync' in ordered and 'directory fsync' in ordered
 crash=read(OUT/'crash-concurrency-matrix.json');assert len(crash['ROWS'])==11 and all(row['RETRY_PERMISSION'] is False for row in crash['ROWS'])
 entry=read(OUT/'phase-and-entry-contract.json');trust=read(OUT/'independent-trust-contract.json');g=read(OUT/'acyclic-trust-dependency-graph.json');assert env['ENVIRONMENT']['ACTUAL_ENFORCEMENT_VERIFIED'] is False and env['ENVIRONMENT']['REQUIRES_PACKAGE86_PIDS_RESULT'] is False
 assert not any((ROOT/p).exists() for p in PATHS),'source already created/conflicting'
 dossier=read(OUT/'unselected-authorization-dossier.json');assert dossier['DECISION_READY'] and dossier['SELECTION'] is None and dossier['SUBJECT_IDENTITY']==sid and sha(ROOT/dossier['SUBJECT_PIN']['path'])==dossier['SUBJECT_PIN']['raw_sha256'];assert [o['OPTION_ID'] for o in dossier['OPTIONS']]==['AUTHORIZE_MINIMAL_H77_02_BOOTSTRAP_CONSTRUCTION_INERT_TEST','DECLINE_MINIMAL_H77_02_BOOTSTRAP_CONSTRUCTION_INERT_TEST'] and all(o['SUBJECT_IDENTITY']==sid for o in dossier['OPTIONS'])
 reg=read(ROOT/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');head='0'*64
 for e in reg['EVENTS']:
  b={k:v for k,v in e.items() if k!='EVENT_HASH'};assert e['PREVIOUS_EVENT_HASH']==head and hashlib.sha256(json.dumps(b,sort_keys=True,separators=(',',':')).encode()).hexdigest()==e['EVENT_HASH'];head=e['EVENT_HASH']
 assert reg['EVENTS'][-1]['LESSON']['LESSON_ID']=='LL-11' and head=='885fd0eaceb15847201dfd058217682741fb43c255298713ccbc1e7251eec791'
 state={'nodes':g['NODES'],'edges':g['EDGES'],'exclusive_status':inventory['EXCLUSIVE_RESERVATION']['CURRENT_STATUS'],'generic_os_status':inventory['PROCESS_CREATION']['CURRENT_STATUS'],'command_id':spec['EXACT_COMMAND_IDENTITY'],'argv':spec['EXACT_COMMAND_ARGUMENT_VECTOR'],'retained_argv':retained['EXACT_COMMAND_ARGV'],'issued_probe_grant':spec['ISSUED_GRANT_REFERENCE'],'construction_grant':subject['ISSUED_GRANT_IDENTITY'],'duplicate_allowed':once['DUPLICATE_CLAIM_ALLOWED'],'crash_reopens':once['CRASH_REOPENS_AUTHORITY'],'unknown_reopens':once['UNKNOWN_OUTCOME_REOPENS_AUTHORITY'],'file_fsync':'file fsync' in ordered,'directory_fsync':'directory fsync' in ordered,'readonly_confirm':True,'arbitrary_commands':False,'actual_permissions_verified':env['ENVIRONMENT']['ACTUAL_ENFORCEMENT_VERIFIED'],'source_paths':subject['EXACT_SOURCE_PATHS'],'limits':subject['RESOURCE_LIMITS'],'tests':subject['EXACT_SYNTHETIC_TESTS'],'no_systemd':subject['NO_SYSTEMD_EXECUTION'],'no_sudo':subject['NO_SUDO_EXECUTION'],'no_H77':subject['NO_H77_02_PROBE'],'no_A15':subject['NO_A15_EXECUTION'],'no_BWRAP':subject['NO_BWRAP_EXECUTION'],'issued_authority':subject['ISSUED_GRANT_IDENTITY'],'bootstrap_behavior_qualified':subject['MECHANISM_ALREADY_QUALIFIED'],'active_ready':entry['ACTIVE_READY'],'explicit_narrow_trust_adoption':'explicit adoption of narrow trusted-fixed-program inert bootstrap assurance contract' in subject['MANDATES'],'all_unknown_entries_deny':entry['FUTURE_ENTRY_NOT_FAKE_PASS']}
 ready=assess(state);neg=[]
 mutations=[('circular trust','edges',state['edges']+[{'FROM':'QUALIFIED_DOCUMENTARY_GOVERNANCE','TO':'CONSTRUCTION_DECISION'}]),('unqualified primitive promoted','exclusive_status','INDEPENDENTLY_QUALIFIED'),('missing command pin','command_id',None),('unissued probe grant effective','issued_probe_grant',{'effective':True}),('duplicate accepted','duplicate_allowed',True),('missing file barrier','file_fsync',False),('missing directory barrier','directory_fsync',False),('crash reopens','crash_reopens',True),('unknown reopens','unknown_reopens',True),('arbitrary launch','arbitrary_commands',True),('unknown permission verified','actual_permissions_verified',True),('unbounded resources','limits',dict(LIMITS,MAX_LIVE_CHILDREN=999)),('unauthorized source creation','source_paths',PATHS+['adapter/extra.py']),('systemd included','no_systemd',False),('sudo included','no_sudo',False),('Bwrap included','no_BWRAP',False),('H77 included','no_H77',False),('A15 included','no_A15',False),('premature issuance','issued_authority',{'issued':True}),('target qualification as own entry','nodes',state['nodes']+['HOST_RESOURCE_ENFORCEMENT_QUALIFICATION'])]
 for name,key,val in mutations:
  m=copy.deepcopy(state);m[key]=val
  try:assess(m)
  except AssertionError:neg.append({'CONTROL':name,'RESULT':'REJECTED'})
  else:raise AssertionError('negative accepted '+name)
 result={'READINESS':ready,'CONSTRUCTION_SUBJECT_IDENTITY':sid,'COORDINATOR_SPEC_IDENTITY':specid,'BOOTSTRAP_TRUST_ROOT_CLASSES':{k:v['CURRENT_STATUS'] for k,v in inventory.items()},'ORIGINAL_CYCLIC_COMPONENT':cs[0],'TRUST_GRAPH_ACYCLIC':True,'LL11_HEAD':head,'NEGATIVES':neg,'BOOTSTRAP_SOURCE_FILES_CREATED':0,'BOOTSTRAP_TESTS_EXECUTED':0,'PROBES_OR_SERVICES_EXECUTED':0}
 result['SEMANTIC_IDENTITY']={'kind':'CONTENT_IDENTITY','namespace':'qualification-h89-independent-verification-v1','sha256':hashlib.sha256(canon(result)).hexdigest()};print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
