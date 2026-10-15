"""Independent grant reader/validator. No issuer import or bootstrap execution."""
import copy,hashlib,json,pathlib,subprocess,sys
OUT=pathlib.Path(__file__).resolve().parent;OLD=OUT.parent/'bootstrap-trust-authority-89';ROOT=pathlib.Path(__file__).resolve().parents[5]
NS='qualification-h90-bootstrap-construction-inert-issued-grant-v1';APPROVED='596a92d446ae2f4b8de57f02b977302577845586c2a45f40d01479e9827a2b3d';OPTION='AUTHORIZE_MINIMAL_H77_02_BOOTSTRAP_CONSTRUCTION_INERT_TEST'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def aid(x,n):return {'kind':'CONTENT_IDENTITY','namespace':n,'sha256':hashlib.sha256(canon(x)).hexdigest()}
FIELDS={'SCHEMA','WORK_PACKAGE','INSTRUMENT_STATUS','APPROVED_SUBJECT_IDENTITY','APPROVED_SUBJECT_PIN','ISSUER_ROLE','GOVERNING_CHARTER_IDENTITY','EFFECTIVE_CHARTER_LIFECYCLE','NORMATIVE_MANDATE_REFERENCE','ISSUER_AUTHORITY_EVIDENCE','PROJECT_OWNER_DECISION_EVIDENCE','PERMITTED_SOURCE_FILES','PERMITTED_INERT_TESTS','RESOURCE_LIMITS','STORE_REQUIREMENTS','OBSERVER_REQUIREMENTS','ENVIRONMENT_REQUIREMENTS','PHASE_GATES','CAMPAIGN_ENTRY_PREDICATES','ENTRY_RULE','OUTPUT_EVIDENCE_BOUNDARY','NO_RETRY_POLICY','HISTORICAL_EXCLUSIONS','EXPLICIT_EXCLUSIONS','MANDATES','BOOTSTRAP_CONTRACT_PINS','TARGET_COMMAND_PIN','TARGET_COMMAND_EXECUTION_PERMITTED','EFFECTIVE_BOUNDARY','REVOCATION_RULE','ISSUANCE_IS_NOT_BEHAVIORAL_QUALIFICATION','GRANT_IDENTITY_RULE'}
PREDICATES=['TEST_PHASE_AUTHORIZED','EXACT_TEST_SET','SYNTHETIC_FIXTURES_SEALED','INDEPENDENT_EXPECTED_OUTPUTS_SEALED','EXECUTABLE_IDENTITY_VERIFIED','STORE_PERMISSIONS_VERIFIED','DURABILITY_CONTROLS_VERIFIED','RESOURCE_LIMITS_ENFORCEABLE','OBSERVER_BOUNDARY_VERIFIED','CAMPAIGN_ENTRY_VERIFIED','NO_REAL_PROBE_PATH_VERIFIED']
EXCLUSIONS=['system-level or user-level systemd service execution','sudo/privilege escalation','Bubblewrap execution','Package86 probe','actual H77-02 probe','native A15 operations/execution/capture','existing H77 gate/A15 adapter/Planner runtime/V3 modification','production/external effects','automatic retries or additional campaigns','grant self-issuance']
def validate(e,s,d,env,phase):
 assert set(e)=={'GRANT_IDENTITY','RECORD'} and e['GRANT_IDENTITY']==aid(e['RECORD'],NS),'identity'
 b=e['RECORD'];assert set(b)==FIELDS,'missing/extra grant field'
 assert b['SCHEMA']=='BOOTSTRAP-CONSTRUCTION-INERT-ISSUED-GRANT-90-1' and b['WORK_PACKAGE']=='E2-P05-D01-H77-02-BOOTSTRAP-GRANT-ISSUANCE-90'
 assert b['INSTRUMENT_STATUS']=='ISSUED_REQUIRES_SEPARATE_EFFECTIVENESS_REFERENCE','state'
 assert b['APPROVED_SUBJECT_IDENTITY']==s['CONTENT_IDENTITY'] and b['APPROVED_SUBJECT_PIN']=={'path':str((OLD/'proposed-construction-test-authority-subject.json').relative_to(ROOT)),'raw_sha256':sha(OLD/'proposed-construction-test-authority-subject.json')},'subject'
 assert b['ISSUER_ROLE']==s['ISSUER_ROLE']==d['ISSUER_ROLE'] and b['GOVERNING_CHARTER_IDENTITY']==s['EFFECTIVE_CHARTER'] and b['EFFECTIVE_CHARTER_LIFECYCLE']==s['EFFECTIVE_LIFECYCLE'],'issuer/charter'
 assert b['NORMATIVE_MANDATE_REFERENCE']==s['NORMATIVE_REFERENCE']
 cref=ROOT/'docs/plans/qualification/KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_ADOPTION_66/effective-charter-reference.json'
 assert b['ISSUER_AUTHORITY_EVIDENCE']=={'EXISTING_CHARTER_REFERENCE_PIN':{'path':str(cref.relative_to(ROOT)),'raw_sha256':sha(cref)},'DIRECT_ROLE':s['ISSUER_ROLE'],'NO_DELEGATION_OR_CREDENTIAL_INVENTED':True}
 assert b['PROJECT_OWNER_DECISION_EVIDENCE']=={'IDENTITY':d['IDENTITY'],'PIN':{'path':str((OUT/'project-owner-decision-provenance.json').relative_to(ROOT)),'raw_sha256':sha(OUT/'project-owner-decision-provenance.json')}}
 assert b['PERMITTED_SOURCE_FILES']==s['EXACT_SOURCE_PATHS'] and b['PERMITTED_INERT_TESTS']==s['EXACT_SYNTHETIC_TESTS'] and len(b['PERMITTED_SOURCE_FILES'])==2 and len(b['PERMITTED_INERT_TESTS'])==14,'source/test scope'
 assert all(type(v) is int for v in b['RESOURCE_LIMITS'].values())
 assert b['RESOURCE_LIMITS']==s['RESOURCE_LIMITS'] and b['NO_RETRY_POLICY']==0,'resources/retry'
 assert b['ENVIRONMENT_REQUIREMENTS']==env['ENVIRONMENT'],'environment'
 assert b['STORE_REQUIREMENTS']=={k:env['ENVIRONMENT'][k] for k in ['FILESYSTEM_TYPE','CONSUMPTION_STORE_PATH','STORE_PERMISSIONS','CAMPAIGN_ROOT_RULE']},'store'
 assert b['PHASE_GATES']==phase['PHASE_GATES'] and b['CAMPAIGN_ENTRY_PREDICATES']==PREDICATES,'entry gates'
 assert b['OUTPUT_EVIDENCE_BOUNDARY']==s['OUTPUT_BOUNDARY'] and b['BOOTSTRAP_CONTRACT_PINS']==s['CONTRACT_PINS'],'pins/output'
 assert b['HISTORICAL_EXCLUSIONS']==s['HISTORICAL_EXCLUSIONS'] and b['EXPLICIT_EXCLUSIONS']==EXCLUSIONS and b['MANDATES']==s['MANDATES'],'exclusions'
 assert b['TARGET_COMMAND_PIN']==s['TARGET_COMMAND_PIN'] and b['TARGET_COMMAND_EXECUTION_PERMITTED'] is False,'no probe'
 bound=b['EFFECTIVE_BOUNDARY'];assert bound['NO_BACKDATING'] and bound['SOURCE_CONSTRUCTION_ACTIVATED_BY_ISSUANCE'] is False and bound['INERT_TEST_ACTIVATED_BY_ISSUANCE'] is False and bound['REAL_PROBE_PERMISSION_INCLUDED'] is False,'early activation'
 assert b['REVOCATION_RULE']['EXPIRATION_DATE'] is None and b['REVOCATION_RULE']['NO_UNBOUNDED_SCOPE_INFERRED'] is True and 'owner' in b['REVOCATION_RULE']['RULE'],'revocation'
 assert 'unknown/unsupported denies activation' in b['ENTRY_RULE'] and 'own wrapper' in b['GRANT_IDENTITY_RULE']
 assert b['ISSUANCE_IS_NOT_BEHAVIORAL_QUALIFICATION'] is True and env['ENVIRONMENT']['ACTUAL_ENFORCEMENT_VERIFIED'] is False
 assert b['OBSERVER_REQUIREMENTS']=={'EXIT_OBSERVER':read(OLD/'command-specific-coordinator-specification.json')['EXIT_OBSERVER'],'TEST_SCOPE_PIN':{'path':str((OLD/'inert-synthetic-qualification-specification.json').relative_to(ROOT)),'raw_sha256':sha(OLD/'inert-synthetic-qualification-specification.json')},'ACCOUNTING':'exact known fixed child roles/cumulative writes/parent deadlines, independent source-reviewed observer; target success is not sole witness'},'observer'
 return True

