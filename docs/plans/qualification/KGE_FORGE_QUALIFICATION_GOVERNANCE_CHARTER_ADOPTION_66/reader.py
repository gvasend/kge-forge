"""Separate read-only lifecycle verifier. No native Planner imports/operations.
--candidate consumes a proposed transition from stdin before publication.
Default mode independently reconstructs only the actually persisted prefix.
"""
import pathlib,json,hashlib,sys,subprocess
P=pathlib.Path('docs/plans');E=pathlib.Path(__file__).parent;D=P/'qualification/KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_65';HASH='d26962c58f17281173e965433dae63a941e078115f3dcc30e2a3512fa21812b8'
def read(p):return json.loads(pathlib.Path(p).read_text())
def cb(v):return ''.join(json.JSONEncoder(sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).iterencode(v)).encode()
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def need(ok,why):
 if not ok:raise ValueError(why)
def aid(v,ns):return {'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':ns,'sha256':hashlib.sha256(cb(v)).hexdigest()}
def raw_id(path):return {'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':'raw-file-sha256','sha256':sha(path)}
index=read(D/'evidence-index.json')['FILES'];need(all(sha(p)==h for p,h in index.items()),'PACKAGE65_CHANGED')
content=read(D/'charter-content.json');charter=aid(content,'kge-forge-qualification-governance-charter-v1');need(charter['sha256']==HASH,'WRONG_CHARTER_CONTENT')
dossier=read(D/'charter-adoption-decision-dossier.json');need(dossier['SUBJECT_CONTENT_IDENTITY']==charter and dossier['SELECTION'] is None,'ORIGINAL_DOSSIER_CHANGED')
initial=read(D/'charter-content-identity.json');need(initial['CURRENT_STATE']=='DRAFT' and initial['CHARTER_APPROVAL_IDENTITY'] is None,'NOT_INITIAL_DRAFT')
source=(E/'owner-adoption-decision-source.txt').read_text();decision=read(E/'owner-adoption-decision.json');decision_id=aid(decision,'kge-forge-charter-owner-adoption-decision-v1')
need('The project owner explicitly selected:' in source and '`ADOPT_KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_V1_0`' in source and HASH in source and 'adoption lifecycle only' in source,'OWNER_DECISION_SOURCE')
need(decision['SELECTED_OPTION']=='ADOPT_KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_V1_0' and decision['APPROVED_CONTENT_IDENTITY']==charter and decision['CHARTER_VERSION']=='1.0','WRONG_OWNER_DECISION')
need(decision['ACTOR_AUTHORIZED_ROLE']==dossier['ISSUING_ROLE'] and decision['REVIEW_ACKNOWLEDGED'] and decision['SCOPE_EXCLUSIONS_APPROVED'] and decision['ORDERED_EFFECTIVENESS_AUTHORIZED'],'WRONG_OWNER_AUTHORITY')
need(not decision['A15_AUTHORITY_ISSUED'] and decision['AUTHORIZATION_LIMIT']=='Charter adoption lifecycle only','DECISION_SCOPE_EXPANSION')
need(decision['QUALIFICATION_SCOPE']==content['QUALIFICATION_SCOPE'] and decision['EXCLUSIONS']==content['EXCLUSIONS'] and decision['ADOPTION_DOSSIER_PIN']['RAW_SHA256']==sha(D/'charter-adoption-decision-dossier.json'),'DECISION_SCOPE_EXCLUSIONS_OR_DOSSIER')
need(decision['SOURCE_PIN']['RAW_SHA256']==sha(E/'owner-adoption-decision-source.txt') and decision['OWNER_DECLARATION_PIN']==dossier['OWNER_DECLARATION_PIN'],'OWNER_PROVENANCE')
policy=read(D/'charter-lifecycle-specification.json');pairs=[('DRAFT','REVIEWED'),('REVIEWED','APPROVED'),('APPROVED','EFFECTIVE')]
original_draft_id=raw_id(D/'charter-content-identity.json')
# Independently check the retained baseline conflict audit and search for
# conflicting actual charter transitions outside this authorized journal.
audit=read(E/'initial-state-conflict-audit.json');need(audit['INITIAL_STATE']=='DRAFT' and not audit['CONFLICTING_TRANSITION_APPROVAL_REVOCATION_RECORDS'],'INITIAL_CONFLICT')
for pin in audit['CHECKED_LOCAL_CHARTER_HASH_RECORDS']:need(sha(pin['PATH'])==pin['RAW_SHA256'],'BASELINE_CONFLICT_AUDIT_SOURCE_CHANGED')
scan=subprocess.run(['rg','-l','--fixed-strings',HASH,str(P),'--glob','*.json'],text=True,capture_output=True,check=False);need(scan.returncode in (0,1),'CONFLICT_SCAN_FAILED')
for name in scan.stdout.splitlines():
 path=pathlib.Path(name)
 if E in path.parents or path.name in ('KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_ADOPTION_66.json',):continue
 def conflict(v):
  if isinstance(v,dict):
   if isinstance(v.get('charter_content_identity'),dict) and v['charter_content_identity'].get('sha256')==HASH and 'from_state' in v and 'to_state' in v:raise ValueError('FOREIGN_LIFECYCLE_CONFLICT:'+str(path))
   if isinstance(v.get('CHARTER_CONTENT_IDENTITY'),dict) and v['CHARTER_CONTENT_IDENTITY'].get('sha256')==HASH and (v.get('CHARTER_ADOPTED') is True or v.get('CHARTER_EFFECTIVE') is True or v.get('CURRENT_STATE') in ('APPROVED','EFFECTIVE','REVOKED','SUPERSEDED')):raise ValueError('FOREIGN_ADOPTION_OR_REVOCATION:'+str(path))
   for child in v.values():conflict(child)
  elif isinstance(v,list):
   for child in v:conflict(child)
 conflict(read(path))
