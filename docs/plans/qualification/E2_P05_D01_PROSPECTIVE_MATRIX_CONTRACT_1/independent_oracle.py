"""Independent planned-coverage oracle from immutable recovery, not built rows."""
import ast
from copy import deepcopy
from contract import ROOT,OUT,D,REC,P,TYPE,read,ref,save,qid,canonical,rawhash,demand,CASES,PHASES,SUBVARIANTS,ERRORS
source=read(REC/'runner-input-matrix.json')
# Build minimal expectation coordinates independently of builder functions.
expected=[]
for original in source:
 name=original['INPUT_ID'];cid=name.split('_')[0] if name.startswith('E2-') else 'E2-D01'
 role='D01-ROLE:CASE:'+cid+':'+name.split('_')[1] if name.startswith('E2-') else 'D01-ROLE:'+name
 boundary=name[len('PHASE_'):] if name.startswith('PHASE_') else PHASES[cid] if cid in PHASES else CASES[cid]['INITIAL_STATE'] if cid in CASES else 'AGGREGATE_QUALIFICATION'
 if cid in SUBVARIANTS:variants=['D01-VARIANT:'+cid+':'+s for s in SUBVARIANTS[cid]]
 elif cid in CASES:variants=['D01-VARIANT:'+cid+':CANONICAL_REQUIRED_BEHAVIOR']
 else:variants=['D01-VARIANT:'+name+':REQUIRED_ROLE']
 expected.append(dict(OBLIGATION_ID='D01-OBL:'+name,CASE_ID=cid,FIXTURE=role,STATE_VARIANT=variants,PHASE=boundary,EXPECTED_ORIGINAL_OUTPUT=CASES[cid]['EXPECTED_STATE'] if cid in CASES else original['EXPECTED_SEMANTICS'],EXPECTED_NEGATIVE_CONTRACT=ERRORS[cid] if cid in ERRORS else 'NOT_APPLICABLE_TO_THIS_OBLIGATION',MUTATION_EXPECTATION=original['EXPECTED_SEMANTICS'] if name.startswith('MUTATION_') or cid.startswith('E2-N') else 'NO_UNDECLARED_MUTATION',INVALIDATION_EXPECTATION=original['EXPECTED_SEMANTICS'] if name.startswith('INVALIDATE_') or cid in ['E2-A15','E2-A16','E2-N04','E2-N09'] else 'NOT_APPLICABLE_UNLESS_EXPLICIT_DEPENDENCY',ORDERING_SEMANTICS=original['ORDERING_SEMANTICS'],EXPECTED_TYPE=original['EXPECTED_TYPE'],CARDINALITY=original['CARDINALITY'],PROVENANCE=original['PROVENANCE']))
expected.sort(key=lambda r:r['OBLIGATION_ID'])
body=dict(kind='INDEPENDENT_PLANNED_REALIZATION_ORACLE_NOT_CONCRETE_FULL_OUTPUT_ORACLE',source=ref(REC/'runner-input-matrix.json'),rows=expected,role_and_variant_definitions='Prospective behavioral contract proposal, not historical inputs',complete_behavioral_value_oracle=False)
body['identity']=qid('independent-planned-oracle',body)
save('independent-expected-plan.json',body)
# Scope the comparison accurately: full behavioral qualification is impossible without native fixtures/runner.
plan=read(OUT/'planned-realization-matrix.json');full=read(OUT/'full-output-comparison-contract.json');runtime=read(OUT/'behavioral-runner-contract.json')['runtime_pins']
sealed_output_fields=set(full['fields'])

