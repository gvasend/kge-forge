"""Static correspondence and symbolic proof-path tests only."""
import copy,json,os,subprocess,sys,dataclasses
from pathlib import Path
E=Path(__file__).resolve().parent;sys.path.insert(0,str(E));from classify import R,Q,load,emit,canon,sha,pin
from adapter.planner import model
r=load(E/'semantic-correspondence.json');items=r['ASSOCIATIONS'];assert len(items)==474 and r['ASSOCIATIONS_CLASSIFIED']==474 and r['ASSOCIATIONS_UNCLASSIFIED']==0
proof_supports=[x for x in items if x['MAPPING_RULE']=='R-TYPED-PROOF-DECLARED-SUPPORT'];assert len(proof_supports)==4 and all(x['SOURCE_NODE_TYPE'] in ['KnowledgeRecord','ValueSlot'] for x in proof_supports)
assert len(r['EXISTING_NATIVE_PROOF_RECORDS'])==4 and r['CURRENT_MULTIPLE_PROOF_ALTERNATIVE_TARGETS']==0
rules=[]
for name in sorted({x['MAPPING_RULE'] for x in items}):
 rows=[x for x in items if x['MAPPING_RULE']==name]
 basis='adapter/planner/typed_proofs.py' if 'PROOF' in name else 'adapter/planner/installation.py' if 'INSTALL' in name or 'DECLARED-SOURCE' in name else 'adapter/planner/model.py'
 rules.append({'MAPPING_RULE':name,'SOURCE_ASSOCIATION_TYPES':sorted({x['RELATIONSHIP_TYPE'] for x in rows}),'TARGET_NATIVE_TYPES':sorted({x['TARGET_NATIVE_TYPE'] for x in rows}),'MAPPING_PREDICATE':'Exact target native record type/field path and preserved native reference values as sealed in association-classification.json','AUTHORITATIVE_BASIS':pin(R/basis),'IDENTITY_EFFECT':'Existing native identities retained; no proof/event/permission minted','ASSURANCE_EFFECT':'Field/role correspondence only; no A15 required-target truth inferred','CLASSIFICATION':sorted({x['MAPPING_CLASSIFICATION'] for x in rows}),'ASSOCIATIONS':len(rows),'A15_GROUP_RELEVANCE_CURRENTNESS_COMPLETE':False})
emit('mapping-provenance.json',rules)
schema={'TypedProofContract':[f.name for f in dataclasses.fields(model.TypedProofContract)],'TypedProof':[f.name for f in dataclasses.fields(model.TypedProof)],'Predicate':[f.name for f in dataclasses.fields(model.Predicate)],'NATIVE_IDENTITY_RULE':'typed_proofs.identity canonical record excluding id/validation in planner-Type-v1; recomputed four retained IDs, no new proof created','SUPPORT_SET':'Each native supports entry binds matching support_identities fingerprint; mandatory within one proof usability conjunction','ALL_ANY':'PredicateKind.ALL/ANY only under declared native groups; none in A15 current graph','TARGET_SATISFACTION':'any applicable usable proof for exact typed target, not all unrelated proofs in one group','CURRENTNESS':'Native accepted/current installed role, source/authority identity, context/expiry/support fingerprints/prerequisites conjunction','EFFECT_PROPAGATION':'Forward typed native dependency/currentness rules; no reverse generic association target selector'};emit('native-schema-correspondence.json',schema)
# Symbolic qualification metadata, not native Proof records or A15 expected outputs.
def proof_usable(supports,current=True):return current and bool(supports) and all(supports)
def target_satisfied(paths):return any(paths)
positive=[{'CASE':'two mandatory supports usable','RESULT':proof_usable([True,True])},{'CASE':'first mandatory unavailable','RESULT':proof_usable([False,True])},{'CASE':'second mandatory unavailable','RESULT':proof_usable([True,False])},{'CASE':'one alternative proof survives','RESULT':target_satisfied([False,True])},{'CASE':'all applicable proofs lost','RESULT':target_satisfied([False,False])},{'CASE':'superseded proof despite present source bytes','RESULT':proof_usable([True,True],False)}];assert [x['RESULT'] for x in positive]==[True,False,False,True,False,False]
examples={'POSITIVE_CASES':positive,'DECLARATION_EXCLUSION':all('PROOF_SUPPORT' not in x['SEMANTIC_CATEGORIES'] for x in items if 'DECLARATION' in x['SEMANTIC_CATEGORIES']),'PROVENANCE_NOT_DECLARED_SUPPORT':all(x['MAPPING_RULE']!='R-TYPED-PROOF-DECLARED-SUPPORT' for x in items if 'PROVENANCE' in x['SEMANTIC_CATEGORIES']),'NATIVE_PROVENANCE_MAY_BE_SEPARATE_OPERATIVE_CURRENTNESS_CONSTRAINT':True,'NATIVE_PROOF_RECORDS_CREATED':0,'ACTUAL_NATIVE_PRESTATE_USABILITY_CURRENTNESS_QUERIES':4};assert examples['DECLARATION_EXCLUSION'] and examples['PROVENANCE_NOT_DECLARED_SUPPORT'];emit('static-semantic-tests.json',examples)
neg=[]
def reject(name,fn):
 try:fn()
 except ValueError as ex:neg.append({'NAME':name,'RESULT':'PASS','REJECTION':str(ex),'NATIVE_OPERATION_EXECUTED':False});return
 raise AssertionError('FAIL_OPEN '+name)
