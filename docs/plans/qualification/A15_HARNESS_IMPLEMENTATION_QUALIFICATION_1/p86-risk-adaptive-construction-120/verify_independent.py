"""Documentary verification only. Never imports or executes prospective source."""
import os,json,pathlib,hashlib,subprocess,sys,copy
O=pathlib.Path(__file__).resolve().parent
R=pathlib.Path.cwd()
B=pathlib.Path('docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1')
def read(n):return json.loads((O/n).read_text())
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def digest(b):return hashlib.sha256(b).hexdigest()
def require(x,reason):
 if not x:raise ValueError(reason)
def acyclic(edges):
 visiting=set();done=set();adj={}
 for a,b in edges:adj.setdefault(a,[]).append(b)
 def visit(n):
  require(n not in visiting,'cycle')
  if n in done:return
  visiting.add(n)
  for v in adj.get(n,[]):visit(v)
  visiting.remove(n);done.add(n)
 for n in adj:visit(n)
 return True
scope=read('two-file-scope.json')['EXACT_PATHS']
base=[len(pathlib.Path(p).read_bytes()) for p in ['adapter/qualification_bootstrap/systemd_pids_once.py','adapter/tests/test_systemd_pids_bootstrap.py']]
e118=B/'p86-construction-scope-closure-118'
oldindex=json.loads((e118/'evidence-index.json').read_text())['FILES']
evidencebase=sum(len((e118/n).read_bytes()) for n in oldindex)
critical=read('allocation-rationale.json')['CRITICAL_SCHEMA_MAXIMAL_INSTANCE']
recordcap=len(canonical(critical))
policy=read('proposed-policy-allocation.json')
auth=read('authority-applicability.json')
graph=read('dependency-graph.json')['EDGES']
originalmatrix=json.loads((B/'p86-construction-activity-budget-119'/'phase-classification-matrix.json').read_text())['REQUIREMENTS']
def validate(m):
 p=m['policy'];a=m['authority']
 require(m['paths']==scope and len(scope)==2,'allowlist')
 require(m['matrix']==originalmatrix and len(m['matrix'])==36,'binding phase changes')
 require(p['STATUS']=='PROPOSED_POLICY_ALLOCATION_NOT_EFFECTIVE','policy status')
 for i,v in enumerate(base):
  f=p['FILES'][i]
  require(f['PATH']==scope[i] and f['PRECEDENT_BYTES']==v,'precedent/path')
  require(f['BASE_ESTIMATE_BYTES']==v and f['POLICY_ADAPTATION_RESERVE_BYTES']==v and f['MAX_RETAINED_SOURCE_BYTES']==2*v,'source policy formula')
  require(f['MAX_FULL_SOURCE_PUBLICATIONS']==3 and f['MAX_MANUAL_RECOVERABLE_REVISIONS']==2 and f['MAX_CUMULATIVE_LOGICAL_SOURCE_BYTES']==6*v,'bounded revisions')
 require(p['MAX_RETAINED_SOURCE_BYTES']==2*sum(base) and p['MAX_CUMULATIVE_LOGICAL_SOURCE_BYTES']==6*sum(base),'source totals')
 require(p['MAX_TOTAL_LOGICAL_EVIDENCE_BYTES']==2*evidencebase+4*recordcap and p['MAX_NORMAL_EVIDENCE_BYTES']==2*evidencebase,'evidence allocation')
 require(p['MAX_CRITICAL_EVIDENCE_RECORD_BYTES']==recordcap and p['PROTECTED_CRITICAL_EVIDENCE_BYTES']==4*recordcap,'protected reserve')
 require(p['MAX_TOTAL_EVIDENCE_RECORDS']==3*len(oldindex)+4,'record count')
 require(p['MAX_CAMPAIGNS']==1 and p['AUTOMATIC_RETRIES']==0 and p['IMPLICIT_RESTARTS']==0,'restart')
 require(p['MAX_STATIC_VERIFICATION_ROUNDS']==3 and p['SEEDS']==[0,1,7,101] and p['MAX_FRESH_SEEDED_VERIFIER_INVOCATIONS']==12 and p['MAX_NEGATIVE_EXECUTIONS']==360,'verification cardinality')
 require(p['MAX_WALL_SECONDS']==6*600 and p['MAX_WORK_UNIT_WALL_SECONDS']==600 and p['MAX_STATIC_ROUND_WALL_SECONDS']==600//3,'wall policy')
 require(p['MAX_AGGREGATE_CPU_SECONDS']==6*300 and p['MAX_PER_PROCESS_CPU_SECONDS']==60,'cpu policy')
 require(p['MAX_PER_PROCESS_ADDRESS_SPACE_BYTES']==256*1024*1024 and p['MAX_AGGREGATE_MEMORY_BYTES']==8*p['MAX_PER_PROCESS_ADDRESS_SPACE_BYTES'],'memory allocation')
 require(p['MAX_OPEN_FDS_PER_PROCESS']==64 and p['MAX_AGGREGATE_OPEN_FDS']==8*64,'descriptor allocation')
 require(p['MAX_LIVE_PROCESSES_AND_THREADS']==8 and p['MAX_TOTAL_PROCESS_CREATIONS']==3*(1+4*9)+2,'process policy')
 require(p['COMPLETE_FIT_PROVEN'] is False and p['ENFORCEMENT_VERIFIED'] is False,'proposed not proof')
 require(p['REAL_PROBE_PUBLICATION_CEILING']==65536 and p['REAL_PROBE_BUDGET_FEASIBILITY']=='UNDETERMINED','real budget unchanged')
 require(a['CONSTRUCTION_DECISION_READY'] is False and a['CONSTRUCTION_SUBJECT_COMPLETE'] is False and a['DECISION_OPTIONS']==[],'incomplete subject not selectable')
 require(not a['CONSTRUCTION_GRANT_ISSUED'] and not a['CONSTRUCTION_GRANT_EFFECTIVE'] and not a['CONSTRUCTION_ENTRY_READY'] and not a['OLD90_94_REUSE'] and not a['CURRENT_OWNER_DIRECTION_EXECUTION_AUTHORITY'],'no implied authority')
 require(m['real_disabled'] and m['fresh_guard'] and m['entry_safety'] and not m['future_result_required'],'entry/result separation')
 require(m['old_attempts']==1 and m['old_retries']==0 and not m['architecture_effective'],'historical governance preserved')
 require(m['first_cause_preserved'] and not m['recursive_logging'] and not m['silent_overflow'] and m['checkpoint_required'],'failure discipline')
 require(not m['submitted_equals_logical'] and not m['transfer_equals_durable'],'separate accounting')
 acyclic(m['edges'])
 return True
model={'policy':policy,'authority':auth,'paths':scope,'matrix':originalmatrix,'edges':graph,'real_disabled':True,'fresh_guard':True,'entry_safety':True,'future_result_required':False,'old_attempts':1,'old_retries':0,'architecture_effective':False,'first_cause_preserved':True,'recursive_logging':False,'silent_overflow':False,'checkpoint_required':True,'submitted_equals_logical':False,'transfer_equals_durable':False}
validate(model)
manifest=read('authenticated-input-manifest.json')
for path,h in manifest['PINS'].items():require(digest(pathlib.Path(path).read_bytes())==h,'input pin '+path)
for path,h in read('preservation-before.json')['FILES'].items():require(digest(pathlib.Path(path).read_bytes())==h,'preservation '+path)
require(all(not pathlib.Path(p).exists() for p in scope),'construction not performed')
fragment=read('construction-only-contract-fragment.json');require(digest(canonical(fragment['CONTENT']))==fragment['IDENTITY']['sha256'],'fragment identity');require(fragment['CONTENT']['OWNER_SELECTION'] is None,'unselected')
require(read('36-row-phase-matrix.json')['REQUIREMENTS']==originalmatrix,'matrix exact')
# Fresh current lifecycle reader, metadata only; no target module or sealed command is executed.
p=subprocess.run([sys.executable,str(B/'p86-publication-amendment-issuance-115'/'verify_independent.py'),'EFFECTIVE'],capture_output=True,text=True)
require(p.returncode==0,'current effective amendment reader');current=json.loads(p.stdout)
# Compare exact adopted content with sealed approval and retained command rather than trusting status text.
effective=json.loads((B/'p86-publication-amendment-issuance-115'/'effective-p86-publication-amendment-reference.json').read_text())
require(effective['IDENTITY']['sha256']=='f39f040197fc3978f284b36f38a9c7e3445acfe1f78a69c9387db8f6bbe83993','effective identity')
negatives=[]
def negative(name,mutate):
 altered=copy.deepcopy(model);mutate(altered)
 try:validate(altered)
 except ValueError as e:negatives.append({'DESIGN':name,'RESULT':'REJECTED','CAUSE':str(e)});return
 raise AssertionError('Negative admitted: '+name)
def setp(k,v):return lambda m:m['policy'].__setitem__(k,v)
def seta(k,v):return lambda m:m['authority'].__setitem__(k,v)
def setm(k,v):return lambda m:m.__setitem__(k,v)
negative('changed path',lambda m:m['paths'].append('adapter/other.py'))
negative('unbounded source',setp('MAX_RETAINED_SOURCE_BYTES',None))
negative('unbounded evidence',setp('MAX_TOTAL_LOGICAL_EVIDENCE_BYTES',None))
negative('missing reserve',setp('PROTECTED_CRITICAL_EVIDENCE_BYTES',0))
negative('unlimited revisions',lambda m:m['policy']['FILES'][0].__setitem__('MAX_MANUAL_RECOVERABLE_REVISIONS',None))
negative('automatic retry',setp('AUTOMATIC_RETRIES',1))
negative('implicit reset',setp('IMPLICIT_RESTARTS',1))
negative('old probe retry changed',setm('old_retries',1))
negative('old probe attempts changed',setm('old_attempts',2))
negative('proposed allocation called proof',setp('COMPLETE_FIT_PROVEN',True))
negative('unverified enforcement called verified',setp('ENFORCEMENT_VERIFIED',True))
negative('per process memory called aggregate',setp('MAX_AGGREGATE_MEMORY_BYTES',256*1024*1024))
negative('unbounded cpu',setp('MAX_AGGREGATE_CPU_SECONDS',None))
negative('unbounded wall',setp('MAX_WALL_SECONDS',None))
negative('unbounded fd',setp('MAX_AGGREGATE_OPEN_FDS',None))
negative('unbounded native descendants',setp('MAX_TOTAL_PROCESS_CREATIONS',None))
negative('real ceiling borrowed as construction evidence',setp('MAX_TOTAL_LOGICAL_EVIDENCE_BYTES',65536))
negative('real budget falsely passed',setp('REAL_PROBE_BUDGET_FEASIBILITY','PASS'))
negative('missing fresh guard',setm('fresh_guard',False))
negative('entry safety deferred',setm('entry_safety',False))
negative('own future result before authority',setm('future_result_required',True))
negative('old grant reused',seta('OLD90_94_REUSE',True))
negative('architectural direction effective',setm('architecture_effective',True))
negative('owner direction treated as execution grant',seta('CURRENT_OWNER_DIRECTION_EXECUTION_AUTHORITY',True))
negative('incomplete subject selectable',seta('CONSTRUCTION_DECISION_READY',True))
negative('grant incorrectly effective',seta('CONSTRUCTION_GRANT_EFFECTIVE',True))
negative('real launch enabled',setm('real_disabled',False))
negative('first cause overwritten',setm('first_cause_preserved',False))
negative('recursive errors',setm('recursive_logging',True))
negative('silent overflow',setm('silent_overflow',True))
negative('missing checkpoint',setm('checkpoint_required',False))
negative('submitted conflated with logical',setm('submitted_equals_logical',True))
negative('transferred conflated with durable',setm('transfer_equals_durable',True))
negative('graph own-result cycle',lambda m:m['edges'].append(['CONSTRUCTION_OUTPUT','CONSTRUCTION_DECISION']))
semantic={'INPUT_PINS':manifest['PINS'],'ALLOWLIST':scope,'POLICY_SHA256':digest(canonical(policy)),'PHASE_MATRIX_SHA256':digest(canonical(originalmatrix)),'FRAGMENT_IDENTITY':fragment['IDENTITY'],'ALLOCATION_FORMULAS_VALID':True,'SEMANTICS':'Policy allocations, not completion/enforcement proof; architecture not effective; exact execution recipe missing','CONSTRUCTION_DECISION_READY':False,'CONSTRUCTION_ENTRY_READY':False,'GRAPH_ACYCLIC':acyclic(graph),'HISTORICAL_PRESERVATION':'PASS','NEGATIVES':negatives,'CURRENT115_IDENTITY':effective['IDENTITY']}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':semantic,'SEMANTIC_SHA256':digest(canonical(semantic))},sort_keys=True))
