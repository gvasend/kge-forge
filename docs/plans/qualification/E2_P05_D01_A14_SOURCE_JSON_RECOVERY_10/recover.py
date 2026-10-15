"""Exact retained source.json recovery. No accepted source.json is created."""
import base64,hashlib,json,subprocess
from pathlib import Path
from adapter.planner import codec,model
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification';C7=Q/'E2_P05_D01_A14_PROVENANCE_FIXTURE_CORRECTION_7';C9=Q/'E2_P05_D01_A14_E2_DECIDE_MATERIALIZATION_9'
def read(p):return json.loads(Path(p).read_bytes())
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p,ptr=''):
 p=Path(p);return {'path':str(p.relative_to(R)),'pointer':ptr,'raw_sha256':sha(p.read_bytes())}
def save(n,v):(O/n).write_bytes(canon(v)+b'\n')
snapshotfile=C7/'corrected-prospective-snapshot.json';s=read(snapshotfile)['snapshot'];required=[]
def find(v,ptr=''):
 if isinstance(v,dict):
  if v.get('$type')=='Provenance' and v.get('path')=='source.json':required.append({'POINTER':'/snapshot'+ptr,'PROVENANCE':v})
  for k,x in v.items():find(x,ptr+'/'+k)
 elif isinstance(v,list):
  for i,x in enumerate(v):find(x,ptr+'/'+str(i))
find(s);assert len(required)==5 and len({canon(r['PROVENANCE']['identity']) for r in required})==1
prov=required[0]['PROVENANCE'];identity=prov['identity'];raw=prov['excerpt'].encode('utf-8');assert sha(raw)==identity['sha256'];assert len(raw)==617
files=subprocess.run(['rg','--files','-uu'],cwd=str(R),capture_output=True,text=True,check=True).stdout.splitlines();files=[R/p for p in files if '.git' not in Path(p).parts and O not in (R/p).parents]
standalone=[];filename=[];embedded=[];references=[];encoded=[];manifest=[];parse_errors=[]
texttypes={'.json','.jsonl','.md','.py','.log','.txt','.yml','.yaml','.toml'}
for p in sorted(files):
 if not p.is_file() or p.is_symlink():continue
 size=p.stat().st_size;manifest.append({'path':str(p.relative_to(R)),'size':size})
 if p.name=='source.json':filename.append({'source':pin(p),'byte_length':size,'matches_expected':sha(p.read_bytes())==identity['sha256']})
 if size==len(raw) and sha(p.read_bytes())==identity['sha256']:standalone.append({'source':pin(p),'byte_length':size,'sha256':identity['sha256'],'LOSSLESS':True})
 if p.suffix not in texttypes:continue
 b=p.read_bytes()
 if not any(n in b for n in [b'source.json',identity['sha256'].encode(),base64.b64encode(raw),raw]):continue
 references.append({'source':pin(p),'path_mentioned':b'source.json' in b,'expected_hash_mentioned':identity['sha256'].encode() in b})
 if base64.b64encode(raw) in b:encoded.append({'source':pin(p),'encoding':'base64 literal','status':'not promoted without source/encoding authority'})
 if p.suffix not in {'.json','.jsonl'}:continue
 try:value=json.loads(b)
 except (ValueError,UnicodeDecodeError) as exc:parse_errors.append({'path':str(p.relative_to(R)),'error':str(exc)});continue
 def walk(v,ptr=''):
  if isinstance(v,dict):
   if v.get('$type')=='Provenance' and v.get('path')=='source.json':references.append({'source':pin(p,ptr),'PROVENANCE':v,'IDENTITY_MATCHES_A14':v.get('identity')==identity})
   for k,x in v.items():walk(x,ptr+'/'+k.replace('~','~0').replace('/','~1'))
  elif isinstance(v,list):
   for i,x in enumerate(v):walk(x,ptr+'/'+str(i))
  elif isinstance(v,str) and len(v.encode())==len(raw) and sha(v.encode())==identity['sha256']:embedded.append({'source':pin(p,ptr),'RECOVERY_METHOD':'lossless JSON string -> UTF-8 bytes','BYTE_LENGTH':len(raw),'SHA256':sha(v.encode()),'CONTENT_IDENTITY':identity,'LOSSLESS':True})
 walk(value)
