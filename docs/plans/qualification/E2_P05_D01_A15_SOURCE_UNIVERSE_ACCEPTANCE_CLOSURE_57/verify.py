import pathlib,json,hashlib
P=pathlib.Path('docs/plans');E=P/'qualification/E2_P05_D01_A15_SOURCE_UNIVERSE_ACCEPTANCE_CLOSURE_57'
def read(p):return json.loads(p.read_text())
old=read(P/'qualification/E2_P05_D01_A15_SOURCE_RELEVANCE_STALE_WITNESS_56/lessons-register-snapshot.json');new=read(E/'lessons-register-snapshot.json');assert new['EVENTS'][:len(old['EVENTS'])]==old['EVENTS'];prev='0'*64
for event in new['EVENTS']:
 body=dict(event);h=body.pop('EVENT_HASH');assert body['PREVIOUS_EVENT_HASH']==prev and hashlib.sha256(json.dumps(body,sort_keys=True,separators=(',',':')).encode()).hexdigest()==h;prev=h
 if event.get('WORK_PACKAGE')=='57':
  src=event['REVIEW']['EVIDENCE'];assert hashlib.sha256(pathlib.Path(src['path']).read_bytes()).hexdigest()==src['raw_sha256']
start=read(E/'starting-state-source-universe.json');assert start['PIN_COUNT']==55 and start['DISTINCT_COUNT']==55 and start['COMPLETE_FOR_NATIVE_PIN_VALIDATION']
inv=read(E/'required-invalidation-source-universe.json');assert inv['MEMBERS'] is None and not inv['COMPLETE']
assert read(E/'baseline-sufficiency-update.json')['BASELINE_OUTCOME']=='UNDETERMINED'
conj=read(E/'frozen-acceptance-conjunction.json');assert len(conj)==12 and all(not x['WHOLE_ACCEPTANCE_COMPLETE'] for x in conj)
assert read(E/'ordered-trace-specification.json')['EXPECTED_INVALIDATION_EVENT_ID'] is None
assert read(E/'reasoning-lessons-evidence-update.json')['NEW_LESSONS']==0
semantic={f:read(E/f) for f in ['starting-state-source-universe.json','operative-support-source-universe.json','required-invalidation-source-universe.json','capture-source-artifact-universe.json','FINISH-held-control-resume-assessment.json','ordered-trace-specification.json','frozen-acceptance-conjunction.json','baseline-sufficiency-update.json','independent-oracle-readiness-matrix.json','reasoning-lessons-evidence-update.json']}
print(hashlib.sha256(json.dumps(semantic,sort_keys=True,separators=(',',':')).encode()).hexdigest())
