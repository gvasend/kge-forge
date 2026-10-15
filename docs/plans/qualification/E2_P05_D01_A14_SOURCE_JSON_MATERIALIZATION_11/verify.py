"""Fresh structural reader, not a qualification cold reader."""
import hashlib,json,runpy
from pathlib import Path
from adapter.planner import codec,model,replay
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;C10=O.parent/'E2_P05_D01_A14_SOURCE_JSON_RECOVERY_10'
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
runpy.run_path(str(O.parent/'E2_P05_D01_A14_E2_DECIDE_MATERIALIZATION_9/verify.py'),run_name='__previous_structural_verify__')
s=read(C10/'bounded-materialization-subject.json');target=codec._path(R,s['EXISTING_RELATIVE_PATH']);assert str(R)==s['EXACT_ROOT'] and target==R/'source.json' and not target.is_symlink()
raw=target.read_bytes();assert raw==(R/s['ISOLATED_RECOVERED_CANDIDATE']['path']).read_bytes()==s['RAW_BYTES_UTF8'].encode() and len(raw)==617 and sha(raw)==s['EXPECTED_SHA256']
for p in s['AUTHORITATIVE_EXACT_BYTE_SOURCES']:assert (R/p['path']).read_bytes()==raw and sha(raw)==p['raw_sha256']
sp=R/s['BASE_SNAPSHOT_SOURCE']['path'];assert sha(sp.read_bytes())==s['BASE_SNAPSHOT_SOURCE']['raw_sha256'];snapshot=codec.decode_snapshot(sp.read_bytes());model.validate_model(snapshot);sid=codec._wire(codec.snapshot_id(snapshot));assert sid==s['BASE_SNAPSHOT_ID']
provs=[p for p in replay.provenance_records(snapshot) if p.path=='source.json'];assert len(provs)==5
for p in provs:
 model.validate_provenance(p);assert p.excerpt.encode()==raw and codec._wire(p.identity)==s['EXPECTED_CONTENT_IDENTITY'];assert codec.load_pinned(R,model.ArtifactPin(p.path,p.identity,model.HashProfile.RAW))==raw
assert codec.parse_json(raw)['scope']=='TEST/scope' and snapshot.context.scope=='E2-QUALIFICATION-ONLY'
required={}
for p in replay.provenance_records(snapshot):
 n=model.ArtifactPin(p.path,p.identity,model.HashProfile.RAW);key=(n.path,n.pointer,n.profile);assert key not in required or required[key]==n;required[key]=n
model.unique(tuple(required.values()),lambda p:(p.path,p.pointer,p.profile))
print(json.dumps({'STATUS':'PASS','BYTE_LENGTH':len(raw),'SHA256':sha(raw),'CONTENT_IDENTITY':s['EXPECTED_CONTENT_IDENTITY'],'PROVENANCE_VALIDATION':'PASS','RAW_PIN_KEYS_UNIQUE':True,'SNAPSHOT_IDENTITY':sid,'RETAINED_COPIES':10,'A14_EXECUTED':False,'QUALIFICATION_COLD_READERS_EXECUTED':0},sort_keys=True))
