"""Read-only repository exact-file and lossless embedded-byte search."""
import base64,hashlib,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification';C7=Q/'E2_P05_D01_A14_PROVENANCE_FIXTURE_CORRECTION_7'
def read(p):return json.loads(p.read_bytes())
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p,ptr=''):
 p=Path(p);return {'path':str(p.relative_to(R)),'pointer':ptr,'raw_sha256':sha(p.read_bytes())}
def save(n,v):(O/n).write_bytes(canon(v)+b'\n')
source=C7/'corrected-prospective-snapshot.json';snapshot=read(source)['snapshot'];action=next(a for a in snapshot['actions'] if a['id']['value']=='E2-DECIDE');prov=action['source'];expected=prov['identity'];embedded=prov['excerpt'].encode('utf-8');assert sha(embedded)==expected['sha256'];size=len(embedded)
files=subprocess.run(['rg','--files','-uu'],cwd=str(R),capture_output=True,text=True,check=True).stdout.splitlines();files=[R/f for f in files if '.git' not in Path(f).parts and O not in (R/f).parents]
exact=[];refs=[];encoded=[];embeddedhits=[];filename=[];manifest=[];errors=[]
texttypes={'.json','.jsonl','.md','.py','.log','.txt','.yaml','.yml','.toml'}
for p in sorted(files):
 if not p.is_file() or p.is_symlink():continue
 stat=p.stat();entry={'path':str(p.relative_to(R)),'size':stat.st_size};manifest.append(entry)
 if p.name=='E2-DECIDE.json':filename.append(entry)
 if stat.st_size==size:
  raw=p.read_bytes()
  if sha(raw)==expected['sha256']:exact.append(pin(p))
 if p.suffix not in texttypes:continue
 raw=p.read_bytes()
 needles=[b'E2-DECIDE.json',expected['sha256'].encode(),base64.b64encode(embedded),embedded]
 if not any(n in raw for n in needles):continue
 ppin=pin(p);refs.append({**ppin,'literal_path_present':needles[0] in raw,'expected_hash_present':needles[1] in raw,'raw_byte_substring_present':needles[3] in raw})
 if needles[2] in raw:encoded.append({'container':ppin,'encoding':'base64 literal','value':needles[2].decode(),'status':'CANDIDATE_REQUIRES_AUTHORITY_ENCODING_METADATA'})
 if p.suffix not in {'.json','.jsonl'}:continue
 try:obj=json.loads(raw)
 except (ValueError,UnicodeDecodeError) as exc:errors.append({'path':str(p.relative_to(R)),'error':str(exc)});continue
 def walk(v,ptr=''):
  if isinstance(v,dict):
   if v.get('$type')=='Provenance' and v.get('path')=='E2-DECIDE.json':
    refs.append({'source':{**ppin,'pointer':ptr},'EXPECTED_IDENTITY':v.get('identity'),'SEMANTIC_PROVENANCE':v})
   for k,x in v.items():walk(x,ptr+'/'+k.replace('~','~0').replace('/','~1'))
  elif isinstance(v,list):
   for i,x in enumerate(v):walk(x,ptr+'/'+str(i))
  elif isinstance(v,str) and len(v.encode('utf-8'))==size and sha(v.encode('utf-8'))==expected['sha256']:
   embeddedhits.append({'source':{**ppin,'pointer':ptr},'representation':'JSON string decoded losslessly as UTF-8','byte_count':size,'sha256':sha(v.encode('utf-8')),'BYTE_PRESERVING':True})
 walk(obj)
