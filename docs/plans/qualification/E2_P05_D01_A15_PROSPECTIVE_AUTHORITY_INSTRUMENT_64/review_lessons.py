"""Append-only review of existing lessons, no new lesson or issuer declaration."""
import pathlib,json,hashlib,copy
P=pathlib.Path('docs/plans');E=pathlib.Path(__file__).parent;C=E.parent/'E2_P05_D01_A15_AUTHORITY_ROOT_RECONCILIATION_63';p=P/'PLANNER_REASONING_LESSONS_REGISTER_1.json';md=P/'PLANNER_REASONING_LESSONS_REGISTER_1.md'
def h(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
r=json.loads(p.read_text());old=copy.deepcopy(r);prior=json.loads((C/'lessons-register-snapshot.json').read_text());assert r['EVENTS'][:len(prior['EVENTS'])]==prior['EVENTS'];head='0'*64
for e in r['EVENTS']:
 assert e['PREVIOUS_EVENT_HASH']==head and h({k:v for k,v in e.items() if k!='EVENT_HASH'})==e['EVENT_HASH'];head=e['EVENT_HASH']
assert len([e for e in r['EVENTS'] if e['EVENT_TYPE']=='LESSON_RECORDED'])==10
notes={1:('SUPPORTING_EVIDENCE','The exact scoped qualification subject is retained; incomplete authority is left at the external governance boundary rather than reopening historical graph recovery.'),2:('NO_NEW_EVIDENCE','No new strategy or measured cost improvement is established.'),3:('SUPPORTING_EVIDENCE','Complete schema and exact mandate content remain distinct from missing current issuer power, governing adoption and composition authority.'),4:('SUPPORTING_EVIDENCE','External issuer/mandate evidence is compressed into one precise gap with independently typed subfields, not repeated broad semantic questions.'),5:('SUPPORTING_EVIDENCE','Historical evidence/native declarations remain immutable; the document is a prospective incomplete instrument definition only.'),6:('SUPPORTING_EVIDENCE','Human issuer authentication does not prove authorization for all three mandates; adoption/execution/capture and draft/issued/event/grant identities are separate.'),7:('NO_NEW_EVIDENCE','The operand frontier remains 109/52; definition is not execution or an operand binding promotion.'),8:('SUPPORTING_EVIDENCE','Only actual native IdentityKind/ArtifactIdentity representations are used; mandate metadata is not added to AuthorityClass or GraphEntity.'),9:('NO_NEW_EVIDENCE','Existing proof/control/resume output distinctions remain unchanged; no native observation is made.'),10:('SUPPORTING_EVIDENCE','Exact oracle/harness/protection identities are bound into an unissued instrument draft; non-circular hashes and structure validation cannot authenticate issuer power.')}
evidence={'path':str(E/'proposed-instrument-content.json'),'raw_sha256':hashlib.sha256((E/'proposed-instrument-content.json').read_bytes()).hexdigest()}
if not any(e.get('WORK_PACKAGE')=='64' for e in r['EVENTS']):
 for i,(classification,note) in notes.items():
  e={'EVENT_TYPE':'LESSON_EVIDENCE_REVIEW','WORK_PACKAGE':'64','PREVIOUS_EVENT_HASH':head,'REVIEW':{'LESSON_ID':'LL-'+str(i).zfill(2),'CLASSIFICATION':classification,'OBSERVATION':note,'EVIDENCE':evidence,'CAUSE_PROVEN':False}};e['EVENT_HASH']=h(e);r['EVENTS'].append(e);head=e['EVENT_HASH']
 p.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
 with md.open('a') as f:
  f.write('\n## Package 64 — Prospective instrument definition review\n\n')
  for i,(classification,note) in notes.items():f.write('- LL-'+str(i).zfill(2)+' — '+classification+': '+note+'\n')
  f.write('\nNo new lesson, quantified benefit or validated causal attribution is claimed. Issuing authority must be independently evidenced outside the proposed instrument. Review head: `'+head+'`.\n')
assert r['EVENTS'][:len(old['EVENTS'])]==old['EVENTS']
(E/'lessons-register-snapshot.json').write_text(p.read_text());(E/'lessons-register-snapshot.md').write_text(md.read_text())
(E/'reasoning-lessons-evidence-update.json').write_text(json.dumps({'LESSONS_REVIEWED':10,'NEW_LESSONS':0,'PRIOR_EVENTS_PRESERVED':True,'LL_10_PRESERVED':True,'PRIOR_EVENT_COUNT':len(prior['EVENTS']),'HEAD':head,'REVIEWS':[e for e in r['EVENTS'] if e.get('WORK_PACKAGE')=='64'],'CAUSAL_ATTRIBUTION_VALIDATED':False},sort_keys=True,indent=2)+'\n')
print(json.dumps({'LESSONS_REVIEWED':10,'NEW_LESSONS':0,'HEAD':head}))
