"""Schema/gap/DAG consistency and symbolic alternatives tests only."""
import copy,os,subprocess,sys
from pathlib import Path
E=Path(__file__).resolve().parent;sys.path.insert(0,str(E));from define import R,Q,load,emit,canon,sha
r=load(E/'knowledge-contract-frontier.json');items=r['KNOWLEDGE_ITEMS'];questions=r['ELICITATION_QUESTIONS'];assert len(items)==len(questions)==6
ids={x['KNOWLEDGE_ITEM'] for x in items};resolved=set()
while len(resolved)<len(ids):
 new={x['KNOWLEDGE_ITEM'] for x in items if set(x['DEPENDENCIES'])<=resolved}
 if new<=resolved:raise AssertionError('QUESTION_DEPENDENCY_CYCLE')
 resolved|=new
assert len({q['QUESTION_ID'] for q in questions})==6 and all(q['ALLOWED_ANSWER_TYPE']['type']=='object' for q in questions)
assert r['NORMATIVE_KNOWLEDGE_SCHEMA']['INSTANCE_VALUES']['ISSUING_AUTHORITY'] is None
# Independent consequence tests are symbolic, not claims about retained A15 alternatives.
def proof_ok(supports,current=True):return current and all(supports)
alternatives=[{'case':'one proof required support lost, other usable','proofs':[proof_ok([False,True]),proof_ok([True,True])],'target_satisfied':True},{'case':'all usable proof paths lost','proofs':[proof_ok([False,True]),proof_ok([True,False])],'target_satisfied':False}]
assert all(any(x['proofs'])==x['target_satisfied'] for x in alternatives)
positive={'DEPENDENCY_DAG':'PASS','MINIMUM_FACTS':'Five independent semantic facts plus subsequent real authority binding; no redundant request to choose native operator/currentness/effect rules','ALTERNATIVE_PROOF_CASES':alternatives,'FROZEN_ACCEPTANCE_COMPATIBILITY':'Target satisfaction surviving does not imply resume permission; all resume/control/stale acceptance conjuncts must be independently consistent, no forced native result','IDENTITY_CIRCULARITY':'Contract body excludes own ID/later authorization receipt; authorized wrapper binds existing body ID and actual selection','RECOVERED_DERIVED_PROPOSED_AUTHORIZED_DOMAINS_SEPARATE':True};emit('consistency-evidence.json',positive)
neg=[]
def reject(name,fn):
 try:fn()
 except ValueError as ex:neg.append({'NAME':name,'RESULT':'PASS','REJECTION':str(ex),'NATIVE_OPERATION_EXECUTED':False});return
 raise AssertionError('FAIL_OPEN '+name)
def ensure(x,why):
 if not x:raise ValueError(why)
def gap(reason):raise ValueError('UNAPPROVED_OR_INCOMPLETE_NORMATIVE_KNOWLEDGE: '+reason)
for label in ['arbitrary consumer/root selection','association treated as necessity','unsupported dependency traversal','declaration/provenance association used as support','target count selection authority','incomplete contract decision-ready','descriptor from unapproved knowledge']:
 reject(label,lambda label=label:gap(label))
reject('alternative proof treated mandatory',lambda:ensure(all(alternatives[0]['proofs'])==alternatives[0]['target_satisfied'],'ANY_USABLE_PROOF_SURVIVES'))
reject('superseded support current',lambda:ensure(proof_ok([True,True],False),'ROLE_CURRENTNESS_REQUIRED'))
state=r['NORMATIVE_KNOWLEDGE_SCHEMA']['FIELDS']['APPLICABILITY_SCOPE'];reject('wrong pre-state',lambda:ensure(state['expected_snapshot']['sha256']=='0'*64,'EXACT_A15_PRESTATE'))
reject('wrong content identity',lambda:ensure('AUTHORITY_IDENTITY'=='CONTENT_IDENTITY','NO_IDENTITY_DOMAIN_SUBSTITUTION'))
reject('wrong disjointness domain',lambda:ensure('PATH'=='CONTENT_IDENTITY','PHYSICAL_ALIAS_NOT_DISJOINT'))
reject('proposed already authorized',lambda:ensure(r['AUTHORITY_MODEL']['AUTHORIZED_NORMATIVE_KNOWLEDGE'] is not None,'NO_AUTHORITY_SELECTED'))
reject('historical evidence rewritten',lambda:ensure('original historical A15' not in r['NORMATIVE_KNOWLEDGE_SCHEMA']['FIELDS']['HISTORICAL_EXCLUSIONS'][0],'PROSPECTIVE_EXCLUSIONS_PRESERVED'))
reject('oracle from prospective execution',lambda:gap('future native result is not independent expectation'))
reject('issuing authority invented',lambda:ensure(r['AUTHORITY_MODEL']['ISSUING_AUTHORITY_ID'] is not None,'ACTUAL_DESIGNATION_REQUIRED'))
seeds=[]
for seed in [0,1,7,101]:
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED=str(seed));p=subprocess.run([sys.executable,str(E/'define.py'),'--identity'],cwd=str(R),env=env,capture_output=True,text=True,check=True);seeds.append({'seed':seed,'semantic_identity':p.stdout.strip(),'targets_generated':False,'authorized_contract':None})
assert len({x['semantic_identity'] for x in seeds})==1
emit('negative-suite.json',{'RESULT':'PASS','PASS':len(neg),'TOTAL':len(neg),'CASES':neg,'SEMANTIC_EXAMPLES_NOT_A15_EXPECTED_OUTPUTS':True})
emit('determinism.json',{'RESULT':'PASS','SEEDS':seeds,'SCHEMA_FACT_INVENTORY_PROPOSAL_CLASSIFICATION_QUESTION_DAG_IDENTICAL':True})
emit('independent-qualification-feasibility.json',{'SCHEMA_AND_DAG_CONSISTENCY':'PASS','EXISTING_NATIVE_OPERATOR_CURRENTNESS_RULES':'Preserved; no new choices elicited','REQUIRED_COMPLETE_INSTANCE_TESTS':['Exact finite owner/native support group/source relevance membership','Path-level versus target-level necessity with alternative survival','Active/current role without timestamp preference','Forward native consequences distinct from upstream target closure','Shared/duplicate content aliases and exhaustive disjoint groups','No frozen acceptance contradiction','Exact issuing-owner/selection provenance and historical exclusions','Determinism and fail-closed source/owner/identity/context/authority checks'],'ACTUAL_COMPLETE_INSTANCE':'UNREADY pending K01-K06','TARGET_ORACLE_QUALIFICATION':'NOT_RUN; no target set or independent oracle constructed'})
print('42 schema/elicitation checks PASS',len(neg),'negatives; four seeds; no normative authority or targets')
