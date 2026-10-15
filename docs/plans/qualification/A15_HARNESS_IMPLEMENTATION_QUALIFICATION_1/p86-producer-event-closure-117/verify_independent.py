"""117 independent static JSON/AST/phase verification. No target module import."""
import pathlib,json,hashlib,ast,copy,subprocess,sys,os
O=pathlib.Path(__file__).resolve().parent;R=O.parents[4];B=O.parent
REF={'kind':'CONTENT_IDENTITY','namespace':'qualification-p86-publication-amendment-effectiveness-reference-v1','sha256':'f39f040197fc3978f284b36f38a9c7e3445acfe1f78a69c9387db8f6bbe83993'}
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
a=read(O/'authenticated-baseline.json')
for p,h in a['PINS'].items():assert sha(R/p)==h
current=json.loads(subprocess.check_output([sys.executable,str(B/'p86-publication-amendment-issuance-115/verify_independent.py'),'EFFECTIVE'],cwd=str(R)))
assert current['RECONSTRUCTION']['AMENDMENT_EFFECTIVE'] and current['RECONSTRUCTION']['EFFECTIVENESS_REFERENCE_IDENTITY']==REF
ref=read(R/a['EFFECTIVE_REFERENCE_PIN']['path']);assert ref['IDENTITY']==REF and sha(R/a['EFFECTIVE_REFERENCE_PIN']['path'])==a['EFFECTIVE_REFERENCE_PIN']['raw_sha256'];record=read(R/ref['CONTENT']['ISSUANCE_RECORD_PIN']['path']);assert a['EXACT_EFFECTIVE_RULE']==record['CONTENT']['ADOPTED_CONTENT']['PROPOSED_NORMATIVE_RULE']
# Reconstruct immutable116 proof prefix, not obsolete source-absence guards after future authorized construction.
old=read(B/'p86-publication-budget-recalculation-116/four-seed-reconstruction.json');core=old['FRESH_PROCESSES'][0]['RECONSTRUCTION'];assert hashlib.sha256(enc(core)).hexdigest()==old['FRESH_PROCESSES'][0]['SEMANTIC_SHA256'];assert len({x['SEMANTIC_SHA256'] for x in old['FRESH_PROCESSES']})==1
for n,h in core['PINS'].items():assert sha(B/'p86-publication-budget-recalculation-116'/n)==h
c=read(O/'unchanged-command-and-accounting.json');assert hashlib.sha256(enc(c['EXACT_ARGV'])).hexdigest()==c['COMMAND_IDENTITY']['sha256']=='e628c8664ea72357963dc58dddee934c28cad3ab5c84450656a6595e6910fb50';assert hashlib.sha256(c['EXACT_ARGV'][-1].encode()).hexdigest()==c['PAYLOAD_RAW_SHA256'];tree=ast.parse(c['EXACT_ARGV'][-1]);emit=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='emit');assert 8192 in [x.value for x in ast.walk(emit) if isinstance(x,ast.Constant)] and any(isinstance(x,ast.While) for x in ast.walk(emit));assert 3*sum(range(1,8193))==c['CONSERVATIVE_API_SUBMISSION_BOUND']==100675584
candidate=read(O/'prospective-canonical-record-contracts.json');bounds={}
for w in candidate['CONTRACTS']:
 x=w['CONTENT'];assert hashlib.sha256(enc(x)).hexdigest()==w['IDENTITY']['sha256'];assert len(enc(x['MAXIMAL_ENCODING_INSTANCE']))==x['MAX_SERIALIZED_BYTES'];assert x['MAX_FIELD_BYTES']['SHA256_HEX_FIELDS']==64 and x['MAX_FIELD_BYTES']['UINT64_DECIMAL_FIELDS']==20 and not x['IMPLEMENTED'];bounds[x['MAXIMAL_ENCODING_INSTANCE']['type']]=x['MAX_SERIALIZED_BYTES']
crit=read(O/'authenticated-critical-records.json');assert sha(R/crit['SOURCE_PIN']['path'])==crit['SOURCE_PIN']['raw_sha256']
for x in crit['CONTENT']['SCHEMAS']:assert len(enc(x['MAXIMAL_ENCODING_INSTANCE']))==x['MAX_RECORD_BYTES']
inv=read(O/'complete-producer-inventory.json');ids=[x['PRODUCER_ID'] for x in inv['PRODUCERS']];assert len(ids)==15 and len(set(ids))==15 and set(x['EFFECTIVE_PRODUCER_CLASS'] for x in inv['PRODUCERS'])==set(a['EXACT_EFFECTIVE_RULE']['COUNTED_PRODUCERS'])
copycontract=read(O/'payload-copy-and-stderr-contract.json');assert copycontract['MAX_CAPTURED_COPIES'] is None and not copycontract['COPY_SCHEDULE_COMPLETE'] and not copycontract['STDERR_BOUND_COMPLETE']
events=read(O/'denial-and-secondary-cardinality.json');assert events['INDIVIDUAL_DENIAL_RECORDS'] is None and not events['DUPLICATE_DENIAL_BOUND_COMPLETE'] and not events['SECONDARY_FAILURE_BOUND_COMPLETE'] and all(x['MAX_SECONDARY_EVENTS'] is None for x in events['SECONDARY_FAILURES'])
allocation=read(O/'reserve-and-publication-paths.json');assert allocation['BUDGET_FEASIBILITY']=='UNDETERMINED' and allocation['MAXIMUM_MODEL']['TOTAL_PROTECTED_ALLOCATION'] is None
scope=read(O/'entry-versus-execution-scope-matrix.json');sr={x['REQUIREMENT_ID']:x for x in scope['REQUIREMENTS']};assert len(sr)==36 and scope['MATRIX_COMPLETE']
for x in scope['REQUIREMENTS']:
 assert all(k in x for k in ['AUTHORITY_SOURCE','APPLICABLE_PHASE','ENTRY_OR_EXECUTION_CLASS','REQUIRED_EVIDENCE','CURRENT_STATUS','ENFORCEMENT_OWNER','FAILURE_RULE','DEPENDENCY_IDENTITIES','NEXT_ACTION'])
