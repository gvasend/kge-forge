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
source=C7/'corrected-prospective-snapshot.json';snapshot=read(source)['snapshot'];route=snapshot['external_gates'][0]['resolution_contracts'][0];prov=route['provenance'];expected=prov['identity'];embedded=prov['excerpt'].encode('utf-8');assert sha(embedded)==expected['sha256'];size=len(embedded)
files=subprocess.run(['rg','--files','-uu'],cwd=str(R),capture_output=True,text=True,check=True).stdout.splitlines();files=[R/f for f in files if '.git' not in Path(f).parts and O not in (R/f).parents]
exact=[];refs=[];encoded=[];embeddedhits=[];filename=[];manifest=[];errors=[]
texttypes={'.json','.jsonl','.md','.py','.log','.txt','.yaml','.yml','.toml'}
for p in sorted(files):
 if not p.is_file() or p.is_symlink():continue
 stat=p.stat();entry={'path':str(p.relative_to(R)),'size':stat.st_size};manifest.append(entry)
 if p.name=='resolution.json':
  b=p.read_bytes();h=sha(b);filename.append({**entry,'sha256':h,'content_identity':{'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':'raw-file-sha256','sha256':h},'matches_A14_pin':h==expected['sha256']})
 if stat.st_size==size:
  raw=p.read_bytes()
  if sha(raw)==expected['sha256']:exact.append(pin(p))
 if p.suffix not in texttypes:continue
 raw=p.read_bytes()
 needles=[b'resolution.json',expected['sha256'].encode(),base64.b64encode(embedded),embedded,b'RESOLUTION']
 if not any(n in raw for n in needles):continue
 ppin=pin(p);refs.append({**ppin,'literal_path_present':needles[0] in raw,'expected_hash_present':needles[1] in raw,'raw_byte_substring_present':needles[3] in raw})
 if needles[2] in raw:encoded.append({'container':ppin,'encoding':'base64 literal','value':needles[2].decode(),'status':'CANDIDATE_REQUIRES_AUTHORITY_ENCODING_METADATA'})
 if p.suffix not in {'.json','.jsonl'}:continue
 try:obj=json.loads(raw)
 except (ValueError,UnicodeDecodeError) as exc:errors.append({'path':str(p.relative_to(R)),'error':str(exc)});continue
 def walk(v,ptr='',context=None):
  if isinstance(v,dict):
   if v.get('$type')=='Provenance' and v.get('path')=='resolution.json':
    refs.append({'source':{**ppin,'pointer':ptr},'EXPECTED_IDENTITY':v.get('identity'),'SEMANTIC_PROVENANCE':v})
   for k,x in v.items():walk(x,ptr+'/'+k.replace('~','~0').replace('/','~1'),context)
  elif isinstance(v,list):
   for i,x in enumerate(v):walk(x,ptr+'/'+str(i),context)
  elif isinstance(v,str) and len(v.encode('utf-8'))==size and sha(v.encode('utf-8'))==expected['sha256']:
   embeddedhits.append({'source':{**ppin,'pointer':ptr},'representation':'JSON string decoded losslessly as UTF-8','byte_count':size,'sha256':sha(v.encode('utf-8')),'BYTE_PRESERVING':True})
 walk(obj)
