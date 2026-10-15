"""Append evidence reviews; retain all prior lesson events and identities."""
import pathlib,json,hashlib,copy
P=pathlib.Path('docs/plans');E=pathlib.Path(__file__).parent;B=E.parent/'E2_P05_D01_A15_BOUNDED_AUTHORITY_QUALIFICATION_62';p=P/'PLANNER_REASONING_LESSONS_REGISTER_1.json';md=P/'PLANNER_REASONING_LESSONS_REGISTER_1.md'
def h(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
r=json.loads(p.read_text());prior=json.loads((B/'lessons-register-snapshot.json').read_text());assert r['EVENTS'][:len(prior['EVENTS'])]==prior['EVENTS'];old=copy.deepcopy(r);head='0'*64
for e in r['EVENTS']:
 assert e['PREVIOUS_EVENT_HASH']==head and h({k:v for k,v in e.items() if k!='EVENT_HASH'})==e['EVENT_HASH'];head=e['EVENT_HASH']
assert len([e for e in r['EVENTS'] if e['EVENT_TYPE']=='LESSON_RECORDED'])==10
notes={1:('SUPPORTING_EVIDENCE','Recovery focuses on the governing authority frontier without reopening source/owner graph qualification.'),2:('NO_NEW_EVIDENCE','No new alternative execution strategy or measured efficiency result is established.'),3:('SUPPORTING_EVIDENCE','Historical human role evidence is available, but exact current issuer designation and A15 instrument mandate remain distinct missing knowledge.'),4:('SUPPORTING_EVIDENCE','One precise issuing-instrument definition can bind the distinct issuer/version/normative/execution/capture subfields; they are not interchangeable.'),5:('SUPPORTING_EVIDENCE','Current native proof validity and historical human decisions do not expand the prospective A15 qualification boundary.'),6:('SUPPORTING_EVIDENCE','Authority to define/adopt fixture semantics, INSTALL, ATTEST, execute, and persist is separated. Explicit no-delegation and subject restrictions block automatic mandate transfer.'),7:('NO_NEW_EVIDENCE','The operand count remains 109/52 by scope; this recovery narrows authority evidence without claiming execution progress or quantified savings.'),8:('SUPPORTING_EVIDENCE','INSTALL admission receipts and operating ATTEST admission receipts are distinguished by actual native schema rather than filenames.'),9:('NO_NEW_EVIDENCE','State/validation/usability/satisfaction/control/resume expectations remain unchanged; no new native observation.'),10:('SUPPORTING_EVIDENCE','Complete sealed oracle/harness identities remain unchanged while authority roots are separately tested for exact issuer/version/subject/mandate applicability.')}
evidence={'path':str(E/'authority-root-inventory.json'),'raw_sha256':hashlib.sha256((E/'authority-root-inventory.json').read_bytes()).hexdigest()}
if not any(e.get('WORK_PACKAGE')=='63' for e in r['EVENTS']):
 for i,(classification,note) in notes.items():
  e={'EVENT_TYPE':'LESSON_EVIDENCE_REVIEW','WORK_PACKAGE':'63','PREVIOUS_EVENT_HASH':head,'REVIEW':{'LESSON_ID':'LL-'+str(i).zfill(2),'CLASSIFICATION':classification,'OBSERVATION':note,'EVIDENCE':evidence,'CAUSE_PROVEN':False}};e['EVENT_HASH']=h(e);r['EVENTS'].append(e);head=e['EVENT_HASH']
 p.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
 with md.open('a') as f:
  f.write('\n## Package 63 — Authority-root reconciliation review\n\n')
  for i,(classification,note) in notes.items():f.write('- LL-'+str(i).zfill(2)+' — '+classification+': '+note+'\n')
  f.write('\nNo new lesson or quantified benefit is claimed. Historical role authentication is not current subject authority; causal hypotheses remain unvalidated. Review head: `'+head+'`.\n')
assert r['EVENTS'][:len(old['EVENTS'])]==old['EVENTS']
(E/'lessons-register-snapshot.json').write_text(p.read_text());(E/'lessons-register-snapshot.md').write_text(md.read_text())
(E/'reasoning-lessons-evidence-update.json').write_text(json.dumps({'LESSONS_REVIEWED':10,'NEW_LESSONS':0,'OLD_EVENTS_PRESERVED':True,'LL_10_PRESERVED':True,'PREVIOUS_EVENT_COUNT':len(prior['EVENTS']),'HEAD':head,'REVIEWS':[e for e in r['EVENTS'] if e.get('WORK_PACKAGE')=='63'],'CAUSAL_HYPOTHESES_VALIDATED':False},sort_keys=True,indent=2)+'\n')
print(json.dumps({'LESSONS_REVIEWED':10,'NEW_LESSONS':0,'HEAD':head}))
