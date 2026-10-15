"""110 independent AST/JSON reconstruction, no payload/target execution."""
import pathlib,json,hashlib,ast,copy,os
O=pathlib.Path(__file__).resolve().parent;R=O.parents[4]
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
a=read(O/'entry-authentication.json')
for p,h in a['PINS'].items():assert sha(R/p)==h
c=read(O/'exact-retained-command-authentication.json');s=read(O.parent/'system-process-enforcement-86/transient-service-specification.json');argv=c['COMMAND_ARGUMENT_VECTOR'];assert argv==s['EXACT_COMMAND_ARGV']
assert hashlib.sha256(enc(argv)).hexdigest()==c['COMMAND_CONTENT_IDENTITY']['sha256']=='e628c8664ea72357963dc58dddee934c28cad3ab5c84450656a6595e6910fb50'
assert hashlib.sha256(argv[-1].encode()).hexdigest()==c['PAYLOAD_RAW_SHA256'];ast.parse(argv[-1]);assert argv[-1]==(O.parent/'system-process-enforcement-86/prospective-payload.txt').read_text()
assert not any(x.startswith('--property=CPUQuota') for x in argv) and '--property=LimitCPU=5' in argv
p=read(O/'numerical-safety-profile.json');assert p['SERVICE_RUNTIME_LIMIT_SECONDS']==20 and p['STOP_TIMEOUT_SECONDS']==2 and p['OBSERVER_WINDOW_SECONDS']==25
assert p['P86_LIMITS']==s['LIMITS'] and p['PUBLICATION_CAP_BYTES']==65536 and not p['RESOURCE_CONFIGURATION_COMPLETE']
for path,h in read(O/'installed-property-documentation-pins.json')['PINS'].items():assert sha(pathlib.Path(path))==h
assert not read(O/'one-attempt-consumption-requirements.json')['QUALIFIED_LAUNCHER_AVAILABLE']
assert not read(O/'independent-observer-contract.json')['CONTRACT_COMPLETE']
assert not read(O/'bounded-evidence-publication-contract.json')['CONTRACT_COMPLETE']
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
state={'command':c['COMMAND_CONTENT_IDENTITY']['sha256'],'unapproved_expansion':False,'unsupported_property':False,'unjustified_limit':False,'user_cgroup_as_service':False,'kernel_inferred':False,'metadata_as_behavior':False,'attestation_as_permission':False,'unit_as_consumption':False,'unqualified_observer':False,'unknown_exit_success':False,'circular_authority':False,'service_created':False,'h77_a15':False}
def valid(x):
 if x['command']!=c['COMMAND_CONTENT_IDENTITY']['sha256']:raise ValueError('wrong_command')
 for k,v in x.items():
  if k!='command' and v:raise ValueError(k)
valid(state);neg=[]
for k in state:
 x=copy.deepcopy(state);x[k]='wrong' if k=='command' else True
 try:valid(x)
 except ValueError as e:neg.append({'CONTROL':k,'RESULT':'REJECTED','CAUSE':str(e)})
 else:raise AssertionError(k)
names=['entry-authentication.json','exact-retained-command-authentication.json','exact-unit-and-scope-assessment.json','systemd-cgroup-v1-property-matrix.json','numerical-safety-profile.json','administrative-permission-contract.json','one-attempt-consumption-requirements.json','independent-observer-contract.json','kernel-metadata-comparison-specification.json','bounded-evidence-publication-contract.json','failure-matrix.json','authority-applicability-assessment.json','qualification-dependency-graph.json','remaining-gap-dossier.json']
s={'PINS':{n:sha(O/n) for n in names},'EXACT_ORIGINAL_COMMAND_IDENTITY':c['COMMAND_CONTENT_IDENTITY'],'GRAPH_ACYCLIC':True,'LL11_HEAD':prev,'HOST_VERIFICATION_DECISION_READY':False,'NEGATIVES':neg}
print(json.dumps({'HASH_SEED':os.environ.get('PYTHONHASHSEED'),'RECONSTRUCTION':s,'SEMANTIC_SHA256':hashlib.sha256(enc(s)).hexdigest()},sort_keys=True))
