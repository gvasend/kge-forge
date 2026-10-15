"""Authorized exact byte copy and static first-failure preflight only."""
import hashlib,json
from pathlib import Path
from adapter.planner import codec,model,replay
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;C10=O.parent/'E2_P05_D01_A14_SOURCE_JSON_RECOVERY_10'
OPTION='AUTHORIZE_BOUNDED_A14_SOURCE_JSON_LOSSLESS_SOURCE_MATERIALIZATION'
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def pin(p):return {'path':str(p.relative_to(R)),'raw_sha256':sha(p.read_bytes())}
def save(n,v):(O/n).write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
def at(v,p):
 for k in p.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
s=read(C10/'bounded-materialization-subject.json');d=read(C10/'bounded-source-decision-dossier.json');body=dict(s);sid=body.pop('SUBJECT_IDENTITY')
assert sid=='qualification-A14-sourcejson-materialization-v1:'+sha(canon(body))
assert d['OPTION']==OPTION and d['SUBJECT_IDENTITY']==sid and d['DECISION_READY'] and d['SELECTION']=='NOT_SELECTED'
assert sha((R/d['EXACT_SUBJECT']['path']).read_bytes())==d['EXACT_SUBJECT']['raw_sha256']
root=Path(s['EXACT_ROOT']);assert root==R and root.resolve()==root and s['EXISTING_RELATIVE_PATH']=='source.json'
target=codec._path(root,s['EXISTING_RELATIVE_PATH']);assert target==R/'source.json' and not target.exists() and not target.is_symlink()
raw=(R/s['ISOLATED_RECOVERED_CANDIDATE']['path']).read_bytes();assert len(raw)==s['EXPECTED_LENGTH']==617 and sha(raw)==s['EXPECTED_SHA256']==s['ISOLATED_RECOVERED_CANDIDATE']['raw_sha256'] and raw==s['RAW_BYTES_UTF8'].encode()
assert len(s['AUTHORITATIVE_EXACT_BYTE_SOURCES'])==10
copies=[]
for p in s['AUTHORITATIVE_EXACT_BYTE_SOURCES']:
 b=(R/p['path']).read_bytes();assert b==raw and sha(b)==p['raw_sha256']==s['EXPECTED_SHA256'];copies.append({'SOURCE':p,'BYTE_LENGTH':len(b),'SHA256':sha(b),'BYTE_EQUALITY':'PASS'})
ep=s['AUTHORITATIVE_A14_EMBEDDED_POINTER'];assert sha((R/ep['path']).read_bytes())==ep['raw_sha256'] and at(read(R/ep['path']),ep['pointer']).encode()==raw
sp=R/s['BASE_SNAPSHOT_SOURCE']['path'];before=sp.read_bytes();assert sha(before)==s['BASE_SNAPSHOT_SOURCE']['raw_sha256'];snapshot=codec.decode_snapshot(before);model.validate_model(snapshot);pre=codec._wire(codec.snapshot_id(snapshot));assert pre==s['BASE_SNAPSHOT_ID']
for ref in s['EXISTING_PROVENANCE_REFERENCES']:assert at(read(sp),ref['POINTER'])==ref['PROVENANCE'] and ref['PROVENANCE']['identity']==s['EXPECTED_CONTENT_IDENTITY'] and ref['PROVENANCE']['path']=='source.json'
save('scope-authentication.json',{'SELECTED_OPTION':OPTION,'SCOPE_AUTHENTICATION':'PASS','METHOD':'Explicit current-user selection matched to sealed option, subject digest and raw subject-file hash, exact root/path, bytes and Snapshot commitment','RECOVERY_DOSSIER':pin(C10/'bounded-source-decision-dossier.json'),'SEALED_SUBJECT':sid,'SUBJECT_SOURCE':pin(C10/'bounded-materialization-subject.json'),'AUTHORIZED_TARGET':str(target),'EXCLUSIONS':s['SCOPE_EXCLUSIONS'],'NATIVE_AUTHORITY_ISSUED':False})
save('retained-copy-consistency.json',{'STATUS':'PASS','COUNT':10,'ROWS':copies})
save('pre-materialization-snapshot-oracle.json',{'SOURCE':s['BASE_SNAPSHOT_SOURCE'],'SNAPSHOT_CONTENT_POINTER':'/snapshot','PRE_MATERIALIZATION_SNAPSHOT_ID':pre,'EXPECTED_POST_MATERIALIZATION_SNAPSHOT_ID':pre,'SOURCE_PROVENANCE':s['EXISTING_PROVENANCE_REFERENCES'],'SCOPE':snapshot.context.scope,'LINEAGE':snapshot.context.lineage,'GENERATION':snapshot.context.generation,'SOURCE_PATH':str(target),'CONTENT_IDENTITY':s['EXPECTED_CONTENT_IDENTITY'],'FULL_OUTPUT_ORACLE':False})
with target.open('xb') as f:f.write(raw)
actual=target.read_bytes();assert actual==raw and len(actual)==617 and sha(actual)==s['EXPECTED_SHA256']
required={}
for prov in replay.provenance_records(snapshot):
 model.validate_provenance(prov);p=model.ArtifactPin(prov.path,prov.identity,model.HashProfile.RAW);codec.validate_pin(p);codec._path(root,p.path);key=(p.path,p.pointer,p.profile);assert key not in required or required[key]==p;required[key]=p
