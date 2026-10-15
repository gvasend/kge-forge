"""Independent documentary reader. Never imports issuer/bootstrap/tests."""
import copy,hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];OUT=Path(__file__).resolve().parent;BASE=OUT.parent;P93=BASE/'bootstrap-entry-oracle-closure-93';OLD=BASE/'bootstrap-trust-authority-89'
NS='qualification-bootstrap-entry-oracle-repair-issued-grant-v1';OPTION='AUTHORIZE_BOUNDED_BOOTSTRAP_ENTRY_ORACLE_REPAIR'
def read(p):return json.loads(p.read_text())
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def aid(v,n):return {'kind':'CONTENT_IDENTITY','namespace':n,'sha256':hashlib.sha256(canon(v)).hexdigest()}
def pin(p):return {'path':str(p.relative_to(ROOT)),'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def inputs():
 p=P93/'proposed-repair-authorization-subject.json';assert pin(p)['raw_sha256']=='856ac2d0bf8948949cad917137d3f9aa3ce5372ebc6d1c1cf49becbab309b32e'
 env=read(p);assert env['IDENTITY']==aid(env['CONTENT'],'qualification-bootstrap-entry-oracle-repair-subject-v1') and env['IDENTITY']['sha256']=='2c3da2af0e05904127e405bc498b350fc7ad04fb7d58746e7ac5d57e35510257'
 s=env['CONTENT'];dossier=read(P93/'unselected-repair-authorization-dossier.json');assert dossier['DECISION_READY'] and dossier['SELECTION'] is None and dossier['SUBJECT_IDENTITY']==env['IDENTITY']
 assert [v['OPTION_ID'] for v in dossier['OPTIONS']]==[OPTION,'DECLINE_BOUNDED_BOOTSTRAP_ENTRY_ORACLE_REPAIR']
 for name,h in read(P93/'evidence-index.json')['FILES'].items():assert pin(P93/name)['raw_sha256']==h
 for p,h in s['CURRENT_SOURCE_PINS'].items():assert pin(ROOT/p)['raw_sha256']==h
 for p in s['EVIDENCE_PINS'].values():assert pin(ROOT/p['path'])==p
 assert read(P93/'independent-verification.json')['RECONSTRUCTION']['REPAIR_DECISION_READY']
 assert read(P93/'independent-verification.json')['RECONSTRUCTION']['PROPOSED_SUBJECT_IDENTITY']==env['IDENTITY']
 assert s['RESOURCE_LIMITS']==read(OLD/'proposed-construction-test-authority-subject.json')['RESOURCE_LIMITS']
 decision=read(OUT/'project-owner-decision-provenance.json');dc=decision['CONTENT']
 assert aid(dc,'qualification-bootstrap-repair-owner-decision-v1')==decision['IDENTITY']
 assert dc['SOURCE_KIND']=='CURRENT_CONVERSATION_USER_MESSAGE' and dc['SELECTION']==OPTION and dc['APPROVED_SUBJECT_IDENTITY']==env['IDENTITY']
 assert dc['SOURCE_PIN']==pin(OUT/'project-owner-decision-source.txt') and dc['OFFERED_DOSSIER_PIN']==pin(P93/'unselected-repair-authorization-dossier.json')
 text=(OUT/'project-owner-decision-source.txt').read_text();assert OPTION in text and env['IDENTITY']['sha256'] in text and 'stop before source modification or testing' in text
 assert dc['GOVERNING_CHARTER']==s['EFFECTIVE_CHARTER'] and dc['ISSUER_ROLE']==s['ISSUER_ROLE']
 assert all(dc[k] is None for k in ('APPROVAL_TIME','SIGNATURE','CREDENTIAL','PERSONAL_IDENTITY','TRANSPORT_MESSAGE_ID'))
 g=read(OUT/'effective-governance-verification.json');assert g['CHARTER_BINDING']==s['EFFECTIVE_CHARTER']
 assert [v['STATE'] for v in g['ORDERED_LIFECYCLE']]==['DRAFT','REVIEWED','APPROVED','EFFECTIVE'] and g['ORDERED_LIFECYCLE'][-1]['EVIDENCE_IDENTITY']==s['EFFECTIVE_LIFECYCLE']
 assert g['ISSUER_ROLE']==s['ISSUER_ROLE'] and g['ISSUER_AUTHORITY_VERIFIED'] and g['PACKAGE90_GRANT_IDENTITY']==s['EFFECTIVE_PACKAGE90_GRANT']
 ref90=read(BASE/'bootstrap-grant-issuance-90/effective-bootstrap-construction-grant-reference.json');assert ref90['BOOTSTRAP_GRANT_EFFECTIVE'] and ref90['GRANT_IDENTITY']==s['EFFECTIVE_PACKAGE90_GRANT']
 assert pin(ROOT/ref90['GRANT_RECORD_PIN']['path'])==ref90['GRANT_RECORD_PIN']
 for p in ref90['VERIFICATION_PINS']:assert pin(ROOT/p['path'])==p
 reg=read(ROOT/'docs/plans/PLANNER_REASONING_LESSONS_REGISTER_1.json');head='0'*64
 for e in reg['EVENTS']:
  b={k:v for k,v in e.items() if k!='EVENT_HASH'};assert e['PREVIOUS_EVENT_HASH']==head and hashlib.sha256(json.dumps(b,sort_keys=True,separators=(',',':')).encode()).hexdigest()==e['EVENT_HASH'];head=e['EVENT_HASH']
 assert head=='885fd0eaceb15847201dfd058217682741fb43c255298713ccbc1e7251eec791' and reg['EVENTS'][-1]['LESSON']['LESSON_ID']=='LL-11'
 assert pin(BASE/'campaign-budget.jsonl')['raw_sha256']=='3491e9003e1a016dbc4208e3963f8abea0f98c439dc892aa89a3811e73d528eb'
 return env,decision,head
FIELDS={'SCHEMA','WORK_PACKAGE','INSTRUMENT_STATUS','APPROVED_SUBJECT_IDENTITY','APPROVED_SUBJECT_PIN','ISSUER_ROLE','GOVERNING_CHARTER_IDENTITY','EFFECTIVE_CHARTER_LIFECYCLE','ISSUER_AUTHORITY_EVIDENCE_PIN','PROJECT_OWNER_DECISION_EVIDENCE','EXISTING_PACKAGE90_GRANT','EXACT_SOURCE_ALLOWLIST','PRIOR_SOURCE_IDENTITIES','ROOT_ENTRY_MAX_BYTES','ORDINARY_RECORD_MAX_BYTES','ROOT_ENTRY_SCHEMA','MAX_JSON_NODES','MAX_JSON_DEPTH','RESOURCE_LIMITS','RESOURCE_LIMITS_UNCHANGED','PARENT_ROOT_INPUT_EXCEPTION','PREFERRED_REPAIR','PERMITTED_REPAIR_OPERATIONS','PERMITTED_STATIC_VERIFICATION','SOURCE_AND_ORACLE_REQUIREMENTS','SYNTHETIC_TEST_SCOPE','TEST_ENTRY_PREDICATES','CONSTRUCTION_ENTRY_PREDICATES','ACTIVE_TEST_ADDITIONAL_GUARD','OUTPUT_EVIDENCE_BOUNDARY','NO_RETRY_POLICY','HISTORICAL_EXCLUSIONS','PROHIBITED_OPERATIONS','EXPLICIT_PACKAGE94_EXCLUSIONS','EFFECTIVE_BOUNDARY','REVOCATION_RULE','EXISTING_GRANTS_AMENDED_IN_PLACE','SCOPE_EXPANSION_ALLOWED','ROOT_EXCEPTION_ENLARGES_ORDINARY_RECORDS','CAMPAIGN_STARTED_BY_ISSUANCE','A15_EXECUTION_GRANT','A15_CAPTURE_GRANT','REAL_PROBE_GRANT','PREDECESSOR_REPAIR_GRANT','IDENTITY_RULE'}
EXCLUSIONS=['systemd service execution','sudo or privilege escalation','Bubblewrap execution','Package86 system-level probe','actual H77-02 probe','actual A15 execution or capture','native Planner runtime or V3 changes','frozen acceptance or historical evidence modification','production or external-system effects','automatic retries or additional campaigns','grant self-issuance']
def validate(e,subject,decision):
 assert set(e)=={'CONTENT','IDENTITY'} and e['IDENTITY']==aid(e['CONTENT'],NS)
 b=e['CONTENT'];s=subject['CONTENT'];assert set(b)==FIELDS
 assert b['SCHEMA']=='BOOTSTRAP-REPAIR-ISSUED-GRANT-94-1' and b['WORK_PACKAGE']=='E2-P05-D01-H77-02-BOOTSTRAP-REPAIR-GRANT-ISSUANCE-94'
 assert b['INSTRUMENT_STATUS']=='ISSUED_PENDING_SEPARATE_EFFECTIVENESS_REFERENCE'
 assert b['APPROVED_SUBJECT_IDENTITY']==subject['IDENTITY'] and b['APPROVED_SUBJECT_PIN']==pin(P93/'proposed-repair-authorization-subject.json')
 for bf,sf in [('ISSUER_ROLE','ISSUER_ROLE'),('GOVERNING_CHARTER_IDENTITY','EFFECTIVE_CHARTER'),('EFFECTIVE_CHARTER_LIFECYCLE','EFFECTIVE_LIFECYCLE'),('EXISTING_PACKAGE90_GRANT','EFFECTIVE_PACKAGE90_GRANT'),('EXACT_SOURCE_ALLOWLIST','SOURCE_ALLOWLIST'),('PRIOR_SOURCE_IDENTITIES','CURRENT_SOURCE_PINS'),('ROOT_ENTRY_SCHEMA','ROOT_ENTRY_SCHEMA'),('MAX_JSON_NODES','MAX_JSON_NODES'),('MAX_JSON_DEPTH','MAX_JSON_DEPTH'),('RESOURCE_LIMITS','RESOURCE_LIMITS'),('PARENT_ROOT_INPUT_EXCEPTION','PARENT_ROOT_INPUT_EXCEPTION'),('PREFERRED_REPAIR','PREFERRED_REPAIR'),('PERMITTED_REPAIR_OPERATIONS','PERMITTED_OPERATIONS'),('SOURCE_AND_ORACLE_REQUIREMENTS','EVIDENCE_PINS'),('SYNTHETIC_TEST_SCOPE','SYNTHETIC_TEST_SCOPE'),('OUTPUT_EVIDENCE_BOUNDARY','OUTPUT_EVIDENCE_BOUNDARY'),('HISTORICAL_EXCLUSIONS','HISTORICAL_EXCLUSIONS'),('PROHIBITED_OPERATIONS','PROHIBITED_OPERATIONS')]:assert b[bf]==s[sf],bf
 assert b['PROJECT_OWNER_DECISION_EVIDENCE']=={'IDENTITY':decision['IDENTITY'],'PIN':pin(OUT/'project-owner-decision-provenance.json')}
 assert b['ISSUER_AUTHORITY_EVIDENCE_PIN']==pin(OUT/'effective-governance-verification.json')
 assert b['ROOT_ENTRY_MAX_BYTES']==s['ROOT_ENTRY_MAX_BYTES']==207444 and b['ORDINARY_RECORD_MAX_BYTES']==s['ORDINARY_PRIVATE_RECORD_MAX_BYTES']==65536
 assert all(type(v) is int for v in b['RESOURCE_LIMITS'].values()) and b['RESOURCE_LIMITS_UNCHANGED'] is True and b['NO_RETRY_POLICY']==0
 assert b['TEST_ENTRY_PREDICATES']==s['ENTRY_PREDICATES']['active_inert'] and b['CONSTRUCTION_ENTRY_PREDICATES']==s['ENTRY_PREDICATES']['construction']
 assert len(b['ACTIVE_TEST_ADDITIONAL_GUARD'])==8 and b['EXPLICIT_PACKAGE94_EXCLUSIONS']==EXCLUSIONS
 assert b['PERMITTED_STATIC_VERIFICATION']==['exact approved source scope and identities','AST/JSON encoder and schema/size reconstruction without target execution','independent full oracle/observer comparison reconstruction','preservation and four-seed static negatives']
 assert b['EFFECTIVE_BOUNDARY']['NO_BACKDATING'] and b['EFFECTIVE_BOUNDARY']['SOURCE_REPAIR_PERFORMED_BY_ISSUANCE'] is False and b['EFFECTIVE_BOUNDARY']['ACTIVE_TESTING_AUTHORIZED_AUTOMATICALLY'] is False
 assert b['REVOCATION_RULE']['EXPIRATION_DATE'] is None and b['REVOCATION_RULE']['NO_UNBOUNDED_SCOPE_INFERRED'] and 'Project-owner explicit' in b['REVOCATION_RULE']['RULE']
 assert all(b[k] is False for k in ('EXISTING_GRANTS_AMENDED_IN_PLACE','SCOPE_EXPANSION_ALLOWED','ROOT_EXCEPTION_ENLARGES_ORDINARY_RECORDS','CAMPAIGN_STARTED_BY_ISSUANCE'))
 assert all(b[k] is None for k in ('A15_EXECUTION_GRANT','A15_CAPTURE_GRANT','REAL_PROBE_GRANT','PREDECESSOR_REPAIR_GRANT'))
 return True

def conflicts(allowed_record=None):
 findings=[]
 target='2c3da2af0e05904127e405bc498b350fc7ad04fb7d58746e7ac5d57e35510257'
 for p in (ROOT/'docs/plans').rglob('*.json'):
  if p==OUT/'grant-candidate.json' or (allowed_record is not None and p==allowed_record):continue
  raw=p.read_bytes()
  if target.encode() not in raw and NS.encode() not in raw:continue
  obj=json.loads(raw)
  def walk(x):
   if isinstance(x,dict):
    ident=x.get('IDENTITY') or x.get('GRANT_IDENTITY')
    if isinstance(ident,dict) and ident.get('namespace')==NS and ('CONTENT' in x or 'RECORD' in x):findings.append({'path':str(p.relative_to(ROOT)),'reason':'other issued repair content'})
    if x.get('INSTRUMENT_STATUS') in ('REVOKED','SUPERSEDED') or x.get('GRANT_STATE') in ('REVOKED','SUPERSEDED'):findings.append({'path':str(p.relative_to(ROOT)),'reason':'revocation/supersession'})
    for v in x.values():walk(v)
   elif isinstance(x,list):
    for v in x:walk(v)
  walk(obj)
 assert not findings,findings
 return findings
subject,decision,head=inputs();binding=read(OUT/'grant-record-binding.json');record=ROOT/binding['FUTURE_RECORD_PATH'];candidate='--candidate' in sys.argv
if '--conflicts' in sys.argv:
 print(json.dumps({'RESULT':'PASS','CONFLICTS':conflicts(record if record.exists() else None),'SCAN_BOUNDARY':'docs/plans JSON explicit repair-issued/revocation/supersession states; proposals not grants'}));raise SystemExit(0)
e=read(OUT/'grant-candidate.json') if candidate else read(record);validate(e,subject,decision)
assert e['IDENTITY']==binding['GRANT_IDENTITY'] and record.name=='issued-bootstrap-repair-grant-'+e['IDENTITY']['sha256']+'.json'
conflicts(record if not candidate else None)
changes=[('wrong subject',lambda b:b['APPROVED_SUBJECT_IDENTITY'].update(sha256='0'*64)),('wrong issuer',lambda b:b.update(ISSUER_ROLE='other')),('wrong charter',lambda b:b['GOVERNING_CHARTER_IDENTITY'].update(sha256='0'*64)),('wrong lifecycle',lambda b:b['EFFECTIVE_CHARTER_LIFECYCLE'].update(sha256='0'*64)),('extra source',lambda b:b['EXACT_SOURCE_ALLOWLIST'].append('adapter/new.py')),('root cap enlarged',lambda b:b.update(ROOT_ENTRY_MAX_BYTES=207445)),('ordinary cap enlarged',lambda b:b.update(ORDINARY_RECORD_MAX_BYTES=207444)),('resource expansion',lambda b:b['RESOURCE_LIMITS'].update(MAX_LIVE_CHILDREN=3)),('missing oracle scope',lambda b:b['SOURCE_AND_ORACLE_REQUIREMENTS'].pop('executable-oracle-bindings.json')),('missing tests',lambda b:b['SYNTHETIC_TEST_SCOPE']['original14_top_level_ids'].pop()),('missing entry predicate',lambda b:b['TEST_ENTRY_PREDICATES'].pop()),('extra campaign',lambda b:b['SYNTHETIC_TEST_SCOPE'].update(extra_campaigns=1)),('retry allowed',lambda b:b.update(NO_RETRY_POLICY=1)),('expanded output',lambda b:b.update(OUTPUT_EVIDENCE_BOUNDARY='/tmp/anywhere')),('lost exclusions',lambda b:b.update(EXPLICIT_PACKAGE94_EXCLUSIONS=[])),('early effectiveness',lambda b:b.update(INSTRUMENT_STATUS='EFFECTIVE')),('automatic testing',lambda b:b['EFFECTIVE_BOUNDARY'].update(ACTIVE_TESTING_AUTHORIZED_AUTOMATICALLY=True)),('probe authority',lambda b:b.update(REAL_PROBE_GRANT={'issued':True})),('A15 authority',lambda b:b.update(A15_EXECUTION_GRANT={'issued':True})),('capture authority',lambda b:b.update(A15_CAPTURE_GRANT={'issued':True})),('circular self grant',lambda b:b.update(PREDECESSOR_REPAIR_GRANT=e['IDENTITY'])),('wrong owner evidence',lambda b:b['PROJECT_OWNER_DECISION_EVIDENCE']['IDENTITY'].update(sha256='0'*64)),('wrong subject raw pin',lambda b:b['APPROVED_SUBJECT_PIN'].update(raw_sha256='0'*64)),('root exception spreads',lambda b:b.update(ROOT_EXCEPTION_ENLARGES_ORDINARY_RECORDS=True))]
negative=[]
for name,change in changes:
 m=copy.deepcopy(e);change(m['CONTENT']);m['IDENTITY']=aid(m['CONTENT'],NS)
 try:validate(m,subject,decision)
 except (AssertionError,KeyError,TypeError,ValueError):negative.append({'CONTROL':name,'RESULT':'REJECTED'})
 else:raise AssertionError('accepted negative '+name)
effective=False
if '--effective' in sys.argv:
 ref=read(OUT/'effective-bootstrap-repair-grant-reference.json')
 assert ref['REPAIR_GRANT_EFFECTIVE'] is True and ref['GRANT_IDENTITY']==e['IDENTITY'] and ref['GRANT_RECORD_PIN']==pin(record)
 assert ref['APPROVED_SUBJECT_IDENTITY']==subject['IDENTITY'] and ref['OWNER_DECISION_IDENTITY']==decision['IDENTITY']
 assert ref['ROOT_ENTRY_MAX_BYTES']==207444 and ref['ORDINARY_RECORD_MAX_BYTES']==65536
 assert ref['ACTIVE_INERT_TEST_READY'] is False and ref['SOURCE_REPAIR_PERFORMED'] is False
 for p in ref['VERIFICATION_PINS']:assert pin(ROOT/p['path'])==p
 effective=True
result={'RESULT':'PASS','MODE':'candidate' if candidate else 'persisted','GRANT_IDENTITY':e['IDENTITY'],'APPROVED_SUBJECT_IDENTITY':subject['IDENTITY'],'OWNER_DECISION_VERIFIED':True,'CHARTER_STATUS':'EXISTING_EFFECTIVE','ISSUER_AUTHORITY_VERIFIED':True,'SOURCE_ALLOWLIST':e['CONTENT']['EXACT_SOURCE_ALLOWLIST'],'ROOT_ENTRY_MAX_BYTES':207444,'ORDINARY_RECORD_MAX_BYTES':65536,'RESOURCE_LIMITS_UNCHANGED':True,'GRANT_PERSISTED':not candidate,'GRANT_EFFECTIVE':effective,'CONSTRUCTION_ENTRY_READY':effective and all(pin(ROOT/p)['raw_sha256']==h for p,h in subject['CONTENT']['CURRENT_SOURCE_PINS'].items()),'ACTIVE_INERT_TEST_READY':False,'LL11_HEAD':head,'NEGATIVES':negative,'ACTUAL_TEST_OR_PROBE_EXECUTION':0}
print(json.dumps({'RECONSTRUCTION':result,'SEMANTIC_IDENTITY':aid(result,'qualification-bootstrap-repair-grant-reconstruction-v1')},sort_keys=True))
