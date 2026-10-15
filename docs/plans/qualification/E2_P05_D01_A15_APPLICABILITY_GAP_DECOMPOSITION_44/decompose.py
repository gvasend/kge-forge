"""Finite gap decomposition, no target/native transition/closure construction."""
import json,hashlib,sys
from pathlib import Path
R=Path('/home/gvasend/app/kge-forge');E=Path(__file__).resolve().parent;sys.path.insert(0,str(R));Q=R/'docs/plans/qualification';C=Q/'E2_P05_D01_A15_NORMATIVE_KNOWLEDGE_CONTRACT_42';P=Q/'E2_P05_D01_A15_NORMATIVE_KNOWLEDGE_INSTANCE_43'
def load(p):return json.loads(Path(p).read_bytes())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def pin(p):return {'path':str(p.relative_to(R)),'raw_sha256':sha(p.read_bytes())}
def emit(n,x):(E/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
def decompose():
 for folder in [C,P]:
  for file,digest in load(folder/'evidence-index.json')['FILES'].items():assert sha((R/file).read_bytes())==digest,file
 instance=load(P/'proposed-typed-instance.json');assert len(instance['FIVE_FACTS'])==5
 graph=load(Q/'E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/accepted-support-graph.json');body=dict(graph);gid=body.pop('GRAPH_IDENTITY');assert gid=='qualification-A15-support-graph-v1:'+sha(canon(body))
 proof=load(Q/'E2_P05_D01_A15_GRAPH_SEMANTIC_PROJECTION_41/semantic-correspondence.json');assert len(proof['ASSOCIATIONS'])==474
 questions=load(C/'future-elicitation-questions.json');roots=load(Q/'E2_P05_D01_A15_CONSUMER_ROOT_OWNERSHIP_CONTRACT_39/consumer-root-inventory.json')
 gaps=[]
 def gap(id,classification,category,value,typ,consumer,contract,known,missing,deps,method,validation,authority,blocked,status='UNRESOLVED'):
  gaps.append({'GAP_ID':id,'CLASSIFICATION':classification,'CATEGORY':category,'REQUIRED_VALUE':value,'EXPECTED_TYPE':typ,'CONSUMER':consumer,'AUTHORITATIVE_CONTRACT':contract,'KNOWN_EVIDENCE':known,'MISSING_INFORMATION':missing,'DEPENDENCIES':deps,'RECOVERY_METHOD':method,'VALIDATION_RULE':validation,'AUTHORITY_REQUIREMENT':authority,'BLOCKED_OUTPUTS':blocked,'STATUS':status})
 base={'schema':pin(C/'normative-knowledge-schema.json'),'questions':pin(C/'future-elicitation-questions.json'),'instance':pin(P/'proposed-typed-instance.json'),'graph':pin(Q/'E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/accepted-support-graph.json')}
 data_defs=[('D01','Native root/consumer ID and serialized acceptance inventory',pin(Q/'E2_P05_D01_A15_CONSUMER_ROOT_OWNERSHIP_CONTRACT_39/consumer-root-inventory.json')),('D02','Existing TypedProof/Contract identities, declared supports/fingerprints and targets',pin(Q/'E2_P05_D01_A15_GRAPH_SEMANTIC_PROJECTION_41/existing-native-proof-correspondence.json')),('D03','Retained native currentness/usability evidence for two contracts/two proofs',pin(Q/'E2_P05_D01_A15_GRAPH_SEMANTIC_PROJECTION_41/verification.json')),('D04','54 exact source/content/provenance identities and context',base['graph']),('D05','474 native association field/type/schema classifications',pin(Q/'E2_P05_D01_A15_GRAPH_SEMANTIC_PROJECTION_41/association-classification.json'))]
 for id,value,source in data_defs:gap(id,'RECOVERABLE_EXISTING_DATA','EXISTING_DATA',value,'Exact pinned native JSON identity/record table','A15 applicability evidence',base['schema'],source,None,[],'Read pinned record/pointer; retain native identity domains and supplied context','Raw/source identity equal and typed fields exact; no owner/target claim','Read-only preparation authority sufficient',['Normative instance reference fields'],status='RECOVERED_EVIDENCE_NOT_NORMATIVELY_ADOPTED')
 semantic=[];per_question={}
 for fact in instance['FIVE_FACTS']:
  qid=fact['QUESTION_ID'];unresolved=[name for name,value in fact['TYPED_FIELDS'].items() if value['STATUS'] not in ['RECOVERED_COMPLETE','SUPPLIED_AND_NATIVE_CONSISTENT']]
  per_question[qid]=[]
  subterms={
   'inclusion_exclusion_meaning':['owner_inclusion_evidence_rule','owner_exclusion_justification'],
   'frozen_stale_held_control_resume_acceptance_mapping':['dependent_admission_staleness_acceptance_scope','held_blocked_descendant_acceptance_scope','control_acceptance_under_alternative_survival','computed_resume_acceptance_under_alternative_survival'],
   'termination_cycle_duplicate_shared_support_rules':['target_closure_stopping_condition','target_closure_cycle_policy','typed_support_duplicate_handling','shared_dependency_owner_reconciliation'],
   'shared_effect_or_protected_set_policy':['shared_effect_overlap_policy','protected_set_definition_and_invariance']}
  for parent in unresolved:
   for name in subterms.get(parent,[parent]):
    id='S'+str(len(semantic)+1).zfill(2);semantic.append((id,qid,name,parent));per_question[qid].append(id)
 assert len(semantic)==26
 dependency_question={'A15-KNOWLEDGE-K01':[],'A15-KNOWLEDGE-K02':['A15-KNOWLEDGE-K01'],'A15-KNOWLEDGE-K03':['A15-KNOWLEDGE-K01','A15-KNOWLEDGE-K02'],'A15-KNOWLEDGE-K04':['A15-KNOWLEDGE-K01','A15-KNOWLEDGE-K02','A15-KNOWLEDGE-K03'],'A15-KNOWLEDGE-K05':['A15-KNOWLEDGE-K03','A15-KNOWLEDGE-K04']}
 for id,qid,name,parent in semantic:
  fact=next(f for f in instance['FIVE_FACTS'] if f['QUESTION_ID']==qid);deps=['D01','D02','D03','D04','D05']+[x for dep in dependency_question[qid] for x in per_question[dep]]
  category='CONSUMER_ROOT_APPLICABILITY' if qid.endswith('K01') else 'CONTENT_IDENTITY_PARTITION' if qid.endswith('K05') else 'QUALIFIED_SUPPORT_DEPENDENCIES'
  gap(id,'MISSING_NORMATIVE_SEMANTICS',category,name,'Contract42 typed normative field/predicate; original expected object schema preserved',qid,dict(base['questions'],pointer='/'+str(fact['FACT_NUMBER']-1)+'/ALLOWED_ANSWER_TYPE/required'),{'supplied_answer':fact['ORIGINAL_ANSWER'],'partial_binding':fact['TYPED_FIELDS'][parent],'data_evidence':base},'Unresolved atomic term '+name+' within Contract42 field '+parent+'; governing value not supplied; data do not define normative scope/necessity',deps,'Authorized knowledge owner supplies finite typed meaning; do not turn into data search','Complete exact predicate/membership/direction/alternatives/context/provenance; coherent frozen acceptance; independently verifiable','Prospective normative knowledge approval required; preparation alone insufficient',['Complete normative instance','A15 role/target/descriptor/oracle applicability'])
 semantic_ids=[x[0] for x in semantic]
 gap('A01','MISSING_AUTHORITY','AUTHORITY','Actual authorized issuing owner/designation reference','Verified existing authority/designation evidence','Contract42 ISSUING_AUTHORITY',base['schema'],{'human43':'Preparation only; no normative adoption'},'No actual normative issuer/designation binding exists',[],'Obtain actual authorized owner/designation; do not invent an identity','Exact provenance and authorized scope; not preparation assertion','Explicit qualification knowledge-owner authority',['Complete issuing-owner semantic body'])
 gap('V01','OTHER','DERIVED_VALUE_BLOCKED','Complete normative contract content identity','Qualification canonical identity; excludes own ID/future selected receipt','Contract42 KNOWLEDGE_CONTRACT_ID',base['schema'],{'preparation_identity':instance['PREPARATION_IDENTITY']},'Derivable only after semantic fields and actual issuing-owner reference complete',semantic_ids+['A01'],'Later deterministic canonical hash; no redundant elicitation','Complete body, identity domains, exclusions and no authority/identity cycle','No target choice; later adoption remains separate',['Exact normative amendment subject'])
 gap('V02','OTHER','DERIVED_VALUE_BLOCKED','Exact bounded normative applicability/adoption subject','Qualification decision subject pinned to complete contract ID','Contract42 K06',base['questions'],None,'Derivable after complete content and acceptance consequences',semantic_ids+['V01'],'Seal exact rule/applicability/consequences/exclusions after content qualification','Independent qualification and unambiguous scope consequences','Do not issue/select until subject ready',['Actual selected adoption receipt'])
 gap('A02','MISSING_AUTHORITY','AUTHORITY','Actual selected normative adoption/acceptance amendment evidence','Verified bounded decision reference','Contract42 K06 actual_decision_evidence_reference',base['questions'],{'authority_issued':False},'No selected normative adoption, as required by preparation scope',['V02'],'Later explicit bounded decision; not part of current preparation','Exact subject/contract/owner/scope binding; no unrelated grant reuse','Human/designated normative owner selection required',['Authorized normative instance','A15 operand adoption'])
 gap_by={g['GAP_ID']:g for g in gaps};done=set();layers=[]
 while len(done)<len(gaps):
  layer=sorted(g['GAP_ID'] for g in gaps if g['GAP_ID'] not in done and set(g['DEPENDENCIES'])<=done)
  if not layer:raise ValueError('CIRCULAR_OR_UNREACHABLE_GAP_GRAPH')
  layers.append(layer);done.update(layer)
 root_inventory=[]
 for i,root in enumerate(roots):
  root_inventory.append(dict(root,ROOT_INVENTORY_ID='A15-ROOT-CANDIDATE-'+str(i+1).zfill(2),APPLICABILITY='UNDETERMINED',A15_APPLICABILITY_GAPS=per_question['A15-KNOWLEDGE-K01'],MISSING_DISCRIMINATOR='Exact finite owner/root-type applicability predicate and inclusion/exclusion meaning; identity/status presence is not membership'))
 dep_inventory=[]
 graph_nodes={n['NODE_ID']:n for n in graph['NODES']}
 for a in proof['ASSOCIATIONS']:
  target=graph_nodes[a['TARGET_NODE']];native_record=target.get('NATIVE_RECORD',{});proof_contract=native_record.get('contract') if target['TYPE']=='TypedProof' else native_record.get('id') if target['TYPE']=='TypedProofContract' else None
  native_group={'record_identity':native_record.get('id'),'declared_supports':native_record.get('supports'),'support_fingerprints':native_record.get('support_identities')} if a['MAPPING_RULE']=='R-TYPED-PROOF-DECLARED-SUPPORT' else None
  qualified='QUALIFIED_SUPPORT' if a['MAPPING_RULE']=='R-TYPED-PROOF-DECLARED-SUPPORT' else 'QUALIFIED_NON_SUPPORT' if 'DECLARATION' in a['SEMANTIC_CATEGORIES'] else 'UNDETERMINED'
  dep_inventory.append({'ASSOCIATION_ID':a['ASSOCIATION_ID'],'SOURCE_ID':a['SOURCE_NATIVE_IDENTITY'],'TARGET_ID':target.get('NATIVE_IDENTITY'),'TARGET_GRAPH_NODE_ID':a['TARGET_NODE'],'RELATIONSHIP_TYPE':a['RELATIONSHIP_TYPE'],'DECLARED_ROLE':a['DECLARED_ROLE'],'PROOF_CONTRACT':proof_contract,'SUPPORT_GROUP':native_group,'CURRENTNESS':a['CURRENTNESS'],'SCOPE':a['SCOPE'],'LINEAGE':a['LINEAGE'],'PROVENANCE':a['PROVENANCE'],'PROJECTION41_CLASSIFICATION':a['SEMANTIC_CATEGORIES'],'MAPPING_RULE':a['MAPPING_RULE'],'QUALIFICATION_STATUS':qualified,'QUALIFICATION_DOMAIN':'Native declared proof-support membership/current retained typed core only; NOT A15 target membership','A15_RELEVANCE':'UNDETERMINED','MISSING_VALUES':[] if qualified!='UNDETERMINED' else per_question['A15-KNOWLEDGE-K02']+per_question['A15-KNOWLEDGE-K03']+['A02'],'CASE_APPLICABILITY_GAPS':per_question['A15-KNOWLEDGE-K01'],'EXCLUSION_LIMIT':'Declaration cannot become declared proof support by incidence; an exact separate native usability constraint is not automatically irrelevant to all consumers'})
 contents={}
 for node in graph['NODES']:
  native=node.get('NATIVE_IDENTITY')
  if not isinstance(native,dict) or native.get('kind',{}).get('value')!='CONTENT_IDENTITY':continue
  key=canon(native);entry=contents.setdefault(key,{'CONTENT_IDENTITY':native,'SOURCE_IDENTITIES':[],'NATIVE_OBJECT_IDENTITIES':[],'PROOF_RELATIONSHIPS':[],'CONSUMER_ROOTS':'Unselected normative applicability','PROVENANCE_PATHS':[],'CURRENTNESS':'Domain-specific retained evidence; no target currentness inferred','SCOPE':graph['CONTEXT']['scope'],'LINEAGE':graph['CONTEXT']['lineage'],'TARGET_MEMBERSHIP':'UNDETERMINED'})
  if node['TYPE']=='SOURCE_CONTENT':entry['SOURCE_IDENTITIES'].append(node['SOURCE_PIN']);entry['PROVENANCE_PATHS'].append(node['SOURCE_PIN']['path'])
  else:entry['NATIVE_OBJECT_IDENTITIES'].append({'node_id':node['NODE_ID'],'native_identity':native,'type':node['TYPE']})
  for assoc in dep_inventory:
   if assoc['SOURCE_ID']==native and ('PROOF' in str(assoc['MAPPING_RULE'])):entry['PROOF_RELATIONSHIPS'].append(assoc['ASSOCIATION_ID'])
 catalog=[]
 for question in questions[:5]:
  q=dict(question);q['DEPENDENT_GAPS']=per_question[question['QUESTION_ID']];q['AVAILABLE_EVIDENCE']['original_bound_answer']=next(f['ORIGINAL_ANSWER'] for f in instance['FIVE_FACTS'] if f['QUESTION_ID']==question['QUESTION_ID']);q['PURPOSE']='Complete the exact missing typed discriminators, not repeat the original broad answer';q['EXPECTED_ANSWER_TYPE']=q.pop('ALLOWED_ANSWER_TYPE');catalog.append(q)
 authority_questions=[{'QUESTION_ID':'A15-AUTHORITY-IDENTITY','QUESTION':'Which actual authorized knowledge-owner/designation evidence applies to this prospective A15 normative definition? Preparation permission is not adoption.','EXPECTED_ANSWER_TYPE':'Verified actual designation/provenance reference','DEPENDENT_GAPS':['A01'],'AUTHORITY_REQUIRED':'Actual authorized qualification knowledge owner','WHEN':'Before complete content identity can bind issuing owner; no new grant created'}, {'QUESTION_ID':'A15-AUTHORITY-ADOPTION','QUESTION':'After complete content and independent qualification, does the authorized owner select the exact bounded normative subject?','EXPECTED_ANSWER_TYPE':'Actual selected decision evidence, not a proposed answer','DEPENDENT_GAPS':['A02'],'AUTHORITY_REQUIRED':'Explicit bounded normative scope adoption','WHEN':'Only after V02; not currently askable or decision-ready'}]
 recovery=[]
 for id,value,source in data_defs:recovery.append({'WORK_PACKAGE':'A15-READONLY-'+id,'SOURCE_FAMILY':source,'EXPECTED_VALUE':value,'IDENTITY_DOMAIN':'Existing native typed identity/record/provenance domains; no source target identity generated','VALIDATION':'Raw pin + exact pointer/native field equality; retained qualifiers preserved','STOP_CONDITION':'Missing/changed field/hash/domain: stop and classify data gap, do not fill normative meaning','CURRENT_SCOPE_EXECUTION':'Already recovered/indexed in this decomposition only; no native case or extended recovery'})
 return {'AUTHENTICATION':{'CONTRACT_42':'PASS','PACKAGE_43':'PASS','SEMANTIC_FACTS_BOUND':'5/5'},'GRAPH_IDENTITY':gid,'TYPED_GAPS':gaps,'GAP_DEPENDENCY_GRAPH':{'LAYERS':layers,'EDGES':[{'PREREQUISITE':dep,'BLOCKED':g['GAP_ID']} for g in gaps for dep in g['DEPENDENCIES']],'CIRCULAR':False,'UNREACHABLE':False,'REDUNDANT_SEMANTIC_QUESTIONS':[]},'ROOT_APPLICABILITY':root_inventory,'DEPENDENCY_INVENTORY':dep_inventory,'CONTENT_IDENTITIES':sorted(contents.values(),key=lambda x:canon(x['CONTENT_IDENTITY'])),'MINIMAL_SEMANTIC_ELICITATION':catalog,'SEPARATE_STAGED_AUTHORITY_REQUIREMENTS':authority_questions,'READONLY_RECOVERY_RECOMMENDATIONS':recovery,'PROJECTION_COMPARISON':{name:{'MEMBERS':len(members),'PROVABLY_INCLUDED':0,'PROVABLY_EXCLUDED':0,'UNDETERMINED':len(members),'DOMAIN':'A15 normative target membership, not retained data/native tuple membership'} for name,members in load(Q/'E2_P05_D01_A15_TARGET_SELECTION_RECONCILIATION_37/membership-semantic-reconciliation.json')['MEMBERSHIPS'].items()},'NORMATIVE_INSTANCE_COMPLETE':False,'DECISION_READY':False,'A15_DESCRIPTOR_READY':False,'A15_FULL_OUTPUT_ORACLE_READY':False,'FIRST_REMAINING_BLOCKER':per_question['A15-KNOWLEDGE-K01'][0]+': exact all-applicable owner predicate; then independent support/coverage/discovery/partition terms','TARGETS_CONSTRUCTED':False,'NATIVE_OPERATIONS_EXECUTED':False}
if __name__=='__main__':
 d=decompose()
 if '--identity' in sys.argv:print(sha(canon(d)));raise SystemExit
 emit('gap-decomposition.json',d)
 for name,key in [('typed-gap-inventory.json','TYPED_GAPS'),('root-applicability-inventory.json','ROOT_APPLICABILITY'),('qualified-dependency-inventory.json','DEPENDENCY_INVENTORY'),('content-identity-inventory.json','CONTENT_IDENTITIES'),('gap-dependency-graph.json','GAP_DEPENDENCY_GRAPH'),('minimal-elicitation-catalog.json','MINIMAL_SEMANTIC_ELICITATION'),('readonly-recovery-recommendations.json','READONLY_RECOVERY_RECOMMENDATIONS')]:emit(name,d[key])
 print('44 decomposition:',len(d['TYPED_GAPS']),'gaps;',len(d['ROOT_APPLICABILITY']),'roots;',len(d['DEPENDENCY_INVENTORY']),'associations; no target membership selected')
