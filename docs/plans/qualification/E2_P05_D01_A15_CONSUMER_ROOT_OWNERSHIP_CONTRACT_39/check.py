"""Static proposal/authority/invariant controls only."""
import copy,os,subprocess,sys
from pathlib import Path
E=Path(__file__).resolve().parent;sys.path.insert(0,str(E));from evaluate import R,Q,load,emit,canon,sha
r=load(E/'ownership-model-evaluation.json');models=r['PROPOSED_MODELS'];assert len(models)==3 and not r['UNIQUE_CONTRACT_DERIVABLE']
for m in models:
 v=dict(m);identity=v.pop('PROPOSAL_IDENTITY');assert identity=='qualification-A15-owner-model-v1:'+sha(canon(v));assert not m['CONTRACT_COMPLETE'] and not m['DECISION_OPTION_READY'] and 'NOT AUTHORIZED' in m['STATUS']
expected={m['MODEL']:m for m in models};neg=[]
def validate(candidate):
 if candidate!=expected[candidate['MODEL']]:raise ValueError('PROPOSED_RULE_SCOPE_IDENTITY_OR_AUTHORITY_CHANGED')
 return True
for m in models:assert validate(m)
def reject(name,fn):
 try:fn()
 except ValueError as ex:neg.append({'NAME':name,'RESULT':'PASS','REJECTION':str(ex),'NATIVE_OPERATION_EXECUTED':False});return
 raise AssertionError('FAIL_OPEN '+name)
changes=[('arbitrary single-root selection','SINGLE_ROOT','OWNERSHIP_PREDICATE','FIRST_ROOT'),('all roots without applicability','ALL_APPLICABLE','OWNERSHIP_PREDICATE','EVERY_RECORD'),('named subset without membership authority','NAMED_SUBSET','ROOT_SELECTION_AUTHORITY','Already historically authorized'),('association treated as required support','SINGLE_ROOT','REQUIRED_SUPPORT_PREDICATE','Any graph edge'),('declaration-only reference treated as necessary','ALL_APPLICABLE','REQUIRED_SUPPORT_PREDICATE','Any source_additions pin'),('provenance-only incidence treated as target','NAMED_SUBSET','REQUIRED_SUPPORT_PREDICATE','All Provenance'),('wrong dependency direction','SINGLE_ROOT','TARGET_CLOSURE','Effect direction reversed'),('unsupported transitive closure','ALL_APPLICABLE','TARGET_CLOSURE','All reachable graph sources'),('incorrect disjointness domain','NAMED_SUBSET','DISJOINT_PARTITION','Different physical paths'),('historical state substituted','SINGLE_ROOT','PRESTATE','Historical equivalent'),('candidate count used as evidence','ALL_APPLICABLE','ROOT_SELECTION_AUTHORITY','Select 49'),('proposed rule labeled historical','SINGLE_ROOT','STATUS','RECOVERED_HISTORICAL'),('scope amendment applied without authorization','NAMED_SUBSET','EXECUTION_AUTHORITY_ISSUED',True),('incomplete candidate decision-ready','ALL_APPLICABLE','DECISION_OPTION_READY',True),('oracle from unapproved targets','SINGLE_ROOT','PROOF_CONTROL_RESUME','Actual prospective result becomes expected oracle')]
for name,model,field,value in changes:
 bad=copy.deepcopy(expected[model]);bad[field]=value;reject(name,lambda bad=bad:validate(bad))
for m in models:
 if m['REQUIRED_SUPPORT_PREDICATE']['STATUS']!='UNRESOLVED' or m['TARGET_CLOSURE']['STATUS']!='UNRESOLVED' or m['DISJOINT_PARTITION']['STATUS']!='UNRESOLVED':raise AssertionError('Unknown terms hidden')
seeds=[]
for seed in [0,1,7,101]:
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED=str(seed));p=subprocess.run([sys.executable,str(E/'evaluate.py'),'--identity'],cwd=str(R),env=env,capture_output=True,text=True,check=True);seeds.append({'seed':seed,'semantic_hash':p.stdout.strip(),'model_selected':None,'target_set_selected':None})
assert len({x['semantic_hash'] for x in seeds})==1
emit('negative-suite.json',{'RESULT':'PASS','PASS':len(neg),'TOTAL':len(neg),'CASES':neg,'INVARIANT_STATUS':'No conditional representation model rejected merely for narrowing/broadening explicit prospective scope; unauthorized/underdefined adoption rejected'})
emit('determinism.json',{'RESULT':'PASS','SEEDS':seeds,'OWNER_INVENTORY_MODEL_CLASSIFICATION_NORMATIVE_GAPS_IDENTICAL':True,'SELECTED_TARGETS':None})
print('39 proposal checks PASS',len(neg),'negatives; four seeds; no ownership model selected')
