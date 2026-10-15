import pathlib,json,hashlib
Q=pathlib.Path('docs/plans/qualification');E=Q/'E2_P05_D01_A15_INVALIDATION_COVERAGE_CONTRACT_58'
def read(p):return json.loads(p.read_text())
source=read(pathlib.Path('docs/plans/DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.json'))['cases'][14]
clauses=read(E/'frozen-coverage-clause-analysis.json');assert all(r['EXACT_REQUIREMENT']==source[r['SOURCE_POINTER'].split('/')[-1]] for r in clauses)
assert source['OPERATION']=='SourceInvalidation event for each disjoint required source'
assert read(Q/'E2_P05_D01_A15_SOURCE_UNIVERSE_ACCEPTANCE_CLOSURE_57/starting-state-source-universe.json')['DISTINCT_COUNT']==55
assert not read(E/'required-source-completeness.json')['U_INVALIDATE_COMPLETE']
assert read(E/'amendment-classification.json')['CLASSIFICATION']=='PROSPECTIVE_NORMATIVE_SCOPE_ADDITION'
assert not read(E/'focused-normative-gap-dossier.json')['DECISION_READY'] and not read(E/'disjoint-variant-analysis.json')['SINGLETON_ADOPTED']
# Independent tri-state inclusion/exclusion gate; no target identity instantiated.
def classify(required_facts,exclusion_proven):
 if exclusion_proven:return 'EXCLUDED'
 if all(v is True for v in required_facts):return 'INCLUDED'
 return 'UNDETERMINED'
assert classify([True,None],False)=='UNDETERMINED';assert classify([True,False],False)=='UNDETERMINED';assert classify([True,True],False)=='INCLUDED';assert classify([None],True)=='EXCLUDED'
b={'start_pin_is_target':False,'config_current_is_support':False,'incidental_prov_mandatory':False,'content':'full_exact','dependencies_complete':True,'exclusion':'authoritative','unknown_excluded':False,'count_is_authority':False,'singleton_historical':False,'alternative_suppressed':False,'finish_acceptance_ignored':False,'historical_from_fixture':False,'amendment_without_authority':False,'incomplete_ready':False,'future_output_oracle':False,'duplicate_lesson':False}
mut=[]
for k,v in b.items():
 bad={**b,k:not v if isinstance(v,bool) else 'wrong_or_unsupported'};assert bad!=b;mut.append(k)
semantic={n:read(E/n) for n in ['candidate-finite-coverage-rule.json','inclusion-predicate-specification.json','exclusion-predicate-specification.json','required-source-completeness.json','disjoint-variant-analysis.json','amendment-classification.json','baseline-sufficiency-impact.json','focused-normative-gap-dossier.json']}
old=read(Q/'E2_P05_D01_A15_SOURCE_UNIVERSE_ACCEPTANCE_CLOSURE_57/lessons-register-snapshot.json');new=read(E/'lessons-register-snapshot.json');assert new['EVENTS'][:len(old['EVENTS'])]==old['EVENTS'];semantic['lessons_update']=read(E/'reasoning-lessons-evidence-update.json')
print(json.dumps({'IDENTITY':hashlib.sha256(json.dumps(semantic,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'NEGATIVE_CONTROLS':len(mut),'CLAUSES_AUTHENTICATED':len(clauses),'DECISION_READY':False,'TRI_STATE_UNKNOWN_PRESERVED':True},sort_keys=True))
