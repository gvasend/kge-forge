"""Complete-set structural preflight; never calls a qualification operation."""
import ast
from copy import deepcopy
import hashlib
import json
from pathlib import Path
from adapter.planner import codec
R=Path(__file__).resolve().parents[4];O=Path(__file__).resolve().parent;Q=R/'docs/plans/qualification';OLD=Q/'E2_P05_D01_RUNNER_FIXTURE_CLOSURE_1';PRIOR=Q/'E2_P05_D01_PROSPECTIVE_MATRIX_CONTRACT_1'
def read(p):return json.loads(Path(p).read_bytes())
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()
def save(n,x):(O/n).write_bytes(canon(x)+b'\n')
def ref(p,pointer=''):return dict(path=str(Path(p).relative_to(R)),pointer=pointer,raw_sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest())
class Reject(ValueError):pass
def demand(v,m):
 if not v:raise Reject(m)
frozen=read(PRIOR/'sealed-128-obligations.json')['obligations'];catalog=read(O/'fixture-catalog.json');dispatch=read(O/'dispatch-table-v2.json');ops=read(OLD/'supported-operation-set.json');variants=read(PRIOR/'state-variant-declarations.json');index=read(OLD/'partial-construction-index.json')['rows'];expectedids={v['VARIANT_ID'] for v in variants}
rows=[];references=[]
for fid,entry in catalog.items():
 pin=entry['artifact'];demand(hashlib.sha256((R/pin['path']).read_bytes()).hexdigest()==pin['raw_sha256'],'FIXTURE_SOURCE_PIN')
 packet=read(R/pin['path']);demand(packet['state_variant_id'] in expectedids,'UNKNOWN_VARIANT')
 native=codec._unwire(packet['canonical_content']['subject']) # structural only
 body=codec._wire(native);demand(body['$type']=='Snapshot','NATIVE_TYPE')
 rows.append(dict(CAPSULE_ID=fid,STATE_VARIANT_ID=packet['state_variant_id'],NATIVE_TYPE='Snapshot',STRUCTURAL_VALIDATION='PASS_TYPES_ONLY',IDENTITY=packet['content_identity'],SCOPE=body['context']['scope'],LINEAGE=body['context']['lineage'],PROVENANCE=packet['provenance']))
demand(len(rows)==len({r['STATE_VARIANT_ID'] for r in rows})==117,'EXACT_117_VARIANTS')
for row in index:
 did=row['RUNNER_DISPATCH_ID'];path=dispatch[did]
 for vid in row['STATE_VARIANT_IDS']:
  entry=next(v for v in catalog.values() if v['state_variant_id']==vid);packet=read(R/entry['artifact']['path']);available=packet['canonical_content']['arguments'];steps=path.get('variant_paths',{}).get(vid,path['steps']);bound=set();missing=[]
  for i,step in enumerate(steps):
   meta=ops[step['operation_id']];module,fn=meta['module'],meta['entrypoint']
   if module:
    tree=ast.parse((R/(module.replace('.','/')+'.py')).read_text());demand(any(isinstance(n,ast.FunctionDef) and n.name==fn for n in tree.body),'MISSING_ENTRYPOINT')
   for b in step['args']:
    if 'fixture_field' in b and b['fixture_field'] not in available:missing.append(dict(step=i,operand=b['fixture_field']))
    if 'prior_result' in b:demand(b['prior_result'] in bound,'ORPHAN_RESULT_BINDING')
   bound.add(step['bind_result_as'])
  references.append(dict(OBLIGATION_ID=row['OBLIGATION_ID'],CAPSULE_ID=entry['fixture_id'],DISPATCH_ID=did,STATE_VARIANT_ID=vid,missing=missing,complete_not_claimed=True))
