"""116 static arithmetic/JSON reconstruction, no target imports or execution."""
import pathlib,json,hashlib,ast,copy,subprocess,sys,os
O=pathlib.Path(__file__).resolve().parent;R=O.parents[4];B=O.parent
EXPECTED_REF={'kind':'CONTENT_IDENTITY','namespace':'qualification-p86-publication-amendment-effectiveness-reference-v1','sha256':'f39f040197fc3978f284b36f38a9c7e3445acfe1f78a69c9387db8f6bbe83993'}
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
a=read(O/'effective-amendment-authentication.json')
for p,h in a['PINS'].items():assert sha(R/p)==h
# Fresh current-status check; parent reconstruction is documentary only.
current=json.loads(subprocess.check_output([sys.executable,str(B/'p86-publication-amendment-issuance-115/verify_independent.py'),'EFFECTIVE'],cwd=str(R)))
assert current['RECONSTRUCTION']['AMENDMENT_EFFECTIVE'] and current['RECONSTRUCTION']['EFFECTIVENESS_REFERENCE_IDENTITY']==EXPECTED_REF
p=a['EFFECTIVENESS_REFERENCE_PIN'];assert sha(R/p['path'])==p['raw_sha256'];ref=read(R/p['path']);assert ref['IDENTITY']==EXPECTED_REF and hashlib.sha256(enc(ref['CONTENT'])).hexdigest()==EXPECTED_REF['sha256']
record=read(R/ref['CONTENT']['ISSUANCE_RECORD_PIN']['path']);exact=read(O/'exact-effective-accounting-rule.json');assert exact['RULE']==record['CONTENT']['ADOPTED_CONTENT']['PROPOSED_NORMATIVE_RULE'] and exact['NORMATIVE_AMENDMENT_IDENTITY']==ref['CONTENT']['APPROVED_SUBJECT_IDENTITY']
c=read(O/'package86-command-and-limits.json');assert hashlib.sha256(enc(c['EXACT_ARGV'])).hexdigest()==c['COMMAND_IDENTITY']['sha256']=='e628c8664ea72357963dc58dddee934c28cad3ab5c84450656a6595e6910fb50';assert hashlib.sha256(c['EXACT_ARGV'][-1].encode()).hexdigest()==c['PAYLOAD_RAW_SHA256'];t=ast.parse(c['EXACT_ARGV'][-1]);emit=next(x for x in t.body if isinstance(x,ast.FunctionDef) and x.name=='emit');tr=next(x for x in t.body if isinstance(x,ast.Try))
assert sum(isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='snapshot' for x in ast.walk(ast.Module(body=tr.body,type_ignores=[])))==2
assert sum(isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='emit' for h in tr.handlers for x in ast.walk(h))==1
assert any(isinstance(x,ast.While) for x in ast.walk(emit)) and 8192 in [x.value for x in ast.walk(emit) if isinstance(x,ast.Constant)]
p=read(O/'partial-write-reconstruction.json');assert p['MAX_WRITE_CALLS']==3*8192==24576 and p['MAX_SUBMITTED_BYTES_PYTHON_API']==3*sum(range(1,8193))==100675584 and p['MAX_LOGICAL_BYTES_SEALED_EMIT_FUNCTION']==24576 and p['NORMAL_TWO_EMIT_LOGICAL_BOUND']==16384
assert not p['API_SUBMISSION_BOUND_CHARGED_AS_OBSERVER_PUBLICATION']
inv=read(O/'publication-producer-applicability-matrix.json');assert len(inv['PRODUCERS'])==15 and set(row['EFFECTIVE_NORMATIVE_PRODUCER_CLASS'] for row in inv['PRODUCERS'])==set(exact['RULE']['COUNTED_PRODUCERS']) and all(row['COUNTED_IN_PUBLICATION_DOMAIN'] for row in inv['PRODUCERS'])
sc=read(O/'critical-evidence-schemas.json');pin=sc['SOURCE_PIN'];assert sha(R/pin['path'])==pin['raw_sha256'];sizes={}
for x in sc['AUTHENTICATED_CONTENT']['SCHEMAS']:assert len(enc(x['MAXIMAL_ENCODING_INSTANCE']))==x['MAX_RECORD_BYTES'];sizes[x['RECORD_TYPE']]=x['MAX_RECORD_BYTES']
base=sizes['FIRST_CAUSAL_FAILURE']+sizes['CONSUMPTION_STATE']+sizes['FINAL_AUDIT'];r=read(O/'protected-critical-reserve-model.json');assert r['CONDITIONAL_SINGLE_PUBLICATION_CORE_COEFFICIENTS']=={'PRIMARY_CONSUMPTION_FINAL':base,'DEFINITE_START_REJECTION':base+sizes['SERVICE_START_FAILURE'],'TIMEOUT_UNKNOWN_EXIT':base+sizes['TIMEOUT']+sizes['UNKNOWN_EXIT'],'OBSERVER_UNKNOWN_EXIT':base+sizes['UNKNOWN_EXIT']}
assert r['CRITICAL_RESERVE_BYTES'] is None and not r['CRITICAL_RESERVE_COMPLETE']
assert read(O/'normal-path-publication-budget.json')['NORMAL_PATH_TOTAL'] is None and read(O/'normal-path-publication-budget.json')['CAPACITY_AFTER_TWO_EMIT_SINGLE_RAW_BOUND']==49152
assert not read(O/'duplicate-denial-accounting.json')['DUPLICATE_DENIAL_BUDGET_COMPLETE'] and read(O/'duplicate-denial-accounting.json')['MAX_DENIAL_AUDITS'] is None
assert not read(O/'secondary-failure-accounting.json')['SECONDARY_FAILURE_BOUNDS_COMPLETE'] and all(x['MAX_OCCURRENCES'] is None for x in read(O/'secondary-failure-accounting.json')['FAILURES'])
maximum=read(O/'maximum-cumulative-publication-model.json');assert maximum['CAPACITY_AFTER_SINGLE_RAW_THREE_EMIT_BOUND']==40960 and maximum['TOTAL_PROTECTED_ALLOCATION'] is None and maximum['BUDGET_FEASIBILITY']=='UNDETERMINED'
construction=read(O/'construction-feasibility-determination.json');assert construction['EXACT_SOURCE_ALLOWLIST']==['adapter/qualification_bootstrap/systemd_pids_fixed_bridge.py','adapter/tests/test_systemd_pids_fixed_bridge.py'] and not construction['CONSTRUCTION_DECISION_READY'];assert all(not (R/p).exists() for p in construction['EXACT_SOURCE_ALLOWLIST'])
for edges in [read(O/'qualification-dependency-graph.json')['EDGES'],[(x['FROM'],x['TO']) for x in read(O/'one-attempt-lifecycle-model.json')['TRANSITIONS']]]:
 adj={}
 for x,y in edges:adj.setdefault(x,[]).append(y)
 def visit(n,active):
  assert n not in active
  for w in adj.get(n,[]):visit(w,active|{n})
 for n in adj:visit(n,set())