def inputs():
 s=read(OLD/'proposed-construction-test-authority-subject.json');assert sha(OLD/'proposed-construction-test-authority-subject.json')=='1db52295406a68d938bb4d4e38b059dd774dcf08903782c411813f0a8363d69e';body=dict(s);sid=body.pop('CONTENT_IDENTITY');assert sid==aid(body,sid['namespace']) and sid['sha256']==APPROVED
 dos=read(OLD/'unselected-authorization-dossier.json');assert dos['SELECTION'] is None and dos['DECISION_READY'] and dos['SUBJECT_IDENTITY']==sid and dos['OPTIONS'][0]['OPTION_ID']==OPTION
 for p in s['CONTRACT_PINS'].values():assert sha(ROOT/p['path'])==p['raw_sha256']
 d=read(OUT/'project-owner-decision-provenance.json');db=dict(d);did=db.pop('IDENTITY');assert did==aid(db,'qualification-h90-bootstrap-owner-decision-v1') and d['SELECTION']==OPTION and d['APPROVED_SUBJECT_IDENTITY']==sid and d['SIGNATURE'] is None and d['CREDENTIAL'] is None and d['PERSONAL_IDENTITY'] is None
 assert d['APPROVED_SUBJECT_RAW_SHA256']==sha(OLD/'proposed-construction-test-authority-subject.json') and d['GOVERNING_CHARTER']==s['EFFECTIVE_CHARTER']
 assert d['DECISION_DOSSIER_PIN']=={'path':str((OLD/'unselected-authorization-dossier.json').relative_to(ROOT)),'raw_sha256':sha(OLD/'unselected-authorization-dossier.json')}
 source=ROOT/d['SOURCE_PIN']['path'];assert sha(source)==d['SOURCE_PIN']['raw_sha256'];assert OPTION in source.read_text() and APPROVED in source.read_text() and 'stop before construction or testing' in source.read_text()
 q=read(OLD/'independent-verification.json');assert q['READINESS']['BOOTSTRAP_CONSTRUCTION_DECISION_READY']=='YES' and q['CONSTRUCTION_SUBJECT_IDENTITY']==sid
 idx=read(OLD/'evidence-index.json')
 for p,h in idx['FILES'].items():assert sha(ROOT/p)==h
 ch=json.loads(subprocess.check_output([sys.executable,'docs/plans/qualification/KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_ADOPTION_66/reader.py'],cwd=str(ROOT),text=True));assert ch['CHARTER_EFFECTIVE'] and s['EFFECTIVE_CHARTER']==ch['CHARTER_CONTENT_IDENTITY'] and [x['STATE'] for x in ch['ORDERED_LIFECYCLE']]==['DRAFT','REVIEWED','APPROVED','EFFECTIVE']
 reg=read(ROOT/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');head='0'*64
 for v in reg['EVENTS']:
  vb={k:x for k,x in v.items() if k!='EVENT_HASH'};assert v['PREVIOUS_EVENT_HASH']==head and hashlib.sha256(json.dumps(vb,sort_keys=True,separators=(',',':')).encode()).hexdigest()==v['EVENT_HASH'];head=v['EVENT_HASH']
 assert reg['EVENTS'][-1]['LESSON']['LESSON_ID']=='LL-11' and head=='885fd0eaceb15847201dfd058217682741fb43c255298713ccbc1e7251eec791'
 return s,d,read(OLD/'resource-and-environment-contract.json'),read(OLD/'phase-and-entry-contract.json'),head

def conflicts():
 findings=[]
 for p in (ROOT/'docs/plans').rglob('*.json'):
  own_allowed={OUT/'grant-candidate.json', ROOT/read(OUT/'grant-record-binding.json')['FUTURE_RECORD_PATH']}
  if p in own_allowed:continue
  raw=p.read_bytes()
  if APPROVED.encode() not in raw and NS.encode() not in raw:continue
  def walk(x):
   if isinstance(x,dict):
    if isinstance(x.get('GRANT_IDENTITY'),dict) and isinstance(x.get('RECORD'),dict):findings.append(str(p))
    if x.get('GRANT_STATE') in ('REVOKED','SUPERSEDED') or x.get('INSTRUMENT_STATUS') in ('REVOKED','SUPERSEDED'):findings.append(str(p))
    for v in x.values():walk(v)
   elif isinstance(x,list):
    for v in x:walk(v)
  walk(read(p))
 assert not findings,'conflicting issuance/revocation/supersession'
 return findings

def main():
 s,d,env,phase,head=inputs();conflicts();bind=read(OUT/'grant-record-binding.json');mode='--candidate' if '--candidate' in sys.argv else '--record';path=ROOT/bind['FUTURE_RECORD_PATH']
 if mode=='--candidate':e=read(OUT/'grant-candidate.json')['ENVELOPE']
 else:e=read(path);assert path.name=='issued-bootstrap-construction-inert-grant-'+e['GRANT_IDENTITY']['sha256']+'.json'
 validate(e,s,d,env,phase);assert e['GRANT_IDENTITY']==bind['GRANT_IDENTITY']
 negatives=[]
 changes=[('wrong subject',lambda b:b.update(APPROVED_SUBJECT_IDENTITY={'sha256':'0'*64})),('wrong issuer',lambda b:b.update(ISSUER_ROLE='other')),('wrong charter',lambda b:b.update(GOVERNING_CHARTER_IDENTITY=None)),('extra source',lambda b:b['PERMITTED_SOURCE_FILES'].append('adapter/extra.py')),('missing test',lambda b:b['PERMITTED_INERT_TESTS'].pop()),('broader resource',lambda b:b['RESOURCE_LIMITS'].update(MAX_LIVE_CHILDREN=99)),('missing store',lambda b:b.update(STORE_REQUIREMENTS={})),('missing observer',lambda b:b.update(OBSERVER_REQUIREMENTS={})),('environment fake pass',lambda b:b['ENVIRONMENT_REQUIREMENTS'].update(ACTUAL_ENFORCEMENT_VERIFIED=True)),('missing entry',lambda b:b['CAMPAIGN_ENTRY_PREDICATES'].pop()),('wrong output',lambda b:b.update(OUTPUT_EVIDENCE_BOUNDARY='/tmp/unbounded')),('retry',lambda b:b.update(NO_RETRY_POLICY=1)),('systemd exclusion lost',lambda b:b['EXPLICIT_EXCLUSIONS'].remove('system-level or user-level systemd service execution')),('sudo exclusion lost',lambda b:b['EXPLICIT_EXCLUSIONS'].remove('sudo/privilege escalation')),('Bwrap exclusion lost',lambda b:b['EXPLICIT_EXCLUSIONS'].remove('Bubblewrap execution')),('probe authorized',lambda b:b.update(TARGET_COMMAND_EXECUTION_PERMITTED=True)),('early construction',lambda b:b['EFFECTIVE_BOUNDARY'].update(SOURCE_CONSTRUCTION_ACTIVATED_BY_ISSUANCE=True)),('early testing',lambda b:b['EFFECTIVE_BOUNDARY'].update(INERT_TEST_ACTIVATED_BY_ISSUANCE=True)),('A15 exclusion lost',lambda b:b['EXPLICIT_EXCLUSIONS'].remove('native A15 operations/execution/capture')),('self issuance exclusion lost',lambda b:b['EXPLICIT_EXCLUSIONS'].remove('grant self-issuance'))]
 for name,change in changes:
  m=copy.deepcopy(e);change(m['RECORD']);m['GRANT_IDENTITY']=aid(m['RECORD'],NS)
  try:validate(m,s,d,env,phase)
  except (AssertionError,KeyError):negatives.append({'CONTROL':name,'RESULT':'REJECTED'})
  else:raise AssertionError('negative accepted: '+name)
 effective=False
 if '--effective' in sys.argv:
  ref=read(OUT/'effective-bootstrap-construction-grant-reference.json');assert ref['BOOTSTRAP_GRANT_EFFECTIVE'] is True and ref['GRANT_IDENTITY']==e['GRANT_IDENTITY'] and ref['APPROVED_SUBJECT_IDENTITY']==s['CONTENT_IDENTITY'];assert ref['GRANT_RECORD_PIN']=={'path':str(path.relative_to(ROOT)),'raw_sha256':sha(path)}
  for p in ref['VERIFICATION_PINS']:assert sha(ROOT/p['path'])==p['raw_sha256']
  assert ref['INERT_TEST_ENTRY_READY'] is False and ref['NO_PROBE_PERMISSION'] is True
  effective=True
 result={'RESULT':'PASS','MODE':mode,'SUBJECT_VERIFIED':True,'CHARTER_STATUS':'VERIFIED_EXISTING_EFFECTIVE','ISSUER_AUTHORITY_VERIFIED':True,'GRANT_IDENTITY':e['GRANT_IDENTITY'],'APPROVED_SUBJECT_IDENTITY':s['CONTENT_IDENTITY'],'GRANT_RECORD_PERSISTED':mode!='--candidate','GRANT_EFFECTIVE':effective,'SOURCE_ALLOWLIST':e['RECORD']['PERMITTED_SOURCE_FILES'],'CONSTRUCTION_ENTRY_READY_SNAPSHOT':all(not(ROOT/p).exists() for p in e['RECORD']['PERMITTED_SOURCE_FILES']) and effective,'INERT_TEST_ENTRY_READY':False,'LL11_HEAD':head,'NEGATIVES':negatives,'CODE_OR_TESTS_CREATED_OR_RUN':0}
 result['SEMANTIC_IDENTITY']=aid(result,'qualification-h90-grant-reconstruction-v1');print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
