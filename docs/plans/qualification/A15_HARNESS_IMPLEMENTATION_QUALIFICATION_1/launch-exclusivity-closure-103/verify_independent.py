"""Read-only103 metadata,keys,scope reconstruction;no source/probe implementation."""
import ast,copy,hashlib,json,os,pathlib
R=pathlib.Path(__file__).resolve().parents[5];B=R/'docs/plans/qualification/A15_HARNESS_IMPLEMENTATION_QUALIFICATION_1';O=pathlib.Path(__file__).parent

def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def require(x,m):
 if not x:raise ValueError(m)
def acyclic(es):
 d={}
 for e in es:d.setdefault(e['from'],[]).append(e['to'])
 active=set();done=set()
 def v(n):
  if n in active:return False
  if n in done:return True
  active.add(n)
  for w in d.get(n,[]):
   if not v(w):return False
  active.remove(n);done.add(n);return True
 return all(v(n) for n in d)
a=read(O/'entry-authentication.json')
for folder in a['PRIOR_INDICES_VERIFIED']:
 for n,h in read(B/folder/'evidence-index.json').get('FILES',{}).items():
  if isinstance(h,str):require(sha(R/n if (R/n).is_file() else B/folder/n)==h,'prior pin')
for p,h in a['SOURCE_IDENTITIES'].items():require(sha(R/p)==h,'old source')
for r in a['GRANT_REFERENCES']:
 require(sha(R/r['path'])==r['raw_sha256'],'effective ref');ref=read(R/r['path']);p=ref['GRANT_RECORD_PIN'];require(sha(R/p['path'])==p['raw_sha256'],'issued pin');g=read(R/p['path']);body=g.get('CONTENT',g.get('RECORD'));require(hashlib.sha256(enc(body)).hexdigest()==r['identity']['sha256'],'issued content')
 for p in ref['VERIFICATION_PINS']:require(sha(R/p['path'])==p['raw_sha256'],'issuance pin')
spec=read(B/'system-process-enforcement-86/transient-service-specification.json');profile=read(O/'fixed-real-probe-profile.json');require(profile['ARGUMENT_VECTOR']==spec['EXACT_COMMAND_ARGV'] and profile['LIMITS']==spec['LIMITS'],'realprofileunchanged');require(hashlib.sha256(enc(profile['ARGUMENT_VECTOR'])).hexdigest()==profile['COMMAND_IDENTITY']['sha256'],'commandid');ast.parse(profile['ARGUMENT_VECTOR'][-1])
old=read(B/'fixed-command-bridge-102/logical-synthetic-identity-manifest.json');bud=read(O/'numeric-inert-controller-budget.json');sizes=[len(enc(f)) for f in old['CONTENT']['FIXTURES']];require(bud['FIXTURE_SIZES']==sizes and sum(sizes)==36710,'fixturebytes');require(len(enc(old))==bud['KNOWN_CANONICAL_MANIFEST_BYTES']==37056,'manifestbytes');require(bud['TOTAL_MAX_WRITTEN_BYTES'] is None and not bud['NUMERIC_INERT_BUDGET_COMPLETE'],'noinventedfullbudget')
oldpath=B/'fixed-command-bridge-102/logical-synthetic-identity-manifest.json';require(len(oldpath.read_bytes())==bud['ORIGINAL_RETAINED_MANIFEST_RAW_BYTES']==54273 and sha(oldpath)==bud['ORIGINAL_RETAINED_MANIFEST_RAW_SHA256'],'raw manifest differs from canonical')
mapping=read(O/'synthetic-consumption-mapping.json');require(len(mapping['MAPPINGS'])==12,'syntheticmappedcases')
for row in mapping['MAPPINGS']:
 oldf=next(f for f in old['CONTENT']['FIXTURES'] if f['CONTENT']['TEST_ID']==row['TEST_ID']);require(row['ORIGINAL102_FIXTURE_IDENTITY']==oldf['IDENTITY'],'fixturepreservation');require(row['SYNTHETIC_GRANT_IDENTITY']==oldf['CONTENT']['SYNTHETIC_GRANT']['IDENTITY'],'grantunchanged');require(hashlib.sha256(enc(row['NEW_KEY_BODY'])).hexdigest()==row['NEW_KEY_IDENTITY']['sha256'],'key');require(row['UNCHANGED_GRANT_ANCHOR']==oldf['CONTENT']['GRANT_ANCHOR'],'anchorunchanged');require('qualified_direct_host_context_identity' in row['NEW_KEY_BODY'] and 'retained_package86_subject_identity' in row['NEW_KEY_BODY'],'87bindingspreserved')
