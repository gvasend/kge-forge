"""Authorized byte copy only. No reserialization, transition, save or restore."""
import hashlib,json
from pathlib import Path
from adapter.planner import codec,model,replay
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification';C8=Q/'E2_P05_D01_A14_E2_DECIDE_SOURCE_RECOVERY_8';C7=Q/'E2_P05_D01_A14_PROVENANCE_FIXTURE_CORRECTION_7'
OPTION='AUTHORIZE_BOUNDED_A14_E2_DECIDE_LOSSLESS_SOURCE_MATERIALIZATION'
def read(p):return json.loads(Path(p).read_bytes())
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p,ptr=''):
 p=Path(p);return {'path':str(p.relative_to(R)),'pointer':ptr,'raw_sha256':sha(p.read_bytes())}
def save(n,v):(O/n).write_bytes(canon(v)+b'\n')
def at(v,ptr):
 for k in ptr.split('/')[1:]:v=v[int(k)] if isinstance(v,list) else v[k.replace('~1','/').replace('~0','~')]
 return v
dossier=read(C8/'bounded-source-decision-dossier.json');subject=read(C8/'bounded-source-materialization-subject.json');body=dict(subject);sid=body.pop('SUBJECT_IDENTITY');assert sid=='qualification-A14-E2DECIDE-materialization-v1:'+sha(canon(body))
assert dossier['OPTION']==OPTION and dossier['SUBJECT_IDENTITY']==sid and dossier['DECISION_READY'];sp=dossier['SUBJECT_SOURCE'];assert sha((R/sp['path']).read_bytes())==sp['raw_sha256']
root=Path(subject['SOURCE_ROOT']);assert root==R and root.resolve()==root;assert subject['PROPOSED_ACCEPTED_PATH']=='E2-DECIDE.json';target=codec._path(root,subject['PROPOSED_ACCEPTED_PATH']);assert target==root/'E2-DECIDE.json' and target.resolve()==target
candidatepin=subject['ISOLATED_CANDIDATE'];raw=(R/candidatepin['path']).read_bytes();assert sha(raw)==candidatepin['raw_sha256']==subject['EXPECTED_RAW_IDENTITY']['sha256'] and len(raw)==subject['BYTE_COUNT']==90
embeddedpin=subject['AUTHORITATIVE_EMBEDDED_BYTE_SOURCE'];container=R/embeddedpin['path'];assert sha(container.read_bytes())==embeddedpin['raw_sha256'];embedded=at(read(container),embeddedpin['pointer']);assert embedded.encode('utf-8')==raw==subject['RAW_BYTES_UTF8'].encode('utf-8')
writer=R/'docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_PC01_WHOLE_MODEL_ORACLE.py';text=writer.read_text();assert 'raw = c.canonical_bytes(body)' in text and 'path.write_bytes(raw)' in text and 'raw.decode()' in text
snapshotpath=R/subject['BASE_CORRECTED_SNAPSHOT_SOURCE']['path'];beforebytes=snapshotpath.read_bytes();assert sha(beforebytes)==subject['BASE_CORRECTED_SNAPSHOT_SOURCE']['raw_sha256'];snapshot=codec.decode_snapshot(beforebytes);pre=codec._wire(codec.snapshot_id(snapshot));assert pre==subject['BASE_CORRECTED_SNAPSHOT_ID'];action=next(a for a in snapshot.actions if a.id.value=='E2-DECIDE');assert codec._wire(action.source)==subject['EXPECTED_EXISTING_PROVENANCE']
save('scope-authentication.json',{'SELECTED_OPTION':OPTION,'SCOPE_AUTHENTICATION':'PASS','METHOD':'Explicit current-user selection matched to exact sealed option, subject digest, raw dossier subject pin, root/path and byte commitment','DOSSIER_SOURCE':pin(C8/'bounded-source-decision-dossier.json'),'SEALED_SUBJECT':sid,'SUBJECT_SOURCE':pin(C8/'bounded-source-materialization-subject.json'),'ALLOWLIST':['Create only /home/gvasend/app/kge-forge/E2-DECIDE.json from exact isolated recovered bytes','Read-only verification and qualification evidence'],'EXCLUSIONS':subject['SCOPE_LIMIT'],'NATIVE_AUTHORITY_ISSUANCE':False})
save('pre-materialization-snapshot-oracle.json',{'SOURCE':pin(snapshotpath),'SNAPSHOT_CONTENT_REFERENCE':pin(snapshotpath,'/snapshot'),'PRE_MATERIALIZATION_SNAPSHOT_ID':pre,'EXPECTED_POST_MATERIALIZATION_SNAPSHOT_ID':pre,'E2_DECIDE_PROVENANCE':codec._wire(action.source),'SOURCE_PATH':action.source.path,'CONTENT_IDENTITY':codec._wire(action.source.identity),'SCOPE':snapshot.context.scope,'LINEAGE':snapshot.context.lineage,'GENERATION':snapshot.context.generation,'SNAPSHOT_FIELDS_CHANGE_AUTHORIZED':False,'EXPECTED_ID_IS_INPUT_COMMITMENT_NOT_FULL_OUTPUT_ORACLE':True})
if target.exists():
 assert not target.is_symlink() and target.read_bytes()==raw,'EXISTING_TARGET_CONFLICT'
 created=False
else:
 with target.open('xb') as stream:stream.write(raw)
 created=True
