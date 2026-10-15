"""Independent reconstruction of resolved input bindings, no case operations."""
import hashlib,json,runpy
from pathlib import Path
from adapter.planner import codec
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification';C3=Q/'E2_P05_D01_OPERAND_CLOSURE_3';C2=Q/'E2_P05_D01_FIXTURE_ORACLE_CLOSURE_2'
def read(p):return json.loads(Path(p).read_bytes())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def qid(v):return 'qualification-D01-reconciliation-v1:'+sha(canon(v))
def snapshotid(s):return {'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':'planner-snapshot-v1','sha256':sha(codec.canonical_bytes({'schema':'PLANNER-SNAPSHOT-1','snapshot':codec._wire(codec._unwire(s))}))}
def at(v,ptr):
 for k in ptr.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
def pinned(p):
 raw=(R/p['path']).read_bytes();assert sha(raw)==p['raw_sha256'];return at(json.loads(raw),p.get('pointer',''))
# Prior standalone verifier independently re-derives its five descriptors and retained source identities.
runpy.run_path(str(C3/'verify.py'),run_name='__metadata_verify__')
prior=read(C3/'operand-source-and-derivation-inventory.json')['ROWS'];freeze=read(O/'frozen-39-bindings.json');resolved=read(O/'resolved-bindings.json');assert freeze['ROWS']==prior==resolved['PRESERVED_39']
assert len(prior)==39 and len(resolved['NEW_BINDINGS'])==13
catalog=read(C2/'fixture-catalog.json');dispatch=read(C2/'dispatch-table-v2.json');frozenobs=read(Q/'E2_P05_D01_PROSPECTIVE_MATRIX_CONTRACT_1/sealed-128-obligations.json')['obligations'];obmap={r['OBLIGATION_ID']:r for r in frozenobs}
# Independent boundary recovery: original experiment cases, explicit native parent links and operation class.
canonical=read(R/'docs/plans/DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.json')['cases'];case={r['CASE_ID']:r for r in canonical}
assert case['E2-A03']['INITIAL_STATE']=='Selected acquisition action with independently specified output contract'
assert case['E2-A14']['OPERATION']=='Native recompute, save, terminate, restore'
a3=read(O/'a03-boundary-oracle.json');a14=read(O/'a14-boundary-oracle.json');prefix=pinned(a3['BUNDLE_SOURCE'])['bundle'];supplied=pinned(a3['SUPPLIED_INPUT_SOURCE']);assert snapshotid(prefix['current'])==supplied['expected_snapshot']==a3['PRE_STATE_IDENTITY']
assert a3['EXPECTED_HEAD']==prefix['events'][-1]['identity'];assert a3['EXPECTED_PARENT']==snapshotid(prefix['current'])
assert next(a for a in prefix['current']['actions'] if a['id']==supplied['action'])['operation']['value']=='SOURCE_ACQUISITION'
gov=pinned(a14['PRE_STATE_SOURCE'])['canonical_content']['subject'];assert snapshotid(gov)==a14['PRE_STATE_IDENTITY'];assert all(not r['rule_known'] for r in gov['evidence_requirements'])
# Reconstruct missing raw-byte map check omitted by the prior subset verifier.
for r in prior:
 if r['OPERAND_NAME']=='source_bytes':
  payload=r['SOURCE_ARTIFACT'];raw=(R/payload['path']).read_bytes();request=read(Q/'E2_P04_CANONICAL_EXECUTION_RETRY_1/a09-command.json')
  def pins(x):
   if isinstance(x,dict):
    if x.get('$type')=='ArtifactPin':yield x
    for v in x.values():yield from pins(v)
   elif isinstance(x,list):
    for v in x:yield from pins(v)
  matches=[p for p in pins(request) if p['identity']['sha256']==sha(raw)];assert len(matches)==1
  v={'representation':'RAW_BYTES_FILE_MAP','entries':[{'key':matches[0]['path'],'source':payload,'sha256':sha(raw)}]}
  assert r['SOURCE_IDENTITY']=='qualification-D01-operands-v1:'+sha(canon(v))
independent=[]
for r in resolved['NEW_BINDINGS']:
 assert r['OPERATION_EXECUTED'] is False and r['MUTATIONS_APPLIED']==r['INVALIDATIONS_APPLIED']==0
 assert dispatch[r['DISPATCH_ID']]['obligation_id']==r['OBLIGATION_ID'];assert obmap[r['OBLIGATION_ID']]['CASE_ID']==r['CASE_ID']
 e=catalog[r['CAPSULE_ID']];packet=pinned(e['artifact']);state=packet['canonical_content']['subject']
 if r['CASE_ID']=='E2-A03':
  value=pinned(r['VALUE_REFERENCE']);assert value==supplied and r['SOURCE_IDENTITY']==qid(supplied);state=prefix['current'];assert r['BOUNDARY_ORACLE']['raw_sha256']==sha((O/'a03-boundary-oracle.json').read_bytes())
 else:
  source=packet['canonical_content']['source'];raw=(R/source['path']).read_bytes();b=json.loads(raw)['bundle'];assert b==packet['canonical_content']['bundle']
  native={'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':'planner-bundle-v1','sha256':sha(raw)}
  assert native==r['VALUE']==r['SOURCE_IDENTITY']
 assert r['SCOPE']==state['context']['scope'] and r['LINEAGE']==state['context']['lineage'] and r['GENERATION']==state['context']['generation']
 pinned(r['SOURCE_ARTIFACT']);independent.append(r)
assert independent==resolved['NEW_BINDINGS']
assert qid({'PRESERVED_39':prior,'NEW_BINDINGS':independent})==resolved['SEMANTIC_IDENTITY']
assert len(read(O/'remaining-frontier.json')['ROWS'])==59
for o in read(O/'a03-invocation-source-overrides.json'):
 assert o['EXPECTED_PARENT']==snapshotid(prefix['current']) and o['EXPECTED_HEAD']==prefix['events'][-1]['identity'];assert o['PHASE']=='PRE_ACQUISITION';assert pinned(o['OPERAND_SOURCE_OVERRIDES']['snapshot'])==prefix['current']
print(json.dumps({'status':'PASS_ALL_52_RESOLVED_BINDING_RECONSTRUCTION','total_resolved':52,'total_unresolved':59,'semantic_identity':resolved['SEMANTIC_IDENTITY'],'qualification_cases_executed':0,'mutations_applied':0,'invalidations_applied':0},sort_keys=True))
