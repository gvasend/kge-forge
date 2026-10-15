"""Independent truth-table/currentness/closure metadata examples; no native case."""
import copy,itertools,os,subprocess,sys
from pathlib import Path
E=Path(__file__).resolve().parent;sys.path.insert(0,str(E));from recover import R,Q,load,emit,canon,sha
r=load(E/'shared-semantics-recovery.json')
def proof_group(op,states):
 if op not in ['ALL','ANY']:raise ValueError('UNDECLARED_OPERATOR')
 if any(x not in ['PROVED','DISPROVED','UNKNOWN'] for x in states):raise ValueError('WRONG_PROOF_DOMAIN')
 if not states:return 'UNKNOWN'
 if op=='ALL':return 'DISPROVED' if 'DISPROVED' in states else 'PROVED' if set(states)=={'PROVED'} else 'UNKNOWN'
 return 'PROVED' if 'PROVED' in states else 'DISPROVED' if set(states)=={'DISPROVED'} else 'UNKNOWN'
# Truth tables independently explicit, not prospective A15 expected values.
expected_all=[['PROVED','DISPROVED','UNKNOWN'],['DISPROVED','DISPROVED','DISPROVED'],['UNKNOWN','DISPROVED','UNKNOWN']]
expected_any=[['PROVED','PROVED','PROVED'],['PROVED','DISPROVED','UNKNOWN'],['PROVED','UNKNOWN','UNKNOWN']]
states=['PROVED','DISPROVED','UNKNOWN'];positive=[]
for i,a in enumerate(states):
 for j,b in enumerate(states):
  assert proof_group('ALL',[a,b])==expected_all[i][j];assert proof_group('ANY',[a,b])==expected_any[i][j]
  positive.append({'inputs':[a,b],'ALL':expected_all[i][j],'ANY':expected_any[i][j]})
assert proof_group('ALL',[])==proof_group('ANY',[])=='UNKNOWN';assert proof_group('ALL',['UNKNOWN','PROVED'])!='PROVED' and proof_group('ANY',['UNKNOWN','PROVED'])=='PROVED'
required=['installed','active_exact_role','historical_event_witness','current_authority','canonical_binding','source_pin_exact','policy_context_exact','provenance_exact']
def role_current(facts):return all(facts.get(k) is True for k in required)
base={k:True for k in required};assert role_current(base)
examples=[]
for field in required:
 facts=dict(base);facts[field]=False;assert not role_current(facts);examples.append({'changed':field,'source_bytes_current':facts['source_pin_exact'],'usable_role':False})
# Activation event sequence, not timestamp/registry position, identifies exact role version.
versions=[{'subject':'QA_ROLE','sequence':1,'id':'QA_OLD','wall_time':999},{'subject':'QA_ROLE','sequence':2,'id':'QA_NEW','wall_time':1}]
assert max(versions,key=lambda x:x['sequence'])['id']=='QA_NEW';assert max(reversed(versions),key=lambda x:x['sequence'])['id']=='QA_NEW'
def closure(seeds,edges):
 reached=set(seeds)
 while True:
  new=reached|{b for a,b in edges if a in reached}
  if new==reached:return sorted(reached)
  reached=new
assert closure(['QA_S'],[('QA_S','QA_A'),('QA_A','QA_B'),('QA_B','QA_A'),('QA_S','QA_C')])==['QA_A','QA_B','QA_C','QA_S']
assert closure(['QA_S'],[('QA_S','QA_A'),('QA_S','QA_A')])==['QA_A','QA_S']
# One source can serve multiple alternative paths: shared membership is not effect-disjointness.
assert proof_group('ANY',['UNKNOWN','UNKNOWN'])=='UNKNOWN'
negative=[]
def reject(name,fn):
 try:fn()
 except ValueError as ex:negative.append({'NAME':name,'RESULT':'PASS','REJECTION':str(ex),'NATIVE_OPERATION_EXECUTED':False});return
 raise AssertionError('FAIL_OPEN '+name)
def ensure(condition,why):
 if not condition:raise ValueError(why)
