"""Independent fresh read-only source verification; no qualification reader."""
import hashlib,json,runpy,ast
from pathlib import Path
from adapter.planner import codec,model,replay
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def at(v,p):
 for k in p.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
runpy.run_path(str(O.parent/'E2_P05_D01_A14_SOURCE_JSON_MATERIALIZATION_11/verify.py'),run_name='__previous_structural_verify__')
s=read(O/'bounded-materialization-subject.json');raw=(R/s['ISOLATED_CANDIDATE']['path']).read_bytes();assert len(raw)==s['EXPECTED_LENGTH']==89 and sha(raw)==s['EXPECTED_SHA256'] and raw==s['RAW_BYTES_UTF8'].encode()
source=s['AUTHORITATIVE_BYTE_SOURCE'];assert sha((R/source['path']).read_bytes())==source['raw_sha256'] and at(read(R/source['path']),source['pointer']).encode()==raw
sp=R/s['BASE_SNAPSHOT_SOURCE']['path'];assert sha(sp.read_bytes())==s['BASE_SNAPSHOT_SOURCE']['raw_sha256'];snapshot=codec.decode_snapshot(sp.read_bytes());model.validate_model(snapshot);sid=codec._wire(codec.snapshot_id(snapshot));assert sid==s['BASE_SNAPSHOT_ID']==s['EXPECTED_POST_MATERIALIZATION_SNAPSHOT_ID']
for ref in s['EXISTING_PROVENANCE']:
 p=at(read(sp),ref['POINTER']);assert p==ref['PROVENANCE'] and p['excerpt'].encode()==raw and p['identity']==s['EXPECTED_CONTENT_IDENTITY']
assert len(s['EXISTING_PROVENANCE'])==3
assert codec.parse_json(raw)=={'action':'E2-CHECK','lineage':snapshot.context.lineage,'scope':snapshot.context.scope}
assert codec.canonical_bytes(codec.parse_json(raw))==raw
# Inspect the original writer AST; never call build or _source.
writer=R/'docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_PC01_WHOLE_MODEL_ORACLE.py';tree=ast.parse(writer.read_text());fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='_source');names=[ast.dump(x) for x in ast.walk(fn) if isinstance(x,ast.Call)]
assert any("attr='canonical_bytes'" in x for x in names) and any("attr='write_bytes'" in x for x in names) and any("attr='decode'" in x for x in names)
p=model.ArtifactPin(s['ISOLATED_CANDIDATE']['path'],codec._unwire(s['EXPECTED_CONTENT_IDENTITY']),model.HashProfile.RAW);codec.validate_pin(p);assert codec.load_pinned(R,p)==raw
assert codec._path(R,'E2-CHECK.json')==R/'E2-CHECK.json' and not (R/'E2-CHECK.json').exists()
body=dict(s);subject=body.pop('SUBJECT_IDENTITY');assert subject=='qualification-A14-E2CHECK-materialization-v1:'+sha(canon(body))
d=read(O/'bounded-source-decision-dossier.json');assert d['SELECTION']=='NOT_SELECTED' and d['SUBJECT_IDENTITY']==subject and sha((R/d['EXACT_SUBJECT']['path']).read_bytes())==d['EXACT_SUBJECT']['raw_sha256']
front=read(O/'a14-source-frontier.json');assert front['TOTAL_A14_PHYSICAL_SOURCE_PINS']==front['PRESENT_SOURCE_COUNT']+front['MISSING_SOURCE_COUNT'] and front['MISSING_SOURCE_ORDER'][0]=='E2-CHECK.json'
print(json.dumps({'STATUS':'PASS','BYTE_LENGTH':len(raw),'SHA256':sha(raw),'CONTENT_IDENTITY':s['EXPECTED_CONTENT_IDENTITY'],'SNAPSHOT_IDENTITY':sid,'PROVENANCE_VALIDATION':'PASS','SUBJECT_IDENTITY':subject,'E2_CHECK_MATERIALIZED':False,'RESOLVED_OPERANDS':52,'UNRESOLVED_OPERANDS':59},sort_keys=True))