assert embeddedhits
save('file-search-manifest.json',{'SCOPE':'All rg --files -uu repository files except .git internals, symlinks and this new package; exact-size hash test considers every extension. Embedded textual search uses listed source/document extensions.','FILES':manifest,'FILE_COUNT':len(manifest),'TEXT_TYPES':sorted(texttypes),'ERRORS':errors})
save('exact-file-search.json',{'EXPECTED_FILENAME':'resolution.json','EXPECTED_HASH':expected['sha256'],'EXPECTED_BYTE_COUNT':size,'FILENAME_HITS':filename,'EXACT_FILE_BYTES_HITS':exact,'RESULT':'EXACT_SOURCE_RETAINED' if exact else 'NO_EXACT_PHYSICAL_SOURCE_FILE_IN_RETAINED_CORPUS'})
save('retained-references.json',refs)
save('embedded-source-search.json',{'LOSSLESS_UTF8_STRING_HITS':embeddedhits,'BASE64_CANDIDATES':encoded,'PRIMARY_SOURCE':pin(source,'/snapshot/external_gates/0/resolution_contracts/0/provenance/excerpt'),'BYTE_COUNT':size,'HASH':expected['sha256'],'QUALIFIED_ENCODING_RULE':'External-unknown source() stores raw.decode() into Provenance.excerpt; JSON container decoding recovers the exact original UTF-8 raw bytes, not a semantically regenerated object'})
writer=R/'adapter/tests/test_planner_external_unknown.py';codec=R/'adapter/planner/codec.py';assert 'raw = codec.canonical_bytes(body)' in writer.read_text() and 'raw.decode()' in writer.read_text()
contract={'SOURCE_ROLE':'Independent governed-external acquisition route source: EXTERNAL-RESOLUTION-CONTRACT-1 envelope binding request, gate/requirement, exact producer/target, source pins, receipt action and reentry/held Actions. This is a qualification premise, not a resolution result, support instance, Evidence, permission or decision choice.','EXPECTED_NATIVE_TYPE':'Plain JSON source envelope for existing native ExternalResolutionContract.provenance; contract body excludes $type and provenance','CONSUMER':'ExternalGate.resolution_contracts[0].provenance; native source-index/replay RAW lookup and external route correspondence','PROVENANCE':prov,'EXPECTED_PATH':'resolution.json','EXPECTED_CONTENT_IDENTITY':expected,'EXPECTED_BYTE_HASH':expected['sha256'],'EXPECTED_BYTE_COUNT':size,'SCOPE':snapshot['context']['scope'],'LINEAGE':snapshot['context']['lineage'],'GENERATION':snapshot['context']['generation'],'BYTE_ASSURANCE':'Complete physical RAW source bytes must match raw-file-sha256; semantic JSON equivalence insufficient','PRIMARY_BYTE_SOURCE':pin(source,'/snapshot/external_gates/0/resolution_contracts/0/provenance/excerpt'),'CANONICAL_SERIALIZER':{'WRITER':pin(writer),'FUNCTION':'source(path,body), used by attach(state,directory)','CALL':'source(resolution.json, {schema:EXTERNAL-RESOLUTION-CONTRACT-1,contract:wire(route) without $type/provenance})','SERIALIZER':pin(codec),'FUNCTION_NAME':'canonical_bytes','SCHEMA_FIELDS':['contract','schema'],'CONTRACT_FIELDS':sorted(json.loads(embedded)['contract']),'ORDERING':'sort_keys=True recursively; native unordered collections use codec._wire set semantics','WHITESPACE':'compact comma/colon separators','ENCODING':'UTF-8','NEWLINE':'none; write_bytes(raw)','ESCAPING':'ensure_ascii=False, standard JSON string escaping','NUMBER_RULE':'allow_nan=False; fixed retained strings/typed identities and arrays, no numeric ambiguity'},'WRITER_SEMANTICS':'RAW_DECODE: source() writes canonical_bytes(body), stores raw.decode() in Provenance.excerpt. attach constructs EXTERNAL-RESOLUTION-CONTRACT-1, omitting native $type/provenance. Exact A14 embedded byte value and raw hash are independently retained; generic writer semantics are inspected, not invoked.','RECOVERY_CLASSIFICATION':'EXACT_SOURCE_RETAINED' if exact else 'LOSSLESS_EMBEDDED_SOURCE','LOSSLESS_BYTE_RECOVERY':True,'HISTORICAL_PHYSICAL_SOURCE_RETAINED':bool(exact),'HISTORICAL_RAW_BYTE_CONTENT_RETAINED':True,'ACCEPTED_FIXTURE_SOURCE':False}
save('source-contract.json',contract)
# Candidate in isolated evidence workspace only; not an accepted source or Snapshot edit.
candidate=O/'candidates/recovered-source-bytes.bin';candidate.parent.mkdir(exist_ok=True);candidate.write_bytes(embedded);assert sha(candidate.read_bytes())==expected['sha256']
save('lossless-candidate.json',{'ARTIFACT':pin(candidate),'SOURCE':contract['PRIMARY_BYTE_SOURCE'],'BYTE_COUNT':size,'BYTE_HASH':sha(embedded),'CONTENT_IDENTITY':expected,'CLASSIFICATION':contract['RECOVERY_CLASSIFICATION'],'ACCEPTED_FIXTURE_SOURCE':False,'ORIGINAL_CORRECTED_SNAPSHOT_EDITED':False})
print(json.dumps({'EXACT_FILE_HITS':len(exact),'LOSSLESS_EMBEDDED_HITS':len(embeddedhits),'REFERENCE_ENTRIES':len(refs),'FILE_COUNT':len(manifest),'BYTE_COUNT':size,'HASH':expected['sha256'],'CLASSIFICATION':contract['RECOVERY_CLASSIFICATION']}))
