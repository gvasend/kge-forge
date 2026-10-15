"""Association evidence classification; no projection object/proof creation or execution."""
import json,hashlib,sys,re
from pathlib import Path
R=Path('/home/gvasend/app/kge-forge');E=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification';G=Q/'E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/accepted-support-graph.json'
sys.path.insert(0,str(R))
from adapter.planner import codec,model,typed_proofs,proof_installation

def load(p):return json.loads(Path(p).read_bytes())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def pin(p):return {'path':str(p.relative_to(R)),'raw_sha256':sha(p.read_bytes())}
def emit(n,x):(E/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
def at(x,pointer):
 for k in pointer.split('/')[1:]:
  k=k.replace('~1','/').replace('~0','~');x=x[int(k)] if isinstance(x,list) else x[k]
 return x

def recover():
 graph=load(G);v=dict(graph);gid=v.pop('GRAPH_IDENTITY');assert gid=='qualification-A15-support-graph-v1:'+sha(canon(v));assert len(graph['NODES'])==131 and len(graph['EDGES'])==474
 nodes={n['NODE_ID']:n for n in graph['NODES']};records=[];inventory=[]
 cap=load(Q/'E2_P05_D01_FIXTURE_ORACLE_CLOSURE_2/fixtures/D01-VARIANT__E2-A15__CANONICAL_REQUIRED_BEHAVIOR.json');snapshot=codec._unwire(cap['canonical_content']['arguments']['snapshot'])
 for n in graph['NODES']:
  if n['TYPE']=='SOURCE_CONTENT':assert sha((R/n['SOURCE_PIN']['path']).read_bytes())==n['NATIVE_IDENTITY']['sha256']
 for node in graph['NODES']:
  if node['TYPE'] not in ['TypedProof','TypedProofContract']:continue
  r=node['NATIVE_RECORD'];native=codec._unwire(r);model.validate_types(native,getattr(model,node['TYPE']));assert codec._wire(typed_proofs.identity(native))==r['id']
  records.append({'NODE_ID':node['NODE_ID'],'NATIVE_TYPE':node['TYPE'],'NATIVE_IDENTITY':r['id'],'PROOF_TYPE':r['proof_type'],'TARGET':r['target'],'DECLARED_SUPPORTS':r['supports'],'SUPPORT_FINGERPRINTS':r['support_identities'],'AUTHORITY':r['authority'],'AUTHORITY_IDENTITY':r['authority_identity'],'SCOPE':r['scope'],'LINEAGE':r['lineage'],'GENERATION':r['generation'],'PROVENANCE':r['provenance'],'EXISTING_RECORD_IDENTITY_VERIFIED':True,'NEW_PROOF_CREATED':False,'USABILITY':typed_proofs.usable(snapshot,native) if node['TYPE']=='TypedProof' else proof_installation.contract_current(snapshot,native),'QUERY_KIND':'Read-only native pre-state usability/currentness; no transition/replay/after-state oracle','SOURCE':pin(G)})
 for edge in graph['EDGES']:
  s=nodes[edge['FROM']];t=nodes[edge['TO']];record=t['NATIVE_RECORD'];field=edge['FIELD_PATH'];categories=[];maptype='SEMANTICALLY_RELATED_ONLY';rule='R-STRUCTURAL-REFERENCE';targettype=t['TYPE']+'.'+field;excluded=None;semantic_direction='Original typed referent -> containing record; native semantic direction must follow field meaning';missing=[]
  if edge['ROLE']=='PROVENANCE_SUPPORT':
   categories=['PROVENANCE'];rule='R-PROVENANCE-BINDING';maptype='EXACT_TYPED_MAPPING';targettype='model.Provenance at '+t['TYPE']+field;assert at(record,field)['identity']==s['NATIVE_IDENTITY'];excluded='Not a member of TypedProof.supports just because provenance exists; may be separately operative under record-specific invalidation/currentness contract'
  elif edge['ROLE']=='INSTALLATION_GRANT_SUPPORT':
   if field.rsplit('/',1)[-1] in ['decision_id','contract_id','provenance']:
    categories=['DEPENDENCY','OTHER_TYPED_ROLE'];rule='R-INSTALLATION-GRANT-SUPPORT';maptype='DETERMINISTIC_PROJECTION';targettype='installation.support_ids exact grant content references';missing=['MISSING_CURRENTNESS','MISSING_CONSUMER_ROOT']
   elif field.rsplit('/',1)[-1]=='content_id':
    categories=['DECLARATION','OTHER_TYPED_ROLE'];rule='R-INSTALL-GRANT-CONTENT-APPLICABILITY';maptype='DETERMINISTIC_PROJECTION';targettype='installation.grant_fields.content_id exact authorized definition content';excluded='Authorized content binding; not installation.support_ids contribution or mandatory proof support'
   else:categories=['UNCLASSIFIED'];maptype='NO_SUPPORTED_MAPPING';rule=None;missing=['MISSING_TYPED_ROLE','MISSING_NORMATIVE_SUPPORT_RULE']
  elif edge['ROLE']=='NATIVE_TYPED_REFERENCE':
   value=at(record,field);assert value==s['NATIVE_IDENTITY'],(t['TYPE'],field)
   if '/request/source_additions/' in field or '/request/definition_sources/' in field:
    categories=['DECLARATION'];rule='R-DECLARED-SOURCE-MEMBERSHIP';maptype='EXACT_TYPED_MAPPING';excluded='Available/declaration pin membership is not declared proof support or a standalone invalidation dependency'
   elif t['TYPE'] in ['TypedProof','TypedProofContract'] and re.fullmatch(r'/supports/\d+',field):
    categories=['PROOF_SUPPORT','DEPENDENCY'];rule='R-TYPED-PROOF-DECLARED-SUPPORT';maptype='EXACT_TYPED_MAPPING';targettype=t['TYPE']+'.supports member paired with support_identities';semantic_direction='Support reference -> proof/contract; mandatory within the individual declared proof path';missing=['MISSING_CURRENTNESS','MISSING_CONSUMER_ROOT']
   elif t['TYPE'] in ['TypedProof','TypedProofContract'] and field=='/target':
    categories=['OWNERSHIP'];rule='R-TYPED-PROOF-TARGET';maptype='DETERMINISTIC_PROJECTION';semantic_direction='Proof/contract -> target (field-defined orientation differs from generic referent -> record association)';missing=['MISSING_CONSUMER_ROOT'];excluded='Native proof-target binding does not designate A15 owner set'
   elif t['TYPE']=='TypedProof' and field=='/contract':
    categories=['PROOF_SUPPORT','OTHER_TYPED_ROLE'];rule='R-PROOF-CONTRACT-BINDING';maptype='EXACT_TYPED_MAPPING';targettype='TypedProof.contract foreign-key binding, not supports tuple membership';missing=['MISSING_CURRENTNESS']
   elif t['TYPE'] in ['TypedProof','TypedProofContract'] and field in ['/authority','/authority_identity']:
    categories=['OTHER_TYPED_ROLE','DEPENDENCY'];rule='R-PROOF-AUTHORITY-USABILITY';maptype='EXACT_TYPED_MAPPING';targettype='Native proof authority/type/identity/currentness constraint; not source-ID substitution';missing=['MISSING_CURRENTNESS']
   elif '/provenance/identity' in field or field=='/source/identity':
    categories=['PROVENANCE','OTHER_TYPED_ROLE'];rule='R-PROVENANCE-IDENTITY';maptype='EXACT_TYPED_MAPPING';excluded='Identity binding only; no new mandatory proof-group membership'
   elif t['TYPE']=='Action' and field.startswith('/prerequisites/'):
    categories=['DEPENDENCY'];rule='R-ACTION-PREREQUISITE';maptype='EXACT_TYPED_MAPPING';semantic_direction='Explicit Gate target -> consuming Action; not generic association inference';missing=['MISSING_CURRENTNESS','MISSING_CONSUMER_ROOT']
   elif t['TYPE'] in ['TypedProofContract','TypedProof'] or field=='/id' or field=='/identity':
    categories=['OTHER_TYPED_ROLE'];rule='R-IDENTITY-FIELD';maptype='EXACT_TYPED_MAPPING';excluded='Identity/self/source reference is not independent support-group membership'
   elif t['TYPE'] in ['ValidationInstance','ValidationSupportRecord','ValidationResultRecord','ReceiptAdmission'] and (field.startswith('/inputs/') or field.startswith('/input_identities/') or field.startswith('/dependencies/')):
    categories=['DEPENDENCY','OTHER_TYPED_ROLE'];rule='R-DECLARED-VALIDATION-RECEIPT-INPUT';maptype='EXACT_TYPED_MAPPING';missing=['MISSING_CURRENTNESS','MISSING_CONSUMER_ROOT','MISSING_NORMATIVE_SUPPORT_RULE']
   else:
    categories=['OTHER_TYPED_ROLE'];rule='R-NATIVE-STRUCTURAL-FIELD';maptype='EXACT_TYPED_MAPPING';excluded='Faithful existing typed field reference only; operative necessity/relevance not supplied by generic bucket';missing=['MISSING_NORMATIVE_SUPPORT_RULE','MISSING_CONSUMER_ROOT']
  else:categories=['UNCLASSIFIED'];maptype='NO_SUPPORTED_MAPPING';rule=None;missing=['MISSING_TYPED_ROLE']
  inventory.append({'ASSOCIATION_ID':'qualification-A15-association-v1:'+sha(canon({'graph':gid,'association':edge})),'SOURCE_NODE':s['NODE_ID'],'SOURCE_NODE_TYPE':s['TYPE'],'TARGET_NODE':t['NODE_ID'],'TARGET_NODE_TYPE':t['TYPE'],'RELATIONSHIP_TYPE':edge['ROLE'],'DECLARED_ROLE':{'FIELD_PATH':field,'EXACT_ASSOCIATION':edge},'SOURCE_NATIVE_IDENTITY':s['NATIVE_IDENTITY'],'CONTENT_IDENTITY':s['NATIVE_IDENTITY'] if isinstance(s['NATIVE_IDENTITY'],dict) and s['NATIVE_IDENTITY'].get('kind',{}).get('value')=='CONTENT_IDENTITY' else None,'SCOPE':graph['CONTEXT']['scope'],'LINEAGE':graph['CONTEXT']['lineage'],'GENERATION':graph['CONTEXT']['generation'],'PROVENANCE':edge.get('PROVENANCE',{'SOURCE':pin(G),'FIELD_PATH':field}),'CURRENTNESS':'Existing serialized record only; role/source/authority/context usability not inferred','AUTHORITATIVE_SOURCE':pin(G),'SEMANTIC_CATEGORIES':categories,'CLASSIFIED':categories!=['UNCLASSIFIED'],'MAPPABLE':maptype in ['EXACT_TYPED_MAPPING','DETERMINISTIC_PROJECTION'],'MAPPING_CLASSIFICATION':maptype,'MAPPING_RULE':rule,'TARGET_NATIVE_TYPE':targettype,'SEMANTIC_DIRECTION':semantic_direction,'MISSING_DISCRIMINATORS':missing,'EXCLUSION_REASON':excluded,'A15_REQUIRED_SUPPORT_RELEVANCE':'UNDETERMINED_OWNER_NECESSITY_CONTEXT; classification does not select targets','IDENTITY_EFFECT':'Preserve existing native fields/IDs; association ID is separate qualification metadata','CREATES_PROOF_REQUIREMENT':False})
 inventory.sort(key=lambda x:x['ASSOCIATION_ID']);assert len({x['ASSOCIATION_ID'] for x in inventory})==474
 counts={k:sum(x['MAPPING_CLASSIFICATION']==k for x in inventory) for k in ['EXACT_TYPED_MAPPING','DETERMINISTIC_PROJECTION','SEMANTICALLY_RELATED_ONLY','NO_SUPPORTED_MAPPING']};categories={k:sum(k in x['SEMANTIC_CATEGORIES'] for x in inventory) for k in ['PROOF_SUPPORT','ALTERNATIVE_PROOF','DECLARATION','PROVENANCE','OWNERSHIP','DEPENDENCY','OTHER_TYPED_ROLE','UNCLASSIFIED']}
 groups={}
 for p in records:
  if p['NATIVE_TYPE']=='TypedProof':groups.setdefault(canon(p['TARGET']).decode(),[]).append(p['NATIVE_IDENTITY'])
 projected_candidates={}
 cmp=load(Q/'E2_P05_D01_A15_TARGET_SELECTION_RECONCILIATION_37/membership-semantic-reconciliation.json')
 for name,members in cmp['MEMBERSHIPS'].items():
  out=[]
  for member in members:
   related=[x for x in inventory if x['SOURCE_NODE']==member['SOURCE_NODE_ID']]
   out.append({'SOURCE_IDENTITY':member['SOURCE_IDENTITY'],'CATEGORIES':sorted({category for x in related for category in x['SEMANTIC_CATEGORIES']}),'ASSOCIATION_IDS':[x['ASSOCIATION_ID'] for x in related],'QUALIFIED_A15_SUPPORT_TARGET':False,'ACTUAL_A15_TARGET_MEMBERSHIP':'UNDETERMINED','NOTE':'Declaration/provenance/typed field categories are not owner-qualified necessity'})
  projected_candidates[name]=out
 return {'GRAPH_IDENTITY':gid,'GRAPH_SOURCE':pin(G),'GRAPH_NODES':131,'GRAPH_ASSOCIATIONS':474,'SOURCE_PINS':54,'ASSOCIATIONS':inventory,'CLASSIFICATION_COUNTS':categories,'MAPPING_COUNTS':counts,'ASSOCIATIONS_CLASSIFIED':sum(x['CLASSIFIED'] for x in inventory),'ASSOCIATIONS_UNCLASSIFIED':sum(not x['CLASSIFIED'] for x in inventory),'EXISTING_NATIVE_PROOF_RECORDS':records,'EXISTING_PROOFS_PER_TARGET':groups,'CURRENT_MULTIPLE_PROOF_ALTERNATIVE_TARGETS':sum(len(v)>1 for v in groups.values()),'A15_GRAPH_PROJECTION_COMPLETE':False,'GRAPH_PROJECTION_IDENTITY':None,'OWNER_INDEPENDENT_TYPED_CORE_CORRESPONDENCE':True,'OWNERSHIP_REQUIRED_FOR_PROJECTION':'NO for faithful existing typed record/field correspondence; YES for required A15 support universe/relevance/necessity closure','A15_TARGET_SELECTION_READY':False,'CANDIDATE_CLASSIFICATIONS':projected_candidates,'MISSING_INFORMATION':['MISSING_CONSUMER_ROOT: A15 owner/relevance universe','MISSING_NORMATIVE_SUPPORT_RULE: case necessity/target closure/disjointness','MISSING_CURRENTNESS: association-level applicability must bind native role/authority/source/context checks','MISSING_PROOF_GROUP: no evidence to turn arbitrary generic associations into declared support groups; existing TypedProof supports already explicit'],'NATIVE_MODEL_CHANGE_REQUIRED':False,'DECISIVE_FINDING':'No adapter is needed to recover existing native TypedProof/Contract records. Metadata field indexing is feasible; whole A15 required-support projection needs normative knowledge/applicability, not a missing generic native type.','NATIVE_PRESTATE_PROOF_CURRENTNESS_QUERIES':4,'TYPED_PROJECTION_ARTIFACT_CREATED':False,'ADAPTER_IMPLEMENTED':False,'DECISION_REQUIRED':True,'DECISION_READY':False,'DECISION_OPTIONS':[]}
if __name__=='__main__':
 r=recover()
 if '--identity' in sys.argv:print(sha(canon(r)));raise SystemExit
 emit('association-classification.json',r['ASSOCIATIONS']);emit('semantic-correspondence.json',r);emit('existing-native-proof-correspondence.json',r['EXISTING_NATIVE_PROOF_RECORDS']);print('41 correspondence',r['CLASSIFICATION_COUNTS'],r['MAPPING_COUNTS'],'complete projection NO')
