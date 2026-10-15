"""Independent metadata reader: AST/JSON only, no target/designer import."""
import ast,copy,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];OUT=Path(__file__).resolve().parent;BASE=OUT.parent;P92=BASE/'bootstrap-inert-readiness-92';P91=BASE/'minimal-bootstrap-construction-91'
def read(p):return json.loads(p.read_text())
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def aid(v,ns):return {'kind':'CONTENT_IDENTITY','namespace':ns,'sha256':hashlib.sha256(canon(v)).hexdigest()}
def pin(p):return {'path':str(p.relative_to(ROOT)),'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
idx=read(P92/'evidence-index.json')
for p,h in idx['FILES'].items():assert pin(P92/p)['raw_sha256']==h
for p,h in idx['SOURCE_PINS'].items():assert pin(ROOT/p)['raw_sha256']==h
old=read(BASE/'bootstrap-trust-authority-89/proposed-construction-test-authority-subject.json')
size=read(OUT/'entry-size-analysis.json');amin=read(OUT/'inline-size-model-min.json');amax=read(OUT/'inline-size-model-max.json')
assert amin['MODEL_ONLY_NOT_EXECUTABLE'] and amax['MODEL_ONLY_NOT_EXECUTABLE']
mn=amin['ENTRY'];mx=amax['ENTRY'];exact_min=len(canon(mn));exact_max=len(canon(mx))
assert size['MODEL_MIN_BYTES']==exact_min and size['MODEL_MAX_BYTES']==exact_max and size['ACTUAL_FINAL_RUNTIME_ENTRY_BYTES'] is None
assert size['AUTHENTICATED_REQUIRED_INLINE_LOWER_BOUND_BYTES']==108353 and size['EXCESS_BYTES_AT_LEAST']==42817
assert size['EXACT_SIZE_FORMULA']['BASE_FIXED_BYTES']+42==exact_min and exact_max==size['EXACT_SIZE_FORMULA']['BASE_FIXED_BYTES']+42*20
assert set(mn)==set(mx) and len(mx['fixtures'])==21
for key in mn['fixtures']:
 a=copy.deepcopy(mn['fixtures'][key]);b=copy.deepcopy(mx['fixtures'][key])
 assert a['entry']['store_device']==a['entry']['store_inode']==1
 assert b['entry']['store_device']==b['entry']['store_inode']==2**64-1
 for n in ('store_device','store_inode'):a['entry'].pop(n);b['entry'].pop(n)
 assert a==b
for name in ('construct_design.py','construct_authority.py'):
 t=ast.parse((OUT/name).read_text());assert not any(isinstance(n,ast.ImportFrom) and n.module and n.module.startswith('adapter') for n in ast.walk(t))
scope=read(OUT/'minimal-source-change-assessment.json');sp={x['SOURCE_PATH']:x['CURRENT_SOURCE_IDENTITY']['sha256'] for x in scope['EXACT_SOURCE_FILES']}
assert sp==idx['SOURCE_PINS'] and list(sp)==old['EXACT_SOURCE_PATHS'] and not scope['SOURCE_CHANGE_PERFORMED']
for p,h in sp.items():assert pin(ROOT/p)['raw_sha256']==h
# Authenticate existing private reader's constant without importing it.
ct=ast.parse((ROOT/list(sp)[0]).read_text());literals=[n.value for n in ast.walk(ct) if isinstance(n,ast.Constant)]
assert 65536 in literals
reg=read(ROOT/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');head='0'*64
for e in reg['EVENTS']:
 body={k:v for k,v in e.items() if k!='EVENT_HASH'}
 assert e['PREVIOUS_EVENT_HASH']==head and hashlib.sha256(json.dumps(body,sort_keys=True,separators=(',',':')).encode()).hexdigest()==e['EVENT_HASH'];head=e['EVENT_HASH']
assert head=='885fd0eaceb15847201dfd058217682741fb43c255298713ccbc1e7251eec791'
assert reg['EVENTS'][-1]['LESSON']['LESSON_ID']=='LL-11'
assert pin(BASE/'campaign-budget.jsonl')['raw_sha256']=='3491e9003e1a016dbc4208e3963f8abea0f98c439dc892aa89a3811e73d528eb'
f=read(P92/'sealed-synthetic-fixture-manifest.json');o=read(P92/'independent-oracle-manifest.json')
assert len(f['CONTENT']['FIXTURES'])==len(o['CONTENT']['ORACLES'])==14
for env in (f,o):assert aid(env['CONTENT'],env['IDENTITY']['namespace'])==env['IDENTITY']
def graph_acyclic(g):
 adj={n:[] for n in g['NODES']};gray=set();done=set()
 for e in g['EDGES']:assert e['from'] in adj and e['to'] in adj;adj[e['from']].append(e['to'])
 def dfs(n):
  assert n not in gray,'cycle'
  if n in done:return
  gray.add(n)
  for v in adj[n]:dfs(v)
  gray.remove(n);done.add(n)
 for n in adj:dfs(n)
 return True
bundle={n:read(OUT/n) for n in ('entry-size-analysis.json','candidate-a-bounded-enlargement.json','candidate-b-immutable-references.json','candidate-b-root-size-model.json','candidate-b-leaf-size-models.json','executable-oracle-bindings.json','minimal-source-change-assessment.json','bootstrap-trust-dependency-graph.json','proposed-repair-authorization-subject.json','unselected-repair-authorization-dossier.json')}
expected_pairs={(v['CONTENT']['INPUT']['TEST_ID'],v['CONTENT']['INPUT']['VARIANT']) for fc in f['CONTENT']['FIXTURES'] for v in fc['CONTENT']['VARIANTS']}
def validate(z):
 s=z['entry-size-analysis.json'];a=z['candidate-a-bounded-enlargement.json'];b=z['candidate-b-immutable-references.json']
 assert s['ACTUAL_FINAL_RUNTIME_ENTRY_BYTES'] is None and s['MODEL_MAX_BYTES']==exact_max and s['MODEL_MIN_BYTES']==exact_min
 assert a['NEW_MAX_ENTRY_BYTES']==a['MAX_SERIALIZED_CAMPAIGN_BYTES']==exact_max
 assert a['PRIVATE_RECORD_LIMIT_UNCHANGED']==65536 and a['SOURCE_CHANGE_SCOPE']==list(sp)
 assert a['MEMORY_IMPACT']['child_address_space_limit']==old['RESOURCE_LIMITS']['CHILD_ADDRESS_SPACE_BYTES']
 assert a['CAMPAIGN_INPUT_AND_EVIDENCE_ENVELOPE']['total_ceiling']==1048576
 assert a['CAMPAIGN_INPUT_AND_EVIDENCE_ENVELOPE']['remaining_for_epochs_receipts_private_audits_accounting_and_critical_evidence']==1048576-655360-65536-exact_max
 leaves=z['candidate-b-leaf-size-models.json']['LEAVES'];assert len(leaves)==b['REFERENCE_COUNT']==b['MAX_REFERENCE_COUNT']==21 and b['MAX_REFERENCE_DEPTH']==1
 ro=z['candidate-b-root-size-model.json'];assert len(canon(ro['ROOT']))==b['ROOT_ENTRY_MODEL_BYTES']<=65536
 assert ro['SOURCE_ROOT_SPEC']['readonly_required'] and ro['SOURCE_ROOT_SPEC']['source_must_be_unwritable_by_test_actor_including_aliases']
 assert aid(ro['SOURCE_ROOT_SPEC'],'bootstrap-inert-reference-source-root-rule-v1')==b['SOURCE_ROOT_IDENTITY']
 total=0
 for l in leaves:
  raw=canon(l['payload']);h=hashlib.sha256(raw).hexdigest()
  assert h==l['raw_sha256']==l['canonical_sha256'] and len(raw)==l['bytes']<=65536
  assert l['identity']==aid(l['payload'],'bootstrap-runtime-fixture-ref-v1')
  assert l['path']=='objects/'+h+'.json'
  total+=len(raw)
 assert total==b['TOTAL_REFERENCED_BYTES']==b['MAX_REFERENCED_BYTES'] and total+len(canon(ro['ROOT']))==b['MAX_TOTAL_LOADED_BYTES']
 assert b['NO_ARBITRARY_OR_RECURSIVE_REFERENCE'] and not b['IMMUTABLE_SOURCE_AVAILABLE_OR_QUALIFIED_NOW']
 edges=b['MODEL_REFERENCE_GRAPH']['edges'];assert len(edges)==21 and all(src==b['ROOT_ENTRY_IDENTITY'] and target in b['DIRECT_REFERENCE_IDENTITIES'] for src,target in edges)
 assert b['MODEL_REFERENCE_GRAPH']['max_depth']==1 and b['MODEL_REFERENCE_GRAPH']['missing']==0
 bindings=z['executable-oracle-bindings.json'];assert bindings['SPECIFICATION_COMPLETE'] and not bindings['BEHAVIORALLY_QUALIFIED']
 assert len(bindings['VARIANTS'])==21 and {(v['TEST_ID'],v['RUNTIME_VARIANT']) for v in bindings['VARIANTS']}==expected_pairs
 for v in bindings['VARIANTS']:
  kinds={c['OBSERVATION'] for c in v['COMPARISONS']}
  assert {'request_and_consumption_identity','callback','durable_store','recovery','first_and_secondary_failure','audit'}<=kinds
  assert v['EXPECTED_RECOVERY_RESULT']['launch_permitted'] is False and v['EXPECTED_RECOVERY_RESULT']['retry_allowed'] is False
  if v['TEST_ID']=='B89-CONCURRENT_CLAIMS':assert {'concurrent_aggregate','concurrent_snapshot'}<=kinds
  if v['TEST_ID']=='B89-CRASH_AFTER_CONSUMPTION':assert {'parent_exit','crash_store_and_recovery'}<=kinds
 assert bindings['NO_UNOBSERVED_PID_TIMESTAMP_OR_SCHEDULE_INVENTED']
 sc=z['minimal-source-change-assessment.json'];assert len(sc['EXACT_SOURCE_FILES'])==2 and [v['SOURCE_PATH'] for v in sc['EXACT_SOURCE_FILES']]==list(sp) and not sc['SOURCE_CHANGE_PERFORMED']
 g=z['bootstrap-trust-dependency-graph.json'];assert graph_acyclic(g) and not g['ENTRY_REPAIR_DEPENDS_ON_HOST_PIDS_PROBE'] and not g['ORACLE_CLOSURE_DEPENDS_ON_BOOTSTRAP_EXECUTION'] and not g['AUTHORITY_DEPENDS_ON_FUTURE_TEST_OUTPUT'] and not g['ACTIVE_READY']
 env=z['proposed-repair-authorization-subject.json'];body=env['CONTENT'];assert aid(body,env['IDENTITY']['namespace'])==env['IDENTITY']
 assert body['SOURCE_ALLOWLIST']==list(sp) and body['CURRENT_SOURCE_PINS']==sp and body['ROOT_ENTRY_MAX_BYTES']==exact_max and body['RESOURCE_LIMITS']==old['RESOURCE_LIMITS']
 assert body['ORDINARY_PRIVATE_RECORD_MAX_BYTES']==65536 and body['APPROVAL_EVIDENCE'] is None and body['ISSUED_GRANT_IDENTITY'] is None and not body['CAMPAIGN_ACTIVATED']
 assert body['PREFERRED_REPAIR']=='A_ROOT_ONLY_BOUNDED_ENLARGEMENT'
 for p in body['EVIDENCE_PINS'].values():assert pin(ROOT/p['path'])==p
 dos=z['unselected-repair-authorization-dossier.json'];assert dos['SELECTION'] is None and not dos['GRANT_ISSUED'] and not dos['ACTIVE_TEST_READY'] and dos['SUBJECT_IDENTITY']==env['IDENTITY']
 assert [x['OPTION_ID'] for x in dos['OPTIONS']]==['AUTHORIZE_BOUNDED_BOOTSTRAP_ENTRY_ORACLE_REPAIR','DECLINE_BOUNDED_BOOTSTRAP_ENTRY_ORACLE_REPAIR']
 return True
validate(bundle)
changes=[('lower bound treated as exact',lambda z:z['entry-size-analysis.json'].update(ACTUAL_FINAL_RUNTIME_ENTRY_BYTES=108353)),('unsupported new size limit',lambda z:z['candidate-a-bounded-enlargement.json'].update(NEW_MAX_ENTRY_BYTES=999999)),('unbounded reference count',lambda z:z['candidate-b-immutable-references.json'].update(MAX_REFERENCE_COUNT=999999)),('unverified reference',lambda z:z['candidate-b-leaf-size-models.json']['LEAVES'][0].update(raw_sha256='0'*64)),('mutable source alias',lambda z:z['candidate-b-root-size-model.json']['SOURCE_ROOT_SPEC'].update(source_must_be_unwritable_by_test_actor_including_aliases=False)),('symlink path traversal',lambda z:z['candidate-b-leaf-size-models.json']['LEAVES'][0].update(path='../alias.json')),('cyclic references',lambda z:z['candidate-b-immutable-references.json']['MODEL_REFERENCE_GRAPH']['edges'].append([z['candidate-b-immutable-references.json']['DIRECT_REFERENCE_IDENTITIES'][0],z['candidate-b-immutable-references.json']['ROOT_ENTRY_IDENTITY']])),('missing concurrent witness',lambda z:z['executable-oracle-bindings.json']['VARIANTS'][5]['COMPARISONS'].pop()),('missing crash recovery comparison',lambda z:z['executable-oracle-bindings.json']['VARIANTS'][8]['COMPARISONS'].pop()),('adapter-generated oracle',lambda z:z['executable-oracle-bindings.json'].update(NO_UNOBSERVED_PID_TIMESTAMP_OR_SCHEDULE_INVENTED=False)),('unauthorized source modification',lambda z:z['minimal-source-change-assessment.json']['EXACT_SOURCE_FILES'][0].update(SOURCE_PATH='adapter/other.py')),('circular bootstrap',lambda z:z['bootstrap-trust-dependency-graph.json']['EDGES'].append({'from':'BASIC_POSIX_ENVIRONMENT','to':'HOST_PIDS_QUALIFICATION','type':'BAD'})),('premature campaign',lambda z:z['unselected-repair-authorization-dossier.json'].update(ACTIVE_TEST_READY=True)),('actual systemd H77 A15',lambda z:z['proposed-repair-authorization-subject.json']['CONTENT']['PERMITTED_OPERATIONS'].append('actual systemd/H77/A15 execution'))]
neg=[]
for name,change in changes:
 z=copy.deepcopy(bundle);change(z)
 try:validate(z)
 except (AssertionError,KeyError,TypeError,ValueError):neg.append({'CONTROL':name,'RESULT':'REJECTED'})
 else:raise AssertionError('accepted negative '+name)
result={'PACKAGE92_AUTHENTICATED':True,'FIXTURE_MANIFEST_IDENTITY':f['IDENTITY'],'ORACLE_MANIFEST_IDENTITY':o['IDENTITY'],'EXACT_INLINE_MODEL_RANGE':[exact_min,exact_max],'EXACT_SIZE_FORMULA_BASE':size['EXACT_SIZE_FORMULA']['BASE_FIXED_BYTES'],'ACTUAL_RUNTIME_ENTRY_BYTES':None,'PREFERRED_REPAIR':'A_ROOT_ONLY_BOUNDED_ENLARGEMENT','PROPOSED_ROOT_CAP_BYTES':exact_max,'ORACLE_BINDINGS_COMPLETE':True,'REFERENCE_MODEL_COMPLETE':True,'SOURCE_PINS':sp,'BOOTSTRAP_TRUST_GRAPH_ACYCLIC':True,'REPAIR_AUTHORITY_ALREADY_APPLICABLE':False,'REPAIR_DECISION_READY':True,'ACTIVE_INERT_TEST_READY':False,'PROPOSED_SUBJECT_IDENTITY':bundle['proposed-repair-authorization-subject.json']['IDENTITY'],'LESSONS_HEAD':head,'NEGATIVES':neg,'TARGET_EXECUTION_COUNT':0,'CONTRACT_IDENTITIES':{n:aid(read(OUT/n),'bootstrap-93-static-artifact-v1') for n in ('entry-size-analysis.json','candidate-a-bounded-enlargement.json','candidate-b-immutable-references.json','strategy-comparison.json','preferred-repair-specification.json','executable-oracle-bindings.json','minimal-source-change-assessment.json','authority-applicability-assessment.json','repair-qualification-tests.json','bootstrap-trust-dependency-graph.json','reasoning-lessons-review.json')}}
print(json.dumps({'RECONSTRUCTION':result,'SEMANTIC_IDENTITY':aid(result,'bootstrap-93-independent-reconstruction-v1')},sort_keys=True))
