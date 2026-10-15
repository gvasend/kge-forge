import pathlib,json,hashlib
P=pathlib.Path('docs/plans');E=P/'qualification/E2_P05_D01_A15_PRODUCER_CURRENTNESS_SOURCE_CLOSURE_55'
def read(p):return json.loads(p.read_text())
old=read(P/'qualification/E2_P05_D01_A15_FINITE_BOUNDARY_BASELINE_54/lessons-register-snapshot.json');x=read(E/'lessons-register-snapshot.json');assert x['EVENTS'][:len(old['EVENTS'])]==old['EVENTS'];prev='0'*64
for event in x['EVENTS']:
 body=dict(event);h=body.pop('EVENT_HASH');assert body['PREVIOUS_EVENT_HASH']==prev and hashlib.sha256(json.dumps(body,sort_keys=True,separators=(',',':')).encode()).hexdigest()==h;prev=h
 if event.get('WORK_PACKAGE')=='55':
  src=event['REVIEW']['EVIDENCE'];assert hashlib.sha256(pathlib.Path(src['path']).read_bytes()).hexdigest()==src['raw_sha256']
assert read(E/'reasoning-lessons-evidence-update.json')['NEW_LESSONS']==0
semantic={f:read(E/f) for f in ['producer-currentness-inventory.json','21-dependency-closure-analysis.json','18-source-role-inventory.json','three-authority-reference-verification.json','dependent-admission-inventory.json','stale-admission-witness-assessment.json','descendant-effects.json','baseline-sufficiency-update.json','reasoning-lessons-evidence-update.json']}
print(hashlib.sha256(json.dumps(semantic,sort_keys=True,separators=(',',':')).encode()).hexdigest())
