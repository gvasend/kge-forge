"""Read-only source-domain recovery. Never calls LOAD_PIN or qualification operations."""
import ast,json,hashlib,sys,copy
from pathlib import Path
R=Path('/home/gvasend/app/kge-forge');E=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification'
sys.path.insert(0,str(R))
from adapter.planner import codec,model
CAP=Q/'E2_P05_D01_RUNNER_FIXTURE_CLOSURE_1/fixtures/D01-VARIANT__SOURCE_BYTES__REQUIRED_ROLE.json'
FROZEN=Q/'E2_P05_D01_PROSPECTIVE_MATRIX_CONTRACT_1/sealed-128-obligations.json'
DISPATCH=Q/'E2_P05_D01_FIXTURE_ORACLE_CLOSURE_2/dispatch-table-v2.json'
def load(p):return json.loads(Path(p).read_bytes())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def pin(p):return {'path':str(p.relative_to(R)),'raw_sha256':sha(p.read_bytes())}
def emit(n,x):(E/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
def walk(x,p=''):
 yield p,x
 if isinstance(x,dict):
  for k,v in x.items():yield from walk(v,p+'/'+k.replace('~','~0').replace('/','~1'))
 elif isinstance(x,list):
  for i,v in enumerate(x):yield from walk(v,p+'/'+str(i))
def key(p):return canon(p)
def recover():
 capsule=load(CAP);content=capsule['canonical_content'];bundle=content['arguments']['bundle'];sources=bundle['sources'];assert len(sources)==51
 d=load(DISPATCH)['D01-DISPATCH:SOURCE_BYTES'];ob=[x for x in load(FROZEN)['obligations'] if x['OBLIGATION_ID']=='D01-OBL:SOURCE_BYTES'];assert len(ob)==1
 previous=load(Q/'E2_P05_D01_A14_RUNTIME_PERSISTENCE_QUALIFICATION_31/operand-post-audit.json');owners=[x['REFERENCE'] for x in previous['ROWS'] if x['REFERENCE']['OBLIGATION_ID']=='D01-OBL:SOURCE_BYTES' and x['REFERENCE']['OPERAND_NAME']=='pin'];assert len(owners)==1
 additions={}
 for i,event in enumerate(bundle['events'],1):
  for source in event['result'].get('source_additions',[]):
   assert key(source) not in additions;additions[key(source)]=i
 assert all(k in {key(p) for p in sources} for k in additions)
 provenance=[]
 for pointer,node in walk(bundle):
  if isinstance(node,dict) and node.get('$type')=='Provenance':provenance.append((pointer,node))
 members=[]
 for pos,p in enumerate(sources):
  native=codec._unwire(p);codec.validate_pin(native);physical=codec._path(R,native.path);raw=physical.read_bytes();assert not physical.is_symlink()
  assert p['profile']['value']=='raw-file-sha256' and sha(raw)==p['identity']['sha256']
  roles=[{'pointer':pointer,'method':node.get('method'),'scope':node.get('scope')} for pointer,node in provenance if node.get('path')==p['path'] and node.get('identity')==p['identity']]
  introduced=additions.get(key(p),0)
  members.append({'SOURCE_ID':'D01-SOURCE:'+sha(key(p)),'PIN':p,'PATH':p['path'],'CONTENT_IDENTITY':p['identity'],'RAW_HASH':sha(raw),'BYTE_LENGTH':len(raw),'PROVENANCE_ROLE':roles,'SEMANTIC_ROLE':'Required native source dependency; '+('event source addition' if introduced else 'initial/prefix source'),'SCOPE':content['scope'],'LINEAGE':content['lineage'],'GENERATION':content['generation'],'CONTEXT_MEANING':'Applicability in owning capsule, not a relabeling of physical payload provenance','COLLECTION_POSITION':pos,'POSITION_SEMANTIC':False,'FIRST_AVAILABLE_EVENT_PREFIX':introduced,'ELIGIBILITY':'ELIGIBLE','ELIGIBILITY_REASON':'Exact member of sealed native bundle.sources; satisfies source-availability member role at/after its admission prefix','ELIGIBLE_AS_SOLE_COLLECTION_REPRESENTATIVE':False,'CANONICAL_PATH':True,'TYPE_DOMAIN_CURRENTNESS':'PASS; unchanged native ArtifactPin/raw-file-sha256 and retained bytes'})
 members.sort(key=lambda x:key(x['PIN']))
 prefixes=[{'PREFIX_EVENT_COUNT':i,'SOURCE_IDS':sorted(x['SOURCE_ID'] for x in members if x['FIRST_AVAILABLE_EVENT_PREFIX']<=i),'AVAILABLE_COUNT':sum(x['FIRST_AVAILABLE_EVENT_PREFIX']<=i for x in members)} for i in range(len(bundle['events'])+1)]
 # Broader original candidates remain unselected, not a merged cross-lineage source pool.
 catalog=load(Q/'E2_P05_D01_RUNNER_INPUT_MATRIX_RECOVERY_1/candidate-source-catalog.json');candidate_scopes=[]
 for cid in ob[0]['ORIGINAL_ROW']['CANDIDATE_IDS']:
  candidate=catalog[cid];p=R/candidate['source']['path'];assert sha(p.read_bytes())==candidate['source']['raw_sha256'];doc=load(p)
  native_pins={key(n):n for pointer,n in walk(doc) if isinstance(n,dict) and n.get('$type')=='ArtifactPin'}
  provenances=[{'pointer':pointer,'path':n.get('path'),'identity':n.get('identity'),'scope':n.get('scope')} for pointer,n in walk(doc) if isinstance(n,dict) and n.get('$type')=='Provenance']
  candidate_scopes.append({'CANDIDATE_ID':cid,'ROLE':candidate['role'],'SOURCE':candidate['source'],'SOURCE_IDENTITY':candidate['source_identity'],'SELECTED':False,'CONTEXT':candidate.get('context'),'SOURCE_PINS':sorted(native_pins.values(),key=key),'PROVENANCE_REFERENCES':provenances,'COLLECTION_STATUS':'Recovered candidate context only; never merged into owning capsule or selected as its replacement'})
 runners=[]
 for c in load(Q/'E2_P05_D01_RUNNER_INPUT_MATRIX_RECOVERY_1/runner-source-candidates.json')['candidates']:
  path=R/c['source']['path'];raw=path.read_bytes();assert sha(raw)==c['source']['raw_sha256'];tree=ast.parse(raw.decode());lines=raw.decode().splitlines();hits=[]
  for n in ast.walk(tree):
   if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ['load_pinned','_verify_sources','_check_snapshot_pins','restore','save_bundle']:
    hits.append({'line':n.lineno,'call':n.func.attr,'text':lines[n.lineno-1].strip()})
  runners.append({'SOURCE':c['source'],'CLASSIFICATION':c['classification'],'DECLARED_BY_SEALED_CONTRACT':c['declared_by_sealed_contract'],'SOURCE_OR_PERSISTENCE_CALLS':sorted(hits,key=lambda x:x['line']),'SINGULAR_PRIMARY_SOURCE_SELECTION_RULE':None,'AUTHORITY':'Component evidence only; no candidate binds complete E2-D01 runner','INTERPRETATION':'Source/persistence helpers validate required dependencies; no SOURCE_BYTES-specific primary/first/last selection rule'})
 assert len(runners)==11
 return {'OWNERS':owners,'DISPATCH':d,'OBLIGATION':ob[0],'CAPSULE_SOURCE':pin(CAP),'MEMBERS':members,'PREFIXES':prefixes,'BROADER_CANDIDATE_CONTEXTS':candidate_scopes,'RUNNER_INSPECTION':runners,'SELECTION_UNIQUE':False,'SELECTED_PIN':None}
if __name__=='__main__':
 result=recover()
 if '--identity' in sys.argv:print(sha(canon(result)));sys.exit(0)
 emit('recovered-contract.json',{'OWNERS':result['OWNERS'],'DISPATCH_V2':result['DISPATCH'],'FROZEN_OBLIGATION':result['OBLIGATION'],'SEMANTIC_ROLE':'Every required native source whose availability/pinned content participates in determinism, qualified at its exact current or event-prefix boundary','NATIVE_CALL_CARDINALITY':1,'AGGREGATE_CARDINALITY':'All required pins per selected checkpoint/prefix','PRIMARY_SOURCE_ROLE_DEFINED':False,'COLLECTION_SEMANTICS':'Native unordered set-like keyed pins; temporal availability ordered','RAW_PIN_KEY':['path','pointer','profile'],'IDENTITY_DISTINCTION':'Native pin content identity authenticates bytes; documentary ordering has no selection authority','NATIVE_SOURCE':pin(R/'adapter/planner/codec.py'),'NATIVE_LOAD_PIN_SIGNATURE':'load_pinned(root,pin) -> bytes or projected JSON','QUALIFICATION_OPERATION_INVOKED':False})
 emit('source-collection.json',{'OWNING_CAPSULE':result['CAPSULE_SOURCE'],'COUNT':51,'MEMBERS':result['MEMBERS'],'PREFIXES':result['PREFIXES'],'BROADER_CANDIDATE_CONTEXTS':result['BROADER_CANDIDATE_CONTEXTS'],'CANDIDATE_CONTEXTS_SELECTED':False,'COMPLETE_AGGREGATE_MATRIX_SOURCE_DOMAIN_SELECTED':False,'A14_10_PIN_SET_IS_THIS_COLLECTION':False})
 emit('runner-candidate-inspection.json',result['RUNNER_INSPECTION'])
 emit('reconstruction.json',{'SEMANTIC_IDENTITY':'qualification-source-bytes-recovery-v1:'+sha(canon(result)),'SOURCE_BYTES_PIN_SELECTION_UNIQUE':False,'SELECTED_PIN':None,'ELIGIBLE_MEMBER_COUNT':51,'ELIGIBLE_SOLE_REPRESENTATIVE_COUNT':0})
 print('RECOVERY: 51 capsule sources; 16 unselected candidate contexts; 11 runners; no unique singular source')