model.unique(tuple(required.values()),lambda p:(p.path,p.pointer,p.profile))
sourcepins=[p for p in required.values() if p.path=='source.json'];assert len(sourcepins)==1 and codec.load_pinned(root,sourcepins[0])==raw
value=codec.parse_json(actual);assert value['schema']=='SYNTHETIC-GOVERNED-RULE-ACQUISITION-1' and value['scope']=='TEST/scope' and value['lineage']=='TEST/lineage'
assert sp.read_bytes()==before;post=codec._wire(codec.snapshot_id(codec.decode_snapshot(sp.read_bytes())));assert pre==post
save('accepted-source-validation.json',{'SOURCE':pin(target),'BYTE_LENGTH':617,'EXPECTED_SHA256':s['EXPECTED_SHA256'],'ACTUAL_SHA256':sha(actual),'BYTE_EQUALITY':'PASS','RETAINED_COPY_CONSISTENCY':'PASS_10_OF_10','CONTENT_IDENTITY':s['EXPECTED_CONTENT_IDENTITY'],'PROVENANCE_VALIDATION':'PASS_NATIVE_RAW_PIN_PATH_PROVENANCE_AND_UNIQUE_KEY','SOURCE_PIN':codec._wire(sourcepins[0]),'SCOPE':snapshot.context.scope,'LINEAGE':snapshot.context.lineage,'PAYLOAD_SCOPE':value['scope'],'PAYLOAD_LINEAGE':value['lineage'],'PAYLOAD_SCOPE_NOTE':'Opaque TEST template payload preserved; native E2 consuming scope and lineage unchanged','RAW_PIN_KEYS_UNIQUE':'PASS','NO_ALIAS':'PASS_NON_SYMLINK_CANONICAL_TARGET','SOURCE_PATH_CHANGED':'NO','SOURCE_PIN_CHANGED':'NO','PROVENANCE_IDENTITY_CHANGED':'NO','CONTENT_IDENTITY_CHANGED':'NO','AUTHORITY_CHANGED':'NO','SCHEMA_CHANGED':'NO','SNAPSHOT_FIELDS_CHANGED':'NO','PRE_MATERIALIZATION_SNAPSHOT_ID':pre,'POST_MATERIALIZATION_SNAPSHOT_ID':post,'SNAPSHOT_IDENTITY_UNCHANGED':'YES'})
lookups=[];block=None
for p in required.values():
 try:codec.load_pinned(root,p);lookups.append({'PIN':codec._wire(p),'STATUS':'PASS'})
 except model.PlannerError as e:
  block={'PIN':codec._wire(p),'STATUS':'BLOCKED','ERROR':str(e),'ROOT':str(root),'OUTSIDE_SELECTED_SCOPE':True};lookups.append(block);break
assert block,'Source lookup frontier exhausted: stop and inspect static contracts; do not execute replay'
impact=read(C10/'operand-impact-and-frontier.json');assert impact['RESOLVED_OPERANDS']==52 and impact['UNRESOLVED_OPERANDS']==59
save('static-a14-handoff-frontier.json',{'LOOKUPS_THROUGH_FIRST_BLOCKER':lookups,'NEXT_A14_BLOCKER':block,'SOURCE_PREFLIGHT':'source.json PASS; stopped at first remaining native source lookup failure','BUNDLE_PREFLIGHT':'NOT_RUN_COMPLETE_SOURCE_POLICY_HISTORY_CLOSURE_REQUIRED','SAVE_PREFLIGHT':'STATIC_CONTRACT_ONLY_NO_SAVE','WRITER_TERMINATION':'FUTURE_PROCESS_BARRIER_REQUIRED_NOT_EXECUTED','COLD_READER_PREFLIGHT':'STATIC_CONTRACT_ONLY_NO_READER','A14_DEPENDENT_REFERENCES':impact['ROWS'],'PREVIOUSLY_RESOLVED':52,'RESOLVED_BY_SOURCE_JSON':0,'TOTAL_RESOLVED':52,'TOTAL_UNRESOLVED':59,'REASON_NO_OPERAND_PROMOTED':'All A14-dependent source/bundle/save/reader operands still require complete source and boundary closure; none depends solely on missing source.json physical bytes','INVOCATION_STATIC_PREFLIGHT':'NOT_RUN','NEXT_BLOCKER_REPAIRED':False})
print(json.dumps({'SCOPE_AUTHENTICATION':'PASS','BYTE_LENGTH':617,'SNAPSHOT_UNCHANGED':True,'NEXT_BLOCKER':block,'COUNTS':'52/59'}))
