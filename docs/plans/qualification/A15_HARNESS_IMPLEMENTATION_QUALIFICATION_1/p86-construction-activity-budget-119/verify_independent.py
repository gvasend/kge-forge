"""119 independent static source/evidence/count ledger reconstruction; no target imports."""
import pathlib,json,hashlib,ast,copy,subprocess,sys,os
O=pathlib.Path(__file__).resolve().parent;R=O.parents[4];B=O.parent
PATHS=['adapter/qualification_bootstrap/systemd_pids_fixed_bridge.py','adapter/tests/test_systemd_pids_fixed_bridge.py']
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
a=read(O/'authenticated-input-manifest.json')
for p,h in a['PINS'].items():assert sha(R/p)==h
fresh=json.loads(subprocess.check_output([sys.executable,str(B/'p86-publication-amendment-issuance-115/verify_independent.py'),'EFFECTIVE'],cwd=str(R)))
assert fresh['RECONSTRUCTION']['AMENDMENT_EFFECTIVE'] and fresh['RECONSTRUCTION']['EFFECTIVENESS_REFERENCE_IDENTITY']['sha256']=='f39f040197fc3978f284b36f38a9c7e3445acfe1f78a69c9387db8f6bbe83993'
assert a['EXACT_PATHS']==PATHS and read(O/'two-file-scope.json')['EXACT_PATHS']==PATHS
src=read(O/'source-byte-ledger.json');observed={}
for p in src['PRECEDENTS']:
 path=R/p['SOURCE_PATH'];assert sha(path)==p['RAW_SHA256'] and len(path.read_bytes())==p['RAW_SOURCE_BYTES'];t=ast.parse(path.read_text());defs={x.name:x for x in t.body if isinstance(x,(ast.FunctionDef,ast.ClassDef))}
 for row in p['TOP_LEVEL_DEFINITIONS']:
  segment=ast.get_source_segment(path.read_text(),defs[row['NAME']]).encode();assert len(segment)==row['UTF8_SEGMENT_BYTES'] and hashlib.sha256(segment).hexdigest()==row['SOURCE_SEGMENT_SHA256']
 observed[p['SOURCE_PATH']]=p['RAW_SOURCE_BYTES']
assert src['COMPARATIVE_PAIR_BYTES']==observed['adapter/qualification_bootstrap/systemd_pids_once.py']+observed['adapter/tests/test_systemd_pids_bootstrap.py']==62517
for row in src['REQUIRED_ROLE_PRECEDENT_MAP']:assert sum(x['UTF8_SEGMENT_BYTES'] for x in row['SELECTED_DEFINITIONS'])==row['SUM_RAW_SEGMENT_BYTES']
assert src['MAX_TOTAL_SOURCE_BYTES']=='UNBOUND' and all(x['MAX_SOURCE_BYTES']=='UNBOUND' and x['MAX_WRITE_OPERATIONS']=='UNBOUND' and x['MAX_REVISIONS']=='UNBOUND' for x in src['PROPOSED_FILES'])
e=read(O/'evidence-publication-ledger.json');rawsum=0;canonsum=0
for p in e['HISTORICAL118_OBSERVATIONS']:
 path=R/p['PATH'];assert sha(path)==p['RAW_SHA256'] and len(path.read_bytes())==p['RAW_BYTES'];rawsum+=p['RAW_BYTES']
 if p['CANONICAL_JSON_BYTES'] is not None:assert len(enc(read(path)))==p['CANONICAL_JSON_BYTES'];canonsum+=p['CANONICAL_JSON_BYTES']
assert len(e['HISTORICAL118_OBSERVATIONS'])==24 and rawsum==e['HISTORICAL118_RAW_RETAINED_BYTES']==4332207 and canonsum==e['HISTORICAL118_CANONICAL_JSON_BYTES']==4195728
assert e['MAX_CONSTRUCTION_EVIDENCE_BYTES']=='UNBOUND' and not e['COMPLETE'] and len(e['CLASSES'])==8
schedule=read(O/'construction-work-unit-attempt-schedule.json');assert len(schedule['WORK_UNITS'])==schedule['MAX_DISTINCT_WORK_UNIT_STAGES']==6 and schedule['AUTOMATIC_RETRIES']==0 and not schedule['COMPLETE']
profile=read(O/'static-verifier-resource-profile.json');assert profile['SEEDS']==[0,1,7,101] and profile['FRESH_SEEDED_PROCESSES']==4 and profile['SOURCE_NOMINAL_PROCESS_LIFETIMES_PER_SEED']==9 and profile['SOURCE_NOMINAL_LIFETIMES_FOUR_SEEDS_PLUS_DRIVER']==1+4*9==37 and profile['SOURCE_NOMINAL_PEAK_FOUR_PARALLEL_CHAINS_PLUS_DRIVER']==1+4*6==25
for p in profile['EXACT_BINARY_OBSERVATIONS']:assert sha(pathlib.Path(p['PATH']))==p['RAW_SHA256']
for p in profile['PINNED_READERS']:assert sha(R/p['PATH'])==p['RAW_SHA256'];ast.parse((R/p['PATH']).read_text())
assert profile['EXACT_FUTURE_CONSTRUCTION_VERIFIER_IDENTITY'] is None and not profile['CURRENT_ENFORCEMENT_VERIFIED'] and profile['CPU_SECONDS_PER_PROCESS']=='UNBOUND'
ledger=read(O/'resource-derivation-ledger.json');assert not ledger['HARD_ALLOCATION_COMPLETE']
for row in ledger['FIELDS']:
 if row['SOURCE_IDENTITY'] is not None:assert sha(R/row['SOURCE_ARTIFACT'])==row['SOURCE_IDENTITY']['sha256']
 assert all(k in row for k in ['UNIT','DERIVATION_FORMULA','ASSUMPTIONS','BOUND_TYPE','ENFORCEMENT_OWNER','INDEPENDENT_CHECK','FAILURE_RULE'])
