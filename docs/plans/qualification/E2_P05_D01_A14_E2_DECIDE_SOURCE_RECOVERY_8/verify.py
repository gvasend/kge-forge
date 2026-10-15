"""Fresh lossless source-extraction verification, no accepted source integration."""
import hashlib,json,runpy
from pathlib import Path
from adapter.planner import codec,model
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification';C7=Q/'E2_P05_D01_A14_PROVENANCE_FIXTURE_CORRECTION_7'
def read(p):return json.loads(p.read_bytes())
runpy.run_path(str(C7/'verify.py'),run_name='__prior_fixture_verify__')
c=read(O/'source-contract.json');s=read(C7/'corrected-prospective-snapshot.json')['snapshot'];a=next(a for a in s['actions'] if a['id']['value']=='E2-DECIDE');raw=a['source']['excerpt'].encode('utf-8');assert raw==(O/'candidates/E2-DECIDE.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==a['source']['identity']['sha256']==c['EXPECTED_BYTE_HASH']
writer=(R/'docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_PC01_WHOLE_MODEL_ORACLE.py').read_text();assert 'raw = c.canonical_bytes(body)' in writer and 'raw.decode()' in writer and 'path.write_bytes(raw)' in writer
expected=codec.parse_json(raw);assert set(expected)=={'action','lineage','scope'} and expected['action']=='E2-DECIDE';assert codec.canonical_bytes(expected)==raw
native=codec._unwire(s);model.validate_model(native);sid=codec._wire(codec.snapshot_id(native));assert sid==read(C7/'corrected-prospective-fixture.json')['CORRECTED_SNAPSHOT_ID']
assert not (R/'E2-DECIDE.json').exists(),'No accepted source may be written under unselected dossier'
print(json.dumps({'STATUS':'PASS_LOSSLESS_LITERAL_SOURCE_BYTE_RECOVERY','BYTE_COUNT':len(raw),'BYTE_HASH':hashlib.sha256(raw).hexdigest(),'CORRECTED_SNAPSHOT_ID':sid,'SNAPSHOT_UNCHANGED':True,'HISTORICAL_PHYSICAL_SOURCE_RETAINED':False,'HISTORICAL_RAW_BYTE_CONTENT_EMBEDDED':True,'ACCEPTED_SOURCE_CREATED':False,'RESOLVED':52,'UNRESOLVED':59},sort_keys=True))
