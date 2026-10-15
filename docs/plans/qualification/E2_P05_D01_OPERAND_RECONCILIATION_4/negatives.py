"""Fail-closed metadata negative guards; no Snapshot or case is mutated."""
import hashlib,json
from copy import deepcopy
from pathlib import Path
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;C3=R/'docs/plans/qualification/E2_P05_D01_OPERAND_CLOSURE_3'
def read(p):return json.loads(p.read_bytes())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
class Reject(ValueError):pass
def need(v,r):
 if not v:raise Reject(r)
prior=read(C3/'operand-source-and-derivation-inventory.json')['ROWS'];new=read(O/'new-source-bindings.json')['ROWS'];a03=read(O/'a03-boundary-oracle.json');a14=read(O/'a14-boundary-oracle.json');overrides=read(O/'a03-invocation-source-overrides.json')
expected={'prior':prior,'new':new,'a03':a03,'a14':a14,'overrides':overrides,'mutation_descriptors':[],'mutations_applied':0,'invalidations_applied':0,'scope_issued':False}
def validate(v):
 need(v['mutations_applied']==v['invalidations_applied']==0,'APPLIED_DESCRIPTOR_FORBIDDEN')
 need(not v['scope_issued'],'NO_SCOPE_AUTHORITY')
 need(v['prior']==prior,'FROZEN_39_BINDING_OR_RECEIPT_ROUTE_CHANGED')
 need(v['mutation_descriptors']==[],'UNSEALED_MUTATION_TARGET_OPERATOR_OR_BASE; no accepted mutation descriptor exists yet')
 need(v['a03']['CASE_ID']=='E2-A03' and v['a03']['PRE_STATE_IDENTITY']==a03['PRE_STATE_IDENTITY'],'A03_PRE_POST_OR_OWNER_BOUNDARY')
 need(v['a14']['CASE_ID']=='E2-A14' and v['a14']['PHASES']==a14['PHASES'] and v['a14']['PRE_STATE_IDENTITY']==a14['PRE_STATE_IDENTITY'],'A14_PRE_POST_OR_OWNER_BOUNDARY')
 need(v['overrides']==overrides,'PARENT_HEAD_PHASE_CONTEXT_OR_SOURCE_OVERRIDE')
 need(v['a03']==a03 and v['a14']==a14,'SEALED_BOUNDARY_ORACLE_CHANGED')
 need(len(v['new'])==13,'NEW_BINDING_COUNT')
 for actual,exp in zip(v['new'],new):
  if actual.get('VALUE'):
   need(actual['VALUE'].get('namespace')=='planner-bundle-v1' and actual['VALUE'].get('kind',{}).get('value')=='CONTENT_IDENTITY','WRONG_NATIVE_IDENTITY_DOMAIN')
  need(actual==exp,'OPERAND_SOURCE_IDENTITY_SCOPE_LINEAGE_PROVENANCE_OR_OWNER_CHANGED')
 return True
validate(expected);results=[]
def reject(name,mutate):
 v=deepcopy(expected);mutate(v)
 try:validate(v)
 except Reject as exc:results.append({'case':name,'status':'REJECTED','reason':str(exc)})
 else:raise AssertionError('UNREJECTED:'+name)
ai=next(i for i,r in enumerate(new) if r['CASE_ID']=='E2-A03');bi=next(i for i,r in enumerate(new) if r['OPERAND_NAME']=='expected_bundle_identity');ii=next(i for i,r in enumerate(prior) if r.get('SOURCE_TYPE')=='SourceInvalidation descriptor');ri=next(i for i,r in enumerate(prior) if r['OBLIGATION_ID']=='D01-OBL:INVALIDATE_EXTERNAL_ROUTE')
reject('A03 pre/post boundary swap',lambda v:v['a03'].update(PRE_STATE_IDENTITY=a14['PRE_STATE_IDENTITY']))
reject('A14 pre/post boundary swap',lambda v:v['a14']['PHASES'].reverse())
reject('A03 operand consumed at A14',lambda v:v['new'][ai].update(CASE_ID='E2-A14'))
reject('A14 operand consumed at A03',lambda v:v['a14'].update(CASE_ID='E2-A03'))
reject('future result used as input',lambda v:v['new'][ai].update(VALUE_REFERENCE={'future_result':'step_0_native_result'}))
reject('post-mutation source used as base',lambda v:v['new'][bi].update(SOURCE_ARTIFACT={'future_mutated_source':True}))
reject('wrong mutation target',lambda v:v['mutation_descriptors'].append({'TARGET':'UNBOUND_WRONG','OPERATOR':'UNBOUND','APPLIED':False}))
reject('wrong mutation operator',lambda v:v['mutation_descriptors'].append({'TARGET':'UNBOUND','OPERATOR':'UNBOUND_WRONG','APPLIED':False}))
reject('mutation descriptor applied instead of bound',lambda v:v.update(mutations_applied=1))
reject('invalidation confused with mutation',lambda v:v['prior'][ii].update(SOURCE_TYPE='MutationDescriptor'))
reject('wrong receipt',lambda v:v['prior'][ii].update(TARGET_IDENTITY={'wrong_receipt':'different'}))
reject('wrong route',lambda v:v['prior'][ri].update(TARGET_IDENTITY={'wrong_route':'different'}))
reject('wrong source',lambda v:v['new'][ai].update(SOURCE_ARTIFACT=a14['PRE_STATE_SOURCE']))
reject('stale source',lambda v:v['new'][bi]['SOURCE_ARTIFACT'].update(raw_sha256='0'*64))
reject('wrong identity domain',lambda v:v['new'][bi]['VALUE'].update(namespace='planner-event-v1'))
reject('wrong parent',lambda v:v['overrides'][0].update(EXPECTED_PARENT=a14['PRE_STATE_IDENTITY']))
reject('wrong head',lambda v:v['overrides'][0].update(EXPECTED_HEAD=None))
reject('wrong phase',lambda v:v['overrides'][0].update(PHASE='POST_ACQUISITION'))
reject('wrong context',lambda v:v['new'][ai].update(GENERATION='OTHER-GENERATION'))
reject('cross-row source leakage',lambda v:v['new'][ai].update(SOURCE_ARTIFACT=v['new'][bi]['SOURCE_ARTIFACT']))
result={'STATUS':'PASS_20_FAIL_CLOSED_STATIC_METADATA_GUARDS','COUNT':len(results),'ROWS':results,'LIMITS':'Mutation target/operator negatives reject unsealed descriptors, not deviations from a complete accepted mutation oracle. Complete invocation static preflight remains NOT_RUN. No native qualification negative is executed.','QUALIFICATION_CASES_EXECUTED':0,'MUTATIONS_APPLIED':0,'INVALIDATIONS_APPLIED':0}
(O/'negative-suite.json').write_bytes(canon(result)+b'\n');print('STATIC_METADATA_NEGATIVES=20/20_REJECTED; NATIVE_CASES=0')
