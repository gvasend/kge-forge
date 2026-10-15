"""Fresh source/model reader; not a qualification cold-reader transaction."""
import hashlib,json,runpy
from pathlib import Path
from adapter.planner import codec,model,replay
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification';C8=Q/'E2_P05_D01_A14_E2_DECIDE_SOURCE_RECOVERY_8'
def read(p):return json.loads(p.read_bytes())
runpy.run_path(str(Q/'E2_P05_D01_A14_PROVENANCE_FIXTURE_CORRECTION_7/verify.py'),run_name='__prior_fixture_verify__')
subject=read(C8/'bounded-source-materialization-subject.json');root=Path(subject['SOURCE_ROOT']);assert root==R;target=root/subject['PROPOSED_ACCEPTED_PATH'];assert target==R/'E2-DECIDE.json' and target.resolve()==target and not target.is_symlink()
raw=target.read_bytes();candidate=(R/subject['ISOLATED_CANDIDATE']['path']).read_bytes();assert raw==candidate==subject['RAW_BYTES_UTF8'].encode() and len(raw)==90;assert hashlib.sha256(raw).hexdigest()==subject['EXPECTED_RAW_IDENTITY']['sha256']
snapshotpath=R/subject['BASE_CORRECTED_SNAPSHOT_SOURCE']['path'];assert hashlib.sha256(snapshotpath.read_bytes()).hexdigest()==subject['BASE_CORRECTED_SNAPSHOT_SOURCE']['raw_sha256'];snapshot=codec.decode_snapshot(snapshotpath.read_bytes());model.validate_model(snapshot);sid=codec._wire(codec.snapshot_id(snapshot));assert sid==subject['BASE_CORRECTED_SNAPSHOT_ID']
a=next(a for a in snapshot.actions if a.id.value=='E2-DECIDE');assert codec._wire(a.source)==subject['EXPECTED_EXISTING_PROVENANCE'];model.validate_provenance(a.source);p=model.ArtifactPin(a.source.path,a.source.identity,model.HashProfile.RAW);assert codec.load_pinned(root,p)==raw
plain=codec.parse_json(raw);assert plain['scope']==snapshot.context.scope and plain['lineage']==snapshot.context.lineage
unique={}
for prov in replay.provenance_records(snapshot):
 key=(prov.path,'',model.HashProfile.RAW);n=model.ArtifactPin(prov.path,prov.identity,model.HashProfile.RAW);assert key not in unique or unique[key]==n;unique[key]=n
model.unique(tuple(unique.values()),lambda x:(x.path,x.pointer,x.profile))
print(json.dumps({'STATUS':'PASS_FRESH_ACCEPTED_SOURCE_AND_UNCHANGED_SNAPSHOT','SOURCE_BYTE_LENGTH':len(raw),'SOURCE_SHA256':hashlib.sha256(raw).hexdigest(),'CONTENT_IDENTITY':codec._wire(a.source.identity),'PROVENANCE':codec._wire(a.source),'SNAPSHOT_IDENTITY':sid,'RAW_PIN_KEYS_UNIQUE':True,'A14_EXECUTED':False,'QUALIFICATION_COLD_READERS_EXECUTED':0},sort_keys=True))
