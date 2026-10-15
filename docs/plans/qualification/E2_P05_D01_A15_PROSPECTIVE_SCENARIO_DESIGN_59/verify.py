import pathlib,json,hashlib
P=pathlib.Path('docs/plans');E=P/'qualification/E2_P05_D01_A15_PROSPECTIVE_SCENARIO_DESIGN_59'
def read(p):return json.loads(p.read_text())
old=read(P/'qualification/E2_P05_D01_A15_INVALIDATION_COVERAGE_CONTRACT_58/lessons-register-snapshot.json');new=read(E/'lessons-register-snapshot.json');assert new['EVENTS'][:len(old['EVENTS'])]==old['EVENTS'];head='0'*64
for event in new['EVENTS']:
 body=dict(event);h=body.pop('EVENT_HASH');assert body['PREVIOUS_EVENT_HASH']==head and hashlib.sha256(json.dumps(body,sort_keys=True,separators=(',',':')).encode()).hexdigest()==h;head=h
 if event.get('WORK_PACKAGE')=='59':
  src=event['REVIEW']['EVIDENCE'];assert hashlib.sha256(pathlib.Path(src['path']).read_bytes()).hexdigest()==src['raw_sha256']
scenario=read(E/'concrete-scenario-specification.json');assert len(scenario['OWNERS'])==2 and len(scenario['VARIANTS'])==2
ids=[v['INITIAL_TARGET_CONTENT_IDENTITY'] for v in scenario['VARIANTS']];assert len({json.dumps(x,sort_keys=True) for x in ids})==2
assert all(v['START_SNAPSHOT']==scenario['START']['SNAPSHOT'] for v in scenario['VARIANTS'])
assert read(E/'protected-effect-policy.json')['DIRECT_PROTECTED_IDENTITIES'] and not read(E/'protected-effect-policy.json')['EMPTY_PROTECTED_SET_ASSUMED']
assert not read(E/'scenario-gap-dossier.json')['DECISION_READY'] and all(v['EXPECTED_EVENT_ID']=='UNBOUND' for v in scenario['VARIANTS'])
case=read(P/'DETERMINISTIC_PLANNER_V0_1_CANONICAL_QUALIFICATION_EXPERIMENT_1.json')['cases'][14]
for row in read(E/'frozen-acceptance-traceability.json'):assert row['FROZEN_REQUIREMENT']==case[row['POINTER'].split('/')[-1]]
semantic={f:read(E/f) for f in ['concrete-scenario-specification.json','proposed-requiredness-rule.json','candidate-invalidation-universe.json','disjoint-variant-policy.json','protected-effect-policy.json','frozen-acceptance-traceability.json','independent-oracle-specification.json','baseline-assessment.json','scenario-gap-dossier.json','reasoning-lessons-evidence-update.json']}
print(hashlib.sha256(json.dumps(semantic,sort_keys=True,separators=(',',':')).encode()).hexdigest())