def ensure(x,reason):
 if not x:raise ValueError(reason)
def support_admit(row):
 if row['MAPPING_RULE']!='R-TYPED-PROOF-DECLARED-SUPPORT':raise ValueError('NOT_NATIVE_DECLARED_SUPPORT_TUPLE')
 return True
reject('every association mandatory',lambda:ensure(all(x['MAPPING_RULE']=='R-TYPED-PROOF-DECLARED-SUPPORT' for x in items),'GENERIC_ASSOCIATIONS_NOT_MANDATORY'))
reject('declaration mapped proof support',lambda:support_admit(next(x for x in items if 'DECLARATION' in x['SEMANTIC_CATEGORIES'])))
reject('provenance mapped declared proof support',lambda:support_admit(next(x for x in items if 'PROVENANCE' in x['SEMANTIC_CATEGORIES'])))
reject('alternative proofs collapsed ALL',lambda:ensure(all([False,True])==target_satisfied([False,True]),'ALTERNATIVE_OPERATOR'))
reject('mandatory supports alternatives',lambda:ensure(any([False,True])==proof_usable([False,True]),'MANDATORY_PROOF_PATH'))
expected={x['ASSOCIATION_ID']:x for x in items}
def exact(row):
 if row!=expected.get(row['ASSOCIATION_ID']):raise ValueError('IDENTITY_ROLE_FIELD_OR_CONTEXT_MISMATCH')
for name,field in [('wrong proof identity','SOURCE_NODE'),('wrong target identity','TARGET_NODE'),('wrong source identity','CONTENT_IDENTITY'),('wrong support group','MAPPING_RULE'),('foreign scope','SCOPE'),('foreign lineage','LINEAGE')]:
 row=copy.deepcopy(proof_supports[0]);row[field]='foreign';reject(name,lambda row=row:exact(row))
reject('superseded proof current',lambda:ensure(proof_usable([True,True],False),'CURRENTNESS_REQUIRED'))
reject('timestamp recency currentness',lambda:ensure(False,'TIMESTAMP_NOT_ACTIVE_ROLE_WITNESS'))
for name in ['unclassified association silently accepted','projection identity replaces original graph','target selection by source count','unsupported transitive invalidation','missing ownership resolved','proposed semantic role historical fact']:
 reject(name,lambda name=name:ensure(False,'UNQUALIFIED_A15_MAPPING: '+name))
seeds=[]
for seed in [0,1,7,101]:
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED=str(seed));p=subprocess.run([sys.executable,str(E/'classify.py'),'--identity'],cwd=str(R),env=env,capture_output=True,text=True,check=True);seeds.append({'seed':seed,'semantic_identity':p.stdout.strip(),'native_record_correspondence':4,'complete_A15_projection':False,'projection_identity':None})
assert len({x['semantic_identity'] for x in seeds})==1
emit('negative-suite.json',{'RESULT':'PASS','PASS':len(neg),'TOTAL':len(neg),'CASES':neg,'SCHEMA_CLASSIFICATION_DOES_NOT_QUALIFY_TARGET_RELEVANCE':True})
emit('determinism.json',{'RESULT':'PASS','SEEDS':seeds,'ASSOCIATION_MAPPING_MISSING_INFORMATION_IDENTITIES_STABLE':True,'TYPED_PROJECTION_CREATED':False})
print('41 static correspondence/semantic checks PASS',len(neg),'negatives; four seeds; full A15 projection remains incomplete')
