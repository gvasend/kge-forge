import pathlib,json,hashlib
P=pathlib.Path('docs/plans');E=P/'qualification/E2_P05_D01_A15_INDEPENDENT_AFTER_STATE_ORACLE_60'
def read(p):return json.loads(p.read_text())
old=read(P/'qualification/E2_P05_D01_A15_PROSPECTIVE_SCENARIO_DESIGN_59/lessons-register-snapshot.json');new=read(E/'lessons-register-snapshot.json');assert new['EVENTS'][:len(old['EVENTS'])]==old['EVENTS'];previous='0'*64;ids=[]
for event in new['EVENTS']:
 body=dict(event);h=body.pop('EVENT_HASH');assert body['PREVIOUS_EVENT_HASH']==previous and hashlib.sha256(json.dumps(body,sort_keys=True,separators=(',',':')).encode()).hexdigest()==h;previous=h
 if event['EVENT_TYPE']=='LESSON_RECORDED':ids.append(event['LESSON']['LESSON_ID'])
assert ids==['LL-%02d'%i for i in range(1,11)]
semantic={'LL10':read(E/'LL-10-append-authentication.json'),'OUTPUTS':[read(p) for p in sorted(E.glob('*-expected-output.json'))]}
print(hashlib.sha256(json.dumps(semantic,sort_keys=True,separators=(',',':')).encode()).hexdigest())
