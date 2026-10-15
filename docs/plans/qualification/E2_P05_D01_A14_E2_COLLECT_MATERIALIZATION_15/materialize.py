"""Bounded byte copy plus read-only native source-pin frontier."""
import hashlib,json,ast
from pathlib import Path
from adapter.planner import codec,model,replay
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;C14=O.parent/'E2_P05_D01_A14_E2_COLLECT_SOURCE_RECOVERY_14'
OPTION='AUTHORIZE_BOUNDED_A14_E2_COLLECT_LOSSLESS_SOURCE_MATERIALIZATION'
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def pin(p):return {'path':str(p.relative_to(R)),'raw_sha256':sha(p.read_bytes())}
def save(n,v):(O/n).write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
def at(v,p):
 for k in p.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
s=read(C14/'bounded-materialization-subject.json');d=read(C14/'bounded-source-decision-dossier.json');body=dict(s);subject=body.pop('SUBJECT_IDENTITY');assert subject=='qualification-A14-E2COLLECT-materialization-v1:'+sha(canon(body))
assert d['OPTION']==OPTION and d['SUBJECT_IDENTITY']==subject and d['DECISION_READY'] and d['SELECTION']=='NOT_SELECTED'
assert sha((R/d['EXACT_SUBJECT']['path']).read_bytes())==d['EXACT_SUBJECT']['raw_sha256']
assert s['EXACT_ROOT']==str(R) and s['EXISTING_RELATIVE_PATH']=='E2-COLLECT.json';target=codec._path(R,s['EXISTING_RELATIVE_PATH']);assert target==R/'E2-COLLECT.json' and not target.exists() and not target.is_symlink()
raw=(R/s['ISOLATED_CANDIDATE']['path']).read_bytes();assert len(raw)==s['EXPECTED_LENGTH']==91 and sha(raw)==s['EXPECTED_SHA256']==s['ISOLATED_CANDIDATE']['raw_sha256'] and raw==s['RAW_BYTES_UTF8'].encode()
embedded=s['AUTHORITATIVE_BYTE_SOURCE'];assert sha((R/embedded['path']).read_bytes())==embedded['raw_sha256'] and at(read(R/embedded['path']),embedded['pointer']).encode()==raw
writer=read(C14/'source-contract.json')['CANONICAL_SERIALIZER']['WRITER'];wp=R/writer['path'];assert sha(wp.read_bytes())==writer['raw_sha256'];tree=ast.parse(wp.read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_source');calls=[ast.dump(n) for n in ast.walk(fn) if isinstance(n,ast.Call)];assert all(any("attr='"+name+"'" in c for c in calls) for name in ['canonical_bytes','write_bytes','decode'])
sp=R/s['BASE_SNAPSHOT_SOURCE']['path'];before=sp.read_bytes();assert sha(before)==s['BASE_SNAPSHOT_SOURCE']['raw_sha256'];snapshot=codec.decode_snapshot(before);model.validate_model(snapshot);pre=codec._wire(codec.snapshot_id(snapshot));assert pre==s['BASE_SNAPSHOT_ID']==s['EXPECTED_POST_MATERIALIZATION_SNAPSHOT_ID']
for ref in s['EXISTING_PROVENANCE']:assert at(read(sp),ref['POINTER'])==ref['PROVENANCE'] and ref['PROVENANCE']['identity']==s['EXPECTED_CONTENT_IDENTITY'] and ref['PROVENANCE']['excerpt'].encode()==raw
save('scope-authentication.json',{'SELECTED_OPTION':OPTION,'SCOPE_AUTHENTICATION':'PASS','METHOD':'Current human selection matched exact Recovery14 option, subject digest, raw subject-file pin, bytes, root/path and unchanged Snapshot commitment','RECOVERY_DOSSIER':pin(C14/'bounded-source-decision-dossier.json'),'SEALED_SUBJECT':subject,'SUBJECT_SOURCE':pin(C14/'bounded-materialization-subject.json'),'ALLOWLIST':[str(target),'New package qualification evidence'],'EXCLUSIONS':s['SCOPE_EXCLUSIONS'],'NOTE':'Recovery14 no-materialization restriction remains historical; this package records its separate explicit bounded authorization','NATIVE_AUTHORITY_ISSUED':False})
save('pre-materialization-snapshot-oracle.json',{'SOURCE':s['BASE_SNAPSHOT_SOURCE'],'SNAPSHOT_CONTENT_POINTER':'/snapshot','PRE_MATERIALIZATION_SNAPSHOT_ID':pre,'EXPECTED_POST_MATERIALIZATION_SNAPSHOT_ID':pre,'SOURCE_PROVENANCE':s['EXISTING_PROVENANCE'],'CONTENT_IDENTITY':s['EXPECTED_CONTENT_IDENTITY'],'PATH':str(target),'SCOPE':snapshot.context.scope,'LINEAGE':snapshot.context.lineage,'GENERATION':snapshot.context.generation,'FULL_OUTPUT_ORACLE':False})
with target.open('xb') as f:f.write(raw)
assert target.read_bytes()==raw and len(target.read_bytes())==91 and sha(target.read_bytes())==s['EXPECTED_SHA256']
pins={}
for prov in replay.provenance_records(snapshot):
 model.validate_provenance(prov);p=model.ArtifactPin(prov.path,prov.identity,model.HashProfile.RAW);codec.validate_pin(p);codec._path(R,p.path);key=(p.path,p.pointer,p.profile);assert key not in pins or pins[key]==p;pins[key]=p
model.unique(tuple(pins.values()),lambda p:(p.path,p.pointer,p.profile));checkpins=[p for p in pins.values() if p.path=='E2-COLLECT.json'];assert len(checkpins)==1 and codec.load_pinned(R,checkpins[0])==raw
value=codec.parse_json(raw);assert value=={'action':'E2-COLLECT','scope':snapshot.context.scope,'lineage':snapshot.context.lineage}
assert sp.read_bytes()==before;post=codec._wire(codec.snapshot_id(codec.decode_snapshot(sp.read_bytes())));assert pre==post
save('accepted-source-validation.json',{'SOURCE':pin(target),'BYTE_LENGTH':91,'EXPECTED_SHA256':s['EXPECTED_SHA256'],'ACTUAL_SHA256':sha(target.read_bytes()),'BYTE_EQUALITY':'PASS','CONTENT_IDENTITY':s['EXPECTED_CONTENT_IDENTITY'],'PROVENANCE_VALIDATION':'PASS_NATIVE_RAW_PIN_CANONICAL_PATH_SCOPE_LINEAGE','SOURCE_PIN':codec._wire(checkpins[0]),'RAW_PIN_KEYS_UNIQUE':'PASS','NO_ALIAS':'PASS_NON_SYMLINK_EXACT_TARGET','SOURCE_PATH_CHANGED':'NO','SOURCE_PIN_CHANGED':'NO','PROVENANCE_IDENTITY_CHANGED':'NO','CONTENT_IDENTITY_CHANGED':'NO','AUTHORITY_CHANGED':'NO','SCHEMA_CHANGED':'NO','SEMANTIC_FACTS_CHANGED':'NO','SNAPSHOT_FIELDS_CHANGED':'NO','PRE_MATERIALIZATION_SNAPSHOT_ID':pre,'POST_MATERIALIZATION_SNAPSHOT_ID':post,'SNAPSHOT_IDENTITY_UNCHANGED':'YES','ORIGINAL_STANDALONE_RETENTION_CLAIMED':False,'NO_RESERIALIZATION':True})
rows=[]
for i,p in enumerate(pins.values()):
 try:codec.load_pinned(R,p);present=True;error=None
 except model.PlannerError as e:present=False;error=str(e)
 rows.append({'SOURCE_PATH':p.path,'EXPECTED_IDENTITY':codec._wire(p.identity),'FIRST_LOOKUP_ORDER':i+1,'PRESENT':'YES' if present else 'NO','ERROR':error})
missing=[r['SOURCE_PATH'] for r in rows if r['PRESENT']=='NO'];old=read(C14/'a14-source-frontier.json');assert len(rows)==10 and missing==old['MISSING_SOURCE_ORDER'][1:] and len(missing)==3
save('a14-source-frontier.json',{'SOURCE_PINS_TOTAL':10,'SOURCE_PINS_PRESENT':7,'SOURCE_PINS_MISSING':3,'MISSING_ORDER':missing,'NEXT_MISSING_SOURCE':missing[0],'ROWS':rows,'LATER_SOURCE_BYTES_RECOVERED':False,'LATER_SOURCES_MATERIALIZED':False,'MODE':'Read-only physical pin availability/authentication only; no source byte extraction'})
impact=read(C14/'operand-impact.json');assert len(impact['ROWS'])==16 and impact['RESOLVED_OPERANDS']==52 and impact['UNRESOLVED_OPERANDS']==59
save('operand-frontier.json',{'PREVIOUSLY_RESOLVED':52,'RESOLVED_BY_E2_COLLECT':0,'TOTAL_RESOLVED':52,'TOTAL_UNRESOLVED':59,'A14_DEPENDENT_REFERENCES':[dict(r,STATUS='UNRESOLVED_NO_PROMOTION',MATERIALIZATION_EFFECT='E2-COLLECT availability satisfied; complete source/bundle or boundary/mutation contract still unsatisfied') for r in impact['ROWS']],'OTHER_UNRESOLVED_COUNT':43,'REASON':'No missing invocation operand is solely the E2-COLLECT file. Bundle, saved identity, reader inputs and transitive N02 boundary/mutation descriptors remain incomplete.','INVOCATION_STATIC_PREFLIGHT':'NOT_RUN'})
save('static-a14-handoff-frontier.json',{'SOURCE_PREFLIGHT':'E2-COLLECT PASS; E2-FINISH first remaining missing source','NEXT_A14_BLOCKER':next(r for r in rows if r['PRESENT']=='NO'),'BUNDLE_PREFLIGHT':'NOT_RUN_COMPLETE_SOURCE_POLICY_HISTORY_CLOSURE_REQUIRED','SAVE_PREFLIGHT':'STATIC_CONTRACT_ONLY_NO_SAVE','WRITER_TERMINATION':'FUTURE_PROCESS_BARRIER_REQUIRED_NOT_EXECUTED','COLD_READER_PREFLIGHT':'STATIC_CONTRACT_ONLY_NO_READER','NEXT_BLOCKER_REPAIRED':False,'CURRENT_AUTHORIZATION_REUSED':False})
print(json.dumps({'SCOPE_AUTHENTICATION':'PASS','BYTE_LENGTH':91,'SNAPSHOT_UNCHANGED':True,'SOURCE_PINS_PRESENT':7,'SOURCE_PINS_MISSING':3,'NEXT_MISSING_SOURCE':missing[0],'COUNTS':'52/59'}))
