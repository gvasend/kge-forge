"""Append reviews in the existing register schema; do not rewrite old events."""
import pathlib,json,hashlib,copy
P=pathlib.Path('docs/plans');E=pathlib.Path(__file__).parent;A=E.parent/'E2_P05_D01_A15_CAPTURE_PERSISTENCE_RESUME_CLOSURE_61';p=P/'PLANNER_REASONING_LESSONS_REGISTER_1.json';md=P/'PLANNER_REASONING_LESSONS_REGISTER_1.md'
def h(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
r=json.loads(p.read_text());prior=json.loads((A/'lessons-register-snapshot.json').read_text());assert r['EVENTS'][:len(prior['EVENTS'])]==prior['EVENTS'];old=copy.deepcopy(r);prev='0'*64
for e in r['EVENTS']:
 assert e['PREVIOUS_EVENT_HASH']==prev and h({k:v for k,v in e.items() if k!='EVENT_HASH'})==e['EVENT_HASH'];prev=e['EVENT_HASH']
assert [e['LESSON']['LESSON_ID'] for e in r['EVENTS'] if e['EVENT_TYPE']=='LESSON_RECORDED']==['LL-'+str(i).zfill(2) for i in range(1,11)]
notes={1:('SUPPORTING_EVIDENCE','Exact prospective checkpoint/oracle/harness scope is carried into authority preparation; no return to broad historical reconstruction.'),2:('NO_NEW_EVIDENCE','No new strategy comparison or quantified efficiency result is established.'),3:('SUPPORTING_EVIDENCE','Authority issuer/version/mandate are separate missing knowledge from complete technical oracle/harness inputs.'),4:('SUPPORTING_EVIDENCE','Three exact authority input gaps block the complete decision; the two-variant technical payload is already independently bound.'),5:('SUPPORTING_EVIDENCE','Prospective evidence is explicitly distinct from historical occurrence and 19 unresolved historical owner classifications.'),6:('SUPPORTING_EVIDENCE','Neither the preparation request, schema version 1, native fixture DECIDE facts nor A14 approval supplies A15 issuer/adoption/execution authority.'),7:('NO_NEW_EVIDENCE','The 109/52 operand count is preserved; technical preparation identity is separate progress from authorization or runtime qualification.'),8:('NO_NEW_EVIDENCE','No new native typed-identity collision is observed.'),9:('NO_NEW_EVIDENCE','Existing exact validation/usability/satisfaction/control/resume distinctions are preserved without new native effects.'),10:('SUPPORTING_EVIDENCE','Package61 full output and updated-bundle capture bindings now have exact evidence pins in the proposed technical authority subject; complete capture expectations do not authenticate an issuer or authorize execution.')}
evidence=[{'path':str(A/'evidence-index.json'),'raw_sha256':hashlib.sha256((A/'evidence-index.json').read_bytes()).hexdigest()},{'path':str(E/'authority-subject-manifest.json'),'raw_sha256':hashlib.sha256((E/'authority-subject-manifest.json').read_bytes()).hexdigest()},{'path':str(E/'authority-gap-dossier.json'),'raw_sha256':hashlib.sha256((E/'authority-gap-dossier.json').read_bytes()).hexdigest()}]
if not any(e.get('WORK_PACKAGE')=='62' for e in r['EVENTS']):
 for i,(classification,note) in notes.items():
  e={'EVENT_TYPE':'LESSON_EVIDENCE_REVIEW','WORK_PACKAGE':'62','PREVIOUS_EVENT_HASH':prev,'REVIEW':{'LESSON_ID':'LL-'+str(i).zfill(2),'CLASSIFICATION':classification,'OBSERVATION':note,'EVIDENCE':evidence,'CAUSE_PROVEN':False}};e['EVENT_HASH']=h(e);r['EVENTS'].append(e);prev=e['EVENT_HASH']
 p.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
 with md.open('a') as f:
  f.write('\n## Package 62 — Bounded authority qualification review\n\n')
  for i,(classification,note) in notes.items():f.write('- LL-'+str(i).zfill(2)+' — '+classification+': '+note+'\n')
  f.write('\nNo new lesson or quantified efficiency claim is added; causal hypotheses remain unvalidated. Review head: `'+prev+'`.\n')
assert r['EVENTS'][:len(old['EVENTS'])]==old['EVENTS']
(E/'lessons-register-snapshot.json').write_text(p.read_text());(E/'lessons-register-snapshot.md').write_text(md.read_text())
(E/'reasoning-lessons-evidence-update.json').write_text(json.dumps({'LESSONS_REVIEWED':10,'NEW_LESSONS':0,'LL_10_PRESERVED':True,'PRIOR_EVENTS_PRESERVED':True,'PACKAGE_61_EVENT_COUNT':len(prior['EVENTS']),'HEAD':prev,'REVIEWS':[e for e in r['EVENTS'] if e.get('WORK_PACKAGE')=='62'],'CAUSAL_ATTRIBUTION_VALIDATED':False,'QUANTIFIED_EFFICIENCY_CLAIMED':False},sort_keys=True,indent=2)+'\n')
print(json.dumps({'LESSONS_REVIEWED':10,'NEW_LESSONS':0,'HEAD':prev}))
