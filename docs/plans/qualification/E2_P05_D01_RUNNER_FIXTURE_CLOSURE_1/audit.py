"""Independent static dispatch/construction audit and integrity negatives."""
import ast
from copy import deepcopy
from common import *
from runner import static_preflight
frozen=read(PRIOR/'sealed-128-obligations.json')['obligations']
paths=read(OUT/'dispatch-table.json');fixtures=read(OUT/'fixture-catalog.json');seal=read(OUT/'runner-source-seal.json')
index=read(OUT/'partial-construction-index.json');schema=read(OUT/'normalization-and-output-schema.json')
# Expected coordinates are read from frozen obligations, not index rows.
expected=[dict(obligation_id=o['OBLIGATION_ID'],case_id=o['CASE_ID'],dispatch_id='D01-DISPATCH:'+o['ORIGINAL_INPUT_ID'],fixture_role_requirement=o['ORIGINAL_ROW']['EXPECTED_TYPE'],output_requirement=o['EXPECTED_OUTPUT'],ordering=o['COMPARISON_EXPECTATION']['ordering']) for o in frozen]
save('independent-expected-construction-coordinates.json',expected)

def validate(p,f,s,ix,out):
 ids=[r['OBLIGATION_ID'] for r in ix['rows']]
 demand(len(ids)==128 and len(set(ids))==128 and set(ids)=={e['obligation_id'] for e in expected},'MISSING_EXTRA_OR_DUPLICATE_OBLIGATION')
 seen=[]
 for e in expected:
  matching=[v for v in p.values() if v['obligation_id']==e['obligation_id']]
  demand(len(matching)==1,'MISSING_OR_AMBIGUOUS_DISPATCH')
  path=matching[0];demand(path['dispatch_id']==e['dispatch_id'],'WRONG_DISPATCH')
  r=next(r for r in ix['rows'] if r['OBLIGATION_ID']==e['obligation_id'])
  demand(r['RUNNER_DISPATCH_ID']==path['dispatch_id'],'ROW_DISPATCH_MISMATCH')
  demand(r['CASE_ID']==e['case_id'],'WRONG_CASE')
  demand(r['NATIVE_OPERATION']==path['operation_ids'],'WRONG_OPERATION_BOUNDARY')
  for op in path['operation_ids']:demand(op in OPERATIONS,'UNKNOWN_NATIVE_OPERATION')
  for fid in r['FIXTURE_IDS']:
   demand(fid in f,'MISSING_FIXTURE')
   x=f[fid];demand(x['state_variant_id'] in r['STATE_VARIANT_IDS'],'WRONG_STATE_VARIANT')
   demand(filehash(ROOT/x['artifact']['path'])==x['artifact']['raw_sha256'],'WRONG_FIXTURE_FILE_IDENTITY')
   body=read(ROOT/x['artifact']['path']);demand(qid('fixture-content',body['canonical_content'])==x['content_identity'],'WRONG_FIXTURE_CONTENT_IDENTITY')
  demand(r['EXPECTED_FULL_OUTPUT_ORACLE_ID'] is None,'UNSUPPORTED_ORACLE_PROMOTION')
  demand(r['READER_MODE']['mode']=='COLD_INDEPENDENT_PROCESS','WARM_READER_SUBSTITUTION')
  demand(r['PERMUTATION_MODE']['native_unordered']==['original','reversed','rotated'],'WRONG_UNORDERED_PERMUTATION_SEMANTICS')
  demand(r['PERMUTATION_MODE']['ordered_ancestry']=='REORDER_MUST_REJECT','ORDERED_ANCESTRY_NOT_PRESERVED')
  demand(r['EXPECTED_COMPARISON']['original_requirement']==e['output_requirement'],'WRONG_EXPECTED_OUTPUT_REQUIREMENT')
 demand(out==schema,'PARTIAL_OR_CHANGED_OUTPUT_SCHEMA')
 for pin in s['body']['runtime_pins']+[s['body']['source'],s['body']['helpers'],s['body']['dispatch'],s['body']['supported_operation_set'],s['body']['output_schema']]:demand(filehash(ROOT/pin['path'])==pin['raw_sha256'],'RUNNER_OR_RUNTIME_PIN_CHANGED')
 demand(s==seal,'MIXED_RUNNER_RUNTIME_PIN_SET')
 demand(ix['kind']=='NOT_COMPLETE_PROSPECTIVE_MATRIX' and ix['complete_rows']==0 and not ix['construction_ready'],'INCOMPLETE_INDEX_PROMOTED_TO_READY')
 return True
