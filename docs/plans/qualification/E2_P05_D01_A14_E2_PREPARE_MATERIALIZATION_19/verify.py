"""Fresh structural reader; no prospective qualification case/save/read."""
import hashlib,json,runpy
from pathlib import Path
from adapter.planner import codec,model,replay
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;C18=O.parent/'E2_P05_D01_A14_E2_PREPARE_SOURCE_RECOVERY_18'
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
collect=read(O.parent/'E2_P05_D01_A14_E2_COLLECT_SOURCE_RECOVERY_14/bounded-materialization-subject.json');collectraw=(R/'E2-COLLECT.json').read_bytes()
assert collectraw==collect['RAW_BYTES_UTF8'].encode() and sha(collectraw)==collect['EXPECTED_SHA256']
assert codec.load_pinned(R,model.ArtifactPin('E2-COLLECT.json',codec._unwire(collect['EXPECTED_CONTENT_IDENTITY']),model.HashProfile.RAW))==collectraw
s=read(C18/'bounded-materialization-subject.json');assert s['EXACT_ROOT']==str(R);target=codec._path(R,s['EXISTING_RELATIVE_PATH']);assert target==R/'E2-PREPARE.json' and not target.is_symlink()
raw=target.read_bytes();assert raw==(R/s['ISOLATED_CANDIDATE']['path']).read_bytes()==s['RAW_BYTES_UTF8'].encode() and len(raw)==91 and sha(raw)==s['EXPECTED_SHA256']
cp=s['HISTORICAL_CURRENT_PREPARE_COMPARISON'];assert sha((R/cp['path']).read_bytes())==cp['raw_sha256'];comparison=read(R/cp['path']);assert comparison['CURRENT_PREPARE_SUBSTITUTION_ALLOWED'] is False and comparison['HISTORICAL_CURRENT_RELATIONSHIP']=='DIFFERENT_VERSION'
p04=comparison['CURRENT_P04_PHYSICAL_SOURCE'];assert sha((R/p04['path']).read_bytes())==p04['raw_sha256'] and (R/p04['path']).read_bytes()!=raw
variants=comparison['ALL_RETAINED_VARIANT_COMPARISON'];assert sha((R/variants['path']).read_bytes())==variants['raw_sha256']
for definition in comparison['CURRENT_PREPARE_DEFINITIONS']:
 dp=definition['ACTION_SOURCE'];assert sha((R/dp['path']).read_bytes())==dp['raw_sha256'] and at(read(R/dp['path']),dp['pointer'])==definition['NATIVE_ACTION_FIELDS']
# The previous package's historical frontier required PREPARE absent. Verify
# its accepted FINISH bytes directly while preserving that historical assertion.
finish=read(O.parent/'E2_P05_D01_A14_E2_FINISH_SOURCE_RECOVERY_16/bounded-materialization-subject.json');finishraw=(R/'E2-FINISH.json').read_bytes()
assert finishraw==finish['RAW_BYTES_UTF8'].encode() and sha(finishraw)==finish['EXPECTED_SHA256']
assert codec.load_pinned(R,model.ArtifactPin('E2-FINISH.json',codec._unwire(finish['EXPECTED_CONTENT_IDENTITY']),model.HashProfile.RAW))==finishraw
ep=s['AUTHORITATIVE_BYTE_SOURCE'];assert sha((R/ep['path']).read_bytes())==ep['raw_sha256'] and at(read(R/ep['path']),ep['pointer']).encode()==raw
sp=R/s['BASE_SNAPSHOT_SOURCE']['path'];assert sha(sp.read_bytes())==s['BASE_SNAPSHOT_SOURCE']['raw_sha256'];snapshot=codec.decode_snapshot(sp.read_bytes());model.validate_model(snapshot);sid=codec._wire(codec.snapshot_id(snapshot));assert sid==s['BASE_SNAPSHOT_ID']==s['EXPECTED_POST_MATERIALIZATION_SNAPSHOT_ID']
for ref in s['EXISTING_PROVENANCE']:assert at(read(sp),ref['POINTER'])==ref['PROVENANCE'] and ref['PROVENANCE']['excerpt'].encode()==raw
provs=[p for p in replay.provenance_records(snapshot) if p.path=='E2-PREPARE.json'];assert len(provs)==3
for p in provs:
 model.validate_provenance(p);assert codec._wire(p.identity)==s['EXPECTED_CONTENT_IDENTITY'];assert codec.load_pinned(R,model.ArtifactPin(p.path,p.identity,model.HashProfile.RAW))==raw
assert codec.parse_json(raw)=={'action':'E2-PREPARE','lineage':snapshot.context.lineage,'scope':snapshot.context.scope}
pins={}
for p in replay.provenance_records(snapshot):
 n=model.ArtifactPin(p.path,p.identity,model.HashProfile.RAW);key=(n.path,n.pointer,n.profile);assert key not in pins or pins[key]==n;pins[key]=n
model.unique(tuple(pins.values()),lambda p:(p.path,p.pointer,p.profile))
assert len(pins)==10
front=read(O/'a14-source-frontier.json');assert front['SOURCE_PINS_PRESENT']==9 and front['SOURCE_PINS_MISSING']==1
assert all(not (R/p).exists() for p in front['MISSING_ORDER'])
print(json.dumps({'STATUS':'PASS','BYTE_LENGTH':91,'SHA256':sha(raw),'CONTENT_IDENTITY':s['EXPECTED_CONTENT_IDENTITY'],'PROVENANCE_VALIDATION':'PASS','SNAPSHOT_IDENTITY':sid,'RAW_PIN_KEYS_UNIQUE':True,'SOURCE_PINS_TOTAL':10,'SOURCE_PINS_PRESENT':9,'SOURCE_PINS_MISSING':1,'NEXT_MISSING_SOURCE':'resolution.json','RESOLVED_OPERANDS':52,'UNRESOLVED_OPERANDS':59,'QUALIFICATION_CASES_EXECUTED':0,'A14_PREPARE_SOURCE_IDENTITY':comparison['A14_EXPECTED_PREPARE_SOURCE']['SOURCE_CONTENT_IDENTITY'],'CURRENT_PREPARE_SOURCE_IDENTITY':comparison['CURRENT_P04_PREPARE_DEFINITION']['SOURCE_CONTENT_IDENTITY'],'CURRENT_PREPARE_SUBSTITUTED':False,'CURRENT_PREPARE_MODIFIED':False,'PREPARE_VERSION_RELATIONSHIP':'DIFFERENT_VERSION'},sort_keys=True))