identity=read(O/'stable-consumption-identity.json');require(identity['ACTUAL_REAL_GRANT_OR_KEY'] is None and not identity['APPROVED_ACTIVE_SCHEMA'],'nofuturegrant')
source=read(O/'two-file-source-boundary.json');require(source['PATHS']==a['PACKAGE102_SOURCE_PATHS'] and len(source['PATHS'])==2 and not any((R/p).exists() for p in source['PATHS']),'sourceboundary')
scope=read(O/'twelve-property-inert-scope.json');require([x['TEST_ID'] for x in scope['EXACT_PROPERTIES']]==a['PACKAGE102_PROPERTIES'] and len(scope['EXACT_PROPERTIES'])==12,'casepreservation')
reg=read(R/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');prev='0'*64
for e in reg['EVENTS']:
 require(e['PREVIOUS_EVENT_HASH']==prev,'lessonprevious');require(hashlib.sha256(json.dumps({k:v for k,v in e.items() if k!='EVENT_HASH'},sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()==e['EVENT_HASH'],'lessonhash');prev=e['EVENT_HASH']
require(prev==a['LL11_HEAD'],'head');require(sha(B/'campaign-budget.jsonl')==a['STOPPED_JOURNAL_SHA256'],'journal')
graph=read(O/'qualification-dependency-graph.json');require(acyclic(graph['EDGES']),'acyclic')
s={'hostwide_binding':False,'hostwide_enforcement_supported':False,'attestation_is_exclusive':False,'duplicate_consumption':False,'reusable_token':False,'unknown_reopens':False,'store_binding_required':True,'directory_fsync_required':True,'numeric_budget_without_derivation':False,'enforcement_promoted':False,'real_systemd_enabled':False,'grant90_as_newauthority':False,'graph':graph['EDGES'],'paths':source['PATHS'],'H77A15':False,'authority_issued':False}
def valid(x):
 require(not x['hostwide_binding'] or x['hostwide_enforcement_supported'],'hostwidebindingnarrowed');require(not x['attestation_is_exclusive'],'attestationastechnicalexclusivity');require(not x['duplicate_consumption'],'duplicate');require(not x['reusable_token'],'reusabletoken');require(not x['unknown_reopens'],'unknownreopens');require(x['store_binding_required'],'storeunbound');require(x['directory_fsync_required'],'directorybarrieromitted');require(not x['numeric_budget_without_derivation'],'arbitrarynumericcap');require(not x['enforcement_promoted'],'unverifiedenforcement');require(not x['real_systemd_enabled'],'reallaunch');require(not x['grant90_as_newauthority'],'wronggrant');require(acyclic(x['graph']),'cycle');require(x['paths']==source['PATHS'],'unauthorizedpath');require(not x['H77A15'],'H77A15');require(not x['authority_issued'],'prematureissue')
valid(s)
mut=[('hostwiderequirementsilentlynarrowed','hostwide_binding',True),('ownerattestationtechnicalexclusivity','attestation_is_exclusive',True),('duplicategrantconsumption','duplicate_consumption',True),('reusabletoken','reusable_token',True),('unknownreopens','unknown_reopens',True),('unboundstore','store_binding_required',False),('missingdirectoryfsync','directory_fsync_required',False),('arbitrarynumericlimit','numeric_budget_without_derivation',True),('unverifiedenforcementqualified','enforcement_promoted',True),('realsystemd','real_systemd_enabled',True),('90grantnewauthority','grant90_as_newauthority',True),('qualificationcycle','graph',graph['EDGES']+[{'from':'BOUNDED_CONSTRUCTOR_RESOURCE_OBSERVER_PROFILE','to':'BRIDGE_INERT_QUALIFICATION'}]),('unauthorizedsource','paths',source['PATHS']+['adapter/unauthorized.py']),('H77A15','H77A15',True),('prematureissuance','authority_issued',True)]
neg=[]
for name,k,v in mut:
 x=copy.deepcopy(s);x[k]=v
 try:valid(x)
 except ValueError as e:neg.append({'CONTROL':name,'RESULT':'REJECTED','CAUSE':str(e)})
 else:raise ValueError('accepted:'+name)
r={'COMMAND_IDENTITY':profile['COMMAND_IDENTITY'],'EXCLUSIVITY_DOMAIN_RESOLVED':False,'A_GRANTLEVEL_BINDING':True,'B_QUALIFICATION_CONTEXT_REQUIRED':True,'C_ISSUED_HOSTWIDE_RULE_FOUND':False,'HOST_ROLE_QUALIFIED':False,'KEY_RULE_PRESERVES87_AND102':True,'REAL_KEY':None,'INERT_PROPERTIES':12,'LOGICAL_MANIFEST_BYTES':37056,'LOGICAL_FIXTURE_SUM':36710,'NUMERIC_INERT_BUDGET_COMPLETE':False,'SOURCE_PATHS':source['PATHS'],'GRAPH_ACYCLIC':True,'DECISION_READY':False,'LL11_HEAD':prev,'NEGATIVES':neg,'CONTRACT_PINS':{p.name:sha(p) for p in O.glob('*.json') if p.name not in ['preservation-before.json','independent-static-verification.json','four-seed-reconstruction.json','negative-control-results.json','governance-authentication.json','report.json','preservation-audit.json','evidence-index.json']},'ASSURANCE':'metadata/schema/policy-read/staticscope reconstruction only;notOSpermission/exclusivityoractiveclaimenforcement'}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':r,'SEMANTIC_SHA256':hashlib.sha256(enc(r)).hexdigest()},sort_keys=True))