files=sorted(E.glob('lifecycle-*.json'));prefix=[];state='DRAFT';prior=original_draft_id
for position,path in enumerate(files,1):
 doc=read(path);record=doc['RECORD'];identity=aid(record,'kge-forge-charter-lifecycle-record-v1')
 need(doc['IDENTITY']==identity and path.name=='lifecycle-'+str(position).zfill(4)+'-'+record['to_state'].lower()+'-'+identity['sha256']+'.json','LIFECYCLE_ID_OR_FILENAME')
 need(position<=3 and record['transition_ordinal']==position and (record['from_state'],record['to_state'])==pairs[position-1],'TRANSITION_SKIPPED_OR_CONFLICT')
 need(record['charter_content_identity']==charter and record['charter_version']=='1.0' and record['predecessor_lifecycle_record_identity']==prior,'WRONG_CHARTER_OR_PREDECESSOR')
 need(record['actor_identity_or_authorized_role']==dossier['ISSUING_ROLE'] and record['decision_evidence_identity']==decision_id,'WRONG_ACTOR_OR_DECISION')
 need(record['historical_exclusions']==content['EXCLUSIONS'] and record['scope']==content['QUALIFICATION_SCOPE'],'SCOPE_EXCLUSIONS_CHANGED')
 for k in policy['EVENT_REQUIRED_FIELDS']:need(k in record,'MISSING_LIFECYCLE_FIELD:'+k)
 need(record['actor_authority_evidence']['OWNER_DECLARATION_PIN']==dossier['OWNER_DECLARATION_PIN'] and record['actor_authority_evidence']['OWNER_DECISION_PIN']['RAW_SHA256']==sha(E/'owner-adoption-decision.json'),'ACTOR_EVIDENCE')
 need(record['independent_qualification_evidence']==dossier['INDEPENDENT_QUALIFICATION_EVIDENCE'],'QUALIFICATION_PIN_MISMATCH')
 need(record['effective_boundary']['NO_BACKDATING'] and record['effective_boundary']['ONLY_AFTER_ORDERED_VALIDATION_AND_PUBLICATION'],'EARLY_EFFECTIVENESS')
 need(record['A15_GRANTS_ISSUED']==[] and not record['A15_EXECUTED'],'A15_GRANT_OR_EXECUTION')
 prefix.append({'PATH':str(path),'IDENTITY':identity,'FROM':state,'TO':record['to_state']});state=record['to_state'];prior=identity
