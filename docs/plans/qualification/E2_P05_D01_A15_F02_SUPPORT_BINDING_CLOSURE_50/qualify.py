import pathlib,json,hashlib,sys
from adapter.planner import codec as c,model as m,typed_proofs as tp,proof_installation as pi,installation as inst
P=pathlib.Path('docs/plans/qualification');E=P/'E2_P05_D01_A15_F02_SUPPORT_BINDING_CLOSURE_50'
def read(p):return json.loads(p.read_text())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def pin(p):return {'path':str(p),'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def write(n,x):(E/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
auth={}
for pack in ['E2_P05_D01_A15_F01_OWNER_ROLE_CLOSURE_49','E2_P05_D01_A15_OWNER_SUPPORT_BINDING_RECOVERY_48','E2_P05_D01_A15_NORMATIVE_INSTANCE_CLOSURE_PLANNING_47','E2_P05_D01_A15_GOVERNED_SEMANTIC_ELICITATION_46','E2_P05_D01_A15_RETAINED_DATA_BINDING_45','E2_P05_D01_SOURCE_BYTES_DISPATCH_CORRECTION_33']:
 for f,h in read(P/pack/'evidence-index.json')['FILES'].items():
  path=pathlib.Path(f)
  if not path.exists():path=P/pack/f
  assert hashlib.sha256(path.read_bytes()).hexdigest()==h,f
  auth[str(path)]=h
front=read(P/'E2_P05_D01_A15_NORMATIVE_INSTANCE_CLOSURE_PLANNING_47/minimal-independent-closure-frontier.json')['ITEMS'];f02=front[1];assert f02['FRONTIER_ID']=='F02'
f49=read(P/'E2_P05_D01_A15_F01_OWNER_ROLE_CLOSURE_49/updated-seven-family-frontier.json')[1];assert all(f49[k]==v for k,v in f02.items())
oldgaps=read(P/'E2_P05_D01_A15_APPLICABILITY_GAP_DECOMPOSITION_44/typed-gap-inventory.json')
accept={'FAMILY_ID':'F02','EXACT_ORIGINAL_FAMILY':f02,'SOURCE':pin(P/'E2_P05_D01_A15_NORMATIVE_INSTANCE_CLOSURE_PLANNING_47/minimal-independent-closure-frontier.json'),'POINTER':'/ITEMS/1','REQUIRED_INPUTS':[f02['MISSING_VALUE']],'DEPENDENT_GAPS':f02['DEPENDENT_GAPS'],'PREREQUISITES_BY_GAP':{r['GAP_ID']:r['DEPENDENCIES'] for r in oldgaps if r['GAP_ID'] in f02['DEPENDENT_GAPS']},'ACCEPTANCE_RULE':f02['VALIDATION_RULE'],'AUTHORITY_REQUIREMENT':f02['AUTHORITY_REQUIRED'],'CLOSURE_CONDITION':{'derived_view':'All operative source-to-support relationships required by applicable owners explicitly bound/current and independently verified; current configuration roles alone insufficient','not_literal_original_field':True},'SCOPE_OF_FOUR_CANDIDATES':'Subset of F02; original family is not restricted to these four'}
gp=P/'E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/accepted-support-graph.json';g=read(gp);cap=pathlib.Path(g['CAPSULE_SOURCE']['path']);assert hashlib.sha256(cap.read_bytes()).hexdigest()==g['CAPSULE_SOURCE']['raw_sha256'];s=c._unwire(read(cap)['canonical_content']['bundle']).current;assert c._wire(c.snapshot_id(s))==g['PRESTATE_ID'];tp.validate_records(s)
original_candidates=read(P/'E2_P05_D01_A15_F01_OWNER_ROLE_CLOSURE_49/four-proof-source-candidates.json');assert len(original_candidates)==4
sources=[n for n in g['NODES'] if n.get('TYPE')=='SOURCE_CONTENT'];records=list(s.proof_contracts)+list(s.typed_proofs);candidates=[]
assoc=read(P/'E2_P05_D01_A15_RETAINED_DATA_BINDING_45/binding-D05.json')['VALUE']
for old in original_candidates:
 native=next(p for p in records if c._wire(p.id)==old['PROOF_ID']);contract=native if type(native) is m.TypedProofContract else next(p for p in s.proof_contracts if p.id==native.contract)
 assert tp.identity(native)==native.id
 aliases=[n['SOURCE_PIN'] for n in sources if n['NATIVE_IDENTITY']==old['CONTENT_IDENTITY']];assert aliases and old['SOURCE_PIN'] in aliases
 for src in aliases:
  assert src['identity']==old['CONTENT_IDENTITY'];assert hashlib.sha256(pathlib.Path(src['path']).read_bytes()).hexdigest()==src['identity']['sha256'];auth[src['path']]=pin(pathlib.Path(src['path']))['raw_sha256']
 configlinks=[]
 for rec in pi.records(s,'ROOT_SLOT_CONFIGURATION_SET'):
  cfg=pi.configuration(rec.request)
  for entity in cfg[-2]:
   if c._wire(entity.identity)==old['CONTENT_IDENTITY'] and any(p.id==contract.id for p in cfg[-1]):
    d,b=pi.descriptor(rec.request.definition)
    inst.validate_authority(rec.request,s.context)
    assert inst.old_reference(s,d)==rec.id
    assert pi.support_current(s,rec) and pi.contract_current(s,contract)
    configlinks.append({'INSTALLED_ID':c._wire(rec.id),'SOURCE_ENTITY_ID':c._wire(entity.id),'ENTITY_IDENTITY':c._wire(entity.identity),'AUTHORITY':c._wire(rec.request.authority),'AUTHORITY_BINDINGS':c._wire(rec.request.authority_bindings),'CONTEXT':c._wire(s.context),'ROLE_DESCRIPTOR':d['subject'],'CONFIGURATION_CURRENT':True,'CONTRACT_CURRENT':True,'NATIVE_RULE':'proof_installation.configuration, support_current, contract_current and normalize_dependencies','PROVENANCE':c._wire(rec.request.definition.provenance)})
 assert configlinks
 declares=c._wire(native.supports);fingerprints=c._wire(native.support_identities)
 assert all(tp.support_identity(s,x)==y for x,y in zip(native.supports,native.support_identities))
 # Exact raw source identity is neither declared SlotId/KnowledgeId nor the proof-support fingerprint namespace.
 assert old['CONTENT_IDENTITY'] not in declares and old['CONTENT_IDENTITY'] not in fingerprints
 graphnode=next(n for n in g['NODES'] if n.get('NATIVE_IDENTITY')==old['PROOF_ID'])
 links=[]
 for j,a in enumerate(assoc):
  edge=a['DECLARED_ROLE']['EXACT_ASSOCIATION']
  if edge.get('TO')==graphnode['NODE_ID'] and (edge.get('CONTENT_IDENTITY')==old['CONTENT_IDENTITY'] or edge.get('REFERENCED_IDENTITY')==old['CONTENT_IDENTITY']):
   isdecl=edge.get('FIELD_PATH','').startswith('/supports/')
   links.append({'ASSOCIATION_ID':a['ASSOCIATION_ID'],'D05_POINTER':f'/VALUE/{j}','MAPPING_RULE':a['MAPPING_RULE'],'SEMANTIC_CATEGORIES':a.get('SEMANTIC_CATEGORIES'),'ROLE':edge['ROLE'],'STATUS':'QUALIFIED_SUPPORT' if isdecl else 'QUALIFIED_NON_SUPPORT','MEANING':'Declared proof tuple member only' if isdecl else 'Exact metadata/reference mapping; not promoted into declared proof support. Installed configuration role separately established.'})
 candidates.append({'CANDIDATE_ID':old['CANDIDATE_ID'],'SOURCE_CONTENT_IDENTITY':old['CONTENT_IDENTITY'],'SOURCE_PIN':old['SOURCE_PIN'],'SOURCE_ALIASES':aliases,'CONFIGURATION_ROLE':configlinks,'NATIVE_SUPPORT_IDENTITY':{'declared_supports':declares,'support_fingerprints':fingerprints,'source_is_declared_support':False},'PROOF_IDENTITY':old['PROOF_ID'],'NATIVE_RECORD_TYPE':type(native).__name__,'CONSUMER_IDENTITY':c._wire(native.target),'SCOPE':native.scope,'LINEAGE':native.lineage,'GENERATION':native.generation,'CURRENTNESS':'CURRENT_OPERATIVE_CONFIGURATION','AUTHORITY':c._wire(native.authority),'CONTEXT':c._wire(s.context),'PROVENANCE':c._wire(native.provenance),'PROOF_SUPPORT_CLASSIFICATION':'CONFIGURATION_ONLY','DECLARED_SUPPORT_ROLE':'Raw configuration source is an installed contract prerequisite, not a member of supports tuple','SUPPORT_GROUP':'ALL declared support members; ANY usable proof paths for target','BINDING_PROVENANCE':{'original_candidate':pin(P/'E2_P05_D01_A15_F01_OWNER_ROLE_CLOSURE_49/four-proof-source-candidates.json'),'native_rule':pin(pathlib.Path('adapter/planner/typed_proofs.py')),'native_configuration_rule':pin(pathlib.Path('adapter/planner/proof_installation.py'))},'ASSOCIATION_QUALIFICATION':links,'SUPPORT_NECESSITY':'UNDETERMINED_FOR_A15','A15_OWNER_APPLICABILITY':'NOT_ADOPTED','A15_INVALIDATION_TARGET':'UNDETERMINED'})
unique=[]
for ci in sorted({canon(x['SOURCE_CONTENT_IDENTITY']).decode() for x in candidates}):
 identity=json.loads(ci);matched=[x for x in candidates if x['SOURCE_CONTENT_IDENTITY']==identity]
 unique.append({'CONTENT_IDENTITY':identity,'CANDIDATES':[x['CANDIDATE_ID'] for x in matched],'ALIASES':matched[0]['SOURCE_ALIASES'],'PHYSICAL_HASH_VERIFIED':True,'IDENTITY_COMPARISON':'Full kind/namespace/sha256, not path/hash alone'})
assert len(unique)==2
collisions=[]
for issue in read(P/'E2_P05_D01_A15_F01_OWNER_ROLE_CLOSURE_49/retained-projection-defect.json'):
 identity=issue['SUBJECT_ID'];matches={typ:[(i,n) for i,n in enumerate(g['NODES']) if n.get('NATIVE_IDENTITY')==identity and n.get('TYPE')==typ] for typ in ('Action','ActionStatus')};assert all(len(v)==1 for v in matches.values())
 def exact(typ):
  i,n=matches[typ][0];return {'NATIVE_IDENTITY':identity,'TYPE':typ,'GRAPH_NODE_IDENTITY':n['NODE_ID'],'CANONICAL_RECORD_HASH_QUALIFICATION_ONLY':hashlib.sha256(canon(n['NATIVE_RECORD'])).hexdigest(),'SOURCE':pin(gp),'POINTER':f'/NODES/{i}/NATIVE_RECORD'}
 collisions.append({'ACTION_ID':identity,'ACTION_DEFINITION_IDENTITY':exact('Action'),'ACTION_STATUS_IDENTITY':exact('ActionStatus'),'ORIGINAL_COLLISION':issue,'CORRECTED_TYPED_KEYS':[['Action',identity],['ActionStatus',identity]],'EVIDENCE_SOURCE':pin(P/'E2_P05_D01_A15_F01_OWNER_ROLE_CLOSURE_49/retained-projection-defect.json')})
assert len(collisions)==4
# Audit known exact consumers of the affected role projection. Metadata root IDs are not themselves defective.
audit=[{'PATH':str(P/'E2_P05_D01_A15_OWNER_SUPPORT_BINDING_RECOVERY_48/owner-role-evidence-inventory.json'),'STATUS':'AMBIGUOUS_HISTORICAL_VIEW','REQUALIFICATION_REQUIRED':'Use separately sealed exact Action/ActionStatus view for native roles, fields and any derived consumer counts; original file retained'}, {'PATH':str(P/'E2_P05_D01_A15_OWNER_SUPPORT_BINDING_RECOVERY_48/per-subject-applicability.json'),'STATUS':'AMBIGUOUS_HISTORICAL_VIEW','REQUALIFICATION_REQUIRED':'Native factual role rationale must use corrected definitions; proposed K01 counts and unadopted authority unchanged'}, {'PATH':str(P/'E2_P05_D01_A15_OWNER_SUPPORT_BINDING_RECOVERY_48/missing-discriminators.json'),'STATUS':'AMBIGUOUS_HISTORICAL_VIEW','REQUALIFICATION_REQUIRED':'Reread affected roles before relying on per-action missing evidence; retain normative ownership gap'}, {'PATH':str(P/'E2_P05_D01_A15_F01_OWNER_ROLE_CLOSURE_49/subject-role-applicability-matrix.json'),'STATUS':'CORRECTED_VIEW_AVAILABLE','REQUALIFICATION_REQUIRED':None}, {'PATH':str(P/'E2_P05_D01_A15_OWNER_SUPPORT_BINDING_RECOVERY_48/source-support-binding-inventory.json'),'STATUS':'UNRELATED','REASON':'Proof/Knowledge/Slot IDs, no Action definition/status selection'}, {'PATH':str(P/'E2_P05_D01_A15_NORMATIVE_INSTANCE_CLOSURE_PLANNING_47/owner-discriminator-inventory.json'),'STATUS':'UNRELATED','REASON':'Retained D01 identities/status and proposed responsibility gaps; does not use ambiguous Action definition'}, {'PATH':str(P/'E2_P05_D01_A15_F01_OWNER_ROLE_CLOSURE_49/updated-seven-family-frontier.json'),'STATUS':'CORRECTED_VIEW_AVAILABLE','REASON':'F01 unresolved; correction does not adopt ownership'}]
subjectmatrix=read(P/'E2_P05_D01_A15_F01_OWNER_ROLE_CLOSURE_49/subject-role-applicability-matrix.json');impact=[]
for r in subjectmatrix:
 new=[x['CANDIDATE_ID'] for x in candidates if x['CONSUMER_IDENTITY']==r['SUBJECT_ID']]
 impact.append({'SUBJECT_ID':r['SUBJECT_ID'],'NATIVE_SUPPORT_CONSUMER':r['NATIVE_SUPPORT_CONSUMER'],'CURRENT_PROOF_RELATIONSHIP':r['PROOF_CONSUMER_STATUS'],'PREVIOUS_CLASSIFICATION':r['A15_OWNER_APPLICABILITY'],'NEW_EVIDENCE':new,'MISSING_DISCRIMINATOR':r['MISSING_OWNERSHIP_DISCRIMINATOR'],'PROPOSED_CLASSIFICATION':r['A15_OWNER_APPLICABILITY'],'AUTHORITY_STATUS':'NOT_AUTHORIZED','NORMATIVE_OWNERSHIP_RULE':'Still incomplete; current native role is not an A15 scope decision'})
updated=read(P/'E2_P05_D01_A15_F01_OWNER_ROLE_CLOSURE_49/updated-seven-family-frontier.json')
family=[]
for f in updated:
 family.append({'FAMILY_ID':f['FRONTIER_ID'],'ORIGINAL_DEFINITION':f,'PREVIOUS_STATUS':f['49_STATUS'],'NEW_EVIDENCE':'Four current configuration roles independently qualified as CONFIGURATION_ONLY' if f['FRONTIER_ID']=='F02' else 'No adopted responsibility rule' if f['FRONTIER_ID']=='F01' else None,'NEW_STATUS':f['49_STATUS'],'FIRST_MISSING_REQUIREMENT':'Complete operative source-to-declared-support relationship/coverage under qualified owners' if f['FRONTIER_ID']=='F02' else 'A15 role-to-responsibility discriminator' if f['FRONTIER_ID']=='F01' else f['MISSING_VALUE']})
gates={'F02_FOUR_CANDIDATE_CURRENTNESS_QUALIFIED':True,'F02_EVIDENCE_READY':False,'F02_CLOSED':False,'F01_CLOSED':False,'NORMATIVE_INSTANCE_COMPLETE':False,'NORMATIVE_DECISION_READY':False,'A15_EXECUTION_CONTRACT_READY':False,'WHY':'Original F02 family requires complete operative source/support table; four configuration-only relationships cannot satisfy declared-support membership or unsealed A15 coverage. Existing Package48 knowledge-source mapping remains separate. F01 responsibility and authority unaffected.','FIRST_REMAINING_INPUT_FAMILY':'F01'}
semantic={'acceptance':accept,'candidates':candidates,'content':unique,'collisions':collisions,'audit':audit,'impact':impact,'frontier':family,'gates':gates};id='qualification-A15-F02-binding-v1:'+hashlib.sha256(canon(semantic)).hexdigest()
if '--stdout' in sys.argv:print(json.dumps({'IDENTITY':id,'CURRENT_CONFIGURATION_ROLES':4,'CONFIGURATION_ONLY':4,'EXACT_DECLARED_SUPPORT':0,'DERIVED_DECLARED_SUPPORT':0},sort_keys=True));sys.exit()
for name,x in [('F02-acceptance-inventory.json',accept),('four-candidate-binding-evidence.json',candidates),('two-content-identity-verification.json',unique),('typed-collisions.json',collisions),('collision-propagation-audit.json',audit),('proof-support-qualification-matrix.json',[{k:x[k] for k in ('CANDIDATE_ID','PROOF_IDENTITY','NATIVE_SUPPORT_IDENTITY','PROOF_SUPPORT_CLASSIFICATION','ASSOCIATION_QUALIFICATION','SUPPORT_NECESSITY')} for x in candidates]),('F01-applicability-impact.json',impact),('updated-seven-family-frontier.json',family),('readiness-gates.json',gates)]:write(name,x)
write('authentication.json',{'F02_AUTHENTICATED':True,'PINNED_FILES':auth,'GRAPH':pin(gp),'CAPSULE':pin(cap),'PRESTATE':g['PRESTATE_ID'],'SEMANTIC_IDENTITY':id,'NO_NATIVE_TRANSITIONS':True})
