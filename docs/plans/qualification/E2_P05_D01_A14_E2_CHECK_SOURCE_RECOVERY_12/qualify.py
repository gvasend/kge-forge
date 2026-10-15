"""Static source recovery and informational physical-source frontier."""
import hashlib,json
from pathlib import Path
from adapter.planner import codec,model,replay
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;Q=O.parent
OPTION='AUTHORIZE_BOUNDED_A14_E2_CHECK_LOSSLESS_SOURCE_MATERIALIZATION'
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def save(n,v):(O/n).write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
def pin(p,ptr=''):return {'path':str(p.relative_to(R)),'pointer':ptr,'raw_sha256':sha(p.read_bytes())}
c=read(O/'source-contract.json');lc=read(O/'lossless-candidate.json');raw=(R/lc['ARTIFACT']['path']).read_bytes();assert sha(raw)==c['EXPECTED_BYTE_HASH']==lc['CONTENT_IDENTITY']['sha256'];assert raw==c['PROVENANCE']['excerpt'].encode()
assert codec.parse_json(raw)=={'action':'E2-CHECK','lineage':c['LINEAGE'],'scope':c['SCOPE']}
assert codec.canonical_bytes(codec.parse_json(raw))==raw
sp=Q/'E2_P05_D01_A14_PROVENANCE_FIXTURE_CORRECTION_7/corrected-prospective-snapshot.json';snapshot=codec.decode_snapshot(sp.read_bytes());model.validate_model(snapshot);sid=codec._wire(codec.snapshot_id(snapshot));assert sid['sha256']=='7ec95347f9662731ad5254221c03196fe789eb3435d02947eb09a70077ab66b9'
refs=[]
def walk(v,ptr=''):
 if isinstance(v,dict):
  if v.get('$type')=='Provenance' and v.get('path')=='E2-CHECK.json':refs.append({'POINTER':ptr,'PROVENANCE':v})
  for k,x in v.items():walk(x,ptr+'/'+k.replace('~','~0').replace('/','~1'))
 elif isinstance(v,list):
  for i,x in enumerate(v):walk(x,ptr+'/'+str(i))
walk(read(sp));assert len(refs)==3 and all(r['PROVENANCE']==c['PROVENANCE'] for r in refs)
codec._path(R,'E2-CHECK.json');assert not (R/'E2-CHECK.json').exists()
provenance=codec._unwire(c['PROVENANCE']);model.validate_provenance(provenance)
candidatepin=model.ArtifactPin(lc['ARTIFACT']['path'],provenance.identity,model.HashProfile.RAW);codec.validate_pin(candidatepin);assert codec.load_pinned(R,candidatepin)==raw
save('source-validation.json',{'STATUS':'PASS','BYTE_LENGTH':len(raw),'SHA256':sha(raw),'CONTENT_IDENTITY':codec._wire(provenance.identity),'NATIVE_SOURCE_DECODE':'PASS_PLAIN_JSON_MARKER','SCHEMA':'EXACT_THREE_STRING_FIELDS_ACTION_LINEAGE_SCOPE','RAW_PIN':'PASS_ISOLATED_EVIDENCE_PATH','PROVENANCE':'PASS_UNCHANGED_THREE_OCCURRENCES','CANONICAL_EXPECTED_PATH':'PASS','EXPECTED_PATH':'E2-CHECK.json','MATERIALIZATION_REQUIRES_REPIN':False,'PROVENANCE_FIELDS_CHANGED':0,'EXPECTED_SNAPSHOT_ID_BEFORE':sid,'EXPECTED_SNAPSHOT_ID_AFTER':sid,'E2_CHECK_MATERIALIZED':False})
exact=read(O/'exact-file-search.json')['EXACT_FILE_BYTES_HITS'];embedded=read(O/'embedded-source-search.json')['LOSSLESS_UTF8_STRING_HITS'];rows=[]
for i,e in enumerate(exact):
 b=(R/e['path']).read_bytes();assert b==raw;rows.append({'CANDIDATE_ID':'CHECK-FILE-'+str(i+1).zfill(4),'SOURCE':e,'POINTER':e['pointer'],'RECOVERY_METHOD':'EXACT_RETAINED_WHOLE_FILE','BYTE_LENGTH':len(b),'SHA256':sha(b),'CONTENT_IDENTITY':c['EXPECTED_CONTENT_IDENTITY'],'LOSSLESS':'YES'})
