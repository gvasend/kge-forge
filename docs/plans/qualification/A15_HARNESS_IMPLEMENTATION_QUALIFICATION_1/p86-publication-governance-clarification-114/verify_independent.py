"""114 static normative-decision verification; no execution or adoption."""
import pathlib,json,hashlib,ast,copy,os
O=pathlib.Path(__file__).resolve().parent;R=O.parents[4]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
a=read(O/'entry-authentication.json')
for p,h in a['PINS'].items():assert sha(R/p)==h
req=read(O/'authenticated-publication-requirement.json');assert sha(R/req['SOURCE_PATH'])==req['SOURCE_RAW_SHA256'] and req['EXACT_FIELD']=={'MAX_OBSERVER_PUBLISHED_BYTES':65536}
orig=read(O.parent/'system-process-enforcement-86/transient-service-specification.json');assert hashlib.sha256(enc(orig['EXACT_COMMAND_ARGV'])).hexdigest()==req['PACKAGE_86_COMMAND_IDENTITY']['sha256']=='e628c8664ea72357963dc58dddee934c28cad3ab5c84450656a6595e6910fb50';tree=ast.parse(orig['EXACT_COMMAND_ARGV'][-1]);emit=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='emit');assert any(isinstance(x,ast.While) for x in ast.walk(emit)) and 8192 in [x.value for x in ast.walk(emit) if isinstance(x,ast.Constant)]
p=read(O/'partial-write-arithmetic-verification.json')['RECONSTRUCTION'];assert p['MAX_EMIT_CALLS']==3 and p['MAX_LOGICAL_BYTES']==3*8192==24576 and p['MAX_SUBMITTED_BYTES_PYTHON_API']==3*sum(range(1,8193))==100675584
subject=read(O/'proposed-normative-decision-subject.json');c=subject['CONTENT'];rule=c['PROPOSED_NORMATIVE_RULE'];assert hashlib.sha256(enc(c)).hexdigest()==subject['IDENTITY']['sha256']
for n,h in c['INDEPENDENT_EVIDENCE_PINS'].items():assert sha(O/n)==h
assert rule==read(O/'proposed-publication-semantics-amendment.json')
expected=['PROBE_PAYLOAD','LAUNCHER_CONSUMPTION_RECORD','LAUNCH_ATTEMPT_RECORD','INDEPENDENT_OBSERVER','SERVICE_STDERR','SERVICE_EXIT_RECORD','TIMEOUT_RECORD','FIRST_CAUSAL_FAILURE','SECONDARY_FAILURE','DUPLICATE_DENIAL_AUDIT','FINAL_AUDIT','NO_RETRY_RECORD']
assert c['PRODUCER_SCOPE']==rule['COUNTED_PRODUCERS']==expected
assert c['GOVERNANCE_CLASSIFICATION']=='NORMATIVE_AMENDMENT_REQUIRED' and c['EXISTING_CEILING']==rule['CUMULATIVE_LIMIT']==rule['MAX_OBSERVER_PUBLISHED_BYTES']==65536
assert c['NO_EXECUTION_AUTHORITY'] and c['NO_CONSTRUCTION_AUTHORITY'] and c['NO_INERT_TEST_AUTHORITY'] and not subject['EFFECTIVE'] and subject['OWNER_SELECTION'] is None
assert not rule['DUPLICATE_AUDIT_RULE']['EXTERNAL_REQUEST_COUNT_ASSUMED_FINITE'] and rule['CRITICAL_EVIDENCE_RULE']['IN_SAME_CEILING'] and rule['CRITICAL_EVIDENCE_RULE']['FINITE_RESERVE_ENTRY_REQUIRED']
assert not rule['SECONDARY_FAILURE_RULE']['EVENT_COUNT_FROM_ONE_ATTEMPT'] and rule['SECONDARY_FAILURE_RULE']['NUMERIC_MAXIMUM'] is None
life=read(O/'governance-lifecycle-specification.json');assert not life['CURRENT_EFFECTIVE'] and not life['APPROVAL_EVIDENCE_CREATED'] and life['ISSUER_ROLE']==c['ISSUER_ROLE']
g=read(O/'qualification-dependency-graph.json');d={}
for x,y in g['EDGES']:d.setdefault(x,[]).append(y)
def visit(n,active):
 assert n not in active
 for w in d.get(n,[]):visit(w,active|{n})
