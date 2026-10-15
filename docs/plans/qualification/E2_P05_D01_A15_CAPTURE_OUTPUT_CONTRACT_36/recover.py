"""Static native-data graph and contract recovery; never transitions/replays/saves."""
import ast,json,hashlib,sys
from pathlib import Path
R=Path('/home/gvasend/app/kge-forge');E=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification'
sys.path.insert(0,str(R))
from adapter.planner import codec
CAP=Q/'E2_P05_D01_FIXTURE_ORACLE_CLOSURE_2/fixtures/D01-VARIANT__E2-A15__CANONICAL_REQUIRED_BEHAVIOR.json'
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
def recover():
 packet=load(CAP);bundle=packet['canonical_content']['arguments']['bundle'];snapshot=codec._wire(codec._unwire(packet['canonical_content']['arguments']['snapshot']));stateid=codec._wire(codec.snapshot_id(codec._unwire(snapshot)));context=snapshot['context']
 nodes=[];edges=[];record_lookup={};native_lookup={};sources={canon(p['identity']):p for p in bundle['sources']}
 for p in sorted(bundle['sources'],key=canon):
  codec.validate_pin(codec._unwire(p));raw=(R/p['path']).read_bytes();assert sha(raw)==p['identity']['sha256']
  identity='qualification-A15-source-node-v1:'+sha(canon(p));nodes.append({'NODE_ID':identity,'TYPE':'SOURCE_CONTENT','NATIVE_IDENTITY':p['identity'],'SOURCE_PIN':p,'SCOPE':context['scope'],'LINEAGE':context['lineage'],'GENERATION':context['generation'],'OWNERSHIP':'Exact sealed bundle source pin; not presumed required for every A15 variant'});native_lookup.setdefault(canon(p['identity']),[]).append(identity)
 for collection,records in snapshot.items():
  if not isinstance(records,list):continue
  for record in records:
   if not isinstance(record,dict):continue
   identity='qualification-A15-record-node-v1:'+sha(canon({'collection':collection,'record':record}));native=record.get('id',record.get('identity'))
   nodes.append({'NODE_ID':identity,'TYPE':record.get('$type','native record'),'COLLECTION':collection,'NATIVE_IDENTITY':native,'NATIVE_RECORD':record,'SCOPE':context['scope'],'LINEAGE':context['lineage'],'GENERATION':context['generation'],'SUPPORT_ROLE':'Exact native '+collection+' record; required-target role still to be qualified'});record_lookup[identity]=record
   if isinstance(native,dict):native_lookup.setdefault(canon(native),[]).append(identity)
 provenance_ids=set();referenced_source_ids=set();categories={}
 for node_id,record in sorted(record_lookup.items()):
  direct=set();refs=set()
  for pointer,value in walk(record):
   if not isinstance(value,dict):continue
   if value.get('$type')=='Provenance':
    content=value['identity'];provenance_ids.add(canon(content));direct.add(canon(content))
    for before in native_lookup.get(canon(content),[]):edges.append({'FROM':before,'TO':node_id,'ROLE':'PROVENANCE_SUPPORT','FIELD_PATH':pointer,'CONTENT_IDENTITY':content,'PROVENANCE':value})
   if value.get('$type')=='ArtifactPin':refs.add(canon(value['identity']))
   if value.get('$type')=='ArtifactIdentity':
    if canon(value) in sources:refs.add(canon(value))
   if value.get('$type','').endswith('Id') or value.get('$type')=='ArtifactIdentity':
    for before in native_lookup.get(canon(value),[]):
     if before!=node_id:edges.append({'FROM':before,'TO':node_id,'ROLE':'NATIVE_TYPED_REFERENCE','FIELD_PATH':pointer,'REFERENCED_IDENTITY':value,'SEMANTICS':'Explicit recorded association/reference; direction does not independently assert mandatory support'})
  # Nested installation grant JSON carries support commitments not always Provanance nodes.
  for pointer,value in walk(record):
   if isinstance(value,str) and pointer.endswith('/grant_json'):
    grant=json.loads(value)
    for field,identity in grant.items():
     if isinstance(identity,dict) and identity.get('kind')=='CONTENT_IDENTITY':
      wire={'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':identity['kind']},'namespace':identity['namespace'],'sha256':identity['sha256']}
      if canon(wire) in sources:
       refs.add(canon(wire))
       for before in native_lookup[canon(wire)]:edges.append({'FROM':before,'TO':node_id,'ROLE':'INSTALLATION_GRANT_SUPPORT','FIELD_PATH':pointer+'/'+field,'CONTENT_IDENTITY':wire})
  referenced_source_ids.update(refs)
  categories.setdefault(record.get('$type','native record'),set()).update(direct|refs)
 edges=sorted({canon(edge):edge for edge in edges}.values(),key=canon);nodes.sort(key=lambda x:x['NODE_ID'])
 graph={'SCHEMA':'A15-STATIC-NATIVE-SUPPORT-ASSOCIATIONS-1','PRESTATE_ID':stateid,'CAPSULE_SOURCE':pin(CAP),'CONTEXT':context,'NODES':nodes,'EDGES':edges,'SOURCE_COUNT':len(sources),'MODEL':'Complete recorded native source/provenance/reference associations; computed proof necessity/cuts are not invented','NATIVE_SEMANTIC_SOURCE_PINS':[pin(R/'adapter/planner/core.py'),pin(R/'adapter/planner/codec.py'),pin(R/'adapter/planner/typed_proofs.py'),pin(R/'adapter/planner/installation.py')]}
 graph['GRAPH_IDENTITY']='qualification-A15-support-graph-v1:'+sha(canon(graph))
 def candidate(predicate,keys):
  keys=set(keys)&set(sources);return {'PREDICATE':predicate,'COUNT':len(keys),'CONTENT_IDENTITIES':sorted([sources[k]['identity'] for k in keys],key=canon),'SELECTED':False,'AUTHORITY':'Diagnostic source-role candidate only; not a qualified target set'}
 a=candidate('Raw pins whose identities occur in native current-state Provenance fields; matches local P03 suite recipe',provenance_ids)
 b=candidate('Raw pins explicitly referenced by current records, including pins/dependency identities and grant content support',referenced_source_ids)
 c=candidate('Provenance/reference identities associated with knowledge/typed proof/proof-contract/authority GraphEntity records',set().union(*(value for typ,value in categories.items() if typ in ['KnowledgeRecord','TypedProof','TypedProofContract','GraphEntity'])))
 # Frozen case/all variants does not promote a local provenance recipe to exact current installed dependency graph ownership.
 target={'TARGETS_UNIQUE':False,'TARGET_CARDINALITY':'All disjoint required accepted-support source variants, each isolated from exact same pre-state; exact set/count unsealed','TARGET_ROLE':'Required accepted knowledge/proof/authority support sources, not one arbitrary bundle source','TARGET_PREDICATE':None,'DISJOINTNESS':'Distinct exact source content identities in separate variant copies; alias paths with same content identity do not create independent targets. Overlapping descendant branches may share support; branch-disjointness is not established.','ORDERING':'Source membership unordered; native parent/ledger trace ordered','CANDIDATE_PROJECTIONS':[a,b,c],'MISSING_RULE':'Authoritative required-support root/consumer-role boundary and exact provenance-vs-transitive dependency source partition for the P04 post-root-proof A15 capsule, with complete supported-variant coverage. Local P03 all-Provenance recipe is component evidence only.','LOCAL_RECIPE_SOURCE':pin(R/'adapter/tests/qualify_p03_prospective.py'),'COMPLETE_TARGET_SET_SELECTED':False,'DESCRIPTOR_CONSTRUCTIBLE_NOW':False}
 return {'GRAPH':graph,'TARGET_CONTRACT':target,'PRESTATE':stateid,'CONTEXT':context,'BUNDLE_SOURCE_COUNT':len(bundle['sources']),'INPUT_EVENT_COUNT':len(bundle['events']),'INPUT_EVENT_HEAD':bundle['events'][-1]['identity'],'NATIVE_EVENT_TRACE':[{'sequence':x['sequence'],'identity':x['identity'],'parent_snapshot':x['parent_snapshot'],'parent_event':x['parent_event'],'after_snapshot':x['after_snapshot'],'result_type':x['result']['$type']} for x in bundle['events']],'MATERIALIZATION_BINDINGS_COUNT':len(bundle.get('dossier_materializations',[])),'POLICY_VERSION':bundle['policy_version'],'NATIVE_SCOPE':bundle['scope'],'SOURCE_BINDINGS':bundle['sources'],'A15_CASE':load(R/'docs/plans/DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.json')['cases'][14],'A16_CASE':load(R/'docs/plans/DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.json')['cases'][15]}
if __name__=='__main__':
 d=recover()
 if '--identity' in sys.argv:print(sha(canon(d)));raise SystemExit
 emit('recovered-contract.json',d);emit('accepted-support-graph.json',d['GRAPH']);emit('target-contract.json',d['TARGET_CONTRACT']);print('GRAPH RECOVERED',len(d['GRAPH']['NODES']),'nodes',len(d['GRAPH']['EDGES']),'edges; diagnostic target counts',[x['COUNT'] for x in d['TARGET_CONTRACT']['CANDIDATE_PROJECTIONS']])