def validate(p,output,runtime_pins):
 demand(p['qualification_type']==TYPE,'HISTORICAL_LABEL_REJECTED')
 demand(p['kind']=='CONSTRUCTION_PLAN_NOT_COMPLETE_EXECUTABLE_MATRIX','PLAN_CANNOT_BE_PROMOTED')
 demand(p['runner_identity'] is None,'WRONG_RUNNER_OR_UNSUPPORTED_IDENTITY')
 rows=p['rows'];ids=[r['OBLIGATION_ID'] for r in rows]
 demand(len(ids)==128 and len(set(ids))==128 and set(ids)=={r['OBLIGATION_ID'] for r in expected},'EXACT_OBLIGATION_COVERAGE')
 demand(set(output['fields'])==sealed_output_fields,'PARTIAL_OUTPUT_COMPARISON_REJECTED')
 demand(output==full,'FULL_OUTPUT_CONTRACT_MISMATCH')
 demand(runtime_pins==runtime,'MIXED_OR_WRONG_RUNTIME_PINS')
 for pin in runtime_pins:demand(rawhash(ROOT/pin['path'])==pin['raw_sha256'],'RUNTIME_PIN_CURRENTNESS')
 mapped={r['OBLIGATION_ID']:r for r in rows}
 for e in expected:
  r=mapped[e['OBLIGATION_ID']]
  for field in ['CASE_ID','FIXTURE','STATE_VARIANT','PHASE']:demand(r[field]==e[field],field+'_MISMATCH:'+e['OBLIGATION_ID'])
  demand(r['RUNNER']=='REQUIRED_PROSPECTIVE_AGGREGATE_RUNNER_CONTRACT; NO_SUPPORTED_UNIQUE_IMPLEMENTATION_SELECTED','RUNNER_MISMATCH')
  demand(r['INPUTS']['original_type']==e['EXPECTED_TYPE'] and r['INPUTS']['cardinality']==e['CARDINALITY'],'INPUT_REQUIREMENT_MISMATCH')
  demand(r['EXPECTED_OUTPUT']['original_requirement']==e['EXPECTED_ORIGINAL_OUTPUT'],'EXPECTED_OUTPUT_MISMATCH')
  demand(r['EXPECTED_OUTPUT']['negative_contract']==e['EXPECTED_NEGATIVE_CONTRACT'],'NEGATIVE_CONTRACT_MISMATCH')
  demand(r['MUTATION_EXPECTATION']['dimension']==e['MUTATION_EXPECTATION'],'WRONG_MUTATION_DIMENSION')
  demand(r['MUTATION_EXPECTATION']['only_sealed_dimension_changes'] and r['MUTATION_EXPECTATION']['unaffected_native_fields_equal'],'MUTATION_COMPLEMENT_VIOLATION')
  demand(r['INVALIDATION_EXPECTATION']['required_behavior']==e['INVALIDATION_EXPECTATION'],'WRONG_INVALIDATION_CASE')
  demand(r['INVALIDATION_EXPECTATION']['only_declared_source_identity_changes'] and r['INVALIDATION_EXPECTATION']['historical_events_retained'],'INVALIDATION_HISTORY_VIOLATION')
  demand(r['READER_MODE']['mode']=='COLD_INDEPENDENT_PROCESS' and r['READER_MODE']['readers_per_checkpoint_seed']>=3,'COLD_READER_REQUIRED')
  demand(r['READER_MODE']['hash_seeds']==[0,1,7,101],'WRONG_SEEDS')
  demand(r['PERMUTATION_MODE']['native_unordered']==['original','reversed','rotated'],'UNORDERED_PRESENTATION_CONTRACT')
  demand(r['PERMUTATION_MODE']['ordered_ancestry']=='REORDER_MUST_REJECT','ORDERED_ANCESTRY_CANNOT_BE_PERMUTED')
  demand(r['PERMUTATION_MODE']['ordered_other_inputs']==e['ORDERING_SEMANTICS'],'ORDERING_REQUIREMENT_MISMATCH')
  demand(r['provenance']==e['PROVENANCE'],'SOURCE_PROVENANCE_MISMATCH')
 return True
validate(plan,full,runtime)
save('independent-plan-comparison.json',dict(coverage='PASS_128_OF_128_PLANNED',roles='PASS_DECLARATIVE',variants='PASS_DECLARED_REQUIRED_CLASSES_ONLY',expected_output_specifications='PASS_ORIGINAL_REQUIREMENTS_AND_PROPOSED_BOUNDARIES_PRESERVED',ordering='PASS_DECLARATIVE',concrete_fixture_and_full_output_oracle='NOT_COMPLETE',INDEPENDENT_MATRIX_ORACLE='NOT_ESTABLISHED_FOR_COMPLETE_EXECUTABLE_MATRIX',constructed_matrix_used_to_generate_expected_plan=False))
# Contract integrity negatives are metadata-only; no native/runner qualification is attempted.
records=[]
def reject(name,fn):
 p=deepcopy(plan);o=deepcopy(full);pins=deepcopy(runtime);fn(p,o,pins)
 try:validate(p,o,pins)
 except ValueError as exc:records.append(dict(case=name,status='REJECTED',reason=str(exc)))
 else:raise AssertionError('CONTRACT_NEGATIVE_ACCEPTED:'+name)
def rowchange(obligation,field,value):
 def change(p,o,pins):next(r for r in p['rows'] if r['OBLIGATION_ID']==obligation)[field]=value
 return change
