"""Read-only documentary grant verifier. No adapter/native imports or calls."""
import copy,hashlib,json,pathlib,subprocess,sys
D=pathlib.Path(__file__).resolve().parent;R=D.parents[3];Q=R/'docs/plans/qualification';P=Q/'E2_P05_D01_A15_IMPLEMENTATION_TEST_AUTHORITY_70'
APPROVED='a2505f248e929f0226d20d813673faa87b8b09fa0e08b071e413d4d7779a9869'
OPTION='AUTHORIZE_BOUNDED_A15_ADAPTER_IMPLEMENTATION_SYNTHETIC_TEST'
NS='qualification-A15-implementation-test-issued-grant-v1'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def aid(ns,x):return {'$type':'ArtifactIdentity','kind':{'$enum':'IdentityKind','value':'CONTENT_IDENTITY'},'namespace':ns,'sha256':canonical(x)}
def pin(p):return {'PATH':str(p.relative_to(R)),'RAW_SHA256':sha(p)}
def inputs():
 for name in ['E2_P05_D01_A15_IMPLEMENTATION_TEST_AUTHORITY_70','E2_P05_D01_A15_NORMATIVE_ADOPTION_ISSUANCE_68','KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_ADOPTION_66','KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_65']:
  obj=read(Q/name/'evidence-index.json')
  for path,h in obj['FILES'].items():assert sha(R/path)==h,path
 # Reconstruct live governance independently; historical Package70 qualification
 # is authenticated as sealed evidence rather than rerunning its preconstruction
 # absence checks after authorized files may legitimately be created.
 normative=json.loads(subprocess.check_output([sys.executable,'docs/plans/qualification/E2_P05_D01_A15_NORMATIVE_ADOPTION_ISSUANCE_68/verify_effective.py'],cwd=str(R)))
 assert normative['NORMATIVE_MANDATE_EFFECTIVE'] is True and not normative['EXECUTION_AUTHORITY'] and not normative['CAPTURE_AUTHORITY']
 result=read(P/'independent-subject-qualification.json')
 assert result['RESULT']=='PASS_CONDITIONAL_AUTHORITY_SUBJECT' and result['IMPLEMENTATION_TEST_DECISION_READY']=='YES'
 subject=read(P/'implementation-test-authority-subject.json');dossier=read(P/'unselected-implementation-test-decision-dossier.json')
 assert subject['IDENTITY']==aid('qualification-A15-implementation-synthetic-test-authority-subject-v1',subject['CONTENT'])
 assert subject['IDENTITY']['sha256']==APPROVED and result['SUBJECT_IDENTITY']==subject['IDENTITY']
 assert dossier['DECISION_READY'] and dossier['SELECTION'] is None and not dossier['ANY_OPTION_SELECTED']
 assert dossier['EXACT_APPROVAL_SUBJECT']==subject['IDENTITY'] and dossier['OPTIONS'][0]['OPTION_ID']==OPTION
 assert dossier['SUBJECT_PIN']==pin(P/'implementation-test-authority-subject.json')
 return subject,dossier,result

def conflicts(grant_id=None):
 found=[];checked=[]
 for path in (R/'docs/plans').rglob('*.json'):
  if D in path.parents or path.name=='DETERMINISTIC_PLANNER_V0_1_E2_P05_D01_A15_IMPLEMENTATION_TEST_GRANT_ISSUANCE_71.json':continue
  raw=path.read_bytes()
  terms=[APPROVED.encode(),NS.encode()]+([grant_id['sha256'].encode()] if grant_id else [])
  if not any(t in raw for t in terms):continue
  checked.append(pin(path));obj=json.loads(raw)
  def walk(x):
   if isinstance(x,dict):
    if isinstance(x.get('GRANT_IDENTITY'),dict) and isinstance(x.get('RECORD'),dict):found.append(str(path.relative_to(R)))
    if x.get('GRANT_STATE') in ['REVOKED','SUPERSEDED'] or x.get('INSTRUMENT_STATUS') in ['REVOKED','SUPERSEDED']:found.append(str(path.relative_to(R)))
    for z in x.values():walk(z)
   elif isinstance(x,list):
    for z in x:walk(z)
  walk(obj)
 assert not found,'CONFLICTING_GRANT_REVOCATION_SUPERSESSION:'+repr(found)
 return {'RESULT':'PASS','CHECKED_PRIOR_RECORDS':checked,'CONFLICTING_RECORDS':found,'SCOPE':'Exact approved subject/current grant namespace and identity in docs/plans; proposed subjects/reference reports are not issuances'}

