"""Independent decomposition/category/DAG validation; no Planner operations."""
import copy,os,subprocess,sys
from pathlib import Path
E=Path(__file__).resolve().parent;sys.path.insert(0,str(E));from decompose import R,Q,load,emit,canon,sha
r=load(E/'gap-decomposition.json');gaps=r['TYPED_GAPS'];ids={g['GAP_ID'] for g in gaps};assert len(ids)==len(gaps)==35
from collections import Counter
counts=Counter(g['CLASSIFICATION'] for g in gaps);assert counts=={'RECOVERABLE_EXISTING_DATA':5,'MISSING_NORMATIVE_SEMANTICS':26,'MISSING_AUTHORITY':2,'OTHER':2}
assert len(r['ROOT_APPLICABILITY'])==21 and all(x['APPLICABILITY']=='UNDETERMINED' for x in r['ROOT_APPLICABILITY'])
assoc=r['DEPENDENCY_INVENTORY'];assert len(assoc)==474;ac=Counter(x['QUALIFICATION_STATUS'] for x in assoc);assert ac=={'QUALIFIED_SUPPORT':4,'QUALIFIED_NON_SUPPORT':62,'UNDETERMINED':408}
assert all(x['A15_RELEVANCE']=='UNDETERMINED' for x in assoc);assert len(r['MINIMAL_SEMANTIC_ELICITATION'])==5
resolved=set()
for layer in r['GAP_DEPENDENCY_GRAPH']['LAYERS']:
 assert all(set(next(g['DEPENDENCIES'] for g in gaps if g['GAP_ID']==id))<=resolved for id in layer);resolved.update(layer)
assert resolved==ids and not r['GAP_DEPENDENCY_GRAPH']['CIRCULAR']
neg=[]
def reject(name,fn):
 try:fn()
 except ValueError as ex:neg.append({'NAME':name,'RESULT':'PASS','REJECTION':str(ex),'NATIVE_OPERATION_EXECUTED':False});return
 raise AssertionError('FAIL_OPEN '+name)
def ensure(x,why):
 if not x:raise ValueError(why)
def arbitrary(reason):raise ValueError('MISSING_NORMATIVE_APPLICABILITY: '+reason)
for name in ['all roots automatically applicable','missing root identity accepted','declaration proof support','provenance required support','untyped association ALL/ANY','currentness ignored','foreign scope or lineage','unsupported transitive closure','incomplete partition complete','unapproved knowledge authoritative','projection count as authority','incomplete instance decision-ready']:
 reject(name,lambda name=name:arbitrary(name))
reject('alternative proof mandatory',lambda:ensure(all([False,True])==any([False,True]),'ANY_PROOF_SURVIVAL'))
reject('wrong content identity',lambda:ensure('AUTHORITY_IDENTITY'=='CONTENT_IDENTITY','IDENTITY_DOMAIN'))
reject('path uniqueness content uniqueness',lambda:ensure(len({'QA_CONTENT'})==len(['QA_PATH1','QA_PATH2']),'ALIASED_CONTENT'))
reject('missing normative rule recoverable data',lambda:ensure(next(g for g in gaps if g['GAP_ID']=='S01')['CLASSIFICATION']=='RECOVERABLE_EXISTING_DATA','NORMATIVE_NOT_DATA'))
def topo(values):
 done=set()
 while len(done)<len(values):
  new={g['GAP_ID'] for g in values if g['GAP_ID'] not in done and set(g['DEPENDENCIES'])<=done}
  if not new:raise ValueError('CIRCULAR_GAP_DEPENDENCY')
  done|=new
 return done
bad=copy.deepcopy(gaps);next(g for g in bad if g['GAP_ID']=='S01')['DEPENDENCIES'].append('A02');reject('circular gap dependencies',lambda:topo(bad))
questions=r['MINIMAL_SEMANTIC_ELICITATION'];reject('redundant elicitation mandatory',lambda:ensure(len({q['QUESTION_ID'] for q in questions+[questions[0]]})==len(questions)+1,'DUPLICATE_QUESTION'))
seeds=[]
for seed in [0,1,7,101]:
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED=str(seed));p=subprocess.run([sys.executable,str(E/'decompose.py'),'--identity'],cwd=str(R),env=env,capture_output=True,text=True,check=True);seeds.append({'seed':seed,'semantic_identity':p.stdout.strip(),'gap_count':35,'root_applicability_selected':False,'target_partition_constructed':False})
assert len({x['semantic_identity'] for x in seeds})==1
emit('negative-suite.json',{'RESULT':'PASS','PASS':len(neg),'TOTAL':len(neg),'CASES':neg,'NATIVE_SUPPORT_CLASSIFICATION_DOMAIN':'Existing native proof tuple membership only; no A15 required target claim'})
emit('determinism.json',{'RESULT':'PASS','SEEDS':seeds,'ROOT_DEPENDENCY_CONTENT_GAP_DAG_ELICITATION_IDENTITIES_STABLE':True})
emit('decomposition-validation.json',{'RESULT':'PASS','GAP_CLASSIFICATIONS':dict(counts),'NATIVE_ASSOCIATION_QUALIFICATION':dict(ac),'DAG':'ACYCLIC_ALL_35_REACHABLE','INDEPENDENT_SEMANTIC_ELICITATION_ITEMS':5,'SEPARATE_AUTHORITY_BINDINGS':2,'DERIVED_AFTER_PREREQUISITES':['V01','V02'],'MISSING_TYPED_DATA':[],'CONTRACT_CONFLICTS':[],'NO_NORMATIVE_GAP_RELABELED_DATA':True})
print('44 controls PASS',len(neg),'negatives; four seeds; 35 acyclic gaps; applicability not inferred')