for i,e in enumerate(embedded):rows.append({'CANDIDATE_ID':'CHECK-EMBED-'+str(i+1).zfill(4),'SOURCE':e['source'],'POINTER':e['source']['pointer'],'RECOVERY_METHOD':'RAW_DECODE_UTF8_JSON_STRING','BYTE_LENGTH':e['byte_count'],'SHA256':e['sha256'],'CONTENT_IDENTITY':c['EXPECTED_CONTENT_IDENTITY'],'LOSSLESS':'YES','WRITER_AUTHORITY':'PC01 _source raw.decode() verified; strongest independent direct evidence is corrected A14 provenance excerpt'})
save('candidate-inventory.json',{'COUNT':len(rows),'ROWS':rows,'EXACT_BYTE_EQUIVALENCE_CLASSES':1,'SEMANTIC_REPORTS_NOT_PROMOTED':True})
subject={'QUALIFICATION_TYPE':'BOUNDED_A14_E2_CHECK_LOSSLESS_SOURCE_MATERIALIZATION','BASE_SNAPSHOT_SOURCE':pin(sp),'BASE_SNAPSHOT_ID':sid,'EXPECTED_POST_MATERIALIZATION_SNAPSHOT_ID':sid,'AUTHORITATIVE_BYTE_SOURCE':c['PRIMARY_BYTE_SOURCE'],'RETAINED_EXACT_SOURCES':exact,'ISOLATED_CANDIDATE':lc['ARTIFACT'],'RAW_BYTES_UTF8':raw.decode(),'EXPECTED_LENGTH':len(raw),'EXPECTED_SHA256':sha(raw),'EXPECTED_CONTENT_IDENTITY':c['EXPECTED_CONTENT_IDENTITY'],'EXISTING_PROVENANCE':refs,'EXACT_ROOT':str(R),'EXISTING_RELATIVE_PATH':'E2-CHECK.json','NO_REPIN':True,'SNAPSHOT_FIELDS_CHANGED':False,'EXPECTED_SNAPSHOT_EFFECT':'UNCHANGED','SELECTED':False,'SCOPE_EXCLUSIONS':['No materialization in Recovery12','No later source materialization/recovery or bundled authority','No source/path/provenance/content/authority/schema/Snapshot change','No root/policy/history/bundle/save/reader repair','No INSTALL, A14/D01/P05/P06 execution, output oracle or END binding'],'HISTORICAL_CLAIM':'Original raw byte value survives in authoritative Provenance.excerpt; isolated extraction is not proof of physical original temporary-file retention'}
subject['SUBJECT_IDENTITY']='qualification-A14-E2CHECK-materialization-v1:'+sha(canon(subject));save('bounded-materialization-subject.json',subject)
save('bounded-source-decision-dossier.json',{'DECISION_REQUIRED':True,'DECISION_READY':True,'OPTION':OPTION,'ALTERNATIVE':'DECLINE_E2_CHECK_MATERIALIZATION','SUBJECT_IDENTITY':subject['SUBJECT_IDENTITY'],'EXACT_SUBJECT':pin(O/'bounded-materialization-subject.json'),'SELECTION':'NOT_SELECTED','REASON':'Current user explicitly excludes E2-CHECK from all previously selected scopes; lossless byte recovery does not authorize accepted physical integration','MATERIALIZATION_REQUIRES_REPIN':False,'EXPECTED_SNAPSHOT_EFFECT':'UNCHANGED'})
# Native provenance enumeration owns lookup order. Retain each unique RAW pin once.
required={};roles={}
for p in replay.provenance_records(snapshot):
 n=model.ArtifactPin(p.path,p.identity,model.HashProfile.RAW);codec.validate_pin(n);codec._path(R,n.path);key=(n.path,n.pointer,n.profile);assert key not in required or required[key]==n;required[key]=n
for a in snapshot.actions:roles.setdefault(a.source.path,[]).append('Action.source:'+a.id.value)
for k in snapshot.knowledge:roles.setdefault(k.provenance.path,[]).append('Snapshot KnowledgeRecord:'+k.id.value)
for a in snapshot.actions:
 for k in a.accepted_inventory:roles.setdefault(k.provenance.path,[]).append('accepted_inventory KnowledgeRecord:'+k.id.value)
front=[]
for i,n in enumerate(required.values()):
 try:codec.load_pinned(R,n);present=True
 except model.PlannerError:present=False
 front.append({'SOURCE_PATH':n.path,'EXPECTED_IDENTITY':codec._wire(n.identity),'EXPECTED_HASH':n.identity.sha256,'PRESENT':'YES' if present else 'NO','FIRST_LOOKUP_ORDER':i+1,'ROLE':roles.get(n.path,['native provenance source; no later-source semantic recovery performed'])})
missing=[r['SOURCE_PATH'] for r in front if r['PRESENT']=='NO'];assert missing and missing[0]=='E2-CHECK.json'
save('a14-source-frontier.json',{'TOTAL_A14_PHYSICAL_SOURCE_PINS':len(front),'PRESENT_SOURCE_COUNT':sum(r['PRESENT']=='YES' for r in front),'MISSING_SOURCE_COUNT':len(missing),'MISSING_SOURCE_ORDER':missing,'ROWS':front,'INFORMATIONAL_ONLY':True,'LATER_SOURCE_BYTES_RECOVERED':False,'LATER_SOURCE_DOSSIERS_CREATED':False,'FIRST_BLOCKER_UNCHANGED':'E2-CHECK.json','ORDERING':'First occurrence in native replay.provenance_records; repeated identical RAW pins deduplicated, not sorted for semantic traversal'})
impact=read(Q/'E2_P05_D01_A14_SOURCE_JSON_RECOVERY_10/operand-impact-and-frontier.json')
save('operand-impact.json',{'E2_CHECK_DEPENDENT_REFERENCES':16,'ROWS':[{**r,'E2_CHECK_DEPENDENCY':'Mandatory provenance source for complete corrected A14 Snapshot bundle/source closure','STATUS':'UNRESOLVED_NO_PROMOTION'} for r in impact['ROWS']],'RESOLVED_OPERANDS':52,'UNRESOLVED_OPERANDS':59,'RESOLVED_BY_RECOVERY':0,'INVOCATION_STATIC_PREFLIGHT':'NOT_RUN','NEXT_BLOCKER':'E2_CHECK_MATERIALIZATION_AUTHORIZATION'})
assert not (R/'E2-CHECK.json').exists()
print(json.dumps({'RECOVERY_CLASSIFICATION':c['RECOVERY_CLASSIFICATION'],'BYTE_LENGTH':len(raw),'SHA256':sha(raw),'FRONTIER_TOTAL':len(front),'PRESENT':len(front)-len(missing),'MISSING_ORDER':missing,'DECISION_READY':True}))
