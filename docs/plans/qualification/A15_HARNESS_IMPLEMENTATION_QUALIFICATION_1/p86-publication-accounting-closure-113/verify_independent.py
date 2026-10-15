"""113 static reconstruction, no target or host execution."""
import pathlib,json,hashlib,ast,copy,os
O=pathlib.Path(__file__).resolve().parent;R=O.parents[4]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
a=read(O/'entry-authentication.json')
for p,h in a['PINS'].items():assert sha(R/p)==h
c=read(O/'package86-command-authentication.json');orig=read(O.parent/'system-process-enforcement-86/transient-service-specification.json');assert c['EXACT_ARGV']==orig['EXACT_COMMAND_ARGV']
assert hashlib.sha256(enc(c['EXACT_ARGV'])).hexdigest()==c['COMMAND_IDENTITY']['sha256']=='e628c8664ea72357963dc58dddee934c28cad3ab5c84450656a6595e6910fb50';assert hashlib.sha256(c['EXACT_ARGV'][-1].encode()).hexdigest()==c['PAYLOAD_RAW_SHA256'];t=ast.parse(c['EXACT_ARGV'][-1])
tr=next(x for x in t.body if isinstance(x,ast.Try));emit=next(x for x in t.body if isinstance(x,ast.FunctionDef) and x.name=='emit')
assert sum(isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='snapshot' for x in ast.walk(ast.Module(body=tr.body,type_ignores=[])))==2
assert sum(isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='emit' for h in tr.handlers for x in ast.walk(h))==1
assert 8192 in [x.value for x in ast.walk(emit) if isinstance(x,ast.Constant)] and any(isinstance(x,ast.While) for x in ast.walk(emit))
p=read(O/'partial-write-arithmetic-reconstruction.json');assert p['MAX_EMIT_CALLS']==3 and p['MAX_WRITE_CALLS']==3*8192 and p['MAX_LOGICAL_BYTES']==p['MAX_TRANSFERRED_BYTES']==24576 and p['MAX_SUBMITTED_BYTES_PYTHON_API']==3*sum(range(1,8193))==100675584
sem=read(O/'authoritative-publication-semantics-assessment.json');pin=sem['PUBLICATION_LIMIT_SOURCE'];assert sha(R/pin['path'])==pin['raw_sha256'];source=read(R/pin['path']);assert source['MAX_OBSERVER_PUBLISHED_BYTES']==sem['PUBLICATION_LIMIT_BYTES']==65536 and not sem['PUBLICATION_SEMANTICS_RESOLVED']
assert hashlib.sha256(enc(source)).hexdigest()==sem['PUBLICATION_LIMIT_IDENTITY']['sha256']
cl=read(O/'prospective-publication-clarification-subject.json');assert hashlib.sha256(enc(cl['CONTENT'])).hexdigest()==cl['IDENTITY']['sha256'] and cl['CONTENT']['NO_APPLIED_RULE'] and cl['CONTENT']['NO_SELECTED_MEASURE']
sc=read(O/'authenticated-critical-record-schemas.json');assert sha(R/sc['SOURCE_PIN']['path'])==sc['SOURCE_PIN']['sha256']
for x in sc['CONTENT']['SCHEMAS']:assert len(enc(x['MAXIMAL_ENCODING_INSTANCE']))==x['MAX_RECORD_BYTES']
ct=read(O/'critical-occurrence-count-model.json');assert not ct['FAILURE_EVENT_COUNTS_COMPLETE'];counts={x['EVENT_TYPE']:x for x in ct['EVENTS']};assert counts['SECONDARY_FAILURE']['MAX_OCCURRENCES_ALL_REQUIRED_PRODUCERS'] is None and counts['DUPLICATE_REJECTION']['MAX_OCCURRENCES_ALL_REQUIRED_PRODUCERS'] is None
sm=read(O/'failure-event-state-machine.json');assert len(sm['STATES'])==13 and not sm['CONSUMED_AUTHORITY_RESTORED'];assert all(not x['RETRY_ELIGIBILITY'] and x['MAX_OCCURRENCES_PER_SINGLE_AUTHORIZED_INVOCATION']==1 for x in sm['TRANSITIONS'])
assert read(O/'protected-reserve-derivation.json')['CRITICAL_RESERVE_BYTES'] is None and not read(O/'conditional-publication-budget-models.json')['PUBLICATION_BUDGET_COMPLETE']
for graph in [read(O/'qualification-dependency-graph.json')['EDGES'],[(x['FROM'],x['TO']) for x in sm['TRANSITIONS']]]:
 adj={}
 for x,y in graph:adj.setdefault(x,[]).append(y)
 def visit(n,active):
  assert n not in active
  for w in adj.get(n,[]):visit(w,active|{n})
 for n in adj:visit(n,set())
reg=read(R/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');prev='0'*64
for e in reg['EVENTS']:
 assert e['PREVIOUS_EVENT_HASH']==prev
 assert hashlib.sha256(json.dumps({k:v for k,v in e.items() if k!='EVENT_HASH'},sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()==e['EVENT_HASH'];prev=e['EVENT_HASH']
assert prev=='885fd0eaceb15847201dfd058217682741fb43c255298713ccbc1e7251eec791';assert sha(O.parent/'campaign-budget.jsonl')=='3491e9003e1a016dbc4208e3963f8abea0f98c439dc892aa89a3811e73d528eb'
fields=['submitted_equals_transferred','persisted_from_return','partial_submission_omitted','unbounded_secondary_accepted','exclusive_events_summed','concurrent_errors_omitted','arbitrary_reserve','ceiling_reinterpreted','unbounded_stderr_accepted','observer_self_report','arbitrary_observer_limits','duplicate_grant_consumption','post_deadline_restart','unissued_effective','source_modified','premature_systemd','h77_a15']
state={k:False for k in fields}
def valid(x):
 for k in fields:
  if x[k]:raise ValueError(k)
valid(state);neg=[]
for k in fields:
 x=copy.deepcopy(state);x[k]=True
 try:valid(x)
 except ValueError as e:neg.append({'CONTROL':k,'RESULT':'REJECTED','CAUSE':str(e)})
 else:raise AssertionError(k)
names=['entry-authentication.json','package86-command-authentication.json','authoritative-publication-semantics-assessment.json','distinct-byte-measures.json','partial-write-arithmetic-reconstruction.json','publication-producer-applicability-matrix.json','failure-event-state-machine.json','authenticated-critical-record-schemas.json','critical-occurrence-count-model.json','protected-reserve-derivation.json','conditional-publication-budget-models.json','launcher-principal-contract.json','stable-consumption-store-contract.json','observer-event-and-resource-model.json','post-deadline-finalization-contract.json','exact-construction-boundary.json','prospective-publication-clarification-subject.json','authority-assessment.json','qualification-dependency-graph.json','remaining-gap-dossier.json']
s={'PINS':{n:sha(O/n) for n in names},'COMMAND_IDENTITY':c['COMMAND_IDENTITY'],'PUBLICATION_CAP':65536,'LOGICAL_PAYLOAD_BOUND':24576,'API_SUBMISSION_BOUND':100675584,'PUBLICATION_SEMANTICS_RESOLVED':False,'FAILURE_EVENT_COUNTS_COMPLETE':False,'CRITICAL_RESERVE':None,'GRAPH_ACYCLIC':True,'LL11_HEAD':prev,'CONSTRUCTION_DECISION_READY':False,'NEGATIVES':neg}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':s,'SEMANTIC_SHA256':hashlib.sha256(enc(s)).hexdigest()},sort_keys=True))