m=read(O/'phase-classification-matrix.json');old=read(B/'p86-construction-scope-closure-118/36-row-construction-entry-execution-matrix.json')['REQUIREMENTS'];assert len(m['REQUIREMENTS'])==len(old)==36
for x,y in zip(m['REQUIREMENTS'],old):assert x['REQUIREMENT_ID']==y['REQUIREMENT_ID'] and x['RETAINED_EARLIEST_PHASE']==y['PHASE'] and x['NO_PHASE_REASSIGNMENT']
auth=read(O/'authority-applicability.json');assert not auth['CONSTRUCTION_DECISION_READY'] and not auth['CONSTRUCTION_GRANT_ISSUED'] and not auth['CONSTRUCTION_ENTRY_READY']
g=read(O/'dependency-graph.json');adj={}
for x,y in g['EDGES']:adj.setdefault(x,[]).append(y)
def visit(n,active):
 assert n not in active
 for w in adj.get(n,[]):visit(w,active|{n})
for n in adj:visit(n,set())
reg=read(R/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');prev='0'*64
for event in reg['EVENTS']:
 assert event['PREVIOUS_EVENT_HASH']==prev
 assert hashlib.sha256(json.dumps({k:v for k,v in event.items() if k!='EVENT_HASH'},sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()==event['EVENT_HASH'];prev=event['EVENT_HASH']
assert prev=='885fd0eaceb15847201dfd058217682741fb43c255298713ccbc1e7251eec791';journalsha=sha(B/'campaign-budget.jsonl');assert journalsha=='3491e9003e1a016dbc4208e3963f8abea0f98c439dc892aa89a3811e73d528eb'
state={'paths':PATHS,'borrowed90':False,'borrowed94':False,'p86_cap_reused':False,'unbound_source_accepted':False,'unbound_evidence_accepted':False,'arbitrary_ceiling':False,'missing_enforcement_accepted':False,'per_process_as_aggregate':False,'unlimited_edits_accepted':False,'retry_reset':False,'missing_static_budget_accepted':False,'unbounded_errors_accepted':False,'real_launch_enabled':False,'future_result_required_for_construction':False,'safety_deferred':False,'construction_grant_effective':False,'historical_exclusions_missing':False,'cyclic_authority':False,'journal_sha256':journalsha,'construction_started':False}
def validate(x):
 assert x['paths']==PATHS,'changed source path';assert x['journal_sha256']==journalsha,'altered stopped journal'
 for k,v in x.items():
  if k not in ['paths','journal_sha256']:assert v is False,k
validate(state);neg=[]
for key in state:
 x=copy.deepcopy(state)
 if key=='paths':x[key]=[PATHS[0],'adapter/tests/test_systemd_pids_bootstrap.py']
 elif key=='journal_sha256':x[key]='0'*64
 else:x[key]=True
 try:validate(x)
 except AssertionError as err:neg.append({'CONTROL':key,'RESULT':'REJECTED','CAUSE':str(err)})
 else:raise AssertionError(key)
names=['authenticated-input-manifest.json','two-file-scope.json','construction-work-unit-attempt-schedule.json','source-byte-ledger.json','evidence-publication-ledger.json','static-verifier-resource-profile.json','construction-time-attempt-policy.json','resource-derivation-ledger.json','phase-classification-matrix.json','authority-applicability.json','dependency-graph.json','exact-remaining-gap-dossier.json','instruction-provenance.json']
s={'PINS':{n:sha(O/n) for n in names},'SOURCE_FILES':2,'PHASE_REQUIREMENTS':36,'WORK_UNIT_STAGES':6,'COMPARATIVE_SOURCE_PAIR_BYTES':62517,'OBSERVED118_RAW_EVIDENCE_BYTES':4332207,'OBSERVED118_CANONICAL_JSON_BYTES':4195728,'SOURCE_NOMINAL_METADATA_LIFETIMES':37,'SOURCE_NOMINAL_METADATA_PEAK':25,'HARD_CONSTRUCTION_ALLOCATION_COMPLETE':False,'CONSTRUCTION_DECISION_READY':False,'CONSTRUCTION_ENTRY_READY':False,'REAL_PROBE_BUDGET_FEASIBILITY':'UNDETERMINED','GRAPH_ACYCLIC':True,'LL11_HEAD':prev,'NEGATIVES':neg}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':s,'SEMANTIC_SHA256':hashlib.sha256(enc(s)).hexdigest()},sort_keys=True))