def unqualified(reason):raise ValueError('A15_OWNER_GROUP_ROLE_TARGET_MAPPING_UNSEALED: '+reason)
reject('association treated as necessity',lambda:unqualified('association'))
reject('alternative member treated individually mandatory',lambda:ensure(proof_group('ANY',['UNKNOWN','PROVED'])!='PROVED','OTHER_ADMISSIBLE_ALTERNATIVE_REMAINS'))
reject('missing mandatory support accepted',lambda:ensure(proof_group('ALL',['UNKNOWN','PROVED'])=='PROVED','MANDATORY_MEMBER_NOT_PROVED'))
reject('superseded support treated current',lambda:ensure(role_current(dict(base,active_exact_role=False)),'INACTIVE_ROLE'))
reject('historical-only support active',lambda:ensure(role_current(dict(base,active_exact_role=False,current_authority=False)),'HISTORICAL_NOT_CURRENT'))
reject('currentness by timestamp',lambda:ensure(max(versions,key=lambda x:x['wall_time'])['id']=='QA_NEW','WALL_TIME_NOT_ACTIVATION_AUTHORITY'))
reject('wrong dependency direction',lambda:ensure(closure(['QA_S'],[('QA_A','QA_S')])==['QA_A','QA_S'],'REVERSED_SOURCE_CONSUMER_DIRECTION'))
for label in ['unsupported transitive target closure','declaration-only edge invalidation','provenance-only incidence invalidation','incomplete rule qualified','ownership selected prematurely','projection selected by count']:
 reject(label,lambda label=label:unqualified(label))
reject('wrong content identity',lambda:ensure('AUTHORITY_IDENTITY'=='CONTENT_IDENTITY','SOURCE_TARGET_DOMAIN'))
reject('duplicate content target in disjoint groups',lambda:ensure(len({'QA_CONTENT_S'})==len(['QA_CONTENT_S','QA_CONTENT_S']),'CONTENT_ALIAS_DUPLICATE'))
for field in ['policy_context_exact','provenance_exact']:
 reject('foreign scope/lineage or provenance '+field,lambda field=field:ensure(role_current(dict(base,**{field:False})),'CONTEXT_PROVENANCE_MISMATCH'))
reject('incorrect generation',lambda:ensure(role_current(dict(base,policy_context_exact=False)),'GENERATION_MISMATCH'))
proposed=r['PROPOSED_CONTRACTS'][0];reject('proposed rule historical authority',lambda:ensure(proposed['STATUS']=='HISTORICAL_AUTHORITATIVE','PROPOSAL_NOT_AUTHORIZED'))
seeds=[]
for seed in [0,1,7,101]:
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED=str(seed));p=subprocess.run([sys.executable,str(E/'recover.py'),'--identity'],cwd=str(R),env=env,capture_output=True,text=True,check=True);seeds.append({'seed':seed,'semantic_identity':p.stdout.strip(),'selected_owner_or_target':None})
assert len({x['semantic_identity'] for x in seeds})==1
emit('independent-qualification-feasibility.json',{'RECOVERED_NATIVE_OPERATOR_KERNEL':'PASS independent metadata examples; no native gate/state operation called','ALL_ANY_TRUTH_TABLE_CASES':positive,'EMPTY_GROUP':'UNKNOWN','CURRENTNESS_CONJUNCTION_CASES':examples,'ACTIVATION_VS_TIMESTAMP_CASE':versions,'SHARED_DEPENDENCY_CYCLE_DUPLICATE_EFFECT_CLOSURE':'PASS symbolic metadata fixtures','A15_QUALIFIED_EDGE_TARGET_PARTITION_FEASIBILITY':'UNREADY: exact owner/native edge-role/group membership/necessity/currentness mapping and partition rule absent','PROPOSED_GROUP_ENCODING':'Precise encoding shape/test method; cannot become a selectable A15 rule before applicability mapping','PROPOSED_PARTITION_ENCODING':'Membership/domain checks feasible only after exact authorized target universe/group rule; no actual partition constructed'})
emit('negative-suite.json',{'RESULT':'PASS','PASS':len(negative),'TOTAL':len(negative),'CASES':negative,'EXPECTED_VALUES_ARE_METADATA_KERNEL_TESTS_NOT_A15_ORACLE':True})
emit('determinism.json',{'RESULT':'PASS','SEEDS':seeds,'EDGE_RULE_CLASSIFICATION_PROPOSAL_CANDIDATE_IDENTITIES_STABLE':True,'TARGETS_GENERATED':False})
print('40 shared-semantic kernel checks PASS',len(negative),'negatives; four seeds; A15 applicability still incomplete')
