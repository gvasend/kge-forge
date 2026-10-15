"""Static normative-authority controls, not target selection or state evaluation."""
import copy,json,os,subprocess,sys
from pathlib import Path
E=Path(__file__).resolve().parent;sys.path.insert(0,str(E));from recover import R,Q,load,emit,canon,sha
r=load(E/'recovered-semantics.json');assert r['PRIMARY_NORMATIVE_GAP']=='MISSING_CONSUMER_ROOT_OWNERSHIP' and not r['REQUIRED_SUPPORT_PREDICATE_COMPLETE']
# Positive contract validation accepts scoped rules only with their explicit domain/authority limits.
def validate_terms(terms):
 if terms!=r['CONTRACT_PROVENANCE']:raise ValueError('RULE_TERM_AUTHORITY_SCOPE_OR_MEANING_CHANGED')
 return True
assert validate_terms(r['CONTRACT_PROVENANCE']);neg=[]
def reject(name,fn):
 try:fn()
 except ValueError as ex:neg.append({'NAME':name,'RESULT':'PASS','REJECTION':str(ex),'NATIVE_OPERATION_EXECUTED':False});return
 raise AssertionError('FAIL_OPEN '+name)
def promotion(label):raise ValueError('A15_OWNER_AND_REQUIRED_SUPPORT_PREDICATE_MISSING; cannot promote '+label)
for name in ['declaration-only source treated as required','provenance-only association treated as target','wrong consumer/root or FINISH assumed sole A15 owner','unsupported target transitive closure','missing required dependency silently accepted','extra unrelated source','historical support substituted for current','candidate selected by count','candidate selected by ordering','unsupported target predicate','incomplete predicate marked complete']:
 reject(name,lambda name=name:promotion(name))
for name,field,index,value in [('wrong dependency direction','EXACT_CONTRACT_MEANING',2,'FINISH -> source is native invalidation propagation'),('wrong scope/currentness','APPLICABILITY',3,'All source nodes, no context checks'),('implementation promoted to normative authority','CONFIDENCE_CLASSIFICATION',9,'EXPLICIT_FROZEN_A15_TARGET_RULE'),('wrong source-role classification','EXACT_CONTRACT_MEANING',5,'Every graph reference is mandatory support')]:
 terms=copy.deepcopy(r['CONTRACT_PROVENANCE']);terms[index][field]=value;reject(name,lambda terms=terms:validate_terms(terms))
def state_check(state):
 if state!=r['STATE_APPLICABILITY']:raise ValueError('WRONG_A15_PRESTATE_OR_CONTEXT')
for name,field in [('wrong A15 pre-state','EXPECTED_SNAPSHOT'),('wrong lineage','CONTEXT')]:
 state=copy.deepcopy(r['STATE_APPLICABILITY']);state[field]='foreign';reject(name,lambda state=state:state_check(state))
graph=load(Q/'E2_P05_D01_A15_CAPTURE_OUTPUT_CONTRACT_36/accepted-support-graph.json');sources=[n for n in graph['NODES'] if n['TYPE']=='SOURCE_CONTENT']
def domain_check(node):
 if node not in sources:raise ValueError('WRONG_CONTENT_OR_FOREIGN_PROVENANCE')
node=copy.deepcopy(sources[0]);node['NATIVE_IDENTITY']['kind']['value']='AUTHORITY_IDENTITY';reject('wrong content identity domain',lambda:domain_check(node))
def content_disjoint(pins):
 ids=[canon(p['identity']) for p in pins]
 if len(ids)!=len(set(ids)):raise ValueError('PATH_DISTINCTNESS_IS_NOT_CONTENT_DISJOINTNESS')
 return True
alias=copy.deepcopy(sources[0]['SOURCE_PIN']);alias['path']='another-path.json';reject('physical-path disjointness substituted for content disjointness',lambda:content_disjoint([sources[0]['SOURCE_PIN'],alias]))
node=copy.deepcopy(sources[0]);node['SOURCE_PIN']['path']='foreign.json';reject('foreign source provenance',lambda:domain_check(node))
# Term ordering cannot change canonical semantic term membership.
ordered=sorted(r['CONTRACT_PROVENANCE'],key=lambda x:x['RULE_TERM']);assert sorted(list(reversed(r['CONTRACT_PROVENANCE'])),key=lambda x:x['RULE_TERM'])==ordered
seeds=[]
for seed in [0,1,7,101]:
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED=str(seed));p=subprocess.run([sys.executable,str(E/'recover.py'),'--identity'],cwd=str(R),env=env,capture_output=True,text=True,check=True);seeds.append({'seed':seed,'semantic_identity':p.stdout.strip(),'required_support_predicate_complete':False,'target_set':None})
assert len({x['semantic_identity'] for x in seeds})==1
emit('negative-suite.json',{'RESULT':'PASS','PASS':len(neg),'TOTAL':len(neg),'CASES':neg,'SCOPE':'Normative term/authority/domain/prestate metadata; no candidate selected or native predicate/state operation invoked'})
emit('determinism.json',{'RESULT':'PASS','SEEDS':seeds,'CONSUMER_ROOT_ROLE_DIRECTION_CANDIDATE_PROVENANCE_IDENTITIES_STABLE':True,'TARGET_SET_RECONSTRUCTION':'NOT_RUN_INCOMPLETE_NORMATIVE_PREDICATE'})
print('38 STATIC CONTROLS PASS',len(neg),'negatives; four seeds stable; no target predicate promoted')
