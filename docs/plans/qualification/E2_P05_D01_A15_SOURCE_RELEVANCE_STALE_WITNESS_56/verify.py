import pathlib,json,hashlib
P=pathlib.Path('docs/plans');E=P/'qualification/E2_P05_D01_A15_SOURCE_RELEVANCE_STALE_WITNESS_56'
def read(p):return json.loads(p.read_text())
old=read(P/'qualification/E2_P05_D01_A15_PRODUCER_CURRENTNESS_SOURCE_CLOSURE_55/lessons-register-snapshot.json');new=read(E/'lessons-register-snapshot.json');assert new['EVENTS'][:len(old['EVENTS'])]==old['EVENTS'];prev='0'*64
for event in new['EVENTS']:
 body=dict(event);h=body.pop('EVENT_HASH');assert body['PREVIOUS_EVENT_HASH']==prev and hashlib.sha256(json.dumps(body,sort_keys=True,separators=(',',':')).encode()).hexdigest()==h;prev=h
 if event.get('WORK_PACKAGE')=='56':
  src=event['REVIEW']['EVIDENCE'];assert hashlib.sha256(pathlib.Path(src['path']).read_bytes()).hexdigest()==src['raw_sha256']
assert read(E/'reasoning-lessons-evidence-update.json')['NEW_LESSONS']==0
mapping=read(E/'conditional-stale-witness-mapping.json');assert len(mapping)==3 and all(x['CLASSIFICATION']=='EXACT_CONDITIONAL_MAPPING' and not x['STALENESS_OBSERVED'] for x in mapping)
assert not read(E/'finite-source-relevance-assessment.json')['FINITE_SOURCE_COVERAGE_COMPLETE'];assert read(E/'baseline-sufficiency-update.json')['OUTCOME']=='UNDETERMINED'
assert read(E/'ordered-trace-contract.json')['FUTURE_EVENT_ID'] is None
semantic={n:read(E/n) for n in ['SLOT-proof-source-inventory.json','ROOT-proof-source-inventory.json','conditional-stale-witness-mapping.json','source-to-effect-coverage-matrix.json','FINISH-effect-contract.json','alternative-proof-analysis.json','baseline-sufficiency-update.json','independent-oracle-readiness.json','reasoning-lessons-evidence-update.json']}
print(hashlib.sha256(json.dumps(semantic,sort_keys=True,separators=(',',':')).encode()).hexdigest())
