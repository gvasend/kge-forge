"""Independent static contradiction and identity verification. No case operations."""
import hashlib,json,runpy
from collections import defaultdict
from pathlib import Path
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;C4=R/'docs/plans/qualification/E2_P05_D01_OPERAND_RECONCILIATION_4'
def read(p):return json.loads(p.read_bytes())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
runpy.run_path(str(C4/'verify.py'),run_name='__metadata_verify__')
f=read(O/'frozen-52-bindings.json');old=read(C4/'resolved-bindings.json');assert f['ROWS_39']==old['PRESERVED_39'] and f['ROWS_13']==old['NEW_BINDINGS'] and f['SEMANTIC_IDENTITY']==old['SEMANTIC_IDENTITY']
bound=read(O/'a14-boundary-oracle.json');p=R/bound['PRE_STATE_SOURCE']['path'];assert sha(p.read_bytes())==bound['PRE_STATE_SOURCE']['raw_sha256'];s=read(p)['canonical_content']['subject']
# Independent conflict proof from entity/knowledge actual fields, not generated inventory.
constraints=defaultdict(set)
for e in s['entities']:
 prov=e['provenance'];constraints[prov['path']].add(prov['identity']['sha256'])
for k in s['knowledge']:
 prov=k['provenance'];constraints[prov['path']].add(prov['identity']['sha256'])
path='qualification://E2-P02-human-decision';assert len(constraints[path])==2 and Path(path).as_posix()!=path
codec=(R/'adapter/planner/codec.py').read_text()
for rule in ["m.unique(bundle.sources, lambda p: (p.path, p.pointer, p.profile))", "if pin.profile is m.HashProfile.RAW and pin.pointer:", "if any((p.path, p.identity) not in raw_sources for p in provenances):", "Path(relative).as_posix() != relative"]:assert rule in codec
inventory=read(O/'bundle-source-inventory.json');conf=next(c for c in inventory['PIN_COLLISIONS'] if c['PATH']==path);assert {i['sha256'] for i in conf['IDENTITIES']}==constraints[path]
assert inventory['UNIQUE_ELIGIBLE_RETAINED_BUNDLE'] is False
handoff=read(O/'handoff-manifest.json');identity=handoff.pop('QUALIFICATION_IDENTITY');assert identity=='qualification-D01-A14-handoff-contract-v1:'+sha(canon(handoff));assert handoff['STATUS']=='BLOCKED_NON_EXECUTABLE_CONTRACT_MANIFEST'
updated=read(O/'updated-operand-inventory.json');assert updated['TOTAL_RESOLVED']==52 and updated['TOTAL_UNRESOLVED']==59 and updated['A14_DEPENDENT_REFERENCES']==16 and updated['A14_REFERENCES_RESOLVED']==0
assert updated['TOTAL_RESOLVED']+updated['TOTAL_UNRESOLVED']==111
print(json.dumps({'status':'PASS_STATIC_CONTRADICTION_AND_ALL_52_PRESERVATION_RECONSTRUCTION','handoff_contract_identity':identity,'binding_semantic_identity':f['SEMANTIC_IDENTITY'],'source_collision':path,'required_distinct_raw_hashes':sorted(constraints[path]),'handoff_execution_ready':False,'qualification_cases_executed':0,'saves_performed':0,'cold_readers_executed':0},sort_keys=True))