assert standalone
save('search-manifest.json',{'FILE_COUNT':len(manifest),'FILES':manifest,'SCOPE':'rg --files -uu repository except .git, symlinks and new package. All extensions exact-size hashed; listed source/document text extensions walked for paths/hash/embedded raw/base64.','TEXT_EXTENSIONS':sorted(texttypes),'JSON_PARSE_ERRORS':parse_errors})
save('standalone-search.json',{'FILENAME_CANDIDATES':filename,'EXACT_RETAINED_MATCHES':standalone,'BYTE_DISTINCT_SAME_FILENAME_CANDIDATES_NOT_COLLAPSED':True,'PRIMARY_CLASSIFICATION':'EXACT_SOURCE_RETAINED','ACCEPTED_EXPECTED_ROOT_FILE_EXISTS':(R/'source.json').exists()})
save('embedded-search.json',{'MATCHES':embedded,'ENCODED_CANDIDATES':encoded,'PRIMARY_A14_LITERAL_EXCERPT':pin(snapshotfile,required[0]['POINTER']+'/excerpt')})
save('retained-references.json',references)
# Pin original writer semantics without executing the probe or fixture factories.
writer=R/'docs/plans/DETERMINISTIC_PLANNER_V0_1_EXTERNAL_UNKNOWN_RULE_RECONCILIATION_1_VALIDATION.json';probe=read(writer)['probe_program'];assert "raw=json.dumps(contract,sort_keys=True,separators=(',',':')).encode()" in probe and 'raw.decode()' in probe and 'path.write_bytes(raw)' in probe
bridge=R/'adapter/tests/test_planner_external_unknown.py';bridgecode=bridge.read_text();assert "program.replace('/tmp/unknown-rule-source.json', self.temp.name+'/source.json')" in bridgecode and "path='source.json'" in bridgecode
whole=R/'docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_PC01_WHOLE_MODEL_ORACLE.py';assert 'raw.decode()' in whole.read_text()
value=codec.parse_json(raw);assert value['schema']=='SYNTHETIC-GOVERNED-RULE-ACQUISITION-1' and value['qualification_only'] is True;assert json.dumps(value,sort_keys=True,separators=(',',':')).encode()==raw
contract={'SOURCE_ROLE':'Shared synthetic governed-rule acquisition qualification premise supporting the held mapping/acquisition Action, external-rule requirement/gate, external-evidence control boundary and goal. Not positive rule Evidence, receipt, decision input, choice/grant, policy or the independent resolution.json route contract.','EXPECTED_NATIVE_TYPE':'Plain source JSON with schema SYNTHETIC-GOVERNED-RULE-ACQUISITION-1; consumed through native Provenance/RAW ArtifactPin, not decoded as native Evidence/ExternalResolutionContract','CONSUMERS':required,'EXPECTED_PATH':'source.json','EXPECTED_CONTENT_IDENTITY':identity,'EXPECTED_HASH':identity['sha256'],'EXPECTED_SIZE':len(raw),'PROVENANCE_ROLE':'SYNTHETIC_CONTRACT shared source; repeated identical provenance uses deduplicate to one RAW key','SCOPE':s['context']['scope'],'LINEAGE':s['context']['lineage'],'GENERATION':s['context']['generation'],'PAYLOAD_SCOPE':value['scope'],'PAYLOAD_LINEAGE':value['lineage'],'PAYLOAD_TEST_IDENTIFIERS':'Original TEST-* template strings are byte-identity-bearing. PC01 renames native model context/Identifier objects; it does not authorize changing raw contract payload text.','BYTE_REQUIREMENT':'Exact entire raw bytes required by CONTENT_IDENTITY/raw-file-sha256; semantic JSON equality insufficient','WRITER_SOURCE':pin(writer,'/probe_program'),'WRITER_SEMANTICS':'Original probe writes raw compact sorted JSON bytes and stores raw.decode() into Provenance.excerpt; external-unknown fixture redirects original temporary file name to source.json and relocates native path; PC01 _rename preserves excerpt bytes while renaming native metadata/context.','ADAPTER_SOURCE':pin(bridge),'WHOLE_MODEL_ADAPTER_SOURCE':pin(whole),'CANONICAL_SERIALIZATION':{'SCHEMA':value['schema'],'FIELD_SET':sorted(value),'FIELD_ORDER':'sorted Unicode keys','WHITESPACE':'compact comma/colon separators; no spaces outside strings','ENCODING':'Python default UTF-8 via encode(); payload ASCII','ESCAPING':'json.dumps default ensure_ascii=True; ordinary JSON string escapes','NEWLINE':'none; write_bytes(raw)','VALUES':'strings, booleans and reentry string array; no numeric ambiguity'},'RECOVERY_CLASSIFICATION':'EXACT_SOURCE_RETAINED','LOSSLESS_BYTE_RECOVERY':True,'HISTORICAL_RAW_SOURCE_BYTES_RETAINED_IN_QUALIFICATION_CORPUS':True,'ORIGINAL_TEMPORARY_FILE_RETENTION_NOT_PROVEN':True,'NO_PAYLOAD_TEST_SCOPE_REWRITING':True,'MATERIALIZATION_REQUIRES_REPIN':False,'SOURCE_ROOT':str(R)}
save('source-contract.json',contract)
candidates=[]
for i,e in enumerate(standalone):candidates.append({'CANDIDATE_ID':'SOURCEJSON-FILE-'+str(i+1).zfill(4),'SOURCE':e['source'],'POINTER':'','RECOVERY_METHOD':'exact retained whole-file bytes','BYTE_LENGTH':e['byte_length'],'SHA256':e['sha256'],'CONTENT_IDENTITY':identity,'LOSSLESS':'YES'})
for i,e in enumerate(embedded):candidates.append({'CANDIDATE_ID':'SOURCEJSON-EMBED-'+str(i+1).zfill(4),'SOURCE':e['source'],'POINTER':e['source']['pointer'],'RECOVERY_METHOD':e['RECOVERY_METHOD'],'BYTE_LENGTH':e['BYTE_LENGTH'],'SHA256':e['SHA256'],'CONTENT_IDENTITY':identity,'LOSSLESS':'YES'})
save('candidate-inventory.json',{'ROWS':candidates,'COUNT':len(candidates),'EXACT_BYTE_EQUIVALENCE_CLASSES':1,'NO_MULTIPLE_DISTINCT_BYTES_MATCH_REQUIRED_COMPLETE_RAW_PIN':True,'SAME_FILENAME_WITH_OTHER_HASH_NOT_SELECTED':filename})
# Read any exact content-equivalent retained file deterministically; location is evidence, not substituted fixture path.
sourcepath=R/standalone[0]['source']['path'];retained=sourcepath.read_bytes();assert retained==raw
candidate=O/'candidates/recovered-source-bytes.bin';candidate.parent.mkdir(exist_ok=True);candidate.write_bytes(retained) # not named source.json, not accepted source
p=model.ArtifactPin(str(candidate.relative_to(R)),codec._unwire(identity),model.HashProfile.RAW);codec.validate_pin(p);assert codec.load_pinned(R,p)==retained
native=codec.decode_snapshot(snapshotfile.read_bytes());sid=codec._wire(codec.snapshot_id(native));assert sid==read(C7/'corrected-prospective-fixture.json')['CORRECTED_SNAPSHOT_ID']
save('source-validation.json',{'BYTE_HASH':'PASS','CONTENT_IDENTITY':'PASS','NATIVE_DECODE':'PASS_codec.parse_json plain source contract JSON','SCHEMA':'PASS_EXACT_AUTHORITATIVE_SCHEMA_AND_BYTE_PAYLOAD','SOURCE_PIN':'PASS_ISOLATED_EVIDENCE_PATH_NATIVE_RAW_LOOKUP','PROVENANCE':'PASS_ALL_FIVE_A14_REFERENCES_USE_SAME_EXACT_IDENTITY_AND_BYTES','EXPECTED_PATH_CANONICAL':'PASS_codec._path_checked_noacceptedfilecreated','EXPECTED_FIXTURE_PATH':'source.json','ACCEPTED_FIXTURE_SOURCE_CREATED':False,'RECOVERED_SOURCE':pin(candidate),'RETAINED_EXACT_SOURCE':standalone[0]['source'],'CONTENT_VALUE':value,'CORRECTED_SNAPSHOT_ID':sid,'EXPECTED_SNAPSHOT_EFFECT':'UNCHANGED if exact same bytes are supplied at existing source.json path; no native field/path/identity changes required'})
proposal={'QUALIFICATION_TYPE':'BOUNDED_A14_SOURCE_JSON_EXACT_RETAINED_SOURCE_MATERIALIZATION','BASE_SNAPSHOT_SOURCE':pin(snapshotfile),'BASE_SNAPSHOT_ID':sid,'AUTHORITATIVE_EXACT_BYTE_SOURCES':[r['source'] for r in standalone],'AUTHORITATIVE_A14_EMBEDDED_POINTER':pin(snapshotfile,required[0]['POINTER']+'/excerpt'),'ISOLATED_RECOVERED_CANDIDATE':pin(candidate),'EXPECTED_LENGTH':len(raw),'EXPECTED_SHA256':identity['sha256'],'EXPECTED_CONTENT_IDENTITY':identity,'RAW_BYTES_UTF8':raw.decode(),'EXISTING_PROVENANCE_REFERENCES':required,'EXISTING_RELATIVE_PATH':'source.json','EXACT_ROOT':str(R),'EXPECTED_SNAPSHOT_EFFECT':'UNCHANGED','PROVENANCE_FIELDS_CHANGED':0,'NO_REPIN':True,'SCOPE_EXCLUSIONS':['No TEST-to-E2 rewriting of the raw source payload','No change to native fields/authority/paths/identities','No other source/root/policy/history repair','No INSTALL/A14/D01/runtime save/cold-reader/oracle/END operation'],'HISTORICAL_CLAIMS':'Exact standalone bytes retained in qualification corpus; copying them to the expected A14 root is new physical materialization, not proof of original temporary-file retention or A14 execution','SELECTED':False}
proposal['SUBJECT_IDENTITY']='qualification-A14-sourcejson-materialization-v1:'+sha(canon(proposal));save('bounded-materialization-subject.json',proposal)
dossier={'DECISION_REQUIRED':True,'DECISION_READY':True,'OPTION':'AUTHORIZE_BOUNDED_A14_SOURCE_JSON_LOSSLESS_SOURCE_MATERIALIZATION','ALTERNATIVE':'DECLINE_SOURCE_JSON_MATERIALIZATION','EXACT_SUBJECT':pin(O/'bounded-materialization-subject.json'),'SUBJECT_IDENTITY':proposal['SUBJECT_IDENTITY'],'REASON':'Current task explicitly forbids creation of source.json; existing selected scopes cover only choice/grant and E2-DECIDE. Exact byte retention establishes recovery, not accepted integration authority.','SELECTION':'NOT_SELECTED','SOURCE_REPIN_REQUIRED':False,'EXPECTED_SNAPSHOT_CHANGE':False,'NATIVE_CAPABILITY_CHANGE_REQUIRED':False};save('bounded-source-decision-dossier.json',dossier)
deps=read(Q/'E2_P05_D01_A14_HANDOFF_CLOSURE_5/a14-dependency-inventory.json')
assert deps['A14_DEPENDENT_REFERENCES']==16
save('operand-impact-and-frontier.json',{'SOURCE_JSON_DEPENDENT_REFERENCES':16,'ROWS':[{**r,'SOURCE_JSON_DEPENDENCY':'Shared acquisition premise is mandatory for complete A14 source/bundle closure and native A14-derived baseline','STATUS':'UNRESOLVED; no operand promoted'} for r in deps['ROWS']],'RESOLVED_OPERANDS':52,'UNRESOLVED_OPERANDS':59,'SOURCE_JSON_MATERIALIZED':False,'MATERIALIZATION_REQUIRES_REPIN':False,'CORRECTED_SNAPSHOT_ID':sid,'EXPECTED_SNAPSHOT_EFFECT':'UNCHANGED','NEXT_BLOCKER':'SOURCE_JSON_MATERIALIZATION_AUTHORIZATION','LATER_SOURCE_LOOKUPS_NOT_PERFORMED':True,'BOUNDARY_NOTE':'16 normative A14-dependent rows; N02 existing later known-rule capsules remain a separate boundary issue, not an accepted source.json substitution'})
assert not (R/'source.json').exists()
print(json.dumps({'CLASSIFICATION':'EXACT_SOURCE_RETAINED','EXACT_FILES':len(standalone),'EMBEDDED':len(embedded),'BYTES':len(raw),'HASH':sha(raw),'DECISION_READY':True,'SOURCE_JSON_CREATED':False}))