if '--candidate' in sys.argv:
 candidate=json.loads(sys.stdin.read());r=candidate['RECORD'];identity=aid(r,'kge-forge-charter-lifecycle-record-v1');n=len(prefix)+1
 need(n<=3 and candidate['IDENTITY']==identity,'CANDIDATE_ID_OR_AFTER_EFFECTIVE')
 need(r['transition_ordinal']==n and (r['from_state'],r['to_state'])==pairs[n-1] and r['predecessor_lifecycle_record_identity']==prior,'CANDIDATE_WRONG_ORDER_OR_PREDECESSOR')
 need(r['charter_content_identity']==charter and r['charter_version']=='1.0' and r['actor_identity_or_authorized_role']==dossier['ISSUING_ROLE'] and r['decision_evidence_identity']==decision_id,'CANDIDATE_AUTHORITY')
 need(all(k in r for k in policy['EVENT_REQUIRED_FIELDS']) and r['historical_exclusions']==content['EXCLUSIONS'] and r['scope']==content['QUALIFICATION_SCOPE'],'CANDIDATE_SCOPE_FIELDS')
 need(r['independent_qualification_evidence']==dossier['INDEPENDENT_QUALIFICATION_EVIDENCE'] and r['actor_authority_evidence']['OWNER_DECLARATION_PIN']==dossier['OWNER_DECLARATION_PIN'] and r['actor_authority_evidence']['OWNER_DECISION_PIN']['RAW_SHA256']==sha(E/'owner-adoption-decision.json'),'CANDIDATE_EVIDENCE')
 need(r['effective_boundary']['NO_BACKDATING'] and r['effective_boundary']['ONLY_AFTER_ORDERED_VALIDATION_AND_PUBLICATION'] and r['A15_GRANTS_ISSUED']==[] and not r['A15_EXECUTED'],'CANDIDATE_EFFECT_BOUNDARY')
 result={'RESULT':'PASS_CANDIDATE','PERSISTED_STATE':state,'CANDIDATE_STATE':r['to_state'],'CANDIDATE_IDENTITY':identity,'PERSISTED_PREFIX_LENGTH':len(prefix)}
else:
 if state=='EFFECTIVE' and (E/'effective-charter-reference.json').exists():
  effective=read(E/'effective-charter-reference.json')
  need(effective['CHARTER_CONTENT_IDENTITY']==charter and effective['EFFECTIVE_LIFECYCLE_IDENTITY']==prior and effective['CHARTER_VERSION']=='1.0' and effective['AUTHORITY_SCOPE']==content['QUALIFICATION_SCOPE'] and effective['EXCLUSIONS']==content['EXCLUSIONS'],'EFFECTIVE_REFERENCE_MISMATCH')
  need(effective['CHARTER_EFFECTIVE'] and effective['CHARTER_ADOPTED'] and not effective['A15_NORMATIVE_AUTHORITY_ISSUED'] and not effective['A15_EXECUTION_AUTHORITY_ISSUED'] and not effective['A15_CAPTURE_AUTHORITY_ISSUED'] and not effective['A15_EXECUTED'],'EFFECTIVE_REFERENCE_GRANT')
 result={'RESULT':'PASS_PERSISTED_PREFIX','CURRENT_STATE':state,'ORDERED_LIFECYCLE':[{'STATE':'DRAFT','EVIDENCE_IDENTITY':original_draft_id}]+[{'STATE':x['TO'],'EVIDENCE_IDENTITY':x['IDENTITY']} for x in prefix],'CHARTER_CONTENT_IDENTITY':charter,'CHARTER_VERSION':'1.0','OWNER_DECISION_IDENTITY':decision_id,'TRANSITIONS_PERSISTED':len(prefix),'CHARTER_EFFECTIVE':state=='EFFECTIVE' and len(prefix)==3,'SCOPE':content['QUALIFICATION_SCOPE'],'EXCLUSIONS':content['EXCLUSIONS'],'A15_NORMATIVE_AUTHORITY_ISSUED':False,'A15_EXECUTION_AUTHORITY_ISSUED':False,'A15_CAPTURE_AUTHORITY_ISSUED':False,'A15_EXECUTED':False}
print(json.dumps(result,sort_keys=True))
