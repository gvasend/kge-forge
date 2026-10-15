"""Fresh structural fixture reader; no native restore or qualification operation."""
import hashlib,json,runpy
from copy import deepcopy
from pathlib import Path
from adapter.planner import codec,model,replay
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification'
def read(p):return json.loads(p.read_bytes())
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
# Prior source/operand verifier does not assume the authorized physical files are absent.
runpy.run_path(str(Q/'E2_P05_D01_OPERAND_RECONCILIATION_4/verify.py'),run_name='__prior_metadata_verify__')
c=read(Q/'E2_P05_D01_A14_SOURCE_PROVENANCE_RECONCILIATION_6/minimum-correction-contract.json');src=c['BASE_SNAPSHOT_SOURCE'];original_packet=read(R/src['path']);assert hashlib.sha256((R/src['path']).read_bytes()).hexdigest()==src['raw_sha256']
original=original_packet['canonical_content']['subject'];expected=deepcopy(original)
# Independent reconstruction from role+identity, rather than recorded pointer substitutions.
changes=[]
def visit(v,ptr=''):
 if isinstance(v,dict):
  if v.get('$type')=='Provenance' and v.get('path')=='qualification://E2-P02-human-decision':
   label='A' if v['method']=='E2-T03-AUTHENTICATED-CHOICE-1' else 'B' if v['method']=='E2-T03-QUALIFICATION-GRANT-1' else None
   assert label;assert v['identity']['sha256']==c['SOURCE_FILE_BYTE_COMMITMENTS'][label]['SHA256'];v['path']=c['SOURCE_ROLE_PATHS'][label];changes.append('/canonical_content/subject'+ptr+'/path')
  for key,value in v.items():visit(value,ptr+'/'+key)
 elif isinstance(v,list):
  for i,value in enumerate(v):visit(value,ptr+'/'+str(i))
visit(expected);assert len(changes)==3 and set(changes)=={x['POINTER'] for x in c['PROVENANCE_PATH_ASSIGNMENTS']}
actual=read(O/'corrected-prospective-snapshot.json')['snapshot'];assert codec._wire(codec._unwire(expected))==actual
native=codec._unwire(actual);model.validate_model(native);sid=codec._wire(codec.snapshot_id(native));fixture=read(O/'corrected-prospective-fixture.json');assert sid==fixture['CORRECTED_SNAPSHOT_ID'] and sid!=c['BASE_SNAPSHOT_IDENTITY']
for label,rel in c['SOURCE_ROLE_PATHS'].items():
 raw=(R/rel).read_bytes();assert raw==c['SOURCE_FILE_BYTE_COMMITMENTS'][label]['RAW_BYTES_UTF8'].encode();assert hashlib.sha256(raw).hexdigest()==c['SOURCE_FILE_BYTE_COMMITMENTS'][label]['SHA256']
 p=model.ArtifactPin(rel,model.ArtifactIdentity(model.IdentityKind.CONTENT_IDENTITY,'raw-file-sha256',hashlib.sha256(raw).hexdigest()),model.HashProfile.RAW);assert codec.load_pinned(R,p)==raw
provenances=replay.provenance_records(native);unique={}
for p in provenances:
 key=(p.path,'','raw-file-sha256');value=codec._wire(p.identity);assert key not in unique or unique[key]==value;unique[key]=value;codec._path(R,p.path)
projection={'snapshot_id':sid,'provenances':[codec._wire(p) for p in provenances]}
print(json.dumps({'STATUS':'PASS_INDEPENDENT_FIXTURE_RECONSTRUCTION','CORRECTED_SNAPSHOT_ID':sid,'PROVENANCE_SEMANTIC_IDENTITY':'qualification-A14-corrected-provenance-v1:'+hashlib.sha256(canon(projection)).hexdigest(),'PATH_CHANGES':3,'A14_EXECUTED':False,'QUALIFICATION_COLD_READERS_EXECUTED':0,'RESOLVED_OPERANDS':52,'UNRESOLVED_OPERANDS':59},sort_keys=True))