assert embeddedhits
save('file-search-manifest.json',{'SCOPE':'All rg --files -uu repository files except .git internals, symlinks and this new package; exact-size hash test considers every extension. Embedded textual search uses listed source/document extensions.','FILES':manifest,'FILE_COUNT':len(manifest),'TEXT_TYPES':sorted(texttypes),'ERRORS':errors})
save('exact-file-search.json',{'EXPECTED_FILENAME':'E2-DECIDE.json','EXPECTED_HASH':expected['sha256'],'EXPECTED_BYTE_COUNT':size,'FILENAME_HITS':filename,'EXACT_FILE_BYTES_HITS':exact,'RESULT':'EXACT_SOURCE_RETAINED' if exact else 'NO_EXACT_PHYSICAL_SOURCE_FILE_IN_RETAINED_CORPUS'})
save('retained-references.json',refs)
save('embedded-source-search.json',{'LOSSLESS_UTF8_STRING_HITS':embeddedhits,'BASE64_CANDIDATES':encoded,'PRIMARY_SOURCE':pin(source,'/snapshot/actions/'+str(snapshot['actions'].index(action))+'/source/excerpt'),'BYTE_COUNT':size,'HASH':expected['sha256'],'QUALIFIED_ENCODING_RULE':'PC01 _source stores raw.decode() into Provenance.excerpt; JSON container decoding recovers the exact original UTF-8 raw bytes, not a semantically regenerated object'})
writer=R/'docs/plans/DETERMINISTIC_PLANNER_V0_1_E2_PC01_WHOLE_MODEL_ORACLE.py';codec=R/'adapter/planner/codec.py';assert 'raw = c.canonical_bytes(body)' in writer.read_text() and 'raw.decode()' in writer.read_text()
contract={'SOURCE_ROLE':'E2-DECIDE Action definition provenance/source envelope; scoped authored definition marker, not complete native Action, decision input, RecordedDecision, choice, grant or policy','EXPECTED_NATIVE_TYPE':'Plain JSON source envelope with exactly action,lineage,scope; Action.source is native Provenance referencing RAW bytes','CONSUMER':'Native Action.source; PersistenceBundle provenance/source-index validation and codec.load_pinned RAW lookup','PROVENANCE':prov,'EXPECTED_PATH':'E2-DECIDE.json','EXPECTED_CONTENT_IDENTITY':expected,'EXPECTED_BYTE_HASH':expected['sha256'],'EXPECTED_BYTE_COUNT':size,'SCOPE':snapshot['context']['scope'],'LINEAGE':snapshot['context']['lineage'],'GENERATION':snapshot['context']['generation'],'BYTE_ASSURANCE':'Exact entire physical RAW bytes under raw-file-sha256; semantic JSON equivalence is insufficient','PRIMARY_BYTE_SOURCE':pin(source,'/snapshot/actions/'+str(snapshot['actions'].index(action))+'/source/excerpt'),'CANONICAL_SERIALIZER':{'WRITER':pin(writer),'FUNCTION':'_source(root,name,body)','CALL':'_source(root,name + ".json", {"action":name,"scope":SCOPE,"lineage":LINEAGE}) where name=E2-DECIDE','SERIALIZER':pin(codec),'FUNCTION_NAME':'canonical_bytes','SCHEMA_FIELDS':['action','lineage','scope'],'ORDERING':'sort_keys=True; action,lineage,scope','WHITESPACE':'separators=(comma,colon); no spaces','ENCODING':'UTF-8','NEWLINE':'none; write_bytes(raw)','ESCAPING':'ensure_ascii=False, JSON escaping','NUMBER_RULE':'Source has strings only; native canonical serializer accepts constrained typed JSON and allow_nan=False'},'RECOVERY_CLASSIFICATION':'EXACT_SOURCE_RETAINED' if exact else 'LOSSLESS_EMBEDDED_SOURCE','LOSSLESS_BYTE_RECOVERY':True,'CANONICAL_BYTE_RECONSTRUCTION_ALSO_SUPPORTED':True,'HISTORICAL_PHYSICAL_SOURCE_RETAINED':bool(exact),'HISTORICAL_RAW_BYTE_CONTENT_RETAINED':True,'PROSPECTIVE_EXTRACTION':'Exact retained raw.decode() byte-value copied from container; not regeneration from Action semantic fields'}
save('source-contract.json',contract)
# Candidate in isolated evidence workspace only; not an accepted source or Snapshot edit.
candidate=O/'candidates/E2-DECIDE.json';candidate.parent.mkdir(exist_ok=True);candidate.write_bytes(embedded);assert sha(candidate.read_bytes())==expected['sha256']
save('lossless-candidate.json',{'ARTIFACT':pin(candidate),'SOURCE':contract['PRIMARY_BYTE_SOURCE'],'BYTE_COUNT':size,'BYTE_HASH':sha(embedded),'CONTENT_IDENTITY':expected,'CLASSIFICATION':contract['RECOVERY_CLASSIFICATION'],'ACCEPTED_FIXTURE_SOURCE':False,'ORIGINAL_CORRECTED_SNAPSHOT_EDITED':False})
print(json.dumps({'EXACT_FILE_HITS':len(exact),'LOSSLESS_EMBEDDED_HITS':len(embeddedhits),'REFERENCE_ENTRIES':len(refs),'FILE_COUNT':len(manifest),'BYTE_COUNT':size,'HASH':expected['sha256'],'CLASSIFICATION':contract['RECOVERY_CLASSIFICATION']}))
