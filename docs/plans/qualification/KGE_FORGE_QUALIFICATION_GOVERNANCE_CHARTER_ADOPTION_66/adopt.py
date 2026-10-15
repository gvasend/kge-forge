"""Authorized documentary charter lifecycle only. Stop on any validation failure.
Each transition is independently validated BEFORE immutable publication, then
reread by a fresh verifier BEFORE proceeding. No native A15 operation occurs.
"""
import pathlib,json,hashlib,os,tempfile,subprocess,sys
P=pathlib.Path('docs/plans');E=pathlib.Path(__file__).parent;D=P/'qualification/KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_65';HASH='d26962c58f17281173e965433dae63a941e078115f3dcc30e2a3512fa21812b8'
def read(p):return json.loads(pathlib.Path(p).read_text())
def cb(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def pin(p):return {'PATH':str(p),'RAW_SHA256':sha(p)}
def aid(v,ns):return {'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':ns,'sha256':hashlib.sha256(cb(v)).hexdigest()}
def immutable(path,value):
 raw=json.dumps(value,sort_keys=True,indent=2,ensure_ascii=False).encode()+b'\n';path=pathlib.Path(path)
 if path.exists():raise ValueError('Conflicting/preexisting publication: '+str(path))
 if path.is_symlink() or path.resolve()!=path.absolute():raise ValueError('Symlink publication: '+str(path))
 fd,name=tempfile.mkstemp(prefix='.charter-staging-',dir=path.parent)
 try:
  with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
  os.link(name,path)
  os.unlink(name)
  dfd=os.open(path.parent,os.O_RDONLY|os.O_DIRECTORY)
  try:os.fsync(dfd)
  finally:os.close(dfd)
 except BaseException:
  if os.path.exists(name):os.unlink(name)
  raise
 if path.read_bytes()!=raw:raise ValueError('Published bytes mismatch')
def reader(candidate=None):
 args=[sys.executable,str(E/'reader.py')]+(['--candidate'] if candidate else [])
 p=subprocess.run(args,input=json.dumps(candidate) if candidate else None,text=True,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),check=True)
 return json.loads(p.stdout)
# Authenticate all sealed input bytes, exact canonical body and approval subject.
sealed=read(D/'evidence-index.json')['FILES'];assert all(sha(p)==h for p,h in sealed.items())
content=read(D/'charter-content.json');charter=aid(content,'kge-forge-qualification-governance-charter-v1');assert charter['sha256']==HASH
initial=read(D/'charter-content-identity.json');policy=read(D/'charter-lifecycle-specification.json');dossier=read(D/'charter-adoption-decision-dossier.json')
assert initial['CURRENT_STATE']==policy['CURRENT_LIFECYCLE_STATE']=='DRAFT' and dossier['SELECTION'] is None and dossier['SUBJECT_CONTENT_IDENTITY']==charter
assert dossier['DECISION_READY'] and dossier['OPTIONS'][0]['OPTION_ID']=='ADOPT_KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_V1_0'
# Conflict search covers local retained JSON records carrying this charter hash.
# Requirement text in draft schemas is not an actual occurrence/approval record.
scan=subprocess.run(['rg','-l','--fixed-strings',HASH,str(P),'--glob','*.json'],text=True,capture_output=True,check=False)
assert scan.returncode in (0,1)
checked=[];conflicts=[]
for name in scan.stdout.splitlines():
 p=pathlib.Path(name);v=read(p);checked.append(pin(p))
 def inspect(x):
  if isinstance(x,dict):
   if isinstance(x.get('charter_content_identity'),dict) and x['charter_content_identity'].get('sha256')==HASH and 'from_state' in x and 'to_state' in x:conflicts.append(str(p))
   if isinstance(x.get('CHARTER_CONTENT_IDENTITY'),dict) and x['CHARTER_CONTENT_IDENTITY'].get('sha256')==HASH and (x.get('CHARTER_ADOPTED') is True or x.get('CHARTER_EFFECTIVE') is True or x.get('CURRENT_STATE') in ('APPROVED','EFFECTIVE','REVOKED','SUPERSEDED')):conflicts.append(str(p))
   for child in x.values():inspect(child)
  elif isinstance(x,list):
   for child in x:inspect(child)
 inspect(v)
