"""Read-only documentary authority verifier. No native Planner operations."""
import copy, hashlib, json, pathlib, subprocess, sys
ROOT=pathlib.Path(__file__).resolve().parents[4]
D=pathlib.Path(__file__).resolve().parent
P=ROOT/'docs/plans/qualification/E2_P05_D01_A15_BOUNDED_AUTHORITY_DECISION_PREPARATION_67'
L=ROOT/'docs/plans/qualification/KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_ADOPTION_66'
def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest()
def read(p): return json.loads(p.read_text())
def pin(p): return {'PATH':str(p.relative_to(ROOT)), 'RAW_SHA256':hashlib.sha256(p.read_bytes()).hexdigest()}
def identity(ns,x): return {'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':ns,'sha256':digest(x)}
def inputs():
 for name in ['E2_P05_D01_A15_BOUNDED_AUTHORITY_DECISION_PREPARATION_67','KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_ADOPTION_66','KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_65']:
  index=read(ROOT/'docs/plans/qualification'/name/'evidence-index.json')
  for path,h in index['FILES'].items(): assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h, path
 charter=json.loads(subprocess.check_output([sys.executable,str((L/'reader.py').relative_to(ROOT))],cwd=str(ROOT)))
 assert charter['CHARTER_EFFECTIVE'] and charter['TRANSITIONS_PERSISTED']==3
 dossier=read(P/'unselected-normative-scope-decision-dossier.json'); subject=read(P/'normative-adoption-subject.json')
 assert subject['IDENTITY']==identity('qualification-A15-normative-adoption-subject-v1',subject['CONTENT'])
 assert subject['IDENTITY']['sha256']=='b83a133c612f690f433e64b4e4f2788369851466d850cfdb7a6fb135d6f8e30d'
 assert dossier['NORMATIVE_SUBJECT_IDENTITY']==subject['IDENTITY'] and dossier['NORMATIVE_SUBJECT_PIN']==dict(pin(P/'normative-adoption-subject.json'),SOURCE_POINTER='/')
 assert dossier['DECISION_READY'] and not dossier['ANY_OPTION_SELECTED']
 assert dossier['CHARTER_CONTENT_IDENTITY']==charter['CHARTER_CONTENT_IDENTITY']
 assert dossier['EFFECTIVE_CHARTER_RECORD_IDENTITY']==charter['ORDERED_LIFECYCLE'][-1]['EVIDENCE_IDENTITY']
 return charter,dossier,subject