def verify(envelope,decision,subject=None,dossier=None,integrity=True,duplicate_count=1):
 if subject is None:subject,dossier,_=inputs()
 if integrity:assert envelope['GRANT_IDENTITY']==aid(NS,envelope['RECORD']),'grant content identity'
 assert duplicate_count==1,'duplicate issuance'
 body=envelope['RECORD'];dc=decision['CONTENT'];c=subject['CONTENT']['CONTRACTS'];env=c['environment-resource-permission-contract.json']
 expected_keys={'SCHEMA_ID','WORK_PACKAGE','INSTRUMENT_STATUS','APPROVED_SUBJECT_IDENTITY','APPROVED_SUBJECT_PIN','ISSUER_ROLE','ISSUER_AUTHORITY_EVIDENCE','GOVERNING_CHARTER_IDENTITY','EFFECTIVE_CHARTER_LIFECYCLE_IDENTITY','NORMATIVE_MANDATE_REFERENCE','PROJECT_OWNER_DECISION_EVIDENCE','PERMITTED_SOURCE_FILES','PERMITTED_TESTS','RESOURCE_LIMITS','PHASE_GATES','TEST_ENTRY_PREDICATES','TEST_ENTRY_ACTIVATION_RULE','TEMPORAL_GATES','ENVIRONMENT_CONTRACT','SYNTHETIC_FIXTURE_CONTRACT','FAILURE_RETRY_CONTROLS','PROCESS_ISOLATION_PERSISTENCE_CONTROLS','IMPLEMENTATION_QUALIFICATION_ACCEPTANCE','EVIDENCE_BOUNDARY','HISTORICAL_EXCLUSIONS','EFFECTIVE_BOUNDARY','REVOCATION_RULE','MANDATE','A15_EXECUTION_GRANT','A15_CAPTURE_GRANT','PREDECESSOR_IMPLEMENTATION_TEST_GRANT','SCOPE_EXPANSION_ALLOWED','EXPLICIT_PACKAGE71_EXCLUSIONS','APPROVED_LIMITS_INTERPRETATION','IDENTITY_RULE','CAMPAIGN_STARTED_BY_ISSUANCE'}
 assert set(body)==expected_keys and set(envelope)=={'GRANT_IDENTITY','RECORD'}
 assert body['SCHEMA_ID']=='A15-IMPLEMENTATION-TEST-ISSUED-GRANT-71-1' and body['WORK_PACKAGE']=='E2-P05-D01-A15-IMPLEMENTATION-TEST-GRANT-ISSUANCE-71'
 assert body['CAMPAIGN_STARTED_BY_ISSUANCE'] is False
 charter=read(Q/'KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_65/charter-content.json')
 assert body['ISSUER_AUTHORITY_EVIDENCE']=={'OWNER_DECLARATION_PIN':charter['GOVERNING_AUTHORITY']['DECLARATION_PIN'],'EFFECTIVE_CHARTER_REFERENCE_PIN':pin(Q/'KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_ADOPTION_66/effective-charter-reference.json'),'DIRECT_ROLE':'No delegation or personal signature invented'}
 assert body['APPROVED_LIMITS_INTERPRETATION']=='Exact approved caps become authorization ceilings only; copied proposed-status metadata does not prove enforcement or resource permissions'
 assert body['IDENTITY_RULE']=='Canonical sorted compact UTF-8 JSON RECORD digest; own wrapper, future effectiveness/verification records and generated code/fixture/profile results excluded'

 assert decision['IDENTITY']==aid('qualification-A15-owner-implementation-test-decision-v1',dc)
 assert dc['SOURCE_KIND']=='CURRENT_CONVERSATION_USER_MESSAGE' and dc['SELECTION']==OPTION
 assert dc['APPROVED_SUBJECT_IDENTITY']==subject['IDENTITY'] and dc['GOVERNING_CHARTER']==subject['CONTENT']['GOVERNING_CHARTER'] and dc['EFFECTIVE_CHARTER_LIFECYCLE']==subject['CONTENT']['EFFECTIVE_CHARTER_LIFECYCLE']
 assert dc['ISSUER_ROLE']==dossier['ISSUER_ROLE']==subject['CONTENT']['ISSUER_ROLE']
 assert dc['DECISION_DOSSIER_PIN']==pin(P/'unselected-implementation-test-decision-dossier.json')
 source=R/dc['SOURCE_PIN']['PATH'];assert sha(source)==dc['SOURCE_PIN']['RAW_SHA256']
 text=source.read_text();assert OPTION in text and APPROVED in text and 'Do not construct the adapter or run synthetic tests during issuance.' in text
 assert 'd26962c58f17281173e965433dae63a941e078115f3dcc30e2a3512fa21812b8' in text and 'a27516baa0ab7f34a36a1130490b6cfa38c508975ca337e0824c8eac33715cbb' in text
 assert dc['AUTHORIZATION_SCOPE']=='Exact approved conditional implementation/test subject only; issuance now, no construction/tests in Package71'
 assert body['APPROVED_SUBJECT_IDENTITY']==subject['IDENTITY'] and body['APPROVED_SUBJECT_PIN']==pin(P/'implementation-test-authority-subject.json')
 assert body['ISSUER_ROLE']==dc['ISSUER_ROLE'] and body['GOVERNING_CHARTER_IDENTITY']==dc['GOVERNING_CHARTER'] and body['EFFECTIVE_CHARTER_LIFECYCLE_IDENTITY']==dc['EFFECTIVE_CHARTER_LIFECYCLE']
 assert body['PROJECT_OWNER_DECISION_EVIDENCE']=={'IDENTITY':decision['IDENTITY'],'PIN':pin(D/'project-owner-decision.json')}
 assert body['PERMITTED_SOURCE_FILES']==c['source-file-scope.json']['PERMITTED_SOURCE_FILES']
 assert body['PERMITTED_TESTS']==c['permitted-test-inventory.json'] and len(body['PERMITTED_TESTS']['TESTS'])==13
 assert body['RESOURCE_LIMITS']==env['RESOURCE_LIMITS'] and body['RESOURCE_LIMITS']['AUTOMATIC_RETRIES']==0
 assert body['PHASE_GATES']==env['PHASE_GUARDS'] and body['TEST_ENTRY_PREDICATES']==env['PREDICATES'] and len(body['TEST_ENTRY_PREDICATES'])==11
 assert body['TEST_ENTRY_ACTIVATION_RULE']==env['ACTIVATION_EVALUATION_RULE'] and body['TEMPORAL_GATES']==env['TEMPORAL_GATES']
 assert body['ENVIRONMENT_CONTRACT']==env and body['SYNTHETIC_FIXTURE_CONTRACT']==c['synthetic-fixture-contract.json']
 assert body['FAILURE_RETRY_CONTROLS']==c['failure-retry-controls.json'] and body['PROCESS_ISOLATION_PERSISTENCE_CONTROLS']==c['process-isolation-persistence-controls.json']
 assert body['IMPLEMENTATION_QUALIFICATION_ACCEPTANCE']==c['implementation-qualification-acceptance.json']
 assert body['EVIDENCE_BOUNDARY']==env['INPUT_OUTPUT_PATH_SELECTION']['EVIDENCE_ROOT']
 assert body['HISTORICAL_EXCLUSIONS']==subject['CONTENT']['HISTORICAL_EXCLUSIONS']
 assert body['REVOCATION_RULE']==subject['CONTENT']['GRANT_TERMINATION_RULE']
 norm=read(Q/'E2_P05_D01_A15_NORMATIVE_ADOPTION_ISSUANCE_68/effective-normative-mandate-reference.json')
 assert body['NORMATIVE_MANDATE_REFERENCE']=={'SUBJECT_IDENTITY':subject['CONTENT']['NORMATIVE_SUBJECT'],'EFFECTIVE_REFERENCE_PIN':subject['CONTENT']['EFFECTIVE_NORMATIVE_REFERENCE_PIN'],'ADOPTION_RECORD_PIN':norm['ADOPTION_RECORD_PIN'],'VERIFICATION_STATUS':'YES; normative-only, not implementation permission'}
 assert body['INSTRUMENT_STATUS']=='ISSUANCE_RECORDED_PENDING_INDEPENDENT_EFFECTIVENESS_VERIFICATION'
 assert body['EFFECTIVE_BOUNDARY']=='Only after exclusive publication, independent persisted reread, four-seed agreement, all negative controls and prior-artifact preservation verification, followed by separately persisted effective reference. No backdating; future operations additionally require corresponding entry/temporal gates.'
 assert body['MANDATE']==subject['CONTENT']['MANDATE'] and body['A15_EXECUTION_GRANT'] is None and body['A15_CAPTURE_GRANT'] is None
 assert body['PREDECESSOR_IMPLEMENTATION_TEST_GRANT'] is None and body['SCOPE_EXPANSION_ALLOWED'] is False
 assert body['EXPLICIT_PACKAGE71_EXCLUSIONS']==['Actual A15 checkpoint or variant execution','Actual A15 apply_event or record_result','Actual A15 capture/save/restore/replay','Native Planner runtime/V3/frozen acceptance modification','Historical proof/admission evidence modification','E1 changes','Production or external-system access','New campaigns or automatic retries','Self-issuance or scope expansion']
 return {'RESULT':'PASS_DOCUMENTARY_GRANT','GRANT_IDENTITY':envelope['GRANT_IDENTITY'],'APPROVED_SUBJECT_IDENTITY':subject['IDENTITY'],'PROJECT_OWNER_DECISION_IDENTITY':decision['IDENTITY'],'MANDATE':body['MANDATE'],'PERMITTED_SOURCE_FILES':body['PERMITTED_SOURCE_FILES'],'TEST_CATEGORY_COUNT':13,'PREDICATE_COUNT':11,'A15_EXECUTION_AUTHORITY':'NO','A15_CAPTURE_AUTHORITY':'NO','ADAPTER_CONSTRUCTION_PERFORMED':'NO','SYNTHETIC_TESTS_EXECUTED':'NO'}
if __name__=='__main__':
 subject,dossier,_=inputs();decision=read(D/'project-owner-decision.json')
 if '--candidate' in sys.argv:
  candidate=json.load(sys.stdin);assert not list(D.glob('issued-implementation-test-grant-*.json'))
  conflicts(candidate['GRANT_IDENTITY']);result=verify(candidate,decision,subject,dossier)
 else:
  files=list(D.glob('issued-implementation-test-grant-*.json'));assert len(files)==1
  record=read(files[0]);assert files[0].name=='issued-implementation-test-grant-'+record['GRANT_IDENTITY']['sha256']+'.json'
  conflicts(record['GRANT_IDENTITY']);result=verify(record,decision,subject,dossier,duplicate_count=len(files))
 print(json.dumps(result,sort_keys=True,ensure_ascii=False))
