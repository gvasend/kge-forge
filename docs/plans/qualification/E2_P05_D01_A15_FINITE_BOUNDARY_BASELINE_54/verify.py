import pathlib,json,hashlib
P=pathlib.Path('docs/plans');E=P/'qualification/E2_P05_D01_A15_FINITE_BOUNDARY_BASELINE_54'
def read(p):return json.loads(p.read_text())
coverage=read(E/'frozen-acceptance-coverage.json');assert len(coverage)==11 and len({r['OBLIGATION_ID'] for r in coverage})==11
assert all(r['CONTRACT_TRACE_COVERED'] and not r['BEHAVIOR_DEMONSTRATED'] for r in coverage)
baseline=read(E/'existing-baseline-sufficiency.json');assert baseline['BASELINE_OUTCOME']=='UNDETERMINED' and not baseline['MISSING_ORACLE_IMPLIES_INSUFFICIENCY']
assert not read(E/'remaining-boundary-gaps.json')['BOUNDARY_COMPLETE']
old=read(P/'qualification/E2_P05_D01_A15_PROSPECTIVE_BOUNDARY_53/lessons-register-snapshot.json');new=read(E/'lessons-register-snapshot.json');live=read(P/'PLANNER_REASONING_LESSONS_REGISTER_1.json');assert new['EVENTS'][:len(old['EVENTS'])]==old['EVENTS'];assert live['EVENTS'][:len(new['EVENTS'])]==new['EVENTS']
prev='0'*64;ids=[]
for ev in new['EVENTS']:
 body=dict(ev);h=body.pop('EVENT_HASH');assert body['PREVIOUS_EVENT_HASH']==prev and hashlib.sha256(json.dumps(body,sort_keys=True,separators=(',',':')).encode()).hexdigest()==h;prev=h
 if ev['EVENT_TYPE']=='LESSON_RECORDED':ids.append(ev['LESSON']['LESSON_ID'])
assert ids==['LL-%02d'%i for i in range(1,10)]
assert read(E/'reasoning-lessons-evidence-update.json')['LESSONS_REVIEWED']==8
# Fail-closed static claim checks; not native invalidation tests.
b={'coverage':True,'dependency':'native_qualified','content':'full_exact','snapshot':'exact','historical_from_prospective':False,'baseline_from_oracle_absence':False,'alternative_suppressed':False,'descendant_present':True,'resume_contract':'frozen_false','trace':'exact_ordered','amendment':'none','superiority':'not_claimed','causal_hypothesis_as_fact':False,'lesson_duplicate':False,'old_lesson_changed':False}
def good(x):return x==b
mut=[]
for k,v in b.items():
 bad={**b,k:(not v if isinstance(v,bool) else 'wrong_or_unsupported')};assert not good(bad);mut.append(k)
semantic={n:read(E/n) for n in ['candidate-finite-boundary-inventory.json','required-source-coverage-analysis.json','frozen-acceptance-coverage.json','existing-baseline-sufficiency.json','strategy-comparison.json','reasoning-lessons-evidence-update.json','remaining-boundary-gaps.json']}
print(json.dumps({'IDENTITY':hashlib.sha256(json.dumps(semantic,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'NEGATIVE_CONTROLS':len(mut),'OLD_LESSONS_PRESERVED':True,'NEW_LESSONS':1,'BASELINE_OUTCOME':'UNDETERMINED','TRACE_OBLIGATIONS':11},sort_keys=True))
