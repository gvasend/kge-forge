"""Independent source/JSON reconstruction. Does not import or execute targets."""
import ast,copy,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];OUT=Path(__file__).resolve().parent;BASE=OUT.parent
PATHS=['adapter/qualification_bootstrap/systemd_pids_once.py','adapter/tests/test_systemd_pids_bootstrap.py']
core=(ROOT/PATHS[0]).read_text();tests=(ROOT/PATHS[1]).read_text()
def digest(raw):return hashlib.sha256(raw).hexdigest()
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def functions(source):return {n.name:n for n in ast.walk(ast.parse(source)) if isinstance(n,ast.FunctionDef)}
def segment(source,name):return ast.get_source_segment(source,functions(source)[name])
def check(c,t):
 ct=ast.parse(c);tt=ast.parse(t);constants={}
 for n in ct.body:
  if isinstance(n,ast.Assign):
   try:value=ast.literal_eval(n.value)
   except (ValueError,TypeError):continue
   for name in n.targets:
    if isinstance(name,ast.Name):constants[name.id]=value
 assert constants['ROOT_ENTRY_MAX_BYTES']==207444 and constants['ORDINARY_RECORD_MAX_BYTES']==65536
 assert constants['ROOT_ENTRY_SCHEMA']=='BOOTSTRAP-INERT-ENTRY-93-V2'
 assert constants['SOURCE_PATHS']==PATHS
 assert constants['REAL_PROBE_BINDING'] is None and constants['LIMITS']==json.loads((BASE/'bootstrap-trust-authority-89/proposed-construction-test-authority-subject.json').read_text())['RESOURCE_LIMITS']
 ordinary=segment(c,'read_at');root=segment(c,'read_root_entry');decode=segment(c,'decode_root_bytes')
 assert 'ROOT_ENTRY_MAX_BYTES' not in ordinary and 'ORDINARY_RECORD_MAX_BYTES + 1' in ordinary
 assert 'len(raw) <= ORDINARY_RECORD_MAX_BYTES' in ordinary and 'min(4096, remaining)' in ordinary
 assert root.index('verify_repair_authority()')<root.index('os.open(')
 assert "path == expected" in root and "'entry.json'" in root and 'ROOT_ROLE_PATH' in root
 assert 'remaining = ROOT_ENTRY_MAX_BYTES + 1' in root and 'min(4096, remaining)' in root
 assert 'len(raw) <= ROOT_ENTRY_MAX_BYTES' in root and root.index('len(raw) <= ROOT_ENTRY_MAX_BYTES')<root.index('decode_root_bytes(raw)')
 assert 'isinstance(raw, bytes)' in decode and 'len(raw) <= ROOT_ENTRY_MAX_BYTES' in decode and 'len(text)' not in decode
 assert decode.index('MAX_JSON_NODES')<decode.index('json.loads(')
 assert 'object_pairs_hook=_unique_object' in decode and 'parse_float=_invalid_number' in decode and 'raw == canonical(value)' in decode
 assert 'ROOT_ENTRY_TYPE' in root and 'ROOT_ENTRY_SCHEMA' in root
 auth=segment(c,'authorize_campaign');assert 'manifest = read_root_entry(entry_pin)' in auth and 'repair_reference' in auth and 'verify_entry_repair_reference(manifest)' in auth
 assert 'REAL_PROBE_GRANT' in segment(c,'verify_repair_authority') and 'A15_EXECUTION_GRANT' in segment(c,'verify_repair_authority')
 tf=functions(t);names=sorted(n for n in tf if n.startswith('test_'));assert len(names)==14
 previous=functions((OUT/'previous-source-1.txt').read_text());assert set(names)=={n for n in previous if n.startswith('test_')}
 concurrent=segment(t,'compare_concurrent_snapshots')
 for item in ('assertLessEqual(successes, 1)','assertLessEqual(callbacks, 1)','final.startswith(actual)','set(item[\'records\']) <= set(expected)','compare_record_state(case, fixture)'):assert item in concurrent,item
 state=segment(t,'compare_record_state')
 for item in ("fixture['expected_records']", "fixture['expected_consumption_state']", "fixture['expected_recovery']", "observed_recovery['launch_permitted']", "observed_recovery['retry_allowed']", "audit['schema']"):assert item in state,item
 crash=segment(t,'test_CRASH_AFTER_CONSUMPTION');assert 'compare_record_state(self, fixture)' in crash and "assertEqual(recovery, fixture['expected_recovery'])" in crash
 controller=segment(t,'run')
 for item in ("receipt['deadline'] - time.monotonic()", "'wait_observed'", "'raw_sha256'", "'fixture_id'", "'status'", 'causal.bootstrap_secondary',"'PYTHONNOUSERSITE': '1'"):assert item in controller,item
 assert "'PYTHONPATH':" not in controller
 campaign=segment(t,'run_campaign');assert 'TextTestRunner(stream=stream, failfast=True)' in campaign and 'BoundedParentStream' in campaign
 assert 'primary_stream_error.bootstrap_secondary' in campaign and 'result_error.bootstrap_secondary' in campaign and 'original.bootstrap_first' in campaign
 assert "'AUTOMATIC_RETRIES': 0" in c and 'os.unlink(' not in c and 'rmtree' not in t
 assert not any(isinstance(n,ast.Import) and any(a.name=='subprocess' for a in n.names) for n in ast.walk(ct))
 assert not any(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('eval','exec','compile') for tree in (ct,tt) for n in ast.walk(tree))
 # Consumption key and irreversible launch core preserved byte-for-byte.
 before=(OUT/'previous-source-0.txt').read_text()
 for name in ('consumption_key','consume_inert','recover_inert','confirm_consumption','_validate'):
  assert ast.dump(functions(c)[name],include_attributes=False)==ast.dump(functions(before)[name],include_attributes=False),name
 return {'constants':constants,'test_names':names}
