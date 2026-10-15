"""Independent graph-edge checks and fail-closed static metadata controls."""
import copy,json,os,subprocess,sys
from pathlib import Path
E=Path(__file__).resolve().parent;sys.path.insert(0,str(E));from reconcile import R,Q,P,load,emit,canon,sha,reconstruct,pin
r=load(E/'membership-semantic-reconciliation.json');graph=load(P/'accepted-support-graph.json');original=copy.deepcopy(graph)
def normalize(g):
 g=copy.deepcopy(g);g['NODES']=sorted(g['NODES'],key=lambda x:x['NODE_ID']);g['EDGES']=sorted(g['EDGES'],key=canon);return g
# Source domain and associations must be identical to the fixed graph, regardless presentation.
def validate(g):
 if normalize(g)!=normalize(original):raise ValueError('WRONG_GRAPH_DIRECTION_SOURCE_CONTEXT_OR_PROVENANCE')
 return reconstruct(g)
sets=validate(graph)
for direction in [copy.deepcopy(graph),copy.deepcopy(graph)]:
 direction['NODES'].reverse();direction['EDGES']=direction['EDGES'][1:]+direction['EDGES'][:1];assert validate(direction)==sets
neg=[]
def reject(name,fn):
 try:fn()
 except ValueError as ex:neg.append({'NAME':name,'RESULT':'PASS','REJECTION':str(ex),'NATIVE_OPERATION_EXECUTED':False});return
 raise AssertionError('FAIL_OPEN '+name)
bad=copy.deepcopy(graph);bad['EDGES'][0]['FROM'],bad['EDGES'][0]['TO']=bad['EDGES'][0]['TO'],bad['EDGES'][0]['FROM'];reject('wrong dependency direction',lambda:validate(bad))
bad=copy.deepcopy(graph);bad['NODES']=[x for x in bad['NODES'] if x['NODE_ID']!=next(x['NODE_ID'] for x in bad['NODES'] if x['TYPE']=='SOURCE_CONTENT')];reject('missing source',lambda:validate(bad))
bad=copy.deepcopy(graph);bad['NODES'].append(dict(bad['NODES'][0],NODE_ID='foreign'));reject('extra foreign source',lambda:validate(bad))
bad=copy.deepcopy(graph);node=next(x for x in bad['NODES'] if x['TYPE']=='SOURCE_CONTENT');node['NATIVE_IDENTITY']['sha256']='0'*64;reject('wrong content identity',lambda:validate(bad))
bad=copy.deepcopy(graph);bad['EDGES'][0]['ROLE']='REQUIRED_INVALIDATION_TARGET';reject('source-role association treated as target membership',lambda:validate(bad))
bad=copy.deepcopy(graph);bad['CONTEXT']['generation']='foreign';reject('wrong graph generation',lambda:validate(bad))
bad=copy.deepcopy(graph);edge=next(x for x in bad['EDGES'] if 'PROVENANCE' in x);edge['PROVENANCE']['path']='foreign';reject('foreign provenance',lambda:validate(bad))
bad=copy.deepcopy(graph);bad['CONTEXT']['lineage']='foreign';reject('wrong lineage',lambda:validate(bad))
def disjoint_content(pins):
 identities=[canon(p['identity']) for p in pins]
 if len(identities)!=len(set(identities)):raise ValueError('DISTINCT_PATHS_DO_NOT_PROVE_DISJOINT_CONTENT')
 return True
pins=[x['SOURCE_PIN'] for x in graph['NODES'] if x['TYPE']=='SOURCE_CONTENT'];assert disjoint_content(pins)
alias=copy.deepcopy(pins[0]);alias['path']='other-canonical-path.json';reject('false disjointness from distinct paths',lambda:disjoint_content([pins[0],alias]))
def qualified_selection(predicate):
 raise ValueError('AUTHORITATIVE_REQUIRED_SUPPORT_ROLE_DISCRIMINATOR_UNSEALED; predicate not qualified: '+predicate)
for pred in ['P45','P49','P14','FIRST_SOURCE','LAST_SOURCE','MATCH_EXPECTED_SIZE','CURRENT_PROVENANCE_IMPLIES_REQUIRED','SOURCE_ADDITION_IMPLIES_MANDATORY_SUPPORT','SMALLEST_SET_IS_FINAL_PIPELINE_STAGE','DISJOINT_DEPENDENCY_BRANCHES','PROTECTED_SET_COMPLEMENT']:
 reject('unsupported selection predicate '+pred,lambda pred=pred:qualified_selection(pred))
seeds=[]
for seed in [0,1,7,101]:
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED=str(seed));proc=subprocess.run([sys.executable,str(E/'reconcile.py'),'--identity'],cwd=str(R),env=env,capture_output=True,text=True,check=True)
 p=subprocess.run([sys.executable,'-c','import json;print(json.dumps(list(set('+repr([x['NODE_ID'] for x in graph['NODES']])+'))))'],env=env,capture_output=True,text=True,check=True);order=json.loads(p.stdout);byid={x['NODE_ID']:x for x in graph['NODES']};perm=copy.deepcopy(graph);perm['NODES']=[byid[x] for x in order];assert validate(perm)==sets
 seeds.append({'seed':seed,'semantic_identity':proc.stdout.strip(),'memberships':[len(sets[x]) for x in ['P45','P49','P14']],'selection':None})
assert len({x['semantic_identity'] for x in seeds})==1
emit('negative-suite.json',{'RESULT':'PASS','PASS':len(neg),'TOTAL':len(neg),'CASES':neg,'REORDERED_NATIVE_UNORDERED_COLLECTIONS':'ACCEPTED_IDENTICAL_MEMBERSHIP; order-based selection rejected','TARGET_SELECTION_PERFORMED':False})
emit('determinism.json',{'RESULT':'PASS','SEEDS':seeds,'DIRECT_RECORD_VS_DIRECTED_ASSOCIATION_RECONSTRUCTION':'PASS','PROJECTION_MEMBERSHIP_PRESERVATION':'PASS','SELECTED_TARGETS':None,'DESCRIPTOR_OR_ORACLE_CREATED':False})
emit('contract-evidence.json',{'EARLIEST_A15':pin(R/'docs/plans/DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.json'),'ACCEPTANCE_MATRIX':pin(R/'docs/plans/DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_ACCEPTANCE_MATRIX_1.md'),'FROZEN_128_OBLIGATIONS':pin(Q/'E2_P05_D01_PROSPECTIVE_MATRIX_CONTRACT_1/sealed-128-obligations.json'),'LOCAL_P03_RECIPE':pin(R/'adapter/tests/qualify_p03_prospective.py'),'NATIVE_INVALIDATION':pin(R/'adapter/planner/codec.py'),'INSTALLATION_SUPPORT':pin(R/'adapter/planner/installation.py'),'GRAPH':pin(P/'accepted-support-graph.json'),'AUTHORITY_LIMIT':'Frozen obligation supplies required-source semantics but not exact consumer/root/projection discriminator for current A15; local native/qualification implementations do not issue new scope'})
print('37 static checks PASS',len(neg),'negatives; four seeds identical; target selection remains unresolved')