save('structural-capsule-preflight.json',dict(count=117,rows=rows,case_operations_executed=0))
save('revised-operand-audit.json',dict(missing_operand_reference_occurrences=sum(len(r['missing']) for r in references),references=references,context_bindings='source_root/store_root explicit context references; exact context paths and archive closure not yet completely materialized',defaults='Explicit native default AST sealed per revised step; non-null applicability defaults still need concrete matrix validation'))
# Identify expected schemas and independent sources; do not generate output from case results.
oracle=[]
for ob in frozen:
 cid=ob['CASE_ID'];classes=['AUTHORITATIVE_CONTRACT','CANONICAL_IDENTITY_RULE','SNAPSHOT_RULE','LEDGER_RULE','PERSISTENCE_RULE','REPLAY_RULE']
 if cid.startswith('E2-N'):classes.append('NEGATIVE_REJECTION_CONTRACT')
 oracle.append(dict(OBLIGATION_ID=ob['OBLIGATION_ID'],SOURCE_CLASSIFICATIONS=classes,INDEPENDENT_SOURCE_PINS=ob['ORIGINAL_ROW']['PROVENANCE'],EXPECTED_BEHAVIOR=ob['EXPECTED_BEHAVIOR'],EXPECTED_OUTPUT_REQUIREMENT=ob['EXPECTED_OUTPUT'],EXPECTED_SCHEMA=ref(OLD/'normalization-and-output-schema.json'),FULL_OUTPUT_ORACLE_ID=None,ORACLE_INDEPENDENCE='NOT_ESTABLISHED_FOR_COMPLETE_GROUND_RECORD',PROSPECTIVE_RUNNER_IS_ORACLE_SOURCE=False,NO_FUTURE_OR_MUTABLE_CASE_OUTPUT_USED=True,complete=False))
save('independent-oracle-source-gap-inventory.json',oracle)
# Metadata negatives compare actual authoritative catalogs and fail closed for incompleteness.
def validate(c,d,inventory):
 actual={e['state_variant_id'] for e in c.values()};demand(actual==expectedids and len(c)==117,'MISSING_WRONG_OR_DUPLICATE_VARIANT')
 for pin in [ref(O/'runner_v2.py'),ref(O/'dispatch-table-v2.json')]:demand((R/pin['path']).is_file(),'MISSING_RUNNER')
 for o in frozen:
  match=[p for p in d.values() if p['obligation_id']==o['OBLIGATION_ID']];demand(len(match)==1,'WRONG_OR_AMBIGUOUS_DISPATCH')
 demand(len(inventory)==128,'ORACLE_ROW_COVERAGE')
 demand(all(not r['complete'] and r['FULL_OUTPUT_ORACLE_ID'] is None and not r['PROSPECTIVE_RUNNER_IS_ORACLE_SOURCE'] for r in inventory),'UNSUPPORTED_ORACLE_PROMOTION')
 return True
validate(catalog,dispatch,oracle)
neg=[]
def reject(name,mutate):
 c,d,i=map(deepcopy,[catalog,dispatch,oracle]);mutate(c,d,i)
 try:validate(c,d,i)
 except Reject as exc:neg.append(dict(case=name,status='REJECTED',reason=str(exc)))
 else:raise AssertionError('UNREJECTED_METADATA_NEGATIVE')
fid=next(iter(catalog));did=next(iter(dispatch))
reject('missing variant',lambda c,d,i:c.pop(fid))
reject('wrong variant',lambda c,d,i:c[fid].update(state_variant_id='WRONG'))
reject('wrong dispatch',lambda c,d,i:d[did].update(obligation_id='WRONG'))
reject('duplicate dispatch',lambda c,d,i:d.update(dup=deepcopy(d[did])))
reject('runner-derived oracle',lambda c,d,i:i[0].update(PROSPECTIVE_RUNNER_IS_ORACLE_SOURCE=True))
reject('partial record promoted to complete oracle',lambda c,d,i:i[0].update(complete=True,FULL_OUTPUT_ORACLE_ID='FAKE'))
reject('oracle row removed',lambda c,d,i:i.pop())
save('static-integrity-negatives.json',dict(status='PASS_INCOMPLETE_CONSTRUCTION_GUARDS_ONLY',cases=neg,full_construction_negative_suite='NOT_COMPLETE_NO_COMPLETE_MATRIX_OR_ORACLES'))
save('static-complete-matrix-preflight.json',dict(status='FAIL_INCOMPLETE_OPERANDS_ORACLES_PROCESS_BINDINGS',dispatch_targets='PASS_EXISTING_NATIVE_FUNCTIONS',structural_capsules='117/117',operand_reference_gaps=sum(len(r['missing']) for r in references),full_output_oracles='0/128',all_output_schemas_ground_values_validated=False,qualification_case_calls=0))
print('STRUCTURAL_CAPSULES_PASS=117/117; COMPLETE_STATIC_PREFLIGHT=FAIL_INCOMPLETE; NO_CASE_RUN')
