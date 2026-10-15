"""Independent read-only pin, coverage, and derived identity verification.
Does not import runner code or invoke any native case operation.
"""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent
P=R/'docs/plans/qualification/E2_P05_D01_PROSPECTIVE_MATRIX_CONTRACT_1'
C=R/'docs/plans/qualification/E2_P05_D01_FIXTURE_ORACLE_CLOSURE_2'
def load(p):return json.loads(p.read_bytes())
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def digest(v):return hashlib.sha256(v).hexdigest()
def get(v,p):
 for k in p.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
inventory=load(O/'initial-111-operand-inventory.json')['ROWS'];sources=load(O/'operand-source-and-derivation-inventory.json')['ROWS'];records=load(O/'invocation-records.partial.json')['ROWS'];frozen=load(P/'sealed-128-obligations.json')['obligations'];catalog=load(C/'fixture-catalog.json');dispatch=load(C/'dispatch-table-v2.json')
assert len(inventory)==111 and len(records)==128
assert len({r['OBLIGATION_ID'] for r in records})==128
assert {r['OBLIGATION_ID'] for r in records}=={r['OBLIGATION_ID'] for r in frozen}
cache={}
def source(p):
 path=R/p['path'];raw=cache.setdefault(str(path),path.read_bytes());assert digest(raw)==p['raw_sha256'];return get(json.loads(raw),p['pointer'])
reconstruction=[]
for r in sources:
 s=source(r['SOURCE_ARTIFACT']);name=r['OPERAND_NAME']
 if name in ('bundle_path','expected_bundle_identity'):
  identity={'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':'planner-bundle-v1','sha256':digest((R/r['SOURCE_ARTIFACT']['path']).read_bytes())}
  assert identity==r['SOURCE_IDENTITY']
 elif name!='source_bytes':assert 'qualification-D01-operands-v1:'+digest(canon(s))==r['SOURCE_IDENTITY']
 if r.get('DERIVATION_SOURCE'):
  from adapter.planner import codec
  packet=source(r['DERIVATION_SOURCE']);state=codec._wire(codec._unwire(packet['canonical_content']['subject']))
  if r['CASE_ID']=='E2-N04':
   receipt=state['receipt_admissions'][0];eid=receipt['artifact']
   if r['STATE_VARIANT_ID'].endswith(':ATTESTOR_INVALIDATED'):
    pred=next(p for p in state['predicates'] if p['id']==receipt['authentication']);eid=pred['entity']
   target=next(e for e in state['entities'] if e['id']==eid)['provenance']['identity']
  else:
   routes=[x for gate in state['external_gates'] for x in gate['resolution_contracts']];assert len(routes)==1;target=routes[0]['provenance']['identity']
  assert s['changed']==[target]
  assert s['expected_snapshot']['sha256']==digest(codec.canonical_bytes({'schema':'PLANNER-SNAPSHOT-1','snapshot':state}))
 reconstruction.append({k:r[k] for k in ['OBLIGATION_ID','STATE_VARIANT_ID','STEP','OPERAND_NAME','SOURCE_IDENTITY']})
for r in records:
 assert not r['COMPLETE'];assert dispatch[r['DISPATCH_ID']]['obligation_id']==r['OBLIGATION_ID']
 for v in r['VARIANTS']:
  assert not v['COMPLETE'];assert v['CAPSULE_SOURCE']==catalog[v['CAPSULE_ID']]['artifact'];source(v['CAPSULE_SOURCE'])
assert len(sources)==len(inventory)-sum(r['STATUS']!='RESOLVED' for r in inventory) and sum(r['STATUS']!='RESOLVED' for r in inventory)==load(O/'summary.json')['FINAL_MISSING_OPERANDS']
result={'status':'PASS_RESOLVED_SUBSET_PINS_AND_COVERAGE_ONLY','resolved_reference_count':len(sources),'remaining_reference_count':sum(r['STATUS']!='RESOLVED' for r in inventory),'case_operations_executed':0,'semantic_full_invocation_reconstruction':'NOT_PASS','resolved_subset_identity':'qualification-D01-resolution-subset-v1:'+digest(canon(sorted(reconstruction,key=lambda r:(r['OBLIGATION_ID'],r['STATE_VARIANT_ID'],r['STEP'],r['OPERAND_NAME']))))}
print(json.dumps(result,sort_keys=True))
