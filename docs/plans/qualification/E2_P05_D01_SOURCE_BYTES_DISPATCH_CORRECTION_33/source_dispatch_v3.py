"""Qualification metadata projection only. No Planner operation invoked here."""
import copy,json,hashlib
from pathlib import Path
R=Path('/home/gvasend/app/kge-forge');E=Path(__file__).resolve().parent

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def read(p):return json.loads(Path(p).read_bytes())
def check_pin(p):
 raw=(R/p['path']).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=p['raw_sha256']:raise ValueError('EXPANSION_PIN_CHANGED')
 return json.loads(raw)
def require(x,why):
 if not x:raise ValueError(why)
def expand_instances(row,path,packet,context):
 require(row['OBLIGATION_ID']==path['obligation_id']=='D01-OBL:SOURCE_BYTES','WRONG_OBLIGATION')
 require(row['RUNNER_DISPATCH_ID']==path['dispatch_id']=='D01-DISPATCH:SOURCE_BYTES','WRONG_DISPATCH')
 expansion=path['per_source_expansion'];require(expansion['runtime_source_selection'] is False,'PRESENTATION_SELECTION_FORBIDDEN');require(expansion['acceptance']=='ALL' and expansion['expected_count']==51,'WRONG_CARDINALITY_OR_AGGREGATION')
 domain=check_pin(expansion['domain']);instances=check_pin(expansion['instances']);aggregate=check_pin(expansion['aggregate']);original=check_pin(expansion['original_fixture'])
 def presentation_free(value):
  value=copy.deepcopy(value)
  for holder in [value['canonical_content'].get('bundle'),value['canonical_content']['arguments'].get('bundle')]:
   if holder is not None:holder['sources']=sorted(holder['sources'],key=canonical)
  return value
 require(presentation_free(packet)==presentation_free(original),'WRONG_CAPSULE_OR_PROVENANCE')
 require(context['source_root']==Path('/home/gvasend/app/kge-forge'),'WRONG_SOURCE_ROOT')
 require(packet['fixture_id']=='D01-FIXTURE:SOURCE_BYTES:REQUIRED_ROLE' and packet['state_variant_id']=='D01-VARIANT:SOURCE_BYTES:REQUIRED_ROLE','WRONG_CAPSULE_ASSOCIATION')
 members=domain['MEMBERS'];required={canonical(x['PIN']):x for x in members}
 supplied=packet['canonical_content']['arguments']['bundle']['sources'];keys=[canonical(x) for x in supplied]
 require(len(keys)==len(set(keys))==len(required)==len(instances)==51 and set(keys)==set(required),'NOT_EXACT_51_SOURCE_BIJECTION')
 jobs=[];seen=set()
 for instance in sorted(instances,key=lambda x:x['instance_identity']):
  k=canonical(instance['source_pin']);require(k in required and k not in seen,'FOREIGN_OR_DUPLICATE_INSTANCE_PIN');seen.add(k);member=required[k]
  require(instance['source_id']==member['SOURCE_ID'] and instance['provenance_role']==member['PROVENANCE_ROLE'] and instance['source_role']==member['SEMANTIC_ROLE'],'CROSS_SOURCE_PROVENANCE')
  require(instance['operands']=={'source_root':str(context['source_root']),'pin':member['PIN']} and instance['mutation_descriptor'] is None,'CROSS_SOURCE_OPERAND')
  for a,b in [('scope','SCOPE'),('lineage','LINEAGE'),('generation','GENERATION')]:require(instance[a]==member[b],'WRONG_CONTEXT')
  value=dict(instance);identity=value.pop('instance_identity');require(identity=='qualification-D01-source-instance-v1:'+hashlib.sha256(canonical(value)).hexdigest(),'INSTANCE_IDENTITY_MISMATCH')
  projected=copy.deepcopy(packet);projected['canonical_content']['arguments']['pin']=member['PIN']
  single=copy.deepcopy(path);single.pop('per_source_expansion')
  jobs.append((instance,projected,single))
 require(seen==set(required),'MISSING_INSTANCE')
 require(sorted(x['instance_identity'] for x in instances)==aggregate['required_instance_identities'],'AGGREGATE_MEMBERSHIP_MISMATCH')
 return jobs

def aggregate_outputs(path,outputs):
 aggregate=check_pin(path['per_source_expansion']['aggregate'])
 require(aggregate['acceptance']=='ALL','AGGREGATE_NOT_ALL')
 ids=[x['instance_identity'] for x in outputs]
 require(len(ids)==len(set(ids))==51 and sorted(ids)==aggregate['required_instance_identities'],'INCOMPLETE_OR_DUPLICATE_AGGREGATE')
 return {'aggregate_identity':aggregate['aggregate_identity'],'acceptance':'ALL','instance_count':51,'instance_outputs':sorted(outputs,key=lambda x:x['instance_identity'])}

def acceptance(contract,statuses):
 require(contract['acceptance']=='ALL','AGGREGATE_NOT_ALL')
 value=dict(contract);identity=value.pop('aggregate_identity');require(identity=='qualification-D01-source-aggregate-v1:'+hashlib.sha256(canonical(value)).hexdigest(),'AGGREGATE_IDENTITY_MISMATCH')
 ids=[x['instance_identity'] for x in statuses]
 require(len(ids)==len(set(ids))==51 and sorted(ids)==contract['required_instance_identities'],'INCOMPLETE_AGGREGATE')
 require(all(x['status']=='PASS' for x in statuses),'INSTANCE_NOT_PASS')
 return True
