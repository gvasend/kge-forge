import pathlib,json,hashlib
P=pathlib.Path('docs/plans');E=P/'qualification/E2_P05_D01_A15_PROSPECTIVE_BOUNDARY_53'
def read(p):return json.loads(p.read_text())
frozen=read(P/'DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.json')['cases'][14];trace=read(E/'acceptance-traceability.json');assert len(trace)==11 and len({r['REQUIREMENT_ID'] for r in trace})==11
assert [r['REQUIREMENT_ID'] for r in trace[:10]]==['A15-R%02d'%i for i in range(1,11)]
for field in ['INITIAL_STATE','OPERATION','PERSISTENCE_REQUIREMENT','DETERMINISM_REQUIREMENT','NEGATIVE_INVARIANTS']:assert any(r['FROZEN_REQUIREMENT']==frozen[field] for r in trace)
for term in ['Dependent admission stale','Ordering obligations retained','held/blocked descendants','resume false','reload preserves invalidation']:assert any(r['FROZEN_REQUIREMENT']==term for r in trace)
for row in trace:
 assert all(row[k] for k in ['REQUIRED_OBSERVATION','MINIMUM_FIXTURE_PRECONDITION','EXPECTED_NATIVE_BEHAVIOR','INDEPENDENT_ORACLE_REQUIREMENT','ASSURANCE_REQUIREMENT','AUTHORITY_REQUIREMENT'])
# Verify immutable event chain and all cited source bytes directly.
register=read(E/'lessons-register-snapshot.json');live=read(P/'PLANNER_REASONING_LESSONS_REGISTER_1.json');assert live['EVENTS'][:len(register['EVENTS'])]==register['EVENTS'];previous='0'*64;ids=[]
for event in register['EVENTS']:
 body=dict(event);digest=body.pop('EVENT_HASH');assert body['PREVIOUS_EVENT_HASH']==previous
 assert hashlib.sha256(json.dumps(body,sort_keys=True,separators=(',',':')).encode()).hexdigest()==digest;previous=digest
 if event['EVENT_TYPE']=='LESSON_RECORDED':
  l=event['LESSON'];ids.append(l['LESSON_ID']);assert l['CONFIDENCE']['causal_hypothesis']=='LOW_UNTESTED'
  for source in l['EVIDENCE_SOURCE']:assert hashlib.sha256(pathlib.Path(source['path']).read_bytes()).hexdigest()==source['raw_sha256']
assert ids==['LL-%02d'%i for i in range(1,9)]
baseline=read(E/'baseline-assessment.json');assert baseline['BASELINE_OUTCOME']=='UNDETERMINED' and not baseline['DECISION_READY']
assert not read(E/'independent-expected-output-contract.json')['READY']
assert not read(E/'remaining-boundary-gaps.json')['MINIMUM_BOUNDARY_COMPLETE']
# Static gates reject unsupported claims, rather than execute an invalidation scenario.
base={'frozen_coverage':True,'exact_sources':True,'oracle_independent':True,'authority':True,'history_rewritten':False,'acceptance_weakened':False,'alternatives_suppressed':False,'computed_resume':True,'persisted_occurrence':True,'cold_memory_isolated':True,'baseline_substitution_authorized':True,'causal_hypothesis_presented_as_fact':False}
def passes(x):return x==base
mut=[]
for k,v in base.items():
 bad={**base,k:not v};assert not passes(bad);mut.append(k)
semantic={n:read(E/n) for n in ['acceptance-traceability.json','prospective-fixture-contract.json','baseline-assessment.json','strategy-comparison.json','remaining-boundary-gaps.json','capability-architectural-impact.json']};semantic['lessons']=register;semantic['negative_controls']=mut
print(json.dumps({'IDENTITY':hashlib.sha256(json.dumps(semantic,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'TRACE_ROWS':len(trace),'LESSONS':8,'EVENTS':len(register['EVENTS']),'NEGATIVE_CONTROLS':len(mut),'MINIMUM_BOUNDARY_COMPLETE':False,'DECISION_READY':False,'CAUSAL_HYPOTHESES_VALIDATED':False},sort_keys=True))