base=check(core,tests)
mutations=[('root cap applied to ordinary',0,'info.st_size <= ORDINARY_RECORD_MAX_BYTES','info.st_size <= ROOT_ENTRY_MAX_BYTES'),('root type spoofing',0,'path == expected','True'),('root over207444',0,'ROOT_ENTRY_MAX_BYTES = 207444','ROOT_ENTRY_MAX_BYTES = 207445'),('ordinary over65536',0,'ORDINARY_RECORD_MAX_BYTES = 65536','ORDINARY_RECORD_MAX_BYTES = 65537'),('character count substituted',0,'isinstance(raw, bytes) and len(raw)','isinstance(raw, bytes) and len(raw.decode())'),('unbounded read',0,'min(4096, remaining)','99999999'),('missing authority',0,'    verify_repair_authority()  # Happens BEFORE the enlarged-size operation.','    pass  # authority omitted'),('missing concurrent snapshot',1,'final.startswith(actual)','True'),('missing crash/recovery comparison',1,"assertEqual(recovery, fixture['expected_recovery'])","assertTrue(True)"),('duplicate callback accepted',1,'assertLessEqual(callbacks, 1)','assertLessEqual(callbacks, 2)'),('missing first cause',1,'original.bootstrap_first','original.replaced_first'),('retry allowed',0,"'AUTOMATIC_RETRIES': 0","'AUTOMATIC_RETRIES': 1"),('unauthorized source',0,"'adapter/tests/test_systemd_pids_bootstrap.py'","'adapter/tests/other.py'"),('real subprocess API',0,'import fcntl','import subprocess\nimport fcntl'),('H77 A15 real binding',0,'REAL_PROBE_BINDING = None','REAL_PROBE_BINDING = True')]
negative=[]
for name,which,old,new in mutations:
 c,t=core,tests
 assert old in (c if which==0 else t),name
 if which==0:c=c.replace(old,new)
 else:t=t.replace(old,new)
 try:check(c,t)
 except (AssertionError,KeyError,ValueError,TypeError,SyntaxError):negative.append({'CONTROL':name,'RESULT':'REJECTED'})
 else:raise AssertionError('accepted static negative '+name)
guard=json.loads((OUT/'fresh-construction-entry.json').read_text());assert guard['RESULT']=='PASS'
ref=json.loads((BASE/'bootstrap-repair-grant-issuance-94/effective-bootstrap-repair-grant-reference.json').read_text());assert ref['REPAIR_GRANT_EFFECTIVE']
for p in ref['VERIFICATION_PINS']:assert digest((ROOT/p['path']).read_bytes())==p['raw_sha256']
assert digest((ROOT/ref['GRANT_RECORD_PIN']['path']).read_bytes())==ref['GRANT_RECORD_PIN']['raw_sha256']
rootmodels=BASE/'bootstrap-entry-oracle-closure-93';sample=json.loads((rootmodels/'inline-size-model-max.json').read_text())['ENTRY']
assert len(canon(sample))==207444 # Metadata model only, not passed to target.
reg=json.loads((ROOT/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json').read_text());head='0'*64
for e in reg['EVENTS']:
 body={k:v for k,v in e.items() if k!='EVENT_HASH'}
 assert e['PREVIOUS_EVENT_HASH']==head and digest(json.dumps(body,sort_keys=True,separators=(',',':')).encode())==e['EVENT_HASH'];head=e['EVENT_HASH']
assert head=='885fd0eaceb15847201dfd058217682741fb43c255298713ccbc1e7251eec791'
result={'SOURCE_PINS':{p:digest((ROOT/p).read_bytes()) for p in PATHS},'ROOT_ENTRY_MAX_BYTES':207444,'ORDINARY_RECORD_MAX_BYTES':65536,'ROOT_SCHEMA':'BOOTSTRAP-INERT-ENTRY-93-V2','ORACLE_COMPARISON_FUNCTIONS':['store_snapshot','compare_record_state','compare_concurrent_snapshots'],'ORIGINAL_TESTS_PRESERVED':base['test_names'],'CONSUMPTION_ALGORITHM_AST_UNCHANGED':True,'NEGATIVES':negative,'LL11_HEAD':head,'ACTIVE_TEST_READY':False,'RUNTIME_ENTRY_ADMISSION':'NOT_TESTED','TARGET_MODULE_IMPORTS_OR_EXECUTION':0,'ASSURANCE':'Independent AST/binding/retained JSON check; not behavioral or OS-enforcement evidence'}
print(json.dumps({'RECONSTRUCTION':result,'SEMANTIC_IDENTITY':{'kind':'CONTENT_IDENTITY','namespace':'bootstrap-entry-oracle-repair-95-static-v1','sha256':digest(canon(result))}},sort_keys=True))
