"""118 construction-only static contract verification. No target import/execution."""
import pathlib,json,hashlib,copy,subprocess,sys,os
O=pathlib.Path(__file__).resolve().parent;R=O.parents[4];B=O.parent
PATHS=['adapter/qualification_bootstrap/systemd_pids_fixed_bridge.py','adapter/tests/test_systemd_pids_fixed_bridge.py']
REF={'kind':'CONTENT_IDENTITY','namespace':'qualification-p86-publication-amendment-effectiveness-reference-v1','sha256':'f39f040197fc3978f284b36f38a9c7e3445acfe1f78a69c9387db8f6bbe83993'}
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
a=read(O/'authenticated-baseline.json')
for p,h in a['PINS'].items():assert sha(R/p)==h
fresh=json.loads(subprocess.check_output([sys.executable,str(B/'p86-publication-amendment-issuance-115/verify_independent.py'),'EFFECTIVE'],cwd=str(R)))
assert fresh['RECONSTRUCTION']['AMENDMENT_EFFECTIVE'] and fresh['RECONSTRUCTION']['EFFECTIVENESS_REFERENCE_IDENTITY']==REF
old117=read(B/'p86-producer-event-closure-117/four-seed-reconstruction.json');core=old117['FRESH_PROCESSES'][0]['RECONSTRUCTION'];assert hashlib.sha256(enc(core)).hexdigest()==old117['FRESH_PROCESSES'][0]['SEMANTIC_SHA256'] and len({x['SEMANTIC_SHA256'] for x in old117['FRESH_PROCESSES']})==1
for n,h in core['PINS'].items():assert sha(B/'p86-producer-event-closure-117'/n)==h
assert core['PHASE_REQUIREMENTS']==36 and core['CANDIDATE_RECORD_MAXIMA']['CONSUMPTION_CLAIM']==920 and core['CANDIDATE_RECORD_MAXIMA']['SERVICE_METADATA']==996 and core['BUDGET_FEASIBILITY']=='UNDETERMINED'
m=read(O/'36-row-construction-entry-execution-matrix.json');old=read(B/'p86-producer-event-closure-117/entry-versus-execution-scope-matrix.json')['REQUIREMENTS'];assert len(m['REQUIREMENTS'])==len(old)==36 and not m['PHASE_REASSIGNMENTS'] and not m['CONTRADICTORY_ASSIGNMENTS']
allowed={'CONSTRUCTION_DECISION_PREREQUISITE','CONSTRUCTION_ENTRY_PREDICATE','INERT_DECISION_OR_ENTRY_PREDICATE','REAL_PROBE_DECISION_OR_ENTRY_PREDICATE','EXECUTION_PRODUCED_OBSERVATION','POST_EXECUTION_QUALIFICATION','UNDETERMINED'}
for i,(x,y) in enumerate(zip(m['REQUIREMENTS'],old)):
 assert x['REQUIREMENT_ID']==y['REQUIREMENT_ID'] and x['PHASE']==y['APPLICABLE_PHASE'] and x['CLASS'] in allowed and not x['PHASE_CHANGED_FROM117'] and not x['CONTRADICTION']
 assert x['EXACT_CLAUSE'][1]['EXACT_TEXT']==y['REQUIRED_EVIDENCE'] and x['EXACT_CLAUSE'][1]['JSON_POINTER']=='/REQUIREMENTS/'+str(i)+'/REQUIRED_EVIDENCE'
 if y['APPLICABLE_PHASE']=='AUTHORIZED_EXECUTION':assert x['CLASS']=='EXECUTION_PRODUCED_OBSERVATION'
 if y['APPLICABLE_PHASE'].startswith('POST_'):assert x['CLASS']=='POST_EXECUTION_QUALIFICATION'
bound=read(O/'exact-two-file-construction-boundary.json');assert bound['EXACT_SOURCE_ALLOWLIST']==PATHS and all(x['REAL_SYSTEMD_LAUNCH_DISABLED'] and x['NO_TEST_AUTHORITY'] and x['CURRENT_RAW_IDENTITY'] is None for x in bound['FILES'])
resources=read(O/'construction-resource-contract.json');limits=resources['LIMITS'];assert limits['MAX_FILES_CHANGED']==2 and limits['NO_AUTOMATIC_RETRY'] and all(limits[k] is None for k in ['MAX_NEW_SOURCE_BYTES','MAX_EVIDENCE_BYTES','MAX_WORK_UNITS','MAX_ATTEMPTS','TIME_BOUND','MEMORY_BOUND_IF_BINDING']) and not resources['COMPLETE']
reuse=read(O/'construction-resource-evidence-reuse.json')
for x in reuse['EFFECTIVE_ORIGINAL_GRANTS']:
 assert not x['APPLICABILITY_TO_NEW_TWO_FILES'] and x['PERMITTED_PATHS']!=PATHS
 for k in ['REFERENCE_PIN','RECORD_PIN']:assert sha(R/x[k]['path'])==x[k]['raw_sha256']
