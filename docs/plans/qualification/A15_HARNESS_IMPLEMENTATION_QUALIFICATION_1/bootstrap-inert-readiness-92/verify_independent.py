"""Independent AST/JSON reconstruction; no encoder or target import/execution."""
import ast,copy,hashlib,json,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];OUT=Path(__file__).resolve().parent;BASE=OUT.parent
P91=BASE/'minimal-bootstrap-construction-91';OLD=BASE/'bootstrap-trust-authority-89'
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def identity(x,ns):return {'kind':'CONTENT_IDENTITY','namespace':ns,'sha256':hashlib.sha256(canon(x)).hexdigest()}
def read(p):return json.loads(p.read_text())
def checkseal(v):assert set(v)=={'CONTENT','IDENTITY'} and identity(v['CONTENT'],v['IDENTITY']['namespace'])==v['IDENTITY']
def acyclic(g):
 nodes=set(g['NODES']);adj={n:[] for n in nodes}
 for e in g['EDGES']:assert e['from'] in nodes and e['to'] in nodes;adj[e['from']].append(e['to'])
 gray=set();done=set()
 def walk(n):
  assert n not in gray,'cycle'
  if n in done:return
  gray.add(n)
  for dep in adj[n]:walk(dep)
  gray.remove(n);done.add(n)
 for n in nodes:walk(n)
 return True
source=read(P91/'source-identity-manifest.json');pins={s['SOURCE_PATH']:s['SOURCE_SHA256'] for s in source['SOURCES']}
subject=read(OLD/'proposed-construction-test-authority-subject.json');spec=read(OLD/'inert-synthetic-qualification-specification.json')
ids=subject['EXACT_SYNTHETIC_TESTS'];assert len(ids)==14
text=(ROOT/list(pins)[1]).read_text();tree=ast.parse(text)
methods=[n.name for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name.startswith('test_')]
assert set(methods)=={'test_'+i[4:] for i in ids} and len(methods)==14
core=ast.parse((ROOT/list(pins)[0]).read_text())
limits_assign=next(n for n in core.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='LIMITS' for t in n.targets))
assert ast.literal_eval(limits_assign.value)==subject['RESOURCE_LIMITS']
for name in ('construct_inputs.py','construct_contracts.py'):
 t=ast.parse((OUT/name).read_text())
 assert not any(isinstance(n,ast.ImportFrom) and n.module and n.module.startswith('adapter') for n in ast.walk(t))
 assert not any(isinstance(n,ast.Import) and any(a.name.startswith('adapter') for a in n.names) for n in ast.walk(t))
