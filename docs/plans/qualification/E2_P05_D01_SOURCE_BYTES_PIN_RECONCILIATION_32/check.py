"""Static metadata negatives and reconstruction; no native source loading operation."""
import copy,json,os,subprocess,sys,hashlib
from pathlib import Path
E=Path(__file__).resolve().parent;sys.path.insert(0,str(E));from reconcile import recover,canon,sha,emit,R,Q,DISPATCH,CAP,FROZEN,pin,load
r=recover();members=r['MEMBERS'];expected={x['SOURCE_ID']:x for x in members};prefixes=r['PREFIXES']
def singular(collection):
 eligible=[x for x in collection if x.get('ELIGIBILITY')=='ELIGIBLE']
 if len(eligible)!=1:raise ValueError('SINGULAR_ROLE_REQUIRES_EXACTLY_ONE; aggregate role requires all members')
 # A single source is not authorized to represent the aggregate collection.
 if not eligible[0]['ELIGIBLE_AS_SOLE_COLLECTION_REPRESENTATIVE']:raise ValueError('PARTIAL_SOURCE_COVERAGE')
 return eligible[0]
def project(collection,prefix):
 if type(prefix) is not int or prefix<0 or prefix>=len(prefixes):raise ValueError('INVALID_PREFIX')
 ids=[x.get('SOURCE_ID') for x in collection]
 if len(set(ids))!=len(ids) or set(ids)!=set(expected):raise ValueError('INCOMPLETE_OR_FOREIGN_COLLECTION')
 for x in collection:
  if x!=expected[x['SOURCE_ID']]:raise ValueError('SOURCE_ROLE_PIN_OR_PROVENANCE_MISMATCH')
 return [{'source_id':x['SOURCE_ID'],'native_entrypoint':'adapter.planner.codec.load_pinned','operands':{'root':str(R),'pin':x['PIN']},'prefix':prefix} for x in sorted(collection,key=lambda x:canon(x['PIN'])) if x['FIRST_AVAILABLE_EVENT_PREFIX']<=prefix]
negative=[]
def rejects(name,fn):
 try:fn()
 except (ValueError,TypeError,KeyError) as ex:negative.append({'NAME':name,'RESULT':'PASS','REJECTION':str(ex),'QUALIFICATION_OPERATION_EXECUTED':False});return
 raise AssertionError('NEGATIVE_ACCEPTED '+name)
rejects('first member implicitly selected',lambda:singular([members[0]]))
rejects('last member implicitly selected',lambda:singular([members[-1]]))
base=project(members,9)
for name,variant in [('original',members),('reversed',list(reversed(members))),('rotated',members[1:]+members[:1])]:
 assert project(variant,9)==base
 rejects('singular selection under '+name,lambda v=variant:singular(v))
for field in ['SEMANTIC_ROLE','CONTENT_IDENTITY','PROVENANCE_ROLE']:
 bad=copy.deepcopy(members);bad[0][field]='wrong';rejects('wrong '+field,lambda b=bad:project(b,9))
foreign=copy.deepcopy(members);foreign[0]['SOURCE_ID']='foreign';rejects('foreign source',lambda:project(foreign,9))
rejects('zero eligible sources accepted',lambda:singular([]))
rejects('multiple eligible sources silently accepted',lambda:singular(members))
rejects('collection passed as singular pin',lambda:singular([{'ELIGIBILITY':'ELIGIBLE','ELIGIBLE_AS_SOLE_COLLECTION_REPRESENTATIVE':False,'PIN':members}]))
other=copy.deepcopy(members);other[0]['LINEAGE']='E2-CANONICAL-BASELINE-1';rejects('source from another case',lambda:project(other,9))
artifact=copy.deepcopy(members);artifact[0]['PIN']['path']='docs/plans/qualification/E2_P05_D01_A14_P06_POLICY_REPLAY_CLOSURE_26/prospective-a14-bundle.json';rejects('A14 persistence artifact substituted for source pin',lambda:project(artifact,9))
rejects('omitted required source',lambda:project(members[:-1],9))
rejects('duplicate source',lambda:project(members+[members[0]],9))
assert len(project(members,0))==16 and len(base)==51
future=next(x for x in members if x['FIRST_AVAILABLE_EVENT_PREFIX']>0);assert future['SOURCE_ID'] not in {x['source_id'] for x in project(members,0)}
rejects('future source made prefix available',lambda:project([dict(x,FIRST_AVAILABLE_EVENT_PREFIX=0) if x['SOURCE_ID']==future['SOURCE_ID'] else x for x in members],0))
# Wrong first/last ordinal rules demonstrably vary under permissible presentations.
assert members[0]['SOURCE_ID']!=list(reversed(members))[0]['SOURCE_ID'] and members[0]['SOURCE_ID']!=(members[1:]+members[:1])[0]['SOURCE_ID']
seed_results=[]
for seed in [0,1,7,101]:
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED=str(seed));p=subprocess.run([sys.executable,str(E/'reconcile.py'),'--identity'],cwd=str(R),env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,check=True)
 seed_results.append({'PYTHONHASHSEED':seed,'SEMANTIC_SHA256':p.stdout.strip(),'SELECTION':'UNRESOLVED','NATIVE_CASE_OPERATION_EXECUTED':False})
