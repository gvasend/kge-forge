"""Bind supplied answers without completing/authorizing their missing semantics."""
import json,hashlib,sys
from pathlib import Path
R=Path('/home/gvasend/app/kge-forge');E=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification';C=Q/'E2_P05_D01_A15_NORMATIVE_KNOWLEDGE_CONTRACT_42'
def load(p):return json.loads(Path(p).read_bytes())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(x):return hashlib.sha256(x).hexdigest()
def pin(p):return {'path':str(p.relative_to(R)),'raw_sha256':sha(p.read_bytes())}
def emit(n,x):(E/n).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
ANSWERS=['All applicable consumer/roots.','Accepted proof support plus qualified dependencies.','Reevaluate all usable proofs using native `ALL`/`ANY` semantics.','Transitive affected closure until a fixed point.','Globally unique content identities with preserved provenance relationships.']
def prepare():
 index=load(C/'evidence-index.json')
 for p,h in index['FILES'].items():
  if sha((R/p).read_bytes())!=h:raise ValueError('BLOCKED_SOURCE_CONTRACT:'+p)
 schema=load(C/'normative-knowledge-schema.json');questions=load(C/'future-elicitation-questions.json');knowledge=load(C/'normative-knowledge-inventory.json');assert len(questions)==len(knowledge)==6
 ids={k['KNOWLEDGE_ITEM'] for k in knowledge};seen=set();order=[]
 while seen!=ids:
  new=sorted(k['KNOWLEDGE_ITEM'] for k in knowledge if k['KNOWLEDGE_ITEM'] not in seen and set(k['DEPENDENCIES'])<=seen)
  if not new:raise ValueError('CIRCULAR_CONTRACT_42_DEPENDENCIES')
  order.extend(new);seen.update(new)
 assert schema['FIELDS']['KNOWLEDGE_CONTRACT_ID'].find('no instance ID before complete')>=0
 bound=[];missing=[]
 for i,(answer,question,item) in enumerate(zip(ANSWERS,questions[:5],knowledge[:5]),1):
  required=question['ALLOWED_ANSWER_TYPE']['required'];fields={field:{'VALUE':None,'STATUS':'UNRESOLVED','REASON':'Not specified by supplied answer; no default invented'} for field in required}
  def setfield(name,value,status='PARTIAL_SUPPLIED',why='Exact supplied meaning only; remaining discriminator unresolved'):
   fields[name]={'VALUE':value,'STATUS':status,'REASON':why}
  if i==1:
   setfield('exact_owner_pairs_or_complete_finite_applicability_rule',{'OWNERSHIP_FORM':'ALL_APPLICABLE','APPLICABILITY_PREDICATE':None,'EXACT_NATIVE_OWNER_IDENTITIES':None})
   setfield('state_scope_lineage_generation',schema['FIELDS']['APPLICABILITY_SCOPE'],'RECOVERED_COMPLETE','Exact sealed Contract42 applicability, not a newly chosen owner set')
   setfield('evidence_pins',{'schema':pin(C/'normative-knowledge-schema.json'),'questions':pin(C/'future-elicitation-questions.json')},'RECOVERED_COMPLETE','Preparation scope references only; no ownership authority')
  elif i==2:
   setfield('typed_owner_support_role_binding_table',{'SUPPORT_CLASSES':['ACCEPTED_PROOF_SUPPORT','QUALIFIED_DEPENDENCIES'],'EXACT_NATIVE_ROLE_BINDINGS':None})
   setfield('currentness_rule_references',{'native_kernel':pin(Q/'E2_P05_D01_A15_SUPPORT_SEMANTICS_CONTRACT_40/rule-provenance.json')},'RECOVERED_COMPLETE','Reuse native currentness rules; association-specific applicability still unbound')
   setfield('declaration_provenance_exclusions','Proof support/qualified dependencies do not become declaration/provenance-only incidence; exact discriminating role predicate absent')
   setfield('evidence_pins',{'typed_core':pin(Q/'E2_P05_D01_A15_GRAPH_SEMANTIC_PROJECTION_41/existing-native-proof-correspondence.json'),'classification':pin(Q/'E2_P05_D01_A15_GRAPH_SEMANTIC_PROJECTION_41/association-classification.json')},'RECOVERED_COMPLETE','Evidence does not establish all-owner relevance')
  elif i==3:
   setfield('alternative_survival_effect_expectations','All usable proofs reassessed; a surviving applicable proof can preserve target satisfaction','SUPPLIED_AND_NATIVE_CONSISTENT','Consequence only, not selection/coverage or scalar resume permission')
   setfield('native_AND_ANY_compatibility',{'PER_PROOF':'ALL declared usable supports','PER_TARGET':'ANY applicable usable proof'},'RECOVERED_COMPLETE','Exact native kernel preserved')
   setfield('proof_path_vs_target_vs_group_coverage_standard',{'REEVALUATION':'ALL_USABLE_PROOFS','INVALIDATION_COVERAGE_STANDARD':None})
   setfield('amendment_exclusions',schema['FIELDS']['HISTORICAL_EXCLUSIONS'],'RECOVERED_COMPLETE','Preparation remains prospective/unapproved')
  elif i==4:
   setfield('closure_mode','TRANSITIVE_AFFECTED_EFFECT_CLOSURE_TO_FIXED_POINT','SUPPLIED_EFFECT_RULE_ONLY','Contract42 K04 target discovery still requires separately defined direction/eligible edges/start; no substitution')
   setfield('termination_cycle_duplicate_shared_support_rules',{'TERMINATION':'FIXED_POINT','NATIVE_FINITE_EFFECT_RULES_PRESERVED':True,'EXACT_TARGET_DISCOVERY_HANDLING':None})
   setfield('exact_specification_reference',{'native_effect_kernel':pin(Q/'E2_P05_D01_A15_SUPPORT_SEMANTICS_CONTRACT_40/shared-semantics-recovery.json')},'RECOVERED_COMPLETE','This reference covers native effects, not missing target-discovery normative rule')
  elif i==5:
   setfield('content_identity_domain','Full CONTENT_IDENTITY kind/namespace/hash','SUPPLIED_AND_NATIVE_CONSISTENT','Content rather than paths/authority/event identity')
   setfield('content_alias_handling',{'IDENTITY_MEMBERSHIP':'GLOBALLY_UNIQUE_CONTENT_IDENTITIES','PROVENANCE':'PRESERVE_ALL_RELATIONSHIPS'},'SUPPLIED_AND_NATIVE_CONSISTENT','No provenance discarded during metadata deduplication; no target partition constructed')
  gaps=[field for field,value in fields.items() if value['STATUS'] not in ['RECOVERED_COMPLETE','SUPPLIED_AND_NATIVE_CONSISTENT']]
  missing.append({'QUESTION_ID':question['QUESTION_ID'],'UNRESOLVED_REQUIRED_FIELDS':gaps,'COMPLETE_REQUIRED_ANSWER':False})
  bound.append({'FACT_NUMBER':i,'QUESTION_ID':question['QUESTION_ID'],'KNOWLEDGE_ITEM':item['KNOWLEDGE_ITEM'],'ORIGINAL_ANSWER':answer,'ANSWER_SOURCE':'Human work-package 43 Phase 2, verbatim; preparation/independent qualification only','ANSWER_BINDING':'BOUND_NOT_ADOPTED','EXPECTED_ANSWER_TYPE':question['ALLOWED_ANSWER_TYPE'],'TYPED_FIELDS':fields,'COMPLETE':False})
 proposal={'SCHEMA':'A15-PROPOSED-NORMATIVE-INSTANCE-PREPARATION-43','VERSION':1,'STATUS':'PROPOSED — NOT AUTHORIZED; incomplete typed answer preparation','CONTRACT_42_SCHEMA':pin(C/'normative-knowledge-schema.json'),'CONTRACT_42_QUESTIONS':pin(C/'future-elicitation-questions.json'),'CONTRACT_42_EVIDENCE_INDEX':pin(C/'evidence-index.json'),'APPLICABILITY_PRECOMMITMENT':schema['FIELDS']['APPLICABILITY_SCOPE'],'FIVE_FACTS':bound,'SEMANTIC_FACTS_BOUND':'5/5','DEPENDENCY_ORDER':order,'KNOWLEDGE_CONTRACT_ID':None,'NORMATIVE_INSTANCE_IDENTITY':None,'ISSUING_AUTHORITY':None,'K06_AUTHORITY_BINDING':None,'AUTHORITY_STATE':'Preparation allowed; no adoption/issuance/amendment/execution','HISTORICAL_EXCLUSIONS':schema['FIELDS']['HISTORICAL_EXCLUSIONS'],'NORMATIVE_RULE_COMPLETE':False,'GRAPH_APPLICABILITY_COMPLETE':False,'MISSING_FIELDS':missing,'TARGETS_CONSTRUCTED':False,'IDENTITY_RULE':'Contract42 forbids complete instance identity before semantics complete. Separate preparation-evidence identity binds these raw answers/question IDs/known fields/gaps, excluding itself and future authority receipt. It is not a normative contract identity.'}
 proposal['PREPARATION_IDENTITY']='qualification-A15-proposed-instance-preparation-v1:'+sha(canon(proposal))
 return proposal
if __name__=='__main__':
 p=prepare()
 if '--identity' in sys.argv:print(p['PREPARATION_IDENTITY']);raise SystemExit
 emit('proposed-typed-instance.json',p);emit('contract-42-authentication.json',{'RESULT':'PASS','INDEX':p['CONTRACT_42_EVIDENCE_INDEX'],'SCHEMA':p['CONTRACT_42_SCHEMA'],'QUESTIONS':p['CONTRACT_42_QUESTIONS'],'HASHES_VERIFIED':len(load(C/'evidence-index.json')['FILES']),'DEPENDENCY_ORDER':p['DEPENDENCY_ORDER'],'PREPARATION_SCOPE_AUTHENTICATED':True,'NORMATIVE_ADOPTION_AUTHORITY':False});print('Contract42 authenticated; 5/5 answers bound; exact required fields incomplete; preparation identity only')