for n in d:visit(n,set())
reg=read(R/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');prev='0'*64
for e in reg['EVENTS']:
 assert e['PREVIOUS_EVENT_HASH']==prev
 assert hashlib.sha256(json.dumps({k:v for k,v in e.items() if k!='EVENT_HASH'},sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()==e['EVENT_HASH'];prev=e['EVENT_HASH']
assert prev=='885fd0eaceb15847201dfd058217682741fb43c255298713ccbc1e7251eec791';assert sha(O.parent/'campaign-budget.jsonl')=='3491e9003e1a016dbc4208e3963f8abea0f98c439dc892aa89a3811e73d528eb'
# Mutate the actual normative decision contract, not OS behavior.
def validate(s):
 x=s['CONTENT'];r=x['PROPOSED_NORMATIVE_RULE']
 if x['EXISTING_CEILING']!=65536 or r['CUMULATIVE_LIMIT']!=65536:raise ValueError('ceiling increased')
 if x['PRODUCER_SCOPE']!=expected or r['COUNTED_PRODUCERS']!=expected:raise ValueError('producer exempted')
 if r['BYTE_MEASURE']!=rule['BYTE_MEASURE']:raise ValueError('byte domain conflation')
 if r['PARTIAL_WRITE_RULE']!=rule['PARTIAL_WRITE_RULE']:raise ValueError('persistence or partial accounting conflated')
 if r['ACCOUNTING_INTERVAL']!=rule['ACCOUNTING_INTERVAL']:raise ValueError('per-record cap substituted')
 if not r['CRITICAL_EVIDENCE_RULE']['IN_SAME_CEILING']:raise ValueError('unbounded critical exemption')
 if r['DUPLICATE_AUDIT_RULE']['EXTERNAL_REQUEST_COUNT_ASSUMED_FINITE']:raise ValueError('duplicate count inferred')
 if r['SECONDARY_FAILURE_RULE']['OPERATIONS']!=rule['SECONDARY_FAILURE_RULE']['OPERATIONS']:raise ValueError('secondary omitted')
 if x['GOVERNANCE_CLASSIFICATION']!='NORMATIVE_AMENDMENT_REQUIRED':raise ValueError('amendment mislabeled')
 if s['EFFECTIVE'] or s['OWNER_SELECTION'] is not None:raise ValueError('unissued effective')
 if not x['NO_EXECUTION_AUTHORITY']:raise ValueError('probe authority inferred')
 if x['HISTORICAL_EXCLUSIONS']!=c['HISTORICAL_EXCLUSIONS']:raise ValueError('historical scope mutation')
 if s.get('CIRCULAR_DEPENDENCY',False):raise ValueError('circular dependency')
 if s.get('EXECUTION_ACTIVE',False):raise ValueError('premature execution')
validate(subject)
mutations=[('ceiling increased',lambda s:s['CONTENT'].__setitem__('EXISTING_CEILING',65537)),('producer silently exempted',lambda s:s['CONTENT']['PRODUCER_SCOPE'].pop()),('submitted transferred conflation',lambda s:s['CONTENT']['PROPOSED_NORMATIVE_RULE'].__setitem__('BYTE_MEASURE','submitted equals transferred')),('persistence inferred',lambda s:s['CONTENT']['PROPOSED_NORMATIVE_RULE'].__setitem__('PARTIAL_WRITE_RULE','write return proves persistence')),('per-record substituted',lambda s:s['CONTENT']['PROPOSED_NORMATIVE_RULE'].__setitem__('ACCOUNTING_INTERVAL','per record')),('critical exemption',lambda s:s['CONTENT']['PROPOSED_NORMATIVE_RULE']['CRITICAL_EVIDENCE_RULE'].__setitem__('IN_SAME_CEILING',False)),('duplicate count assumed',lambda s:s['CONTENT']['PROPOSED_NORMATIVE_RULE']['DUPLICATE_AUDIT_RULE'].__setitem__('EXTERNAL_REQUEST_COUNT_ASSUMED_FINITE',True)),('secondary omitted',lambda s:s['CONTENT']['PROPOSED_NORMATIVE_RULE']['SECONDARY_FAILURE_RULE'].__setitem__('OPERATIONS',[])),('amendment mislabeled',lambda s:s['CONTENT'].__setitem__('GOVERNANCE_CLASSIFICATION','INTERPRETIVE_CLARIFICATION')),('unissued effective',lambda s:s.__setitem__('EFFECTIVE',True)),('probe authority inferred',lambda s:s['CONTENT'].__setitem__('NO_EXECUTION_AUTHORITY',False)),('history modified',lambda s:s['CONTENT'].__setitem__('HISTORICAL_EXCLUSIONS',[])),('circular dependency',lambda s:s.__setitem__('CIRCULAR_DEPENDENCY',True)),('premature execution',lambda s:s.__setitem__('EXECUTION_ACTIVE',True))]
neg=[]
for name,mut in mutations:
 s=copy.deepcopy(subject);mut(s)
 try:validate(s)
 except ValueError as e:neg.append({'CONTROL':name,'RESULT':'REJECTED','CAUSE':str(e)})
 else:raise AssertionError(name)
names=['authenticated-publication-requirement.json','producer-applicability-matrix.json','byte-counting-semantics-comparison.json','partial-write-arithmetic-verification.json','cumulative-accounting-scope.json','critical-evidence-applicability.json','duplicate-denial-audit-policy.json','secondary-failure-event-policy.json','clarification-versus-amendment-assessment.json','proposed-publication-semantics-amendment.json','governance-lifecycle-specification.json','post-decision-work.json','qualification-dependency-graph.json','proposed-normative-decision-subject.json']
s={'PINS':{n:sha(O/n) for n in names},'SUBJECT_IDENTITY':subject['IDENTITY'],'CLASSIFICATION':'NORMATIVE_AMENDMENT_REQUIRED','GOVERNANCE_DECISION_READY':True,'CLARIFICATION_EFFECTIVE':False,'AMENDMENT_EFFECTIVE':False,'CONSTRUCTION_DECISION_READY':False,'REAL_PROBE_EXECUTION_READY':False,'GRAPH_ACYCLIC':True,'LL11_HEAD':prev,'NEGATIVES':neg}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':s,'SEMANTIC_SHA256':hashlib.sha256(enc(s)).hexdigest()},sort_keys=True))