validate(paths,fixtures,seal,index,schema)
records=[]
def reject(name,fn):
 p,f,s,ix,out=map(deepcopy,[paths,fixtures,seal,index,schema]);fn(p,f,s,ix,out)
 try:validate(p,f,s,ix,out)
 except Reject as exc:records.append(dict(case=name,status='REJECTED',reason=str(exc)))
 else:raise AssertionError('NEGATIVE_ACCEPTED:'+name)
first=next(iter(paths));fid=next(iter(fixtures));rowid=next(r['OBLIGATION_ID'] for r in index['rows'] if r['FIXTURE_IDS'])
reject('wrong dispatch',lambda p,f,s,i,o:i['rows'][0].update(RUNNER_DISPATCH_ID='WRONG'))
reject('ambiguous dispatch',lambda p,f,s,i,o:p.update(ALIAS=deepcopy(p[first])))
reject('missing fixture',lambda p,f,s,i,o:f.pop(fid))
reject('wrong fixture identity',lambda p,f,s,i,o:f[fid].update(content_identity='WRONG'))
reject('wrong state variant',lambda p,f,s,i,o:next(r for r in i['rows'] if r['OBLIGATION_ID']==rowid).update(STATE_VARIANT_IDS=['WRONG']))
# No actual oracle exists; validate refuses any fabricated oracle as if one were sealed.
reject('wrong oracle substituted for missing independent oracle',lambda p,f,s,i,o:i['rows'][0].update(EXPECTED_FULL_OUTPUT_ORACLE_ID='FABRICATED'))
reject('wrong operation boundary',lambda p,f,s,i,o:i['rows'][0].update(NATIVE_OPERATION=['NONEXISTENT']))
reject('partial expected output',lambda p,f,s,i,o:o['fields'].pop('typed_snapshot'))
reject('warm-reader substitution',lambda p,f,s,i,o:i['rows'][0]['READER_MODE'].update(mode='WARM'))
reject('wrong permutation semantics',lambda p,f,s,i,o:i['rows'][0]['PERMUTATION_MODE'].update(ordered_ancestry='PERMUTABLE'))
reject('runner source changed',lambda p,f,s,i,o:s['body']['source'].update(raw_sha256='0'*64))
reject('matrix row removed',lambda p,f,s,i,o:i['rows'].pop())
reject('matrix row added',lambda p,f,s,i,o:i['rows'].append(deepcopy(i['rows'][0])))
reject('mixed runtime pins',lambda p,f,s,i,o:s['body']['runtime_pins'][0].update(raw_sha256='0'*64))
reject('incomplete construction promoted to READY',lambda p,f,s,i,o:i.update(construction_ready=True))
save('construction-integrity-negatives.json',dict(status='PASS_STATIC_INCOMPLETE_CONSTRUCTION_ONLY',cases=records,not_a_complete_matrix_negative_suite=True,missing_oracle_control='Complete matrix cannot pass while oracle missing; no fabricated substitute admitted'))
static=static_preflight();save('static-runner-preflight.json',static)
save('independent-construction-comparison.json',dict(dispatch_coordinates='PASS_128_OF_128',obligation_case_associations='PASS',materialized_fixture_reference_integrity='PASS',full_concrete_matrix='NOT_AVAILABLE',full_independent_matrix_comparison='NOT_PERFORMED',expected_coordinates_generated_from_frozen_obligations=True,qualification_cases_executed=0))
print('STATIC_CONSTRUCTION_AUDIT_PASS; INTEGRITY_NEGATIVES='+str(len(records)))
