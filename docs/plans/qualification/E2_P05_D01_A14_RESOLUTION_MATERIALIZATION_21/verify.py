"""Fresh complete-source structural verifier; never a qualification reader."""
import hashlib,json,runpy
from pathlib import Path
from adapter.planner import codec,model,replay
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;C20=O.parent/'E2_P05_D01_A14_RESOLUTION_SOURCE_RECOVERY_20'
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def at(v,p):
 for k in p.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
runpy.run_path(str(O.parent/'E2_P05_D01_A14_PROVENANCE_FIXTURE_CORRECTION_7/verify.py'),run_name='__frozen_bindings_and_fixture_verification__')
s=read(C20/'bounded-materialization-subject.json');target=codec._path(R,s['EXISTING_RELATIVE_PATH']);assert target==R/'resolution.json' and not target.is_symlink() and s['EXACT_ROOT']==str(R)
raw=target.read_bytes();assert raw==(R/s['ISOLATED_CANDIDATE']['path']).read_bytes()==s['RAW_BYTES_UTF8'].encode() and len(raw)==1430 and sha(raw)==s['EXPECTED_SHA256']
ep=s['AUTHORITATIVE_BYTE_SOURCE'];assert at(read(R/ep['path']),ep['pointer']).encode()==raw and sha((R/ep['path']).read_bytes())==ep['raw_sha256']
sp=R/s['BASE_SNAPSHOT_SOURCE']['path'];assert sha(sp.read_bytes())==s['BASE_SNAPSHOT_SOURCE']['raw_sha256'];snapshot=codec.decode_snapshot(sp.read_bytes());model.validate_model(snapshot);sid=codec._wire(codec.snapshot_id(snapshot));assert sid==s['BASE_SNAPSHOT_ID']==s['EXPECTED_POST_MATERIALIZATION_SNAPSHOT_ID']
oracle=read(R/s['POST_MATERIALIZATION_SOURCE_ORACLE']['path']);pins={}
for prov in replay.provenance_records(snapshot):
 model.validate_provenance(prov);p=model.ArtifactPin(prov.path,prov.identity,model.HashProfile.RAW);key=(p.path,p.pointer,p.profile);assert key not in pins or pins[key]==p;pins[key]=p
model.unique(tuple(pins.values()),lambda p:(p.path,p.pointer,p.profile));assert len(pins)==10
for row in oracle['ROWS']:
 p=codec._unwire(row['EXPECTED_PIN']);codec.validate_pin(p);assert p in pins.values();b=codec.load_pinned(R,p);assert sha(b)==row['EXPECTED_SHA256'];assert codec._path(R,p.path).is_file() and not (R/p.path).is_symlink()
 assert row['SCOPE']==snapshot.context.scope and row['LINEAGE']==snapshot.context.lineage
 for ref in row['EXACT_PROVENANCE_REFERENCES']:assert at(read(sp),ref['POINTER'])==ref['PROVENANCE']
route=snapshot.external_gates[0].resolution_contracts[0];body=codec._wire(route);del body['$type'];del body['provenance'];assert codec.canonical_bytes({'schema':'EXTERNAL-RESOLUTION-CONTRACT-1','contract':body})==raw
audit=read(O/'full-111-reference-audit.json');assert len(audit['ROWS'])==111 and audit['TOTAL_RESOLVED']==52 and audit['TOTAL_UNRESOLVED']==59
assert read(O/'a14-dependent-reference-audit.json')['A14_REFERENCES_RESOLVED']==0
print(json.dumps({'STATUS':'PASS','BYTE_LENGTH':1430,'SHA256':sha(raw),'CONTENT_IDENTITY':s['EXPECTED_CONTENT_IDENTITY'],'PROVENANCE_VALIDATION':'PASS','SNAPSHOT_IDENTITY':sid,'SOURCE_PINS_TOTAL':10,'SOURCE_PINS_PRESENT':10,'SOURCE_PINS_MISSING':0,'RESOLVED_OPERANDS':52,'UNRESOLVED_OPERANDS':59,'FIRST_NON_SOURCE_BLOCKER':'BUNDLE_CONTRACT','QUALIFICATION_CASES_EXECUTED':0},sort_keys=True))
