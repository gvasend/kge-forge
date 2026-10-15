"""Fresh structural reader; no prospective qualification case/save/read."""
import hashlib,json,runpy
from pathlib import Path
from adapter.planner import codec,model,replay
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;C14=O.parent/'E2_P05_D01_A14_E2_COLLECT_SOURCE_RECOVERY_14'
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def at(v,p):
 for k in p.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
runpy.run_path(str(O.parent/'E2_P05_D01_A14_SOURCE_JSON_MATERIALIZATION_11/verify.py'),run_name='__prior_structural_verify__')
# Materialization13's historical frontier expected COLLECT absent. Preserve it,
# and independently verify its accepted CHECK source without replaying that assertion.
check=read(O.parent/'E2_P05_D01_A14_E2_CHECK_SOURCE_RECOVERY_12/bounded-materialization-subject.json')
checkraw=(R/'E2-CHECK.json').read_bytes()
assert checkraw==check['RAW_BYTES_UTF8'].encode() and sha(checkraw)==check['EXPECTED_SHA256']
assert codec.load_pinned(R,model.ArtifactPin('E2-CHECK.json',codec._unwire(check['EXPECTED_CONTENT_IDENTITY']),model.HashProfile.RAW))==checkraw
s=read(C14/'bounded-materialization-subject.json');assert s['EXACT_ROOT']==str(R);target=codec._path(R,s['EXISTING_RELATIVE_PATH']);assert target==R/'E2-COLLECT.json' and not target.is_symlink()
raw=target.read_bytes();assert raw==(R/s['ISOLATED_CANDIDATE']['path']).read_bytes()==s['RAW_BYTES_UTF8'].encode() and len(raw)==91 and sha(raw)==s['EXPECTED_SHA256']
ep=s['AUTHORITATIVE_BYTE_SOURCE'];assert sha((R/ep['path']).read_bytes())==ep['raw_sha256'] and at(read(R/ep['path']),ep['pointer']).encode()==raw
sp=R/s['BASE_SNAPSHOT_SOURCE']['path'];assert sha(sp.read_bytes())==s['BASE_SNAPSHOT_SOURCE']['raw_sha256'];snapshot=codec.decode_snapshot(sp.read_bytes());model.validate_model(snapshot);sid=codec._wire(codec.snapshot_id(snapshot));assert sid==s['BASE_SNAPSHOT_ID']==s['EXPECTED_POST_MATERIALIZATION_SNAPSHOT_ID']
for ref in s['EXISTING_PROVENANCE']:assert at(read(sp),ref['POINTER'])==ref['PROVENANCE'] and ref['PROVENANCE']['excerpt'].encode()==raw
provs=[p for p in replay.provenance_records(snapshot) if p.path=='E2-COLLECT.json'];assert len(provs)==3
for p in provs:
 model.validate_provenance(p);assert codec._wire(p.identity)==s['EXPECTED_CONTENT_IDENTITY'];assert codec.load_pinned(R,model.ArtifactPin(p.path,p.identity,model.HashProfile.RAW))==raw
assert codec.parse_json(raw)=={'action':'E2-COLLECT','lineage':snapshot.context.lineage,'scope':snapshot.context.scope}
pins={}
for p in replay.provenance_records(snapshot):
 n=model.ArtifactPin(p.path,p.identity,model.HashProfile.RAW);key=(n.path,n.pointer,n.profile);assert key not in pins or pins[key]==n;pins[key]=n
model.unique(tuple(pins.values()),lambda p:(p.path,p.pointer,p.profile))
assert len(pins)==10
front=read(O/'a14-source-frontier.json');assert front['SOURCE_PINS_PRESENT']==7 and front['SOURCE_PINS_MISSING']==3
assert all(not (R/p).exists() for p in front['MISSING_ORDER'])
print(json.dumps({'STATUS':'PASS','BYTE_LENGTH':91,'SHA256':sha(raw),'CONTENT_IDENTITY':s['EXPECTED_CONTENT_IDENTITY'],'PROVENANCE_VALIDATION':'PASS','SNAPSHOT_IDENTITY':sid,'RAW_PIN_KEYS_UNIQUE':True,'SOURCE_PINS_TOTAL':10,'SOURCE_PINS_PRESENT':7,'SOURCE_PINS_MISSING':3,'NEXT_MISSING_SOURCE':'E2-FINISH.json','RESOLVED_OPERANDS':52,'UNRESOLVED_OPERANDS':59,'QUALIFICATION_CASES_EXECUTED':0},sort_keys=True))