assert not conflicts,conflicts
assert not list(E.glob('lifecycle-*.json')) and not (E/'effective-charter-reference.json').exists()
immutable(E/'initial-state-conflict-audit.json',{'RESULT':'PASS','CANONICAL_HASH':HASH,'INITIAL_STATE':'DRAFT','DRAFT_STATE_EVIDENCE':pin(D/'charter-content-identity.json'),'DRAFT_LIFECYCLE_EVIDENCE':pin(D/'charter-lifecycle-specification.json'),'CHECKED_LOCAL_CHARTER_HASH_RECORDS':checked,'CONFLICTING_TRANSITION_APPROVAL_REVOCATION_RECORDS':conflicts,'LOCAL_RETAINED_EVIDENCE_ONLY':True,'PACKAGE65_SEALS_VERIFIED':len(sealed),'NO_STATIC_PASS_USED_AS_ADOPTION':True})
owner={'SCHEMA_ID':'KGE-FORGE-OWNER-CHARTER-ADOPTION-DECISION-1','WORK_PACKAGE':'KGE-FORGE-QUALIFICATION-GOVERNANCE-CHARTER-ADOPTION-66','SOURCE_KIND':'EXPLICIT_PROJECT_OWNER_SELECTION_VIA_USER_ROLE_CURRENT_CONVERSATION','SOURCE_PIN':pin(E/'owner-adoption-decision-source.txt'),'SELECTED_OPTION':'ADOPT_KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_V1_0','APPROVED_CONTENT_IDENTITY':charter,'CHARTER_VERSION':'1.0','ACTOR_AUTHORIZED_ROLE':dossier['ISSUING_ROLE'],'OWNER_DECLARATION_PIN':dossier['OWNER_DECLARATION_PIN'],'ADOPTION_DOSSIER_PIN':pin(D/'charter-adoption-decision-dossier.json'),'REVIEW_ACKNOWLEDGED':True,'SCOPE_EXCLUSIONS_APPROVED':True,'ORDERED_EFFECTIVENESS_AUTHORIZED':True,'QUALIFICATION_SCOPE':content['QUALIFICATION_SCOPE'],'EXCLUSIONS':content['EXCLUSIONS'],'AUTHORIZATION_LIMIT':'Charter adoption lifecycle only','EFFECTIVENESS_CONDITION':'After all three ordered transitions have been independently validated and persisted; no earlier/retroactive effect','A15_AUTHORITY_ISSUED':False,'NAMED_PERSON_SIGNATURE_MESSAGE_ID_INVENTED':False}
immutable(E/'owner-adoption-decision.json',owner);decision_id=aid(owner,'kge-forge-charter-owner-adoption-decision-v1')
# Independently establish initial DRAFT after decision capture, before any step.
start=reader();assert start['CURRENT_STATE']=='DRAFT' and start['TRANSITIONS_PERSISTED']==0
immutable(E/'initial-independent-state-verification.json',start)
last_state='DRAFT';predecessor={'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':'raw-file-sha256','sha256':sha(D/'charter-content-identity.json')};transitions=[]
try:
 for ordinal,(before,after) in enumerate([('DRAFT','REVIEWED'),('REVIEWED','APPROVED'),('APPROVED','EFFECTIVE')],1):
  record={'SCHEMA_ID':policy['SCHEMA_ID'],'transition_ordinal':ordinal,'charter_content_identity':charter,'charter_version':'1.0','from_state':before,'to_state':after,'actor_identity_or_authorized_role':dossier['ISSUING_ROLE'],'actor_authority_evidence':{'OWNER_DECLARATION_PIN':dossier['OWNER_DECLARATION_PIN'],'OWNER_DECISION_PIN':pin(E/'owner-adoption-decision.json'),'ROOT_BASIS':'Explicit project-owner declaration and current exact adoption selection; not a derived static PASS'},'decision_evidence_identity':decision_id,'effective_boundary':{'ONLY_AFTER_ORDERED_VALIDATION_AND_PUBLICATION':True,'NO_BACKDATING':True,'CHARTER_EFFECT_BEGINS':'Only on independently verified complete persisted DRAFT->REVIEWED->APPROVED->EFFECTIVE chain','THIS_STEP_MEANING':{'REVIEWED':'Owner explicitly acknowledged review of exact content and qualification evidence','APPROVED':'Owner explicitly approved exact v1.0 scope/exclusions with exact REVIEWED predecessor','EFFECTIVE':'Owner authorized effectiveness after ordered independent validation/persistence with exact APPROVED predecessor'}[after]},'predecessor_lifecycle_record_identity':predecessor,'historical_exclusions':content['EXCLUSIONS'],'scope':content['QUALIFICATION_SCOPE'],'independent_qualification_evidence':dossier['INDEPENDENT_QUALIFICATION_EVIDENCE'],'A15_GRANTS_ISSUED':[],'A15_EXECUTED':False}
  identity=aid(record,'kge-forge-charter-lifecycle-record-v1');candidate={'IDENTITY':identity,'RECORD':record}
  pre=reader(candidate);assert pre['RESULT']=='PASS_CANDIDATE' and pre['PERSISTED_STATE']==last_state
  immutable(E/(str(ordinal).zfill(4)+'-'+after.lower()+'-prepublication-validation.json'),pre)
  target=E/('lifecycle-'+str(ordinal).zfill(4)+'-'+after.lower()+'-'+identity['sha256']+'.json')
  immutable(target,candidate)
  post=reader();assert post['CURRENT_STATE']==after and post['TRANSITIONS_PERSISTED']==ordinal and post['ORDERED_LIFECYCLE'][-1]['EVIDENCE_IDENTITY']==identity
  # Durable independent post-publication evidence must exist before continuing.
  immutable(E/(str(ordinal).zfill(4)+'-'+after.lower()+'-postpublication-verification.json'),post)
  transitions.append({'STATE':after,'IDENTITY':identity,'PATH':str(target),'VALIDATION':'PASS','PERSISTENCE':'PASS','INDEPENDENT_POSTPUBLICATION':'PASS'})
  last_state=after;predecessor=identity
  print(json.dumps({'TRANSITION':before+' -> '+after,'IDENTITY':identity,'RESULT':'PASS_VALIDATED_PERSISTED_INDEPENDENTLY_REREAD'}),flush=True)
 final=reader();assert final['CHARTER_EFFECTIVE'] and last_state=='EFFECTIVE' and len(transitions)==3
 reference={'SCHEMA_ID':'KGE-FORGE-EFFECTIVE-QUALIFICATION-CHARTER-REFERENCE-1','CHARTER_CONTENT_IDENTITY':charter,'CHARTER_VERSION':'1.0','CHARTER_CONTENT_PIN':pin(D/'charter-content.json'),'CURRENT_LIFECYCLE_STATE':'EFFECTIVE','CHARTER_EFFECTIVE':True,'CHARTER_ADOPTED':True,'OWNER_DECISION_IDENTITY':decision_id,'OWNER_DECISION_PIN':pin(E/'owner-adoption-decision.json'),'EFFECTIVE_LIFECYCLE_IDENTITY':predecessor,'TRANSITIONS':transitions,'EFFECTIVE_BOUNDARY':'Actual Package66 immutable publication and independent reread of all three ordered lifecycle records, with durable post-publication validation evidence; no earlier effect or backdating','AUTHORITY_SCOPE':content['QUALIFICATION_SCOPE'],'RESOURCE_PERMISSION_BOUNDARY':content['RESOURCE_AND_SECURITY_BOUNDARY'],'EXCLUSIONS':content['EXCLUSIONS'],'A15_NORMATIVE_AUTHORITY_ISSUED':False,'A15_EXECUTION_AUTHORITY_ISSUED':False,'A15_CAPTURE_AUTHORITY_ISSUED':False,'A15_EXECUTED':False,'BASELINE_AMENDED':False,'NEXT_BOUNDARY':'BOUNDED_A15_AUTHORITY_DECISION_PREPARATION'}
 immutable(E/'effective-charter-reference.json',reference)
 immutable(E/'final-independent-lifecycle-verification.json',final)
except BaseException as exc:
 failure={'RESULT':'FAIL_STOPPED','LAST_INDEPENDENTLY_VALIDATED_PERSISTED_STATE':last_state,'TRANSITIONS':transitions,'FAILED_WITH':type(exc).__name__+': '+str(exc),'CHARTER_EFFECTIVE_REPORTED':False,'NO_RETRY_OR_ROLLBACK_PERFORMED':True,'A15_GRANTS_ISSUED':[]}
 if not (E/'adoption-failure.json').exists():immutable(E/'adoption-failure.json',failure)
 raise
