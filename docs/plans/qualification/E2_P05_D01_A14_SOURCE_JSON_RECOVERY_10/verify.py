"""Read-only independent recovery verification; no Planner transition."""
import hashlib,json,runpy
from pathlib import Path
from adapter.planner import codec,model
R=Path(__file__).resolve().parents[4]; O=Path(__file__).resolve().parent
def read(p): return json.loads(p.read_bytes())
def sha(b): return hashlib.sha256(b).hexdigest()
def canonical(v): return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def pointer(v,p):
 for k in p.split('/')[1:]: v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
runpy.run_path(str(O.parent/'E2_P05_D01_A14_E2_DECIDE_MATERIALIZATION_9/verify.py'),run_name='__prior_read_only_verify__')
s=read(O/'bounded-materialization-subject.json'); raw=(R/s['ISOLATED_RECOVERED_CANDIDATE']['path']).read_bytes()
assert len(raw)==s['EXPECTED_LENGTH']==617 and sha(raw)==s['EXPECTED_SHA256'] and raw==s['RAW_BYTES_UTF8'].encode()
for pin in s['AUTHORITATIVE_EXACT_BYTE_SOURCES']:
 assert (R/pin['path']).read_bytes()==raw and pin['raw_sha256']==sha(raw)
snapshotpath=R/s['BASE_SNAPSHOT_SOURCE']['path']; assert sha(snapshotpath.read_bytes())==s['BASE_SNAPSHOT_SOURCE']['raw_sha256']
wire=read(snapshotpath); snapshot=codec.decode_snapshot(snapshotpath.read_bytes()); model.validate_model(snapshot)
assert codec._wire(codec.snapshot_id(snapshot))==s['BASE_SNAPSHOT_ID']
for ref in s['EXISTING_PROVENANCE_REFERENCES']:
 p=pointer(wire,ref['POINTER']); assert p==ref['PROVENANCE'] and p['excerpt'].encode()==raw and p['identity']==s['EXPECTED_CONTENT_IDENTITY'] and p['path']=='source.json'
ep=s['AUTHORITATIVE_A14_EMBEDDED_POINTER']; assert pointer(read(R/ep['path']),ep['pointer']).encode()==raw
value=codec.parse_json(raw); assert value['schema']=='SYNTHETIC-GOVERNED-RULE-ACQUISITION-1' and value['scope']=='TEST/scope'
assert json.dumps(value,sort_keys=True,separators=(',',':')).encode()==raw
pin=model.ArtifactPin(s['ISOLATED_RECOVERED_CANDIDATE']['path'],codec._unwire(s['EXPECTED_CONTENT_IDENTITY']),model.HashProfile.RAW)
codec.validate_pin(pin); assert codec.load_pinned(R,pin)==raw
assert codec._path(R,'source.json')==R/'source.json' and not (R/'source.json').exists()
identity=s.pop('SUBJECT_IDENTITY'); assert identity=='qualification-A14-sourcejson-materialization-v1:'+sha(canonical(s))
d=read(O/'bounded-source-decision-dossier.json'); assert d['SUBJECT_IDENTITY']==identity and d['SELECTION']=='NOT_SELECTED'
assert sha((O/'bounded-materialization-subject.json').read_bytes())==d['EXACT_SUBJECT']['raw_sha256']
print(json.dumps({'STATUS':'PASS','BYTE_LENGTH':len(raw),'SHA256':sha(raw),'CONTENT_IDENTITY':s['EXPECTED_CONTENT_IDENTITY'],'SNAPSHOT_IDENTITY':s['BASE_SNAPSHOT_ID'],'SUBJECT_IDENTITY':identity,'SOURCE_JSON_MATERIALIZED':False},sort_keys=True))
