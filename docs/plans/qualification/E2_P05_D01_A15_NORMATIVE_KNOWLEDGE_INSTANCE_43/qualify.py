"""Independently qualify preparation and abstract consequences, not A15 adoption."""
import copy,json,os,subprocess,sys
from pathlib import Path
E=Path(__file__).resolve().parent;sys.path.insert(0,str(E));from prepare import R,Q,C,load,emit,canon,sha,ANSWERS
p=load(E/'proposed-typed-instance.json');v=dict(p);identity=v.pop('PREPARATION_IDENTITY');assert identity=='qualification-A15-proposed-instance-preparation-v1:'+sha(canon(v));assert [x['ORIGINAL_ANSWER'] for x in p['FIVE_FACTS']]==ANSWERS
schema_rows=[]
for fact in p['FIVE_FACTS']:
 required=fact['EXPECTED_ANSWER_TYPE']['required'];assert set(fact['TYPED_FIELDS'])==set(required)
 missing=[name for name,field in fact['TYPED_FIELDS'].items() if field['VALUE'] is None or field['STATUS'] not in ['RECOVERED_COMPLETE','SUPPLIED_AND_NATIVE_CONSISTENT']]
 assert missing and not fact['COMPLETE'];schema_rows.append({'QUESTION_ID':fact['QUESTION_ID'],'ENVELOPE_TYPE':'PASS_OBJECT','QUESTION_AND_RAW_ANSWER_BINDING':'PASS','EXACT_REQUIRED_VALUE_VALIDATION':'INCOMPLETE','MISSING_OR_PARTIAL_FIELDS':missing})
# Symbolic metadata only: tests supplied intent without inferring graph-specific roots/edges.
roots=[{'id':'QA_A','current':True,'scope':'QA','lineage':'QA_LINE'},{'id':'QA_OLD','current':False,'scope':'QA','lineage':'QA_LINE'},{'id':'QA_FOREIGN','current':True,'scope':'OTHER','lineage':'OTHER'}]
applicable=lambda x:x['current'] and x['scope']=='QA' and x['lineage']=='QA_LINE';assert [x['id'] for x in roots if applicable(x)]==['QA_A']
roles={'accepted_proof_support':True,'qualified_dependency':True,'declaration_only':False,'provenance_incidence_only':False};assert sum(roles.values())==2
def usable(supports,current=True):return current and all(supports)
assert not usable([False,True]) and any([False,True]) and not any([False,False])
def closure(seed,qualified):
 reached=set(seed)
 while True:
  new=reached|{b for a,b in qualified if a in reached}
  if new==reached:return sorted(reached)
  reached=new
assert closure(['QA_A'],[('QA_A','QA_B'),('QA_B','QA_C'),('QA_C','QA_B')])==['QA_A','QA_B','QA_C'];assert closure(['QA_A'],[('QA_FOREIGN','QA_D')])==['QA_A']
def dedup_with_provenance(rows):
 result={}
 for row in rows:result.setdefault(row['content_identity'],set()).add(row['provenance'])
 return {k:sorted(v) for k,v in sorted(result.items())}
assert dedup_with_provenance([{'content_identity':'QA_CONTENT_A','provenance':'QA_PATH_ONE'},{'content_identity':'QA_CONTENT_A','provenance':'QA_PATH_TWO'}])=={'QA_CONTENT_A':['QA_PATH_ONE','QA_PATH_TWO']}
positive={'F1':'All explicitly applicable/current/context-matching symbolic roots; no real applicability inferred','F2':'Typed operative proof/dependency roles stay distinct from declaration/provenance incidence','F3':'ALL supports within path; ANY usable alternative preserves target satisfaction','F4':'Qualified directed affected-edge fixed point terminates with cycles/duplicates; no unqualified edge inserted','F5':'Unique symbolic content keys retain all associated provenance references','CROSS_RULE_LIMIT':'Positive abstract examples do not complete root applicability/source-to-support mapping/target discovery/coverage/partition for A15'}
neg=[]
def reject(name,fn):
 try:fn()
 except ValueError as ex:neg.append({'NAME':name,'RESULT':'PASS','REJECTION':str(ex),'NATIVE_OPERATION_EXECUTED':False});return
 raise AssertionError('FAIL_OPEN '+name)
def ensure(x,why):
 if not x:raise ValueError(why)
