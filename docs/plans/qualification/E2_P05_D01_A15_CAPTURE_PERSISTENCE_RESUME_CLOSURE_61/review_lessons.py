"""Append-only evidence reviews using the authenticated register event schema."""
import json,pathlib,hashlib,copy
E=pathlib.Path(__file__).parent;P=pathlib.Path('docs/plans');p=P/'PLANNER_REASONING_LESSONS_REGISTER_1.json';md=P/'PLANNER_REASONING_LESSONS_REGISTER_1.md'
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
r=json.loads(p.read_text());original=copy.deepcopy(r);prev='0'*64
for e in r['EVENTS']:
 assert e['PREVIOUS_EVENT_HASH']==prev and digest({k:v for k,v in e.items() if k!='EVENT_HASH'})==e['EVENT_HASH'];prev=e['EVENT_HASH']
sealed=json.loads((E.parent/'E2_P05_D01_A15_INDEPENDENT_AFTER_STATE_ORACLE_60/lessons-register-snapshot.json').read_text())
assert r['EVENTS'][:len(sealed['EVENTS'])]==sealed['EVENTS']
assert [e['LESSON']['LESSON_ID'] for e in r['EVENTS'] if e['EVENT_TYPE']=='LESSON_RECORDED']==['LL-'+str(i).zfill(2) for i in range(1,11)]
evidence={'path':str(E/'readiness-gates.json'),'raw_sha256':hashlib.sha256((E/'readiness-gates.json').read_bytes()).hexdigest()}
notes={1:('SUPPORTING_EVIDENCE','Work addresses the two previously isolated blockers and prepares a bounded authority subject; the aggregate operand frontier remains unchanged by design.'),2:('NO_NEW_EVIDENCE','No new qualification strategy was selected; the retained prospective scenario was reused.'),3:('SUPPORTING_EVIDENCE','Four actual ResumeEligibility fields are separated from candidate labels that the schema does not expose.'),4:('SUPPORTING_EVIDENCE','Capture carrier and complete resume-route comparison close two shared static blockers for both variants.'),5:('SUPPORTING_EVIDENCE','Conditional prospective expectations are separate from observed historical occurrences and still require scope adoption.'),6:('SUPPORTING_EVIDENCE','Persistence capabilities from A14 do not supply A15 authority; static readiness is not an execution grant.'),7:('NO_NEW_EVIDENCE','Operand frontier stays 109/52; static oracle/harness closure is distinct assurance progress, not runtime qualification.'),8:('NO_NEW_EVIDENCE','No new typed-identity collision was found.'),9:('SUPPORTING_EVIDENCE','FINISH BLOCKED/PLAN_DEFECT and global resume reasons for completed E2-REENTER are independently compared; no FINISH-specific reason is invented.'),10:('SUPPORTING_EVIDENCE','Complete capture result is bound to the updated PersistenceBundle at post-record and post-restore; byte and reason-order negatives reject partial carriers.')}
reviews=[]
if not any(e.get('WORK_PACKAGE')=='61' for e in r['EVENTS']):
 for i,(classification,note) in notes.items():
  e={'EVENT_TYPE':'LESSON_EVIDENCE_REVIEW','WORK_PACKAGE':'61','PREVIOUS_EVENT_HASH':prev,'REVIEW':{'LESSON_ID':'LL-'+str(i).zfill(2),'CLASSIFICATION':classification,'OBSERVATION':note,'EVIDENCE':evidence,'CAUSE_PROVEN':False}}
  e['EVENT_HASH']=digest(e);r['EVENTS'].append(e);prev=e['EVENT_HASH'];reviews.append(e)
 p.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
 with md.open('a') as f:
  f.write('\n## Package 61 — Capture, persistence, and resume evidence review\n\n')
  for i,(classification,note) in notes.items():f.write('- LL-'+str(i).zfill(2)+' — '+classification+': '+note+'\n')
  f.write('\nNo new lesson is appended. Static contract agreement supplies no observed runtime outcome and proves no causal hypothesis. Append-only review head: `'+prev+'`.\n')
assert r['EVENTS'][:len(original['EVENTS'])]==original['EVENTS']
(E/'lessons-register-snapshot.json').write_text(p.read_text());(E/'lessons-register-snapshot.md').write_text(md.read_text())
(E/'reasoning-lessons-evidence-update.json').write_text(json.dumps({'LESSONS_REVIEWED':10,'NEW_LESSONS':0,'LL_10_REGISTERED':True,'PRIOR_EVENT_COUNT':len(sealed['EVENTS']),'PRIOR_EVENTS_PRESERVED':True,'REVIEW_EVENTS':[e for e in r['EVENTS'] if e.get('WORK_PACKAGE')=='61'],'HEAD':prev,'CAUSAL_HYPOTHESES_PROVEN':False},sort_keys=True,indent=2)+'\n')
print(json.dumps({'REVIEWED':10,'NEW_LESSONS':0,'HEAD':prev}))
