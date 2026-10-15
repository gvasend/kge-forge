"""Bind exact D01-D05 values as retained evidence, not normative adoption."""
import json,hashlib,sys
from pathlib import Path
R=Path('/home/gvasend/app/kge-forge');E=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification';P=Q/'E2_P05_D01_A15_APPLICABILITY_GAP_DECOMPOSITION_44'
sys.path.insert(0,str(R));from adapter.planner import codec,model,typed_proofs

def load(p):return json.loads(Path(p).read_bytes())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def pin(p):return {'path':str(p.relative_to(R)),'raw_sha256':sha(p.read_bytes())}
def emit(n,x):(E/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
def bind():
 index=load(P/'evidence-index.json')
 for file,h in index['FILES'].items():assert sha((R/file).read_bytes())==h,file
 allgaps=load(P/'typed-gap-inventory.json');assert len(allgaps)==35;gaps=[g for g in allgaps if g['CLASSIFICATION']=='RECOVERABLE_EXISTING_DATA'];assert [g['GAP_ID'] for g in gaps]==['D01','D02','D03','D04','D05']
 graphpath=Q/'E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/accepted-support-graph.json';graph=load(graphpath);nodes={n['NODE_ID']:n for n in graph['NODES']};context=graph['CONTEXT'];binding=[]
 for gap in gaps:
  source=gap['KNOWN_EVIDENCE'];file=R/source['path'];raw=file.read_bytes();assert sha(raw)==source['raw_sha256'];doc=json.loads(raw);id=gap['GAP_ID'];pointer='';extraction=None
  if id=='D01':
   assert isinstance(doc,list) and len(doc)==21;value=doc;typ='QualificationNativeRootConsumerInventory';assert all(r['ROOT_ID'] and r['ROOT_ID'].get('$type') in ['ActionId','ConditionId','SlotId','KnowledgeId','EntityId','EvidenceId'] for r in value)
   for r in value:assert (r['SCOPE'],r['LINEAGE'],r['GENERATION'])==(context['scope'],context['lineage'],context['generation'])
   current='Serialized native statuses/context only; A15 applicability remains UNDETERMINED'
  elif id=='D02':
   assert isinstance(doc,list) and len(doc)==4;value=doc;typ='RetainedNativeTypedProofContractCorrespondenceTable'
   for r in value:
    native=codec._unwire(nodes[r['NODE_ID']]['NATIVE_RECORD']);model.validate_types(native,getattr(model,r['NATIVE_TYPE']));assert codec._wire(typed_proofs.identity(native))==r['NATIVE_IDENTITY'];assert r['USABILITY'] is True and r['DECLARED_SUPPORTS']==nodes[r['NODE_ID']]['NATIVE_RECORD']['supports'];assert (r['SCOPE'],r['LINEAGE'],r['GENERATION'])==(context['scope'],context['lineage'],context['generation'])
   current='Exact retained pre-state proof/contract currentness evidence; no post-invalidation state claimed'
  elif id=='D03':
   assert isinstance(doc,dict) and doc['RESULT']=='PASS' and doc['READ_ONLY_PRESTATE_CURRENTNESS_USABILITY']=='4/4 PASS';value=doc;typ='RetainedQualificationCurrentnessValidationEvidence'
   corroboration=load(R/gaps[1]['KNOWN_EVIDENCE']['path']);assert len(corroboration)==4 and all(r['USABILITY'] is True for r in corroboration)
   current='Retained exact validation evidence corroborated by four native-ID-specific D02 observations, unchanged graph/pre-state/runtime/sources; not a report substituted for a native proof'
  elif id=='D04':
   pointer='/NODES';extraction={'operator':'FILTER_EXACT_NATIVE_METADATA_NODE_TYPE','field':'TYPE','equals':'SOURCE_CONTENT'};value=[n for n in doc['NODES'] if n['TYPE']=='SOURCE_CONTENT'];typ='FrozenNativeSourceContentPinInventory';assert len(value)==54
   for n in value:
    p=n['SOURCE_PIN'];native=codec._unwire(p);codec.validate_pin(native);assert native.identity.kind is model.IdentityKind.CONTENT_IDENTITY;actual=codec._path(R,native.path).read_bytes();assert sha(actual)==native.identity.sha256
    assert (n['SCOPE'],n['LINEAGE'],n['GENERATION'])==(context['scope'],context['lineage'],context['generation'])
   current='54 exact source physical bytes/profile/content pins and frozen applicability context PASS; no target relevance inferred'
  elif id=='D05':
   assert isinstance(doc,list) and len(doc)==474 and len({a['ASSOCIATION_ID'] for a in doc})==474;value=doc;typ='RetainedNativeAssociationFieldCorrespondenceInventory'
   assert all(a['CLASSIFIED'] for a in value)
   for a in value:assert (a['SCOPE'],a['LINEAGE'],a['GENERATION'])==(context['scope'],context['lineage'],context['generation'])
   current='Retained field/role classification only; not total native edge currentness or A15 necessity'
  content={'GAP_ID':id,'VALUE':value,'VALUE_TYPE':typ,'SOURCE_PATH':source['path'],'SOURCE_HASH':source['raw_sha256'],'SOURCE_POINTER':pointer,'SOURCE_EXTRACTION_RULE':extraction,'CONTENT_IDENTITY':{'kind':'CONTENT_IDENTITY','namespace':'raw-file-sha256','sha256':source['raw_sha256']},'VALUE_COMPARISON_IDENTITY':'qualification-retained-data-value-v1:'+sha(canon(value)),'NATIVE_CONTENT_IDENTITY_NOTE':'CONTENT_IDENTITY authenticates exact retained physical container bytes; native subject identities remain unchanged inside VALUE. VALUE_COMPARISON_IDENTITY is qualification-only, not a native proof/event identity','SCOPE':context['scope'],'LINEAGE':context['lineage'],'GENERATION':context['generation'],'CURRENTNESS':current,'PROVENANCE':[{'SOURCE':source,'POINTER':pointer,'EXTRACTION_RULE':extraction},{'GAP_SOURCE':pin(P/'typed-gap-inventory.json'),'GAP_ID':id},{'GRAPH_SOURCE':pin(graphpath),'EXACT_PRESTATE':graph['PRESTATE_ID']}],'VALIDATION_RESULT':'BOUND_PASS','DEPENDENT_GAPS':sorted(g['GAP_ID'] for g in allgaps if id in g['DEPENDENCIES']),'NORMATIVE_INTERPRETATION_ADOPTED':False}
  content['BINDING_IDENTITY']='qualification-A15-retained-binding-v1:'+sha(canon(content));binding.append(content)
 return {'PACKAGE_44_AUTHENTICATED':True,'PACKAGE44_INDEX':pin(P/'evidence-index.json'),'DATA_GAP_IDS':[g['GAP_ID'] for g in gaps],'BINDINGS':binding,'RETAINED_DATA_BINDING':'PASS','EXACT_DECLARED_SOURCE_PRECEDENCE':'Package44 KNOWN_EVIDENCE exact pin selects each retained artifact; corroboration never replaces this source','NORMATIVE_INSTANCE_COMPLETE':False,'AUTHORITY_ISSUED':False,'NATIVE_CASE_OPERATIONS_EXECUTED':0}
if __name__=='__main__':
 d=bind()
 if '--identity' in sys.argv:print(sha(canon(d)));raise SystemExit
 emit('retained-data-bindings.json',d)
 for b in d['BINDINGS']:emit('binding-'+b['GAP_ID']+'.json',b)
 print('45 BOUND_PASS D01-D05; native types/domains/source/context preserved; no normative adoption')
