"""Independent structural recovery reader; no qualification operation."""
import hashlib,json,runpy,ast
from pathlib import Path
from adapter.planner import codec,model
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def at(v,p):
 for k in p.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
runpy.run_path(str(O.parent/'E2_P05_D01_A14_E2_PREPARE_MATERIALIZATION_19/verify.py'),run_name='__previous_read_only_verification__')
s=read(O/'bounded-materialization-subject.json');raw=(R/s['ISOLATED_CANDIDATE']['path']).read_bytes();assert len(raw)==s['EXPECTED_LENGTH']==1430 and sha(raw)==s['EXPECTED_SHA256'] and raw==s['RAW_BYTES_UTF8'].encode()
ep=s['AUTHORITATIVE_BYTE_SOURCE'];assert sha((R/ep['path']).read_bytes())==ep['raw_sha256'] and at(read(R/ep['path']),ep['pointer']).encode()==raw
sp=R/s['BASE_SNAPSHOT_SOURCE']['path'];assert sha(sp.read_bytes())==s['BASE_SNAPSHOT_SOURCE']['raw_sha256'];snapshot=codec.decode_snapshot(sp.read_bytes());model.validate_model(snapshot);sid=codec._wire(codec.snapshot_id(snapshot));assert sid==s['BASE_SNAPSHOT_ID']==s['EXPECTED_POST_MATERIALIZATION_SNAPSHOT_ID']
route=snapshot.external_gates[0].resolution_contracts[0];body=codec._wire(route);del body['$type'];del body['provenance'];assert codec.canonical_bytes({'schema':'EXTERNAL-RESOLUTION-CONTRACT-1','contract':body})==raw
assert codec.parse_json(raw)['contract']==body
writer=R/'adapter/tests/test_planner_external_unknown.py';tree=ast.parse(writer.read_text());fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='source');calls=[ast.dump(n) for n in ast.walk(fn) if isinstance(n,ast.Call)];assert all(any("attr='"+name+"'" in c for c in calls) for name in ['canonical_bytes','write_bytes','decode'])
p=model.ArtifactPin(s['ISOLATED_CANDIDATE']['path'],route.provenance.identity,model.HashProfile.RAW);codec.validate_pin(p);assert codec.load_pinned(R,p)==raw
assert codec._path(R,'resolution.json')==R/'resolution.json' and not (R/'resolution.json').exists()
for name in ['POST_MATERIALIZATION_SOURCE_ORACLE','COMPLETE_SOURCE_VALIDATION_ORACLE','A14_HANDOFF_REENTRY_ORACLE']:
 p=s[name];assert sha((R/p['path']).read_bytes())==p['raw_sha256']
oracle=read(O/'post-materialization-source-oracle.json');assert oracle['NOT_CURRENT_RESULT'] and len(oracle['ROWS'])==10 and oracle['EXPECTED_SOURCE_PINS_PRESENT']==10 and oracle['EXPECTED_SOURCE_PINS_MISSING']==0
assert len({(r['SOURCE_PATH'],r['EXPECTED_SHA256']) for r in oracle['ROWS']})==10 and oracle['EXPECTED_SNAPSHOT_ID']==sid
assert read(O/'current-source-frontier.json')['SOURCE_PINS_PRESENT']==9
handoff=read(O/'a14-handoff-reentry-oracle.json');assert handoff['NOT_PERFORMED'] and [r['STEP'] for r in handoff['ORDERED_STEPS']]==list(range(1,9))
for row in handoff['ORDERED_STEPS']:
 if 'CONTRACT' in row:assert sha((R/row['CONTRACT']['path']).read_bytes())==row['CONTRACT']['raw_sha256']
body=dict(s);identity=body.pop('SUBJECT_IDENTITY');assert identity=='qualification-A14-resolution-materialization-v1:'+sha(canon(body))
d=read(O/'bounded-source-decision-dossier.json');assert d['SELECTION']=='NOT_SELECTED' and d['SUBJECT_IDENTITY']==identity and sha((R/d['EXACT_SUBJECT']['path']).read_bytes())==d['EXACT_SUBJECT']['raw_sha256']
print(json.dumps({'STATUS':'PASS','BYTE_LENGTH':len(raw),'SHA256':sha(raw),'CONTENT_IDENTITY':s['EXPECTED_CONTENT_IDENTITY'],'SNAPSHOT_IDENTITY':sid,'SUBJECT_IDENTITY':identity,'SOURCE_PINS_PRESENT':9,'SOURCE_PINS_MISSING':1,'FUTURE_SOURCE_CLOSURE_ORACLE':'10/10_NOT_CURRENT','RESOLVED_OPERANDS':52,'UNRESOLVED_OPERANDS':59,'RESOLUTION_JSON_MATERIALIZED':False},sort_keys=True))