pub=read(O/'publication-construction-applicability.json');assert pub['MAX_OBSERVER_PUBLISHED_BYTES']==65536 and not pub['CONSTRUCTION_ENTRY_BYTE_CEILING'] and pub['IMPLEMENTATION_INVARIANT'] and pub['REAL_PROBE_DECISION_ENTRY_GATE'] and not pub['INERT_AUTOMATIC_BUDGET_APPLICABILITY']
assert pub['EXACT_RULE_ACCOUNTING_INTERVAL']==read(O/'authority-clause-catalog.json')['EXACT_EFFECTIVE_PUBLICATION_RULE']['ACCOUNTING_INTERVAL']
tests=read(O/'twelve-inert-property-mapping.json');orig=read(B/'fixed-command-bridge-102/minimal-inert-qualification-specification.json');assert len(tests['TESTS'])==12 and [x['TEST_ID'] for x in tests['TESTS']]==[x['TEST_ID'] for x in orig['TESTS']] and all(x['STATUS']=='NOT_EXECUTED' for x in tests['TESTS']) and not tests['INERT_TEST_AUTHORIZED']
draft=read(O/'construction-only-contract-draft.json');assert hashlib.sha256(enc(draft['CONTENT'])).hexdigest()==draft['IDENTITY']['sha256'];d=draft['CONTENT'];assert d['STATUS']=='INCOMPLETE_NOT_AUTHORIZATION_SUBJECT' and not d['DECISION_READY'] and d['SELECTION'] is None and d['CONSTRUCTION_RESOURCE_LIMITS']==limits
assert read(O/'static-source-acceptance-contract.json')['STATIC_ACCEPTANCE_CONTRACT_COMPLETE'] and not read(O/'readiness-assessment.json')['CONSTRUCTION_DECISION_READY']
g=read(O/'qualification-dependency-graph.json');adj={}
for x,y in g['EDGES']:adj.setdefault(x,[]).append(y)
def visit(n,active):
 assert n not in active
 for w in adj.get(n,[]):visit(w,active|{n})
for n in adj:visit(n,set())
reg=read(R/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');prev='0'*64
for e in reg['EVENTS']:
 assert e['PREVIOUS_EVENT_HASH']==prev
 assert hashlib.sha256(json.dumps({k:v for k,v in e.items() if k!='EVENT_HASH'},sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()==e['EVENT_HASH'];prev=e['EVENT_HASH']
assert prev=='885fd0eaceb15847201dfd058217682741fb43c255298713ccbc1e7251eec791';assert sha(B/'campaign-budget.jsonl')=='3491e9003e1a016dbc4208e3963f8abea0f98c439dc892aa89a3811e73d528eb'
# Mutations of the current incomplete construction-only model, not target runtime tests.
state={'subject_identity':draft['IDENTITY'],'paths':PATHS,'extra_file':False,'real_systemd_enabled':False,'construction_as_test_authority':False,'old90_reused':False,'old94_reused':False,'fresh_guard_required':True,'new_source_byte_limit':None,'future_probe_result_required_for_construction':False,'binding_safety_deferred':False,'permanent_anchor':True,'duplicate_launch_admitted':False,'observer_self_report_independent':False,'budget':'UNDETERMINED','amendment_reinterpreted':False,'history_changed':False,'h77_permission':False,'a15_permission':False,'graph_cycle_hidden':False}
def valid(x):
 assert x['subject_identity']==draft['IDENTITY'],'wrong subject identity';assert x['paths']==PATHS,'altered source path';assert x['fresh_guard_required'],'missing fresh guard';assert x['permanent_anchor'],'missing permanent anchor';assert x['new_source_byte_limit'] is None,'arbitrary ungrounded numeric limit';assert x['budget']=='UNDETERMINED','unclosed budget promoted'
 for k,v in x.items():
  if k not in ['subject_identity','paths','fresh_guard_required','permanent_anchor','new_source_byte_limit','budget']:assert v is False,k
valid(state);neg=[]
for k in state:
 x=copy.deepcopy(state)
 if k=='subject_identity':x[k]={}
 elif k=='paths':x[k]=['adapter/qualification_bootstrap/systemd_pids_once.py',PATHS[1]]
 elif k in ['fresh_guard_required','permanent_anchor']:x[k]=False
 elif k=='new_source_byte_limit':x[k]=65536
 elif k=='budget':x[k]='PASS'
 else:x[k]=True
 try:valid(x)
 except AssertionError as e:neg.append({'CONTROL':k,'RESULT':'REJECTED','CAUSE':str(e)})
 else:raise AssertionError(k)
names=['authenticated-baseline.json','authority-clause-catalog.json','36-row-construction-entry-execution-matrix.json','exact-two-file-construction-boundary.json','construction-resource-evidence-reuse.json','construction-resource-contract.json','static-source-acceptance-contract.json','principal-store-phase-contract.json','publication-construction-applicability.json','twelve-inert-property-mapping.json','construction-entry-guard-contract.json','construction-only-contract-draft.json','qualification-dependency-graph.json','remaining-gap-dossier.json','readiness-assessment.json']
s={'PINS':{n:sha(O/n) for n in names},'EFFECTIVE_AMENDMENT_IDENTITY':REF,'PHASE_REQUIREMENTS':36,'MATRIX_COMPLETE':True,'EXACT_SOURCE_PATHS':PATHS,'CONSTRUCTION_RESOURCE_CONTRACT_COMPLETE':False,'STATIC_ACCEPTANCE_COMPLETE':True,'CONSTRUCTION_DECISION_READY':False,'CONSTRUCTION_ENTRY_READY':False,'INERT_DECISION_READY':False,'REAL_PROBE_DECISION_READY':False,'BUDGET_FEASIBILITY':'UNDETERMINED','GRAPH_ACYCLIC':True,'LL11_HEAD':prev,'NEGATIVES':neg}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':s,'SEMANTIC_SHA256':hashlib.sha256(enc(s)).hexdigest()},sort_keys=True))