fm=read(OUT/'sealed-synthetic-fixture-manifest.json');om=read(OUT/'independent-oracle-manifest.json')
bundle={'source_pins':pins,'fixtures':fm,'oracles':om,'graph':read(OUT/'acyclic-bootstrap-qualification-graph.json'),'store':read(OUT/'disposable-store-contract.json'),'resources':read(OUT/'resource-enforcement-matrix.json'),'controller':read(OUT/'controller-observer-contract.json'),'authority':read(OUT/'campaign-authority-assessment.json'),'encoder_target_imports':False,'operations':['READ_ONLY_METADATA','STATIC_JSON_CONSTRUCTION'],'campaign_activated':False}
fields={'SCHEMA_VERSION','INPUT_IDENTITY','TEST_ID','VARIANT','EXPECTED_CLAIM_RESULT','EXPECTED_CONSUMPTION_STATE','EXPECTED_DURABLE_RECORD','EXPECTED_CALLBACK_COUNT','EXPECTED_CALLBACK_ORDER','EXPECTED_FAILURE_CLASS','EXPECTED_FIRST_COUNTEREXAMPLE','EXPECTED_SECONDARY_FAILURES','EXPECTED_RETRY_ELIGIBILITY','EXPECTED_AUDIT_EVIDENCE','EXPECTED_RECOVERY','SOURCE_OBSERVATION_VECTOR','COMPARISON_RULE','ORACLE_COMPLETENESS','UNBOUND_FIELDS','DERIVATION_RULE','ADAPTER_OUTPUT_USED','EXCEPTION_FORMAT_ENTRY_RULE','CONCURRENT_COMPARISON'}
def validate(b):
 assert b['source_pins']==pins
 for p,h in b['source_pins'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
 assert not b['encoder_target_imports'] and b['operations']==['READ_ONLY_METADATA','STATIC_JSON_CONSTRUCTION'] and not b['campaign_activated']
 checkseal(b['fixtures']);checkseal(b['oracles'])
 fixtures=b['fixtures']['CONTENT']['FIXTURES'];oracles=b['oracles']['CONTENT']['ORACLES']
 assert len(fixtures)==len(oracles)==14 and [x['CONTENT']['TEST_ID'] for x in fixtures]==ids
 assert len({json.dumps(x['IDENTITY'],sort_keys=True) for x in fixtures})==14
 count=0;complete=0;runtime_keys=[]
 for fc,oc in zip(fixtures,oracles):
  checkseal(fc);checkseal(oc)
  assert fc['CONTENT']['EXPECTED_ORACLE_IDENTITY']==oc['IDENTITY']
  assert len(fc['CONTENT']['VARIANTS'])==len(oc['CONTENT']['VARIANTS'])
  partial=False
  for f,o in zip(fc['CONTENT']['VARIANTS'],oc['CONTENT']['VARIANTS']):
   checkseal(f);checkseal(o);x=f['CONTENT']['INPUT'];v=o['CONTENT'];count+=1
   assert set(v)==fields and v['EXPECTED_CALLBACK_ORDER'] is not None
   assert f['CONTENT']['INPUT_IDENTITY']==identity(x,'bootstrap-inert-input-v1')==v['INPUT_IDENTITY']
   assert f['CONTENT']['EXPECTED_ORACLE_IDENTITY']==o['IDENTITY']
   grant=x['SYNTHETIC_GRANT'];g=grant['content']
   assert grant['identity']==identity(g,'bootstrap-inert-grant-v1') and g['issuer']=='SYNTHETIC_ONLY_NOT_PROJECT_AUTHORITY'
   assert all(g[k]['namespace'].startswith('bootstrap-inert-') for k in ('subject_identity','retained_identity','command_identity','context_identity'))
   assert g['command_identity']==identity({'operation':'INERT_CALLBACK','argv':[]},'bootstrap-inert-command-v1')
   assert g['context_identity']==identity(x['SYNTHETIC_EXECUTION_CONTEXT'],'bootstrap-inert-context-v1')
   expected={'schema':'SYSTEM-PIDS-SINGLE-ATTEMPT-KEY-1','issued_grant_identity':grant['identity'],'approved_probe_subject_identity':g['subject_identity'],'retained_package86_subject_identity':g['retained_identity'],'exact_command_identity':g['command_identity'],'qualified_execution_context_identity':g['context_identity'],'authorized_attempt_number':1}
   assert x['CONSUMPTION_KEY_CONTENT']==expected and x['CONSUMPTION_KEY']==identity(expected,'qualification-h87-system-probe-consumption-key-v1')
   assert v['EXPECTED_RETRY_ELIGIBILITY'] is False and v['EXPECTED_RECOVERY']['launch_permitted'] is False and v['EXPECTED_RECOVERY']['retry_allowed'] is False
   assert v['ADAPTER_OUTPUT_USED'] is False
   if x['TEST_ID'] in ('B89-DUPLICATE_CONSUMPTION','B89-ZERO_RETRIES') and x['VARIANT']=='primary':
    message=str(FileExistsError(17,os.strerror(17),x['CONSUMPTION_KEY']['sha256']+'.claim.json'))
    assert v['EXPECTED_FIRST_COUNTEREXAMPLE']=={'type':'FileExistsError','message':message}
   if x['TEST_ID']=='B89-CONCURRENT_CLAIMS':
    policy=v['CONCURRENT_COMPARISON'];assert policy['WINNERS_EXACT']==1 and policy['CALLBACKS_EXACT']==1 and len(policy['ACCEPTED_HELPER_VECTORS'])==3
    assert policy['LOSER_FAILURES'][0]['message']==str(BlockingIOError(11,os.strerror(11)))
    assert policy['EXPECTED_FINAL_RECORDS']==v['EXPECTED_DURABLE_RECORD']
   if v['UNBOUND_FIELDS']:assert v['ORACLE_COMPLETENESS']=='PARTIAL';partial=True
   else:assert v['ORACLE_COMPLETENESS']=='COMPLETE_STATIC_VARIANT'
   for filename,raw_hex in v['EXPECTED_DURABLE_RECORD'].items():
    if not raw_hex:assert x['FAULT_CONFIGURATION']['point']=='DURING_CLAIM';continue
    doc=json.loads(bytes.fromhex(raw_hex))
    if filename.endswith('.claim.json'):
     assert doc['content']=={'schema':'BOOTSTRAP-CONSUMPTION-1','key':expected,'state':'CONSUMED'}
     assert doc['identity']==identity(doc['content'],'bootstrap-inert-consumption-record-v1')
    elif filename=='crash-witness.json':assert doc['point']==x['VARIANT'] and doc['retry_count']==0
    else:assert doc['schema']=='BOOTSTRAP-AUDIT-1' and doc['key']==x['CONSUMPTION_KEY'] and doc['phase'] in ('consumed','attempt','completed','unknown')
   runtime_keys.append((x['TEST_ID'],x['VARIANT'],x['CONSUMPTION_KEY']['sha256']))
  assert oc['CONTENT']['ORACLE_COMPLETENESS']==('PARTIAL' if partial else 'COMPLETE')
  if not partial:complete+=1
 assert count==21 and complete==14 and b['oracles']['CONTENT']['COMPLETE_CASES']==14
 for tid in ('B89-DUPLICATE_CONSUMPTION','B89-ZERO_RETRIES'):
  assert len({k for t,v,k in runtime_keys if t==tid})==1
 assert acyclic(b['graph'])
 s=b['store'];assert not s['CAMPAIGN_ROOT_CREATED'] and s['FILE_FSYNC'] and s['DIRECTORY_FSYNC'] and s['INDEPENDENT_REREAD']
 assert s['FILESYSTEM_TYPE']['active_store_type_mount_and_device']=='UNDETERMINED'
 assert b['resources']['EXACT_ISSUED_GRANT_LIMITS']==subject['RESOURCE_LIMITS']
 assert not b['resources']['ENFORCEMENT_VERIFIED'] and all(c['QUALIFIED'] is False for c in b['resources']['CONTROLS'])
 assert not b['controller']['CURRENT_COMPLETE'] and b['controller']['SOURCE_IDENTITIES']==pins
 assert b['controller']['TEST_SELECTION']==ids
 assert not b['authority']['CURRENT_ACTIVE_CAMPAIGN_ACTIVATED'] and not b['authority']['UNSELECTED_DOSSIER_CREATED'] and b['authority']['NO_RETRY_POLICY']==0
 return {'fixtures_logical':14,'runtime_variants':21,'complete_case_oracles':14,'graph_acyclic':True,'source_identities':pins,'active_ready':False,'decision_ready':False}
result=validate(bundle)
# Static negative controls mutate only documentary inputs; no target execution.
changes=[('wrong source',lambda b:b['source_pins'].update({next(iter(pins)):'0'*64})),('missing fixture',lambda b:b['fixtures']['CONTENT']['FIXTURES'].pop()),('duplicate fixture identity',lambda b:b['fixtures']['CONTENT']['FIXTURES'].__setitem__(1,b['fixtures']['CONTENT']['FIXTURES'][0])),('real grant input',lambda b:b['fixtures']['CONTENT']['FIXTURES'][0]['CONTENT']['VARIANTS'][0]['CONTENT']['INPUT']['SYNTHETIC_GRANT']['identity'].update(namespace='qualification-real-issued-grant-v1')),('bootstrap-derived oracle',lambda b:b.update(encoder_target_imports=True)),('missing callback witness',lambda b:b['oracles']['CONTENT']['ORACLES'][0]['CONTENT']['VARIANTS'][0]['CONTENT'].pop('EXPECTED_CALLBACK_ORDER')),('missing first failure',lambda b:b['oracles']['CONTENT']['ORACLES'][0]['CONTENT']['VARIANTS'][0]['CONTENT'].pop('EXPECTED_FIRST_COUNTEREXAMPLE')),('missing directory fsync',lambda b:b['store'].update(DIRECTORY_FSYNC=None)),('unverified control qualified',lambda b:b['resources']['CONTROLS'][0].update(QUALIFIED=True)),('unbounded test selection',lambda b:b['controller']['TEST_SELECTION'].append('UNAUTHORIZED_EXTRA_TEST')),('retry',lambda b:b['authority'].update(NO_RETRY_POLICY=1)),('circular dependency',lambda b:b['graph']['EDGES'].append({'from':'BASIC_RESOURCE_CONTROLS','to':'HOST_PIDS_QUALIFICATION','type':'CIRCULAR'})),('systemd sudo Bubblewrap',lambda b:b['operations'].append('SYSTEMD_SUDO_BWRAP_EXECUTION')),('H77 A15 execution',lambda b:b['operations'].append('H77_A15_EXECUTION')),('premature activation',lambda b:b.update(campaign_activated=True))]
negative=[]
for name,modify in changes:
 b=copy.deepcopy(bundle);modify(b)
 try:validate(b)
 except (AssertionError,KeyError,ValueError,TypeError):negative.append({'CONTROL':name,'RESULT':'REJECTED'})
 else:raise AssertionError('accepted negative '+name)
result['fixture_manifest_identity']=fm['IDENTITY'];result['oracle_manifest_identity']=om['IDENTITY'];result['negative_controls']=negative
result['source_only_review']=True;result['target_imports_or_execution']=0
result['contract_identities']={name:identity(read(OUT/name),'bootstrap-inert-92-contract-reconstruction-v1') for name in ('entry-authentication.json','fourteen-test-inventory.json','disposable-store-contract.json','durability-qualification-requirements.json','resource-enforcement-matrix.json','controller-observer-contract.json','acyclic-bootstrap-qualification-graph.json','campaign-authority-assessment.json','entry-size-compatibility.json','exception-format-profile.json','oracle-and-fixture-binding-assessment.json','remaining-gap-dossier.json','lessons-register-review.json')}
print(json.dumps({'SEMANTIC_IDENTITY':identity(result,'bootstrap-inert-92-independent-reconstruction-v1'),'RECONSTRUCTION':result},sort_keys=True))
