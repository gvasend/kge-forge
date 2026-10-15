"""Append-only lesson evidence reviews; no new lesson or permission claim."""
import pathlib,json,hashlib,copy
P=pathlib.Path('docs/plans');E=pathlib.Path(__file__).parent;D=E.parent/'KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_65';p=P/'PLANNER_REASONING_LESSONS_REGISTER_1.json';md=P/'PLANNER_REASONING_LESSONS_REGISTER_1.md'
def h(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
r=json.loads(p.read_text());prior=json.loads((D/'lessons-register-preservation-snapshot.json').read_text());assert r['EVENTS'][:len(prior['EVENTS'])]==prior['EVENTS'];old=copy.deepcopy(r);head='0'*64
for ev in r['EVENTS']:
 assert ev['PREVIOUS_EVENT_HASH']==head and h({k:v for k,v in ev.items() if k!='EVENT_HASH'})==ev['EVENT_HASH'];head=ev['EVENT_HASH']
assert len([ev for ev in r['EVENTS'] if ev['EVENT_TYPE']=='LESSON_RECORDED'])==10
notes={1:('SUPPORTING_EVIDENCE','Effective reusable governance root resolves issuer-policy prerequisites, while separate execution/environment gates remain explicit.'),2:('NO_NEW_EVIDENCE','No new execution strategy or quantified comparison is claimed.'),3:('SUPPORTING_EVIDENCE','Static harness specification, interpreter binary and qualified A15 executable/invocation are distinct types of evidence.'),4:('SUPPORTING_EVIDENCE','The remaining frontier is qualified executor/invocation and sealed environment permissions, not repeated owner/source/authority-root searches.'),5:('SUPPORTING_EVIDENCE','Exact prospective normative-only adoption can be reviewed without asserting historical occurrence or qualifying all historical owners.'),6:('SUPPORTING_EVIDENCE','Effective charter supplies scoped project-owner governance power but no operating-system/external resource permissions or automatic A15 grant.'),7:('SUPPORTING_EVIDENCE','Normative decision becomes ready; execution/capture/combined readiness remains false. Operand accounting stays 109/52 by scope, not a claimed lack of all progress.'),8:('NO_NEW_EVIDENCE','Native typed identities and exact source/charter/instrument domains remain unchanged; no new collision observed.'),9:('NO_NEW_EVIDENCE','Native validation/usability/satisfaction/control/resume comparisons remain preserved; no new native result.'),10:('SUPPORTING_EVIDENCE','Complete independent oracle and capture contracts remain unchanged, but qualified runtime carrier/launcher and resource profile are separate execution prerequisites.')}
evidence={'path':str(E/'decision-readiness.json'),'raw_sha256':hashlib.sha256((E/'decision-readiness.json').read_bytes()).hexdigest()}
if not any(ev.get('WORK_PACKAGE')=='67' for ev in r['EVENTS']):
 for i,(classification,note) in notes.items():
  ev={'EVENT_TYPE':'LESSON_EVIDENCE_REVIEW','WORK_PACKAGE':'67','PREVIOUS_EVENT_HASH':head,'REVIEW':{'LESSON_ID':'LL-'+str(i).zfill(2),'CLASSIFICATION':classification,'OBSERVATION':note,'EVIDENCE':evidence,'CAUSE_PROVEN':False,'COUNTEREVIDENCE':'Static qualification and present-process access observations are not actual native execution qualification or proof of quantified benefit.'}};ev['EVENT_HASH']=h(ev);r['EVENTS'].append(ev);head=ev['EVENT_HASH']
 p.write_text(json.dumps(r,sort_keys=True,indent=2)+'\n')
 with md.open('a') as f:
  f.write('\n## Package 67 — Effective governance and runtime-permission review\n\n')
  for i,(classification,note) in notes.items():f.write('- LL-'+str(i).zfill(2)+' — '+classification+': '+note+'\n')
  f.write('\nCounterevidence: no native A15 executor or environment was qualified/executed here; no quantified benefit or validated cause is asserted. No duplicate/new lesson. Review head: `'+head+'`.\n')
assert r['EVENTS'][:len(old['EVENTS'])]==old['EVENTS']
(E/'lessons-register-snapshot.json').write_text(p.read_text());(E/'lessons-register-snapshot.md').write_text(md.read_text())
(E/'reasoning-lessons-evidence-update.json').write_text(json.dumps({'LESSONS_REVIEWED':10,'NEW_LESSONS':0,'PRIOR_EVENTS_AND_LL_10_PRESERVED':True,'HEAD':head,'REVIEWS':[ev for ev in r['EVENTS'] if ev.get('WORK_PACKAGE')=='67'],'CAUSAL_ATTRIBUTION_VALIDATED':False},sort_keys=True,indent=2)+'\n')
print(json.dumps({'LESSONS_REVIEWED':10,'NEW_LESSONS':0,'HEAD':head}))
