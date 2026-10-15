"""Exact authorized byte copy, unchanged Snapshot and complete physical sources."""
import json,hashlib
from pathlib import Path
from adapter.planner import codec,model,replay
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;C20=O.parent/'E2_P05_D01_A14_RESOLUTION_SOURCE_RECOVERY_20'
OPTION='AUTHORIZE_BOUNDED_A14_RESOLUTION_LOSSLESS_SOURCE_MATERIALIZATION'
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def pin(p):return {'path':str(p.relative_to(R)),'raw_sha256':sha(p.read_bytes())}
def save(n,v):(O/n).write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
def at(v,p):
 for k in p.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
s=read(C20/'bounded-materialization-subject.json');d=read(C20/'bounded-source-decision-dossier.json');body=dict(s);identity=body.pop('SUBJECT_IDENTITY');assert identity=='qualification-A14-resolution-materialization-v1:'+sha(canon(body))
assert d['OPTION']==OPTION and d['SUBJECT_IDENTITY']==identity and d['DECISION_READY'];assert sha((R/d['EXACT_SUBJECT']['path']).read_bytes())==d['EXACT_SUBJECT']['raw_sha256']
for k in ['POST_MATERIALIZATION_SOURCE_ORACLE','COMPLETE_SOURCE_VALIDATION_ORACLE','A14_HANDOFF_REENTRY_ORACLE']:
 p=s[k];assert sha((R/p['path']).read_bytes())==p['raw_sha256']
assert s['EXACT_ROOT']==str(R) and s['EXISTING_RELATIVE_PATH']=='resolution.json';target=codec._path(R,'resolution.json');assert target==R/'resolution.json' and not target.exists() and not target.is_symlink()
raw=(R/s['ISOLATED_CANDIDATE']['path']).read_bytes();assert len(raw)==s['EXPECTED_LENGTH']==1430 and sha(raw)==s['EXPECTED_SHA256']==s['ISOLATED_CANDIDATE']['raw_sha256'] and raw==s['RAW_BYTES_UTF8'].encode()
ep=s['AUTHORITATIVE_BYTE_SOURCE'];assert sha((R/ep['path']).read_bytes())==ep['raw_sha256'] and at(read(R/ep['path']),ep['pointer']).encode()==raw
sp=R/s['BASE_SNAPSHOT_SOURCE']['path'];before=sp.read_bytes();assert sha(before)==s['BASE_SNAPSHOT_SOURCE']['raw_sha256'];snapshot=codec.decode_snapshot(before);model.validate_model(snapshot);pre=codec._wire(codec.snapshot_id(snapshot));assert pre==s['BASE_SNAPSHOT_ID']==s['EXPECTED_POST_MATERIALIZATION_SNAPSHOT_ID']
save('scope-authentication.json',{'SELECTED_OPTION':OPTION,'SCOPE_AUTHENTICATION':'PASS','SEALED_SUBJECT':identity,'RECOVERY_DOSSIER':pin(C20/'bounded-source-decision-dossier.json'),'METHOD':'Current explicit human selection matched option, exact subject hash/digest, byte commitment, root/path and unchanged Snapshot. Current task additionally authorizes sealed read-only validation/static reentry; no runtime authority.','ALLOWLIST':[str(target),'Read-only complete-source oracle','Static handoff/111-reference audit','New package evidence'],'EXCLUSIONS':s['SCOPE_EXCLUSIONS'],'NATIVE_AUTHORITY_ISSUED':False})
save('pre-materialization-snapshot-oracle.json',{'SOURCE':s['BASE_SNAPSHOT_SOURCE'],'PRE_MATERIALIZATION_SNAPSHOT_ID':pre,'EXPECTED_POST_MATERIALIZATION_SNAPSHOT_ID':pre,'SOURCE_PROVENANCE':s['EXISTING_PROVENANCE'],'CONTENT_IDENTITY':s['EXPECTED_CONTENT_IDENTITY'],'PATH':str(target),'SCOPE':snapshot.context.scope,'LINEAGE':snapshot.context.lineage,'GENERATION':snapshot.context.generation,'FULL_OUTPUT_ORACLE':False})
with target.open('xb') as f:f.write(raw)
actual=target.read_bytes();assert actual==raw and len(actual)==1430 and sha(actual)==s['EXPECTED_SHA256']
oracle=read(R/s['POST_MATERIALIZATION_SOURCE_ORACLE']['path']);pins={}
for prov in replay.provenance_records(snapshot):
 model.validate_provenance(prov);p=model.ArtifactPin(prov.path,prov.identity,model.HashProfile.RAW);codec.validate_pin(p);codec._path(R,p.path);key=(p.path,p.pointer,p.profile);assert key not in pins or pins[key]==p;pins[key]=p