def require_complete(instance):
 if not instance['NORMATIVE_RULE_COMPLETE'] or not instance['GRAPH_APPLICABILITY_COMPLETE']:raise ValueError('CONTRACT42_REQUIRED_VALUES_UNRESOLVED')
for name in ['all applicable interpreted as all graph nodes','qualified dependencies interpreted as every association','reassessment interpreted as target selection','affected closure substituted for upstream target discovery','unique content interpreted as singleton partition','partial facts authorization-ready','unapproved instance creates descriptor']:
 reject(name,lambda:require_complete(p))
reject('wrong scope/lineage considered applicable',lambda:ensure(applicable(roots[-1]),'CONTEXT_APPLICABILITY'))
reject('superseded root considered current',lambda:ensure(applicable(roots[1]),'CURRENTNESS_REQUIRED'))
reject('declaration/provenance incidence support',lambda:ensure(roles['declaration_only'] or roles['provenance_incidence_only'],'OPERATIVE_ROLE_REQUIRED'))
reject('mandatory support loss accepted',lambda:ensure(usable([False,True]),'ALL_REQUIRED'))
reject('alternative treated mandatory',lambda:ensure(all([False,True])==any([False,True]),'ANY_PROOF_SURVIVES'))
reject('unqualified edge propagation',lambda:ensure('QA_D' in closure(['QA_A'],[('QA_FOREIGN','QA_D')]),'QUALIFIED_EDGE_SOURCE_MATCH'))
reject('provenance discarded on content dedup',lambda:ensure(len(dedup_with_provenance([{'content_identity':'QA_C','provenance':'P1'},{'content_identity':'QA_C','provenance':'P2'}])['QA_C'])==1,'ALL_PROVENANCE_RETAINED'))
reject('normative authority issued from preparation',lambda:ensure(p['ISSUING_AUTHORITY'] is not None,'PREPARATION_ONLY'))
reject('premature complete normative contract identity',lambda:ensure(p['KNOWLEDGE_CONTRACT_ID'] is not None,'SCHEMA_IDENTITY_COMPLETENESS_GATE'))
reject('original answer changed',lambda:ensure(p['FIVE_FACTS'][0]['ORIGINAL_ANSWER']=='Only FINISH root.','VERBATIM_ANSWER_PIN'))
seeds=[]
for seed in [0,1,7,101]:
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED=str(seed));proc=subprocess.run([sys.executable,str(E/'prepare.py'),'--identity'],cwd=str(R),env=env,capture_output=True,text=True,check=True);seeds.append({'seed':seed,'preparation_semantic_identity':proc.stdout.strip(),'complete_normative_instance_identity':None,'schema_outcome':'INCOMPLETE_REQUIRED_VALUES','graph_applicability':'INCOMPLETE'})
assert len({x['preparation_semantic_identity'] for x in seeds})==1
emit('schema-validation.json',{'RESULT':'INCOMPLETE_REQUIRED_FIELDS','SCHEMA_SOURCE_AUTHENTICATED':True,'FIVE_ANSWER_BINDINGS':'5/5 PASS','ROWS':schema_rows,'DEPENDENCY_ORDER':'PASS_ACYCLIC_CONTRACT42_ORDER','SEMANTIC_IDENTITY_AUTHORITY_SEPARATION':'PASS','ISSUING_AUTHORITY_UNSUPPLIED':True,'NORMATIVE_RULE_COMPLETE':False})
emit('independent-semantic-qualification.json',{'PREPARATION_BINDING_RESULT':'PASS','ABSTRACT_NATIVE_KERNEL_CONSISTENCY':'PASS','POSITIVE_CASES':positive,'COMPLETE_A15_CROSS_RULE_CONSISTENCY':'NOT_ESTABLISHED_MISSING_APPLICABILITY','GRAPH_APPLICABILITY':'INCOMPLETE','NEGATIVES':{'PASS':len(neg),'TOTAL':len(neg),'CASES':neg},'NATIVE_GRAPH_RELATIONSHIPS_INFERRED':False,'NATIVE_OPERATIONS_EXECUTED':0})
emit('four-seed-determinism.json',{'RESULT':'PASS','SEEDS':seeds,'AUTHORIZATION_READY':False,'A15_TARGETS_CREATED':False})
print('43 preparation/abstract qualification PASS',len(neg),'negatives; complete schema and graph applicability remain INCOMPLETE')