reject('missing obligation',lambda p,o,pins:p['rows'].pop())
reject('duplicate obligation substituted for another',lambda p,o,pins:p['rows'].__setitem__(-1,deepcopy(p['rows'][0])))
reject('wrong runner',rowchange('D01-OBL:RUNNER_EXECUTABLE','RUNNER','RECOVERED_ORIGINAL_RUNNER'))
reject('wrong runner version',lambda p,o,pins:p.update(runner_identity='unsupported-runner-version'))
reject('wrong fixture role',rowchange('D01-OBL:E2-A01_OPERANDS','FIXTURE','D01-ROLE:WRONG'))
reject('wrong state variant',rowchange('D01-OBL:E2-N05_OPERANDS','STATE_VARIANT',['WRONG']))
reject('wrong phase',rowchange('D01-OBL:PHASE_POST_REENTRY','PHASE','EVIDENCE_RECEIVED'))
reject('wrong expected output',lambda p,o,pins:p['rows'][0]['EXPECTED_OUTPUT'].update(original_requirement='scalar PASS only'))
reject('wrong mutation dimension',lambda p,o,pins:next(r for r in p['rows'] if r['OBLIGATION_ID']=='D01-OBL:MUTATION_LINEAGE')['MUTATION_EXPECTATION'].update(dimension='change authority instead'))
reject('wrong invalidation case',lambda p,o,pins:next(r for r in p['rows'] if r['OBLIGATION_ID']=='D01-OBL:INVALIDATE_KNOWLEDGE')['INVALIDATION_EXPECTATION'].update(required_behavior='withdraw receipt'))
reject('warm reader substituted for cold reader',lambda p,o,pins:p['rows'][0]['READER_MODE'].update(mode='WARM_PROCESS'))
reject('unordered permutation treated as semantic difference',lambda p,o,pins:p['rows'][0]['PERMUTATION_MODE'].update(native_unordered=['ORDER_SENSITIVE']))
reject('ordered ancestry permutation accepted',lambda p,o,pins:p['rows'][0]['PERMUTATION_MODE'].update(ordered_ancestry='REORDER_ACCEPTED'))
reject('partial output comparison',lambda p,o,pins:o['fields'].pop('typed_snapshot'))
reject('mixed incompatible runtime pins',lambda p,o,pins:pins[0].update(raw_sha256='0'*64))
reject('historical label applied to prospective matrix',lambda p,o,pins:p.update(qualification_type='HISTORICAL_RECONSTRUCTION'))
reject('incomplete plan promoted to executable matrix',lambda p,o,pins:p.update(kind='COMPLETE_EXECUTABLE_MATRIX'))
# Documentary unordered job/presentation changes must not differ, while native sequences preserve order.
permuted=deepcopy(plan);permuted['rows'].reverse();validate(permuted,full,runtime)
save('matrix-contract-negative-results.json',dict(status='PASS_METADATA_CONTRACT_ONLY',rejected=records,unordered_documentary_row_presentation='ACCEPTED_EQUIVALENT',native_fixtures_or_runner_executed=False,full_runtime_negative_qualification='NOT_RUN'))
# Native exact-message provenance catalog, no operation invoked.
native_errors=[]
for pin in runtime:
 tree=ast.parse((ROOT/pin['path']).read_text())
 for n in ast.walk(tree):
  if isinstance(n,ast.Raise) and isinstance(n.exc,ast.Call) and n.exc.args:
   arg=n.exc.args[0]
   msg=arg.value if isinstance(arg,ast.Constant) and isinstance(arg.value,str) else ast.dump(arg)
   native_errors.append(dict(source=pin,line=n.lineno,error_expression=msg))
save('native-error-source-inventory.json',native_errors)
save('cross-row-consistency.json',dict(status='PASS_DECLARATIVE_PLAN',complete_native_matrix_consistency='NOT_ESTABLISHED',runtime_baseline='One exact pinned comparison baseline; not a selected runner',scope='Recovered qualification-only requirements retained; no invented context/authority transfer',Action_definition_versions='Exact per-fixture versions required; no actual definitions changed',lineage_generation='Native retained contexts preserved; compatible per-equivalence-class generation required before construction',source_policy_pins='Exact closure required, not concretely chosen',identity='Qualification namespace distinct from native; original ordering obligations preserved',runner_version='Unique complete implementation absent; cannot claim runner-version consistency for execution'))
print('INDEPENDENT_PLANNED_COVERAGE_PASS_128_OF_128; CONTRACT_NEGATIVES_REJECTED='+str(len(records)))