model.unique(tuple(pins.values()),lambda p:(p.path,p.pointer,p.profile));assert len(pins)==len(oracle['ROWS'])==10
assert {canon(codec._wire(p)) for p in pins.values()}=={canon(r['EXPECTED_PIN']) for r in oracle['ROWS']}
rows=[]
for row in oracle['ROWS']:
 p=codec._unwire(row['EXPECTED_PIN']);b=codec.load_pinned(R,p);assert sha(b)==row['EXPECTED_SHA256'];assert codec._path(R,p.path).is_file() and not (R/p.path).is_symlink()
 assert row['SCOPE']==snapshot.context.scope and row['LINEAGE']==snapshot.context.lineage and row['GENERATION']==snapshot.context.generation
 for ref in row['EXACT_PROVENANCE_REFERENCES']:assert at(read(sp),ref['POINTER'])==ref['PROVENANCE'] and ref['PROVENANCE']['scope']==snapshot.context.scope
 rows.append({'SOURCE_PATH':p.path,'CONTENT_IDENTITY':codec._wire(p.identity),'SHA256':sha(b),'PIN':codec._wire(p),'PROVENANCE_ROLES':row['PROVENANCE_ROLES'],'SCOPE':row['SCOPE'],'LINEAGE':row['LINEAGE'],'STATUS':'PASS','PHYSICAL_SOURCE':pin(R/p.path)})
route=snapshot.external_gates[0].resolution_contracts[0];rb=codec._wire(route);del rb['$type'];del rb['provenance'];assert codec.canonical_bytes({'schema':'EXTERNAL-RESOLUTION-CONTRACT-1','contract':rb})==raw
assert sp.read_bytes()==before;post=codec._wire(codec.snapshot_id(codec.decode_snapshot(sp.read_bytes())));assert pre==post
save('accepted-source-validation.json',{'SOURCE':pin(target),'BYTE_LENGTH':1430,'EXPECTED_SHA256':s['EXPECTED_SHA256'],'ACTUAL_SHA256':sha(actual),'BYTE_EQUALITY':'PASS','CONTENT_IDENTITY':s['EXPECTED_CONTENT_IDENTITY'],'PROVENANCE_VALIDATION':'PASS_NATIVE_RAW_PIN_PATH_SCOPE_LINEAGE_AND_ROUTE_BODY','SOURCE_PATH_CHANGED':'NO','SOURCE_PIN_CHANGED':'NO','PROVENANCE_IDENTITY_CHANGED':'NO','CONTENT_IDENTITY_CHANGED':'NO','AUTHORITY_CHANGED':'NO','SCHEMA_CHANGED':'NO','SNAPSHOT_FIELDS_CHANGED':'NO','PRE_MATERIALIZATION_SNAPSHOT_ID':pre,'POST_MATERIALIZATION_SNAPSHOT_ID':post,'SNAPSHOT_IDENTITY_RESULT':'PASS_UNCHANGED_AS_SEALED_BY_RECOVERY20'})
save('complete-source-validation.json',{'STATUS':'PASS','SEALED_ORACLE':s['COMPLETE_SOURCE_VALIDATION_ORACLE'],'SOURCE_PINS_TOTAL':10,'SOURCE_PINS_PRESENT':10,'SOURCE_PINS_MISSING':0,'A14_PHYSICAL_SOURCE_CLOSURE':'PASS','ROWS':rows,'ALL_NATIVE_PROVENANCE_PRESENT':'PASS','RAW_PIN_KEYS_UNIQUE':'PASS','CANONICAL_PATHS':'PASS','NO_ALIASES_LAUNDERING':'PASS_EXACT_PHYSICAL_LOOKUP_AND_IDENTITIES','NATIVE_MODEL_SNAPSHOT_VALIDATION':'PASS','SNAPSHOT_IDENTITY':post,'ORDERED_HISTORY_OR_BUNDLE_CLOSURE_PROVEN':False,'QUALIFICATION_OPERATIONS_EXECUTED':0})
print(json.dumps({'SCOPE_AUTHENTICATION':'PASS','BYTES':1430,'PHYSICAL_SOURCE_CLOSURE':'10/10_PASS','SNAPSHOT_UNCHANGED':True}))