def verify(envelope,decision,source,duplicates=1):
 charter,dossier,subject=inputs(); r=envelope['RECORD']
 assert duplicates==1,'duplicate adoption'
 assert envelope['IDENTITY']==identity('qualification-A15-normative-adoption-record-v1',r),'record identity'
 assert decision['IDENTITY']==identity('qualification-A15-owner-normative-decision-v1',decision['CONTENT'])
 dc=decision['CONTENT']; assert dc['SOURCE_PIN']==pin(source)
 assert 'AUTHORIZE_BOUNDED_PROSPECTIVE_A15_NORMATIVE_SCOPE' in source.read_text()
 for field,h in [('NORMATIVE_SUBJECT','b83a133c612f690f433e64b4e4f2788369851466d850cfdb7a6fb135d6f8e30d'),('GOVERNING_CHARTER','d26962c58f17281173e965433dae63a941e078115f3dcc30e2a3512fa21812b8'),('EFFECTIVE_LIFECYCLE','a27516baa0ab7f34a36a1130490b6cfa38c508975ca337e0824c8eac33715cbb'),('TECHNICAL_SUBJECT','befe07aacc6b4c4e203488bce731f265a0520cf145174dca33dbfb4e68b43e9b')]:
  assert dc[field]['sha256']==h and h in source.read_text()
 assert dc['SOURCE_KIND']=='CURRENT_CONVERSATION_USER_MESSAGE' and dc['ISSUER_ROLE']==dossier['ISSUER_ROLE']
 assert dc['OPTION_ID']==dossier['OPTIONS'][0]['OPTION_ID'] and dc['MANDATE']=='NORMATIVE_SCOPE_ONLY'
 assert dc['OFFERED_DOSSIER_PIN']==pin(P/'unselected-normative-scope-decision-dossier.json')
 assert r['NORMATIVE_SUBJECT']==subject['IDENTITY'] and r['NORMATIVE_SUBJECT_PIN']==pin(P/'normative-adoption-subject.json')
 assert r['GOVERNING_CHARTER']==dc['GOVERNING_CHARTER'] and r['EFFECTIVE_LIFECYCLE']==dc['EFFECTIVE_LIFECYCLE']
 assert r['TECHNICAL_SUBJECT']==dossier['EXACT_A15_TECHNICAL_SUBJECT']
 assert r['OWNER_DECISION']==decision['IDENTITY'] and r['OWNER_DECISION_PIN']==pin(D/'project-owner-decision.json')
 assert r['OPTION_ID']==dc['OPTION_ID'] and r['ISSUER_ROLE']==dc['ISSUER_ROLE']
 assert r['MANDATE']=='NORMATIVE_SCOPE_ONLY' and r['STATUS']=='ADOPTION_RECORDED_PENDING_INDEPENDENT_EFFECTIVENESS_VERIFICATION'
 assert r['ADOPTED_CONTENT']==subject['CONTENT'], 'scope/protection/exclusions changed'
 assert r['EXECUTION_GRANT'] is None and r['CAPTURE_GRANT'] is None
 assert r['EFFECTIVENESS_RULE']=='Only after immutable persistence, independent reread, four-seed agreement and all negative controls pass; no backdating'
 assert r['PREDECESSOR_ADOPTION'] is None
 assert r['PROHIBITED_OPERATIONS']==['native invalidation','apply_event','record_result','capture/save/restore/replay','writer/cold-reader operations','baseline amendment','V3/Planner runtime modification','E1 modification','production/external-system effects']
 return {'RESULT':'PASS','ADOPTION_RECORD_IDENTITY':envelope['IDENTITY'],'OWNER_DECISION_IDENTITY':decision['IDENTITY'],'NORMATIVE_SUBJECT':subject['IDENTITY'],'MANDATE':'NORMATIVE_SCOPE_ONLY','CHARTER_LIFECYCLE_VERIFIED':True,'EXECUTION_AUTHORITY':False,'CAPTURE_AUTHORITY':False}

def conflicts():
 found=[]
 # Explicit issued/adopted records; retained proposals are not grants.
 for p in (ROOT/'docs/plans').rglob('*.json'):
  if D in p.parents: continue
  raw=p.read_bytes()
  if b'b83a133c612f690f433e64b4e4f2788369851466d850cfdb7a6fb135d6f8e30d' not in raw: continue
  obj=json.loads(raw)
  def walk(x):
   if isinstance(x,dict):
    if any(x.get(k) is True for k in ['NORMATIVE_ADOPTED','NORMATIVE_MANDATE_EFFECTIVE','A15_NORMATIVE_AUTHORITY_ISSUED']) or x.get('STATUS') in ['ISSUED','REVOKED','SUPERSEDED','ADOPTED']: found.append(str(p.relative_to(ROOT)))
    for v in x.values(): walk(v)
   elif isinstance(x,list):
    for v in x: walk(v)
  walk(obj)
 assert not found, 'conflicting authority records: '+repr(found)
 return {'RESULT':'PASS','CONFLICTING_OR_PRIOR_ADOPTIONS':found,'SCAN_BOUNDARY':'docs/plans JSON, explicit authority state only; Package68 records verified separately'}
if __name__=='__main__':
 conflicts()
 records=list(D.glob('normative-adoption-record-*.json'))
 assert len(records)==1
 out=verify(read(records[0]),read(D/'project-owner-decision.json'),D/'project-owner-decision-source.txt',len(records))
 print(json.dumps(out,sort_keys=True))