assert len({x['SEMANTIC_SHA256'] for x in seed_results})==1
# Hash-seed presentations use a set only to perturb documentary order, never choose a member.
for seed in [0,1,7,101]:
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED=str(seed));p=subprocess.run([sys.executable,'-c','import json; print(json.dumps(list(set('+repr([x['SOURCE_ID'] for x in members])+'))))'],env=env,stdout=subprocess.PIPE,text=True,check=True)
 order=json.loads(p.stdout);assert project([expected[i] for i in order],9)==base
 rejects('hash-seed '+str(seed)+' ordinal selection',lambda o=order:singular([expected[o[0]]]))
emit('negative-suite.json',{'RESULT':'PASS','PASS':len(negative),'TOTAL':len(negative),'CONTROLS':negative,'ORDER_PRESENTATIONS':'original/reversed/rotated + fresh hash-seed sets','AGGREGATE_PROJECTION_INVARIANT':True,'SINGULAR_SELECTION_INVARIANT':'UNRESOLVED for every presentation'})
emit('determinism.json',{'RESULT':'PASS','FRESH_PROCESSES':seed_results,'SOURCE_SELECTION_PERFORMED':False,'SOURCE_IDS_AND_ELIGIBILITY_INVARIANT':True})
correction={'TYPE':'PROPOSED_CARDINALITY_PRESERVING_DISPATCH_CORRECTION','STATUS':'SEALED_PROPOSAL_ONLY_NOT_APPLIED','AUTHORITATIVE_RULE':'Each current/prefix-available source; future additions excluded from earlier replay','OWNING_OBLIGATION':'D01-OBL:SOURCE_BYTES','OWNING_DISPATCH':'D01-DISPATCH:SOURCE_BYTES','CURRENT_DISPATCH':pin(DISPATCH),'CURRENT_CAPSULE':pin(CAP),'FROZEN_OBLIGATIONS':pin(FROZEN),'AGGREGATE_CARDINALITY':'ALL_REQUIRED_MEMBERS','NATIVE_CALL_CARDINALITY':1,'NATIVE_ENTRYPOINT':'adapter.planner.codec.load_pinned','ROOT':str(R),'COLLECTION_POINTER':'/canonical_content/arguments/bundle/sources','INPUT_COLLECTION_COUNT':51,'COLLECTION_IDENTITY':'qualification-source-bytes-collection-v1:'+sha(canon(sorted([x['PIN'] for x in members],key=canon))),'SELECTION':'No single member selected; exact source membership preserved','PROJECTION':'For each explicitly owned selected checkpoint and exact prefix, enumerate every prefix-available pin and invoke existing native LOAD_PIN once per pin. Stable sorting organizes job records only; source collection is semantically unordered. Do not merge foreign checkpoint collections or use future additions in earlier prefixes.','PREFIX_MEMBERSHIP_RULE':'Remove exact source_additions declared by ordered native event records from terminal source set for prefix 0; add each only at its owning recorded admission/install/materialization prefix. Never execute an event to derive the metadata. Original event/parent/ledger order remains exact.','CURRENT_PREFIX_JOB_COUNTS':[x['AVAILABLE_COUNT'] for x in prefixes],'OUTPUT_CAPTURE_SCHEMA':{'key':['owning_checkpoint_identity','event_prefix','native_pin_key','content_identity'],'value':'Complete native pinned-byte/projected-value result; independent expected values left to later oracle package'},'FAILURE_IF_ZERO':'Reject nonempty required domain reduced to zero; native empty source sets only with explicit checkpoint contract','FAILURE_IF_MULTIPLE':'Singular-source selector fails closed for multiple matches; aggregate enumeration requires exact complete set, not a unique aggregate member','FAILURE_IF_MISSING_EXTRA_DUPLICATE_FOREIGN_OR_FUTURE':'Reject before any native qualification invocation','POLICY_SEPARATION':{'pin':load(CAP)['canonical_content']['arguments']['bundle']['policy'],'role':'D01-OBL:POLICY owns versioned selector policy; native complete bundle source validation also loads this separately. Policy is not silently selected as SOURCE_BYTES.pin.'},'MUTATION_INVALIDATION':'NONE; unchanged/source availability role, separate mutation/invalidation obligations preserved','NATIVE_CAPABILITY_CHANGE_REQUIRED':False,'NATIVE_SOURCE_STATE_CHANGED':False,'OBLIGATION_COUNT_REMAINS':128,'REQUIRED_FUTURE_IDENTITY_CHANGES':['New runner/dispatch identity when proposal applied','Affected invocation-record identities','Future matrix identity'],'HISTORICAL_RUNNER_SELECTED':False,'BROADER_CHECKPOINT_SELECTION_PERFORMED':False,'AUTHORITY':'Existing frozen all-members rule determines correction. No legitimate scope-preserving single-source choice exists. This package does not apply the proposal or authorize qualification execution.'}
correction['PROPOSAL_IDENTITY']='qualification-source-bytes-dispatch-correction-v1:'+sha(canon(correction));emit('dispatch-correction-proposal.json',correction)
emit('proposed-projection-current-domain.json',{'NOT_AN_INVOCATION_BINDING':True,'CURRENT_PREFIX_PROJECTIONS':[{'PREFIX':i,'JOBS':project(members,i)} for i in range(10)],'FULL_OUTPUT_ORACLES_CONSTRUCTED':0,'NATIVE_OPERATIONS_INVOKED':0})
print('STATIC CHECKS PASS',len(negative),'negatives; four-seed reconstruction PASS; proposal sealed, not applied')