state={'amendment':EXPECTED_REF,'ceiling':65536,'distinct_domains':True,'charge_api_resubmission':False,'capture_included':True,'claim_launch_included':True,'denials_included':True,'unknown_secondary_accepted':False,'exclusive_summed':False,'concurrent_omitted':False,'reserve':None,'resources_from_bytes':False,'unqualified_launcher_accepted':False,'budget_feasible':False,'execution_authority_inferred':False,'h77_a15':False}
def valid(x):
 assert x['amendment']==EXPECTED_REF,'wrong effective amendment';assert x['ceiling']==65536,'ceiling increased';assert x['distinct_domains'],'domains conflated';assert not x['charge_api_resubmission'],'wrong submission charge';assert x['capture_included'],'payload copy omitted';assert x['claim_launch_included'],'claim/launch omitted';assert x['denials_included'],'denials omitted';assert not x['unknown_secondary_accepted'],'secondary unbounded';assert not x['exclusive_summed'],'exclusive double count';assert not x['concurrent_omitted'],'concurrent failures omitted';assert x['reserve'] is None,'arbitrary reserve';assert not x['resources_from_bytes'],'resource inference';assert not x['unqualified_launcher_accepted'],'unqualified launcher';assert not x['budget_feasible'],'incomplete feasible';assert not x['execution_authority_inferred'],'authority inferred';assert not x['h77_a15'],'H77/A15'
valid(state);neg=[]
for key in state:
 x=copy.deepcopy(state);x[key]={} if key=='amendment' else 65537 if key=='ceiling' else 1 if key=='reserve' else not x[key]
 try:valid(x)
 except AssertionError as e:neg.append({'CONTROL':key,'RESULT':'REJECTED','CAUSE':str(e)})
 else:raise AssertionError(key)
names=['effective-amendment-authentication.json','exact-effective-accounting-rule.json','package86-command-and-limits.json','partial-write-reconstruction.json','distinct-byte-accounting-model.json','critical-evidence-schemas.json','publication-producer-applicability-matrix.json','one-attempt-lifecycle-model.json','primary-outcome-bounds.json','duplicate-denial-accounting.json','secondary-failure-accounting.json','protected-critical-reserve-model.json','normal-path-publication-budget.json','failure-path-publication-budgets.json','maximum-cumulative-publication-model.json','observer-launcher-store-gap-assessment.json','construction-feasibility-determination.json','qualification-dependency-graph.json','remaining-gap-dossier.json']
s={'PINS':{n:sha(O/n) for n in names},'EFFECTIVE_AMENDMENT_IDENTITY':EXPECTED_REF,'ACCOUNTING_RULE_APPLIED':True,'PAYLOAD_LOGICAL_BOUND':24576,'PAYLOAD_API_SUBMISSION_BOUND':100675584,'CONDITIONAL_CRITICAL_COEFFICIENTS':r['CONDITIONAL_SINGLE_PUBLICATION_CORE_COEFFICIENTS'],'PUBLICATION_CEILING':65536,'CRITICAL_RESERVE':None,'BUDGET_FEASIBILITY':'UNDETERMINED','GRAPH_ACYCLIC':True,'CONSTRUCTION_DECISION_READY':False,'REAL_PROBE_EXECUTION_READY':False,'NEGATIVES':neg}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':s,'SEMANTIC_SHA256':hashlib.sha256(enc(s)).hexdigest()},sort_keys=True))