for rid in ['ACTUAL_SERVICE_CGROUP','OBSERVED_KERNEL_PIDS_MAX','ACTUAL_EXIT','ACTUAL_RESOURCE_CONSUMPTION','ACTUAL_PUBLICATION_CHARGES','ACTUAL_FAILURE_EVENTS','ACTUAL_DURABILITY']:assert sr['P117-'+rid]['ENTRY_OR_EXECUTION_CLASS']=='EXECUTION_OBSERVATION_REQUIRED'
for rid in ['CONSTRUCTION_RESULTS','INERT_RESULTS','FINAL_QUALIFICATION']:assert sr['P117-'+rid]['ENTRY_OR_EXECUTION_CLASS']=='POST_EXECUTION_QUALIFICATION_REQUIRED'
for rid in ['INERT_RESOURCE_ENFORCEMENT','REAL_SAFETY_BOUNDARY','REAL_ADMIN_PERMISSION']:assert sr['P117-'+rid]['ENTRY_OR_EXECUTION_CLASS']=='ENTRY_PREDICATE_PENDING'
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
# Actual static model mutations, not running the future bridge or service.
state={'amendment':REF,'command':c['COMMAND_IDENTITY']['sha256'],'ceiling':65536,'producers':ids,'copy_accounted':True,'hash_field_bound':64,'stderr_unbounded_accepted':False,'duplicate_requests_assumed_finite':False,'overflow_silent':False,'recursive_errors':False,'first_cause_overwritten':False,'reserve':None,'exclusive_double_count':False,'concurrent_error_omitted':False,'submission_as_publication':False,'transfer_as_durability':False,'static_as_enforced':False,'budget_feasible':False,'construction_authority':False,'inert_authority':False,'probe_authority':False,'construction_results_required_before_authority':False,'inert_results_required_before_authority':False,'probe_results_required_before_authority':False,'entry_safety_deferred':False,'unqualified_launcher_accepted':False,'unqualified_observer_accepted':False,'history_modification_allowed':False,'h77_execution':False,'a15_execution':False}
def validate(s):
 assert s['amendment']==REF,'wrong amendment';assert s['command']==c['COMMAND_IDENTITY']['sha256'],'wrong command';assert s['ceiling']==65536,'raised ceiling';assert s['producers']==ids,'omitted producer';assert s['copy_accounted'],'omitted copy';assert s['hash_field_bound']==64,'unbounded field';assert s['reserve'] is None,'arbitrary reserve'
 for k,v in s.items():
  if k not in ['amendment','command','ceiling','producers','copy_accounted','hash_field_bound','reserve']:assert v is False,k
validate(state);neg=[]
for k in state:
 s=copy.deepcopy(state)
 if k=='amendment':s[k]={}
 elif k=='command':s[k]='wrong'
 elif k=='ceiling':s[k]=65537
 elif k=='producers':s[k]=ids[:-1]
 elif k=='copy_accounted':s[k]=False
 elif k=='hash_field_bound':s[k]=None
 elif k=='reserve':s[k]=1024
 else:s[k]=True
 try:validate(s)
 except AssertionError as e:neg.append({'CONTROL':k,'RESULT':'REJECTED','CAUSE':str(e)})
 else:raise AssertionError(k)
names=['authenticated-baseline.json','unchanged-command-and-accounting.json','prospective-canonical-record-contracts.json','authenticated-critical-records.json','complete-producer-inventory.json','payload-copy-and-stderr-contract.json','denial-and-secondary-cardinality.json','failure-lifecycle-model.json','reserve-and-publication-paths.json','enforcement-and-minimal-design-change-assessment.json','entry-versus-execution-scope-matrix.json','qualification-dependency-graph.json','construction-readiness-assessment.json','remaining-gap-dossier.json']
semantic={'PINS':{n:sha(O/n) for n in names},'EFFECTIVE_AMENDMENT_IDENTITY':REF,'COMMAND_IDENTITY':c['COMMAND_IDENTITY'],'CANDIDATE_RECORD_MAXIMA':bounds,'PRODUCERS':15,'PHASE_REQUIREMENTS':36,'ENTRY_EXECUTION_SCOPE_MATRIX_COMPLETE':True,'ENTRY_EXECUTION_DEPENDENCY_CYCLE':False,'GRAPH_ACYCLIC':True,'PUBLICATION_BUDGET_COMPLETE':False,'BUDGET_FEASIBILITY':'UNDETERMINED','CONSTRUCTION_DECISION_READY':False,'CONSTRUCTION_ENTRY_READY':False,'INERT_QUALIFICATION_DECISION_READY':False,'INERT_QUALIFICATION_ENTRY_READY':False,'REAL_PROBE_DECISION_READY':False,'REAL_PROBE_ENTRY_READY':False,'POST_EXECUTION_QUALIFICATION_COMPLETE':False,'LL11_HEAD':prev,'NEGATIVES':neg}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':semantic,'SEMANTIC_SHA256':hashlib.sha256(enc(semantic)).hexdigest()},sort_keys=True))