actual=target.read_bytes();assert len(actual)==90 and actual==raw and sha(actual)==subject['EXPECTED_RAW_IDENTITY']['sha256']
p=model.ArtifactPin(action.source.path,action.source.identity,model.HashProfile.RAW);codec.validate_pin(p);model.validate_provenance(action.source);assert codec.load_pinned(root,p)==raw
value=codec.parse_json(actual);assert value=={'action':'E2-DECIDE','lineage':snapshot.context.lineage,'scope':snapshot.context.scope}
required={}
for prov in replay.provenance_records(snapshot):
 np=model.ArtifactPin(prov.path,prov.identity,model.HashProfile.RAW);codec.validate_pin(np);codec._path(root,np.path);key=(np.path,np.pointer,np.profile);assert key not in required or required[key]==np;required[key]=np
model.unique(tuple(required.values()),lambda np:(np.path,np.pointer,np.profile))
post=codec._wire(codec.snapshot_id(snapshot));assert pre==post and snapshotpath.read_bytes()==beforebytes
save('accepted-source-validation.json',{'SOURCE_ARTIFACT':pin(target),'SOURCE_ROOT':str(root),'SOURCE_RELATIVE_PATH':action.source.path,'CREATED_THIS_PACKAGE':created,'EXPECTED_BYTE_LENGTH':90,'ACTUAL_BYTE_LENGTH':len(actual),'RECOVERED_SOURCE':candidatepin,'AUTHORITATIVE_EMBEDDED_SOURCE':embeddedpin,'EXPECTED_SHA256':subject['EXPECTED_RAW_IDENTITY']['sha256'],'ACTUAL_SHA256':sha(actual),'BYTE_EQUALITY':'PASS','CONTENT_IDENTITY':codec._wire(action.source.identity),'NATIVE_SOURCE_PIN':codec._wire(p),'NATIVE_DECODE':'PASS_PLAIN_JSON_SOURCE_ENVELOPE','NATIVE_PROVENANCE_VALIDATION':'PASS','RAW_PIN_KEY_UNIQUENESS':'PASS','NO_ALIAS':'PASS_CANONICAL_EXACT_ROOT_PATH_NON_SYMLINK','SCOPE_LINEAGE':'PASS_SOURCE_JSON_AND_SNAPSHOT_CONTEXT_MATCH','SOURCE_PATH_CHANGED':'NO','PROVENANCE_IDENTITY_CHANGED':'NO','CONTENT_IDENTITY_CHANGED':'NO','AUTHORITY_CHANGED':'NO','SCHEMA_CHANGED':'NO','SNAPSHOT_FIELDS_CHANGED':'NO','PRE_MATERIALIZATION_SNAPSHOT_ID':pre,'POST_MATERIALIZATION_SNAPSHOT_ID':post,'SNAPSHOT_IDENTITY_UNCHANGED':True,'NO_BYTES_RESERIALIZED':True,'HISTORICAL_PHYSICAL_SOURCE_RETENTION_CLAIMED':False,'NEW_PHYSICAL_SOURCE_IS_IDENTICAL_PROSPECTIVE_EXTRACTION':True})
# Stop at the first remaining native lookup failure; do not inspect/repair its bytes.
lookups=[];nextblock=None
for np in required.values():
 try:codec.load_pinned(root,np);lookups.append({'PIN':codec._wire(np),'STATUS':'PASS'})
 except model.PlannerError as exc:
  nextblock={'PIN':codec._wire(np),'STATUS':'BLOCKED','ERROR':str(exc),'ROOT':str(root),'SCOPE':'OUTSIDE_CURRENT_E2_DECIDE_AUTHORIZATION'};lookups.append(nextblock);break
assert nextblock and nextblock['PIN']['path']=='source.json'
save('static-a14-handoff-frontier.json',{'SOURCE_PREFLIGHT':'E2_DECIDE_NATIVE_RAW_LOOKUP_PASS; FIRST_REMAINING_SOURCE_BLOCKED','LOOKUPS_THROUGH_FIRST_BLOCKER':lookups,'NEXT_A14_BLOCKER':nextblock,'BUNDLE_PREFLIGHT':'NOT_RUN_COMPLETE_SOURCE_POLICY_HISTORY_INPUTS_STILL_MISSING','SAVE_PREFLIGHT':'STATIC_CONTRACT_ONLY; no bundle bytes or save identity invented','WRITER_TERMINATION_PREFLIGHT':'REQUIRED_FUTURE_PROCESS_BARRIER; not executed','COLD_READER_PREFLIGHT':'STATIC_CONTRACT_ONLY; complete saved artifact/operands still unavailable','A14_DEPENDENT_UNRESOLVED_REFERENCE_COUNT':16,'PREVIOUSLY_RESOLVED':52,'RESOLVED_BY_E2_DECIDE_MATERIALIZATION':0,'TOTAL_RESOLVED':52,'TOTAL_UNRESOLVED':59,'REASON_NO_OPERAND_PROMOTED':'No remaining missing reference was blocked solely by this source; native Bundle, saved identity, reader baseline and mutation/invalidation boundary still require independent missing sources/policy/history','INVOCATION_STATIC_PREFLIGHT':'NOT_RUN','NEXT_BLOCKER_REPAIRED':False,'CURRENT_AUTHORIZATION_REUSED_FOR_NEXT_BLOCKER':False})
print(json.dumps({'SCOPE_AUTHENTICATION':'PASS','SOURCE':str(target),'BYTES':len(actual),'SHA256':sha(actual),'SNAPSHOT_UNCHANGED':pre==post,'NEXT_BLOCKER':nextblock['PIN']['path'],'COUNTS':'52/59'}))
