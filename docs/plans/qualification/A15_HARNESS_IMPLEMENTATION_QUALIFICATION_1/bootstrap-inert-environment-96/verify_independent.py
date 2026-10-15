"""Metadata-only independent96 verifier. Never imports target modules or launches them."""
import ast,copy,hashlib,json,os,pathlib
R=pathlib.Path(__file__).resolve().parents[5]
B=R/'docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1'
O=pathlib.Path(__file__).parent

def read(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def require(x,m):
 if not x:raise ValueError(m)
def acyclic(edges):
 adj={}
 for e in edges:adj.setdefault(e['from'],[]).append(e['to'])
 done=set();active=set()
 def visit(v):
  if v in active:return False
  if v in done:return True
  active.add(v)
  for w in adj.get(v,[]):
   if not visit(w):return False
  active.remove(v);done.add(v);return True
 return all(visit(v) for v in adj)
def validate(s):
 require(s['sources']==read(B/'bootstrap-entry-oracle-repair-95/source-identity-manifest.json') and all(digest(R/x['SOURCE_PATH'])==x['SOURCE_SHA256'] for x in s['sources']['SOURCES']),'source mismatch')
 require(s['root']==207444 and s['ordinary']==65536,'limit classification')
 require(s['runtime']=='NOT_TESTED','unsupported runtime admission')
 require(not s['store_verified'] and s['dir_fsync'],'unqualified store/barrier')
 require(s['children']==2 and s['launches']==16 and s['fixed_child_scope'],'unbounded process scope')
 require(s['hard_timeout_required'] and not s['timeout_qualified'],'unknown hard timeout')
 require(s['cumulative_accounting_required'] and not s['cumulative_accounting_qualified'],'unverified write accounting')
 require(not s['observer_qualified'],'unverified observer')
 require(s['authority']=='CONDITIONAL_ONE_INERT_CAMPAIGN_ONLY' and not s['activated'],'premature campaign authority')
 require(acyclic(s['edges']) and not any(e['from']=='BASIC_RESOURCE_CONTROLS' and e['to']=='HOST_PIDS_QUALIFICATION' for e in s['edges']),'dependency cycle')
 require(s['retry']==0 and not any(s['real_execution'].values()),'retry or real execution')
 return True
manifest=read(O/'authenticated-source-manifest.json')
seal=read(B/'bootstrap-entry-oracle-repair-95/source-identity-manifest.json')
require(manifest['SOURCES']=={x['SOURCE_PATH']:x['SOURCE_SHA256'] for x in seal['SOURCES']},'96 source map')
idx=read(B/'bootstrap-entry-oracle-repair-95/evidence-index.json')
for n,h in idx['FILES'].items():require(digest(B/'bootstrap-entry-oracle-repair-95'/n)==h,'95 pin')
for r in manifest['EFFECTIVE_GRANT_REFERENCES']:
 require(digest(R/r['path'])==r['raw_sha256'],'effective reference')
 ref=read(R/r['path']);p=ref['GRANT_RECORD_PIN'];require(digest(R/p['path'])==p['raw_sha256'],'grant raw pin')
 g=read(R/p['path']);body=g.get('RECORD',g.get('CONTENT'));require(hashlib.sha256(canonical(body)).hexdigest()==r['identity']['sha256'],'grant content')
 for p in ref['VERIFICATION_PINS']:require(digest(R/p['path'])==p['raw_sha256'],'issuance evidence pin')
core=(R/'adapter/qualification_bootstrap/systemd_pids_once.py').read_text();test=(R/'adapter/tests/test_systemd_pids_bootstrap.py').read_text()
tree=ast.parse(core);tt=ast.parse(test)
func={n.name:n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef)}
def excerpt(name):return ast.get_source_segment(core,func[name])
require('ORDINARY_RECORD_MAX_BYTES' in excerpt('read_at') and 'ROOT_ENTRY_MAX_BYTES' not in excerpt('read_at'),'ordinary read size')
require('verify_repair_authority()' in excerpt('read_root_entry') and 'ROOT_ENTRY_MAX_BYTES' in excerpt('read_root_entry'),'root classification')
require('os.fsync' in excerpt('_publish') and 'os.fsync(directory)' in excerpt('_publish'),'durability source')
require('REAL_PROBE_BINDING = None' in core,'real binding')
names=[n.name for n in ast.walk(tt) if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')];require(len(names)==14,'test selection')
require('child.wait(timeout=remaining)' in test and 'child.wait(timeout=2)' in test,'parent lifecycle')
fixture=read(B/'bootstrap-inert-readiness-92/sealed-synthetic-fixture-manifest.json');oracle=read(B/'bootstrap-inert-readiness-92/independent-oracle-manifest.json')
for x in (fixture,oracle):require(hashlib.sha256(canonical(x['CONTENT'])).hexdigest()==x['IDENTITY']['sha256'],'manifest identity')
require(len(fixture['CONTENT']['FIXTURES'])==14 and sum(len(x['CONTENT']['VARIANTS']) for x in fixture['CONTENT']['FIXTURES'])==21,'fixture closure')
require(len(oracle['CONTENT']['ORACLES'])==14,'oracle closure')
graph=read(O/'acyclic-dependency-contract.json')
s={'sources':seal,'root':207444,'ordinary':65536,'runtime':'NOT_TESTED','store_verified':False,'dir_fsync':True,'children':2,'launches':16,'fixed_child_scope':True,'hard_timeout_required':True,'timeout_qualified':False,'cumulative_accounting_required':True,'cumulative_accounting_qualified':False,'observer_qualified':False,'authority':read(O/'prospective-campaign-authority-assessment.json')['CAMPAIGN_AUTHORITY_APPLICABLE'],'activated':False,'edges':graph['EDGES'],'retry':0,'real_execution':{'systemd':False,'sudo':False,'bwrap':False,'H77':False,'A15':False}}
validate(s)
mutations=[('wrong repaired source',lambda x:x['sources']['SOURCES'][0].update(SOURCE_SHA256='0'*64)),('root cap on ordinary',lambda x:x.update(ordinary=207444)),('runtime without execution',lambda x:x.update(runtime='ADMITTED')),('store promoted',lambda x:x.update(store_verified=True)),('directory barrier omitted',lambda x:x.update(dir_fsync=False)),('unbounded children',lambda x:x.update(children=3)),('missing hard timeout',lambda x:x.update(hard_timeout_required=False)),('missing cumulative accounting',lambda x:x.update(cumulative_accounting_required=False)),('unverified observer promoted',lambda x:x.update(observer_qualified=True)),('effectiveness as activation',lambda x:x.update(authority='UNCONDITIONAL')),('future pids dependency',lambda x:x['edges'].append({'from':'BASIC_RESOURCE_CONTROLS','to':'HOST_PIDS_QUALIFICATION','type':'INVALID'})),('retry enabled',lambda x:x.update(retry=1)),('real system tools',lambda x:x['real_execution'].update(systemd=True,sudo=True,bwrap=True)),('H77 A15 included',lambda x:x['real_execution'].update(H77=True,A15=True)),('premature activation',lambda x:x.update(activated=True))]
results=[]
for name,mut in mutations:
 x=copy.deepcopy(s);mut(x)
 try:validate(x)
 except ValueError as e:results.append({'CONTROL':name,'RESULT':'REJECTED','CAUSE':str(e)})
 else:raise ValueError('negative accepted:'+name)
lessons=read(R/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');prev='0'*64
for e in lessons['EVENTS']:
 require(e['PREVIOUS_EVENT_HASH']==prev,'lesson linkage');body={k:v for k,v in e.items() if k!='EVENT_HASH'};require(hashlib.sha256(json.dumps(body,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()==e['EVENT_HASH'],'lesson hash');prev=e['EVENT_HASH']
require(prev=='885fd0eaceb15847201dfd058217682741fb43c255298713ccbc1e7251eec791','LL11 head')
require(digest(B/'campaign-budget.jsonl')=='3491e9003e1a016dbc4208e3963f8abea0f98c439dc892aa89a3811e73d528eb','stopped journal')
reconstruction={'SOURCE_IDENTITIES':manifest['SOURCES'],'FIXTURE_IDENTITY':fixture['IDENTITY'],'ORACLE_IDENTITY':oracle['IDENTITY'],'LIMITS':read(O/'resource-enforcement-matrix.json')['APPROVED_LIMITS'],'ROOT_MAX':207444,'ORDINARY_MAX':65536,'EXACT_TEST_NAMES':sorted(names),'GRAPH_ACYCLIC':acyclic(s['edges']),'LL11_HEAD':prev,'DECISION_READY':False,'EXECUTION_READY':False,'RUNTIME':'NOT_TESTED','NEGATIVES':results,'CONTRACT_PINS':{n:digest(O/n) for n in ['runtime-entry-admission-contract.json','disposable-store-qualification-contract.json','resource-enforcement-matrix.json','controller-observer-contract.json','prospective-campaign-authority-assessment.json','remaining-gap-dossier.json']},'ASSURANCE':'metadata and AST only; no target imports/execution or OS enforcement tests'}
print(json.dumps({'PYTHONHASHSEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':reconstruction,'SEMANTIC_SHA256':hashlib.sha256(canonical(reconstruction)).hexdigest()},sort_keys=True))
