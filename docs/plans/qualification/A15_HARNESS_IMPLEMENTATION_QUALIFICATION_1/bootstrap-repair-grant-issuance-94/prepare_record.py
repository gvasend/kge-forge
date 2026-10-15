"""Prepare exact documentary issuance candidate. No source repair or testing."""
import hashlib,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];OUT=Path(__file__).resolve().parent;BASE=OUT.parent;P93=BASE/'bootstrap-entry-oracle-closure-93';P90=BASE/'bootstrap-grant-issuance-90'
WP='E2-P05-D01-H77-02-BOOTSTRAP-REPAIR-GRANT-ISSUANCE-94';OPTION='AUTHORIZE_BOUNDED_BOOTSTRAP_ENTRY_ORACLE_REPAIR'
def read(p):return json.loads(p.read_text())
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def aid(v,ns):return {'kind':'CONTENT_IDENTITY','namespace':ns,'sha256':hashlib.sha256(canon(v)).hexdigest()}
def pin(p):return {'path':str(p.relative_to(ROOT)),'raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def save(n,v):
 p=OUT/n;raw=json.dumps(v,indent=2,sort_keys=True)+'\n'
 if p.exists():assert p.read_text()==raw;return
 p.write_text(raw)
subject=read(P93/'proposed-repair-authorization-subject.json');s=subject['CONTENT']
assert pin(P93/'proposed-repair-authorization-subject.json')['raw_sha256']=='856ac2d0bf8948949cad917137d3f9aa3ce5372ebc6d1c1cf49becbab309b32e'
assert aid(s,subject['IDENTITY']['namespace'])==subject['IDENTITY'] and subject['IDENTITY']['sha256']=='2c3da2af0e05904127e405bc498b350fc7ad04fb7d58746e7ac5d57e35510257'
dossier=read(P93/'unselected-repair-authorization-dossier.json');assert dossier['DECISION_READY'] and dossier['SELECTION'] is None and dossier['OPTIONS'][0]['OPTION_ID']==OPTION and dossier['SUBJECT_IDENTITY']==subject['IDENTITY']
source='''# Package 94 project-owner decision provenance

Source: current conversation user-role Package94 instruction. This is a retained exact authority/exclusion excerpt, not a fabricated signature, credential, account, transport ID or approval timestamp.

WORK_PACKAGE = E2-P05-D01-H77-02-BOOTSTRAP-REPAIR-GRANT-ISSUANCE-94
The KGE-Forge project owner explicitly selected:
AUTHORIZE_BOUNDED_BOOTSTRAP_ENTRY_ORACLE_REPAIR

Exact approved subject:
CONTENT_IDENTITY/qualification-bootstrap-entry-oracle-repair-subject-v1:2c3da2af0e05904127e405bc498b350fc7ad04fb7d58746e7ac5d57e35510257
Subject raw SHA-256:
856ac2d0bf8948949cad917137d3f9aa3ce5372ebc6d1c1cf49becbab309b32e
Governing authority: Effective KGE-Forge Qualification Governance Charter v1.0.

The approval permits issuance of the exact bounded repair instrument after authentication.
It does not authorize source modification before grant effectiveness or active testing before separate entry verification.
ROOT_ENTRY_MAX_BYTES = 207444
ORDINARY_RECORD_MAX_BYTES = 65536
RESOURCE_LIMITS = UNCHANGED

The grant must not automatically authorize an active inert campaign. Before any active testing require exact repaired executable identity; independently sealed fixtures/oracles; verified environment/store controls; enforceable resource limits; qualified observer; exact campaign entry; applicable active-test authority; no real probe execution path. Unknown/unsupported predicates block testing.

Explicit exclusions: systemd service execution; sudo/privilege escalation; Bubblewrap; Package86 system-level probe; actual H77-02 probe; actual A15 execution/capture; native Planner/V3 changes; frozen acceptance or historical evidence mutation; production/external-system effects; automatic retries/additional campaigns; grant self-issuance.

If issuance passes, stop before source modification or testing.
'''
p=OUT/'project-owner-decision-source.txt'
if p.exists():assert p.read_text()==source
else:p.write_text(source)
decision_body={'SCHEMA':'BOOTSTRAP-REPAIR-OWNER-DECISION-94-1','WORK_PACKAGE':WP,'SOURCE_KIND':'CURRENT_CONVERSATION_USER_MESSAGE','SOURCE_PIN':pin(p),'SELECTION':OPTION,'APPROVED_SUBJECT_IDENTITY':subject['IDENTITY'],'APPROVED_SUBJECT_RAW_SHA256':'856ac2d0bf8948949cad917137d3f9aa3ce5372ebc6d1c1cf49becbab309b32e','OFFERED_DOSSIER_PIN':pin(P93/'unselected-repair-authorization-dossier.json'),'ISSUER_ROLE':s['ISSUER_ROLE'],'GOVERNING_CHARTER':s['EFFECTIVE_CHARTER'],'APPROVAL_TIME':None,'SIGNATURE':None,'CREDENTIAL':None,'PERSONAL_IDENTITY':None,'TRANSPORT_MESSAGE_ID':None,'PERMISSION':'exact bounded repair instrument issuance; construction after effectiveness and fresh guard, active testing only after separate applicable entry qualification'}
decision={'CONTENT':decision_body,'IDENTITY':aid(decision_body,'qualification-bootstrap-repair-owner-decision-v1')};save('project-owner-decision-provenance.json',decision)
# Fresh independent documentary readers only.
def reader(path,args=()):
 run=subprocess.run(['/usr/bin/python3.8',str(path.relative_to(ROOT)),*args],cwd=str(ROOT),capture_output=True,text=True,check=True);return json.loads(run.stdout)
charter=reader(ROOT/'docs/plans/qualification/KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_ADOPTION_66/reader.py')
assert charter['CHARTER_EFFECTIVE'] and [v['STATE'] for v in charter['ORDERED_LIFECYCLE']]==['DRAFT','REVIEWED','APPROVED','EFFECTIVE']
assert charter['CHARTER_CONTENT_IDENTITY']==s['EFFECTIVE_CHARTER']
norm=reader(ROOT/'docs/plans/qualification/E2_P05_D01_A15_NORMATIVE_ADOPTION_ISSUANCE_68/verify_effective.py');assert norm['NORMATIVE_MANDATE_EFFECTIVE'] and not norm['EXECUTION_AUTHORITY'] and not norm['CAPTURE_AUTHORITY']
base=reader(P90/'verify.py',('--effective',));assert base['GRANT_EFFECTIVE'] and base['GRANT_IDENTITY']==s['EFFECTIVE_PACKAGE90_GRANT']
qualified=reader(P93/'verify_independent.py');assert qualified['RECONSTRUCTION']['REPAIR_DECISION_READY'] and qualified['RECONSTRUCTION']['PROPOSED_SUBJECT_IDENTITY']==subject['IDENTITY']
for key,p in s['EVIDENCE_PINS'].items():assert pin(ROOT/p['path'])==p
for path,h in s['CURRENT_SOURCE_PINS'].items():assert pin(ROOT/path)['raw_sha256']==h
save('exact-subject-authentication.json',{'RESULT':'PASS','SUBJECT_IDENTITY':subject['IDENTITY'],'SUBJECT_PIN':pin(P93/'proposed-repair-authorization-subject.json'),'DOSSIER_PIN':pin(P93/'unselected-repair-authorization-dossier.json'),'INDEPENDENT_VERIFICATION_PIN':pin(P93/'independent-verification.json'),'FRESH_QUALIFICATION_RECONSTRUCTION':qualified['SEMANTIC_IDENTITY'],'OWNER_DECISION_IDENTITY':decision['IDENTITY'],'SOURCE_ALLOWLIST':s['SOURCE_ALLOWLIST'],'ROOT_ENTRY_MAX_BYTES':207444,'ORDINARY_RECORD_MAX_BYTES':65536,'RESOURCE_LIMITS':s['RESOURCE_LIMITS'],'ALL_EVIDENCE_AND_SOURCE_PINS_EXACT':True})
# Do not copy normative adoption contents or charter activation booleans into
# new foreign evidence shapes recognized by historical conflict readers.
save('effective-governance-verification.json',{'RESULT':'PASS','CHARTER_BINDING':s['EFFECTIVE_CHARTER'],'ORDERED_LIFECYCLE':charter['ORDERED_LIFECYCLE'],'CHARTER_STATUS':'EXISTING_EFFECTIVE_INDEPENDENTLY_VERIFIED','ISSUER_ROLE':s['ISSUER_ROLE'],'ISSUER_AUTHORITY_VERIFIED':True,'NORMATIVE_BINDING':norm['ADOPTION_RECORD_IDENTITY'],'NORMATIVE_STATUS':'EXISTING_EFFECTIVE_NORMATIVE_ONLY','PACKAGE90_GRANT_IDENTITY':base['GRANT_IDENTITY'],'PACKAGE90_STATUS':'EXISTING_EFFECTIVE','NORMATIVE_REFERENCE_PIN':pin(ROOT/'docs/plans/qualification/E2_P05_D01_A15_NORMATIVE_ADOPTION_ISSUANCE_68/effective-normative-mandate-reference.json'),'CHARTER_REFERENCE_PIN':pin(ROOT/'docs/plans/qualification/KGE_FORGE_QUALIFICATION_GOVERNANCE_CHARTER_ADOPTION_66/effective-charter-reference.json'),'NO_EXTERNAL_RESOURCE_PERMISSIONS_CREATED':True})
explicit=['systemd service execution','sudo or privilege escalation','Bubblewrap execution','Package86 system-level probe','actual H77-02 probe','actual A15 execution or capture','native Planner runtime or V3 changes','frozen acceptance or historical evidence modification','production or external-system effects','automatic retries or additional campaigns','grant self-issuance']
body={'SCHEMA':'BOOTSTRAP-REPAIR-ISSUED-GRANT-94-1','WORK_PACKAGE':WP,'INSTRUMENT_STATUS':'ISSUED_PENDING_SEPARATE_EFFECTIVENESS_REFERENCE','APPROVED_SUBJECT_IDENTITY':subject['IDENTITY'],'APPROVED_SUBJECT_PIN':pin(P93/'proposed-repair-authorization-subject.json'),'ISSUER_ROLE':s['ISSUER_ROLE'],'GOVERNING_CHARTER_IDENTITY':s['EFFECTIVE_CHARTER'],'EFFECTIVE_CHARTER_LIFECYCLE':s['EFFECTIVE_LIFECYCLE'],'ISSUER_AUTHORITY_EVIDENCE_PIN':pin(OUT/'effective-governance-verification.json'),'PROJECT_OWNER_DECISION_EVIDENCE':{'IDENTITY':decision['IDENTITY'],'PIN':pin(OUT/'project-owner-decision-provenance.json')},'EXISTING_PACKAGE90_GRANT':s['EFFECTIVE_PACKAGE90_GRANT'],'EXACT_SOURCE_ALLOWLIST':s['SOURCE_ALLOWLIST'],'PRIOR_SOURCE_IDENTITIES':s['CURRENT_SOURCE_PINS'],'ROOT_ENTRY_MAX_BYTES':207444,'ORDINARY_RECORD_MAX_BYTES':65536,'ROOT_ENTRY_SCHEMA':s['ROOT_ENTRY_SCHEMA'],'MAX_JSON_NODES':s['MAX_JSON_NODES'],'MAX_JSON_DEPTH':s['MAX_JSON_DEPTH'],'RESOURCE_LIMITS':s['RESOURCE_LIMITS'],'RESOURCE_LIMITS_UNCHANGED':True,'PARENT_ROOT_INPUT_EXCEPTION':s['PARENT_ROOT_INPUT_EXCEPTION'],'PREFERRED_REPAIR':s['PREFERRED_REPAIR'],'PERMITTED_REPAIR_OPERATIONS':s['PERMITTED_OPERATIONS'],'PERMITTED_STATIC_VERIFICATION':['exact approved source scope and identities','AST/JSON encoder and schema/size reconstruction without target execution','independent full oracle/observer comparison reconstruction','preservation and four-seed static negatives'],'SOURCE_AND_ORACLE_REQUIREMENTS':s['EVIDENCE_PINS'],'SYNTHETIC_TEST_SCOPE':s['SYNTHETIC_TEST_SCOPE'],'TEST_ENTRY_PREDICATES':s['ENTRY_PREDICATES']['active_inert'],'CONSTRUCTION_ENTRY_PREDICATES':s['ENTRY_PREDICATES']['construction'],'ACTIVE_TEST_ADDITIONAL_GUARD':['exact repaired executable and dependency identity','independently sealed exact runtime fixtures and oracles','verified environment and store controls','enforceable unchanged resource limits','qualified independent observer','exact campaign entry and still-available one-campaign permission','applicable combined active-test authority','no real probe execution path'],'OUTPUT_EVIDENCE_BOUNDARY':s['OUTPUT_EVIDENCE_BOUNDARY'],'NO_RETRY_POLICY':0,'HISTORICAL_EXCLUSIONS':s['HISTORICAL_EXCLUSIONS'],'PROHIBITED_OPERATIONS':s['PROHIBITED_OPERATIONS'],'EXPLICIT_PACKAGE94_EXCLUSIONS':explicit,'EFFECTIVE_BOUNDARY':{'RULE':'Only after authenticated owner selection, exclusive durable publication, independent reread, four-seed agreement, all negatives and preservation audit, followed by a separate exclusively published effectiveness reference. Fresh construction and active-test entry predicates remain independent.','NO_BACKDATING':True,'SOURCE_REPAIR_PERFORMED_BY_ISSUANCE':False,'ACTIVE_TESTING_AUTHORIZED_AUTOMATICALLY':False},'REVOCATION_RULE':{'RULE':'Project-owner explicit revocation/supersession makes future entry fail closed; unknown/currentness mismatch denies. Already consumed campaign/attempt never reopens.','EXPIRATION_DATE':None,'NO_UNBOUNDED_SCOPE_INFERRED':True},'EXISTING_GRANTS_AMENDED_IN_PLACE':False,'SCOPE_EXPANSION_ALLOWED':False,'ROOT_EXCEPTION_ENLARGES_ORDINARY_RECORDS':False,'CAMPAIGN_STARTED_BY_ISSUANCE':False,'A15_EXECUTION_GRANT':None,'A15_CAPTURE_GRANT':None,'REAL_PROBE_GRANT':None,'PREDECESSOR_REPAIR_GRANT':None,'IDENTITY_RULE':'canonical sorted compact UTF8 CONTENT; own wrapper and future effectiveness/verification/source/test identities excluded. Issued identity reconstructed from actual persisted content.'}
envelope={'CONTENT':body,'IDENTITY':aid(body,'qualification-bootstrap-entry-oracle-repair-issued-grant-v1')}
save('grant-candidate.json',envelope)
save('grant-record-binding.json',{'GRANT_IDENTITY':envelope['IDENTITY'],'FUTURE_RECORD_PATH':str((OUT/('issued-bootstrap-repair-grant-'+envelope['IDENTITY']['sha256']+'.json')).relative_to(ROOT)),'NO_IDENTITY_INVENTED':True,'REQUIRES_INDEPENDENT_PERSISTED_RECONSTRUCTION':True})
print('EXACT_AUTHENTICATION_PASS; CANDIDATE_PREPARED_NOT_PUBLISHED',envelope['IDENTITY'])
